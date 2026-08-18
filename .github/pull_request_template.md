## What skill does this add/change?

<!-- Name, technique family or cross-cutting method, one-line summary -->

## Checklist

- [ ] `SKILL.md` frontmatter is complete (`name`, `description`, `license`, `metadata.modality`)
- [ ] `metadata.modality` matches the top-level folder it's in
- [ ] `SKILL.md` has `## Overview`, `## When to use this skill`, and `## Validation & Pitfalls`; if
      it has a `references/` folder, it has a routing table linking every reference
- [ ] Every `references/*.md` file has a `## Validation & Pitfalls` section
- [ ] Validation & Pitfalls cites a real standard/reference and lists concrete failure modes
- [ ] `python scan_skills.py` passes
- [ ] Added/updated the corresponding row(s) in `docs/skills.md`
- [ ] If this could plausibly overlap an existing cross-cutting skill (`materials-stats`,
      `materials-informatics-ml`, `materials-data-standards`, `materials-figures`), checked
      `docs/skills.md`'s ownership notes and linked instead of restating
