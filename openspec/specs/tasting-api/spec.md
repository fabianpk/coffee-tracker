### Requirement: POST /api/tastings creates a tasting
The system SHALL provide a `POST /api/tastings` route that accepts a JSON body and saves a new `Tasting` to the database.

Required fields: `coffee_id`. Optional fields: `brew_type`, `dosage`, `score`, `notes`.

- On success, SHALL return HTTP 201 with the saved tasting as JSON (including `id` and `created_at`).
- If `coffee_id` is missing or does not refer to an existing coffee, SHALL return HTTP 400.

#### Scenario: Save a tasting with all fields
- **WHEN** a POST to `/api/tastings` is made with `{"coffee_id": 1, "brew_type": "espresso", "dosage": "18g", "score": 4, "notes": "Sweet finish"}`
- **THEN** the response SHALL be HTTP 201 with a JSON body containing all submitted fields plus `id` and `created_at`

#### Scenario: Save a tasting with only coffee_id
- **WHEN** a POST to `/api/tastings` is made with `{"coffee_id": 1}`
- **THEN** the response SHALL be HTTP 201 with optional fields as `null`

#### Scenario: Missing coffee_id
- **WHEN** a POST to `/api/tastings` is made without `coffee_id`
- **THEN** the response SHALL be HTTP 400

### Requirement: GET /api/tastings lists tastings for a coffee
The system SHALL provide a `GET /api/tastings?coffee_id=<id>` route that returns all tastings for the given coffee, ordered by `created_at` descending.

#### Scenario: List tastings for a coffee
- **WHEN** a GET to `/api/tastings?coffee_id=1` is made and coffee 1 has two tastings
- **THEN** the response SHALL be HTTP 200 with a JSON array of two tasting objects, most recent first

#### Scenario: No tastings for coffee
- **WHEN** a GET to `/api/tastings?coffee_id=99` is made and coffee 99 has no tastings
- **THEN** the response SHALL be HTTP 200 with an empty JSON array `[]`

### Requirement: GET /api/coffees includes average_score
The existing `GET /api/coffees` route SHALL include an `average_score` field on each coffee object, computed as the average of all `score` values from the coffee's tastings (rounded to one decimal place), or `null` if no tastings exist.

#### Scenario: Coffee with tastings returns average_score
- **WHEN** a GET to `/api/coffees` is made and a coffee has tastings with scores 4 and 5
- **THEN** that coffee's JSON object SHALL include `"average_score": 4.5`

#### Scenario: Coffee with no tastings returns null average_score
- **WHEN** a GET to `/api/coffees` is made and a coffee has no tastings
- **THEN** that coffee's JSON object SHALL include `"average_score": null`
