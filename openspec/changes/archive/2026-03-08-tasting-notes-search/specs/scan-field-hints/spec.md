## MODIFIED Requirements

### Requirement: Vision model upgrade
The system SHALL use `claude-sonnet-4-6` for both image-based extraction (`extract_coffee_details`) and text-based extraction (`extract_coffee_from_text`). The tasting_notes instruction in both prompts SHALL request a comma-separated list of individual notes rather than raw text with arbitrary separators.

#### Scenario: Image scan uses upgraded model
- **WHEN** an image is sent to `extract_coffee_details()`
- **THEN** the Claude API call SHALL use model `claude-sonnet-4-6`

#### Scenario: Text scan uses upgraded model
- **WHEN** text is sent to `extract_coffee_from_text()`
- **THEN** the Claude API call SHALL use model `claude-sonnet-4-6`

#### Scenario: Image scan prompt requests comma-separated tasting notes
- **WHEN** an image is sent to `extract_coffee_details()`
- **THEN** the prompt SHALL instruct Claude to return tasting_notes as a comma-separated list

#### Scenario: Text scan prompt requests comma-separated tasting notes
- **WHEN** text is sent to `extract_coffee_from_text()`
- **THEN** the prompt SHALL instruct Claude to return tasting_notes as a comma-separated list
