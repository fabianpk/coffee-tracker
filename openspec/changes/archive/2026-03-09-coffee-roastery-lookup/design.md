## Context

Coffee Tracker lets users scan coffee bags or manually add coffees. When a roastery is identified (via scan match or user input), there's currently no way to auto-fill details from the roastery's website. Swedish specialty roasteries publish rich product information on their websites — some via structured JSON-LD (WooCommerce stores like Gringo Nordic), others via product descriptions (Shopify stores like Morgon Coffee and Kafferäven).

The existing `roastery-matching` capability already identifies known roasters from scans. This change builds on that by adding a lookup step that fetches product details from the matched roastery's website.

## Goals / Non-Goals

**Goals:**
- Fetch structured coffee details from roastery websites given a coffee name
- Support two platform types: WooCommerce (JSON-LD extraction) and Shopify (JSON API + Haiku text extraction)
- Ship with three roasteries: Gringo Nordic, Morgon Coffee Roasters, Kafferäven
- Make adding a new Shopify roastery a one-line config change
- Provide a lookup API endpoint that the frontend can call
- Integrate lookup into both scan and manual-add review flows

**Non-Goals:**
- Caching or storing lookup results (each lookup is a fresh fetch)
- Automatic lookup without user action (always user-triggered via button)
- Handling authentication-gated roastery pages
- Auto-detecting platform type for unknown roasteries

## Decisions

### 1. Two provider types: WooCommerce and Shopify

Investigation of three Swedish roasteries revealed two distinct platform patterns:

| | Gringo Nordic | Morgon Coffee | Kafferäven |
|---|---|---|---|
| Platform | WooCommerce | Shopify | Shopify |
| Structured data | Rich JSON-LD with `additionalProperty` | Minimal JSON-LD | None |
| Shopify `.json` API | N/A | Yes | Yes |
| Coffee details location | JSON-LD fields (Swedish keys) | `body_html` (semi-structured text) | `body_html` (narrative text) |

This naturally produces two provider classes rather than one-size-fits-all.

**WooCommerceProvider**: Configured with `base_url` and a `field_map` that maps site-specific JSON-LD property names to CoffeeBean fields. Extraction is purely mechanical (JSON parsing). Free — no API calls.

**ShopifyProvider**: Configured with just a `base_url`. Uses the Shopify `.json` product endpoint for structured fields (price, weight, title) and sends `body_html` to Claude Haiku to extract coffee details (origin, process, variety, tasting notes). Adding a new Shopify roastery = one line of config.

**Why two types over one**: WooCommerce has no `.json` API. Shopify has no rich JSON-LD. The extraction strategies are fundamentally different. Forcing them into one abstraction adds complexity without benefit.

### 2. Shopify: use predictive search API for product discovery

Search flow: `GET /search/suggest?q={coffee_name}&resources[type]=product` → returns JSON with matching products including handles → fetch `/products/{handle}.json`.

**Why over guessing the handle**: Coffee names are entered by users or extracted from scans — the slug format is unpredictable. The predictive search API is built into all Shopify stores and returns structured JSON.

**Why over `/search?q=`**: The suggest endpoint returns machine-readable JSON, while the search page returns HTML that would need parsing.

### 3. WooCommerce: search via `?s=` URL, then extract JSON-LD

Search flow: `GET /?s={coffee_name}&post_type=product` → parse HTML for product URLs → fetch product page → extract JSON-LD `additionalProperty` array → map via `field_map`.

**Why**: WooCommerce has no equivalent of Shopify's predictive search API. The `?s=` search parameter is the standard WooCommerce search pattern.

### 4. Claude Haiku for Shopify body_html extraction

Shopify product descriptions vary widely between roasteries — Morgon uses semi-structured `"Variety: Catuai\nProcessing: Honey"` while Kafferäven writes narrative text. Regex per-roastery would be fragile and require maintenance.

Sending the text to Claude Haiku (claude-haiku-4-5-20251001) to extract structured coffee fields handles all description formats without per-roastery customization. The prompt asks for the same fields as the scan prompt but operates on text instead of images.

**Cost**: ~$0.001 per lookup. Negligible for personal use.

**Why Haiku, not Sonnet**: Text extraction from product descriptions is straightforward — no image understanding needed. Haiku is sufficient and cheaper.

### 5. Provider registry as a dict mapping names to provider instances

```
PROVIDERS = {
    "gringo": WooCommerceProvider("gringonordic.se", field_map={...}),
    "morgon": ShopifyProvider("morgoncoffeeroasters.com"),
    "kafferäven": ShopifyProvider("kafferaven.se"),
}
```

Matching uses case-insensitive substring comparison (same logic as existing roastery-matching). Adding a new Shopify roastery is one line. Adding a WooCommerce roastery requires a field_map for that site's JSON-LD property names.

### 6. New `POST /api/lookup` endpoint

Accepts `{ "roaster": "...", "coffee_name": "..." }` and returns a dict of extracted fields (matching CoffeeBean field names) or an error. The frontend calls this from the review form.

**Why a separate endpoint** (vs. embedding in `/api/scan`): Lookup is user-triggered and independent of scanning. It works for both scanned and manually-added coffees. Keeping it separate avoids slowing down scan responses.

### 7. Use `urllib` for HTTP requests (no new dependencies)

The app already uses `urllib.request`. Use the same for search and product page fetching. Shopify `.json` responses and JSON-LD are parsed with the `json` module. HTML parsing for WooCommerce search results uses `html.parser` (already imported).

### 8. Swedish data values throughout

Most roasteries are Swedish. Extracted values (tasting notes, process names, etc.) are kept in Swedish as-is — no translation. The Haiku extraction prompt can work in Swedish.

## Risks / Trade-offs

- **[Website structure changes]** → JSON-LD and Shopify `.json` API are stable, but could change. Mitigation: providers return partial results gracefully; missing fields left empty.
- **[Shopify predictive search quality]** → May not find the right product for vague names. Mitigation: user can adjust coffee name and retry.
- **[Haiku extraction accuracy]** → May misparse unusual description formats. Mitigation: user reviews and can edit all fields before saving; only empty fields are filled.
- **[Network latency]** → Lookup requires 2-3 HTTP requests (search + product page + optional Haiku). Mitigation: frontend shows loading state; lookup is user-triggered.
- **[Shopify `.json` endpoint deprecation]** → Shopify could restrict public `.json` access. Mitigation: unlikely for product pages; could fall back to HTML scraping if needed.
