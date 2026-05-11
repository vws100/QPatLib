# Contributing to QPatLib

Thank you for contributing to **QPatLib**. This project is designed to maximize **correct attribution and citations** for pattern contributors while keeping GitHub lightweight and runnable.

## Guiding principles

1. **GitHub stores code and documentation only.**
   - Generated circuits and patterns are **NOT** committed to GitHub.
   - Output directories are ignored via `.gitignore`.

2. **Zenodo stores citable patterns or pattern sets.**
   - Each contributed pattern (or pattern set) should be uploaded to the **QPatLib Zenodo community**:
     https://zenodo.org/communities/qpatlib/
   - The Zenodo record is the authoritative artifact for citation and credit.

3. **Circuits are local by default.**
   - Users working on this specific code set generate circuits locally using the notebooks/scripts in:
     `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Circuit_Code/`
   - The repository does **not** download circuits from Zenodo.
   - Circuits may be uploaded to Zenodo as a ZIP for reference/validation.

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

## Contributor credit rules

### Credit for patterns is defined by the Zenodo record metadata
To ensure contributors receive academic credit:

- The **Creators** listed on the Zenodo record are the credited contributors.
- Contributors should include **ORCID** identifiers when possible.
- If a contribution is collaborative, list all appropriate creators on the Zenodo record.

---

## What to contribute

- New MBQC patterns (JSON plus the corresponding OpenQASM 3 circuit).
- Improvements to circuit-generation or pattern-generation code.
- Validation tooling, tests, documentation, examples.

---

## Uploading patterns to Zenodo

1. Prepare a pattern bundle directory containing at least:
   - Pattern JSON output in standard format 
   - the associated OpenQASM 3 circuit file(s)
   - minimal metadata (recommended):
     - pattern identifier
     - creator(s) + ORCID(s)
     - generation parameters (e.g., coloring strategy)
     - code version / commit hash used to generate it

2. Upload the bundle to Zenodo as a **new record**.
3. Add it to the **QPatLib** Zenodo community:
   https://zenodo.org/communities/qpatlib/
4. Publish the record and obtain the **DOI**.

(Optional) Open a GitHub issue/PR that links the pattern DOI so we can reference it in documentation/catalog.

---

## Pull requests (code and docs)

### Before submitting
- Keep generated data out of GitHub.
- Ensure outputs go into ignored directories (see `.gitignore`).

### PR checklist
- [ ] No generated circuit output directories included (`qasm_circuit_files_*`)
- [ ] No generated pattern output directories included (`json_output_pattern_*`)
- [ ] Documentation updated if behavior changes

---

## Code of conduct
Be respectful, constructive, and collaborative.
