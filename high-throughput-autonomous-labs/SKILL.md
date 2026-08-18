---
name: high-throughput-autonomous-labs
description: Combinatorial synthesis, robotic experimentation, and closed-loop active-learning materials discovery. A smaller, less standardized community than the rest of this repo's skills — real and growing (self-driving labs, Bayesian-optimization-guided synthesis campaigns), but with less mature tooling conventions.
license: MIT
allowed-tools: Read Write Edit Bash
compatibility: Examples use scikit-optimize/botorch-style Bayesian optimization conventions; lab-automation hardware/software integration is highly setup-specific and not covered in depth here.
metadata:
  version: "1.0"
  skill-author: matsci-skills contributors
  modality: high-throughput-autonomous-labs
---

# High-Throughput and Autonomous Materials Discovery

## Overview

Autonomous/self-driving labs close the loop between synthesis, characterization, and decision-making
— an algorithm (typically Bayesian optimization or a related active-learning method) selects the next
experiment based on prior results, without waiting for a human to manually plan each iteration. This
is a genuinely different workflow from every other skill in this repo, which assume a human plans
each characterization/synthesis step; it's included because it's real and growing, but the tooling
here is less standardized than characterization or DFT conventions.

## When to use this skill

Activate when the request involves:
- High-throughput synthesis, combinatorial screening, autonomous lab, self-driving lab, active
  learning for materials discovery, Bayesian optimization (applied to synthesis/experiments)
- Terms: acquisition function, exploration-exploitation, closed-loop experimentation, design of
  experiments for screening
- "Plan a high-throughput screening campaign," "set up Bayesian optimization for synthesis parameters"

## Core usage

### Bayesian optimization for synthesis parameter selection

```python
from skopt import gp_minimize
from skopt.space import Real

def objective(params):
    """Wraps the actual synthesis + characterization pipeline — in a real
    autonomous lab, this triggers hardware and waits for a measured result;
    here it's the interface point where this skill hands off to
    synthesis-processing and the relevant characterization skill."""
    temperature, precursor_ratio = params
    measured_property = run_synthesis_and_characterize(temperature, precursor_ratio)  # placeholder for the real pipeline
    return -measured_property  # gp_minimize minimizes; negate if maximizing the target property

search_space = [Real(400, 800, name="temperature_C"), Real(0.5, 2.0, name="precursor_ratio")]
result = gp_minimize(objective, search_space, n_calls=30, random_state=42)
best_params = result.x
```

### Design-of-experiments screening (before optimization — establishing the response surface)

```python
from scipy.stats import qmc

def latin_hypercube_screening_design(n_samples, parameter_bounds):
    """Space-filling design for initial screening — better coverage of the
    parameter space than a naive grid for a given experiment budget, standard
    practice before committing to a more targeted optimization campaign."""
    sampler = qmc.LatinHypercube(d=len(parameter_bounds))
    unit_samples = sampler.random(n=n_samples)
    lower_bounds, upper_bounds = zip(*parameter_bounds)
    return qmc.scale(unit_samples, lower_bounds, upper_bounds)
```

## Validation & Pitfalls

Canonical references: Shahriari et al. (2016), "Taking the human out of the loop: A review of
Bayesian optimization," *Proceedings of the IEEE*, for the general methodology; MacLeod et al. (2020),
"Self-driving laboratory for accelerated discovery of thin-film materials," *Science Advances*, for a
representative autonomous-lab implementation.

- **Bayesian optimization's efficiency gains depend on the underlying response surface being
  reasonably smooth/well-behaved — a genuinely discontinuous or highly multimodal property landscape
  can mislead the surrogate model** and the optimizer toward a local rather than global optimum.
  Don't assume convergence to a good result without checking whether the explored space and found
  optimum make physical sense.
- **The measurement/characterization step feeding the optimization loop has its own noise and
  systematic error (see the relevant characterization skill's Validation & Pitfalls) — an
  optimization loop built on noisy or biased measurements can converge confidently to a wrong
  answer.** The optimization algorithm doesn't know the measurement is unreliable; validate
  measurement quality independently, not just optimization convergence behavior.
- **This field's tooling and conventions are less standardized than the rest of materials
  characterization — a workflow that works well for one lab's specific hardware/software stack often
  doesn't transfer directly to another's.** Treat the code here as illustrating the underlying
  optimization concepts, not a drop-in pipeline; real autonomous-lab integration requires
  hardware/software-specific engineering this skill doesn't cover.
- **A successful autonomous campaign optimizes the specific objective function defined — a poorly
  chosen objective (e.g. optimizing one property while ignoring a constraint like stability or cost)
  can produce a "successful" result that's practically useless.** Define the objective function
  (including any constraints, as penalty terms or explicit constraint handling) carefully before
  running a campaign, not after seeing where it converges.
- **Batch/parallel experimentation (common in robotic labs, running many experiments simultaneously
  rather than one at a time) requires optimization strategies designed for batch acquisition** — a
  purely sequential Bayesian optimization strategy applied naively to batch selection can pick
  redundant (too-similar) experiments within a batch; use a batch-aware acquisition strategy when the
  lab setup actually runs experiments in parallel.
