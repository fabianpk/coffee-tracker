## Why

The Claude vision prompt currently has minimal guidance about expected field values (e.g., process types, bean varieties, origin countries). The user has domain knowledge about what values are common for their collection, and providing these as hints would improve scan accuracy. Currently, updating hints requires editing Python string literals in `app.py`, which is error-prone and not user-friendly.

## What Changes

- Add a `scan_hints.md` markdown file at the project root where the user can document expected/common values for each scannable field (process, bean_type, country_grown, roast_level, etc.)
- Load `scan_hints.md` at scan time and append its content to the Claude vision prompt as additional context
- The hints file is optional — if missing or empty, scanning works exactly as before

## Capabilities

### New Capabilities
- `scan-field-hints`: User-editable markdown hints file loaded into Claude scan prompts

### Modified Capabilities

## Impact

- **`scan_hints.md`** (new) — User-editable markdown file with field value hints
- **`app.py`** — Both `extract_coffee_details()` and `extract_coffee_from_text()` load and append hints to the prompt
