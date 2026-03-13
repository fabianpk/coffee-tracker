## Context

The coffee tracker has a plugin-based roastery lookup system (`CoffeeSearcher` ABC) with Shopify and WooCommerce providers. Currently, if a roastery has no provider or the coffee is delisted from the roastery's site, the lookup simply fails. Baristashopen.se is a Swedish coffee retailer that stocks products from many roasteries, making it a useful fallback source. It runs on the Textalk/Abicart platform, which exposes a public JSON-RPC API at `/backend/jsonrpc/v1/`.

## Goals / Non-Goals

**Goals:**
- Add a `TextalkSearcher` provider that uses the Abicart JSON-RPC API (`Article.list` with search filters) to find and extract coffee product data from Textalk-powered shops.
- Implement a fallback chain in `lookup_coffee()`: try the primary roastery provider first, then try baristashopen.se if the primary returns no results or no provider exists.
- Return source metadata (`"source": "roastery"` or `"source": "baristashopen"`) in the API response so the frontend can indicate where data came from.

**Non-Goals:**
- Supporting arbitrary Textalk shops as roastery providers (only baristashopen.se for now).
- Changing the existing non-destructive field-fill behavior in the frontend.
- Adding user-configurable fallback shop URLs.

## Decisions

### 1. Use Abicart JSON-RPC API directly (not HTML scraping)

Baristashopen.se renders search results client-side via JavaScript, making HTML scraping impractical. The Textalk/Abicart platform provides a public JSON-RPC 2.0 API at `https://www.baristashopen.se/backend/jsonrpc/v1/`.

**Search**: `Article.list` with `filters.search` accepts a `term` and `relevance` threshold. We'll request `uid`, `name`, `url`, `price`, `weight`, `description`, and `introductionText` fields.

**Product details**: `Article.get` can fetch full product data by UID, including structured fields like `description` (which typically contains origin, process, etc. for coffee products).

**Alternative considered**: Scraping with a headless browser — rejected as too heavy a dependency for a simple lookup.

### 2. TextalkSearcher implements the existing CoffeeSearcher ABC

The new provider fits naturally into the existing plugin pattern:
- `search(coffee_name)` → calls `Article.list` with search filter, returns the best-matching article UID
- `fetch_product(uid)` → calls `Article.get` with the UID, returns the article dict
- `extract(article)` → parses name, price, weight from structured fields; extracts coffee-specific fields from description text using the existing `_extract_labeled_fields()` helper

This requires no changes to the base class.

### 3. Fallback chain in lookup_coffee()

Modify `lookup_coffee()` to accept an optional `fallback=True` parameter (default True). The flow becomes:

1. Try `_match_provider(roaster)` → if found, call `provider.lookup(coffee_name)`
2. If step 1 returns None (no provider or coffee not found), and fallback is enabled, try `FALLBACK_PROVIDER.lookup(coffee_name)` (searching by coffee name only)
3. Return result with a `_source` key indicating origin

The `/api/lookup` endpoint will include the `source` field in the JSON response.

### 4. Frontend indicates fallback source

When lookup results include `"source": "baristashopen"`, show a subtle note below the lookup button (e.g., "Found on Baristashopen.se") so the user knows the data didn't come from the roastery directly. This is informational only — no workflow changes.

### 5. Lookup button always available

Since baristashopen.se acts as a universal fallback, the lookup button should always be shown when both roaster and coffee name are filled in — not just for roasters with dedicated providers. Update `GET /api/lookup/available` to always return `true` when a roaster is provided (since the fallback is always available), or alternatively, just show the button unconditionally in the frontend when roaster is non-empty.

## Risks / Trade-offs

- **Textalk API stability**: The JSON-RPC API is public and documented but could change. → Mitigation: The `TextalkSearcher` is isolated; changes only affect one class.
- **Search relevance**: Baristashopen may stock thousands of products; search relevance depends on their `Article.list` search quality. → Mitigation: Use `SequenceMatcher` to verify the best result actually matches the query, with a similarity threshold.
- **Multilingual field labels**: Baristashopen product descriptions are likely in Swedish. → Mitigation: The existing `FIELD_LABELS` dict already includes Swedish labels.
- **Rate limiting**: No known rate limits on the Textalk API, but we should still be respectful. → Mitigation: Single request per lookup, no bulk operations.
