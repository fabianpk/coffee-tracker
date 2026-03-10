## 1. CoffeeSearcher Base Class

- [x] 1.1 Create `CoffeeSearcher` base class in `lookup.py` with abstract methods `search()`, `fetch_product()`, `extract()` and default `lookup()` implementation that chains them

## 2. Shopify Deterministic Extraction

- [x] 2.1 Define `FIELD_LABELS` mapping of CoffeeBean field names to lists of known English/Swedish labels (Country, Origin, Land, Ursprung, Variety, Process, etc.)
- [x] 2.2 Implement `_extract_labeled_fields(text, labels)` helper that pattern-matches `label:?\s*value` in stripped HTML text and returns a dict of extracted fields
- [x] 2.3 Rewrite `ShopifyProvider` as `ShopifySearcher(CoffeeSearcher)` — keep `search()` and `fetch_product()` as-is, replace `extract()` to use pattern matching instead of Haiku, remove `_extract_with_haiku()`

## 3. WooCommerce Refactor

- [x] 3.1 Rename `WooCommerceProvider` to `WooCommerceSearcher(CoffeeSearcher)` — adapt `search()` and `fetch_and_extract()` to match the base class interface (`fetch_product()` + `extract()`)

## 4. Registry and Cleanup

- [x] 4.1 Update `PROVIDERS` dict to use new class names (`ShopifySearcher`, `WooCommerceSearcher`), type hint as `dict[str, CoffeeSearcher]`
- [x] 4.2 Remove `import anthropic` and `import os` (no longer needed for Haiku), verify `has_provider()` and `lookup_coffee()` still work unchanged
- [x] 4.3 Verify the app starts and the `/api/lookup` and `/api/lookup/available` endpoints respond correctly
