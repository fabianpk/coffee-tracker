## Why

WooCommerce lookup returns wrong products. Searching "Purple Pacamara" on Gringo Nordic returns a Sumatra coffee (wrong country, wrong price) instead of the correct El Salvador Purple Pacamara. Root cause: `_LinkExtractor` captures all `/product/` links on the page (footer, sidebar, related products) rather than just search result entries, and there's no minimum similarity threshold so garbage matches (0.28 ratio) are accepted.

## What Changes

- Fix `_LinkExtractor` to only capture product links from the WooCommerce search results section (look for `.woocommerce-loop-product__link` or equivalent WooCommerce-specific product card markup)
- Add a minimum similarity threshold (~0.4) to `WooCommerceSearcher.search()` so low-confidence matches are rejected rather than returning wrong data
- Verify the fix works against the Gringo Nordic site with "Purple Pacamara" query

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `roastery-lookup`: WooCommerce search result extraction is more precise and rejects low-confidence matches

## Impact

- **`lookup.py`**: Fix `_LinkExtractor` and add similarity threshold in `WooCommerceSearcher.search()`
- No API, frontend, or dependency changes
