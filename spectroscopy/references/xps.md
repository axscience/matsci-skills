# X-Ray Photoelectron Spectroscopy (XPS)

Modality-specific detail for [../SKILL.md](../SKILL.md). XPS measures binding energy of
photoemitted electrons, giving elemental composition and oxidation state at the sample surface
(top few nm) — a surface-sensitive technique, distinct from bulk-sensitive spectroscopies.

## Charge correction (required before any binding-energy comparison)

```python
def charge_correct(binding_energies, reference_peak_measured, reference_peak_literature=284.8):
    """Non-conductive samples charge during XPS acquisition, shifting all peaks by
    a constant offset. Standard correction: shift so the adventitious carbon C 1s
    peak (or another internal reference) lands at its known literature value."""
    shift = reference_peak_literature - reference_peak_measured
    return binding_energies + shift
```

## Oxidation state assignment via peak position and fitting

```python
# Oxidation states shift binding energy by chemically meaningful, tabulated amounts
# (e.g. Fe metal ~706.8 eV vs Fe2O3 ~710.9 eV for Fe 2p3/2) — assignment requires
# comparing fitted peak positions against reference tables (e.g. NIST XPS Database),
# not just visual inspection.
FE_2P3_REFERENCE_EV = {"Fe(0)": 706.8, "Fe(II)": 709.5, "Fe(III)": 710.9}  # illustrative, check current NIST values

def assign_oxidation_state(fitted_peak_ev, reference_table, tolerance=0.3):
    matches = {state: abs(fitted_peak_ev - ev) for state, ev in reference_table.items()}
    best_match = min(matches, key=matches.get)
    return best_match if matches[best_match] <= tolerance else "unassigned — check reference table/tolerance"
```

## Quantitative surface composition (relative sensitivity factors)

```python
def xps_quantify(peak_areas, sensitivity_factors):
    """peak_areas, sensitivity_factors: dicts keyed by element (or core level).
    Atomic % from peak-area-to-sensitivity-factor ratios."""
    normalized = {el: peak_areas[el] / sensitivity_factors[el] for el in peak_areas}
    total = sum(normalized.values())
    return {el: (v / total) * 100 for el, v in normalized.items()}
```

## Validation & Pitfalls

Canonical reference: NIST X-ray Photoelectron Spectroscopy Database (for reference binding energies);
Moulder et al., *Handbook of X-ray Photoelectron Spectroscopy* (1992), for methodology.

- **Charge correction to the adventitious carbon C 1s peak is standard but not universally reliable**
  — the "known" C 1s reference value itself has some reported variability, and the adventitious
  carbon layer's composition/thickness varies by sample. For rigorous work, an internal standard
  specific to the sample, or charge-neutralization-system calibration, is more defensible than
  reflexively assuming C 1s = 284.8 eV.
- **XPS probes only the top few nanometers — surface composition often does not represent bulk
  composition**, especially after air exposure (surface oxidation, adventitious carbon/hydrocarbon
  contamination). A claim about bulk stoichiometry needs a bulk-sensitive technique (e.g. XRD, bulk
  chemical analysis), not XPS alone.
- **Peak fitting with multiple overlapping oxidation states is underdetermined without physically
  motivated constraints** (fixed spin-orbit splitting ratios and separations for p/d/f orbitals,
  shared FWHM across related components) — an unconstrained multi-peak fit can converge to a
  chemically implausible solution that nonetheless fits the data well; apply known physical
  constraints, don't let the fit run free.
- **Relative sensitivity factors are instrument- and sometimes even transmission-function-specific**
  — using a generic literature RSF table without confirming it matches (or is cross-calibrated for)
  the specific instrument used can introduce systematic quantification error.
