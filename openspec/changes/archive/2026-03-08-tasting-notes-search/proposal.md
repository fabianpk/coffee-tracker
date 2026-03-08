## Why

Tasting notes are currently stored as a single free-text string, making it impossible to search for coffees by individual tasting note. Users want to find all coffees with e.g. "Chocolate" as a tasting note, even when it appears alongside other notes like "Chocolate, Strawberry, Peach". Additionally, the Tasting model has no `tasting_notes` field, so individual brew tastings can't record what flavors were detected.

**Prerequisite**: This change assumes `rename-notes-to-comments` has been applied.

## What Changes

- Update the Claude scan prompt to return tasting notes as a clean comma-separated list
- Add `tasting_notes` field to the `Tasting` model and DB table
- Add a search/filter API endpoint that can find coffees matching a specific tasting note
- Add frontend search UI to filter the coffee list by tasting note
- Display tasting notes as individual tags/chips in the UI for clarity
- Add tasting notes input to the Conduct Tasting modal

## Capabilities

### New Capabilities
- `tasting-notes-filter`: Search/filter coffees by individual tasting note, display notes as tags

### Modified Capabilities
- `coffee-bean-model`: Scan prompt updated to produce clean comma-separated tasting notes
- `scan-field-hints`: Scan prompt updated to produce clean comma-separated tasting notes
- `tasting-model`: Add `tasting_notes` field to Tasting dataclass and DB table
- `tasting-ui`: Add tasting notes input to Conduct Tasting modal and tasting history display

## Impact

- **`app.py`**: Update scan prompts; add search/filter endpoint; add `tasting_notes` column to tastings table; update tasting save route
- **`templates/index.html`**: Add tasting notes input to tasting modal; render notes as tags; add filter UI
- **`models.py`**: Add `tasting_notes` to `Tasting` dataclass
- **Database**: Add `tasting_notes` column to `tastings` table; existing coffee tasting_notes data may have inconsistent separators
