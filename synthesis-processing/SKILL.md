---
name: synthesis-processing
description: Materials synthesis and processing routes — solid-state synthesis, sol-gel, chemical/physical vapor deposition (CVD/PVD), epitaxy, and additive manufacturing. Upstream of every characterization skill in this repo — use this to plan how a sample is made, which determines what the characterization techniques will actually measure.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: This skill is primarily process-parameter and stoichiometry guidance rather than a specific software package.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: synthesis-processing
---

# Synthesis and Processing

## Overview

Every characterization skill in this repo analyzes a sample that came from somewhere — this skill is
that somewhere. Synthesis route determines microstructure, phase purity, and defect density in ways
that downstream characterization then measures; a poorly controlled synthesis produces a sample where
characterization results reflect synthesis artifacts as much as the intended material.

## When to use this skill

Activate when the request involves:
- Solid-state synthesis, sol-gel, CVD, chemical vapor deposition, PVD, physical vapor deposition,
  sputtering, epitaxy, additive manufacturing, 3D printing (materials)
- Terms: precursor, stoichiometry, calcination, annealing, deposition rate, substrate, growth rate
- "Plan a synthesis route for...," "calculate precursor stoichiometry," "what deposition parameters..."

## Core usage

### Solid-state synthesis — stoichiometric precursor calculation

```python
def solid_state_precursor_masses(target_formula_moles, precursor_molar_masses, target_mass_g, molar_mass_target):
    """target_formula_moles: dict of precursor -> stoichiometric coefficient in the
    target formula unit. Scales to a target sample mass."""
    total_moles_target = target_mass_g / molar_mass_target
    return {
        precursor: total_moles_target * coeff * precursor_molar_masses[precursor]
        for precursor, coeff in target_formula_moles.items()
    }
```

### Sol-gel — precursor solution molarity and gelation planning

```python
def sol_gel_precursor_volume(target_molarity, target_volume_ml, precursor_molarity_stock):
    """Dilution calculation for a stock precursor solution — standard sol-gel prep step."""
    return (target_molarity * target_volume_ml) / precursor_molarity_stock  # mL of stock needed
```

### CVD/PVD — deposition rate and thickness planning

```python
def deposition_time_for_thickness(target_thickness_nm, deposition_rate_nm_per_min):
    """Deposition rate must be calibrated per-tool/per-condition (see pitfalls) —
    this is planning arithmetic, not a substitute for that calibration."""
    return target_thickness_nm / deposition_rate_nm_per_min
```

### Epitaxy — lattice mismatch calculation (a key screening step for substrate selection)

```python
def lattice_mismatch_percent(film_lattice_parameter, substrate_lattice_parameter):
    """Large mismatch (~beyond a few %) drives strain relaxation via dislocations
    above a critical thickness — a first-order screening calculation before
    attempting epitaxial growth on a candidate substrate."""
    return ((film_lattice_parameter - substrate_lattice_parameter) / substrate_lattice_parameter) * 100
```

## Validation & Pitfalls

Canonical references: West, *Solid State Chemistry and its Applications* (2nd ed., 2014), for
solid-state synthesis; Ohring, *Materials Science of Thin Films* (2nd ed., 2001), for CVD/PVD/epitaxy.

- **Solid-state synthesis reaction completeness cannot be assumed from following a recipe — it must
  be verified** (typically via `diffraction` to confirm phase purity, absence of unreacted precursor
  peaks). A characterization result on an incompletely reacted sample reflects a mixture, not the
  intended single phase, regardless of how carefully the recipe was followed.
- **Calcination/annealing atmosphere (air, inert, reducing) changes achievable oxidation states and
  phase stability** — a synthesis recipe's atmosphere requirement is not incidental detail; running
  the "same" recipe in a different atmosphere can produce a different phase or oxidation state
  entirely.
- **Deposition rate calibration drifts with tool conditioning, target/source aging, and chamber
  cleanliness** — a rate measured weeks or tool-cleanings ago is not reliable for precise thickness
  targeting; recalibrate (e.g. via a witness sample measured with `microscopy` or profilometry) before
  a thickness-critical deposition.
- **Epitaxial quality depends on more than lattice mismatch alone** (thermal expansion mismatch,
  surface reconstruction, growth temperature/kinetics) — a favorable lattice-mismatch calculation is
  a necessary screening step, not a guarantee of good epitaxial quality; verify actual film quality
  via `diffraction` (rocking curve) and `microscopy`, not the mismatch calculation alone.
- **Precursor purity and stoichiometric calculation errors compound in multi-precursor syntheses** —
  a small stoichiometry error in a complex (3+ precursor) solid-state or sol-gel synthesis can shift
  the product into a different region of a phase diagram entirely (see `computational-materials`/
  `materials-structure-analysis` for phase-diagram tools to check target-composition stability before
  committing to a synthesis).
