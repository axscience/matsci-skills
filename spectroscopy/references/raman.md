# Raman Spectroscopy

Modality-specific detail for [../SKILL.md](../SKILL.md). Raman measures inelastic light scattering
from vibrational/rotational modes — complementary to FTIR (different selection rules: Raman-active
modes involve a polarizability change, IR-active modes a dipole-moment change), and widely used for
carbon materials (graphene/graphite D/G bands), semiconductors, and mineral/phase identification.

## Cosmic ray spike removal (a Raman-specific artifact)

```python
import numpy as np

def remove_cosmic_ray_spikes(spectrum, threshold_sigma=8, window=5):
    """Cosmic ray hits on the detector produce narrow, high-intensity spikes
    (unlike any real Raman peak's width) — detect and remove via local outlier
    detection, distinct from the general baseline correction in ../SKILL.md."""
    cleaned = spectrum.copy()
    median_filtered = np.array([
        np.median(spectrum[max(0, i - window):i + window + 1])
        for i in range(len(spectrum))
    ])
    residual = spectrum - median_filtered
    threshold = threshold_sigma * np.std(residual)
    spike_indices = np.where(np.abs(residual) > threshold)[0]
    cleaned[spike_indices] = median_filtered[spike_indices]
    return cleaned, spike_indices
```

## Carbon material D/G band analysis (graphene, graphite, disordered carbon)

```python
def carbon_d_g_analysis(fitted_d_peak, fitted_g_peak):
    """D band (~1350 cm^-1, disorder-activated) to G band (~1580 cm^-1, sp2 C-C
    stretch) intensity ratio is a standard proxy for defect density/disorder in
    graphitic carbons — higher I(D)/I(G) indicates more disorder/smaller crystallite size."""
    id_ig_ratio = fitted_d_peak["amplitude"] / fitted_g_peak["amplitude"]
    return id_ig_ratio
```

## Validation & Pitfalls

Canonical reference: Ferrari & Robertson (2000), "Interpretation of Raman spectra of disordered and
amorphous carbon," *Physical Review B*, for carbon D/G band interpretation specifically; Long, *The
Raman Effect* (2002), for general Raman methodology.

- **Laser-induced heating can shift and broaden peaks, or damage the sample, especially at high laser
  power or on absorbing/dark samples** — check for peak position drift with increasing exposure time
  or power before trusting a measurement, and use the lowest power that gives adequate signal.
- **Fluorescence background (from the sample or impurities) can completely swamp weak Raman signal**
  — this is a different, usually much larger and more slowly varying background than the baseline
  correction in `../SKILL.md` is designed for; a strongly fluorescing sample may need a different
  excitation wavelength (fluorescence is wavelength-dependent, Raman shift is not) rather than more
  aggressive baseline subtraction.
- **The I(D)/I(G) ratio's relationship to crystallite size/disorder is non-monotonic across the full
  disorder range** (the Tuinstra-Koenig relationship holds in one regime, an inverse relationship in
  a more disordered regime) — know which regime a sample is likely in before applying a single
  interpretation of the ratio.
- **Peak position (not just presence) is often the diagnostic feature** (e.g. strain or doping shift
  the G band in graphene) — a peak-presence-only analysis misses information a peak-position fit
  would capture; fit peaks properly (per `../SKILL.md`) rather than just reporting visual peak lists.
