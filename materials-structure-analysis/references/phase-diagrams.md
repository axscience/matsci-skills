# Phase Diagrams and Stability Analysis

Deeper detail for [../SKILL.md](../SKILL.md). Covers constructing phase diagrams from computed
energies and determining thermodynamic stability — the standard high-throughput screening question
in computational materials science: "is this candidate composition/structure stable?"

## Building a phase diagram from computed entries

```python
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter
from pymatgen.entries.computed_entries import ComputedEntry

entries = [
    ComputedEntry("Fe", -8.3),
    ComputedEntry("O2", -9.9),
    ComputedEntry("Fe2O3", -41.2),
    ComputedEntry("FeO", -16.9),
    # in practice, entries typically come from a database query — see materials-project-queries.md
]

pd = PhaseDiagram(entries)
plotter = PDPlotter(pd)
plotter.get_plot()
```

## Stability and decomposition analysis

```python
target_entry = ComputedEntry("FeO", -16.9)

e_above_hull = pd.get_e_above_hull(target_entry)   # eV/atom above the convex hull — 0 = stable
decomposition = pd.get_decomposition(target_entry.composition)  # what it would decompose into, if unstable

print(f"E above hull: {e_above_hull:.4f} eV/atom")
if e_above_hull > 0:
    print("Decomposes into:", decomposition)
```

## Grand potential phase diagrams (open-system stability, e.g. vs. an oxygen reservoir)

```python
from pymatgen.analysis.phase_diagram import GrandPotentialPhaseDiagram
from pymatgen.core import Element

o2_chemical_potential = -9.9  # eV, e.g. from a computed O2 reference energy at a given condition
gpd = GrandPotentialPhaseDiagram(entries, {Element("O"): o2_chemical_potential})
```

## Validation & Pitfalls

Canonical reference: Ong et al. (2008), "Li-Fe-P-O2 phase diagram from first principles calculations,"
*Chemistry of Materials* — an early, representative application of this exact pymatgen phase-diagram
workflow.

- **Energy above hull depends entirely on the energies of the entries used to build the hull —
  mixing energies from different calculation settings (different DFT functional, pseudopotentials, or
  even different codes) produces a meaningless hull.** All entries in a `PhaseDiagram` must come from
  a consistent calculation methodology; this is the single most common way this analysis goes wrong.
- **A small positive energy above hull (a few meV/atom to ~25-50 meV/atom, roughly) doesn't
  necessarily mean a material is unsynthesizable** — DFT energies carry their own uncertainty, and
  many experimentally realized materials sit slightly above the computed hull (metastable phases,
  kinetically stabilized). Treat "on the hull" as a useful screening heuristic, not a hard
  synthesizability criterion, and check against known metastable-phase literature for a specific
  system before over-interpreting a small positive value.
- **Finite-temperature effects (vibrational free energy, configurational entropy) are absent from a
  standard 0K DFT-energy phase diagram** — a compound stable at 0K can become unstable at synthesis/
  operating temperature, and vice versa; for temperature-sensitive stability questions, this
  static-energy hull is a starting point, not the full answer (see CALPHAD-based approaches in
  `phase-field-calphad` for temperature-dependent phase equilibria).
- **Grand potential (open-system) phase diagrams require a physically meaningful chemical potential
  for the "open" element, and the choice of that value changes the result substantially** — an
  arbitrary or poorly justified chemical potential value produces a stability assessment that doesn't
  correspond to any real synthesis condition; ground the chemical potential in an actual reference
  state relevant to the question (e.g. O2 partial pressure at a synthesis temperature).
