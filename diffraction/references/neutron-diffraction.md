# Neutron Diffraction

Modality-specific detail for [../SKILL.md](../SKILL.md). Neutrons scatter off atomic nuclei (not
electron density, as in XRD), giving different — and often complementary — sensitivity: strong
scattering from light elements (H, Li, O) that scatter X-rays weakly, sensitivity to magnetic
structure via neutron spin, and roughly element-independent scattering lengths (no monotonic
increase with atomic number the way X-ray form factors have).

## Core usage — magnetic structure refinement (the most distinctive neutron-specific workflow)

```python
# Magnetic Rietveld refinement adds magnetic scattering to the nuclear (structural)
# scattering already covered in ../SKILL.md's core Rietveld workflow — GSAS-II and
# FullProf both support this via a magnetic structure/propagation vector model.
import GSASIIscriptable as G2sc

gpx = G2sc.G2Project(newgpx="magnetic_refinement.gpx")
hist = gpx.add_powder_histogram("neutron_pattern.dat", "instrument.prm")
phase = gpx.add_phase("nuclear_structure.cif", histograms=[hist])
# Adding a magnetic phase/propagation vector requires GSAS-II's magnetic structure
# tools specifically — see GSAS-II documentation for the current magnetic-phase API,
# since this workflow is more involved than nuclear-only refinement.
```

## Isotope-specific scattering length lookup

```python
# Unlike X-ray form factors (smoothly increasing with atomic number), neutron
# scattering lengths vary non-monotonically and differ by isotope, not just element —
# this matters for both experimental design (contrast, e.g. H/D substitution) and
# structure refinement (wrong isotope assumption gives wrong intensities).
NEUTRON_SCATTERING_LENGTHS_FM = {
    "H": -3.74, "D": 6.67,   # hydrogen vs deuterium — dramatically different, used for contrast
    "O": 5.80, "Li": -1.90, "Fe": 9.45,
}  # abbreviated — full tables in NIST/ILL neutron scattering length references
```

## Validation & Pitfalls

Canonical reference: Sears (1992), "Neutron scattering lengths and cross sections," *Neutron News*,
for scattering-length data; Rietveld (1969), "A profile refinement method for nuclear and magnetic
structures," *Journal of Applied Crystallography*, for the original magnetic Rietveld method.

- **Neutron sources (reactor vs. spallation) produce fundamentally different data — constant
  wavelength vs. time-of-flight — requiring different instrument-resolution modeling.** Code and
  refinement setups aren't interchangeable between the two without adapting the instrument parameter
  file; using a constant-wavelength refinement template on time-of-flight data (or vice versa)
  produces a nonsensical fit.
- **H/D contrast variation is a deliberate experimental technique, not just a data quirk** —
  substituting deuterium for hydrogen changes scattering contrast dramatically (see the table above),
  used intentionally in soft-matter and biological neutron scattering. Confirm which isotope is
  actually present in a sample before assuming standard hydrogen scattering lengths apply.
- **Magnetic structure refinement requires a propagation vector and magnetic space group
  determination that has no XRD analog** — this is a genuinely harder, more manual process than
  nuclear-only refinement (multiple candidate magnetic structures often need to be tested against the
  data), not just "the same Rietveld workflow with an extra checkbox."
- **Sample volume/mass requirements for neutron diffraction are typically much larger than for XRD**
  (weaker interaction with matter, requiring more scattering material or longer counting times) —
  this is an experimental-design constraint to flag, not purely an analysis one, and affects what
  sample sizes are even feasible to measure.
