## MODIFIED Requirements

### Requirement: Tasting history per coffee card
Each coffee card SHALL include a collapsible section that shows the tasting history for that coffee, fetched from `GET /api/tastings?coffee_id=<id>`.

Each tasting entry SHALL show: brew type, dosage, score, notes, date, and a **delete** button.

Clicking the delete button SHALL confirm with the user, then call `DELETE /api/tastings/<id>`. On success, the tasting list SHALL refresh and the coffee list SHALL reload to update the average score.

#### Scenario: Delete a tasting from history
- **WHEN** the user clicks "delete" on a tasting entry and confirms
- **THEN** the tasting SHALL be deleted via the API, the tasting list SHALL refresh, and the coffee card's average score SHALL update

#### Scenario: Cancel tasting deletion
- **WHEN** the user clicks "delete" on a tasting entry and cancels the confirm dialog
- **THEN** no deletion SHALL occur

### Requirement: Coffee deletion confirm mentions tastings
The confirm dialog when deleting a coffee SHALL mention that associated tastings will also be removed (e.g. "Delete this coffee and all its tastings?").

#### Scenario: Delete coffee confirmation message
- **WHEN** the user clicks "delete" on a coffee card
- **THEN** the confirm dialog SHALL warn that tastings will also be deleted
