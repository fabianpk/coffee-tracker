## Context

Both `CoffeeBean` and `Tasting` have a `notes` field used for free-form text. With the upcoming tasting-notes-search change adding structured comma-separated `tasting_notes` to the Tasting model, having both `notes` and `tasting_notes` would be confusing. Renaming `notes` → `comments` makes the distinction clear.

## Goals / Non-Goals

**Goals:**
- Rename `notes` → `comments` across both models, DB, API, and frontend
- Update all UI labels to "General Comments"

**Non-Goals:**
- Changing behavior — this is a pure rename
- DB migration — alpha project, wipe the DB

## Decisions

### 1. Column and property name: `comments`

**Choice**: Rename to `comments` (not `general_comments` or `comment`).

**Rationale**: Short, clear, distinct from `tasting_notes`. Plural matches the convention of the other fields.

### 2. No DB migration

**Choice**: Wipe the database rather than migrating. Project is alpha.

**Rationale**: Adding ALTER TABLE RENAME COLUMN for two tables is unnecessary churn when the DB can simply be recreated.

## Risks / Trade-offs

- **[Breaking change]** All existing data in `notes` columns is lost → Acceptable in alpha
