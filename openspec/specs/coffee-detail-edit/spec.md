### Requirement: Coffee detail panel
The system SHALL display a full-screen overlay panel when the user taps/clicks a coffee card in the list. The panel SHALL show all CoffeeBean fields (roaster, name, country_grown, country_roasted, origin, process, roast_level, tasting_notes, weight, price, brew_score, espresso_score, other, notes) as editable inputs.

#### Scenario: Open detail panel by clicking a card
- **WHEN** the user clicks a coffee item in the list
- **THEN** the detail panel SHALL slide into view showing all fields pre-populated with the entry's current values

#### Scenario: Detail panel shows all fields
- **WHEN** the detail panel is open
- **THEN** all CoffeeBean fields SHALL be displayed as editable form inputs, matching the layout used in the initial review form

#### Scenario: Close detail panel without saving
- **WHEN** the user clicks the close button with no unsaved changes
- **THEN** the panel SHALL close and return to the list view

#### Scenario: Warn before closing with unsaved changes
- **WHEN** the user has edited one or more fields and clicks the close button
- **THEN** the system SHALL prompt the user to confirm discarding changes before closing

### Requirement: Edit and save a coffee entry
The system SHALL allow the user to edit any field in the detail panel and save changes back to the database via `PUT /api/coffees/<id>`.

#### Scenario: Save edited entry
- **WHEN** the user modifies one or more fields and clicks Save
- **THEN** the system SHALL send a PUT request to `/api/coffees/<id>` with all current field values
- **AND** on success the panel SHALL close and the list SHALL refresh to show updated values

#### Scenario: PUT /api/coffees/<id> updates the entry
- **WHEN** a PUT request is made to `/api/coffees/<id>` with a valid JSON body containing CoffeeBean fields
- **THEN** the corresponding database row SHALL be updated and the response SHALL return the updated entry as JSON

### Requirement: GET /api/coffees/<id> single entry route
The system SHALL provide a `GET /api/coffees/<id>` route that returns a single coffee entry as JSON.

#### Scenario: Fetch existing entry
- **WHEN** a GET request is made to `/api/coffees/1` for an entry that exists
- **THEN** the response SHALL be HTTP 200 with the CoffeeBean fields as JSON

#### Scenario: Fetch non-existent entry
- **WHEN** a GET request is made to `/api/coffees/999` for an entry that does not exist
- **THEN** the response SHALL be HTTP 404
