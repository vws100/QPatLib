# Contributing to QPatLib

Thank you for contributing to **QPatLib**. This project is designed to maximize **correct attribution and citations** for pattern contributors while keeping GitHub lightweight and runnable.

## Guiding principles

1. **GitHub stores code and documentation only.**
   - Generated circuits and patterns are **NOT** committed to GitHub.
   - Output directories are ignored via `.gitignore`.

2. **Zenodo stores citable pattern artifacts (one DOI per pattern).**
   - Each contributed pattern should be uploaded as a **separate Zenodo record** in the **QPatLib Zenodo community**.
   - The Zenodo record is the authoritative artifact for citation.

3. **Circuits are local by default.**
   - Users generate circuits locally using `Circuit_Code/`.
   - The repository does **not** download circuits from Zenodo.
   - Circuits may be uploaded to Zenodo as a ZIP for reference/validation.

---

## Contributor credit rules

### A) Credit for patterns is defined by Zenodo record metadata
To ensure contributors receive academic credit:

- The **Creators** listed on the Zenodo record are the credited contributors.
- Contributors should include **ORCID** identifiers when possible.
- If a contribution is collaborative, list all appropriate creators on the Zenodo record.

### B) How others should cite your contribution
- Users of a specific pattern should cite the **pattern DOI** (Zenodo record DOI).
- Users of the code/tooling should cite the **QPatLib tooling/index DOI** minted via Zenodo for GitHub releases (DOI placeholder: `xxx`).

---

## What to contribute

- Zenodo: New MBQC patterns (Graphix JSON plus the corresponding OpenQASM 3 circuit).
- Github: Improvements to circuit-generation or pattern-generation code.
- Github: Validation tooling, tests, documentation, examples.

---

## Local workflow (generate circuits → generate patterns)

### 1) Generate circuits (local)
Run the notebooks/scripts in:

- `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Circuit_Code/`

**Output:** circuits are written to local output subdirectories under `Circuit_Code/` that are ignored by git.

### 2) Generate patterns (local)
Run the notebooks/scripts in:

- `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Pattern_Code/`

**Input:** reads circuits from the local `Circuit_Code/` output directories.

**Output:** patterns are written to local output subdirectories under `Pattern_Code/` that are ignored by git.

---

## Uploading a pattern to Zenodo (per-pattern DOI)

1. Prepare a **pattern bundle** directory containing at least:
   - Graphix pattern output (JSON)
   - OpenQASM 3 circuit file(s) used to generate it
   - A small metadata file (recommended) describing:
     - pattern identifier
     - creators + ORCIDs
     - generation parameters (e.g., coloring strategy)
     - code version / commit hash used to generate it

2. Upload the bundle to Zenodo as a **new record**.
3. Add it to the **QPatLib community**:
   https://zenodo.org/communities/qpatlib/
4. Publish the record and obtain the **pattern DOI**.
5. (Optional) Open a GitHub issue/PR linking the DOI so we can reference it in documentation/catalog.

---

## Pull requests (code and docs)

### Before submitting
- Keep generated data out of GitHub.
- Ensure outputs go into ignored directories (see `.gitignore`).

### PR checklist
- [ ] No generated circuit output directories included (`qasm_circuit_files_*`, `full_circuit_files_*`)
- [ ] No generated pattern output directories included (`json_output_pattern_*`)
- [ ] Documentation updated if behavior changes

---

## Code of conduct
Be respectful, constructive, and collaborative.
