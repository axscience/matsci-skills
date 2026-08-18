---
name: phase-field-calphad
description: Mesoscale microstructure evolution and thermodynamic phase-diagram modeling — phase-field simulation (MOOSE and similar) and CALPHAD (Thermo-Calc, pycalphad) for temperature-dependent phase equilibria. Bridges atomistic simulation (computational-materials) and continuum mechanics (finite-element-modeling).
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples target pycalphad (open-source, Python) for CALPHAD; phase-field examples are conceptual given MOOSE's C++/input-file-based workflow.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: phase-field-calphad
---

# Phase-Field Modeling and CALPHAD

## Overview

CALPHAD (CALculation of PHAse Diagrams) computes temperature- and composition-dependent phase
equilibria from thermodynamic databases — the standard tool for multi-component phase diagrams and
alloy design. Phase-field modeling simulates how microstructure (grain growth, phase transformation,
precipitation) evolves over time, often using CALPHAD-derived thermodynamic data as input. Both sit
at the mesoscale, between atomistic simulation (`computational-materials`) and continuum mechanics
(`finite-element-modeling`).

## When to use this skill

Activate when the request involves:
- CALPHAD, phase diagram (temperature-dependent, not the 0K DFT hull in `materials-structure-analysis`),
  phase-field simulation, microstructure evolution, grain growth, precipitation, Thermo-Calc, pycalphad
- Terms: Gibbs free energy, thermodynamic database (.tdb), order parameter, interface mobility
- "Compute this alloy's phase diagram at temperature X," "simulate grain growth/precipitation"

## Core usage

### CALPHAD phase equilibrium calculation (pycalphad)

```python
from pycalphad import Database, equilibrium, variables as v

db = Database("alloy_system.tdb")   # thermodynamic database — see pitfalls on database provenance
components = ["FE", "C", "VA"]     # VA = vacancy, a CALPHAD convention for sublattice models
phases = list(db.phases.keys())

eq = equilibrium(db, components, phases, {v.X("C"): 0.01, v.T: 1000, v.P: 101325, v.N: 1})
print(eq.GM.values)   # Gibbs energy of the equilibrium state
```

### Binary phase diagram construction

```python
import numpy as np
from pycalphad import binplot

binplot(
    db, components, phases,
    {v.X("C"): (0, 0.05, 0.001), v.T: (300, 1300, 10), v.P: 101325, v.N: 1},
)
```

### Phase-field simulation (conceptual — MOOSE/similar is input-file/C++-driven, not primarily scripted in Python)

```python
# A phase-field model tracks one or more order parameters (phase fraction,
# composition) evolving under a free-energy functional (often CALPHAD-derived)
# via the Allen-Cahn (non-conserved order parameter, e.g. grain boundaries) or
# Cahn-Hilliard (conserved, e.g. composition) equations. MOOSE's phase-field
# module handles this via input files defining the free energy, mobility, and
# interface parameters — see MOOSE documentation for the current input syntax,
# which is substantial and version-specific.
```

## Validation & Pitfalls

Canonical references: Saunders & Miodownik, *CALPHAD: Calculation of Phase Diagrams* (1998), for
CALPHAD methodology; Chen (2002), "Phase-field models for microstructure evolution," *Annual Review
of Materials Research*, for phase-field modeling.

- **CALPHAD results are only as good as the thermodynamic database used, and databases vary in
  quality, scope, and the systems they were assessed for** — a database extrapolated outside the
  composition/temperature range it was fitted to can give a plausible-looking but unreliable phase
  diagram; check the database's documented valid range before trusting results outside it.
- **Metastable phases and phases outside the database's assessed system are invisible to a CALPHAD
  calculation by construction** — a CALPHAD phase diagram shows equilibrium among the phases included
  in the database, not necessarily every phase that could actually form (including kinetically
  stabilized ones); this is a different limitation than the 0K-only nature of the DFT-hull approach in
  `materials-structure-analysis`, but similarly requires stating what the calculation does and
  doesn't capture.
- **Phase-field simulation results depend heavily on interface energy/mobility parameters, which are
  often uncertain or fit rather than independently measured** — treat quantitative kinetic predictions
  (transformation timescales) with more skepticism than qualitative morphology predictions unless the
  parameters were specifically validated against experimental kinetics for the system in question.
- **Grid resolution and interface width in phase-field simulations are numerical parameters, not
  physical ones, and must be checked for convergence** — an under-resolved interface (too few grid
  points across the diffuse interface width) produces numerically unstable or spuriously fast
  dynamics; verify convergence with respect to grid resolution before trusting simulated kinetics.
- **CALPHAD equilibrium calculations assume full thermodynamic equilibrium is reached** — real
  processes (rapid cooling/quenching, short-duration heat treatments) can leave a material in a
  non-equilibrium state a CALPHAD diagram doesn't directly predict; this is where the phase-field
  (kinetic) approach complements the CALPHAD (equilibrium) one, not a substitute for it.
