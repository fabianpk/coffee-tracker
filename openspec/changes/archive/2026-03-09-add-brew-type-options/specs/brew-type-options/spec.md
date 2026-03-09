## ADDED Requirements

### Requirement: Brew type registry
The frontend SHALL define a brew type registry mapping each brew type key to a display label and emoji. The registry SHALL include the following entries:

| Key           | Label        | Emoji |
|---------------|-------------|-------|
| `espresso`    | Espresso    | (espresso-appropriate emoji) |
| `brew`        | Brew        | (brew-appropriate emoji) |
| `metal_brew`  | Metal Brew  | (metal-brew-appropriate emoji) |
| `cappuccino`  | Cappuccino  | (cappuccino-appropriate emoji) |

#### Scenario: All four brew types are defined
- **WHEN** the brew type registry is accessed
- **THEN** it SHALL contain exactly four entries: `espresso`, `brew`, `metal_brew`, `cappuccino`

#### Scenario: Each entry has an emoji and label
- **WHEN** any brew type entry is accessed from the registry
- **THEN** it SHALL have a non-empty `emoji` string and a non-empty `label` string

### Requirement: Brew type buttons rendered from registry
The tasting modal brew type selector SHALL render one button per registry entry. Each button SHALL display the emoji followed by the label text.

#### Scenario: Four brew type buttons displayed
- **WHEN** the tasting modal opens
- **THEN** four brew type buttons SHALL be visible: Espresso, Brew, Metal Brew, and Cappuccino, each with its emoji

#### Scenario: Selecting a brew type
- **WHEN** the user clicks a brew type button
- **THEN** that button SHALL become active and the brew type key SHALL be stored for submission

### Requirement: Brew type display with emoji in tasting history
When displaying a tasting's brew type in the tasting history, the system SHALL look up the brew type key in the registry and display the emoji followed by the label. If the key is not found in the registry, the raw value SHALL be displayed without an emoji.

#### Scenario: Known brew type in tasting history
- **WHEN** a tasting with `brew_type: "cappuccino"` is rendered in the history
- **THEN** it SHALL display the cappuccino emoji followed by "Cappuccino"

#### Scenario: Unknown brew type in tasting history
- **WHEN** a tasting with a `brew_type` value not in the registry is rendered
- **THEN** it SHALL display the raw brew type value without an emoji
