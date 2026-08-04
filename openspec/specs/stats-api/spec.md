## ADDED Requirements

### Requirement: Stats endpoint returns aggregated tasting data
The system SHALL expose a `GET /api/stats` endpoint that returns tasting scores aggregated per coffee and brew type, grouped by roastery.

#### Scenario: Fetch all stats
- **WHEN** a GET request is made to `/api/stats` with no parameters
- **THEN** the response SHALL contain an `entries` array with objects having `roaster`, `name`, `brew_type`, `avg_score`, and `tasting_count` fields, ordered by roaster name then score descending
- **AND** the response SHALL contain a `brew_types` array listing all distinct brew types with tastings

#### Scenario: Filter by brew type
- **WHEN** a GET request is made to `/api/stats?brew_type=espresso`
- **THEN** the response `entries` array SHALL only include tastings with `brew_type` equal to `espresso`
- **AND** the `brew_types` array SHALL still contain all available brew types

#### Scenario: No rated coffees
- **WHEN** a GET request is made to `/api/stats` and no tastings have scores
- **THEN** the response SHALL contain an empty `entries` array and an empty `brew_types` array
