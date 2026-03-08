## ADDED Requirements

### Requirement: Delete coffee from detail panel
The detail panel SHALL include a "Delete" button that allows the user to delete the currently viewed coffee entry. The button SHALL be visually styled as a destructive action (red) and placed at the bottom of the panel, separated from save/rescan actions. Clicking it SHALL show a confirmation dialog. On confirmation, the system SHALL call `DELETE /api/coffees/<id>`, close the detail panel, and refresh the coffee list.

#### Scenario: Delete button visible in detail panel
- **WHEN** the user opens the detail panel for a coffee entry
- **THEN** a "Delete" button SHALL be visible at the bottom of the panel, styled as a destructive action

#### Scenario: Delete with confirmation
- **WHEN** the user clicks "Delete" in the detail panel and confirms the dialog
- **THEN** the coffee and its tastings SHALL be deleted via the API, the detail panel SHALL close, and the coffee list SHALL refresh

#### Scenario: Cancel delete
- **WHEN** the user clicks "Delete" in the detail panel and cancels the confirmation dialog
- **THEN** no deletion SHALL occur and the detail panel SHALL remain open
