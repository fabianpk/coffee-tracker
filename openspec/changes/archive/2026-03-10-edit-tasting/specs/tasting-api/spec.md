## ADDED Requirements

### Requirement: Update tasting endpoint
The system SHALL expose a `PUT /api/tastings/<id>` endpoint that accepts a JSON body with tasting fields (`brew_type`, `dosage`, `score`, `tasting_notes`, `comments`). The endpoint SHALL update the existing tasting record and return the updated tasting object. The `created_at` timestamp SHALL NOT be modified.

#### Scenario: Successful update
- **WHEN** a PUT request is made to `/api/tastings/5` with `{ "brew_type": "espresso", "score": 4, "comments": "Updated notes" }`
- **THEN** the response SHALL have status 200 and return the full updated tasting object including `id`, `coffee_id`, and original `created_at`

#### Scenario: Tasting not found
- **WHEN** a PUT request is made to `/api/tastings/999` where tasting 999 does not exist
- **THEN** the response SHALL have status 404 and return `{ "error": "Not found" }`

#### Scenario: Partial update
- **WHEN** a PUT request is made with only `score` in the body
- **THEN** the response SHALL update only the `score` field and preserve all other existing field values
