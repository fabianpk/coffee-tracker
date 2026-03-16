## ADDED Requirements

### Requirement: GET /api/tastings/recent returns recent tastings with coffee context
The system SHALL provide a `GET /api/tastings/recent` endpoint that accepts an optional `limit` query parameter (default 2). It SHALL return the N most recent tastings across all coffees, ordered by `created_at` descending. Each tasting object SHALL include `coffee_name` and `coffee_roaster` fields joined from the `coffees` table.

#### Scenario: Fetch 2 most recent tastings
- **WHEN** a GET to `/api/tastings/recent?limit=2` is made and 10 tastings exist
- **THEN** the response SHALL be HTTP 200 with a JSON array of 2 tasting objects, each including `coffee_name`, `coffee_roaster`, and all standard tasting fields

#### Scenario: Fetch recent with no tastings
- **WHEN** a GET to `/api/tastings/recent` is made and no tastings exist
- **THEN** the response SHALL be HTTP 200 with an empty JSON array

#### Scenario: Default limit
- **WHEN** a GET to `/api/tastings/recent` is made without a `limit` parameter
- **THEN** the response SHALL return at most 2 tastings
