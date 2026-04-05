## Purpose
Allow rescanning a coffee bag from the detail panel to fill in missing fields without overwriting existing data.

## Requirements

### Requirement: Rescan button in detail panel
The detail panel SHALL include a "Scan another side" button that triggers a camera file input and runs a new scan against the existing `/api/scan` endpoint.

#### Scenario: Rescan button triggers camera
- **WHEN** the user clicks "Scan another side" in the detail panel
- **THEN** the device camera or file picker SHALL open, identical to the initial scan flow

#### Scenario: Rescan loading state
- **WHEN** an image has been selected and the scan is in progress
- **THEN** the "Scan another side" button SHALL be disabled and show a loading indicator

### Requirement: Merge rescan results into open form
After a rescan completes, the system SHALL merge the returned fields into the detail form without overwriting fields that already have a value.

#### Scenario: Rescan fills empty fields only
- **WHEN** a rescan returns a field value that is non-null
- **AND** the corresponding form field is currently empty
- **THEN** the form field SHALL be updated with the scanned value

#### Scenario: Rescan does not overwrite existing values
- **WHEN** a rescan returns a field value that is non-null
- **AND** the corresponding form field already has a value
- **THEN** the existing form field value SHALL remain unchanged

#### Scenario: Rescan with no new information
- **WHEN** a rescan completes and all returned fields are either null or already populated in the form
- **THEN** the form SHALL remain unchanged and no save shall occur automatically
