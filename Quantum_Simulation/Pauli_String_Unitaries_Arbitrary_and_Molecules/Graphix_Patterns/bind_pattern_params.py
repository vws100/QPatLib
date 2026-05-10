# bind_pattern_params.py
"""
Bind (instantiate) Graphix Pattern parameters `c[0]`, `c[1]`, ... with numbers.

Works with Graphix 0.3.x. It collects the *actual* Placeholder objects from the
final Pattern and replaces them by object identity, ensuring TensorNetwork
backend receives numeric angles only.

Public API
----------
- bind_pattern_by_names(pattern, {'c[i]': value, ...}, verify=True) -> pattern
- bind_pattern(pattern, {Placeholder: value}, verify=True) -> pattern
- collect_placeholders(pattern) -> {'c[i]': Placeholder}
- find_parameterized_angles(pattern) -> iterator of (node, angle)

This module **does not import graphix** at import time; it relies on the
runtime shape of objects exposed by graphix 0.3.x.
"""
from __future__ import annotations
from typing import Dict, Mapping, Iterable, Tuple, Any

# ---- internal helpers -------------------------------------------------------

def _is_measurement(cmd: Any) -> bool:
    kind = getattr(cmd, "kind", None)
    name = getattr(kind, "name", None)
    return name == "M"


def _iter_measure_angles(pattern: Any) -> Iterable[Tuple[Any, Any]]:
    for cmd in pattern:  # Pattern.__iter__ -> commands
        if _is_measurement(cmd):
            yield cmd, getattr(cmd, "angle", 0)

# ---- public helpers ---------------------------------------------------------

def collect_placeholders(pattern: Any) -> Dict[str, Any]:
    """Return {'c[i]': Placeholder(...)} found in measurement angles of *pattern*."""
    name_to_placeholder: Dict[str, Any] = {}
    for _, angle in _iter_measure_angles(pattern):
        if hasattr(angle, "x"):
            ph = angle.x  # Graphix Placeholder
            name_to_placeholder[getattr(ph, "name", str(ph))] = ph
        elif hasattr(angle, "xreplace") and not isinstance(angle, (int, float)):
            # Non-affine expression; not common in current flows. Left as-is.
            pass
    return name_to_placeholder


def build_assignment_from_names(pattern: Any, name_to_value: Mapping[str, float]) -> Dict[Any, float]:
    """Return {Placeholder: float} using placeholders *from pattern* by name."""
    ph_by_name = collect_placeholders(pattern)
    assignment: Dict[Any, float] = {}
    for name, value in name_to_value.items():
        ph = ph_by_name.get(name)
        if ph is not None:
            assignment[ph] = float(value)
    return assignment


def bind_pattern(pattern: Any, assignment: Mapping[Any, float], *, verify: bool = True):
    """Bind placeholders across *pattern* using {Placeholder: number} mapping.

    Returns a new Pattern (Graphix's xreplace preserves immutability of inputs).
    If *verify* is True, raise ValueError if any parameter expression remains.
    """
    if not assignment:
        return pattern
    p_bound = pattern.xreplace(dict(assignment))
    if verify:
        leftover = list(find_parameterized_angles(p_bound))
        if leftover:
            preview = ", ".join(f"node={n}, angle={a}" for n, a in leftover[:5])
            raise ValueError(
                "Unbound parameter expressions remain in the pattern after replacement: "
                f"{preview}"
            )
    return p_bound


def bind_pattern_by_names(pattern: Any, name_to_value: Mapping[str, float] | list[float] | tuple[float, ...], *, verify: bool = True):
    """Bind by names or by a list of values (index -> c[index]).

    Examples
    --------
    bind_pattern_by_names(p, {'c[0]': 0.5, 'c[3]': 1.2})
    bind_pattern_by_names(p, [0.5, 0.0, 0.0, 1.2])
    """
    if not isinstance(name_to_value, dict):
        # Treat as a sequence: index -> c[index]
        name_to_value = {f"c[{i}]": float(v) for i, v in enumerate(name_to_value)}
    assignment = build_assignment_from_names(pattern, name_to_value)
    return bind_pattern(pattern, assignment, verify=verify)


def find_parameterized_angles(pattern: Any):
    """Iterate (node, angle) for measurement angles that still look parameterized."""
    for cmd, angle in _iter_measure_angles(pattern):
        if hasattr(angle, "x"):
            yield (getattr(cmd, "node", None), angle)
        elif hasattr(angle, "xreplace") and not isinstance(angle, (int, float)):
            yield (getattr(cmd, "node", None), angle)

__all__ = [
    "collect_placeholders",
    "build_assignment_from_names",
    "bind_pattern",
    "bind_pattern_by_names",
    "find_parameterized_angles",
]
