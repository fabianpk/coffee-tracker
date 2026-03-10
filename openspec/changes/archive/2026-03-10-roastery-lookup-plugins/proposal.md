## Why

The current roastery lookup system uses Claude Haiku to extract coffee details from Shopify product page HTML, which is unreliable — LLM extraction produces inconsistent results across different page layouts and languages. Replacing this with deterministic, platform-specific parsers (plugins) that extract structured data directly from known page formats will make lookups faster, cheaper, and more predictable.

## What Changes

- **BREAKING**: Remove LLM-based extraction from the Shopify provider — replace with deterministic HTML/JSON parsing
- Refactor lookup providers into a cleaner plugin architecture with a `CoffeeSearcher` base abstraction
- Each plugin handles a specific e-commerce platform (Shopify, WooCommerce) with deterministic extraction
- All plugins return a uniform result dict mapped to CoffeeBean fields
- Remove the `anthropic` dependency from the lookup module entirely
- Keep the same three roasters (Gringo/WooCommerce, Morgon/Shopify, Kafferäven/Shopify) as initial plugins
- No frontend changes — the existing lookup button and fill-empty-fields behavior stays the same
- No API contract changes — `/api/lookup` and `/api/lookup/available` endpoints keep the same request/response format

## Capabilities

### New Capabilities

_(none — this is a refactor of the existing capability)_

### Modified Capabilities

- `roastery-lookup`: Shopify provider switches from LLM extraction to deterministic HTML parsing; internal architecture changes to a `CoffeeSearcher` base class, but external API behavior is unchanged

## Impact

- **`lookup.py`**: Full rewrite of `ShopifyProvider` extraction logic; refactor class hierarchy to use `CoffeeSearcher` base class
- **`app.py`**: No changes (endpoints and imports stay the same)
- **`templates/index.html`**: No changes
- **Dependencies**: The lookup module no longer needs the `anthropic` SDK; no new dependencies added
- **Environment**: `ANTHROPIC_API_KEY_FOR_LOOKUP` is still needed for scan but no longer used by lookup
