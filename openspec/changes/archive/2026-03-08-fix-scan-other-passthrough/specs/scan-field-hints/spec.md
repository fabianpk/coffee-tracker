## MODIFIED Requirements

### Requirement: Other field is ephemeral scan output
The scan review form SHALL display the "Other (from scan)" field as a read-only textarea for reference during review. The `other` field is purely ephemeral — it SHALL NOT be included in any save payload, SHALL NOT exist in the `CoffeeBean` model, and SHALL NOT have a column in the database. The `/api/scan` endpoint SHALL preserve the raw `other` value from Claude's response before `CoffeeBean.from_scan()` conversion and inject it into the response JSON alongside other transient metadata (`matched_roaster`, `qr_url`).

#### Scenario: Other field shown during review but not saved
- **WHEN** the user scans a coffee bag and the scan returns an `other` value
- **THEN** the review form SHALL display the value in a read-only textarea labeled "Other (from scan)"
- **AND** when the user clicks Save, the `other` field SHALL NOT be included in the POST request to `/api/coffees`

#### Scenario: Other removed from CoffeeBean model
- **WHEN** `CoffeeBean` is defined in `models.py`
- **THEN** it SHALL NOT have an `other` property

#### Scenario: Other column removed from database
- **WHEN** `init_db()` creates or migrates the `coffees` table
- **THEN** the table SHALL NOT include an `other` column

#### Scenario: Other preserved through scan endpoint
- **WHEN** Claude's scan response includes an `other` value
- **THEN** the `/api/scan` endpoint SHALL capture `details.get("other")` before calling `CoffeeBean.from_scan(details)`
- **AND** inject the captured value into the response dict after `coffee.to_dict()`

#### Scenario: Other absent from scan response
- **WHEN** Claude's scan response does not include an `other` key
- **THEN** the `/api/scan` endpoint SHALL not inject `other` into the response (or inject `None`)

#### Scenario: Review form notes placeholder
- **WHEN** the scan review form is displayed
- **THEN** the comments textarea SHALL display "General comments" as placeholder text
