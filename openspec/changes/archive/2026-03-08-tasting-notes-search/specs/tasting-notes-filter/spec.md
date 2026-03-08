## ADDED Requirements

### Requirement: Filter coffees by tasting note
The `GET /api/coffees` endpoint SHALL accept an optional `?note=` query parameter. When provided, the response SHALL include only coffees whose `tasting_notes` field contains the specified note as an individual item in the comma-separated list. Matching SHALL be case-insensitive.

#### Scenario: Filter by exact note match
- **WHEN** a GET request is made to `/api/coffees?note=Chocolate`
- **THEN** the response SHALL include coffees with tasting_notes "Chocolate, Strawberry, Peach" and "Raspberry, Chocolate, Rum" but NOT "Chocolate Fudge, Berry"

#### Scenario: Case-insensitive matching
- **WHEN** a GET request is made to `/api/coffees?note=chocolate`
- **THEN** the response SHALL include coffees with tasting_notes "Chocolate, Berry" (matching is case-insensitive)

#### Scenario: No note parameter returns all coffees
- **WHEN** a GET request is made to `/api/coffees` without a `note` parameter
- **THEN** the response SHALL return all coffees as before

#### Scenario: No matches found
- **WHEN** a GET request is made to `/api/coffees?note=Unicorn`
- **THEN** the response SHALL return an empty array

### Requirement: Tasting notes displayed as tags
The frontend SHALL render each coffee's tasting notes as individual tag chips instead of a single text line. Each note in the comma-separated list SHALL be displayed as a separate styled tag.

#### Scenario: Multiple notes rendered as separate tags
- **WHEN** a coffee card is displayed with tasting_notes "Chocolate, Strawberry, Peach"
- **THEN** three separate tag elements SHALL be rendered: "Chocolate", "Strawberry", "Peach"

#### Scenario: Null tasting notes
- **WHEN** a coffee card has no tasting_notes
- **THEN** no tags SHALL be rendered

### Requirement: Clickable tasting note tags filter the list
Clicking a tasting note tag SHALL filter the coffee list to show only coffees that share that note. The active filter SHALL be displayed and clearable.

#### Scenario: Click a tag to filter
- **WHEN** the user clicks the "Chocolate" tag on any coffee card
- **THEN** the coffee list SHALL filter to show only coffees with "Chocolate" in their tasting notes
- **AND** an active filter indicator SHALL be displayed showing "Chocolate" with a clear/close button

#### Scenario: Clear the filter
- **WHEN** the user clicks the clear button on the active filter indicator
- **THEN** the full unfiltered coffee list SHALL be restored

### Requirement: Get all unique tasting notes
The system SHALL provide a `GET /api/tasting-notes` endpoint that returns a sorted list of all unique individual tasting notes across all coffees.

#### Scenario: Return unique notes
- **WHEN** a GET request is made to `/api/tasting-notes`
- **THEN** the response SHALL be a JSON array of unique tasting note strings, sorted alphabetically, with no duplicates
