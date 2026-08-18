# Density Functional Theory (DFT)

Modality-specific detail for [../SKILL.md](../SKILL.md). Covers convergence, functional selection,
and pseudopotential choice — the setup decisions that determine whether a DFT calculation's results
are trustworthy, more than the specific code used (VASP and Quantum Espresso conventions both shown;
`materials-structure-analysis/references/electronic-structure-io.md` covers the file I/O layer for both).

## Convergence testing (required before any production calculation)

```python
# Two independent convergence parameters must each be tested: plane-wave energy
# cutoff (ENCUT in VASP, ecutwfc in QE) and k-point mesh density. Converge one
# at a time, holding the other generously large, then confirm the pair together.

def energy_cutoff_convergence_series(cutoffs_ev, energies_ev_per_atom, tolerance_mev=1):
    """A cutoff series should show energy changes below `tolerance_mev` between
    consecutive points before calling it converged — inspect the actual series,
    don't just pick a commonly-cited cutoff value."""
    diffs = [abs(energies_ev_per_atom[i] - energies_ev_per_atom[i - 1]) * 1000 for i in range(1, len(cutoffs_ev))]
    converged_at = next((cutoffs_ev[i] for i, d in enumerate(diffs) if d < tolerance_mev), None)
    return {"converged_cutoff_ev": converged_at, "differences_mev": diffs}
```

## Functional selection

```python
# GGA (PBE): good general-purpose default, systematically underestimates band
#   gaps, struggles with strongly correlated electrons (many transition-metal
#   oxides) and van der Waals interactions without a correction.
# GGA+U: adds a Hubbard U correction for localized d/f electrons — necessary
#   for many transition-metal oxides to get qualitatively correct behavior
#   (e.g. correct insulating ground state), but U itself is a fitted/chosen
#   parameter, not a first-principles quantity, unless computed self-consistently.
# Hybrid functionals (HSE06): more accurate band gaps and electronic structure,
#   substantially more expensive — reserve for systems/properties where PBE's
#   known limitations (band gap, correlated electrons) actually matter to the question.
# van der Waals corrections (DFT-D3, etc.): required for systems where dispersion
#   forces matter (layered materials, molecular crystals, adsorption) — plain
#   GGA systematically underbinds these without a correction.
```

## Pseudopotential/basis-set considerations

```python
# Pseudopotential choice affects both accuracy and required energy cutoff —
# "hard" (more accurate, especially for elements with tightly bound core
# electrons) pseudopotentials require higher cutoffs than "soft" ones. Mixing
# pseudopotentials from different generations/families within one calculation,
# or comparing energies across calculations using different pseudopotentials,
# is a common, serious methodology error (see pitfalls).
```

## Validation & Pitfalls

Canonical references: Kresse & Furthmüller (1996), "Efficient iterative schemes for ab initio
total-energy calculations using a plane-wave basis set," *Physical Review B*, for VASP's underlying
method; Perdew, Burke & Ernzerhof (1996), "Generalized gradient approximation made simple," *Physical
Review Letters*, for the PBE functional; Cohen et al. (2012), "Insights into current limitations of
density functional theory," *Science*, for a candid survey of DFT's known failure modes.

- **Comparing total energies across calculations with different pseudopotentials, cutoffs, or
  k-point densities is not valid** — even the same code, same functional, different settings can
  differ by an amount comparable to the energy differences being studied (formation energies, phase
  stability). All entries in a comparison (e.g. feeding into `materials-structure-analysis`'s phase
  diagram workflow) must share methodology.
- **Convergence must be tested for the specific property being extracted, not assumed adequate from
  a general-purpose default.** A cutoff/k-mesh adequate for total energy convergence may be
  inadequate for forces, band structure detail, or magnetic moment convergence — these can require
  tighter settings than energy alone.
- **The PBE band-gap underestimation and self-interaction error in correlated systems are
  well-documented, systematic limitations, not calculation mistakes** — reporting a PBE band gap as
  if it were an accurate absolute prediction, or getting a qualitatively wrong (e.g. metallic instead
  of insulating) ground state for a correlated oxide without +U or a hybrid functional, are both
  predictable consequences of functional choice, not surprises to be debugged as if something went
  wrong.
- **Structural relaxation convergence criteria (force/energy thresholds) affect the final structure
  used for all downstream properties** — an under-converged relaxation feeds a not-quite-right
  structure into every subsequent calculation (band structure, phase diagram entry, etc.); check the
  relaxation actually converged (via `materials-structure-analysis/references/electronic-structure-io.md`'s
  convergence check) before trusting anything built on top of it.
- **Magnetic systems require explicit initialization of magnetic moments and checking for the
  correct (not just any) converged magnetic ground state** — DFT can converge to a metastable magnetic
  configuration (wrong spin ordering) that's a valid self-consistent solution but not the true ground
  state; test multiple initial magnetic configurations for systems where magnetic ordering matters.
