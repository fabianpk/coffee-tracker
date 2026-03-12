## 1. Handle single-result redirect

- [x] 1.1 Modify `WooCommerceSearcher.search()` to use `urlopen` response URL — if the final URL contains `/product/`, return it directly as the match (WooCommerce single-result redirect)

## 2. Fix multi-result link extraction

- [x] 2.1 Rewrite `_LinkExtractor` to only capture links within WooCommerce product title elements (class `jet-woo-builder-archive-product-title` or `woocommerce-loop-product__title`), ignoring sidebar/footer/related product links

## 3. Add similarity threshold

- [x] 3.1 Add minimum similarity threshold of 0.3 in `WooCommerceSearcher.search()` — return None if best match ratio is below threshold

## 4. Verification

- [x] 4.1 Test "Purple Pacamara" lookup against Gringo Nordic — should return El Salvador, 169 SEK
