## MODIFIED Requirements

### Requirement: WooCommerce provider extracts data from JSON-LD
The WooCommerce provider (renamed `WooCommerceSearcher`) SHALL be configured with a `base_url` and a `field_map` dict that maps site-specific JSON-LD `additionalProperty` names to CoffeeBean field names. It SHALL search using the WooCommerce search URL pattern (`/?s={query}&post_type=product`), find the best matching product page, fetch it, and extract data from JSON-LD `application/ld+json` script tags.

The provider SHALL parse the Product entity's `additionalProperty` array and map values using the configured `field_map`. Fields not in the map SHALL be ignored. The provider SHALL NOT use any LLM or external AI service.

When searching, the provider SHALL handle the case where WooCommerce redirects a single-result search directly to the product page. If the response URL contains `/product/`, the provider SHALL use that URL directly as the matched product.

When extracting product links from multi-result search pages, the provider SHALL only consider links within known WooCommerce product title elements (e.g., elements with class `jet-woo-builder-archive-product-title` or `woocommerce-loop-product__title`), not sidebar, footer, or related product links.

The provider SHALL reject search matches where the title similarity ratio is below 0.3.

#### Scenario: Single search result redirects to product page
- **WHEN** a WooCommerce search for "Purple Pacamara" returns a redirect to `/product/el-salvador-purple-pacamara-2/`
- **THEN** the provider SHALL use that redirected URL as the matched product

#### Scenario: Multi-result search picks best match
- **WHEN** a WooCommerce search returns multiple product results
- **THEN** the provider SHALL only consider product links within search result title elements, not sidebar or footer links

#### Scenario: Low similarity match rejected
- **WHEN** the best matching product title has a similarity ratio below 0.3
- **THEN** the provider SHALL return None (no match) rather than the low-confidence result

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
