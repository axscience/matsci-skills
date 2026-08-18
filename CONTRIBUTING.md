# Contributing a skill

A skill is one materials-science technique family or cross-cutting methodology, documented so an
AI agent can use it correctly. This doc is the spec for adding or editing one.

## Design principle

**Technique-first for characterization and simulation, cross-cutting for everything downstream of
raw results.** Each characterization technique (diffraction, microscopy, spectroscopy...) and each
simulation approach (DFT, MD, phase-field...) gets its own top-level folder, since the acquisition
and raw-data-handling steps are technique-specific and don't generalize. Statistics, ML property
prediction, data standards, and figures span every technique — those live in their own cross-cutting
skills (`materials-stats/`, `materials-informatics-ml/`, `materials-data-standards/`,
`materials-figures/`) referenced from technique skills rather than restated in each one.

**Completeness over avoiding overlap with other repos.** A researcher using this repo shouldn't need
to also clone a different skills repo to get core functionality — so this repo includes a full
`materials-structure-analysis/` skill covering what `pymatgen` provides (structure/composition
objects, symmetry, phase diagrams, electronic-structure I/O, Materials Project queries), written as
original content here rather than assumed to live elsewhere. Other repos covering similar library
ground (e.g. K-Dense's `scientific-agent-skills`) don't change what belongs in this one — the bar is
"does a materials researcher need this," not "is it covered somewhere else already."

## 1. Pick where the skill lives

- **New characterization technique or simulation method, not yet covered**: new top-level folder.
- **New sub-topic within an existing technique family** (e.g. a new diffraction variant): a new file
  under that skill's `references/`, not a new top-level folder. Check the routing table first.
- **New cross-cutting method used across ≥3 technique families**: new top-level folder, or a
  reference under an existing cross-cutting skill if it fits.
- **Unsure**: open an issue before writing content.

## 2. Folder layout

```
<technique-or-method>/
  SKILL.md              # required — overview + when-to-use + core usage + routing table (if references/ exists) + validation
  references/             # optional — one file per sub-topic, loaded on demand
    <sub-topic>.md
```

## 3. `SKILL.md` frontmatter

```yaml
---
name: skill-name
description: What this covers and when to reach for it over a neighboring skill. Name the neighbor explicitly if there's overlap.
license: <license of the underlying software/technique, e.g. "MIT">
allowed-tools: Read Write Edit Bash   # only the tools this skill's workflow actually needs
compatibility: Version/environment notes for the underlying software, if relevant
metadata:
  version: "1.0"
  skill-author: <your name or handle>
  modality: <matches the top-level folder name exactly>
---
```

## 4. `SKILL.md` body

Required sections:

1. **Overview** — what this covers and when to use it over a neighboring skill.
2. **When to use this skill** — a bulleted trigger list: keywords/terms, file extensions, and task
   phrases that should surface this skill. Separate from and more literal than the frontmatter
   `description`.
3. **A routing table**, if this skill has a `references/` folder — right at the top of Core usage.
   Not optional for multi-reference skills.
4. **Core usage** — the shared/entry-point guidance, with real worked code.
5. **Validation & Pitfalls** — required, not optional, at both the top-level SKILL.md and in every
   reference file. At minimum: a citation to the canonical methods reference or standard, and the
   3-5 most common ways this goes wrong in practice.

## 5. Agent behavior when a skill is loaded

This applies once, repo-wide — don't restate it inside individual skills. Before writing code or
analysis for anything beyond a trivial, unambiguous request, an agent following any skill in this
repo should: state the research question or goal, justify why this technique/method fits the sample
and question, declare the expected output, note assumptions and limitations (sample prep quality,
instrument calibration, whatever the Validation & Pitfalls section flags), and confirm the plan
before executing anything with real analytic-choice consequences.

## 6. Before opening a PR

```bash
python scan_skills.py
```

It checks: frontmatter is present and well-formed, `metadata.modality` matches the top-level folder,
a routing table exists in `SKILL.md` when `references/` is non-empty, required body sections exist
in every `SKILL.md` and reference file, and internal links resolve to real files.

## 7. Scope

This repo is materials science only — characterization, synthesis/processing, computational
materials science, and the cross-cutting methodology that spans them. Biomaterials (materials/
biology boundary — biocompatibility, scaffold characterization) is explicitly out of scope, same
reasoning as excluding genomics from a neuroscience skills repo: it belongs in a life-sciences-
focused repo, not here.
