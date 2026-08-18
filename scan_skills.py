#!/usr/bin/env python3
"""Validate the modality-first skill tree: frontmatter schema, modality-folder
consistency, required sections, reference discoverability, and dead internal
links. Stdlib only — no dependencies to install.

Usage: python scan_skills.py
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent

NON_SKILL_DIRS = {".git", ".github", "docs"}

REQUIRED_FRONTMATTER = ["name", "description", "license", "metadata"]
REQUIRED_SKILL_SECTIONS = ["## Overview", "## When to use this skill"]
VALIDATION_SECTION_PREFIX = "## Validation & Pitfalls"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
LINK_RE = re.compile(r"\]\(([^)]+\.md[^)]*)\)")


def parse_frontmatter(text):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text
    raw, body = match.group(1), text[match.end():]

    data, metadata = {}, {}
    in_metadata = False
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("metadata:"):
            in_metadata = True
            continue
        if in_metadata and line.startswith("  "):
            key, _, val = line.strip().partition(":")
            metadata[key.strip()] = val.strip().strip('"')
            continue
        in_metadata = False
        key, _, val = line.partition(":")
        data[key.strip()] = val.strip()
    data["metadata"] = metadata
    return data, body


def has_section(body, prefix_or_exact, exact=False):
    for line in body.splitlines():
        if exact:
            if line.strip() == prefix_or_exact:
                return True
        elif line.strip().startswith(prefix_or_exact):
            return True
    return False


def validate_reference(ref_path, modality_dir):
    errors = []
    text = ref_path.read_text()
    if not text.lstrip().startswith("#"):
        errors.append(f"{ref_path}: doesn't start with a top-level '# ' title")
    if not has_section(text, VALIDATION_SECTION_PREFIX):
        errors.append(f"{ref_path}: missing a '{VALIDATION_SECTION_PREFIX}' section")
    for link in LINK_RE.findall(text):
        link_path = link.split("#")[0]
        if link_path.startswith("http"):
            continue
        target = (ref_path.parent / link_path).resolve()
        if not target.exists():
            errors.append(f"{ref_path}: broken link to '{link}'")
    return errors


def validate_skill(modality_dir):
    errors = []
    skill_md = modality_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{modality_dir}: missing SKILL.md"]

    frontmatter, body = parse_frontmatter(skill_md.read_text())
    if frontmatter is None:
        return [f"{skill_md}: missing or malformed frontmatter block"]

    for key in REQUIRED_FRONTMATTER:
        if not frontmatter.get(key):
            errors.append(f"{skill_md}: missing required frontmatter field '{key}'")

    if frontmatter.get("name") != modality_dir.name:
        errors.append(
            f"{skill_md}: frontmatter name '{frontmatter.get('name')}' != folder name '{modality_dir.name}'"
        )

    meta_modality = frontmatter.get("metadata", {}).get("modality")
    if meta_modality != modality_dir.name:
        errors.append(
            f"{skill_md}: metadata.modality '{meta_modality}' != folder name '{modality_dir.name}'"
        )

    for section in REQUIRED_SKILL_SECTIONS:
        if not has_section(body, section, exact=True):
            errors.append(f"{skill_md}: missing required section '{section}'")
    if not has_section(body, VALIDATION_SECTION_PREFIX):
        errors.append(f"{skill_md}: missing a '{VALIDATION_SECTION_PREFIX}' section")

    for link in LINK_RE.findall(body):
        link_path = link.split("#")[0]
        if link_path.startswith("http"):
            continue
        target = (modality_dir / link_path).resolve()
        if not target.exists():
            errors.append(f"{skill_md}: broken link to '{link}'")

    references_dir = modality_dir / "references"
    reference_files = sorted(references_dir.glob("*.md")) if references_dir.exists() else []
    for ref_path in reference_files:
        rel_link = f"references/{ref_path.name}"
        if rel_link not in body:
            errors.append(
                f"{skill_md}: {rel_link} exists but isn't linked from SKILL.md — "
                f"add it to the routing table so it's discoverable"
            )
        errors.extend(validate_reference(ref_path, modality_dir))

    return errors


def main():
    modality_dirs = sorted(
        p for p in REPO_ROOT.iterdir()
        if p.is_dir() and p.name not in NON_SKILL_DIRS and not p.name.startswith(".")
    )

    if not modality_dirs:
        print("No skill directories found.")
        return 0

    all_errors = []
    for modality_dir in modality_dirs:
        all_errors.extend(validate_skill(modality_dir))

    if all_errors:
        print(f"Validated {len(modality_dirs)} skill(s) — {len(all_errors)} problem(s):\n")
        for error in all_errors:
            print(f"  - {error}")
        return 1

    print(f"Validated {len(modality_dirs)} skill(s) — all passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
