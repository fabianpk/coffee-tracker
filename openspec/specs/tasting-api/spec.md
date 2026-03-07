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

### Requirement: DELETE /api/tastings/<id> deletes a tasting
The system SHALL provide a `DELETE /api/tastings/<id>` route that deletes a single tasting by ID.

- On success, SHALL return HTTP 200 with `{"status": "deleted"}`.
- If the tasting ID does not exist, SHALL return HTTP 404.

#### Scenario: Delete an existing tasting
- **WHEN** a DELETE to `/api/tastings/5` is made and tasting 5 exists
- **THEN** the tasting SHALL be removed from the database and the response SHALL be HTTP 200

#### Scenario: Delete a non-existent tasting
- **WHEN** a DELETE to `/api/tastings/999` is made and no tasting with that ID exists
- **THEN** the response SHALL be HTTP 404

### Requirement: DELETE /api/coffees/<id> cascade-deletes tastings
The existing `DELETE /api/coffees/<id>` route SHALL delete all tastings associated with the coffee before deleting the coffee itself. Both operations SHALL occur in a single transaction.

#### Scenario: Delete a coffee with tastings
- **WHEN** a DELETE to `/api/coffees/1` is made and coffee 1 has 3 tastings
- **THEN** all 3 tastings SHALL be deleted and then the coffee SHALL be deleted

#### Scenario: Delete a coffee with no tastings
- **WHEN** a DELETE to `/api/coffees/2` is made and coffee 2 has no tastings
- **THEN** the coffee SHALL be deleted normally
