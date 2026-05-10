# QUICKSTART — QPatLib (absolute-path workflow)

This QuickStart follows the intended local workflow:

1. **Generate circuits locally** (OpenQASM 3 outputs)
2. **Generate MBQC patterns locally** (Graphix JSON outputs) from those circuits
3. **Upload patterns manually to Zenodo** (one DOI per pattern)

Generated outputs are intentionally **not tracked** and are ignored via `.gitignore`. citeturn9search38turn9search42

---

## 0) Prerequisites

- Python 3.10+ recommended
- Clone the repository:

```bash
git clone https://github.com/vws100/QPatLib.git
cd QPatLib
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

(Optionally, if/when you package code under `src/`, you can use `pip install -e .`.)

---

## 1) Set absolute paths (recommended)

Because you want an **absolute-path** workflow, set a single absolute project root at the top of each notebook.

### Option A (simplest): define `QPATLIB_ROOT` manually

In the first cell of each notebook:

```python
from pathlib import Path

# EDIT THIS to your local clone location
QPATLIB_ROOT = Path(r"/ABSOLUTE/PATH/TO/QPatLib").resolve()

CIRCUIT_CODE_DIR = QPATLIB_ROOT / "Quantum_Simulation" / "Pauli_String_Unitaries_Arbitrary_and_Molecules" / "Circuit_Code"
GRAPHIX_PATTERNS_DIR = QPATLIB_ROOT / "Quantum_Simulation" / "Pauli_String_Unitaries_Arbitrary_and_Molecules" / "Graphix_Patterns"
```

### Option B: environment variable (more portable)

Set an environment variable once:

```bash
export QPATLIB_ROOT=/ABSOLUTE/PATH/TO/QPatLib
```

Then in notebooks:

```python
import os
from pathlib import Path

QPATLIB_ROOT = Path(os.environ["QPATLIB_ROOT"]).resolve()
CIRCUIT_CODE_DIR = QPATLIB_ROOT / "Quantum_Simulation" / "Pauli_String_Unitaries_Arbitrary_and_Molecules" / "Circuit_Code"
GRAPHIX_PATTERNS_DIR = QPATLIB_ROOT / "Quantum_Simulation" / "Pauli_String_Unitaries_Arbitrary_and_Molecules" / "Graphix_Patterns"
```

---

## 2) Generate circuits locally

Run the circuit-generation notebook(s) in:

- `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Circuit_Code/`

### Output directories (kept local; ignored)

Your circuit pipeline should write outputs **only** under `Circuit_Code/` into subdirectories with names:

- `qasm_circuit_files_.../`
- `full_circuit_files_.../`

These directories are ignored by `.gitignore` and will not be pushed to GitHub. citeturn9search38turn9search42

### Suggested absolute-path output roots

In your circuit notebook, set:

```python
from pathlib import Path

DIR_PATH_STORAGE = CIRCUIT_CODE_DIR / f"qasm_circuit_files_{NAME_TO_FIND}_{COLORING_STRATEGY}"
DIR_PATH_STORAGE.mkdir(parents=True, exist_ok=True)
```

(and similarly for `full_circuit_files_...`).

---

## 3) Generate patterns locally (Graphix)

Run the pattern-generation notebook(s) in:

- `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Graphix_Patterns/`

### Read circuits from local outputs (absolute path)

In the pattern notebook, point the input circuits directory to the **absolute** path created above, e.g.:

```python
CIRCUITS_ROOT = CIRCUIT_CODE_DIR / f"qasm_circuit_files_{NAME_TO_FIND}_{COLORING_STRATEGY}"
```

### Output directories (kept local; ignored)

Your pattern pipeline should write patterns under `Graphix_Patterns/` into subdirectories with names:

- `json_output_pattern_.../`

These directories are ignored by `.gitignore` and will not be pushed to GitHub. citeturn9search38turn9search42

Suggested absolute-path output root:

```python
PATTERN_OUT = GRAPHIX_PATTERNS_DIR / f"json_output_pattern_{NAME_TO_FIND}_{COLORING_STRATEGY}"
PATTERN_OUT.mkdir(parents=True, exist_ok=True)
```

---

## 4) Upload patterns to Zenodo (manual; per-pattern DOI)

To contribute a pattern to QPatLib:

1. Prepare a pattern bundle directory containing at least:
   - Graphix pattern JSON output
   - the associated OpenQASM 3 circuit file(s)
   - minimal metadata (pattern identifier, creator(s), parameters, and code version/commit hash)
2. Upload the bundle as a **new Zenodo record**.
3. Add it to the **QPatLib Zenodo community**:
   https://zenodo.org/communities/qpatlib/
4. Publish the record and obtain the **per-pattern DOI**.

---

## 5) (Optional) Archive circuits ZIP on Zenodo (reference only)

You may upload the locally generated circuit corpus as a ZIP file to Zenodo for reference/validation. The repository code does **not** download circuits from Zenodo; users are expected to generate circuits locally.

---

## Troubleshooting

### My generated outputs appear in `git status`

- If they are **untracked**, ensure `.gitignore` contains the patterns for the output directories.
- If they were **committed previously**, `.gitignore` will not stop tracking them; you must untrack them from the index. citeturn9search38turn9search39

