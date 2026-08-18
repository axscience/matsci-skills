# Transmission Electron Microscopy (TEM / STEM / EELS / EDS)

Modality-specific detail for [../SKILL.md](../SKILL.md). Covers bright-field/dark-field imaging
interpretation and STEM-based spectrum imaging (EELS, EDS) — the highest-resolution characterization
technique in this repo, and the one with the most involved data-analysis pipeline.

## Loading and processing spectrum images (HyperSpy)

```python
import hyperspy.api as hs

spectrum_image = hs.load("eels_spectrum_image.dm4")   # (x, y, energy_loss) datacube
spectrum_image.plot()

# Background subtraction before the ionization edge of interest (standard EELS practice)
background_removed = spectrum_image.isig[100.0:600.0].remove_background(
    signal_range=(100.0, 150.0), background_type="Power law"
)
```

## Elemental quantification from an EELS edge

```python
# Integrating the background-subtracted intensity under a known ionization edge,
# then normalizing by the tabulated partial ionization cross-section, gives
# elemental quantification — HyperSpy provides this via a fitted-model workflow:
elements = ["Fe", "O"]
spectrum_image.add_elements(elements)
model = spectrum_image.create_model()
model.fit()   # fits background + edges simultaneously, more robust than sequential subtraction
composition_maps = model.quantify()
```

## Bright-field / dark-field contrast

```python
# Bright-field: image formed from the direct (unscattered) beam — mass-thickness
# and diffraction contrast. Dark-field: image formed from a specific diffracted
# beam, selected via an objective aperture — highlights regions satisfying that
# specific diffraction condition (e.g. one grain orientation among many).
# This is an acquisition-mode choice, not a post-processing step — flag it
# explicitly when interpreting contrast in an image.
```

## Validation & Pitfalls

Canonical reference: Williams & Carter, *Transmission Electron Microscopy* (2nd ed., 2009), Parts
2-4 (Diffraction, Imaging, Spectrometry); Egerton, *Electron Energy-Loss Spectroscopy in the Electron
Microscope* (3rd ed., 2011), for EELS specifically.

- **Sample thickness strongly affects both image contrast and EELS quantification accuracy, and is
  rarely uniform.** Thicker regions increase plural/multiple scattering, distorting EELS background
  shape and biasing quantification; check relative thickness (e.g. via the EELS log-ratio method)
  across a spectrum image before trusting quantification uniformity.
- **Diffraction contrast in bright/dark-field images depends on local crystal orientation relative to
  the beam — the same defect or grain boundary can look completely different, or invisible, at a
  different sample tilt.** A single bright-field image is not a complete structural characterization;
  report the diffraction/tilt condition used, and note that some features are genuinely
  orientation-dependent to observe, not absent.
- **EELS background-subtraction model choice (power law is standard but not universal) affects
  extracted edge intensities, especially for edges close together or with a low signal-to-background
  ratio** — check the fit visually before trusting quantification, particularly for weak or
  overlapping edges.
- **Electron beam damage is a serious concern at TEM/STEM dose rates**, often worse than SEM given
  higher beam energies and longer dwell times for spectrum imaging — verify sample stability across
  the acquisition (e.g. compare a quick survey image before and after spectrum imaging) for
  beam-sensitive materials.
- **STEM spatial resolution in a spectrum image is limited by beam broadening within the sample, not
  just probe size** — thicker samples give worse effective spatial resolution than the nominal probe
  size suggests; don't assume nanometer probe size guarantees nanometer-resolution compositional maps
  on a thick sample.
