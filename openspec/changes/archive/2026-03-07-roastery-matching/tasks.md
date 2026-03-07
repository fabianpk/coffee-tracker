## 1. Matching Logic

- [x] 1.1 Add `match_roaster(scanned_name: str, db) -> str | None` function to `app.py`: queries `SELECT DISTINCT roaster FROM coffees`, compares using `difflib.SequenceMatcher` (case-insensitive, ratio >= 0.7 or substring with min 4 chars), returns best match or `None`
- [x] 1.2 Update `POST /api/scan` route: after `extract_coffee_details()`, call `match_roaster()` and overwrite `roaster` in the result if matched; add `matched_roaster` to the response dict

## 2. Model Update

- [x] 2.1 Update `CoffeeBean.to_dict()` to include `matched_roaster` (default `None`); no new dataclass field needed — pass it through scan response only
