# Scanning Electron Microscopy (SEM)

Modality-specific detail for [../SKILL.md](../SKILL.md). Covers secondary/backscattered electron
contrast interpretation and EDS (energy-dispersive X-ray spectroscopy) elemental mapping, both
acquired on the same instrument.

## EDS quantification (elemental composition from X-ray spectrum)

```python
import numpy as np

def eds_quantify_standardless(peak_intensities, k_factors):
    """Standardless (ZAF/k-factor-based) quantification — a common but approximate
    method. peak_intensities and k_factors: dicts keyed by element symbol.
    Standardless quantification typically carries larger uncertainty than
    standards-based quantification — see pitfalls."""
    corrected = {el: peak_intensities[el] * k_factors[el] for el in peak_intensities}
    total = sum(corrected.values())
    return {el: (v / total) * 100 for el, v in corrected.items()}  # atomic or weight %, depending on k-factor convention
```

## EDS elemental map to particle-composition correlation

```python
def map_composition_per_particle(elemental_maps, particle_labels):
    """elemental_maps: dict of element -> 2D intensity array, same shape as particle_labels.
    Returns mean elemental signal within each segmented particle (see ../SKILL.md's
    segment_and_measure for producing particle_labels)."""
    from skimage.measure import regionprops
    results = {}
    for element, intensity_map in elemental_maps.items():
        results[element] = {
            region.label: intensity_map[particle_labels == region.label].mean()
            for region in regionprops(particle_labels)
        }
    return results
```

## Validation & Pitfalls

Canonical reference: Goldstein et al., *Scanning Electron Microscopy and X-Ray Microanalysis*
(4th ed., 2017), Chapters on EDS quantification specifically.

- **Standardless EDS quantification typically has ~5-10% relative uncertainty even under good
  conditions, and substantially worse for light elements (below Na) or overlapping peaks** — report
  it as approximate, and use standards-based quantification when accuracy below a few percent
  matters for a specific claim.
- **The interaction volume (where X-rays actually originate) is larger than the beam spot and depends
  on accelerating voltage and sample density** — a "point" EDS measurement at high kV on a
  low-density sample can sample a much larger volume than the visible beam position suggests,
  degrading spatial resolution claims for compositional mapping.
- **Charging artifacts on non-conductive samples distort both imaging contrast and can shift/distort
  EDS peaks** — an uncoated or poorly grounded insulating sample produces artifacts that can look
  like real topographic or compositional features; confirm appropriate coating/grounding for
  non-conductive samples before interpreting results.
- **Secondary electron (topographic contrast) and backscattered electron (compositional/Z contrast)
  images answer different questions and are easy to conflate** — a bright region in backscattered
  imaging indicates higher average atomic number, not necessarily a topographic feature; confirm
  which detector/mode produced a given image before interpreting contrast.
