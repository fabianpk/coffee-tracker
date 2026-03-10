## Why

Tastings can only be deleted, not edited. If a user makes a mistake (wrong score, typo in notes, wrong brew type), they must delete and re-create the tasting, losing the original timestamp.

## What Changes

- Add `PUT /api/tastings/<id>` backend endpoint to update an existing tasting
- Add an "edit" button to each tasting entry in the tasting history
- Reuse the existing tasting modal for editing — pre-populate fields with existing values, switch button text to "Update Tasting"
- Track edit state so the save handler sends PUT (update) instead of POST (create)

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `tasting-api`: Adding PUT endpoint for updating a tasting
- `tasting-ui`: Adding edit button to tasting entries and edit mode for the tasting modal

## Impact

- **`app.py`**: New `PUT /api/tastings/<id>` route (~15 lines)
- **`templates/index.html`**: Edit button in tasting entry template, modal edit mode logic, pre-population of form fields
- No model, dependency, or schema changes needed
