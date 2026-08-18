# X-Ray Diffraction

Modality-specific detail for [../SKILL.md](../SKILL.md). Covers powder XRD phase identification and
peak-fitting-based microstructure analysis (crystallite size, microstrain) specifically.

## Loading and background-subtracting a pattern

```python
import numpy as np
from scipy.signal import savgol_filter

def load_and_subtract_background(two_theta, intensity, poly_order=3, iterations=100):
    """Iterative polynomial background subtraction (a simple, standard approach —
    more sophisticated methods exist, e.g. Sonneveld-Visser, for complex backgrounds)."""
    background = intensity.copy()
    for _ in range(iterations):
        fit = np.polyval(np.polyfit(two_theta, background, poly_order), two_theta)
        background = np.minimum(background, fit)
    return intensity - background
```

## Phase identification (search-match against a reference database)

```python
from scipy.signal import find_peaks

def extract_peak_positions(two_theta, intensity, prominence=100):
    peaks, properties = find_peaks(intensity, prominence=prominence)
    return two_theta[peaks], intensity[peaks]

# Compare extracted peak positions/relative intensities against reference patterns
# from ICDD PDF or a structure database (see materials-databases) — phase ID is a
# pattern-matching problem, not solvable from a single peak position alone.
```

## Crystallite size and microstrain (Williamson-Hall analysis)

```python
import numpy as np

def williamson_hall(two_theta_peaks, fwhm_peaks, wavelength, instrument_fwhm_peaks):
    """Separates crystallite-size broadening (angle-independent in this form) from
    microstrain broadening (angle-dependent) using a linear fit."""
    theta = np.radians(two_theta_peaks / 2)
    beta = np.radians(fwhm_peaks) - np.radians(instrument_fwhm_peaks)  # instrument-corrected
    beta_cos_theta = beta * np.cos(theta)
    four_sin_theta = 4 * np.sin(theta)

    slope, intercept = np.polyfit(four_sin_theta, beta_cos_theta, 1)
    microstrain = slope
    crystallite_size = 0.9 * wavelength / intercept if intercept > 0 else np.nan  # Scherrer-derived intercept
    return crystallite_size, microstrain
```

## Validation & Pitfalls

Canonical reference: Williamson & Hall (1953), "X-ray line broadening from filed aluminium and
wolfram," *Acta Metallurgica*, for the Williamson-Hall method; Langford & Wilson (1978), "Scherrer
after sixty years," *Journal of Applied Crystallography*, for Scherrer-equation limitations.

- **The Scherrer equation gives a lower bound on crystallite size, not an exact value, and assumes
  broadening is purely size-driven** — applying it without separating strain contributes to a common
  systematic underestimate of true crystallite size when microstrain is also present. Use
  Williamson-Hall (or a more complete method) when both contributions plausibly matter.
- **Peak overlap in complex or low-symmetry patterns makes automated peak-finding unreliable** —
  `find_peaks`-style detection can merge nearby peaks or miss shoulders; visually verify extracted
  peaks against the raw pattern before feeding them into size/strain analysis, especially for
  multi-phase or low-symmetry samples.
- **Preferred orientation and specimen displacement error both shift/distort peaks in ways that
  masquerade as lattice-parameter or phase-fraction changes** — a specimen height error of even
  tens of microns produces a systematic 2θ shift; verify sample height/alignment before attributing a
  peak shift to a real structural change.
- **Background subtraction method choice affects extracted peak intensities and can bias quantitative
  phase-fraction analysis** (Rietveld or reference-intensity-ratio methods) — state the background
  model used, and check sensitivity to it for any quantitative (not just qualitative phase-ID) claim.
