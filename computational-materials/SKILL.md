---
name: computational-materials
description: First-principles and classical simulation of materials — DFT (VASP/Quantum Espresso), classical/reactive molecular dynamics (LAMMPS), and machine-learned interatomic potentials (MACE/NequIP-class models). Use this for any simulation-based (not experimental-characterization) approach to predicting or explaining material properties.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: References target VASP 6.x/Quantum Espresso 7.x conventions, LAMMPS (stable release), and MACE/NequIP for ML potentials.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: computational-materials
---

# Computational Materials Science

## Overview

Three simulation approaches cover most of computational materials science: DFT for accurate
first-principles electronic/energetic properties at the cost of system-size limits (hundreds of
atoms, typically), classical molecular dynamics for large systems/long timescales at the cost of
force-field accuracy, and machine-learned interatomic potentials — a fast-growing middle ground
combining near-DFT accuracy with MD-scale system sizes. This skill routes to the method that fits the
question; `materials-structure-analysis` covers the structure/data objects all three consume and
produce.

## When to use this skill

Activate when the request involves:
- DFT, density functional theory, VASP, Quantum Espresso, molecular dynamics, LAMMPS, force field,
  machine-learned potential, MACE, NequIP, interatomic potential
- Terms: convergence, pseudopotential, k-points, exchange-correlation functional, ensemble (NVT/NPT),
  potential fitting
- "Set up a DFT calculation," "run an MD simulation," "fit/use an ML interatomic potential"

## Which reference to read

| You have... | Read |
|---|---|
| A first-principles/DFT question (convergence, functional choice, pseudopotentials) | [references/dft.md](references/dft.md) |
| A classical or reactive MD question (force fields, ensembles, timestep) | [references/molecular-dynamics.md](references/molecular-dynamics.md) |
| A question about ML interatomic potentials (training, using, or validating one) | [references/ml-interatomic-potentials.md](references/ml-interatomic-potentials.md) |

For structure/composition object handling, symmetry, phase diagrams, and file I/O that all three
methods use, see `materials-structure-analysis` — this skill covers the simulation methods
themselves, not the data layer beneath them.

## Validation & Pitfalls

- **Method choice should be driven by the question's accuracy/scale requirements, not habit or
  familiarity.** DFT for a question needing accurate electronic structure on a small system; MD for
  large-system/long-timescale dynamics where force-field accuracy is adequate; ML potentials when
  near-DFT accuracy is needed at MD-relevant scale and a suitable trained (or trainable) potential
  exists. Using DFT-scale methods on a question that actually needs large-system statistics (or
  vice versa) wastes compute without answering the question asked.
- **Simulation results are only as good as the input structure and methodology — a beautifully
  converged calculation on a wrong or unvalidated structure produces a precise, wrong answer.**
  Confirm the input structure (from `materials-structure-analysis` or experimental characterization)
  is actually representative of the system being modeled before investing in expensive convergence.
