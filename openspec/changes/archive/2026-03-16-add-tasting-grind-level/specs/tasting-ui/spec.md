## MODIFIED Requirements

### Requirement: Conduct Tasting modal
Clicking **Conduct Tasting** SHALL open a modal that allows the user to record a tasting for an existing coffee.

The modal SHALL contain:
- A dropdown/select listing all coffees in the database (label: roaster + name, or "Unknown" if both are null)
- A brew type selector with the options: **Espresso**, **Brew**, **Metal Brew**, **Cappuccino** — rendered as buttons, each displaying an emoji and label from the brew type registry
- A dosage dropdown/select with values from 10.0gr to 20.0gr in 0.1gr increments
- A grind-level dropdown/select with values from 3.0 to 22.0 in 0.2 increments, using the same spinning-wheel style as dosage
- A score picker (1-5 stars or buttons, same visual pattern as existing score inputs)
- A tasting notes input labeled "Tasting Notes" with placeholder "e.g. Chocolate, Berry, Citrus" for comma-separated flavor notes
- A comments textarea labeled "General Comments"
- A **Save Tasting** button and a **Cancel** button

#### Scenario: Open tasting modal
- **WHEN** the user clicks "Conduct Tasting"
- **THEN** the tasting modal SHALL appear with four brew type buttons showing emojis, the coffee dropdown populated from the database, and the grind-level selector

#### Scenario: Save a tasting with grind level
- **WHEN** the user fills in grind level 6.4 and clicks "Save Tasting"
- **THEN** the tasting SHALL be posted to `POST /api/tastings` with `grind_level: 6.4`

#### Scenario: Cancel tasting
- **WHEN** the user clicks "Cancel" in the tasting modal
- **THEN** the modal SHALL close without saving

### Requirement: Tasting history per coffee card
Each coffee card SHALL include a collapsible section that shows the tasting history for that coffee, fetched from `GET /api/tastings?coffee_id=<id>`.

Each tasting entry SHALL show: brew type, dosage, grind level, score, tasting notes (as tags), comments, date, and a **delete** button.

Clicking the delete button SHALL confirm with the user, then call `DELETE /api/tastings/<id>`. On success, the tasting list SHALL refresh and the coffee list SHALL reload to update the average score.

#### Scenario: Tasting entry displays grind level
- **WHEN** a tasting history entry has grind_level 6.4
- **THEN** the entry SHALL display the grind level (e.g., "grind 6.4")

#### Scenario: Tasting entry without grind level
- **WHEN** a tasting history entry has grind_level null
- **THEN** the entry SHALL not display any grind level text

#### Scenario: Delete a tasting from history
- **WHEN** the user clicks "delete" on a tasting entry and confirms
- **THEN** the tasting SHALL be deleted via the API, the tasting list SHALL refresh, and the coffee card's average score SHALL update
