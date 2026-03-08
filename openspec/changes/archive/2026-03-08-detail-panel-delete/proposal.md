## Why

When a user taps a coffee entry to open the detail panel, there is no way to delete it from there. The only delete button is on the list card itself, which is easy to miss. Users expect to be able to delete from the detail view they're already looking at.

## What Changes

- Add a "Delete" button to the detail/edit panel in the frontend
- Confirmation dialog before deletion (reuses existing pattern)
- On successful deletion, close the detail panel and refresh the coffee list

## Capabilities

### New Capabilities

### Modified Capabilities
- `coffee-detail-edit`: Add a delete action to the detail panel

## Impact

- **`templates/index.html`** — New delete button in the detail panel HTML and corresponding JavaScript handler
