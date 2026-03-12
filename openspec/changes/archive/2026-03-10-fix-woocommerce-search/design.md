## Context

The `WooCommerceSearcher.search()` uses Python's `urlopen` which follows redirects transparently. When WooCommerce has a single search result, it 302-redirects to the product page. The code then parses the product page with `_LinkExtractor`, which picks up sidebar/related product links instead of the actual product.

On multi-result pages, the search results use Jet WooCommerce Builder with `jet-woo-builder-archive-product-title` class for product titles, not plain `<a>` tags with `/product/` in href.

## Goals / Non-Goals

**Goals:**
- Handle single-result redirects (detect redirect URL is a product page)
- Fix multi-result extraction to only target search result product titles
- Add minimum similarity threshold to reject garbage matches

**Non-Goals:**
- Changing the Shopify searcher
- Changing the base class interface

## Decisions

### 1. Detect single-result redirect via response URL

Use `urlopen` response's `.url` attribute to check if we were redirected to a product page. If the final URL contains `/product/`, that IS our result — return it directly without link extraction.

**Why**: This is how WooCommerce handles single-result searches. The redirect URL is the correct answer.

### 2. Fix `_LinkExtractor` for multi-result pages

Gringo uses Jet WooCommerce Builder. Search result titles are in elements with class `jet-woo-builder-archive-product-title`. Only extract links from within these title elements.

However, since other WooCommerce sites may use standard WooCommerce markup (class `woocommerce-loop-product__title` or `woocommerce-LoopProduct-link`), we should check for both Jet-style and standard WooCommerce patterns.

**Approach**: Track whether we're inside a known product title container and only capture links from those containers.

### 3. Add similarity threshold of 0.3

Reject matches below 0.3 ratio. The current bug had a 0.28 match being accepted. A 0.3 threshold is low enough to allow partial matches but high enough to reject random noise.

**Why**: Even with better link extraction, a threshold prevents returning confidently wrong results.

## Risks / Trade-offs

- **[Jet WooBuilder-specific parsing]** → If a future WooCommerce roaster uses different markup, extraction may fail. Mitigation: falls back to returning None (no wrong data), and the `_LinkExtractor` can be extended with new class patterns.
