# Symmetry Analysis and Structure Transformations

Deeper detail for [../SKILL.md](../SKILL.md). Covers space group determination, symmetry-equivalent
sites, and common structure transformations (supercells, substitutions, strain).

## Space group and symmetry analysis

```python
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

sga = SpacegroupAnalyzer(structure, symprec=0.01)   # symprec: tolerance for symmetry detection — see pitfalls
print(sga.get_space_group_symbol(), sga.get_space_group_number())

symmetrized_structure = sga.get_symmetrized_structure()
equivalent_sites = symmetrized_structure.equivalent_sites   # groups of symmetry-related atoms

primitive = sga.get_primitive_standard_structure()
conventional = sga.get_conventional_standard_structure()
```

## Supercells and substitutions

```python
supercell = structure.copy()
supercell.make_supercell([2, 2, 2])   # 2x2x2 expansion

doped = structure.copy()
doped.replace(0, "Mn")   # substitute the atom at site index 0

from pymatgen.transformations.standard_transformations import SubstitutionTransformation
transform = SubstitutionTransformation({"Fe": "Mn"})   # replace all Fe with Mn
doped_structure = transform.apply_transformation(structure)
```

## Applying strain

```python
strained = structure.copy()
strained.apply_strain(0.02)   # 2% isotropic strain — for anisotropic strain, pass a 3-component array
```

## Validation & Pitfalls

Canonical reference: Hahn (ed.), *International Tables for Crystallography, Volume A* (space group
conventions); Ong et al. (2013) for pymatgen's symmetry implementation (built on spglib).

- **`symprec` (symmetry-detection tolerance) directly determines what space group is found, and the
  default isn't universally appropriate** — a structure with small numerical noise (e.g. from a DFT
  relaxation that didn't fully converge to high symmetry) can be assigned a lower symmetry than
  intended with a tight `symprec`, or a spuriously higher symmetry with a loose one. Check sensitivity
  to `symprec` when the symmetry assignment itself is part of a claim, not just downstream analysis.
- **Primitive vs. conventional cell choice affects atom count and is a common source of confusion
  when comparing structures or supercell sizes across sources** — always confirm which cell
  convention a structure (yours or a downloaded one) uses before comparing atom counts or building
  supercells for consistency with another dataset.
- **Substitution transformations don't check chemical plausibility** — `SubstitutionTransformation`
  will happily substitute an element into a site regardless of whether the resulting structure is
  physically reasonable (charge balance, ionic radius compatibility); a substituted structure needs
  independent validation (e.g. via `computational-materials` relaxation, or bond-valence-sum checks)
  before treating it as a real candidate material.
- **Applying strain to a structure changes its energy/stability, which is not automatically
  recomputed** — a strained structure object is just geometrically modified; any energetic claim about
  the strained structure requires re-running the relevant calculation, not assuming the original
  structure's computed properties still apply.
