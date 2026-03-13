## 1. TextalkSearcher Provider

- [x] 1.1 Add `_fetch_jsonrpc()` helper function in `lookup.py` that sends JSON-RPC 2.0 POST requests and returns the `result` field from the response
- [x] 1.2 Implement `TextalkSearcher` class inheriting from `CoffeeSearcher` with `base_url` config and API endpoint construction
- [x] 1.3 Implement `TextalkSearcher.search()` — call `Article.list` with search filter (`term` + `relevance`), request `uid` and `name` fields, select best match via `SequenceMatcher` with 0.3 threshold
- [x] 1.4 Implement `TextalkSearcher.fetch_product()` — call `Article.get` with UID, request `name`, `price`, `weight`, `description`, `introductionText`, `url` fields
- [x] 1.5 Implement `TextalkSearcher.extract()` — extract `name` (Swedish locale), `price`, `weight` from structured fields; parse `description`/`introductionText` with `_extract_labeled_fields()` for coffee-specific fields

## 2. Fallback Lookup Chain

- [x] 2.1 Register baristashopen.se `TextalkSearcher` instance as `FALLBACK_PROVIDER` in `lookup.py`
- [x] 2.2 Modify `lookup_coffee()` to implement fallback chain: try primary provider first, then fallback if primary returns None or no provider exists. Add `_source` key to result dict (`"roastery"` or `"baristashopen"`)
- [x] 2.3 Update `has_provider()` to always return True when a roaster name is provided (since fallback is always available)

## 3. API Updates

- [x] 3.1 Update `POST /api/lookup` in `app.py` to pass through the `source` field from the lookup result and remove the `_source` internal key before returning
- [x] 3.2 Remove the early 404 return for missing providers in `/api/lookup` (since fallback handles unknown roasters now)

## 4. Frontend Updates

- [x] 4.1 Remove the `/api/lookup/available` check — always show the lookup button when the roaster field is non-empty
- [x] 4.2 After a successful lookup, check the `source` field in the response and display a note like "Found on Baristashopen.se" near the lookup button when `source === "baristashopen"`
