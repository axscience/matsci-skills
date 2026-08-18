---
name: materials-databases
description: Querying public materials databases beyond Materials Project — AFLOW, OQMD, NOMAD, and JARVIS — plus cross-database comparison conventions. These are live, API-integrated compute resources researchers query directly, not one-time-download datasets. For Materials Project specifically, see materials-structure-analysis/references/materials-project-queries.md.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use each database's own Python client/REST API as of 2026 — check current documentation for endpoint/schema changes, which happen more often for these than for stable desktop software.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: materials-databases
---

# Materials Databases

## Overview

Unlike neuroscience's mostly-passive public datasets, several materials databases are live APIs that
a workflow queries directly and repeatedly, not a corpus downloaded once — hence this being a full
skill rather than an appendix to a data-standards skill. Materials Project queries are covered in
`materials-structure-analysis/references/materials-project-queries.md`; this skill covers the other
major databases and how to compare results across them.

## When to use this skill

Activate when the request involves:
- AFLOW, OQMD, Open Quantum Materials Database, NOMAD, JARVIS, ICSD, Matbench
- Terms: high-throughput database, DFT-computed properties (from a database, not your own calculation),
  benchmark dataset, FAIR data
- "Query AFLOW/OQMD/NOMAD/JARVIS for...," "compare this property across databases," "find a benchmark dataset"

## Core usage

### AFLOW

```python
from aflow import search, K

results = search(catalog="icsd").filter(K.species == ("Fe", "O")).select(K.energy_atom, K.spacegroup_relax)
for entry in results:
    print(entry.auid, entry.energy_atom, entry.spacegroup_relax)
```

### OQMD (Open Quantum Materials Database)

```python
import requests

response = requests.get(
    "http://oqmd.org/oqmdapi/formationenergy",
    params={"composition": "Fe2O3", "fields": "name,delta_e,spacegroup"},
)
entries = response.json()["data"]
```

### NOMAD

```python
import requests

response = requests.post(
    "https://nomad-lab.eu/prod/v1/api/v1/entries/query",
    json={"query": {"results.material.elements": {"all": ["Fe", "O"]}}, "pagination": {"page_size": 20}},
)
entries = response.json()["data"]
```

### JARVIS (NIST)

```python
from jarvis.db.figshare import data as jarvis_data

dft_3d = jarvis_data("dft_3d")   # downloads/caches the JARVIS-DFT 3D materials dataset
fe_containing = [entry for entry in dft_3d if "Fe" in entry["formula"]]
```

### Matbench — standardized ML benchmark suite

```python
from matbench.bench import MatbenchBenchmark

mb = MatbenchBenchmark(autoload=False)
for task in mb.tasks:
    task.load()   # loads a specific standardized materials-property-prediction benchmark
```

## Validation & Pitfalls

Canonical references: Curtarolo et al. (2012), "AFLOW: An automatic framework for high-throughput
materials discovery," *Computational Materials Science*; Saal et al. (2013), "Materials design and
discovery with high-throughput density functional theory: the Open Quantum Materials Database
(OQMD)," *JOM*; Draxl & Scheffler (2019), "The NOMAD laboratory: from data sharing to artificial
intelligence," *Journal of Physics: Materials*; Choudhary et al. (2020), "The joint automated
repository for various integrated simulations (JARVIS) for data-driven materials design," *npj
Computational Materials*.

- **Different databases use different DFT methodologies (functional, pseudopotentials, convergence
  settings), so a property value for the "same" material can differ meaningfully across databases —
  this is not noise or an error in one of them, it's a real methodology difference.** Never mix
  entries from different databases into the same phase-diagram or stability analysis (same
  methodology-consistency principle as `materials-structure-analysis/references/phase-diagrams.md`);
  cross-database comparison is useful for sanity-checking a value's robustness, not for building a
  single consistent dataset.
- **API schemas and endpoints for these databases change over time, sometimes without long
  deprecation notices** — code that worked against a database's API a year ago may fail or return
  differently structured data today; verify against current documentation rather than assuming a
  cached example (including the ones above) is still exactly correct.
- **Database coverage is not uniform across chemical space** — some databases emphasize inorganic
  crystals (Materials Project, OQMD, AFLOW), others are broader in scope (NOMAD accepts many
  calculation types and codes) or benchmark-focused (Matbench). Check whether a database actually
  covers the chemistry/property of interest before assuming an absence of results means the material
  is unstudied, rather than just absent from that particular database.
- **A high-throughput database entry represents one calculation, not a validated, peer-reviewed
  result** — treat database-sourced values with the same skepticism as any single calculation (see
  `computational-materials/references/dft.md`'s convergence/methodology caveats), not as ground truth
  simply because it's in a large curated database.
- **Rate limits and bulk-query etiquette matter for these APIs** — an unbounded or high-frequency
  query pattern can get an API key throttled or blocked; bound queries explicitly and check each
  database's documented rate limits before running a large automated query campaign.
