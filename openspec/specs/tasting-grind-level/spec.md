### Requirement: Grind level selector in tasting modal
The tasting modal SHALL include a grind-level selector using the same `<select>` spinning-wheel pattern as the dosage selector. The selector SHALL offer values from 3.0 to 22.0 in increments of 0.2, displayed with one decimal place.

#### Scenario: Grind level selector is visible
- **WHEN** the tasting modal opens (create or edit mode)
- **THEN** a grind-level dropdown SHALL be visible, using the same styling as the dosage dropdown

#### Scenario: Grind level options
- **WHEN** the user opens the grind-level dropdown
- **THEN** the options SHALL range from 3.0 to 22.0 in steps of 0.2 (i.e., 3.0, 3.2, 3.4, ..., 21.8, 22.0)

### Requirement: Grind level default from previous tasting
When opening the tasting modal for a coffee that has previous tastings with a grind level, the grind-level selector SHALL default to the grind level from the most recent tasting of that coffee.

#### Scenario: Coffee with previous grind level
- **WHEN** the user selects a coffee that has a previous tasting with grind_level 6.4
- **THEN** the grind-level selector SHALL default to 6.4

#### Scenario: Coffee with no previous grind level
- **WHEN** the user selects a coffee that has no previous tastings (or none with a grind level set)
- **THEN** the grind-level selector SHALL use the brew-type default

### Requirement: Grind level brew-type defaults
When no previous grind level exists for the selected coffee, the grind-level selector SHALL use brew-type-specific defaults:
- Espresso: 4.0
- Brew: 14.0
- Metal Brew: 18.0
- Cappuccino: 4.0

#### Scenario: Default for espresso
- **WHEN** the user selects brew type "Espresso" and no prior grind level exists for the coffee
- **THEN** the grind-level selector SHALL default to 4.0

#### Scenario: Default for brew
- **WHEN** the user selects brew type "Brew" and no prior grind level exists for the coffee
- **THEN** the grind-level selector SHALL default to 14.0

#### Scenario: Default for metal brew
- **WHEN** the user selects brew type "Metal Brew" and no prior grind level exists for the coffee
- **THEN** the grind-level selector SHALL default to 18.0

#### Scenario: Default for cappuccino
- **WHEN** the user selects brew type "Cappuccino" and no prior grind level exists for the coffee
- **THEN** the grind-level selector SHALL default to 4.0

#### Scenario: Changing brew type updates default
- **WHEN** the user changes the brew type and has not manually adjusted the grind level
- **THEN** the grind-level selector SHALL update to the new brew-type default

### Requirement: Grind level displayed in tasting history
Each tasting entry in the tasting history SHALL display the grind level alongside the existing brew type and dosage information.

#### Scenario: Tasting with grind level
- **WHEN** a tasting history entry has grind_level 6.4
- **THEN** the entry SHALL display the grind level (e.g., "grind 6.4")

#### Scenario: Tasting without grind level
- **WHEN** a tasting history entry has grind_level null
- **THEN** the entry SHALL not display any grind level indicator

### Requirement: Grind level pre-populated in edit mode
When editing an existing tasting, the grind-level selector SHALL be pre-populated with the tasting's current grind_level value.

#### Scenario: Edit tasting with grind level
- **WHEN** the user clicks edit on a tasting with grind_level 8.2
- **THEN** the grind-level selector SHALL show 8.2 as the selected value
