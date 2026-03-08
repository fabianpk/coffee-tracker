## MODIFIED Requirements

### Requirement: Coffee detail panel
The system SHALL display a full-screen overlay panel when the user taps/clicks a coffee card in the list. The panel SHALL show all CoffeeBean fields as editable inputs. The `comments` field SHALL be displayed as a textarea labeled "General Comments".

#### Scenario: Detail panel shows all fields
- **WHEN** the detail panel is open
- **THEN** all CoffeeBean fields SHALL be displayed as editable form inputs, with the `comments` textarea labeled "General Comments"

#### Scenario: Comments field placeholder
- **WHEN** the detail panel is open
- **THEN** the comments textarea SHALL display "General comments" as placeholder text
