# Machine-Learned Interatomic Potentials

Modality-specific detail for [../SKILL.md](../SKILL.md). MLIPs (MACE, NequIP, CHGNet, M3GNet, and
similar equivariant graph-neural-network models) approximate DFT-quality potential energy surfaces
at a fraction of the computational cost, enabling MD-scale simulations (thousands of atoms,
nanoseconds) with near-DFT accuracy — the fastest-growing area in this skill's scope.

## Using a pretrained foundation model (e.g. MACE-MP-0, trained broadly on Materials Project data)

```python
from mace.calculators import mace_mp
from ase.io import read
from ase.optimize import BFGS

calculator = mace_mp(model="medium", device="cuda")   # or "cpu"

atoms = read("structure.cif")
atoms.calc = calculator

optimizer = BFGS(atoms)
optimizer.run(fmax=0.01)   # relax to a force convergence threshold, ASE-style

energy = atoms.get_potential_energy()
forces = atoms.get_forces()
```

## Running MD with an MLIP calculator (ASE-based, bridges to LAMMPS-scale questions with DFT-level accuracy)

```python
from ase.md.npt import NPT
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
import ase.units as units

MaxwellBoltzmannDistribution(atoms, temperature_K=300)
dyn = NPT(atoms, timestep=1 * units.fs, temperature_K=300, externalstress=0, ttime=25 * units.fs, pfactor=None)
dyn.run(10000)
```

## Fine-tuning a foundation model on system-specific DFT data

```python
# Foundation models (broad training data) often benefit from fine-tuning on a
# smaller set of DFT calculations specific to the system of interest, when high
# accuracy for that specific chemistry/configuration space is needed —
# conceptually: collect a training set spanning the relevant configuration space
# (e.g. from short DFT-driven MD trajectories or structure perturbations), then
# fine-tune following the specific MLIP package's training workflow (mace_run_train
# for MACE, nequip-train for NequIP).
```

## Validation & Pitfalls

Canonical references: Batatia et al. (2022), "MACE: Higher order equivariant message passing neural
networks for fast and accurate force fields," *NeurIPS*; Batzner et al. (2022), "E(3)-equivariant
graph neural networks for data-efficient and accurate interatomic potentials," *Nature
Communications* (NequIP).

- **A foundation model's accuracy is not uniform across chemical space — it reflects its training
  data's coverage, and performs worse (sometimes badly) on chemistry underrepresented in training**
  (unusual oxidation states, exotic bonding, elements/combinations rare in the training set). Check
  whether the specific system of interest is well-represented in the model's training domain before
  trusting predictions, especially for out-of-distribution chemistry.
- **MLIP energies/forces should be spot-checked against DFT on a subset of configurations before
  trusting a large-scale simulation built on them** — an MLIP can be systematically biased (e.g.
  slightly wrong equilibrium volume or elastic constants) in ways that compound over a long MD
  trajectory even if per-configuration errors look individually small.
- **Uncertainty quantification is available for some MLIP frameworks (ensemble methods, some
  architectures' native uncertainty estimates) and should be used when extrapolating beyond validated
  configurations** — running an MLIP on configurations far from anything in training or validation
  data without any uncertainty check is a common way to get a confident, wrong answer that looks like
  a normal simulation output.
- **Fine-tuning on a small, poorly-sampled dataset can degrade a foundation model's broader
  reliability (catastrophic forgetting) while only marginally improving accuracy on the target
  system** — validate a fine-tuned model against both the target system's DFT data and a broader
  sanity-check set (e.g. known elastic constants, phonon stability) rather than only the fine-tuning
  metric.
- **This is a fast-moving area — model architectures, foundation-model training sets, and even which
  package is "the" standard choice change on a timescale of months, not years.** Check current
  documentation/benchmarks for the specific package version in use rather than assuming older
  guidance (including this reference, over time) still reflects best practice.
