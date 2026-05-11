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

## Citation instructions (A–C)

### (A) If you use a pattern
Cite the **pattern's Zenodo DOI** . Each pattern (or set of patterns) is a separate Zenodo record:

- Pattern DOI: [10.5281/zenodo.20115266](https://doi.org/10.5281/zenodo.20115266) 

### (B) If you use QPatLib code/tooling (this repository)
Cite the **QPatLib repository DOI** minted by Zenodo for the GitHub repository:

- **QPatLib repository DOI:** [10.5281/zenodo.20114339](https://doi.org/10.5281/zenodo.20114339)

### (C) If you use both a pattern and the tooling
Cite **both**:

- the **pattern DOI** [10.5281/zenodo.20115266](https://doi.org/10.5281/zenodo.20115266) 
- the **QPatLib repository DOI**. [10.5281/zenodo.20114339](https://doi.org/10.5281/zenodo.20114339)


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
