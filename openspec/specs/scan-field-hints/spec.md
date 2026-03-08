### Requirement: Scan hints file
The system SHALL support an optional `scan_hints.md` file in the project root directory. When present and non-empty, its contents SHALL be appended to the Claude vision prompt as additional context for field extraction. The file SHALL be read on each scan request so edits take effect without restarting the service.

#### Scenario: Hints file exists and is non-empty
- **WHEN** a scan is performed and `scan_hints.md` exists with content
- **THEN** the content SHALL be appended to the Claude prompt after the existing field instructions

#### Scenario: Hints file is missing
- **WHEN** a scan is performed and `scan_hints.md` does not exist
- **THEN** the scan SHALL proceed normally with the default prompt, with no error

#### Scenario: Hints file is empty
- **WHEN** a scan is performed and `scan_hints.md` exists but is empty
- **THEN** the scan SHALL proceed normally with the default prompt

#### Scenario: Hints apply to both image and text scan
- **WHEN** hints are loaded
- **THEN** they SHALL be appended to both `extract_coffee_details()` (image scan) and `extract_coffee_from_text()` (text/URL scan) prompts

#### Scenario: Hints file content truncated if too long
- **WHEN** `scan_hints.md` exceeds 2000 characters
- **THEN** the content SHALL be truncated to 2000 characters before appending to the prompt

### Requirement: Scan hints example file
The system SHALL include a `scan_hints.example.md` file demonstrating the expected format with common coffee field values (process types, bean varieties, origin countries, roast levels). This file serves as a starting template for users.

#### Scenario: Example file provides starter content
- **WHEN** a user wants to create their own hints
- **THEN** they can copy `scan_hints.example.md` to `scan_hints.md` and customize it

### Requirement: Scan hints file gitignored
The `scan_hints.md` file SHALL be listed in `.gitignore` so each user can maintain their own hints without version control conflicts.

#### Scenario: Gitignore includes scan_hints.md
- **WHEN** `.gitignore` is checked
- **THEN** it SHALL contain an entry for `scan_hints.md`

### Requirement: Other field is ephemeral scan output
The scan review form SHALL display the "Other (from scan)" field as a read-only textarea for reference during review. The `other` field is purely ephemeral — it SHALL NOT be included in any save payload, SHALL NOT exist in the `CoffeeBean` model, and SHALL NOT have a column in the database.

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

#### Scenario: Review form notes placeholder
- **WHEN** the scan review form is displayed
- **THEN** the notes textarea SHALL display "Other notes" as placeholder text

### Requirement: Vision model upgrade
The system SHALL use `claude-sonnet-4-6` (instead of `claude-haiku-4-5-20251001`) for both image-based extraction (`extract_coffee_details`) and text-based extraction (`extract_coffee_from_text`) to improve text recognition accuracy.

#### Scenario: Image scan uses upgraded model
- **WHEN** an image is sent to `extract_coffee_details()`
- **THEN** the Claude API call SHALL use model `claude-sonnet-4-6`

#### Scenario: Text scan uses upgraded model
- **WHEN** text is sent to `extract_coffee_from_text()`
- **THEN** the Claude API call SHALL use model `claude-sonnet-4-6`
