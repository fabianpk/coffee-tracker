## 1. Backend

- [x] 1.1 Add `PUT /api/tastings/<int:tasting_id>` endpoint in `app.py` — validate tasting exists, update all fields, preserve `created_at`, return updated tasting

## 2. Frontend: Edit button

- [x] 2.1 Add "edit" button next to "delete" in tasting entry template (in `toggleTastingHistory`), wired to `editTasting(tastingId, coffeeId)`

## 3. Frontend: Modal edit mode

- [x] 3.1 Add `editingTastingId` and `editingCoffeeId` state variables, add `openTastingModal(tasting, coffeeId)` function that pre-populates all fields (brew type, dosage, score, tasting notes, comments), disables coffee selector, sets title to "Edit Tasting" and button to "Update Tasting"
- [x] 3.2 Update existing "Conduct Tasting" button handler to reset `editingTastingId = null` and ensure title/button text are in create mode
- [x] 3.3 Update save handler to PUT `/api/tastings/<id>` when `editingTastingId` is set, then refresh tasting history for the specific coffee and reload coffees

## 4. Verification

- [x] 4.1 Restart service and verify editing a tasting works end-to-end (edit button → modal → update → refreshed history)
