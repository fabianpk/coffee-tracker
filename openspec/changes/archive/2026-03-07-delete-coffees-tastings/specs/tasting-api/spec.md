## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: DELETE /api/coffees/<id> cascade-deletes tastings
The existing `DELETE /api/coffees/<id>` route SHALL delete all tastings associated with the coffee before deleting the coffee itself. Both operations SHALL occur in a single transaction.

#### Scenario: Delete a coffee with tastings
- **WHEN** a DELETE to `/api/coffees/1` is made and coffee 1 has 3 tastings
- **THEN** all 3 tastings SHALL be deleted and then the coffee SHALL be deleted

#### Scenario: Delete a coffee with no tastings
- **WHEN** a DELETE to `/api/coffees/2` is made and coffee 2 has no tastings
- **THEN** the coffee SHALL be deleted normally
