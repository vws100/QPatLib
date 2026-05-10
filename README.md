# QPatLib — A community repository of MBQC patterns

QPatLib is a community repository for **measurement-based quantum computing (MBQC) patterns** and supporting tooling.

**Project policy**

- **GitHub hosts code + documentation only** (not the generated circuit/pattern artifacts).
- Users generate **circuits locally**, then generate **patterns locally** from those circuits.
- Generated output folders are intentionally **not tracked** and are ignored via `.gitignore`. 
- **Patterns are uploaded manually to Zenodo** (one Zenodo record + DOI per pattern). The Zenodo community is: https://zenodo.org/communities/qpatlib/

GitHub repo: https://github.com/vws100/QPatLib

---

## Repository layout

The notebooks/scripts live here:

- Circuits: `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Circuit_Code/`
- Patterns (Graphix): `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Graphix_Patterns/`

Generated outputs (ignored by git):

- Circuits: `qasm_circuit_files_*` and `full_circuit_files_*` under `Circuit_Code/`
- Patterns: `json_output_pattern_*` under `Graphix_Patterns/`

---

## QuickStart

See **[QUICKSTART.md](QUICKSTART.md)** for step-by-step instructions using **absolute paths**.

---

## How to cite

### Cite the tooling/index (this GitHub repository)

Add `CITATION.cff` at the repository root (already planned/used). GitHub will display a “Cite this repository” UI when `CITATION.cff` is present on the default branch.

When you enable the Zenodo–GitHub integration, each GitHub **Release** is archived on Zenodo and receives a DOI. 

- **QPatLib tooling/index DOI (Zenodo, via GitHub releases):** `xxx`

### Cite a pattern (preferred)

Each pattern should be uploaded as its own Zenodo record and cited using its **per-pattern DOI**.

- **Per-pattern DOI:** `xxx`

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

Notebooks/scripts should be placed under:

- `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Circuit_Code/`
- `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Graphix_Patterns/`
