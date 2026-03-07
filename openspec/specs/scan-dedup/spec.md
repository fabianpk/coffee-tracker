### Requirement: Duplicate detection after scan
After a scan populates the review form, the frontend SHALL check the cached coffee list for an existing coffee with the same `roaster` and `name` (case-insensitive, trimmed). If a match is found, the review form SHALL display an info banner (e.g. "A coffee with this name already exists") and change the save options.

#### Scenario: Scan returns a known coffee
- **WHEN** a scan returns roaster "Gringo" and name "Finca La Esperanza" and a coffee with the same roaster+name exists
- **THEN** the review form SHALL show a duplicate warning banner and display "Update Existing" and "Save as New" buttons instead of the normal "Save" button

#### Scenario: Scan returns a new coffee
- **WHEN** a scan returns a roaster+name combination that does not exist in the database
- **THEN** the review form SHALL show the normal "Save" button with no warning

### Requirement: Update existing coffee from scan
When the user clicks "Update Existing" on a duplicate match, the system SHALL send a `PUT /api/coffees/<id>` request with the form data to update the matched coffee entry.

#### Scenario: Update existing coffee
- **WHEN** the user clicks "Update Existing" after a duplicate is detected
- **THEN** the matched coffee SHALL be updated via PUT and the coffee list SHALL reload

### Requirement: Save as new requires uniqueness
When the user clicks "Save as New" on a duplicate match, the system SHALL verify that either the `roaster` or `name` field has been changed from the matched coffee's values before saving. If both are unchanged, the save SHALL be blocked with an alert.

#### Scenario: Save as new with changed name
- **WHEN** the user changes the name field and clicks "Save as New"
- **THEN** the coffee SHALL be saved as a new entry

#### Scenario: Save as new without changes blocked
- **WHEN** the user clicks "Save as New" without changing roaster or name
- **THEN** an alert SHALL inform the user to change the name or roaster first and the save SHALL NOT proceed
