---
name: materials-structure-analysis
description: Core structure and composition analysis for materials — reading/writing/manipulating crystal structures, composition handling, symmetry analysis, phase diagram construction, electronic-structure file I/O, and Materials Project database queries. Built primarily around pymatgen, the standard toolkit for this layer. Use this as the foundational data layer that diffraction, computational-materials, and materials-databases all build on.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples target pymatgen 2024.x+ and mp-api 0.4x+. Materials Project queries require a free API key (MP_API_KEY).
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: materials-structure-analysis
---

# Materials Structure and Composition Analysis

## Overview

This is the foundational data layer nearly every other skill in this repo builds on: representing
compositions and crystal structures as objects, converting between file formats, determining
symmetry, constructing phase diagrams from computed energies, reading/writing electronic-structure
code files, and querying public materials databases. pymatgen is the standard tool for all of this —
this skill covers its core workflows as complete, usable content, not a pointer elsewhere.

## When to use this skill

Activate when the request involves:
- Crystal structures, compositions, space groups, phase diagrams, convex hull, electronic structure
  files, Materials Project
- Terms: pymatgen, Structure, Composition, SpacegroupAnalyzer, PhaseDiagram, POSCAR, band structure,
  DOS, mp-api
- File formats: `.cif`, `.poscar`/`CONTCAR`, `.xyz`, VASP/Quantum Espresso structure/output files
- "Parse this structure file," "determine the space group," "build a phase diagram," "query Materials Project"

## Which reference to read

| You have... | Read |
|---|---|
| A question about symmetry, transformations, or structure manipulation beyond basic I/O | [references/symmetry-and-transformations.md](references/symmetry-and-transformations.md) |
| A question about phase stability, convex hull, or phase diagrams | [references/phase-diagrams.md](references/phase-diagrams.md) |
| A question about reading/writing DFT code files (VASP, Quantum Espresso) or band structure/DOS | [references/electronic-structure-io.md](references/electronic-structure-io.md) |
| A question about querying the Materials Project database specifically | [references/materials-project-queries.md](references/materials-project-queries.md) |

For the DFT calculation itself (running VASP/QE, convergence, pseudopotentials), see
`computational-materials/references/dft.md` — this skill covers the structure/data objects those
calculations consume and produce, not running the calculation.

## Core usage — structure and composition basics

### Composition handling

```python
from pymatgen.core import Composition

comp = Composition("Fe2O3")
print(comp.weight)                  # molecular weight
print(comp.get_atomic_fraction("Fe"))
print(comp.reduced_formula)          # normalized formula
```

### Reading, writing, and inspecting structures

```python
from pymatgen.core import Structure

structure = Structure.from_file("material.cif")     # also reads POSCAR, .xyz, and other formats by extension
print(structure.composition)
print(structure.lattice)
print(structure.density)

structure.to(filename="material.poscar", fmt="poscar")
```

### Building a structure from scratch

```python
from pymatgen.core import Structure, Lattice

lattice = Lattice.cubic(4.2)
structure = Structure(lattice, ["Na", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]])
```

### Structure matching (comparing two structures, e.g. before/after relaxation)

```python
from pymatgen.analysis.structure_matcher import StructureMatcher

matcher = StructureMatcher()
are_equivalent = matcher.fit(structure_1, structure_2)   # accounts for symmetry-equivalent representations
```

## Validation & Pitfalls

Canonical reference: Ong et al. (2013), "Python Materials Genomics (pymatgen): A robust, open-source
python library for materials analysis," *Computational Materials Science* — the foundational
pymatgen paper covering the scope this skill is built around.

- **File format auto-detection by extension can fail silently on nonstandard filenames** — a
  correctly-formatted POSCAR file not named `POSCAR`/`CONTCAR` or lacking a recognized extension may
  parse incorrectly or raise an unclear error; when in doubt, specify the format explicitly rather
  than relying on auto-detection.
- **`reduced_formula` normalizes to integer ratios and can obscure the actual unit cell content** —
  for a structure with an unusual number of formula units per cell (e.g. Z=4), the reduced formula
  doesn't tell you the actual cell composition; check `structure.composition` (unreduced) when cell
  content specifically matters, not just stoichiometric ratio.
- **`StructureMatcher`'s default tolerances are reasonable for many cases but not universal** — very
  similar-but-genuinely-distinct structures (e.g. polymorphs with subtle distortions) can be
  reported as matching, or vice versa, depending on tolerance settings; check and report the
  tolerances used for any claim resting on structure equivalence.
- **A structure parsed from a computational output file (e.g. a relaxed VASP structure) carries no
  information about calculation convergence or accuracy** — treat a structure object as exactly what
  it is (a set of coordinates), not implicitly validated data; convergence/accuracy questions belong
  to `computational-materials`, not this layer.
