## MODIFIED Requirements

### Requirement: Shopify provider uses predictive search and JSON API
The Shopify provider (renamed `ShopifySearcher`) SHALL be a generic provider configured with a `base_url` and optional custom field labels. It SHALL search for coffees using the Shopify predictive search endpoint (`/search/suggest?q={query}&resources[type]=product`), select the best matching product, then fetch product data from the Shopify JSON endpoint (`/products/{handle}.json`).

#### Scenario: Product found via predictive search
- **WHEN** the ShopifySearcher searches for "Montero Family" on morgoncoffeeroasters.com
- **THEN** it SHALL call `/search/suggest.json?q=Montero+Family&resources[type]=product`, find the matching product handle, and fetch `/products/{handle}.json`

#### Scenario: No search results
- **WHEN** the ShopifySearcher searches for a coffee name that returns no results
- **THEN** it SHALL return None indicating coffee not found

#### Scenario: Multiple search results
- **WHEN** the predictive search returns multiple products
- **THEN** the provider SHALL select the product whose title best matches the query using sequence matching

### Requirement: Shopify provider extracts structured fields deterministically
The ShopifySearcher SHALL extract `name` from the product title, `price` from variant data, and `weight` from the variant title. For coffee-specific fields (`country_grown`, `bean_type`, `process`, `roast_level`, `tasting_notes`), it SHALL parse the `body_html` content using pattern matching against known field labels. The provider SHALL NOT use any LLM or external AI service for extraction.

The provider SHALL search for label-value patterns in the stripped HTML text, matching labels in both English and Swedish (e.g., "Country", "Origin", "Land", "Ursprung" for `country_grown`). Labels SHALL be matched case-insensitively.

#### Scenario: Structured key-value extraction
- **WHEN** the provider fetches a product with `body_html` containing "Country: Costa Rica" and "Process: Honey" and variants with price 199 / 250g
- **THEN** the returned dict SHALL contain `country_grown: "Costa Rica"`, `process: "Honey"`, `price: "199 SEK"`, `weight: "250g"`

#### Scenario: Swedish label extraction
- **WHEN** the provider fetches a product with `body_html` containing "Ursprung: Brasilien" and "Processmetod: Natural"
- **THEN** the returned dict SHALL contain `country_grown: "Brasilien"` and `process: "Natural"`

#### Scenario: Missing fields in description
- **WHEN** the `body_html` mentions only origin and process but not variety or roast level
- **THEN** the returned dict SHALL contain `country_grown` and `process` but omit `bean_type` and `roast_level`

#### Scenario: No matching labels in description
- **WHEN** the `body_html` contains only narrative text with no recognizable field labels
- **THEN** the returned dict SHALL contain only `name`, `price`, and `weight` (from JSON API data) with no body-extracted fields

### Requirement: WooCommerce provider extracts data from JSON-LD
The WooCommerce provider (renamed `WooCommerceSearcher`) SHALL be configured with a `base_url` and a `field_map` dict that maps site-specific JSON-LD `additionalProperty` names to CoffeeBean field names. It SHALL search using the WooCommerce search URL pattern (`/?s={query}&post_type=product`), find the best matching product page, fetch it, and extract data from JSON-LD `application/ld+json` script tags.

The provider SHALL parse the Product entity's `additionalProperty` array and map values using the configured `field_map`. Fields not in the map SHALL be ignored. The provider SHALL NOT use any LLM or external AI service.

#### Scenario: Gringo Nordic field mapping
- **WHEN** the provider is configured with `field_map: {"land": "country_grown", "art-varietet": "bean_type", "processmetod": "process"}` and fetches a page with those JSON-LD properties
- **THEN** the returned dict SHALL contain CoffeeBean-named fields with the values from JSON-LD

#### Scenario: Partial data on product page
- **WHEN** the provider fetches a product page where some `additionalProperty` entries are missing
- **THEN** the returned dict SHALL contain only the fields that were present, with missing fields omitted

#### Scenario: Product name cleaned of roastery suffix
- **WHEN** the JSON-LD product name is "Peru Nueva Florida - Gringo Nordic Coffee Roaster"
- **THEN** the returned `name` field SHALL be "Peru Nueva Florida" (suffix removed)

#### Scenario: WooCommerce search returns multiple results
- **WHEN** the search returns multiple product links
- **THEN** the provider SHALL select the product whose name best matches the search query

### Requirement: Provider registry with roaster matching
The system SHALL maintain a registry of lookup providers (now typed as `CoffeeSearcher`) keyed by roastery name. When a lookup is requested, the system SHALL match the given `roaster` value against provider keys using case-insensitive comparison. A match SHALL succeed if the provider key is a substring of the roaster name or vice versa.

#### Scenario: Exact match
- **WHEN** lookup is requested with roaster "Gringo Nordic"
- **THEN** the system SHALL match to the "gringo" provider

#### Scenario: Partial match
- **WHEN** lookup is requested with roaster "Gringo Nordic Coffee Roasters"
- **THEN** the system SHALL match to the "gringo" provider

#### Scenario: No match
- **WHEN** lookup is requested with roaster "Unknown Roasters"
- **THEN** the system SHALL return no matching provider

### Requirement: Initial provider configuration
The system SHALL ship with three configured providers:
- `"gringo"` → WooCommerceSearcher for `gringonordic.se` with Swedish JSON-LD field mapping
- `"morgon"` → ShopifySearcher for `morgoncoffeeroasters.com`
- `"kafferäven"` → ShopifySearcher for `kafferaven.se`

#### Scenario: All three providers available
- **WHEN** lookups are requested for roasters matching "Gringo", "Morgon", and "Kafferäven"
- **THEN** all three SHALL resolve to their respective providers and return coffee data

## REMOVED Requirements

### Requirement: Shopify provider extracts structured fields and uses Haiku for body_html
**Reason**: Replaced by deterministic pattern-matching extraction. LLM-based extraction was unreliable and added latency/cost.
**Migration**: The new `ShopifySearcher` extracts the same fields using label pattern matching in `body_html` instead of sending text to Claude Haiku.

## ADDED Requirements

### Requirement: CoffeeSearcher base class
All lookup providers SHALL inherit from a `CoffeeSearcher` base class that defines the plugin interface. The base class SHALL define three abstract methods: `search(coffee_name) -> identifier`, `fetch_product(identifier) -> product_data`, and `extract(product_data) -> dict`. It SHALL provide a default `lookup(coffee_name) -> dict | None` method that calls search → fetch_product → extract in sequence.

#### Scenario: Plugin implements all required methods
- **WHEN** a new platform plugin is created inheriting from `CoffeeSearcher`
- **THEN** it SHALL implement `search()`, `fetch_product()`, and `extract()` methods

#### Scenario: Default lookup orchestration
- **WHEN** `lookup()` is called on any `CoffeeSearcher` subclass
- **THEN** it SHALL call `search()` to find the product, `fetch_product()` to get product data, and `extract()` to produce the result dict
- **AND** if `search()` returns None, `lookup()` SHALL return None
- **AND** if `fetch_product()` returns None, `lookup()` SHALL return None
