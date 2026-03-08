## Context

The coffee tracker scans coffee bag photos using Claude Haiku 4.5 vision and presents a review form before saving. Currently:
- The "Your Notes" field uses placeholder "How was it?" which implies tasting feedback, but it's meant for general notes
- The "Other" field from scans is saved to the database, but it contains miscellaneous scan output (markdown) that's only useful as reference during review
- Text recognition quality from Haiku 4.5 is poor for reading coffee bag labels

## Goals / Non-Goals

**Goals:**
- Clarify the notes field's purpose by changing placeholder text to "Other notes"
- Make the scan "Other" field display-only — shown during review but not persisted
- Improve text recognition by switching to a more capable vision model

**Non-Goals:**
- Changing the tasting notes field or tasting workflow
- Adding new fields or restructuring the data model

## Decisions

### 1. Vision model: Switch to Claude Sonnet 4.6

**Choice**: Replace `claude-haiku-4-5-20251001` with `claude-sonnet-4-6` in both `extract_coffee_details()` and `extract_coffee_from_text()`.

**Rationale**: Sonnet 4.6 has significantly better vision/OCR capabilities while remaining cost-efficient. Opus would be overkill for structured extraction from a single image.

**Alternative considered**: Keeping Haiku and tuning the prompt — rejected because the issue is model capability, not prompt quality.

### 2. "Other" field: Stop sending in save payload, keep in DB schema

**Choice**: Remove `other` from the JavaScript save payload in both the review form and detail/edit panel. Remove the `other` column in the database and `CoffeeBean` model since the project is not live so no backward compatibility is needed.

**Rationale**: Project is not live yet, so existing data is no issue. Even wiping the database is no problem at this stage of the project. New entries won't have it populated.

### 3. Review form "Other (from scan)": Keep as ephemeral reference

**Choice**: The scan review form already shows "Other (from scan)" as readonly. Keep it visible during review but exclude from the save payload.

## Risks / Trade-offs

- **[Cost increase]** Sonnet is more expensive per call than Haiku → Acceptable for a personal tool with low scan volume
- **[Existing `other` data]** Old entries still have `other` values that display in the list/detail views → If this is an issue, just delete them.
- **[Model ID stability]** `claude-sonnet-4-6` may need updating as new models release → Same situation as current Haiku ID
