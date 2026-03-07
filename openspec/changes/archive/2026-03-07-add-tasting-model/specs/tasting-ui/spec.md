## ADDED Requirements

### Requirement: Two top-level action buttons
The page header SHALL contain two buttons: **Scan Coffee** (existing behaviour) and **Conduct Tasting** (new). The existing single "Scan / Add Coffee" button SHALL be replaced by these two.

#### Scenario: Both buttons visible on load
- **WHEN** the app loads
- **THEN** both "Scan Coffee" and "Conduct Tasting" buttons SHALL be visible at the top of the page

### Requirement: Conduct Tasting modal
Clicking **Conduct Tasting** SHALL open a modal that allows the user to record a tasting for an existing coffee.

The modal SHALL contain:
- A dropdown/select listing all coffees in the database (label: roaster + name, or "Unknown" if both are null)
- A brew type selector with at least the options: **Espresso**, **Brew** — rendered as buttons or a select
- A dosage dropdown/select with values from 10.0gr to 20.0gr in 0.1gr increments
- A score picker (1–5 stars or buttons, same visual pattern as existing score inputs)
- A notes textarea
- A **Save Tasting** button and a **Cancel** button

#### Scenario: Open tasting modal
- **WHEN** the user clicks "Conduct Tasting"
- **THEN** the tasting modal SHALL appear with the coffee dropdown populated from the database

#### Scenario: Save a tasting
- **WHEN** the user selects a coffee, picks a brew type, enters a score, and clicks "Save Tasting"
- **THEN** the tasting SHALL be posted to `POST /api/tastings` and the modal SHALL close on success

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

Each tasting entry SHALL show: brew type, dosage, score, notes, and date.

#### Scenario: Expand tasting history
- **WHEN** the user clicks to expand a coffee card's tasting section
- **THEN** all tastings for that coffee SHALL be displayed, most recent first

#### Scenario: No tastings yet
- **WHEN** the user expands a coffee with no tastings
- **THEN** the section SHALL show a message such as "No tastings yet"
