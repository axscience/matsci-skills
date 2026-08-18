---
name: microscopy
description: Electron and probe microscopy for materials characterization — SEM, TEM (incl. STEM/EELS/EDS), and AFM. Image-analysis-heavy workflow shared across all three (drift/distortion correction, segmentation, particle/feature sizing), with references per technique. Use this for any imaging-based materials characterization at micro/nanoscale.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use scikit-image/numpy for general image processing; HyperSpy for EELS/EDS spectrum-image analysis.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: microscopy
---

# Microscopy

## Overview

SEM, TEM, and AFM all produce spatially resolved images of a material's surface or internal
structure, at scales from microns down to atomic resolution. They share a substantial image-analysis
workflow — drift/distortion correction, segmentation, feature/particle sizing — even though the
physical contrast mechanisms (secondary/backscattered electrons for SEM, transmitted/diffracted
electrons for TEM, tip-sample force for AFM) are entirely different.

## When to use this skill

Activate when the request involves:
- SEM, scanning electron microscopy, TEM, transmission electron microscopy, STEM, EELS, EDS/EDX,
  AFM, atomic force microscopy
- Terms: secondary electron, backscattered electron, bright-field/dark-field, particle sizing,
  segmentation, tip artifact
- File formats: `.dm3`/`.dm4` (Gatan), `.emd`, `.tif` (common microscope export), `.ibw`/`.spm` (AFM)
- "Segment particles in this SEM image," "analyze this EELS spectrum image," "measure roughness from AFM"

## Which reference to read

| You have... | Read |
|---|---|
| SEM images (secondary/backscattered electron, EDS elemental maps) | [references/sem.md](references/sem.md) |
| TEM images, diffraction, or STEM/EELS/EDS spectrum imaging | [references/tem.md](references/tem.md) |
| AFM topography, phase, or force data | [references/afm.md](references/afm.md) |

For electron diffraction specifically (SAED, acquired in a TEM), see `diffraction/references/electron-diffraction.md`.

## Core usage — shared image processing

### Drift correction (cross-correlation registration across a stack)

```python
import numpy as np
from skimage.registration import phase_cross_correlation
from scipy.ndimage import shift as ndi_shift

def correct_drift(image_stack):
    """image_stack: (n_frames, height, width). Registers each frame to the first."""
    reference = image_stack[0]
    corrected = [reference]
    for frame in image_stack[1:]:
        shift_estimate, _, _ = phase_cross_correlation(reference, frame, upsample_factor=10)
        corrected.append(ndi_shift(frame, shift_estimate))
    return np.array(corrected)
```

### Particle/feature segmentation and sizing

```python
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import remove_small_objects

def segment_and_measure(image, min_size_px=20):
    binary = image > threshold_otsu(image)
    binary = remove_small_objects(binary, min_size=min_size_px)
    labeled = label(binary)
    return [
        {"area_px": r.area, "equivalent_diameter_px": r.equivalent_diameter, "eccentricity": r.eccentricity}
        for r in regionprops(labeled)
    ]
```

Convert pixel measurements to physical units using the image's calibrated pixel size (from
instrument metadata) before reporting — see Validation & Pitfalls.

## Validation & Pitfalls

Canonical reference: Williams & Carter, *Transmission Electron Microscopy* (2nd ed., 2009), and
Goldstein et al., *Scanning Electron Microscopy and X-Ray Microanalysis* (4th ed., 2017), for
instrument-level physics across both techniques.

- **Pixel-to-physical-unit calibration is instrument- and magnification-setting-specific and must be
  read from image metadata, not assumed constant.** Reporting particle sizes without confirming the
  actual calibration for that specific image (not a remembered "typical" value) is a common source of
  systematically wrong measurements.
- **Segmentation threshold choice (Otsu or any automatic method) can fail on images with uneven
  illumination, charging artifacts (SEM), or low contrast** — visually verify segmentation results
  against the raw image on a representative sample before trusting automated measurements at scale.
- **"The image looks clear" is not the same as "the sample is representative"** — imaging a small
  field of view at high magnification risks sampling bias; report how many fields/particles were
  measured and whether they were selected systematically (e.g. a grid pattern) rather than by eye,
  which biases toward visually striking (often larger, more distinct) features.
