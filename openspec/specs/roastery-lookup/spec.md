## ADDED Requirements

### Requirement: Lookup API endpoint
The system SHALL expose a `POST /api/lookup` endpoint that accepts a JSON body with `roaster` (string) and `coffee_name` (string) fields. The endpoint SHALL return a JSON object with extracted coffee details mapped to CoffeeBean field names, or an error response.

#### Scenario: Successful lookup via Shopify provider
- **WHEN** a POST request is made to `/api/lookup` with `{ "roaster": "Morgon", "coffee_name": "Montero Family Espresso" }`
- **THEN** the response SHALL have status 200 and return a JSON object containing extracted fields such as `country_grown`, `bean_type`, `process`, and `tasting_notes`

#### Scenario: Successful lookup via WooCommerce provider
- **WHEN** a POST request is made to `/api/lookup` with `{ "roaster": "Gringo", "coffee_name": "Peru Nueva Florida" }`
- **THEN** the response SHALL have status 200 and return a JSON object containing at minimum `country_grown`, `bean_type`, and `process` fields

#### Scenario: Roaster has no lookup provider
- **WHEN** a POST request is made to `/api/lookup` with a roaster that has no registered provider
- **THEN** the response SHALL have status 404 and return `{ "error": "No lookup provider for this roaster" }`

#### Scenario: Coffee not found on roastery website
- **WHEN** a POST request is made to `/api/lookup` with a valid roaster but a coffee name that yields no search results
- **THEN** the response SHALL have status 404 and return `{ "error": "Coffee not found" }`

#### Scenario: Missing required fields
- **WHEN** a POST request is made to `/api/lookup` without `roaster` or `coffee_name`
- **THEN** the response SHALL have status 400 and return an error message

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

### Requirement: Provider registry with roaster matching
The system SHALL maintain a registry of lookup providers (typed as `CoffeeSearcher`) keyed by roastery name. When a lookup is requested, the system SHALL match the given `roaster` value against provider keys using case-insensitive comparison. A match SHALL succeed if the provider key is a substring of the roaster name or vice versa.

#### Scenario: Exact match
- **WHEN** lookup is requested with roaster "Gringo Nordic"
- **THEN** the system SHALL match to the "gringo" provider

#### Scenario: Partial match
- **WHEN** lookup is requested with roaster "Gringo Nordic Coffee Roasters"
- **THEN** the system SHALL match to the "gringo" provider

#### Scenario: No match
- **WHEN** lookup is requested with roaster "Unknown Roasters"
- **THEN** the system SHALL return no matching provider

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

### Requirement: Initial provider configuration
The system SHALL ship with three configured providers:
- `"gringo"` → WooCommerceSearcher for `gringonordic.se` with Swedish JSON-LD field mapping
- `"morgon"` → ShopifySearcher for `morgoncoffeeroasters.com`
- `"kafferäven"` → ShopifySearcher for `kafferaven.se`

#### Scenario: All three providers available
- **WHEN** lookups are requested for roasters matching "Gringo", "Morgon", and "Kafferäven"
- **THEN** all three SHALL resolve to their respective providers and return coffee data

### Requirement: Lookup availability indicator in API
The system SHALL expose a `GET /api/lookup/available` endpoint that accepts a `roaster` query parameter and returns whether a lookup provider exists for that roaster.

#### Scenario: Provider available
- **WHEN** a GET request is made to `/api/lookup/available?roaster=Gringo`
- **THEN** the response SHALL return `{ "available": true }`

#### Scenario: Provider not available
- **WHEN** a GET request is made to `/api/lookup/available?roaster=Unknown`
- **THEN** the response SHALL return `{ "available": false }`

### Requirement: Frontend lookup button in review form
The review form (used for both scan results and manual-add) SHALL display a "Lookup" button when the roaster field value matches a roastery with an available lookup provider. The button SHALL be positioned near the coffee name field.

#### Scenario: Lookup button appears for known roastery
- **WHEN** the user enters "Gringo" in the roaster field of the review form
- **THEN** a "Lookup" button SHALL appear near the coffee name field

#### Scenario: Lookup button hidden for unknown roastery
- **WHEN** the user enters "Unknown Roasters" in the roaster field
- **THEN** no lookup button SHALL be displayed

#### Scenario: Lookup button hidden when roaster field is empty
- **WHEN** the roaster field is empty
- **THEN** no lookup button SHALL be displayed

### Requirement: Lookup fills empty fields only
When lookup results are applied to the review form, the system SHALL only fill fields that are currently empty. Fields that already contain a value (from scan or user input) SHALL NOT be overwritten.

#### Scenario: Empty fields filled
- **WHEN** the review form has `country_grown` empty and lookup returns `country_grown: "Peru"`
- **THEN** the `country_grown` field SHALL be set to "Peru"

#### Scenario: Existing values preserved
- **WHEN** the review form has `country_grown` set to "Colombia" and lookup returns `country_grown: "Peru"`
- **THEN** the `country_grown` field SHALL remain "Colombia"

#### Scenario: Loading state during lookup
- **WHEN** the user clicks the lookup button
- **THEN** the button SHALL show a loading indicator until the lookup completes or fails

#### Scenario: Lookup error displayed
- **WHEN** the lookup fails (network error or coffee not found)
- **THEN** the form SHALL display a brief error message and no fields SHALL be modified
