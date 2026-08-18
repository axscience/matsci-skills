---
name: materials-informatics-ml
description: Machine learning for materials property prediction and generative design — descriptor-based models, graph neural networks for crystal structures (CGCNN/MEGNet-class), and generative models for candidate material discovery. Distinct from ml-interatomic-potentials (which predicts energies/forces for simulation) — this is property/structure prediction as an end goal, not a simulation surrogate.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use scikit-learn for descriptor-based models, matminer for featurization, and PyTorch/PyG-style conventions for GNN-based models.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: materials-informatics-ml
---

# Materials Informatics and ML

## Overview

Materials informatics applies machine learning to predict material properties from composition/
structure (screening candidates faster than DFT or experiment) or to generate novel candidate
structures. This is distinct from `computational-materials/references/ml-interatomic-potentials.md`,
which uses ML to approximate a potential energy surface for simulation — here, ML predicts a target
property (band gap, formation energy, hardness) directly, or generates new structures, as an end
goal in itself.

## When to use this skill

Activate when the request involves:
- Materials property prediction, ML for materials, CGCNN, MEGNet, graph neural network for crystals,
  generative model for materials, materials descriptors/featurization
- Terms: matminer, crystal graph, composition-based feature vector, train/test split for materials data
- "Predict this property from composition/structure," "featurize these materials for ML," "generate
  candidate structures with property X"

## Core usage

### Descriptor-based property prediction (matminer featurization + scikit-learn)

```python
from matminer.featurizers.composition import ElementProperty
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd

featurizer = ElementProperty.from_preset("magpie")
df = featurizer.featurize_dataframe(df, col_id="composition")   # df has a pymatgen Composition column

feature_cols = [c for c in df.columns if c.startswith("MagpieData")]
X_train, X_test, y_train, y_test = train_test_split(df[feature_cols], df["target_property"], test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
```

### Graph neural network property prediction (conceptual — CGCNN-class model)

```python
# Crystal graph convolutional networks represent a structure as a graph (atoms
# as nodes, bonds/neighbors as edges) and learn representations directly from
# structure rather than hand-engineered descriptors — typically outperforming
# descriptor-based models when enough training structures are available.
# Training requires a graph-construction step (e.g. via pymatgen's structure
# graph tools) feeding into a PyTorch Geometric-style GNN — see the specific
# package (CGCNN, MEGNet, ALIGNN) for its current data-pipeline conventions,
# which differ meaningfully between packages.
```

### Model evaluation with materials-appropriate cross-validation

```python
from sklearn.model_selection import GroupKFold

def composition_aware_cv(X, y, chemical_system_groups, n_splits=5):
    """Random K-fold on materials data can leak information when chemically
    similar/related compounds end up split across train and test — grouping by
    chemical system (or another structural-similarity grouping) gives a more
    honest estimate of generalization to genuinely new chemistry."""
    cv = GroupKFold(n_splits=n_splits)
    return list(cv.split(X, y, groups=chemical_system_groups))
```

## Validation & Pitfalls

Canonical references: Ward et al. (2016), "A general-purpose machine learning framework for
predicting properties of inorganic materials," *npj Computational Materials* (the Magpie featurization
approach); Xie & Grossman (2018), "Crystal graph convolutional neural networks for an accurate and
interpretable prediction of material properties," *Physical Review Letters* (CGCNN).

- **Random train/test splitting on materials data typically overstates real-world generalization,
  the same core problem as in other domains' ML but with a materials-specific cause: many datasets
  contain multiple compositions/structures from the same chemical system or even the same base
  structure with minor substitutions.** A model can "predict" a held-out entry partly by having seen
  a near-identical relative in training. Use grouped/chemical-system-aware splitting (as above) for
  an honest generalization estimate, especially when the claim is about predicting genuinely novel
  chemistry.
- **A model trained on DFT-computed labels inherits DFT's own systematic errors (e.g. underestimated
  band gaps for GGA-trained models) — it will confidently reproduce those errors, not correct them.**
  State what labels a model was trained on, and don't present ML-predicted properties as more
  accurate than the ground truth they were trained against.
- **Descriptor-based models are only as good as the descriptors' ability to capture what determines
  the target property** — a composition-only descriptor (like the Magpie example above) cannot
  distinguish between polymorphs with identical composition but different structure/properties; use
  structure-aware descriptors or graph-based models when polymorph-level distinction matters for the
  question.
- **Extrapolation outside a model's training distribution (new element combinations, property ranges
  far from training data) is unreliable and often silent** — a model doesn't know it's extrapolating
  unless specifically designed to flag it (e.g. via an ensemble-based uncertainty estimate or a
  distance-to-training-data metric); check whether a candidate material is actually within the
  training distribution before trusting a screening prediction for it.
- **Generative models can produce chemically implausible or synthetically inaccessible structures**
  — a generated candidate passing a property-prediction filter still needs independent validation
  (stability via `materials-structure-analysis`'s phase-diagram tools, and realistic synthesizability
  assessment) before being treated as a real candidate, not just a model output that looks reasonable.
