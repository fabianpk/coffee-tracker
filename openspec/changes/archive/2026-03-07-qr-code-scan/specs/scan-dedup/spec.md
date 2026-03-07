## MODIFIED Requirements

### Requirement: Duplicate detection after scan
After a scan populates the review form, the frontend SHALL check the cached coffee list for an existing coffee with the same `roaster` and `name` (case-insensitive, trimmed). If a match is found, the review form SHALL display an info banner (e.g. "A coffee with this name already exists") and change the save options. If a `qr_url` was detected, the banner MAY also mention that data was enriched from the product page.

#### Scenario: Scan returns a known coffee
- **WHEN** a scan returns roaster "Gringo" and name "Finca La Esperanza" and a coffee with the same roaster+name exists
- **THEN** the review form SHALL show a duplicate warning banner and display "Update Existing" and "Save as New" buttons instead of the normal "Save" button

#### Scenario: Scan returns a new coffee
- **WHEN** a scan returns a roaster+name combination that does not exist in the database
- **THEN** the review form SHALL show the normal "Save" button with no warning

#### Scenario: Scan with QR enrichment shows source info
- **WHEN** a scan returns data with a non-null `qr_url`
- **THEN** the review form SHALL display a note indicating data was enriched from the product page URL
