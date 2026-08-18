# Electronic-Structure Code File I/O

Deeper detail for [../SKILL.md](../SKILL.md). Covers reading/writing DFT-code-specific input/output
files and extracting electronic-structure results (band structure, density of states) — the file
format layer that `computational-materials/references/dft.md` assumes.

## VASP input file generation

```python
from pymatgen.io.vasp.sets import MPRelaxSet

vasp_input_set = MPRelaxSet(structure)   # Materials-Project-consistent default parameters
vasp_input_set.write_input("vasp_calculation_dir")   # writes INCAR, POSCAR, POTCAR, KPOINTS
```

## VASP output parsing

```python
from pymatgen.io.vasp.outputs import Vasprun

vasprun = Vasprun("vasprun.xml")
final_energy = vasprun.final_energy
final_structure = vasprun.final_structure
converged = vasprun.converged   # check before trusting any extracted result — see pitfalls

band_structure = vasprun.get_band_structure()
dos = vasprun.complete_dos
```

## Band structure and DOS extraction/plotting

```python
from pymatgen.electronic_structure.plotter import BSPlotter, DosPlotter

bs_plotter = BSPlotter(band_structure)
bs_plotter.get_plot()

band_gap_info = band_structure.get_band_gap()   # dict with 'energy', 'direct' (bool), 'transition'

dos_plotter = DosPlotter()
dos_plotter.add_dos("Total DOS", dos)
dos_plotter.get_plot()
```

## Quantum Espresso I/O (a second common DFT code)

```python
from pymatgen.io.pwscf import PWInput

pw_input = PWInput(structure, pseudo={"Fe": "Fe.pbe-spn-kjpaw_psl.1.0.0.UPF", "O": "O.pbe-n-kjpaw_psl.1.0.0.UPF"})
pw_input.write_file("pw.in")
```

## Validation & Pitfalls

Canonical reference: Ong et al. (2013) for pymatgen's I/O module scope; VASP and Quantum Espresso's
own documentation for code-specific file format details, which change across versions.

- **`vasprun.converged` (or the equivalent convergence check for other codes) must be checked before
  trusting any extracted energy, structure, or electronic property** — parsing succeeds even for a
  non-converged or crashed calculation's partial output; an unchecked convergence flag is the single
  most common way a bad calculation's results get silently used downstream.
- **Default input-generation parameter sets (like `MPRelaxSet`) encode specific convergence and
  methodology choices (functional, k-point density, energy cutoff) matched to a particular database's
  conventions (Materials Project's, in this case)** — using them without understanding what they
  specify means inheriting those conventions' assumptions, which may not be appropriate for every
  research question (e.g. a system needing a different functional for correct physics — see
  `computational-materials/references/dft.md`).
- **Band gap `direct`/`indirect` classification and the reported gap value depend on the k-point mesh
  actually sampled** — a coarse k-mesh can miss the true band extrema location, misreporting an
  indirect gap as direct (or the wrong gap value entirely); confirm k-point density is adequate for
  band-structure-sensitive claims, not just for total-energy convergence.
- **DFT-computed band gaps are systematically underestimated relative to experiment for standard
  functionals (GGA/PBE)** — this is a well-known, methodology-inherent limitation (the "band gap
  problem"), not a calculation error; don't compare a standard-DFT band gap directly against an
  experimental value without accounting for this, or use a corrected method (hybrid functional, GW)
  when accurate absolute gap values matter.
