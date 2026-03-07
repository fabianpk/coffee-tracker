## Why

Coffee entries in the list are currently read-only cards with no way to view full details or correct scan errors. Real coffee bags often require scanning multiple sides to capture all information, and Claude's vision extraction is imperfect — users need a way to review, fix, and supplement scanned data after saving.

## What Changes

- **Add a detail/edit view** for saved coffee entries: clicking a coffee card opens a full-screen panel showing all fields, editable in-place with a Save button.
- **Add a "Scan another side" button** in the detail view that triggers the camera and merges the new scan's non-null fields into the currently displayed entry, without overwriting fields that already have values (unless the user edits them manually).
- **Add `PUT /api/coffees/<id>` route** to support updating an existing entry.
- **Add `GET /api/coffees/<id>` route** to fetch a single entry by ID.

## Capabilities

### New Capabilities
- `coffee-detail-edit`: View and edit a saved coffee entry via a detail panel opened by clicking a list card.
- `coffee-rescan`: Scan an additional bag side from within the detail view to merge new extracted fields into the existing entry.

### Modified Capabilities
_(none — existing list and scan flows are unchanged)_

## Impact

- **`app.py`** — Two new routes: `GET /api/coffees/<id>` and `PUT /api/coffees/<id>`.
- **`models.py`** — No changes needed; `CoffeeBean` already covers all fields.
- **`templates/index.html`** — New detail panel UI, click handler on list cards, rescan button and merge logic.
