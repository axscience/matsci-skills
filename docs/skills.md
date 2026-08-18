# Skill index

20 top-level skills, 17 nested references. Run `python scan_skills.py` to validate before
regenerating by hand.

## By technique family

| Skill | Description |
|---|---|
| [diffraction](../diffraction/SKILL.md) | XRD, neutron, and electron diffraction — space groups, Rietveld refinement, CIF. |
| [microscopy](../microscopy/SKILL.md) | SEM, TEM (incl. STEM/EELS/EDS), AFM — drift correction, segmentation, feature sizing. |
| [spectroscopy](../spectroscopy/SKILL.md) | XPS, Raman, FTIR, solid-state NMR — peak fitting, baseline correction, assignment. |
| [thermal-analysis](../thermal-analysis/SKILL.md) | DSC, TGA, dilatometry — Tg/melting/crystallization, mass-loss steps, CTE. |
| [mechanical-testing](../mechanical-testing/SKILL.md) | Tensile/compression, nanoindentation, fatigue, fracture toughness, Weibull statistics. |
| [electrochemistry](../electrochemistry/SKILL.md) | Cyclic voltammetry, battery cycling, EIS, corrosion (Tafel analysis). |
| [synthesis-processing](../synthesis-processing/SKILL.md) | Solid-state synthesis, sol-gel, CVD/PVD, epitaxy — the acquisition stage. |
| [polymer-characterization](../polymer-characterization/SKILL.md) | GPC/SEC molecular weight, rheology, DMA — polymer-specific tooling. |
| [semiconductor-characterization](../semiconductor-characterization/SKILL.md) | Hall effect, four-point probe, I-V/C-V — carrier transport and device measurement. |
| [materials-structure-analysis](../materials-structure-analysis/SKILL.md) | Structure/composition objects, symmetry, phase diagrams, electronic-structure I/O, Materials Project queries. |
| [computational-materials](../computational-materials/SKILL.md) | DFT, classical/reactive MD, ML interatomic potentials. |
| [phase-field-calphad](../phase-field-calphad/SKILL.md) | CALPHAD thermodynamic phase equilibria, phase-field microstructure evolution. |
| [finite-element-modeling](../finite-element-modeling/SKILL.md) | Continuum-scale mechanical/thermal/multiphysics FEA. |
| [high-throughput-autonomous-labs](../high-throughput-autonomous-labs/SKILL.md) | Combinatorial synthesis, robotic experimentation, closed-loop active learning. |
| [materials-databases](../materials-databases/SKILL.md) | AFLOW, OQMD, NOMAD, JARVIS, Matbench queries. |
| [materials-data-standards](../materials-data-standards/SKILL.md) | CIF format, OPTIMADE cross-database query standard. |
| [materials-stats](../materials-stats/SKILL.md) | Design of experiments, uncertainty propagation, replicate-measurement statistics. |
| [materials-informatics-ml](../materials-informatics-ml/SKILL.md) | Property-prediction ML (descriptor-based, GNN), generative materials design. |
| [materials-lit-search](../materials-lit-search/SKILL.md) | Literature search query formulation and synthesis discipline. |
| [materials-figures](../materials-figures/SKILL.md) | Phase diagrams, pole figures, stress-strain curves, band structure/DOS plots. |

## Coverage matrix — where each concern lives, by technique

| Technique family | Acquisition | Analysis | Stats | Visualization |
|---|---|---|---|---|
| Diffraction (XRD/neutron/electron) | scan parameters, in-skill | Rietveld refinement, in-skill | → `materials-stats` | → `materials-figures` |
| Microscopy (SEM/TEM/AFM) | imaging conditions, in-skill | segmentation, particle sizing, in-skill | → `materials-stats` | → `materials-figures` |
| Spectroscopy (XPS/Raman/FTIR/NMR) | acquisition params, in-skill | peak fitting/assignment, in-skill | → `materials-stats` | → `materials-figures` |
| Mechanical testing | test setup, in-skill | stress-strain, fatigue-life, in-skill | Weibull → in-skill; general → `materials-stats` | → `materials-figures` |
| Electrochemistry | cell/electrode setup, in-skill | EIS equivalent-circuit, Tafel, in-skill | → `materials-stats` | → `materials-figures` |
| Polymers | sample prep, in-skill | GPC/rheology/DMA, in-skill | → `materials-stats` | → `materials-figures` |
| Semiconductors | contact setup, in-skill | Hall/4pp/I-V extraction, in-skill | → `materials-stats` | → `materials-figures` |
| DFT / MD / ML potentials | input file conventions, in-skill | property extraction, in-skill | uncertainty → `materials-stats` | band structure/DOS → `materials-figures` |
| Any technique | → `synthesis-processing` for how the sample was made | → `materials-informatics-ml` for ML property prediction | → `materials-stats` | → `materials-figures` |

## Databases and standards

Several materials databases are live APIs a workflow queries directly, not one-time-download
corpora — hence `materials-databases` and `materials-structure-analysis`'s Materials Project
reference being full skills, not appendices.

| Resource | Covered in |
|---|---|
| Materials Project | [materials-structure-analysis/references/materials-project-queries.md](../materials-structure-analysis/references/materials-project-queries.md) |
| AFLOW, OQMD, NOMAD, JARVIS, Matbench | [materials-databases/SKILL.md](../materials-databases/SKILL.md) |
| CIF, OPTIMADE | [materials-data-standards/SKILL.md](../materials-data-standards/SKILL.md) |

## Ownership notes (read before adding overlapping content)

- **`pymatgen` functionality is covered fully in `materials-structure-analysis`**, as original
  content — not a pointer to another repo. If you're extending structure/composition/symmetry/phase-
  diagram/electronic-structure-I/O coverage, it belongs there, not duplicated into
  `computational-materials` or `materials-databases`.
- **Weibull statistics for brittle-fracture strength data live in `mechanical-testing`**, not
  `materials-stats` — the ASTM conventions and specimen-population context are inseparable from that
  technique. `materials-stats` covers DOE, uncertainty propagation, and replicate-measurement
  statistics generally.
- **Bayesian optimization for *selecting the next experiment* lives in
  `high-throughput-autonomous-labs`**; general uncertainty quantification and DOE for a fixed
  experimental plan live in `materials-stats`.
- **DFT-computed phase stability (0K convex hull) lives in `materials-structure-analysis`; 
  temperature-dependent phase equilibria (CALPHAD) live in `phase-field-calphad`** — related but
  distinct questions, don't conflate them.
- **ML interatomic potentials (`computational-materials/references/ml-interatomic-potentials.md`,
  predicting energies/forces for simulation) and materials informatics ML (`materials-informatics-ml`,
  predicting a target property directly) are different uses of ML** — a new ML-for-materials skill
  should go in whichever matches its actual purpose, not be merged into the other by default.

## Known gaps

Not yet covered: biomaterials (materials/biology boundary — biocompatibility, scaffold
characterization; explicitly out of scope, same reasoning as excluding genomics from a neuroscience
skills repo), device fabrication/lithography process details (semiconductor-characterization covers
electrical measurement of fabricated devices, not the fabrication process itself), and additive
manufacturing process-parameter depth beyond what `synthesis-processing` sketches (a real candidate
for a dedicated skill if AM-specific depth is needed later).

## Adding a skill

See [CONTRIBUTING.md](../CONTRIBUTING.md) — placement (new technique family vs. new reference vs.
new cross-cutting skill) is the first decision to get right, before writing content.
