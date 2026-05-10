# QPatLib — Pauli String Unitaries (Arbitrary and Molecules)

This folder provides code (Jupyter notebooks / scripts) to generate:

1. **OpenQASM 3 circuits** for commuting subsets of Pauli strings relevant to benchmark Hamiltonians.
2. **Graphix MBQC patterns** generated from those circuits using **measurement-calculus–standard** workflows.

**Project policy:** Generated **circuits** and **patterns** are *not* stored in GitHub. They are generated locally and ignored via `.gitignore`. **Patterns** are uploaded manually to the **Zenodo QPatLib community** as citable records (**one DOI per pattern**).

- GitHub repo: https://github.com/vws100/QPatLib
- Zenodo community: https://zenodo.org/communities/qpatlib/

---

## Repository layout (relevant paths)

Within the QPatLib repository, the intended code layout is:

```
Quantum_Simulation/
  Pauli_String_Unitaries_Arbitrary_and_Molecules/
    Circuit_Code/
      ... notebooks / scripts that generate circuits locally ...
      qasm_circuit_files_*      (generated; ignored)
      full_circuit_files_*      (generated; ignored)
    Pattern_Code/
      ... notebooks / scripts that generate patterns locally ...
      json_output_pattern_*     (generated; ignored)
```

---

## Quickstart (local workflow)

### 1) Generate circuits locally
1. Run the notebook(s) / scripts in:
   `Circuit_Code/`
2. The circuit generator writes QASM3 circuits into local output subdirectories under `Circuit_Code/`.
3. These output folders are ignored by git (see `.gitignore`).

### 2) Generate patterns locally (from locally generated circuits)
1. Run the notebook(s) / scripts in:
   `Pattern_Code/`
2. The pattern generator reads the local circuits produced by `Circuit_Code/`.
3. Patterns are written into local output subdirectories under `Pattern_Code/`.
4. These output folders are ignored by git (see `.gitignore`).

### 3) Upload patterns to Zenodo (manual, per-pattern)
Community users should upload each pattern bundle (Graphix JSON + QASM3 + metadata) as a **separate Zenodo record** in the QPatLib community so each pattern is citable with its own DOI.

> Circuits may also be uploaded to Zenodo as a ZIP for reference/validation, but the code in this repository does **not** fetch circuits from Zenodo. Users should generate circuits locally.

---

## How to cite

### Cite the tooling/index (this repository code)
When the repository is archived on Zenodo via GitHub releases, cite the DOI minted for the corresponding release:

- **QPatLib (tooling/index DOI):** `xxx`

### Cite a pattern (preferred)
Each MBQC pattern is uploaded as its own Zenodo record and should be cited by its **pattern DOI**:

- **Pattern DOI (per-pattern):** `xxx`

**Rule of thumb:** cite the *pattern DOI* whenever you use a specific pattern, and cite the *tooling/index DOI* when you use QPatLib code/tooling.

---

## License

MIT License (see `LICENSE`).
