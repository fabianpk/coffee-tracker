## MODIFIED Requirements

### Requirement: POST /api/tastings creates a tasting
The system SHALL provide a `POST /api/tastings` route that accepts a JSON body and saves a new `Tasting` to the database.

Required fields: `coffee_id`. Optional fields: `brew_type`, `dosage`, `grind_level`, `score`, `tasting_notes`, `comments`.

- On success, SHALL return HTTP 201 with the saved tasting as JSON (including `id` and `created_at`).
- If `coffee_id` is missing or does not refer to an existing coffee, SHALL return HTTP 400.

#### Scenario: Save a tasting with all fields
- **WHEN** a POST to `/api/tastings` is made with `{"coffee_id": 1, "brew_type": "espresso", "dosage": 18.0, "grind_level": 4.0, "score": 4, "tasting_notes": "Sweet finish"}`
- **THEN** the response SHALL be HTTP 201 with a JSON body containing all submitted fields including `grind_level` plus `id` and `created_at`

#### Scenario: Save a tasting with only coffee_id
- **WHEN** a POST to `/api/tastings` is made with `{"coffee_id": 1}`
- **THEN** the response SHALL be HTTP 201 with optional fields including `grind_level` as `null`

#### Scenario: Missing coffee_id
- **WHEN** a POST to `/api/tastings` is made without `coffee_id`
- **THEN** the response SHALL be HTTP 400

### Requirement: Update tasting endpoint
The system SHALL expose a `PUT /api/tastings/<id>` endpoint that accepts a JSON body with tasting fields (`brew_type`, `dosage`, `grind_level`, `score`, `tasting_notes`, `comments`). The endpoint SHALL update the existing tasting record and return the updated tasting object. The `created_at` timestamp SHALL NOT be modified.

#### Scenario: Successful update
- **WHEN** a PUT request is made to `/api/tastings/5` with `{ "brew_type": "espresso", "grind_level": 5.6, "score": 4, "comments": "Updated notes" }`
- **THEN** the response SHALL have status 200 and return the full updated tasting object including `grind_level`, `id`, `coffee_id`, and original `created_at`

#### Scenario: Tasting not found
- **WHEN** a PUT request is made to `/api/tastings/999` where tasting 999 does not exist
- **THEN** the response SHALL have status 404 and return `{ "error": "Not found" }`

#### Scenario: Partial update
- **WHEN** a PUT request is made with only `grind_level` in the body
- **THEN** the response SHALL update only the `grind_level` field and preserve all other existing field values
