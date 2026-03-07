## Context

`CoffeeBean` currently stores `brew_score` and `espresso_score` as flat columns. This ties identity (what coffee this is, where it's from) to tasting results, making it impossible to record multiple evaluations of the same bag at different doses or brew methods. The app is single-user, SQLite-backed, with all logic in `app.py` and `models.py`.

## Goals / Non-Goals

**Goals:**
- Introduce a `Tasting` model that belongs to a `CoffeeBean` (many-to-one)
- Support `brew_type` (espresso, brew, etc.) and `dosage` (drop-down list, from 10.0gr to 20.0gr, increments of 0.1gr) per tasting
- Compute per-coffee average score dynamically from all its tastings
- Add a "Conduct Tasting" UI flow separate from the scan flow
- Migrate the database without losing existing data

**Non-Goals:**
- Changing the scan/vision prompt or extraction logic
- Dropping existing `brew_score`/`espresso_score` columns (left unused to avoid risky DDL)
- Multi-user or auth changes
- Tasting statistics beyond a simple average

## Decisions

### 1. Normalized `tastings` table (not embedded JSON in `coffees`)
Separate table with `coffee_id` FK. Enables clean SQL aggregation and future filtering by brew type. Embedding as JSON would make querying and averaging awkward.

### 2. `brew_type` as free-text string, not an enum/FK
Avoids a migration each time a new method is added. The UI can offer preset options (espresso, brew) with a free-text fallback. Validated loosely — any non-empty string is accepted.

### 3. Average score computed in Python at fetch time, not stored
Matches the existing pattern (no ORM, plain `sqlite3`). A single `SELECT AVG(score) FROM tastings WHERE coffee_id=?` per coffee on `GET /api/coffees` is cheap at this scale. No materialized view needed.

### 4. Old `brew_score`/`espresso_score` columns left in place
SQLite 3.35+ supports `DROP COLUMN`, but migrating a production SQLite file destructively is risky with no test suite. The columns are simply ignored going forward. `init_db()` adds the `tastings` table if absent; no further schema changes to `coffees`.

### 5. "Conduct Tasting" as a modal, not a separate page
The existing UI is a single-page app with inline JS/CSS. A modal keeps the pattern consistent and avoids routing complexity.

## Risks / Trade-offs

- **Old score data is orphaned** — existing `brew_score`/`espresso_score` values in the DB will not be migrated to `Tasting` rows, since there's no timestamp or brew-type metadata to attach. Acceptable: these are early test entries. → No mitigation needed; document as known loss.
- **Average score absent when no tastings exist** — `average_score` will be `null` in the API. Frontend must handle gracefully. → Show "–" or empty instead of 0.

## Migration Plan

1. `init_db()` gains a `CREATE TABLE IF NOT EXISTS tastings (...)` block — safe to run repeatedly.
2. No destructive changes to `coffees` table.
3. Deploy by restarting the systemd service (`sudo systemctl restart coffee-tracker`).
4. Rollback: revert code, restart — old `coffees` columns are untouched.
