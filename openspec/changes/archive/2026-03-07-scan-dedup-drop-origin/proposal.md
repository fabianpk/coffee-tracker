## Why

Users sometimes forget they already scanned a coffee and scan it again, creating duplicates. The app should detect this and let the user choose to update the existing entry or save as a new (unique) coffee. Separately, the model has both `origin` and `country_grown` which overlap — `origin` should be removed and its meaning folded into `country_grown`.

## What Changes

- **Duplicate detection**: After a scan, the system checks if a coffee with the same roaster+name already exists. If a match is found, the review form offers two options:
  - **Update existing** — merges the new scan data into the existing coffee entry
  - **Save as new** — requires changing the name or roaster to differentiate before saving
- **Drop `origin` field**: Remove `origin` from the `CoffeeBean` dataclass, database schema (leave column, ignore it), Claude vision prompt, and all UI forms. The prompt instruction for `origin` ("list all countries/regions") moves to `country_grown`.
- **Updated Claude prompt**: No longer asks for `origin`; `country_grown` description updated to include regions/countries of origin

## Capabilities

### New Capabilities

- `scan-dedup`: Post-scan duplicate detection by roaster+name match, with update-existing and save-as-new UI flows

### Modified Capabilities

- `coffee-bean-model`: Remove `origin` field from dataclass; update `from_row()` to ignore it in old rows; update `from_scan()` to map old `origin` to `country_grown` if present; update Claude vision prompt to drop `origin` and expand `country_grown`

## Impact

- `models.py`: remove `origin` field, update `from_scan()`
- `app.py`: update scan prompt, add duplicate-check logic in `/api/scan` response
- `templates/index.html`: remove origin from review form and detail panel, add duplicate detection UI (update/save-as-new buttons), remove origin from coffee card display
- SQLite: `origin` column left in place but ignored by `from_row()`
