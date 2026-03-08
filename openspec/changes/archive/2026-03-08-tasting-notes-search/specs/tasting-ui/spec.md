## MODIFIED Requirements

### Requirement: Conduct Tasting modal
Clicking **Conduct Tasting** SHALL open a modal that allows the user to record a tasting for an existing coffee.

The modal SHALL contain:
- A dropdown/select listing all coffees in the database
- A brew type selector with at least: **Espresso**, **Brew**
- A dosage dropdown/select with values from 10.0gr to 20.0gr in 0.1gr increments
- A score picker (1–5)
- A tasting notes input labeled "Tasting Notes" with placeholder "e.g. Chocolate, Berry, Citrus" for comma-separated flavor notes
- A comments textarea labeled "General Comments"
- A **Save Tasting** button and a **Cancel** button

#### Scenario: Save a tasting with tasting notes
- **WHEN** the user fills in tasting notes "Chocolate, Berry" and clicks "Save Tasting"
- **THEN** the tasting SHALL be posted to `POST /api/tastings` with `tasting_notes: "Chocolate, Berry"`

### Requirement: Tasting history per coffee card
Each tasting entry SHALL show: brew type, dosage, score, tasting notes (as tags), comments, date, and a **delete** button.

#### Scenario: Tasting entry displays tasting notes as tags
- **WHEN** a tasting history entry has `tasting_notes: "Chocolate, Berry"`
- **THEN** the entry SHALL display "Chocolate" and "Berry" as individual tag elements
