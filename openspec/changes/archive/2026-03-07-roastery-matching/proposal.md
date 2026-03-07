## Why

When scanning a new coffee bag, Claude often returns slightly different roastery names for the same roaster (e.g. "Gringo" vs "Gringo Nordic Roasters"). This creates duplicate roasteries in the database and makes it harder to browse the collection. Since most new scans are from roasteries the user has already encountered, matching the scanned roastery name against known ones can eliminate these inconsistencies automatically.

## What Changes

- After a scan returns a roastery name, the system looks up all distinct roaster names already in the database
- It performs a fuzzy match (case-insensitive, substring/similarity) to find the best match among known roasteries
- If a match is found above a confidence threshold, the scan result uses the existing roaster name instead of the raw scan output
- The matched roaster name is pre-filled in the review form; the user can still override it
- No changes to the scan prompt itself — matching happens post-scan in the backend

## Capabilities

### New Capabilities

- `roastery-matching`: Post-scan logic to match a scanned roastery name against known roasters in the database and return the best match

### Modified Capabilities

- `coffee-bean-model`: The scan endpoint response includes a `matched_roaster` field alongside the raw `roaster` so the frontend can show which known roaster was matched

## Impact

- `app.py`: New matching function; updated `/api/scan` route to run matching after extraction
- `models.py`: Minor — `from_scan()` or `to_dict()` may carry the matched name
- `templates/index.html`: Review form pre-fills with the matched roaster name (existing behaviour, just more accurate data)
- No new dependencies — matching uses Python stdlib (e.g. `difflib.SequenceMatcher`)
