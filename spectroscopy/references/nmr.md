# Solid-State NMR

Modality-specific detail for [../SKILL.md](../SKILL.md). Solid-state NMR probes local atomic
environment via nuclear spin, giving information complementary to diffraction (works on amorphous
and disordered materials, sensitive to short-range order that diffraction, a long-range-order probe,
can miss).

## Chemical shift referencing

```python
def reference_chemical_shift(raw_shift_ppm, standard_measured_ppm, standard_literature_ppm=0.0):
    """Chemical shifts are reported relative to a standard reference compound
    (e.g. TMS for 1H/13C, or a nucleus-specific standard) — like XPS charge
    correction, this is a required calibration step, not optional post-processing."""
    return raw_shift_ppm - standard_measured_ppm + standard_literature_ppm
```

## Magic-angle spinning (MAS) sideband identification

```python
def identify_spinning_sidebands(peak_positions_hz, spinning_rate_hz, isotropic_peak_hz):
    """MAS spinning sidebands appear at isotropic_peak +/- n*spinning_rate for
    integer n — must be distinguished from real chemically distinct peaks, which
    don't shift when spinning rate changes."""
    sidebands = []
    for peak in peak_positions_hz:
        offset = peak - isotropic_peak_hz
        n = offset / spinning_rate_hz
        if abs(n - round(n)) < 0.05 and round(n) != 0:
            sidebands.append({"peak_hz": peak, "sideband_order": round(n)})
    return sidebands
```

## Validation & Pitfalls

Canonical reference: Duer (ed.), *Solid-State NMR Spectroscopy: Principles and Applications* (2002),
for methodology; MacKenzie & Smith, *Multinuclear Solid-State NMR of Inorganic Materials* (2002),
for materials-specific applications.

- **Spinning sidebands can be mistaken for real chemically distinct sites if spinning rate isn't
  varied to confirm.** The standard check — acquire at two different MAS rates and confirm which
  peaks shift (sidebands) vs. stay fixed (real isotropic peaks) — is not optional when sidebands might
  overlap with real peaks of interest.
- **Quantitative solid-state NMR requires accounting for relaxation times (T1) in the pulse sequence
  recycle delay** — an insufficient recycle delay under-represents nuclei with long T1, systematically
  biasing quantitative site-population estimates; confirm the recycle delay is appropriate (typically
  ≥5×T1) before treating peak areas as quantitative.
- **Cross-polarization (CP) experiments (common for enhancing sensitivity of low-abundance/
  low-gyromagnetic-ratio nuclei like 13C, 29Si) are not quantitative by default** — CP efficiency
  depends on the local dipolar coupling environment, which varies by site; a CP spectrum's peak areas
  reflect a mix of population and CP efficiency, not population alone, unless specifically calibrated.
- **Different nuclei require fundamentally different experimental considerations** (quadrupolar
  nuclei like 27Al or 17O have additional line-broadening mechanisms beyond what spin-1/2 nuclei like
  1H/13C/29Si experience) — a workflow validated for one nucleus type doesn't automatically transfer;
  check whether the nucleus of interest is quadrupolar before assuming standard spin-1/2 methodology
  applies.
