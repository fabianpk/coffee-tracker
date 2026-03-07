## MODIFIED Requirements

### Requirement: CoffeeBean from scan result
The `CoffeeBean` class SHALL provide a classmethod `from_scan(data: dict)` that maps Claude API scan output to a `CoffeeBean` instance. The scan dict uses key `roastery` which SHALL be mapped to the `roaster` property. The method SHALL also accept and preserve a `matched_roaster` key if present, storing it so it can be included in `to_dict()` output.

#### Scenario: Mapping scan output to CoffeeBean
- **WHEN** `CoffeeBean.from_scan({"roastery": "Square Mile", "name": "Red Brick", ...})` is called
- **THEN** the returned instance SHALL have `roaster` set to `"Square Mile"` and `name` set to `"Red Brick"`

#### Scenario: Missing fields in scan output
- **WHEN** `CoffeeBean.from_scan({})` is called with an empty dict
- **THEN** all properties SHALL be `None` (no KeyError raised)

#### Scenario: Scan output with matched_roaster
- **WHEN** `CoffeeBean.from_scan({"roastery": "Gringo Nordic Roasters", "matched_roaster": "Gringo Nordic Roasters", ...})` is called
- **THEN** the returned instance SHALL have `roaster` set to `"Gringo Nordic Roasters"` and `to_dict()` SHALL include `"matched_roaster": "Gringo Nordic Roasters"`

#### Scenario: Scan output without matched_roaster
- **WHEN** `CoffeeBean.from_scan({"roastery": "New Place", ...})` is called without a `matched_roaster` key
- **THEN** `to_dict()` SHALL include `"matched_roaster": null`
