# Electron Diffraction (SAED)

Modality-specific detail for [../SKILL.md](../SKILL.md). Selected area electron diffraction (SAED),
performed inside a TEM, uses electrons' strong interaction with matter to get diffraction from
nanoscale or even single-crystallite regions — complementary to bulk powder XRD, and often the only
option for nanocrystalline or small-volume samples. See `microscopy/references/tem.md` for the
imaging side of the same instrument.

## Core usage — indexing a diffraction pattern

```python
import numpy as np

def camera_length_calibration(measured_spot_distance_px, known_d_spacing_angstrom, pixel_size_um, wavelength_angstrom):
    """Electron diffraction pattern distances relate to d-spacing via the camera
    length, which must be calibrated against a known standard (e.g. evaporated Au)
    before absolute d-spacing measurements from an unknown sample are meaningful."""
    camera_constant = measured_spot_distance_px * pixel_size_um * known_d_spacing_angstrom
    return camera_constant  # use this calibration constant for subsequent patterns at the same camera length

def spot_to_d_spacing(spot_distance_px, camera_constant, pixel_size_um):
    return camera_constant / (spot_distance_px * pixel_size_um)

def index_zone_axis(d_spacings, angles_between_spots, candidate_structure):
    """Indexing (assigning hkl to each spot) requires matching observed d-spacings
    AND inter-spot angles against a candidate structure's calculated reflections —
    d-spacing alone is insufficient since multiple reflections can share a d-spacing.
    Software (e.g. CrystalMaker, JEMS, or pymatgen's diffraction module) handles this
    systematically; this illustrates the underlying two-constraint matching problem."""
    pass  # conceptual placeholder — real indexing needs a candidate structure and simulated pattern comparison
```

## Validation & Pitfalls

Canonical reference: Williams & Carter, *Transmission Electron Microscopy* (2nd ed., 2009), Part 3
(Diffraction), for SAED methodology and its practical constraints.

- **Camera length calibration drifts and must be checked per session, not assumed stable from a
  prior calibration** — a wrong camera constant produces systematically wrong d-spacings that can
  masquerade as a different, plausible-looking phase or lattice distortion.
- **Dynamical scattering (multiple scattering events within a thick sample) distorts relative spot
  intensities in ways kinematic diffraction theory (used for straightforward indexing) doesn't
  predict** — intensity-based structure analysis from SAED (as opposed to just position-based
  indexing) requires either very thin samples or dynamical-scattering-aware simulation; don't treat
  SAED spot intensities as directly comparable to XRD peak intensities.
- **A single zone-axis pattern under-determines the 3D crystal structure** — multiple zone axes (via
  sample tilting) are needed to fully index an unknown structure or distinguish between candidate
  space groups; a single pattern can be consistent with more than one structure.
- **Beam damage from the electron beam itself can alter or destroy the sample during acquisition**,
  particularly for beam-sensitive materials (many organics, some battery materials, zeolites) —
  verify the diffraction pattern is stable across repeated exposures before trusting it represents
  the undamaged material, and use low-dose techniques when beam sensitivity is a known concern.
