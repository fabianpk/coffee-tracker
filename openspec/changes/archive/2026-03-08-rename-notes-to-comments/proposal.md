## Why

The `notes` field on both `CoffeeBean` and `Tasting` is ambiguous — it's unclear whether it's for tasting notes or general comments. Renaming to `comments` clarifies the purpose: free-form prose commentary, distinct from structured `tasting_notes`. This rename is a prerequisite for the tasting-notes-search change which adds tag-based tasting notes filtering.

## What Changes

- **BREAKING**: Rename `notes` property to `comments` on `CoffeeBean` dataclass
- **BREAKING**: Rename `notes` property to `comments` on `Tasting` dataclass
- **BREAKING**: Rename `notes` column to `comments` in both `coffees` and `tastings` DB tables
- Update all API routes to use `comments` instead of `notes`
- Update frontend labels from "Your Notes" / "Notes" to "General Comments"
- Update placeholder text accordingly

## Capabilities

### New Capabilities

### Modified Capabilities
- `coffee-bean-model`: Rename `notes` → `comments` on CoffeeBean
- `tasting-model`: Rename `notes` → `comments` on Tasting
- `coffee-detail-edit`: Update label and field name in detail panel
- `tasting-ui`: Update label and field name in tasting modal and history

## Impact

- **`models.py`**: Rename property on both dataclasses
- **`app.py`**: Rename column in both CREATE TABLE statements, update save/update routes
- **`templates/index.html`**: Rename all `f-notes`, `d-notes`, `t-notes` references; update labels
- **Database**: Project is alpha — wipe DB (no migration needed)
