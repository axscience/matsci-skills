---
name: materials-stats
description: Statistical methods shared across materials characterization and simulation — design of experiments (DOE), uncertainty quantification and propagation, and general statistical treatment of materials data. Cross-cutting by design; Weibull statistics for brittle-fracture data specifically live in mechanical-testing (where the domain context matters), and experiment-selection Bayesian optimization lives in high-throughput-autonomous-labs — this skill covers what's genuinely shared beyond those.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use scipy/statsmodels/pyDOE2.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: materials-stats
---

# Materials Statistics

## Overview

Three things come up across nearly every technique in this repo: designing an experimental campaign
efficiently (DOE), propagating measurement uncertainty through a derived quantity, and treating
replicate/repeated measurements correctly. This skill covers those. Weibull statistics for
brittle-fracture strength data live in `mechanical-testing` specifically because the domain context
(what counts as a valid specimen population, ASTM conventions) is inseparable from the technique
there; Bayesian-optimization-for-experiment-selection lives in `high-throughput-autonomous-labs`
since that's about choosing the next experiment, not analyzing completed ones.

## When to use this skill

Activate when the request involves:
- Design of experiments, DOE, factorial design, uncertainty quantification, error propagation,
  measurement uncertainty, replicate measurements
- Terms: full factorial, fractional factorial, Latin hypercube, propagation of error, confidence
  interval
- "Design an experiment to test multiple factors," "propagate uncertainty through this calculation,"
  "how many replicates do I need"

## Core usage

### Design of experiments — factorial design

```python
from pyDOE2 import fullfact, fracfact

full_design = fullfact([3, 3, 2])   # 3 levels x 3 levels x 2 levels — e.g. temperature x time x atmosphere
# Full factorial grows combinatorially — fractional factorial trades some
# interaction-effect resolution for far fewer runs, standard for screening
# many factors before a smaller focused full-factorial or response-surface study:
frac_design = fracfact("a b c abc")
```

### Uncertainty propagation (a general, technique-agnostic tool)

```python
import numpy as np

def propagate_uncertainty(func, values, uncertainties, n_samples=100000, seed=42):
    """Monte Carlo error propagation — more robust than analytical propagation
    formulas for nonlinear functions or correlated/non-Gaussian inputs, at the
    cost of being approximate/sampling-based rather than exact."""
    rng = np.random.default_rng(seed)
    sampled_inputs = [rng.normal(v, u, n_samples) for v, u in zip(values, uncertainties)]
    sampled_outputs = func(*sampled_inputs)
    return {"mean": sampled_outputs.mean(), "std": sampled_outputs.std()}

# Example: propagating uncertainty in density = mass / volume
density_result = propagate_uncertainty(
    lambda m, v: m / v, values=[10.5, 2.1], uncertainties=[0.02, 0.01]
)
```

### Replicate measurement treatment

```python
from scipy import stats

def replicate_summary(measurements, confidence=0.95):
    """Standard error and confidence interval from replicate measurements —
    required whenever reporting a mean value from more than one measurement,
    across any technique in this repo."""
    n = len(measurements)
    mean = np.mean(measurements)
    sem = stats.sem(measurements)
    ci = stats.t.interval(confidence, n - 1, loc=mean, scale=sem)
    return {"mean": mean, "sem": sem, f"{int(confidence*100)}%_CI": ci, "n": n}
```

## Validation & Pitfalls

Canonical references: Montgomery, *Design and Analysis of Experiments* (10th ed., 2019), for DOE;
Taylor, *An Introduction to Error Analysis* (2nd ed., 1997), for uncertainty propagation.

- **Fractional factorial designs sacrifice the ability to resolve certain interaction effects — check
  the design's resolution (which interactions are confounded with which) before choosing one, not
  just the run-count savings.** A resolution III design confounds main effects with two-factor
  interactions, which can be seriously misleading if those interactions are actually important for
  the system being studied.
- **Monte Carlo uncertainty propagation assumes the input uncertainty distributions (often assumed
  Gaussian, as in the code above) are actually representative** — a systematic (not random) error
  source, or a genuinely non-Gaussian measurement error distribution, isn't captured correctly by a
  naive Gaussian Monte Carlo approach; identify systematic error sources separately rather than
  folding them into a random-uncertainty propagation.
- **A single measurement has no meaningful "uncertainty" without either an instrument-specified
  precision or actual replicate measurements — don't report a confidence interval computed from a
  single data point treated as if it were a distribution.** Replicate measurements (not just repeated
  reads of the same acquisition) are needed to capture real measurement-to-measurement variability.
- **Reporting "n" (number of replicates/samples) is not optional** — a mean value without a stated
  sample size and uncertainty is incomplete for any quantitative materials claim, matching the
  broader principle (shared with this repo's sibling neuroscience skills project) that no reported
  number should stand without its uncertainty.
- **DOE assumes factors are actually independently controllable at the specified levels** — in
  practice, some factor combinations may be physically unachievable or produce a different regime
  entirely (e.g. a temperature/atmosphere combination that changes reaction mechanism) — check that
  the full designed factor space is physically sensible before running it, not just statistically
  efficient.
