---
name: mechanical-testing
description: Mechanical property characterization — tensile/compression testing, nanoindentation, fatigue, and fracture toughness. Stress-strain analysis, Weibull statistics for brittle-fracture data, and material-class-specific failure model notes (ceramic vs. polymer vs. metal). Use this for any technique that measures a material's mechanical response to applied load.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use numpy/scipy; conventions follow ASTM standards where cited.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: mechanical-testing
---

# Mechanical Testing

## Overview

Mechanical testing quantifies how a material responds to applied stress — tensile/compression
testing for bulk stress-strain behavior, nanoindentation for local hardness/modulus at small scales,
fatigue for cyclic-loading lifetime, and fracture toughness for resistance to crack propagation. The
underlying physics and failure modes differ substantially by material class (metals yield plastically;
ceramics fail brittlely with statistical scatter; polymers show viscoelastic/rate-dependent behavior).

## When to use this skill

Activate when the request involves:
- Tensile testing, compression testing, stress-strain curve, nanoindentation, hardness, fatigue,
  fracture toughness, Weibull statistics
- Terms: Young's modulus, yield strength, ultimate tensile strength, S-N curve, K_IC, Oliver-Pharr
- File formats: instrument-specific exports (Instron, MTS), common CSV load-displacement data
- "Analyze this stress-strain curve," "compute fracture strength Weibull modulus," "fit an S-N curve"

## Core usage

### Stress-strain curve analysis (tensile/compression)

```python
import numpy as np

def stress_strain_properties(strain, stress, gauge_length_mm, cross_section_mm2):
    """Standard tensile properties from an engineering stress-strain curve.
    elastic_modulus: fit on the initial linear region, not the whole curve."""
    linear_region = strain < 0.002  # typical small-strain window for modulus fit — adjust per material
    elastic_modulus = np.polyfit(strain[linear_region], stress[linear_region], 1)[0]

    yield_strength = offset_yield_strength(strain, stress, elastic_modulus, offset=0.002)
    ultimate_tensile_strength = stress.max()
    return {
        "elastic_modulus": elastic_modulus,
        "yield_strength_0.2%_offset": yield_strength,
        "UTS": ultimate_tensile_strength,
    }

def offset_yield_strength(strain, stress, elastic_modulus, offset=0.002):
    """0.2% offset method — standard for materials without a sharp yield point."""
    offset_line = elastic_modulus * (strain - offset)
    diff = stress - offset_line
    sign_changes = np.where(np.diff(np.sign(diff)))[0]
    return stress[sign_changes[0]] if len(sign_changes) > 0 else np.nan
```

### Nanoindentation (Oliver-Pharr method)

```python
def oliver_pharr_modulus_hardness(load, displacement, contact_stiffness, contact_area, poisson_ratio_sample=0.3, poisson_ratio_indenter=0.07, modulus_indenter_gpa=1141):
    """Reduced modulus from unloading stiffness, then sample modulus via the
    standard Oliver-Pharr relation (indenter properties for diamond shown)."""
    reduced_modulus = contact_stiffness * np.sqrt(np.pi) / (2 * np.sqrt(contact_area))
    inv_sample_modulus = (1 / reduced_modulus) - (1 - poisson_ratio_indenter**2) / modulus_indenter_gpa
    sample_modulus = (1 - poisson_ratio_sample**2) / inv_sample_modulus
    hardness = load.max() / contact_area
    return {"reduced_modulus_gpa": reduced_modulus, "sample_modulus_gpa": sample_modulus, "hardness_gpa": hardness}
```

### Weibull statistics for brittle-fracture strength data

```python
from scipy import stats
import numpy as np

def weibull_fit(fracture_strengths):
    """Ceramics/glasses/brittle materials show statistical (not deterministic)
    strength — Weibull analysis is the standard approach, not a normal-distribution
    fit. shape (Weibull modulus, m): higher = less scatter/more reliable."""
    shape, loc, scale = stats.weibull_min.fit(fracture_strengths, floc=0)
    return {"weibull_modulus_m": shape, "characteristic_strength": scale}

def median_rank_weibull_plot_data(fracture_strengths):
    """Median rank (Bernard's approximation) — standard plotting-position method
    for Weibull probability plots, more appropriate than naive rank/N for small
    sample sizes typical of fracture testing."""
    sorted_strengths = np.sort(fracture_strengths)
    n = len(sorted_strengths)
    ranks = np.arange(1, n + 1)
    median_rank = (ranks - 0.3) / (n + 0.4)
    return sorted_strengths, median_rank
```

### Fatigue — S-N curve fitting (Basquin relation)

```python
def basquin_fit(stress_amplitude, cycles_to_failure):
    """log-log linear fit — standard for the finite-life regime of an S-N curve."""
    log_n = np.log10(cycles_to_failure)
    log_s = np.log10(stress_amplitude)
    slope, intercept = np.polyfit(log_n, log_s, 1)
    return {"basquin_exponent": slope, "basquin_coefficient": 10**intercept}
```

## Validation & Pitfalls

Canonical references: ASTM E8 (tensile testing of metals), ASTM C1239 (Weibull analysis of
brittle-material strength), Oliver & Pharr (1992), "An improved technique for determining hardness
and elastic modulus using load and displacement sensing indentation experiments," *Journal of
Materials Research*, for nanoindentation.

- **Engineering vs. true stress-strain matter, and the difference is not negligible at large
  strain** — engineering stress/strain (using original cross-section/gauge length) diverges from
  true stress/strain (using instantaneous values) especially past yield/necking. State which is
  reported, and use true stress-strain for any analysis involving large plastic deformation.
- **Weibull modulus fitting is unstable with small sample sizes, and small-N Weibull moduli are
  frequently over-interpreted** — brittle-fracture testing standards (e.g. ASTM C1239) typically call
  for 30+ specimens for a reliable Weibull modulus estimate; report sample size alongside any fitted
  m, and treat single-digit-N estimates as preliminary.
- **Nanoindentation results are sensitive to indenter tip-area-function calibration, surface
  roughness, and pile-up/sink-in behavior not accounted for in the basic Oliver-Pharr model** — a
  poorly calibrated tip area function or unaccounted pile-up can bias modulus/hardness by a
  significant fraction; verify tip calibration against a reference material (e.g. fused silica)
  before trusting absolute values.
- **Material-class failure models don't transfer** — a ductile-metal yield-strength framework applied
  to a brittle ceramic (which doesn't yield plastically the same way) or a viscoelastic polymer
  (whose stress-strain response is strain-rate- and temperature-dependent) produces a
  physically-meaningless "yield strength." Match the analysis framework to the material class, and
  for polymers specifically, always report strain rate and temperature alongside any modulus/strength
  value.
- **S-N curve fatigue data has a runout convention (specimens that survive to a set cycle count
  without failing) that a naive log-log fit ignores if not handled explicitly** — treating runouts as
  failures at the runout cycle count biases the fitted curve; use a method that properly accounts for
  censored (runout) data.
