## 1. Lookup Module Foundation

- [x] 1.1 Create `lookup.py` with provider registry (`PROVIDERS` dict), `lookup_coffee(roaster, coffee_name)` function, and `has_provider(roaster)` function. Roaster matching uses case-insensitive substring comparison.

## 2. Shopify Provider

- [x] 2.1 Implement `ShopifyProvider` class with `base_url` config. Search via predictive search API (`/search/suggest?q={query}&resources[type]=product`), select best matching product handle.
- [x] 2.2 Fetch product data from `/products/{handle}.json`. Extract `price` and `weight` from variant data, `name` from title.
- [x] 2.3 Send `body_html` (stripped of HTML tags) to Claude Haiku (claude-haiku-4-5-20251001) to extract coffee-specific fields (`country_grown`, `bean_type`, `process`, `tasting_notes`, etc.). Keep values in Swedish.

## 3. WooCommerce Provider

- [x] 3.1 Implement `WooCommerceProvider` class with `base_url` and `field_map` config. Search via `/?s={query}&post_type=product`, parse HTML for product URLs, select best match.
- [x] 3.2 Fetch product page, extract JSON-LD `application/ld+json` script tags, parse Product entity's `additionalProperty` array, map fields via `field_map`. Extract name (cleaned of roastery suffix), weight, and price from main Product object.

## 4. Provider Configuration

- [x] 4.1 Register three providers: `"gringo"` → WooCommerceProvider for gringonordic.se (with Swedish field_map: land→country_grown, art-varietet→bean_type, processmetod→process), `"morgon"` → ShopifyProvider for morgoncoffeeroasters.com, `"kafferäven"` → ShopifyProvider for kafferaven.se

## 5. API Endpoints

- [x] 5.1 Add `POST /api/lookup` route in `app.py` — accepts `{ roaster, coffee_name }`, calls `lookup_coffee()`, returns extracted fields or error (400/404)
- [x] 5.2 Add `GET /api/lookup/available` route in `app.py` — accepts `roaster` query param, returns `{ available: bool }`

## 6. Frontend Integration

- [x] 6.1 Add lookup button to the review form, visible when roaster field matches a provider (check via `/api/lookup/available` on roaster field change, debounced)
- [x] 6.2 Implement lookup button click handler: call `POST /api/lookup`, show loading state, fill empty form fields with results, show error on failure
- [x] 6.3 Ensure lookup works in both scan review and manual-add review flows
