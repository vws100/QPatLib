# qasm_to_graphix.py
"""
OpenQASM 3 -> Graphix **Circuit** importer (no transpile)
=========================================================

This utility reads an OpenQASM 3 program (string or file), and constructs a
**Graphix `Circuit`** while preserving QASM `input float ...` variables as
Graphix `Placeholder`s. It **does not** create a Pattern; you decide when (or if)
to call `circuit.transpile().pattern` later.

**Parameter renaming**: identifiers of the form ``_c_0_``, ``_c_1_``, ... are
normalized to ``c[0]``, ``c[1]``, ... in the Graphix Circuit and any later
pattern printouts.

Design notes
------------
- Parsing uses the OpenQASM 3 reference Python front-end (`openqasm3.parse`),
  which expects program **text**. A convenience loader for `Path` is provided.
- The OpenQASM 3 AST exposes `IODeclaration(io_identifier: IOKeyword, ...)` and
  gate operands as `IndexedIdentifier` with index elements that are either
  `DiscreteSet` or a list of expressions/ranges; both forms for `q[<int>]` are
  handled here.
- Gate arguments are evaluated with enum operators (`BinaryOperator`,
  `UnaryOperator`), including `**`.

Installation
------------
- `pip install openqasm3`  (ensure the "[parser]" extra is installed if needed)
- `pip install graphix`

Gate set implemented
--------------------
`rz, h, s, x, y, z, cx, swap`  — `s` uses `circuit.s(i)` if available, or
fallback to `rz(pi/2)` otherwise.

"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple
import math
import re

# Runtime imports (present in the user's environment)
import openqasm3
import openqasm3.ast as qast

from graphix import Circuit
from graphix.parameter import Placeholder

__all__ = [
    "build_graphix_from_qasm",
    "load_circuit_from_qasm_path",
    "QasmImportResult",
    "format_angle_compact",
    "circuit_to_compact_string",
]


@dataclass
class QasmImportResult:
    """Container for the result of importing a QASM program.

    Attributes
    ----------
    circuit : Circuit
        The Graphix circuit constructed from the QASM program.
    placeholders : Dict[str, Placeholder]
        Mapping from *normalized* name -> Graphix Placeholder. For names of the
        form ``_c_k_`` we normalize to ``c[k]``.
    """
    circuit: Circuit
    placeholders: Dict[str, Placeholder]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_C_RE = re.compile(r"^_c_(\d+)_$")

def _normalize_param_name(name: str) -> str:
    """Map OpenQASM identifiers like ``_c_7_`` -> ``c[7]``; leave others as is."""
    m = _C_RE.match(name)
    if m:
        return f"c[{int(m.group(1))}]"
    return name


def _eval_number_expr(expr) -> int | float:
    """Evaluate a numeric AST node (int/float literals or simple arithmetic).

    Used only for sizes like `qubit[16] q;` — minimal support.
    """
    if expr is None:
        return 0
    if isinstance(expr, qast.IntegerLiteral):
        return int(expr.value)
    if isinstance(expr, qast.FloatLiteral):
        return float(expr.value)
    if isinstance(expr, qast.BinaryExpression):
        l = _eval_number_expr(expr.lhs)
        r = _eval_number_expr(expr.rhs)
        op = expr.op
        if op == qast.BinaryOperator["+"]:
            return l + r
        if op == qast.BinaryOperator["-"]:
            return l - r
        if op == qast.BinaryOperator["*"]:
            return l * r
        if op == qast.BinaryOperator["/"]:
            return l / r
        if op == qast.BinaryOperator["%"]:
            return l % r
        if op == qast.BinaryOperator["**"]:
            return l ** r
    if isinstance(expr, qast.Identifier) and expr.name == "pi":
        return math.pi
    raise NotImplementedError(f"Unsupported numeric expression for size: {type(expr).__name__}")


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------

def build_graphix_from_qasm(qasm_src: str) -> Tuple[Circuit, Dict[str, Placeholder]]:
    """Parse OpenQASM 3 text and build a Graphix **Circuit**.

    Parameters
    ----------
    qasm_src : str
        The OpenQASM 3 program **as a string**.

    Returns
    -------
    (circuit, placeholders)
        A Graphix `Circuit` and a dict mapping *normalized* identifiers (e.g.,
        ``c[0]``) to Graphix `Placeholder`s.  **No** pattern is created here.
    """
    # 1) Parse to AST
    mod = openqasm3.parse(qasm_src)

    placeholders: Dict[str, Placeholder] = {}
    alias_map: Dict[str, Placeholder] = {}   # original_name -> Placeholder
    nqubits: int | None = None

    # 2) First pass: qubit declaration + input floats -> Placeholders
    for stmt in mod.statements:
        if isinstance(stmt, qast.QubitDeclaration):
            size_expr = stmt.size
            nqubits = int(_eval_number_expr(size_expr)) if size_expr is not None else 1
        elif isinstance(stmt, qast.IODeclaration):
            io_kw = getattr(stmt, "io_identifier", None) or getattr(stmt, "direction", None)
            ty    = getattr(stmt, "type", None) or getattr(stmt, "ty", None)
            if io_kw == qast.IOKeyword.input and isinstance(ty, qast.FloatType):
                orig = stmt.identifier.name
                newn = _normalize_param_name(orig)
                ph   = Placeholder(newn)
                placeholders[newn] = ph
                alias_map[orig] = ph
                alias_map[newn] = ph

    if nqubits is None:
        raise ValueError("No 'qubit[...]' declaration found in the QASM source.")

    circ = Circuit(nqubits)

    # 3) Expression evaluator: handles Enum operators (+, -, *, /, %, **)
    bin_map = {
        qast.BinaryOperator["+"]:  lambda a, b: a + b,
        qast.BinaryOperator["-"]:  lambda a, b: a - b,
        qast.BinaryOperator["*"]:  lambda a, b: a * b,
        qast.BinaryOperator["/"]:  lambda a, b: a / b,
        qast.BinaryOperator["%"]:  lambda a, b: a % b,
        qast.BinaryOperator["**"]: lambda a, b: a ** b,
    }

    def eval_expr(expr):
        if isinstance(expr, qast.BinaryExpression):
            l = eval_expr(expr.lhs)
            r = eval_expr(expr.rhs)
            op = expr.op
            if op in bin_map:
                return bin_map[op](l, r)
            raise NotImplementedError(f"Unsupported binary op {op!r}")
        if isinstance(expr, qast.UnaryExpression):
            v = eval_expr(expr.expression)
            if expr.op == qast.UnaryOperator["-"]:
                return -v
            if expr.op in (qast.UnaryOperator["~"], qast.UnaryOperator["!"]):
                raise NotImplementedError("Bitwise/logical unary ops are not supported in angles.")
            return v
        if isinstance(expr, qast.Identifier):
            name = expr.name
            if name == "pi":
                return math.pi
            if name in alias_map:
                return alias_map[name]
            raise KeyError(f"Unknown identifier {name!r}")
        if isinstance(expr, qast.FloatLiteral):
            return float(expr.value)
        if isinstance(expr, qast.IntegerLiteral):
            return int(expr.value)
        raise NotImplementedError(f"Unsupported expression type: {type(expr).__name__}")

    # 4) Robust qubit index extraction
    def qubit_index(qref) -> int:
        if isinstance(qref, qast.IndexedIdentifier):
            if not qref.indices:
                raise ValueError("IndexedIdentifier has no indices.")
            idx_elem = qref.indices[0]

            if isinstance(idx_elem, qast.DiscreteSet):
                if len(idx_elem.values) != 1:
                    raise NotImplementedError("q[{i,j}] (multi-value) is not supported.")
                return int(eval_expr(idx_elem.values[0]))

            if isinstance(idx_elem, list):
                if len(idx_elem) == 1:
                    item = idx_elem[0]
                    if isinstance(item, (qast.IntegerLiteral, qast.FloatLiteral, qast.Identifier, qast.BinaryExpression, qast.UnaryExpression)):
                        return int(eval_expr(item))
                    if isinstance(item, qast.RangeDefinition):
                        if item.start is not None and item.end is None and item.step is None:
                            return int(eval_expr(item.start))
                        raise NotImplementedError("Slice indices like q[1:4] not yet supported.")
                raise NotImplementedError("Only single-element index lists like q[14] are supported.")

            if isinstance(idx_elem, qast.IndexExpression):
                el = idx_elem.index
                if isinstance(el, qast.DiscreteSet) and len(el.values) == 1:
                    return int(eval_expr(el.values[0]))
                if isinstance(el, list) and len(el) == 1:
                    return int(eval_expr(el[0]))
                raise NotImplementedError("Complex index expression not supported.")

            raise TypeError(f"Unexpected index node type: {type(idx_elem).__name__}")

        elif isinstance(qref, qast.Identifier):
            raise ValueError(f"Expected q[<i>], got bare identifier {qref.name!r}.")
        else:
            raise TypeError(f"Unexpected qubit node type: {type(qref).__name__}")

    # 5) Translate gates to Graphix Circuit
    for stmt in mod.statements:
        if isinstance(stmt, qast.QuantumGate):
            gate = stmt.name.name.lower()
            args = [eval_expr(a) for a in (stmt.arguments or [])]
            qbs  = [qubit_index(q) for q in stmt.qubits]

            if gate in ("cx", "cnot"):
                circ.cnot(qbs[0], qbs[1])
            elif gate == "swap":
                circ.swap(qbs[0], qbs[1])
            elif gate == "rz":
                circ.rz(qbs[0], args[0])
            elif gate == "h":
                circ.h(qbs[0])
            elif gate == "s":
                if hasattr(circ, "s"):
                    circ.s(qbs[0])
                else:
                    circ.rz(qbs[0], math.pi / 2)
            elif gate == "x":
                circ.x(qbs[0])
            elif gate == "y":
                circ.y(qbs[0])
            elif gate == "z":
                circ.z(qbs[0])
            else:
                raise NotImplementedError(f"Gate {gate!r} not implemented in importer.")

    return circ, placeholders


def load_circuit_from_qasm_path(path: Path) -> Tuple[Circuit, Dict[str, Placeholder]]:
    """Read a QASM file from disk and build a Graphix **Circuit**.

    Returns (circuit, placeholders)."""
    if not path.is_file():
        raise FileNotFoundError(path)
    qasm_text = path.read_text(encoding="utf-8")
    return build_graphix_from_qasm(qasm_text)


# ---------------------------------------------------------------------------
# Compact formatting helpers (no trailing "+ 0.0"; cleaner coeffs)
# ---------------------------------------------------------------------------

def _strip_trailing_zeros(x: float, *, tol: float = 1e-12) -> str:
    if abs(x) < tol:
        return "0"
    if abs(x - int(round(x))) < tol:
        return str(int(round(x)))
    return f"{x:.12g}"


def format_angle_compact(expr) -> str:
    """Format Graphix angle (float or AffineExpression) without adding a "+ 0.0".
    If coeff == 1 -> `x`; coeff == -1 -> `-x`; omit zero offsets.
    """
    try:
        from graphix.parameter import AffineExpression
    except Exception:
        AffineExpression = tuple()  # type: ignore

    if isinstance(expr, (int, float)):
        return _strip_trailing_zeros(float(expr))

    if hasattr(expr, 'a') and hasattr(expr, 'b') and hasattr(expr, 'x'):
        a = float(expr.a)
        b = float(expr.b)
        x = expr.x
        xname = getattr(x, 'name', str(x))
        if abs(a - 1.0) < 1e-12:
            coeff = ''
        elif abs(a + 1.0) < 1e-12:
            coeff = '-'
        else:
            coeff = _strip_trailing_zeros(a) + ' * '
        if abs(b) < 1e-12:
            return f"{coeff}{xname}" if coeff else f"{xname}"
        sign = '+' if b > 0 else '-'
        b_str = _strip_trailing_zeros(abs(b))
        return f"{coeff}{xname} {sign} {b_str}"

    return str(expr)


def circuit_to_compact_string(circuit) -> str:
    """Render a Graphix Circuit similar to its repr but with compact angle formatting.
    This avoids showing "+ 0.0" in affine angles.
    """
    items = []
    for instr in getattr(circuit, 'instruction', []):
        k = getattr(getattr(instr, 'kind', None), 'name', instr.__class__.__name__).upper()
        if k in ('CNOT', 'CX') and hasattr(instr, 'control') and hasattr(instr, 'target'):
            items.append(f"CNOT({instr.control}, {instr.target})")
        elif k == 'RZ' and hasattr(instr, 'target') and hasattr(instr, 'angle'):
            items.append(f"RZ({instr.target}, {format_angle_compact(instr.angle)})")
        elif k == 'RX' and hasattr(instr, 'target') and hasattr(instr, 'angle'):
            items.append(f"RX({instr.target}, {format_angle_compact(instr.angle)})")
        elif k == 'RY' and hasattr(instr, 'target') and hasattr(instr, 'angle'):
            items.append(f"RY({instr.target}, {format_angle_compact(instr.angle)})")
        elif k in ('H','S','X','Y','Z') and hasattr(instr, 'target'):
            items.append(f"{k}({instr.target})")
        elif k == 'SWAP' and hasattr(instr, 'targets'):
            try:
                a, b = instr.targets
                items.append(f"SWAP({a}, {b})")
            except Exception:
                items.append(repr(instr))
        else:
            items.append(repr(instr))
    return f"Circuit(width={circuit.width}, instr=[{', '.join(items)}])"


# ---------------------------------------------------------------------------
# CLI (optional) — never transpiles unless you call transpile() yourself
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="OpenQASM3 -> Graphix Circuit importer (no transpile)")
    ap.add_argument("qasm_file", type=Path, help="Path to .qasm file")
    ap.add_argument("--summary", action="store_true", help="Print a short circuit summary")
    ap.add_argument("--compact", action="store_true", help="Use compact circuit printing (no + 0.0)")
    args = ap.parse_args()

    circuit, params = load_circuit_from_qasm_path(args.qasm_file)

    if args.summary:
        if args.compact:
            print(circuit_to_compact_string(circuit))
        else:
            print(circuit)
        print(f"Qubits (width): {circuit.width}")
        print(f"Placeholders: {sorted(params.keys())}")
