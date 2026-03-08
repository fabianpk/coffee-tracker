## Why

After removing `other` from the `CoffeeBean` model, the scan endpoint's "Other (from scan)" field in the review form is always empty. Claude still returns `other` in its JSON response, but `CoffeeBean.from_scan()` silently drops unknown keys. The raw `other` value needs to be passed through to the frontend as ephemeral scan reference.

## What Changes

- Preserve the raw `other` value from Claude's response before `CoffeeBean.from_scan()` drops it
- Inject it back into the scan endpoint's response alongside `matched_roaster` and `qr_url`

## Capabilities

### New Capabilities

### Modified Capabilities
- `scan-field-hints`: Fix the ephemeral `other` passthrough in the scan endpoint

## Impact

- **`app.py`**: One-line change in the `/api/scan` route to preserve and re-inject `details.get("other")`
