## ADDED Requirements

### Requirement: Roastery detail view on button tap
When a roastery button is tapped on the home screen, the roastery grid SHALL be replaced with a detail view showing all coffees from that roastery and their associated tastings.

#### Scenario: Tap a roastery with 3 coffees
- **WHEN** the user taps the "Koppi" roastery button and Koppi has 3 coffees
- **THEN** the roastery grid SHALL be hidden and a detail view SHALL appear showing 3 coffee cards with Koppi's emoji and name as header

#### Scenario: Roastery with one coffee
- **WHEN** the user taps a roastery button for a roaster with 1 coffee
- **THEN** the detail view SHALL show that single coffee card

### Requirement: Roastery detail shows coffee cards with tastings
Each coffee in the roastery detail view SHALL be rendered as a card showing: coffee name, origin, bean type, tasting notes (as tags), price, average score, and date added. Each card SHALL show its tasting history inline (expanded by default), not requiring an extra toggle.

#### Scenario: Coffee card with tastings
- **WHEN** the roastery detail view shows a coffee that has 2 tastings
- **THEN** the coffee card SHALL display both tastings inline with brew type, dosage, grind level, score, and date

#### Scenario: Coffee card with no tastings
- **WHEN** the roastery detail view shows a coffee that has no tastings
- **THEN** the coffee card SHALL display "No tastings yet" in the tasting area

### Requirement: Back navigation from roastery detail
The roastery detail view SHALL include a back button/header that returns the user to the home screen (roastery grid + recent tastings). Tapping back SHALL restore the previous home screen state.

#### Scenario: Navigate back to home
- **WHEN** the user is viewing a roastery detail and taps the back button
- **THEN** the roastery detail view SHALL be hidden and the home screen with roastery grid SHALL be restored

### Requirement: Coffee card tap opens detail panel
Tapping a coffee card in the roastery detail view SHALL open the existing detail/edit panel (same behavior as the current flat list).

#### Scenario: Open detail panel from roastery view
- **WHEN** the user taps a coffee card within the roastery detail view
- **THEN** the existing detail panel SHALL open with that coffee's data, allowing editing and deletion
