## ADDED Requirements

### Requirement: Stats button in top navigation
The system SHALL display a "Stats" button in the top button bar alongside the existing "Add Coffee to Database" and "Conduct Tasting" buttons.

#### Scenario: User opens stats view
- **WHEN** the user taps the "Stats" button
- **THEN** the home view SHALL be hidden and the stats view SHALL be displayed

### Requirement: Stats view displays coffees grouped by roastery
The stats view SHALL show rated coffees grouped by roastery, with each roastery section displaying a weighted average score and individual coffee entries showing name, average score, brew type, and tasting count.

#### Scenario: Roastery grouping with averages
- **WHEN** the stats view is displayed with rated coffees
- **THEN** coffees SHALL be grouped under their roastery name
- **AND** each roastery header SHALL show the weighted average score across all its coffees

#### Scenario: Brew type hidden when filtered
- **WHEN** the user filters by a specific brew type
- **THEN** the brew type column SHALL be hidden from individual coffee entries since all entries share the same brew type

### Requirement: Brew type filter dropdown
The stats view SHALL include a dropdown to filter results by brew type, populated with all available brew types from the database.

#### Scenario: Filter by brew type
- **WHEN** the user selects a brew type from the dropdown
- **THEN** the stats view SHALL reload showing only tastings for that brew type

#### Scenario: Clear filter
- **WHEN** the user selects "All brew types" from the dropdown
- **THEN** the stats view SHALL show all tastings across all brew types

### Requirement: Back navigation
The stats view SHALL include a back button that returns the user to the home screen.

#### Scenario: Navigate back
- **WHEN** the user taps the back button in the stats view
- **THEN** the stats view SHALL be hidden and the home view SHALL be displayed
