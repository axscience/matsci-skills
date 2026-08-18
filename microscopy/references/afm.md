# Atomic Force Microscopy (AFM)

Modality-specific detail for [../SKILL.md](../SKILL.md). AFM measures surface topography (and,
depending on mode, mechanical/electrical/magnetic properties) via a physical probe tip, not electron
or photon scattering — a genuinely different measurement class with its own artifact profile.

## Loading and leveling topography data

```python
import numpy as np

def plane_level(topography, mask=None):
    """Removes sample tilt (a near-universal AFM artifact from imperfect sample
    mounting) by fitting and subtracting a plane. mask: optional boolean array to
    exclude features (e.g. large particles) from the plane fit."""
    height, width = topography.shape
    y, x = np.mgrid[0:height, 0:width]
    fit_mask = mask if mask is not None else np.ones_like(topography, dtype=bool)

    A = np.column_stack([x[fit_mask], y[fit_mask], np.ones(fit_mask.sum())])
    coeffs, _, _, _ = np.linalg.lstsq(A, topography[fit_mask], rcond=None)
    plane = coeffs[0] * x + coeffs[1] * y + coeffs[2]
    return topography - plane

def line_level(topography):
    """Row-by-row median subtraction — corrects scan-line-to-scan-line offset
    artifacts (common in AFM, from slow thermal/piezo drift between lines)."""
    return topography - np.median(topography, axis=1, keepdims=True)
```

## Roughness quantification

```python
def surface_roughness(topography):
    """Standard roughness parameters (ISO 25178 / ASME B46.1 conventions)."""
    mean_height = topography.mean()
    ra = np.mean(np.abs(topography - mean_height))       # arithmetic mean roughness
    rq = np.sqrt(np.mean((topography - mean_height) ** 2))  # RMS roughness
    return {"Ra": ra, "Rq_RMS": rq}
```

## Validation & Pitfalls

Canonical reference: Eaton & West, *Atomic Force Microscopy* (2010), for general AFM methodology
and artifact characterization.

- **Tip convolution (finite tip radius) systematically distorts measured feature shape and size** —
  a feature narrower than or comparable to the tip radius appears wider than it actually is, and
  sharp features appear rounded. This is a fundamental measurement limitation, not a processing
  artifact fixable by better leveling — report tip radius (from manufacturer spec or a calibration
  standard) alongside any lateral-dimension claim from AFM.
- **Roughness parameters (Ra, Rq) depend on scan size and, for fractal/multi-scale-rough surfaces,
  don't converge to a single "true" value** — report the scan size used, and don't compare roughness
  values measured at different scan sizes as if they were equivalent.
- **Plane-leveling and line-leveling can remove real, large-scale sample curvature along with tilt
  artifacts** — for genuinely curved samples (e.g. a coated fiber), naive plane subtraction introduces
  its own distortion; check whether the sample is expected to be locally flat before applying a
  standard leveling algorithm.
- **Contact-mode vs. tapping-mode (AC mode) AFM have different artifact profiles** — contact mode can
  drag/damage soft samples (giving apparent topographic streaking), tapping mode is gentler but its
  phase-image contrast reflects a mix of mechanical properties that isn't straightforwardly
  interpretable as a single material property without additional calibration.
