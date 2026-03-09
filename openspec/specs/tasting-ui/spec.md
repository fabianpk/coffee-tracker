### Requirement: Two top-level action buttons
The page header SHALL contain two buttons: **Scan Coffee** (existing behaviour) and **Conduct Tasting** (new). The existing single "Scan / Add Coffee" button SHALL be replaced by these two.

#### Scenario: Both buttons visible on load
- **WHEN** the app loads
- **THEN** both "Scan Coffee" and "Conduct Tasting" buttons SHALL be visible at the top of the page

### Requirement: Conduct Tasting modal
Clicking **Conduct Tasting** SHALL open a modal that allows the user to record a tasting for an existing coffee.

The modal SHALL contain:
- A dropdown/select listing all coffees in the database (label: roaster + name, or "Unknown" if both are null)
- A brew type selector with the options: **Espresso**, **Brew**, **Metal Brew**, **Cappuccino** — rendered as buttons, each displaying an emoji and label from the brew type registry
- A dosage dropdown/select with values from 10.0gr to 20.0gr in 0.1gr increments
- A score picker (1-5 stars or buttons, same visual pattern as existing score inputs)
- A tasting notes input labeled "Tasting Notes" with placeholder "e.g. Chocolate, Berry, Citrus" for comma-separated flavor notes
- A comments textarea labeled "General Comments"
- A **Save Tasting** button and a **Cancel** button

#### Scenario: Open tasting modal
- **WHEN** the user clicks "Conduct Tasting"
- **THEN** the tasting modal SHALL appear with four brew type buttons showing emojis and the coffee dropdown populated from the database

#### Scenario: Save a tasting with tasting notes
- **WHEN** the user fills in tasting notes "Chocolate, Berry" and clicks "Save Tasting"
- **THEN** the tasting SHALL be posted to `POST /api/tastings` with `tasting_notes: "Chocolate, Berry"` and `comments`

#### Scenario: Cancel tasting
- **WHEN** the user clicks "Cancel" in the tasting modal
- **THEN** the modal SHALL close without saving

### Requirement: Average score shown on coffee card
Each coffee card in the list SHALL display the `average_score` returned by the API. If `average_score` is `null`, the card SHALL show "–" in its place. The individual `brew_score` and `espresso_score` fields SHALL be removed from the card display.

#### Scenario: Coffee with tastings shows average
- **WHEN** a coffee card renders and the coffee has `average_score: 4.5`
- **THEN** the card SHALL display "4.5" (or equivalent star representation) labelled as the average score

#### Scenario: Coffee with no tastings shows placeholder
- **WHEN** a coffee card renders and the coffee has `average_score: null`
- **THEN** the card SHALL display "–" where the score would appear

### Requirement: Tasting history per coffee card
Each coffee card SHALL include a collapsible section that shows the tasting history for that coffee, fetched from `GET /api/tastings?coffee_id=<id>`.

Each tasting entry SHALL show: brew type, dosage, score, tasting notes (as tags), comments, date, and a **delete** button.

Clicking the delete button SHALL confirm with the user, then call `DELETE /api/tastings/<id>`. On success, the tasting list SHALL refresh and the coffee list SHALL reload to update the average score.

#### Scenario: Tasting entry displays tasting notes as tags
- **WHEN** a tasting history entry has `tasting_notes: "Chocolate, Berry"`
- **THEN** the entry SHALL display "Chocolate" and "Berry" as individual tag elements

#### Scenario: Tasting entry displays comments
- **WHEN** a tasting history entry is rendered with a comments value
- **THEN** the entry SHALL display the comments text

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
