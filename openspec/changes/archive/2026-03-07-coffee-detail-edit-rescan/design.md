## Context

The current frontend is a single-page app with a flat coffee list. Each card shows a summary (roaster, name, origin, tasting notes, rating) but there is no way to open a full view or edit saved entries. The scan flow only runs before saving — once saved, data is permanent. Users on mobile can photograph one side of a bag at a time, so multi-side scanning needs to be seamless within the editing flow.

## Goals / Non-Goals

**Goals:**
- Detail panel showing all CoffeeBean fields for a saved entry, opened by tapping/clicking a card
- All fields editable inline; changes saved via `PUT /api/coffees/<id>`
- "Scan another side" button in the detail panel that runs the existing vision extraction and merges results into the open form
- New backend routes: `GET /api/coffees/<id>` and `PUT /api/coffees/<id>`

**Non-Goals:**
- Version history or undo for edits
- Conflict resolution if two scans return contradictory values — user resolves manually in the form
- Image storage / displaying the original bag photo

## Decisions

### 1. Detail panel as a full-page overlay, not a separate route
**Choice:** Slide-up overlay panel (like a bottom sheet) rendered over the list, no URL routing.
**Rationale:** The app has no router and no build step. Adding hash-based routing or a full router library would be over-engineering for a single-page personal app. An overlay matches the mobile-first UX already established.

### 2. Merge strategy: new scan fills only null/empty fields, never overwrites
**Choice:** When a rescan completes, iterate the returned fields and only apply values where the current form field is empty.
**Rationale:** The user already reviewed and possibly corrected fields from the first scan. Overwriting would undo their work. They can manually edit any field they want to update.

### 3. `PUT /api/coffees/<id>` replaces the full entry
**Choice:** Accept all CoffeeBean fields in the request body and do a full-row update (not a PATCH).
**Rationale:** The detail form always shows all fields; sending the full form state on save is simpler than tracking which fields changed. Data volume is tiny.

### 4. `GET /api/coffees/<id>` for fetching a single entry
**Choice:** Add a dedicated single-item route rather than filtering the list response client-side.
**Rationale:** The list is already loaded when a card is clicked, so we can open the detail panel directly from the in-memory list data — no extra fetch needed on click. The `GET` route is still useful for direct linking or future use.

### 5. Rescan reuses the existing `/api/scan` endpoint
**Choice:** The "Scan another side" button POSTs to the same `/api/scan` as the initial scan.
**Rationale:** No changes to the scan pipeline needed. The merge logic lives entirely in the frontend.

## Risks / Trade-offs

- **[Overlay on small screens]** A full-height overlay may feel heavy on very small phones. → The existing card-based UI is already mobile-first; the overlay will use the same max-width container.
- **[Lost edits on accidental close]** Tapping outside or pressing back could lose unsaved edits. → Add a "close" button only (no tap-outside-to-close); warn the user if they attempt to close with unsaved changes.
