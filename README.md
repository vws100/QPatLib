# QPatLib — A community repository of MBQC patterns

QPatLib is a community repository for **measurement-based quantum computing (MBQC) patterns** and supporting tooling.

**Project policy**

- **GitHub hosts code + documentation only** (not the generated circuit/pattern artifacts).
- Users generate **circuits locally**, then generate **patterns locally** from those circuits.
- Generated output folders are intentionally **not tracked** and are ignored via `.gitignore`.
- **Patterns are uploaded manually to Zenodo** in the QPatLib Zenodo community.

GitHub repo: https://github.com/vws100/QPatLib
Zenodo community: https://zenodo.org/communities/qpatlib/

---

## Repository layout

The notebooks/scripts live in subdirectories, e.g., :

- Circuits: `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Circuit_Code/`
- Patterns (Graphix): `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Graphix_Patterns/`

Generated outputs (ignored by git):

- Circuits: `qasm_circuit_files_*` and `full_circuit_files_*` under `Circuit_Code/`
- Patterns: `json_output_pattern_*` under `Graphix_Patterns/`

---

## QuickStart

See **[QUICKSTART.md](QUICKSTART.md)** for step-by-step instructions using **absolute paths**.

---

## How to cite (A–C)

### (A) If you use a specific pattern
Cite the **pattern's Zenodo DOI** (each pattern is a separate Zenodo record):

- **Per-pattern DOI:** `xxx`

### (B) If you use QPatLib code/tooling (this repository)
Cite the **QPatLib repository DOI** minted by Zenodo for the GitHub repository:

- **QPatLib repository DOI: 10.5281/zenodo.20114340

> Tip: Use the Zenodo **concept DOI** as the single stable project DOI; use a Zenodo **version DOI** if you need strict reproducibility.

### (C) If you use both a pattern and the tooling
Cite **both**:

- the **pattern DOI**, and
- the **QPatLib repository DOI**.

---

## Placement instructions (important)

Keep these files at the **top level** of the GitHub repository (repo root):

- `README.md` (this file)
- `QUICKSTART.md`
- `LICENSE` (MIT)
- `CITATION.cff`
- `CONTRIBUTING.md`
- `requirements.txt`
- `pyproject.toml`
- `.gitignore`

Notebooks/scripts should be placed under relevant subdirectories, e.g.,:

- `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Circuit_Code/`
- `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Graphix_Patterns/`
