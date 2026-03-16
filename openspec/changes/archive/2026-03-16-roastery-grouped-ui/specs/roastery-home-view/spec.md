## ADDED Requirements

### Requirement: Home screen shows recent tastings section
The home screen SHALL display a "Recent Tastings" section at the top of the main content area (below the action buttons, above the roastery grid). This section SHALL show the last 2 tastings across all coffees, ordered by most recent first.

Each tasting card SHALL display: brew type with emoji, dosage, grind level, score (as stars), tasting notes, the coffee name, and the roaster name. If fewer than 2 tastings exist, the section SHALL show only what exists. If no tastings exist, the section SHALL not be rendered.

#### Scenario: Two recent tastings displayed
- **WHEN** the home screen loads and there are 5 tastings across various coffees
- **THEN** the Recent Tastings section SHALL show the 2 most recently created tastings with coffee name and roaster context

#### Scenario: One tasting exists
- **WHEN** the home screen loads and there is only 1 tasting total
- **THEN** the Recent Tastings section SHALL show that single tasting

#### Scenario: No tastings exist
- **WHEN** the home screen loads and there are no tastings
- **THEN** the Recent Tastings section SHALL not be rendered

### Requirement: Home screen shows roastery button grid
The home screen SHALL display a grid of buttons, one per distinct roastery. Each button SHALL display the roastery's cached emoji followed by the roastery name. Buttons SHALL be sorted alphabetically by roastery name.

#### Scenario: Multiple roasteries displayed
- **WHEN** the home screen loads and there are coffees from 3 different roasters
- **THEN** 3 roastery buttons SHALL be rendered in alphabetical order, each showing its emoji and name

#### Scenario: No coffees exist
- **WHEN** the home screen loads and there are no coffees
- **THEN** the empty state message "No coffees yet. Add your first coffee!" SHALL be displayed instead of the roastery grid

### Requirement: Flat coffee list is replaced
The existing flat list of all coffee cards SHALL be replaced by the roastery button grid. Individual coffee cards SHALL only be visible within a roastery detail view.

#### Scenario: Home screen no longer shows individual coffee cards
- **WHEN** the home screen loads with 10 coffees from 3 roasters
- **THEN** the main area SHALL show the roastery grid (3 buttons), NOT 10 individual coffee cards
