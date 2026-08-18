---
name: diffraction
description: Diffraction-based structure characterization — X-ray (XRD), neutron, and electron (SAED) diffraction. Space group determination, Rietveld refinement, phase identification, and CIF handling, with references per diffraction type. Use this for any technique that determines crystal structure from a diffraction pattern.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: References target GSAS-II (Python, open-source), with notes on FullProf/TOPAS conventions since they're common in the field.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: diffraction
---

# Diffraction

## Overview

Diffraction techniques determine atomic structure by measuring how a sample scatters X-rays,
neutrons, or electrons. All three share the underlying crystallography (Bragg's law, space groups,
structure factors) but differ in what they're sensitive to (X-rays: electron density; neutrons:
nuclear positions, strong for light elements like H/Li; electrons: strong scattering, useful for
nanocrystals and local/SAED work) and in practical acquisition constraints. This skill covers what's
shared — space groups, Rietveld refinement, CIF format — and routes to type-specific references.

## When to use this skill

Activate when the request involves:
- XRD, X-ray diffraction, powder diffraction, neutron diffraction, SAED, electron diffraction
- Terms: Bragg's law, space group, Rietveld refinement, structure factor, d-spacing, CIF
- File formats: `.cif`, `.xrdml`, `.raw` (diffractometer formats), `.gsas`
- "Index this diffraction pattern," "refine this crystal structure," "identify this phase"

## Which reference to read

| You have... | Read |
|---|---|
| Powder or single-crystal X-ray diffraction | [references/xrd.md](references/xrd.md) |
| Neutron diffraction | [references/neutron-diffraction.md](references/neutron-diffraction.md) |
| Electron diffraction (SAED, in a TEM) | [references/electron-diffraction.md](references/electron-diffraction.md) — also see `microscopy/references/tem.md` |

## Core usage — shared crystallography

### Reading and writing structures (CIF format)

```python
from pymatgen.core import Structure

structure = Structure.from_file("material.cif")
print(structure.get_space_group_info())   # (symbol, number)
structure.to(filename="material_out.cif")
```

Structure/composition object handling is covered in depth in `materials-structure-analysis` — this
skill focuses on the diffraction-specific measurement and refinement workflow.

### Rietveld refinement (GSAS-II, scripted)

```python
import GSASIIscriptable as G2sc

gpx = G2sc.G2Project(newgpx="refinement.gpx")
hist = gpx.add_powder_histogram("pattern.xrdml", "instrument.prm")
phase = gpx.add_phase("material.cif", histograms=[hist])

hist.set_refinements({"Background": {"no. coeffs": 6, "refine": True}})
hist.set_refinements({"Cell": True})   # refine lattice parameters
gpx.do_refinements([{}])   # execute the refinement steps queued above
gpx.save()

r_wp = hist.get_wR()   # weighted-profile R-factor — goodness of fit, see pitfalls
```

## Validation & Pitfalls

Canonical reference: Toby & Von Dreele (2013), "GSAS-II: the genesis of a modern open-source all
purpose crystallography software package," *Journal of Applied Crystallography*, for Rietveld
methodology and tooling; Young (ed.), *The Rietveld Method* (1993), for the foundational method.

- **A low R-factor (Rwp) does not by itself mean the refined structure is correct.** Rwp measures
  fit quality against the data, but an over-parameterized model (too many refined variables for the
  data quality) can achieve a low Rwp while being physically implausible. Check the goodness-of-fit
  (GOF/chi-squared) and refine parameters in a stable, physically motivated order (scale → background
  → lattice → peak shape → atomic positions → thermal parameters), not all at once.
- **Preferred orientation (non-random crystallite orientation in a powder sample) systematically
  distorts relative peak intensities** and, if not modeled, biases refined atomic positions and
  site occupancies. Check for it (peak intensity ratios inconsistent with the structure model) before
  trusting a refinement, especially for plate- or needle-shaped crystallites.
- **Phase identification from peak positions alone is ambiguous when multiple candidate phases share
  similar unit cells** — always cross-check against a reference database (ICDD PDF, or a structure
  database — see `materials-databases`) rather than accepting the closest peak-position match without
  verifying peak intensity ratios too.
- **Instrument contribution to peak broadening must be characterized (e.g. via a standard reference
  material) before extracting sample-intrinsic broadening** (crystallite size, microstrain) — treating
  raw peak width as purely sample-intrinsic overestimates strain/underestimates crystallite size.
