## Context

The project has no README.md. CLAUDE.md serves as internal dev docs but is outdated after the coffee-bean-model change (missing `models.py`, new fields, migration logic). Both need to reflect the current state.

## Goals / Non-Goals

**Goals:**
- Create a README.md that serves as the public-facing project overview
- Update CLAUDE.md to accurately describe the current architecture including `models.py`

**Non-Goals:**
- API documentation or detailed field-level docs (the code and specs cover this)
- Contributing guide or license setup

## Decisions

### 1. README structure
Keep it simple: project description, prerequisites, setup, usage, and a brief architecture note. No badges, no screenshots — match the project's lightweight style.

### 2. CLAUDE.md scope of update
Only update sections that are factually wrong: add `models.py` to Architecture, mention `CoffeeBean` model, note migration behavior. Don't restructure or expand beyond what's needed.

## Risks / Trade-offs

- **[Docs drift]** README/CLAUDE.md can go stale again after future changes. → Accepted; keeping docs minimal reduces maintenance surface.
