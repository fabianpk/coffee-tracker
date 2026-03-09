## Why

When adding or scanning a coffee from a known roastery, the user currently has to manually fill in details like origin, process, bean type, and tasting notes. Swedish specialty roasteries publish rich product information on their websites. Automating lookup from roastery homepages saves time and ensures accurate, complete coffee entries.

## What Changes

- Add a pluggable roastery lookup system with two provider types: Shopify (generic, one-line config per roastery) and WooCommerce (with per-site field mapping)
- Shopify provider uses the `.json` product API for structured data and Claude Haiku for extracting coffee details from description text
- WooCommerce provider parses JSON-LD structured data mechanically (no API calls)
- Ship with three providers: Gringo Nordic (WooCommerce), Morgon Coffee Roasters (Shopify), Kafferäven (Shopify)
- New `POST /api/lookup` and `GET /api/lookup/available` endpoints
- Frontend lookup button in review form (both scan and manual-add flows) that auto-fills empty fields

## Capabilities

### New Capabilities
- `roastery-lookup`: Core lookup system — provider registry, Shopify and WooCommerce provider implementations, lookup API endpoints, and frontend integration for auto-filling coffee details from roastery websites

### Modified Capabilities
_None — this adds a new capability that integrates with existing scan and manual-add flows at the UI/API level without changing their spec-level requirements._

## Impact

- **Backend**: New `lookup.py` module with provider classes. New API endpoints in `app.py`. Uses existing `urllib` and `json` — no new dependencies. Shopify lookups use Claude Haiku API calls (uses existing `ANTHROPIC_API_KEY_FOR_LOOKUP`).
- **Frontend**: New lookup button in the review form in `templates/index.html`. Auto-fill logic for form fields from lookup results.
- **External dependencies**: Network requests to roastery websites and Shopify APIs at lookup time. Haiku API calls for Shopify description extraction.
