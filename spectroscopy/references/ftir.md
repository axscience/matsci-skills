# Fourier-Transform Infrared Spectroscopy (FTIR)

Modality-specific detail for [../SKILL.md](../SKILL.md). FTIR measures infrared absorption from
vibrational modes with a changing dipole moment (complementary to Raman's polarizability-based
selection rule) — widely used for functional group identification in polymers, organics, and
surface-adsorbed species.

## ATR correction (attenuated total reflectance — the most common sampling mode)

```python
import numpy as np

def atr_correction(wavenumber, absorbance, refractive_index_sample=1.5, refractive_index_crystal=2.4):
    """ATR spectra have wavenumber-dependent penetration depth, distorting relative
    peak intensities (especially at low wavenumber) compared to transmission FTIR —
    ATR correction compensates for this before comparing to transmission-mode
    reference spectra or literature."""
    penetration_depth_factor = wavenumber / (
        2 * np.pi * refractive_index_crystal * np.sqrt(
            (refractive_index_crystal / refractive_index_sample) ** 2 - 1
        )
    )
    return absorbance * penetration_depth_factor  # simplified illustrative correction — see software (OMNIC, OPUS) for full implementation
```

## Functional group peak assignment

```python
# Peak assignment is fundamentally a lookup against known functional-group
# wavenumber ranges — a curated reference table, cross-checked against multiple
# peaks (a single peak is rarely diagnostic alone) is the standard approach.
FUNCTIONAL_GROUP_RANGES_CM1 = {
    "O-H stretch (broad)": (3200, 3550),
    "C-H stretch (aliphatic)": (2850, 2960),
    "C=O stretch": (1650, 1750),
    "C=C stretch (aromatic)": (1450, 1600),
    "C-O stretch": (1000, 1300),
}

def suggest_functional_groups(peak_wavenumber, reference_ranges=FUNCTIONAL_GROUP_RANGES_CM1):
    return [group for group, (lo, hi) in reference_ranges.items() if lo <= peak_wavenumber <= hi]
```

## Validation & Pitfalls

Canonical reference: Griffiths & de Haseth, *Fourier Transform Infrared Spectrometry* (2nd ed.,
2007), for methodology; Socrates, *Infrared and Raman Characteristic Group Frequencies* (3rd ed.,
2001), for peak-assignment reference tables.

- **A single peak in a broad, overlapping range (e.g. "C=O stretch") is rarely sufficient for
  unambiguous functional group assignment** — multiple corroborating peaks (and their relative
  intensities/shapes) are needed; a single-peak match against a reference table is a hypothesis, not
  a confirmed assignment.
- **ATR and transmission spectra are not directly comparable without correction** (see above) —
  comparing an uncorrected ATR spectrum against transmission-mode literature spectra can produce
  apparent intensity differences that are measurement-mode artifacts, not real compositional
  differences.
- **Atmospheric CO2 and water vapor absorb in specific FTIR regions (~2350 cm⁻¹ for CO2, broad bands
  ~3500-3900 and ~1300-1900 cm⁻¹ for water vapor) and require background subtraction** — an
  un-purged or poorly background-corrected measurement can show these as sample peaks; check for
  their characteristic sharp/broad signatures before attributing a peak in these regions to the
  sample.
- **Sample thickness/concentration must be within the linear (Beer-Lambert) regime for quantitative
  peak-area comparisons** — a saturated (fully absorbing) peak has a distorted, flattened shape that
  no longer scales linearly with concentration; check for peak saturation (unusually flat-topped
  peaks) before using peak area for quantification.
