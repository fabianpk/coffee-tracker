## Context

The `/api/scan` endpoint sends a coffee bag photo to Claude and receives structured JSON including a `roastery` field. This raw name is passed through `CoffeeBean.from_scan()` and returned to the frontend review form. Claude sometimes returns variations of the same roaster name across scans. The database already accumulates distinct roaster names over time, providing a ground-truth list to match against.

## Goals / Non-Goals

**Goals:**
- Match a scanned roastery name against known roasters in the database
- Replace the raw scan name with the matched name when confidence is high enough
- Keep the original scan name available so the user can see what was detected
- Zero new dependencies — use Python stdlib only

**Non-Goals:**
- Building a separate roastery table or normalized roastery model
- Allowing the user to manage/merge roasteries manually
- Matching other fields (origin, process, etc.)

## Decisions

### 1. Use `difflib.SequenceMatcher` for fuzzy matching

**Why**: It's in the stdlib, handles substring similarity well, and is fast for small lists (< 1000 roasters). Alternatives considered:
- **Levenshtein distance** (`python-Levenshtein`): would add a dependency for marginal benefit at this scale
- **Embedding-based similarity**: overkill for matching short business names

**Approach**: Compare the scanned name (lowercased, stripped) against each known roaster name using `SequenceMatcher.ratio()`. Also check if one is a substring of the other (handles "Gringo" matching "Gringo Nordic Roasters").

### 2. Matching threshold of 0.7 with substring override

- `SequenceMatcher.ratio() >= 0.7` → match
- If the scanned name is a substring of a known name (or vice versa), and the shorter string is at least 4 characters → match regardless of ratio
- If multiple matches, pick the one with the highest ratio
- Below threshold → use the raw scanned name as-is

### 3. Matching runs server-side in the scan endpoint

The match happens in `POST /api/scan` after `extract_coffee_details()` returns, before sending the response. This keeps it invisible to the frontend except for the result.

The response gains a `matched_roaster` field:
- If a match was found: `matched_roaster` = the known roaster name, `roaster` = same (overwritten)
- If no match: `matched_roaster` = `null`, `roaster` = raw scan value

### 4. No model or schema changes

The `roaster` field on `CoffeeBean` is unchanged. Matching is purely a post-processing step in the scan route. No database migration needed.

## Risks / Trade-offs

- **False positives** — two genuinely different roasters with similar names could be merged. → Mitigated by the 0.7 threshold and the user always reviewing before saving.
- **Substring matching too aggressive** — a short roaster name like "Koppi" could match "Koppi Coffee Roasters" which is correct, but also hypothetically "Koppigen Kaffee" which is not. → Mitigated by requiring at least 4 characters and combining with ratio check.
- **Performance at scale** — `O(n)` comparison against all known roasters on every scan. At typical personal-collection sizes (< 100 roasters), this is negligible.
