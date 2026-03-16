## Why

When a coffee is no longer listed on a roastery's own website (or the roastery has no lookup provider at all), there's no way to fill in product details automatically. Baristashopen.se is a Swedish coffee retailer that stocks products from many roasteries, so it can serve as a fallback source for coffee metadata when the primary roastery lookup fails or isn't available.

## What Changes

- Add a new `TextalkSearcher` provider class that queries the Abicart/Textalk JSON-RPC API (`Article.list` with search filters) used by baristashopen.se.
- Introduce a **fallback lookup** mechanism: when the primary roastery provider returns no results (or no provider exists for the roaster), automatically try baristashopen.se as a last resort.
- Update the frontend to indicate when results came from the fallback shop rather than the roastery directly.
- Expose baristashopen.se as a usable provider so it can also be triggered explicitly for roasteries without a dedicated provider.

## Capabilities

### New Capabilities
- `textalk-provider`: A new `CoffeeSearcher` implementation for Textalk/Abicart-powered shops, using their JSON-RPC API for search and product data retrieval.
- `fallback-lookup`: A fallback chain mechanism that tries the primary roastery provider first, then falls back to baristashopen.se if no result is found or no provider exists.

### Modified Capabilities

## Impact

- **`lookup.py`**: New `TextalkSearcher` class, updated `lookup_coffee()` to support fallback chain, new fallback provider registration.
- **`app.py`**: Update `/api/lookup` route to support fallback and communicate source info (primary vs fallback) in the response.
- **`templates/index.html`**: Minor frontend update to show feedback when results came from the fallback shop.
- **No new dependencies**: Uses `requests` (already available) for JSON-RPC calls over HTTP.
