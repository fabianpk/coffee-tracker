## ADDED Requirements

### Requirement: Edit button on tasting entries
Each tasting entry in the tasting history SHALL display an "edit" button alongside the existing "delete" button. Clicking the edit button SHALL open the tasting modal pre-populated with the tasting's current values.

#### Scenario: Edit button visible
- **WHEN** the tasting history is shown for a coffee
- **THEN** each tasting entry SHALL display an "edit" button

#### Scenario: Clicking edit opens populated modal
- **WHEN** the user clicks the edit button on a tasting with brew_type "espresso", dosage 18.0, score 4, tasting_notes "Chocolate", and comments "Good"
- **THEN** the tasting modal SHALL open with all fields pre-populated with those values

### Requirement: Tasting modal edit mode
The tasting modal SHALL support an edit mode in addition to the existing create mode. In edit mode:
- The coffee selector SHALL be disabled (locked to the tasting's coffee)
- The save button text SHALL read "Update Tasting"
- The modal title SHALL read "Edit Tasting"
- On save, the system SHALL send a PUT request to update the existing tasting instead of POST

#### Scenario: Modal in create mode
- **WHEN** the user clicks "Conduct Tasting" from the top button
- **THEN** the modal title SHALL be "Conduct Tasting", the save button SHALL read "Save Tasting", and the coffee selector SHALL be enabled

#### Scenario: Modal in edit mode
- **WHEN** the user clicks "edit" on an existing tasting entry
- **THEN** the modal title SHALL be "Edit Tasting", the save button SHALL read "Update Tasting", and the coffee selector SHALL be disabled

#### Scenario: Successful edit updates tasting history
- **WHEN** the user edits a tasting and clicks "Update Tasting"
- **THEN** the modal SHALL close, and the tasting history for that coffee SHALL refresh to show the updated values

#### Scenario: Cancel edit
- **WHEN** the user clicks "Cancel" while in edit mode
- **THEN** the modal SHALL close without making any changes
