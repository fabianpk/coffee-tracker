## MODIFIED Requirements

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
