# Materials Project Queries

Deeper detail for [../SKILL.md](../SKILL.md). Covers querying the Materials Project database via
`mp-api` — structures, computed properties, and phase-diagram entries pulled directly rather than
computed from scratch. For comparing Materials Project against other databases (AFLOW, OQMD, NOMAD,
JARVIS) side by side, see `materials-databases`.

## Setup

```python
from mp_api.client import MPRester

# Requires a free API key from materialsproject.org, set as MP_API_KEY env var
# or passed explicitly — never hardcode a key in committed code.
with MPRester() as mpr:
    ...
```

## Structure and summary property queries

```python
with MPRester() as mpr:
    docs = mpr.materials.summary.search(
        formula="Fe2O3",
        fields=["material_id", "structure", "energy_above_hull", "band_gap"],
    )
    for doc in docs:
        print(doc.material_id, doc.energy_above_hull, doc.band_gap)
```

## Fetching entries for a phase diagram (feeds directly into phase-diagrams.md's workflow)

```python
with MPRester() as mpr:
    entries = mpr.get_entries_in_chemsys(["Fe", "O"])   # all computed entries in the Fe-O chemical system

from pymatgen.analysis.phase_diagram import PhaseDiagram
pd = PhaseDiagram(entries)
```

## Bulk/high-throughput queries with explicit bounds

```python
with MPRester() as mpr:
    candidates = mpr.materials.summary.search(
        elements=["Li", "Fe", "P", "O"],
        energy_above_hull=(0, 0.05),   # near-hull candidates only — bound the query explicitly
        num_chunks=1, chunk_size=100,   # explicit size bound — see pitfalls on unbounded queries
        fields=["material_id", "formula_pretty", "energy_above_hull"],
    )
```

## Validation & Pitfalls

Canonical reference: Jain et al. (2013), "Commentary: The Materials Project: A materials genome
approach to accelerating materials innovation," *APL Materials* — the foundational Materials Project
paper.

- **Never hardcode or commit an API key.** Read it from an environment variable or a local,
  gitignored secrets file — the same discipline as any other credentialed API in this repo's sibling
  skills (e.g. neuroscience's dataset-access skills).
- **An unbounded high-throughput query can return an unexpectedly large result set and consume
  significant time/bandwidth** — always bound queries explicitly (by chemical system, property range,
  or an explicit `chunk_size`/limit) rather than fetching "everything matching a broad filter" during
  exploration.
- **Materials Project computed properties use specific, versioned calculation settings (functional,
  convergence parameters) that can change between database releases** — a property value pulled today
  may differ from the same material's value pulled a year from now if the underlying calculation was
  redone with updated settings. For reproducible work, record the database version/access date
  alongside any value used in a downstream analysis.
- **`energy_above_hull` values from a bulk MP query reflect MP's own phase diagram construction
  (built from MP's full entry set for that chemical system)** — mixing an MP-sourced hull value with
  your own locally-computed entries in the same stability analysis (per `phase-diagrams.md`) requires
  the same calculation methodology across both, or the comparison is invalid (same pitfall as in that
  reference, specifically relevant here since it's the most common way MP data gets misused).
- **A `material_id` is stable, but the material it refers to can have its computed data revised
  across database updates** — don't assume a cached/older `material_id` → property mapping remains
  current without re-querying.
