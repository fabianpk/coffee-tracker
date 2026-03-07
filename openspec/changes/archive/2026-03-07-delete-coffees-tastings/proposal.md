## Why

Deleting a coffee does not remove its associated tastings (orphaned rows). There is no way to delete individual tastings at all. Both are needed for basic data hygiene.

## What Changes

- `DELETE /api/coffees/<id>` now cascade-deletes all associated tastings before removing the coffee
- New `DELETE /api/tastings/<id>` route to delete a single tasting
- Frontend: tasting history entries gain a delete button
- Frontend: deleting a coffee warns that its tastings will also be removed

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `tasting-api`: Add `DELETE /api/tastings/<id>` route; update cascade behaviour on coffee deletion
- `tasting-ui`: Add delete button per tasting entry in the history section

## Impact

- `app.py`: update `delete_coffee()`, add `delete_tasting()` route
- `templates/index.html`: delete button in tasting entries, updated confirm message on coffee delete
