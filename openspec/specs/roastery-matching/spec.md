## Purpose
Match scanned roastery names against known roasters in the database using fuzzy comparison to normalize roaster names.

## Requirements

### Requirement: Match scanned roastery against known roasters
After extracting coffee details from a scan, the system SHALL compare the scanned `roastery` name against all distinct `roaster` values in the `coffees` table. Matching SHALL use case-insensitive fuzzy comparison via `difflib.SequenceMatcher`.

A match SHALL be accepted when:
- `SequenceMatcher.ratio() >= 0.7`, OR
- One name is a substring of the other and the shorter string is at least 4 characters

If multiple roasters match, the one with the highest ratio SHALL be selected.

#### Scenario: Exact match with different casing
- **WHEN** a scan returns `roastery: "gringo"` and the database contains a coffee with `roaster: "Gringo"`
- **THEN** the system SHALL match to "Gringo"

#### Scenario: Substring match
- **WHEN** a scan returns `roastery: "Gringo"` and the database contains a coffee with `roaster: "Gringo Nordic Roasters"`
- **THEN** the system SHALL match to "Gringo Nordic Roasters"

#### Scenario: Fuzzy match above threshold
- **WHEN** a scan returns `roastery: "Gringo Nordic"` and the database contains `roaster: "Gringo Nordic Roasters"` (ratio ~0.83)
- **THEN** the system SHALL match to "Gringo Nordic Roasters"

#### Scenario: No match found
- **WHEN** a scan returns `roastery: "Brand New Roasters"` and no known roaster is similar
- **THEN** the system SHALL use the raw scanned name as-is

#### Scenario: First-ever scan (empty database)
- **WHEN** a scan returns a roastery name and no coffees exist in the database
- **THEN** the system SHALL use the raw scanned name as-is

### Requirement: Scan response includes matched_roaster field
The `POST /api/scan` response SHALL include a `matched_roaster` field.

- If a known roaster was matched: `matched_roaster` SHALL be the matched roaster name, and `roaster` SHALL be overwritten with the same value
- If no match: `matched_roaster` SHALL be `null`, and `roaster` SHALL be the raw scanned value

#### Scenario: Scan with successful match
- **WHEN** a scan matches "Gringo" to known roaster "Gringo Nordic Roasters"
- **THEN** the response SHALL include `"roaster": "Gringo Nordic Roasters"` and `"matched_roaster": "Gringo Nordic Roasters"`

#### Scenario: Scan with no match
- **WHEN** a scan finds no matching roaster
- **THEN** the response SHALL include the raw scanned roaster name and `"matched_roaster": null`
