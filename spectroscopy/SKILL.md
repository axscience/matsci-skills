---
name: spectroscopy
description: Vibrational, electronic, and nuclear spectroscopy for materials characterization — XPS, Raman, FTIR, and solid-state NMR. Shared peak-fitting/baseline-correction workflow, with references per technique. Use this for any technique that identifies chemical bonding, oxidation state, or molecular structure from a spectrum.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use scipy/lmfit for peak fitting, applicable across all four techniques.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: spectroscopy
---

# Spectroscopy

## Overview

XPS, Raman, FTIR, and solid-state NMR all identify chemical/structural information from a spectrum
(binding energy, Raman shift, wavenumber, or chemical shift respectively) — different physics, but a
shared analysis workflow: baseline correction, peak fitting, and peak assignment against reference
data. This skill covers what's shared and routes to technique-specific references.

## When to use this skill

Activate when the request involves:
- XPS, X-ray photoelectron spectroscopy, Raman spectroscopy, FTIR, infrared spectroscopy,
  solid-state NMR
- Terms: binding energy, oxidation state, peak fitting, baseline correction, chemical shift,
  wavenumber
- File formats: `.vms`/`.xy` (XPS), `.spc`/`.txt` (Raman/FTIR common exports)
- "Fit peaks in this XPS/Raman/FTIR spectrum," "identify oxidation state," "assign these NMR peaks"

## Which reference to read

| You have... | Read |
|---|---|
| XPS (oxidation state, surface composition) | [references/xps.md](references/xps.md) |
| Raman spectroscopy | [references/raman.md](references/raman.md) |
| FTIR / infrared spectroscopy | [references/ftir.md](references/ftir.md) |
| Solid-state NMR | [references/nmr.md](references/nmr.md) |

## Core usage — shared peak fitting

### Baseline correction (asymmetric least squares — works across all four techniques)

```python
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

def als_baseline(intensity, lam=1e5, p=0.01, n_iter=10):
    """Asymmetric least squares baseline (Eilers & Boelens, 2005) — standard,
    technique-agnostic baseline correction for peaked spectra."""
    L = len(intensity)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
    D = lam * D.dot(D.transpose())
    w = np.ones(L)
    W = sparse.spdiags(w, 0, L, L)
    for _ in range(n_iter):
        W.setdiag(w)
        baseline = spsolve(W + D, w * intensity)
        w = p * (intensity > baseline) + (1 - p) * (intensity < baseline)
    return baseline
```

### Peak fitting (Voigt profile — appropriate for most XPS/Raman/FTIR peaks)

```python
from lmfit.models import VoigtModel

def fit_peak(x, y, center_guess):
    model = VoigtModel()
    params = model.guess(y, x=x)
    params["center"].set(value=center_guess)
    result = model.fit(y, params, x=x)
    return result   # result.params gives fitted center, amplitude, sigma, gamma
```

Everything technique-specific — peak assignment tables, reference databases, artifact profiles — is
in the references above.

## Validation & Pitfalls

- **Peak shape (Gaussian, Lorentzian, or Voigt) should be chosen based on the physical broadening
  mechanism, not fit convenience** — instrumental broadening tends toward Gaussian, natural/lifetime
  broadening toward Lorentzian; a Voigt profile (convolution of both) is a reasonable general default,
  but forcing a pure Gaussian or Lorentzian fit on data that doesn't match can bias fitted peak
  positions and areas.
- **Baseline correction parameters (like `lam`/`p` above) change fitted peak areas, sometimes
  substantially, and are not neutral defaults** — report the method and parameters used, and check
  sensitivity when a quantitative (not just qualitative) claim depends on peak area.
