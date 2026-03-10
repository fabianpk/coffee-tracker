## Context

The coffee tracker has a roastery lookup feature that fetches coffee details from roastery websites. Currently, the `ShopifyProvider` uses Claude Haiku to parse product description HTML into structured fields. The `WooCommerceProvider` already uses deterministic JSON-LD parsing. The user wants to eliminate LLM usage from lookup entirely, making all providers deterministic.

The existing module (`lookup.py`, 388 lines) has two provider classes with no shared base class, a provider registry dict, and public functions `has_provider()` / `lookup_coffee()`. The Flask endpoints (`/api/lookup`, `/api/lookup/available`) and frontend lookup button are working and will not change.

## Goals / Non-Goals

**Goals:**
- Remove LLM dependency from lookup — all extraction is deterministic HTML/JSON parsing
- Introduce a `CoffeeSearcher` base class that formalizes the plugin interface
- Rewrite Shopify extraction to parse `body_html` with pattern-matching instead of Haiku
- Keep the external API contract identical (same endpoints, same request/response format)
- Keep the same three roasters working (Gringo, Morgon, Kafferäven)

**Non-Goals:**
- Adding new roasters (can be done later by adding entries to the registry)
- Changing the frontend lookup UI
- Modifying the scan flow (which still uses Claude for vision)
- Building a generic "any roastery" scraper — each provider targets a known platform

## Decisions

### 1. Introduce `CoffeeSearcher` abstract base class

The base class defines the plugin interface:

```python
class CoffeeSearcher:
    def search(self, coffee_name: str) -> str | None: ...
    def fetch_product(self, identifier: str) -> dict | None: ...
    def extract(self, product_data: dict) -> dict: ...
    def lookup(self, coffee_name: str) -> dict | None: ...
```

`lookup()` has a default implementation calling search → fetch → extract. Subclasses override the individual steps.

**Why**: Formalizes what a plugin must implement, makes it easy to add new platform types (e.g. SquarespaceSearcher) without changing surrounding code. The base class also provides the `lookup()` template method so subclasses only need to implement the three steps.

**Alternative considered**: Keep separate classes without a base — rejected because the uniform interface is the whole point of the refactor.

### 2. Shopify extraction via structured HTML patterns

Shopify product descriptions frequently use patterns like:
- Key-value pairs: `<strong>Country:</strong> Colombia` or `Country: Colombia`
- Labeled list items: `<li>Process: Washed</li>`
- Comma-separated tasting notes after a label

The new `ShopifySearcher.extract()` will:
1. Extract `name`, `price`, `weight` from the JSON API (same as today)
2. Parse `body_html` with regex patterns to find known field labels and extract their values
3. Fall back gracefully — missing fields just stay empty

**Why**: Shopify product pages from coffee roasters follow fairly consistent patterns. For the two roasters we support (Morgon, Kafferäven), pattern matching is sufficient and eliminates the per-lookup Haiku API call (~$0.001/call, ~2s latency).

**Alternative considered**: Use CSS selectors / BeautifulSoup — rejected to avoid adding a dependency. The stdlib `HTMLParser` + regex is sufficient for the structured patterns.

### 3. Keep `WooCommerceSearcher` largely unchanged

The WooCommerce provider already does deterministic JSON-LD extraction. It just needs to be renamed to `WooCommerceSearcher` and inherit from `CoffeeSearcher`.

**Why**: It already works correctly without LLM. No reason to rewrite.

### 4. Registry stays a plain dict

```python
PROVIDERS: dict[str, CoffeeSearcher] = {
    "gringo": WooCommerceSearcher(...),
    "morgon": ShopifySearcher(...),
    "kafferäven": ShopifySearcher(...),
}
```

**Why**: Three entries doesn't need a plugin discovery system. Adding a roaster = adding a line.

### 5. Shopify body_html field extraction strategy

Define a mapping of known labels → CoffeeBean fields:

```python
FIELD_LABELS = {
    "country_grown": ["Country", "Origin", "Land", "Region", "Ursprung"],
    "bean_type": ["Variety", "Varietal", "Bean", "Sort", "Art"],
    "process": ["Process", "Processing", "Processmetod"],
    "roast_level": ["Roast", "Roast Level", "Rostning", "Rostgrad"],
    "tasting_notes": ["Tasting Notes", "Notes", "Smaknoter", "Smaknot", "Flavor", "Flavour"],
}
```

For each field, search the stripped HTML text for `label:?\s*value` patterns. This handles both English and Swedish labels common across Nordic coffee roasters.

**Why**: Simple, fast, no dependencies. Easy to extend with new labels per roaster if needed.

## Risks / Trade-offs

- **[Less flexible extraction]** → Pattern matching will miss fields that Haiku could infer from narrative text. Mitigation: acceptable trade-off since the user explicitly wants deterministic behavior, and missing fields can be filled manually or via scan.
- **[Per-roaster label variations]** → Different Shopify roasters may use different label words. Mitigation: the label list covers common English + Swedish terms; can be extended per-provider if needed by passing custom labels to `ShopifySearcher.__init__()`.
- **[Shopify page format changes]** → If a roaster changes their description format, extraction breaks silently. Mitigation: same risk existed with Haiku (just less visible); at least deterministic parsing fails predictably and is easy to debug.
