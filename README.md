# QPatLib — A community repository of MBQC patterns

QPatLib is a community repository for **measurement-based quantum computing (MBQC) patterns** and supporting tooling.

**Project policy**

- **GitHub hosts code + documentation only** (not the generated circuit/pattern artifacts).
- Users generate **circuits locally**, then generate **patterns locally** from those circuits.
- Generated output folders are intentionally **not tracked** and are ignored via `.gitignore`.
- **Patterns are uploaded manually to Zenodo** in the QPatLib Zenodo community.

GitHub repo: https://github.com/vws100/QPatLib

Zenodo community: https://zenodo.org/communities/qpatlib/

QPatLib Paper: https://arxiv.org/abs/2605.12502 

---

## QuickStart

See **[QUICKSTART.md](QUICKSTART.md)** for step-by-step instructions using **absolute paths**.


--

## Workflow (v1.0)

(i) Pauli strings choices: For <6 qubits, all possible strings are chosen.  For 6 or more qubits, strings from benchmark molecules in HamLib are used. 

(ii) We then arrange collections of strings into commuting subsets using NetworkX.

(iii) Each subset is then used to build a single measurement pattern using Graphix.

(iv) Finally, the pattern from each subset is validated and stored in the library.

## Library Format


1. Format: One JSON object per line. The file begins with a header (Hamiltonian-level metadata), may include optional summary/comparison blocks, followed by one entry per commuting subset.

2. Header: Hamiltonian name; instance tag; number of qubits; full list of Pauli-string coefficients and corresponding Pauli terms; subset/coloring strategy; mapping from subset index to commuting Pauli strings; provenance (software versions, backend, flags, seed); global summary statistics (e.g., concatenated depth, global max degree).

3. Summary: Strategy-comparison block(s) that report aggregate pattern statistics for an alternative construction (e.g., total node count, max degree, depth, max edge layer span, and Pauli-measurement counts.)

 4. For each subset:  
  * node number, input/output node lists, max degree, Pauli-X and Pauli-Y measurement counts, number of layers (flow depth), max edge layer span, and a node-to-layer map (e.g., causal-flow layering).
  * pattern ascii with the measurement-calculus string (nodes, edges, measurements with signal dependencies, and byproduct operators) stored as readable ASCII using variables/symbols.



---

## Repository layout

The notebooks/scripts live in subdirectories, e.g., :

- Circuits: `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Circuit_Code/`
- Patterns (Graphix): `Quantum_Simulation/Pauli_String_Unitaries_Arbitrary_and_Molecules/Graphix_Patterns/`

Generated outputs (ignored by git):

- Circuits: `qasm_circuit_files_*` and `full_circuit_files_*` under `Circuit_Code/`
- Patterns: `json_output_pattern_*` under `Graphix_Patterns/`


---

## Citation instructions (A–C)

### (A) If you use a pattern
Cite the pattern's Zenodo DOI and Paper. Each pattern (or set of patterns) is a separate Zenodo record:

- Pattern DOI: [10.5281/zenodo.20115266](https://doi.org/10.5281/zenodo.20115266)
- Paper DOI: [10.48550/arXiv.2605.12502] (https://doi.org/10.48550/arXiv.2605.12502)

### (B) If you use QPatLib code/tooling (this repository)
Cite the QPatLib Paper and repository DOI minted by Zenodo for the GitHub repository:

- QPatLib repository DOI: [10.5281/zenodo.20114339](https://doi.org/10.5281/zenodo.20114339)
- Paper DOI: [10.48550/arXiv.2605.12502] (https://doi.org/10.48550/arXiv.2605.12502)


### (C) If you use both a pattern and the tooling
Cite:

- Pattern DOI: [10.5281/zenodo.20115266](https://doi.org/10.5281/zenodo.20115266)
- QPatLib repository DOI: [10.5281/zenodo.20114339](https://doi.org/10.5281/zenodo.20114339)
- Paper DOI: [10.48550/arXiv.2605.12502] (https://doi.org/10.48550/arXiv.2605.12502)


---

## Placement instructions 

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
