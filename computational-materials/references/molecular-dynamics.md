# Classical and Reactive Molecular Dynamics

Modality-specific detail for [../SKILL.md](../SKILL.md). Covers LAMMPS-based classical MD — force
field selection, ensemble choice, and timestep/equilibration considerations.

## Basic LAMMPS input structure

```python
# LAMMPS input scripts are its own domain-specific language, not Python — shown
# here as the standard workflow structure (conceptually, via PyLAMMPS/lammps
# Python bindings for programmatic control):
from lammps import lammps

lmp = lammps()
lmp.command("units metal")               # unit system — must match force field convention
lmp.command("atom_style atomic")
lmp.command("read_data structure.data")
lmp.command("pair_style eam/alloy")        # force field type — see selection notes below
lmp.command("pair_coeff * * potential.eam.alloy Fe")

lmp.command("fix 1 all npt temp 300 300 0.1 iso 0 0 1.0")   # NPT ensemble
lmp.command("timestep 0.001")               # ps, for metal units — see pitfalls on timestep choice
lmp.command("run 100000")
```

## Force field selection

```python
# EAM (embedded atom method): standard for metals, captures many-body metallic bonding.
# Reactive force fields (ReaxFF): allow bond breaking/formation — needed for
#   chemical reactions, combustion, some battery-interface chemistry — at
#   substantially higher computational cost than non-reactive force fields.
# Coarse-grained (e.g. MARTINI): trades atomic detail for larger system size/longer
#   timescale — appropriate when atomic-resolution detail isn't the question.
# Force field validity is system-specific — a force field parameterized for one
# chemical environment (e.g. bulk metal) may not transfer to another (e.g. a
# metal surface or nanoparticle) without explicit validation.
```

## Ensemble and equilibration

```python
# NVE: energy-conserving, used for production dynamics after equilibration.
# NVT: constant temperature (thermostat) — for equilibrating at a target temperature.
# NPT: constant temperature and pressure (thermostat + barostat) — for
#   equilibrating cell volume/shape, e.g. before measuring a temperature-dependent
#   lattice parameter or density.
# Equilibration must be confirmed (e.g. temperature/pressure/energy plateauing),
# not assumed complete after a fixed number of steps chosen without checking.
```

## Validation & Pitfalls

Canonical references: Plimpton (1995), "Fast parallel algorithms for short-range molecular
dynamics," *Journal of Computational Physics* (the original LAMMPS paper); Daw & Baskes (1984),
"Embedded-atom method: Derivation and application to impurity, surface, and other defects in
metals," *Physical Review B*, for EAM.

- **Timestep must be small enough to resolve the fastest vibrational motion in the system — too
  large a timestep produces energy drift or an outright unstable simulation, and this failure can be
  subtle (gradual energy drift) rather than an obvious crash.** A common starting point is ~1 fs for
  systems with light atoms/fast vibrations (e.g. containing hydrogen), larger for heavier-atom-only
  systems — but this must be verified for the specific system, not assumed from a rule of thumb.
- **Classical force fields do not capture chemistry (bond breaking/forming) unless specifically
  reactive (ReaxFF or similar)** — using a non-reactive force field on a system where bonds actually
  break/form during the simulated process (e.g. a battery interface reaction) produces qualitatively
  wrong physics, not just quantitatively imprecise results.
- **Finite simulation size and periodic boundary conditions can introduce artifacts** (a property that
  depends on long-range correlations, or a defect interacting with its own periodic images) —
  check convergence with respect to system size for properties sensitive to this, don't assume a
  single system size is adequate without testing.
- **Statistical properties (diffusion coefficients, radial distribution functions, thermodynamic
  averages) require adequate sampling time after equilibration — a short production run gives a
  statistically unreliable estimate even from a well-equilibrated, well-parameterized simulation.**
  Report both simulation length and an estimate of statistical uncertainty (e.g. via block averaging),
  not just a point estimate.
- **Force field transferability is not guaranteed outside the conditions/systems it was fit to** — a
  force field validated for bulk crystal properties may perform poorly for surfaces, defects, or
  amorphous structures unless specifically validated for those; check the force field's original
  parameterization scope before trusting it in a different context.
