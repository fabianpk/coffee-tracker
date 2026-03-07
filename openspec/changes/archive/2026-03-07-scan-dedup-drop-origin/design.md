## Context

The scan endpoint returns structured data from Claude vision. Currently the review form only offers "Save" and "Cancel". There's no check for existing coffees with the same identity. The `origin` field duplicates `country_grown` and creates confusion.

## Goals / Non-Goals

**Goals:**
- Detect duplicate coffees (same roaster+name) after a scan and present options
- Remove `origin` from the data model and prompt
- Fold `origin` semantics into `country_grown`

**Non-Goals:**
- Fuzzy/approximate duplicate matching (exact roaster+name match is sufficient)
- Migrating existing `origin` data into `country_grown` in the database
- Blocking saves — the user always has final say

## Decisions

### 1. Duplicate check happens client-side against cached coffee list

The frontend already fetches all coffees via `GET /api/coffees` (stored in `coffeeCache`). After a scan populates the review form, JS checks `coffeeCache` for a match on `roaster` + `name` (case-insensitive). No new API endpoint needed.

**Why not server-side**: The coffee list is already loaded. A client-side check is instant and avoids an extra round-trip. The list is small enough that this is reliable.

### 2. Duplicate UI: conditional buttons in the review form

When a duplicate is detected:
- Show an info banner: "A coffee with this name already exists"
- Replace the single "Save" button with two: **"Update Existing"** and **"Save as New"**
- "Update Existing" sends `PUT /api/coffees/<id>` to the matched coffee
- "Save as New" validates that either `roaster` or `name` has been changed from the matched coffee before allowing save (to prevent exact duplicates)

When no duplicate:
- Normal "Save" button (existing behaviour)

### 3. Drop `origin` by ignoring in `from_row()`, same as `brew_score`

The `origin` column stays in the SQLite schema (no destructive DDL). `CoffeeBean.from_row()` already filters to known fields, so removing `origin` from the dataclass is sufficient.

### 4. `from_scan()` maps `origin` to `country_grown` as fallback

If the Claude prompt somehow still returns `origin` (or old scan data is re-processed), `from_scan()` merges `origin` into `country_grown` when `country_grown` is empty. This is a one-way fallback.

### 5. Updated Claude prompt

Remove `"origin"` from the JSON template. Update `country_grown` instruction to: "country_grown is the country or region where the beans were grown; list all separated by commas if multiple (e.g. a blend)."

## Risks / Trade-offs

- **Existing `origin` data orphaned** — old entries with `origin` set will lose that display. Acceptable since `country_grown` usually had the same info. → No migration.
- **Case-insensitive match might miss edge cases** — e.g. trailing spaces. → `trim()` + `toLowerCase()` comparison is good enough.
