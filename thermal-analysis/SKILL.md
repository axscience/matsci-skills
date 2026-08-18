---
name: thermal-analysis
description: Thermal characterization — differential scanning calorimetry (DSC), thermogravimetric analysis (TGA), and dilatometry. Glass transition/melting/crystallization detection, mass-loss event analysis, and thermal expansion measurement. Use this for any technique that characterizes a material's response to controlled heating/cooling.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use numpy/scipy; real instrument software (TA Instruments TRIOS, Netzsch Proteus) has built-in analysis that this complements for custom/batch analysis.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: thermal-analysis
---

# Thermal Analysis

## Overview

DSC measures heat flow associated with thermal transitions (glass transition, melting,
crystallization, curing, decomposition); TGA measures mass change with temperature (decomposition,
volatile loss, oxidation); dilatometry measures dimensional change (thermal expansion, sintering
shrinkage). All three run a controlled temperature program and extract event-specific quantitative
measures from the resulting curve.

## When to use this skill

Activate when the request involves:
- DSC, differential scanning calorimetry, TGA, thermogravimetric analysis, dilatometry
- Terms: glass transition (Tg), melting point, crystallization, mass loss, coefficient of thermal
  expansion, heat flow
- File formats: instrument-specific exports (`.dsc`, common CSV/TXT exports)
- "Find the glass transition in this DSC curve," "quantify mass loss steps in this TGA," "compute CTE"

## Core usage

### DSC — glass transition and melting/crystallization peak detection

```python
import numpy as np
from scipy.signal import find_peaks, savgol_filter

def find_glass_transition(temperature, heat_flow, window=21):
    """Tg appears as a step change (inflection), not a peak — detect via the
    derivative's local extremum, not peak-finding on the raw curve."""
    smoothed = savgol_filter(heat_flow, window, 3)
    derivative = np.gradient(smoothed, temperature)
    inflection_idx = np.argmax(np.abs(derivative))
    return temperature[inflection_idx]  # midpoint-Tg convention — see pitfalls for other conventions

def find_melting_crystallization_peaks(temperature, heat_flow, prominence=0.1):
    """Melting: endothermic peak; crystallization: exothermic peak — sign
    convention depends on instrument software (heat-flow-up vs -down); confirm
    which convention applies before interpreting peak direction."""
    peaks, properties = find_peaks(heat_flow, prominence=prominence)
    return temperature[peaks], properties
```

### TGA — mass-loss step quantification

```python
def quantify_mass_loss_steps(temperature, mass_percent, step_boundaries):
    """step_boundaries: list of (T_start, T_end) tuples bounding each mass-loss
    event, typically identified from the derivative (DTG) curve's peaks."""
    steps = []
    for t_start, t_end in step_boundaries:
        mask = (temperature >= t_start) & (temperature <= t_end)
        mass_lost = mass_percent[mask][0] - mass_percent[mask][-1]
        steps.append({"T_range": (t_start, t_end), "mass_loss_percent": mass_lost})
    return steps

def dtg_curve(temperature, mass_percent):
    """Derivative TGA — sharpens mass-loss steps into peaks, standard for
    identifying step boundaries and overlapping events."""
    return np.gradient(mass_percent, temperature)
```

### Dilatometry — coefficient of thermal expansion (CTE)

```python
def coefficient_of_thermal_expansion(temperature, length, T1, T2, L0):
    """Linear CTE over a temperature range — must specify the range, since CTE is
    rarely constant across a wide temperature span (phase transitions, anisotropy)."""
    mask = (temperature >= T1) & (temperature <= T2)
    delta_L = length[mask][-1] - length[mask][0]
    delta_T = temperature[mask][-1] - temperature[mask][0]
    return (delta_L / L0) / delta_T
```

## Validation & Pitfalls

Canonical reference: Höhne, Hemminger & Flammersheim, *Differential Scanning Calorimetry* (2nd ed.,
2003); ASTM E1356 (DSC glass transition), ASTM E1131 (TGA compositional analysis), and ASTM E228
(dilatometry CTE) for standard measurement conventions.

- **Tg has multiple reporting conventions (onset, midpoint, inflection) that give different
  numbers from the same curve** — state which convention was used; comparing Tg values across
  studies/instruments without confirming matched conventions is a common source of apparent
  discrepancy that isn't a real material difference.
- **Heating rate affects observed transition temperatures, sometimes substantially** — Tg and
  crystallization temperature both shift with scan rate (kinetic, not purely thermodynamic,
  transitions for polymers especially). Report the heating/cooling rate used; don't compare
  transition temperatures measured at different rates as if rate-independent.
- **TGA mass-loss step boundaries chosen by eye are subjective, especially for overlapping/gradual
  events** — use the DTG (derivative) curve to identify step boundaries systematically rather than
  reading approximate onset/endset temperatures directly off the raw mass curve.
- **Furnace atmosphere (inert vs. oxidizing) changes TGA decomposition pathways and apparent mass-loss
  temperatures** — a material's TGA curve in air vs. nitrogen can differ substantially (e.g. oxidative
  vs. purely thermal decomposition); confirm and report the atmosphere used.
- **CTE measured over a wide temperature range that spans a phase transition or Tg gives a
  physically meaningless average** — always report CTE for a bounded range that stays within one
  physical regime (below Tg, above Tg, etc.), not a single number spanning transitions.
