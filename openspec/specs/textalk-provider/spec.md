## Purpose
Implement a TextalkSearcher provider that searches and extracts coffee data from Textalk/Abicart-based shops via JSON-RPC API.

## Requirements

### Requirement: TextalkSearcher implements CoffeeSearcher ABC
The `TextalkSearcher` class SHALL inherit from `CoffeeSearcher` and implement the `search()`, `fetch_product()`, and `extract()` methods. It SHALL be configured with a `base_url` (the shop's domain) and use the Abicart JSON-RPC 2.0 API at `{base_url}/backend/jsonrpc/v1/` for all data access.

#### Scenario: Provider instantiation
- **WHEN** a `TextalkSearcher` is created with `base_url="baristashopen.se"`
- **THEN** it SHALL use the API endpoint `https://www.baristashopen.se/backend/jsonrpc/v1/`

### Requirement: TextalkSearcher searches via Article.list JSON-RPC
The `search()` method SHALL send a JSON-RPC 2.0 POST request to the API endpoint calling `Article.list`. The request SHALL include a search filter with the coffee name as term and a relevance threshold. The method SHALL request at minimum the fields `uid` and `name`. It SHALL select the best matching article by comparing article names to the query using `SequenceMatcher`, and return the article UID.

#### Scenario: Successful search with results
- **WHEN** `search("Ethiopia Guji")` is called
- **THEN** it SHALL POST a JSON-RPC request with method `Article.list`, params containing `filters.search.term` set to `"Ethiopia Guji"`, and return the UID of the best-matching article

#### Scenario: No search results
- **WHEN** `search("Nonexistent Coffee XYZ123")` is called and the API returns an empty result list
- **THEN** `search()` SHALL return `None`

#### Scenario: Multiple results with best match selection
- **WHEN** the API returns multiple articles for a search query
- **THEN** the method SHALL use `SequenceMatcher` to compare each article's name against the query and select the article with the highest similarity ratio

#### Scenario: Low similarity match rejected
- **WHEN** the best matching article name has a similarity ratio below 0.3
- **THEN** `search()` SHALL return `None`

### Requirement: TextalkSearcher fetches product via Article.get JSON-RPC
The `fetch_product()` method SHALL send a JSON-RPC 2.0 POST request calling `Article.get` with the article UID. It SHALL request fields including `name`, `price`, `weight`, `description`, `introductionText`, and `url`. It SHALL return the article data dict.

#### Scenario: Successful product fetch
- **WHEN** `fetch_product(12345)` is called with a valid article UID
- **THEN** it SHALL POST a JSON-RPC request with method `Article.get` and return the article data dict containing name, price, weight, and description fields

#### Scenario: Invalid UID
- **WHEN** `fetch_product(99999999)` is called with a nonexistent UID
- **THEN** it SHALL return `None`

### Requirement: TextalkSearcher extracts coffee fields deterministically
The `extract()` method SHALL extract structured coffee data from the article dict without using any LLM. It SHALL:
- Extract `name` from the article's `name` field (using the Swedish `sv` locale key if the name is a language dict)
- Extract `price` from the article's `price` field (current price)
- Extract `weight` from the article's `weight` field
- Parse the `description` and/or `introductionText` fields using the shared `_extract_labeled_fields()` helper to find `country_grown`, `bean_type`, `process`, `roast_level`, and `tasting_notes`

#### Scenario: Full data extraction
- **WHEN** an article dict contains name "Ethiopia Guji Natural", price 149 SEK, weight 250g, and description with "Ursprung: Etiopien" and "Process: Natural"
- **THEN** `extract()` SHALL return a dict with `name`, `price`, `weight`, `country_grown`, and `process` fields populated

#### Scenario: Multilingual name field
- **WHEN** the article's `name` field is `{"sv": "Kaffe Blend", "en": "Coffee Blend"}`
- **THEN** `extract()` SHALL use the Swedish (`sv`) value "Kaffe Blend"

#### Scenario: Missing description
- **WHEN** the article dict has no `description` or `introductionText`
- **THEN** `extract()` SHALL return only `name`, `price`, and `weight` with no coffee-specific fields

### Requirement: JSON-RPC request format
All API requests SHALL use JSON-RPC 2.0 format with `Content-Type: application/json`. Each request SHALL include `jsonrpc: "2.0"`, a `method` string, a `params` array, and an `id` field. The response result SHALL be extracted from the `result` field of the JSON-RPC response.

#### Scenario: Valid JSON-RPC request structure
- **WHEN** any API call is made
- **THEN** the request body SHALL be valid JSON-RPC 2.0 with all required fields
