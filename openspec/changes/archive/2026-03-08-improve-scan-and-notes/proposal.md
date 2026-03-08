## Why

The scan review form has confusing note fields: "Your Notes" with "How was it?" placeholder conflates personal tasting impressions with general notes, and the "Other (Markdown)" field from scanning gets saved to the database even though it's only useful as reference during review. Additionally, the current Claude Haiku 4.5 model used for image scanning produces poor text recognition results from coffee bag photos.

## What Changes

- Rename "Your Notes" placeholder from "How was it?" to "Other notes" across the review form and detail/edit panel
- Make the "Other (from scan)" / "Other (markdown)" field read-only reference that is NOT saved to the database — it's shown during scan review but excluded from the save payload
- Switch the vision model from `claude-haiku-4-5-20251001` to a more capable model (e.g. `claude-sonnet-4-6`) for better text recognition in `extract_coffee_details()` and `extract_coffee_from_text()`

## Capabilities

### New Capabilities

### Modified Capabilities
- `coffee-detail-edit`: Remove "other" field from being editable/saved; rename "Your Notes" placeholder
- `scan-field-hints`: "Other" becomes display-only during scan review, not persisted

## Impact

- **`templates/index.html`**: Update placeholder text, remove `other` from save payloads, make "Other" field display-only in review form
- **`app.py`**: Change model in `extract_coffee_details()` and `extract_coffee_from_text()` from Haiku to a more capable model; optionally stop saving `other` field in `save_coffee()` / `update_coffee()`
- **`models.py`**: Remove `other` from `CoffeeBean`
- **Database**: Existing `other` column data is deleted and new entries won't populate it
