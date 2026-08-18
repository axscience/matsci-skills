---
name: semiconductor-characterization
description: Electrical characterization of semiconductors — Hall effect (carrier density/mobility/type), four-point probe resistivity, and I-V/C-V device measurements. A distinct measurement class from electrochemistry (device transport properties, not electrolytic/redox behavior) and from mechanical/thermal characterization.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use numpy/scipy; conventions follow ASTM F76 (Hall/resistivity) where cited.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: semiconductor-characterization
---

# Semiconductor Characterization

## Overview

Semiconductor electrical characterization measures transport properties — carrier concentration,
mobility, carrier type, resistivity — that determine device performance. Hall effect measurement and
four-point probe resistivity are the two standard bulk/thin-film techniques; I-V and C-V measurements
characterize fabricated devices (diodes, transistors, capacitor structures) directly. This is a
different measurement class from `electrochemistry` (which covers electrolytic/redox systems, not
solid-state carrier transport).

## When to use this skill

Activate when the request involves:
- Hall effect, Hall measurement, carrier concentration, carrier mobility, four-point probe,
  sheet resistance, resistivity, I-V curve, C-V curve, doping concentration
- Terms: van der Pauw, Hall coefficient, n-type/p-type, depletion width, threshold voltage
- "Compute carrier density from Hall data," "extract resistivity from four-point probe," "analyze this I-V curve"

## Core usage

### Hall effect — carrier density, mobility, and type

```python
def hall_analysis(hall_voltage, current, magnetic_field, thickness, charge=1.602e-19):
    """Van der Pauw / standard Hall bar geometry. Sign of hall_voltage (with
    known current and field directions) determines carrier type — see pitfalls
    on getting sign conventions right."""
    sheet_carrier_density = (current * magnetic_field) / (charge * hall_voltage)
    carrier_density_3d = sheet_carrier_density / thickness
    carrier_type = "n-type" if hall_voltage > 0 else "p-type"  # convention-dependent — verify against your setup
    return {"sheet_carrier_density_per_m2": sheet_carrier_density, "carrier_density_per_m3": carrier_density_3d, "type": carrier_type}

def hall_mobility(sheet_resistance, sheet_carrier_density, charge=1.602e-19):
    return 1 / (charge * sheet_carrier_density * sheet_resistance)
```

### Four-point probe — sheet resistance and resistivity

```python
import numpy as np

def four_point_probe_sheet_resistance(voltage, current, geometric_correction_factor=4.532):
    """4.532 = pi/ln(2), the standard correction factor for a large, thin sample
    with equally spaced collinear probes — see pitfalls for when this doesn't apply."""
    return geometric_correction_factor * (voltage / current)  # ohms/square

def resistivity_from_sheet_resistance(sheet_resistance, thickness):
    return sheet_resistance * thickness
```

### I-V curve — diode parameter extraction

```python
from scipy.optimize import curve_fit
import numpy as np

def diode_equation(voltage, I0, n, T=300):
    """Shockley diode equation — extracts saturation current and ideality factor."""
    k_over_q = 8.617e-5  # eV/K (Boltzmann constant / elementary charge)
    return I0 * (np.exp(voltage / (n * k_over_q * T)) - 1)

def fit_diode_parameters(voltage, current):
    popt, _ = curve_fit(diode_equation, voltage, current, p0=[1e-12, 1.5], maxfev=5000)
    return {"saturation_current_I0": popt[0], "ideality_factor_n": popt[1]}
```

## Validation & Pitfalls

Canonical references: ASTM F76 (standard test methods for Hall/resistivity measurements of
semiconductors); Schroder, *Semiconductor Material and Device Characterization* (3rd ed., 2006).

- **Hall carrier-type sign convention depends on the specific current/field/voltage-probe geometry
  used, and getting it backwards silently reports the wrong carrier type** — verify the sign
  convention against the specific measurement setup (not a remembered rule of thumb) before reporting
  n-type vs. p-type.
- **The four-point-probe geometric correction factor (π/ln2 above) assumes a specific
  geometry (semi-infinite thin sample, equally spaced collinear probes)** — a small or non-standard
  sample geometry requires a different correction factor (finite-size corrections); using the
  standard factor on a sample that doesn't meet these assumptions produces a systematically wrong
  sheet resistance.
- **Contact quality (ohmic vs. non-ohmic/Schottky contacts) affects both Hall and four-point-probe
  measurements, and non-ohmic contacts can produce a nonlinear or asymmetric I-V response that biases
  results** — verify ohmic contact behavior (linear I-V through the contacts) before trusting
  extracted transport parameters.
- **Measured mobility is an average over all carrier scattering mechanisms present (phonon,
  ionized-impurity, etc.) and is temperature-dependent** — a mobility value without a stated
  measurement temperature is incomplete, and mobility values measured at different temperatures
  aren't directly comparable.
- **Diode ideality factor extraction is sensitive to the voltage range used for fitting** — series
  resistance dominates at high forward bias and recombination-current effects dominate at low bias,
  distorting the ideal exponential region; fit only the voltage range where the diode equation's
  assumptions actually hold, and check the fit residual rather than fitting the full curve blindly.
