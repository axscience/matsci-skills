# matsci-skills

Open, plug-and-play [Agent Skills](https://github.com/anthropics/skills) for materials science
research — curated, validated knowledge that any AI agent (Claude Code, Cursor, a research-workspace
platform's own agent, etc.) can load to correctly analyze materials data, instead of generating
analysis code from parametric memory alone.

Clone the repo, point any agent at it, and it gains validated, ready-to-run materials-science
knowledge — across characterization techniques, synthesis/processing, computational materials
science, and cross-cutting statistics/informatics.

## What makes this different from a generic skills catalog

1. **Technique-first for characterization and simulation, cross-cutting for everything downstream.**
   Each characterization technique (`diffraction/`, `microscopy/`, `spectroscopy/`, ...) and each
   simulation approach (`computational-materials/`, `phase-field-calphad/`, ...) gets its own
   top-level folder, since acquisition and raw-data handling are technique-specific. Statistics, ML
   property prediction, data standards, and figures span every technique — those are cross-cutting
   skills referenced from technique skills, not restated in each one.
2. **Complete, not deferential to other repos.** Other agent-skills collections (e.g. K-Dense's
   `scientific-agent-skills`) cover some overlapping ground — a `pymatgen` skill, cheminformatics
   tooling. This repo doesn't skip that just because it exists elsewhere: a researcher using this
   repo alone should have what they need, so `materials-structure-analysis/` covers structure/
   composition analysis, symmetry, phase diagrams, and Materials Project queries as original content
   here.
3. **Every skill and reference carries a Validation & Pitfalls section.** A citation to the canonical
   standard or methods reference, and the common failure modes an agent (or a researcher) actually
   hits — not just tool usage, but where the usage goes wrong.

## Standalone by design

This repo has no dependency on any particular platform. Clone it and use it with anything that can
read Agent Skills:

```bash
git clone https://github.com/axscience/matsci-skills.git
```

- **Claude Code / Cursor / any Agent-Skills-compatible tool**: point it at this repo's root (or copy
  individual top-level skill folders into your tool's skills directory) and the agent picks up
  `SKILL.md` automatically.
- **A custom platform's own agent**: read `SKILL.md` frontmatter (see [CONTRIBUTING.md](CONTRIBUTING.md)
  for the schema) to retrieve and inject skill content into your own prompt/tool pipeline.

This repo is skills (knowledge), not tools (capability) — the same distinction as its sibling
`neuro-skills` repo: an agent needs its own code-execution environment with the right packages
installed (see `requirements.txt`), and network access for the database-query skills, on top of
these skills.

## Structure

```
<technique-or-method>/
  SKILL.md               # frontmatter + overview + when-to-use + core usage + routing table + validation
  references/               # optional — one file per sub-topic, loaded on demand
    <sub-topic>.md
docs/
  skills.md               # full index, by technique and by coverage matrix
plugin.json                # agent-plugins.org manifest
requirements.txt             # consolidated pip dependencies across all skills
scan_skills.py                # validator — frontmatter schema, folder consistency, dead links
```

## Status

20 top-level skills, 17 nested references — spanning diffraction (XRD/neutron/electron), microscopy
(SEM/TEM/AFM), spectroscopy (XPS/Raman/FTIR/NMR), thermal analysis, mechanical testing,
electrochemistry, synthesis/processing, polymer and semiconductor characterization, structure/
composition analysis (the pymatgen layer), DFT/MD/ML-interatomic-potentials, phase-field/CALPHAD,
finite element modeling, high-throughput/autonomous labs, materials databases and data standards,
statistics, informatics/ML, literature search, and figures. See [docs/skills.md](docs/skills.md) for
the full index, coverage matrix, and ownership notes on where overlapping content belongs. See
[CONTRIBUTING.md](CONTRIBUTING.md) to add a skill — known remaining gaps are listed at the bottom of
the skill index.

## License

MIT — see [LICENSE.md](LICENSE.md).
