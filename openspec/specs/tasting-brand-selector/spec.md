## Purpose
Provide brand and coffee dropdown selectors in the tasting modal with sorting by recent tasting date and auto-selection for single-coffee brands.

## Requirements

### Requirement: Brand selector in tasting modal
The tasting modal SHALL display a brand (roaster) dropdown as the first selection step. The dropdown SHALL list all roasters from the database, sorted alphabetically. Selecting a brand SHALL populate the coffee selector with coffees from that brand.

#### Scenario: Brand dropdown shows all roasters
- **WHEN** the tasting modal opens in create mode
- **THEN** the brand dropdown SHALL list all distinct roasters alphabetically

#### Scenario: Selecting a brand populates coffee list
- **WHEN** the user selects "Roaster X" from the brand dropdown
- **THEN** the coffee dropdown SHALL appear and be populated with all coffees from "Roaster X", sorted by most recent tasting date descending

### Requirement: Coffee selector filtered by brand
The tasting modal SHALL display a coffee dropdown that shows only coffees belonging to the selected brand. The coffee dropdown SHALL be hidden or disabled until a brand is selected.

#### Scenario: Coffee dropdown hidden before brand selection
- **WHEN** the tasting modal opens and no brand is selected
- **THEN** the coffee dropdown SHALL not be visible

#### Scenario: Coffee dropdown visible after brand selection
- **WHEN** the user selects a brand
- **THEN** the coffee dropdown SHALL become visible and contain only coffees from that brand

### Requirement: Coffees sorted by last tasting date
Within the coffee dropdown, coffees SHALL be sorted by most recent tasting date (descending). Coffees that have never been tasted SHALL appear at the end of the list.

#### Scenario: Coffee with recent tasting appears first
- **WHEN** brand "Roaster X" has Coffee A (last tasted yesterday) and Coffee B (last tasted last week)
- **THEN** Coffee A SHALL appear before Coffee B in the dropdown

#### Scenario: Never-tasted coffee appears last
- **WHEN** brand "Roaster X" has Coffee A (tasted once) and Coffee B (never tasted)
- **THEN** Coffee B SHALL appear after Coffee A in the dropdown

### Requirement: Auto-select single coffee
When a brand has exactly one coffee, that coffee SHALL be automatically selected after the user selects the brand. The coffee dropdown SHALL still be visible showing the selected coffee.

#### Scenario: Brand with one coffee auto-selects
- **WHEN** the user selects a brand that has exactly one coffee "Morning Blend"
- **THEN** "Morning Blend" SHALL be automatically selected in the coffee dropdown

#### Scenario: Brand with multiple coffees does not auto-select
- **WHEN** the user selects a brand that has 3 coffees
- **THEN** no coffee SHALL be auto-selected; the user MUST choose one

### Requirement: Edit mode shows pre-filled brand and coffee
In edit mode, the brand dropdown SHALL show the tasting's coffee roaster and the coffee dropdown SHALL show the tasting's coffee name. Both dropdowns SHALL be disabled.

#### Scenario: Edit mode pre-fills both selectors
- **WHEN** the user edits a tasting for "Roaster X - Morning Blend"
- **THEN** the brand dropdown SHALL show "Roaster X" (disabled) and the coffee dropdown SHALL show "Morning Blend" (disabled)
