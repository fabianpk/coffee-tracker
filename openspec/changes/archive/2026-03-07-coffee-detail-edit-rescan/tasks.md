## 1. Backend Routes

- [x] 1.1 Add `GET /api/coffees/<id>` route returning a single entry as JSON (404 if not found)
- [x] 1.2 Add `PUT /api/coffees/<id>` route that updates all CoffeeBean fields and returns the updated entry

## 2. Detail Panel UI

- [x] 2.1 Add detail panel HTML structure (full-screen overlay with close button, all field inputs, Save button, and "Scan another side" button)
- [x] 2.2 Add detail panel CSS (overlay positioning, slide-in animation, matching dark theme)
- [x] 2.3 Add click handler on coffee list cards that opens the detail panel and populates all fields from the in-memory coffee object
- [x] 2.4 Implement close button logic: close immediately if no unsaved changes, otherwise prompt for confirmation
- [x] 2.5 Implement Save button: PUT to `/api/coffees/<id>`, close panel on success, refresh list

## 3. Rescan

- [x] 3.1 Add a hidden file input for the rescan camera trigger in the detail panel
- [x] 3.2 Wire "Scan another side" button to trigger the file input and POST selected image to `/api/scan`
- [x] 3.3 Implement merge logic: for each returned field, apply value to form only if the current field is empty
- [x] 3.4 Show loading state on the rescan button while scan is in progress; restore on completion
