## MODIFIED Requirements

### Requirement: Conduct Tasting modal
Clicking **Conduct Tasting** SHALL open a modal that allows the user to record a tasting for an existing coffee.

The modal SHALL contain:
- A dropdown/select listing all coffees in the database (label: roaster + name, or "Unknown" if both are null)
- A brew type selector with at least the options: **Espresso**, **Brew** — rendered as buttons or a select
- A dosage dropdown/select with values from 10.0gr to 20.0gr in 0.1gr increments
- A score picker (1–5 stars or buttons, same visual pattern as existing score inputs)
- A comments textarea labeled "General Comments"
- A **Save Tasting** button and a **Cancel** button

#### Scenario: Save a tasting
- **WHEN** the user selects a coffee, picks a brew type, enters a score, and clicks "Save Tasting"
- **THEN** the tasting SHALL be posted to `POST /api/tastings` with `comments` (not `notes`) and the modal SHALL close on success

### Requirement: Tasting history per coffee card
Each coffee card SHALL include a collapsible section that shows the tasting history for that coffee, fetched from `GET /api/tastings?coffee_id=<id>`.

Each tasting entry SHALL show: brew type, dosage, score, comments, date, and a **delete** button.

#### Scenario: Tasting entry displays comments
- **WHEN** a tasting history entry is rendered with a comments value
- **THEN** the entry SHALL display the comments text
