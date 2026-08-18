---
name: materials-data-standards
description: Data organization and interoperability standards for materials science — CIF (crystal structure files), OPTIMADE (a common query API standard across databases), and Materials Project/NOMAD-style schema conventions. Use this to understand how materials data is organized and made interoperable, distinct from materials-databases which covers querying specific live databases.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples target OPTIMADE API v1.x and standard CIF 2.0 conventions.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: materials-data-standards
---

# Materials Data Standards

## Overview

CIF (Crystallographic Information File) is the near-universal structure exchange format across
crystallography and materials science; OPTIMADE is a common query API specification adopted across
multiple materials databases (Materials Project, OQMD, AFLOW, and others) specifically so a single
query interface can search across them. Understanding both is what makes cross-database work in
`materials-databases` actually tractable, rather than requiring bespoke code per database.

## When to use this skill

Activate when the request involves:
- CIF format, crystallographic information file, OPTIMADE, cross-database query, data provenance,
  FAIR data principles
- File formats: `.cif`
- "Is this a valid CIF file," "query multiple databases with one interface," "what's OPTIMADE"

## Core usage

### CIF structure and validation

```python
from pymatgen.io.cif import CifParser

parser = CifParser("material.cif")
structures = parser.parse_structures(primitive=False)   # a CIF can contain more than one structure

# Check for parsing warnings — CIF files from different sources vary in
# completeness/strictness, and pymatgen surfaces issues rather than failing silently
warnings = parser.warnings
```

### OPTIMADE — one query interface across multiple databases

```python
import requests

def optimade_query(base_url, elements, response_fields="chemical_formula_reduced,elements"):
    """OPTIMADE-compliant databases (Materials Project, OQMD, AFLOW, and others)
    all expose this same query filter syntax — one query pattern works across
    providers, unlike each database's native API."""
    params = {
        "filter": f'elements HAS ALL {",".join(f\'"{e}"\' for e in elements)}',
        "response_fields": response_fields,
    }
    response = requests.get(f"{base_url}/structures", params=params)
    return response.json()["data"]

# Provider base URLs are listed in the OPTIMADE providers registry (optimade.org/providers)
mp_results = optimade_query("https://optimade.materialsproject.org/v1", ["Fe", "O"])
```

## Validation & Pitfalls

Canonical references: Hall, Allen & Brown (1991), "The Crystallographic Information File (CIF): a
new standard archive file for crystallography," *Acta Crystallographica Section A*, for CIF;
Andersen et al. (2021), "OPTIMADE, an API for exchanging materials data," *Scientific Data*, for
OPTIMADE.

- **CIF files vary widely in completeness and strictness across sources** — a CIF exported from one
  crystallography software package may lack fields (or use nonstandard tags) that another expects;
  always check for and handle parsing warnings rather than assuming a successfully-parsed CIF is
  fully complete.
- **A CIF can define a structure with partial occupancies or multiple disordered sites, which not
  every downstream tool handles the same way** — verify how partial/disordered occupancy is being
  interpreted (e.g. as an averaged structure vs. requiring explicit ordering) before using such a
  structure in a calculation that assumes fully ordered occupancy (most DFT codes do).
- **Not every materials database implements the full OPTIMADE specification, or implements it
  identically** — some fields/filter capabilities may be partial or provider-specific; check a given
  provider's OPTIMADE implementation notes rather than assuming full spec compliance guarantees
  identical query behavior across all providers.
- **OPTIMADE gives structural/compositional query capability across providers, but computed
  *property* values (energies, band gaps) still come with each provider's own methodology** — the
  same "mixing methodologies" pitfall from `materials-databases` and
  `materials-structure-analysis/references/phase-diagrams.md` applies just as much when results are
  aggregated via OPTIMADE as when queried natively; a unified query interface doesn't create unified
  methodology.
- **Provenance (which calculation, code version, and settings produced a given value) is often
  under-preserved when data moves between formats/databases** — NOMAD specifically emphasizes FAIR
  (Findable, Accessible, Interoperable, Reusable) provenance tracking for this reason; when
  provenance matters for a claim, prefer a source that preserves it explicitly over one that doesn't.
