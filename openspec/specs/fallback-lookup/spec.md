## Purpose
Implement a fallback lookup chain using baristashopen.se when the primary roastery provider returns no results.

## Requirements

### Requirement: Fallback lookup chain
The `lookup_coffee()` function SHALL implement a fallback chain. When the primary roastery provider returns no results (or no provider exists for the roaster), the system SHALL automatically attempt a lookup using the fallback provider (baristashopen.se). The fallback SHALL search using the coffee name.

#### Scenario: Primary provider succeeds
- **WHEN** `lookup_coffee("Morgon", "Ethiopia Guji")` is called and the Morgon ShopifySearcher returns a result
- **THEN** the result SHALL be returned with `_source` set to `"roastery"` and no fallback attempt SHALL be made

#### Scenario: Primary provider fails, fallback succeeds
- **WHEN** `lookup_coffee("Morgon", "Discontinued Blend")` is called and the Morgon ShopifySearcher returns None
- **THEN** the system SHALL attempt lookup via the baristashopen.se TextalkSearcher
- **AND** if the fallback finds the coffee, the result SHALL be returned with `_source` set to `"baristashopen"`

#### Scenario: No primary provider, fallback succeeds
- **WHEN** `lookup_coffee("Unknown Roastery", "Ethiopia Guji")` is called and no provider exists for "Unknown Roastery"
- **THEN** the system SHALL skip the primary lookup and attempt the baristashopen.se fallback directly
- **AND** if the fallback finds the coffee, the result SHALL be returned with `_source` set to `"baristashopen"`

#### Scenario: Both primary and fallback fail
- **WHEN** `lookup_coffee("Morgon", "Nonexistent XYZ")` is called and both the primary provider and the fallback return None
- **THEN** `lookup_coffee()` SHALL return `None`

### Requirement: API response includes source information
The `POST /api/lookup` endpoint SHALL include a `source` field in successful responses indicating where the data was found. The value SHALL be `"roastery"` when found via the primary provider or `"baristashopen"` when found via the fallback.

#### Scenario: Source field in primary result
- **WHEN** a lookup succeeds via the primary roastery provider
- **THEN** the JSON response SHALL include `"source": "roastery"`

#### Scenario: Source field in fallback result
- **WHEN** a lookup succeeds via the baristashopen.se fallback
- **THEN** the JSON response SHALL include `"source": "baristashopen"`

### Requirement: Lookup button always visible for non-empty roaster
Since the fallback provider is always available, the lookup button SHALL be shown whenever the roaster field contains a non-empty value, regardless of whether a dedicated provider exists for that roaster.

#### Scenario: Known roaster shows lookup button
- **WHEN** the user enters "Gringo" in the roaster field
- **THEN** the lookup button SHALL be visible

#### Scenario: Unknown roaster still shows lookup button
- **WHEN** the user enters "Some Unknown Roastery" in the roaster field
- **THEN** the lookup button SHALL still be visible (because the fallback is always available)

#### Scenario: Empty roaster hides lookup button
- **WHEN** the roaster field is empty
- **THEN** the lookup button SHALL be hidden

### Requirement: Frontend indicates fallback source
When lookup results include `source: "baristashopen"`, the frontend SHALL display a brief note near the lookup button indicating the data was found on Baristashopen.se rather than the roastery's own website.

#### Scenario: Fallback source indication
- **WHEN** the lookup returns results with `"source": "baristashopen"`
- **THEN** a note such as "Found on Baristashopen.se" SHALL be displayed near the lookup button

#### Scenario: Primary source no indication
- **WHEN** the lookup returns results with `"source": "roastery"`
- **THEN** no special source note SHALL be displayed (or a note like "Found on roastery website")
