# Architecture decision records

This directory is empty as of this writing — no decisions have been
recorded in ADR format yet. The project's real decision history so far
lives in prose form in `docs/build-plan.md` (initial stack choice, content
model, phased roadmap) and `docs/graph-3d-plan.md` (3D graph view: library
choice, layout algorithm, deviations from the original reference spec).
Those aren't going to be retroactively split into individual ADRs.

Use this directory going forward for new architecture-level decisions —
one file per decision, numbered sequentially.

## Format

`NNNN-short-title.md`, e.g. `0001-use-content-collections-not-flat-frontmatter-parsing.md`.

```markdown
# NNNN. Title

Date: YYYY-MM-DD
Status: proposed | accepted | superseded by NNNN

## Context

What problem or question forced this decision. Constraints that mattered.

## Decision

What was actually decided.

## Consequences

What this makes easier, what it makes harder, what it forecloses.
```

Keep them short. An ADR records *that* a decision was made and *why*, not
a design spec — implementation detail belongs in code comments or a
regular doc, not here.
