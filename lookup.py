"""Coffee roastery lookup — fetch product details from roastery websites."""

import json
import os
import re
from difflib import SequenceMatcher
from html.parser import HTMLParser
from urllib.parse import quote_plus, urljoin
from urllib.request import urlopen, Request
from urllib.error import URLError

import anthropic


def _fetch_json(url: str) -> dict | list | None:
    """Fetch a URL and parse as JSON."""
    try:
        req = Request(url, headers={"User-Agent": "CoffeeTracker/1.0"})
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return None


def _fetch_html(url: str) -> str | None:
    """Fetch a URL and return raw HTML."""
    try:
        req = Request(url, headers={"User-Agent": "CoffeeTracker/1.0"})
        with urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def _strip_html(html: str) -> str:
    """Strip HTML tags and return plain text."""
    class _Stripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self._parts: list[str] = []
            self._skip = False
        def handle_starttag(self, tag, attrs):
            self._skip = tag in ("script", "style", "noscript")
        def handle_endtag(self, tag):
            if tag in ("script", "style", "noscript"):
                self._skip = False
        def handle_data(self, data):
            if not self._skip:
                self._parts.append(data)
        def get_text(self) -> str:
            return " ".join(self._parts)
    s = _Stripper()
    s.feed(html)
    return s.get_text().strip()


# ── Shopify Provider ────────────────────────────────────────────────────────

class ShopifyProvider:
    """Generic lookup provider for any Shopify-based roastery."""

    def __init__(self, base_url: str):
        self.base_url = f"https://www.{base_url}" if not base_url.startswith("http") else base_url

    def search(self, coffee_name: str) -> str | None:
        """Search for a product and return the best matching handle."""
        url = f"{self.base_url}/search/suggest.json?q={quote_plus(coffee_name)}&resources[type]=product"
        data = _fetch_json(url)
        if not data:
            return None
        try:
            products = data["resources"]["results"]["products"]
        except (KeyError, TypeError):
            return None
        if not products:
            return None
        # Pick best matching product by title similarity
        query_lower = coffee_name.lower()
        best_handle = None
        best_ratio = 0.0
        for p in products:
            title = p.get("title", "")
            ratio = SequenceMatcher(None, query_lower, title.lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_handle = p.get("handle")
        return best_handle

    def fetch_product(self, handle: str) -> dict | None:
        """Fetch product data from the Shopify JSON API."""
        url = f"{self.base_url}/products/{handle}.json"
        data = _fetch_json(url)
        if not data:
            return None
        return data.get("product")

    def extract(self, product: dict) -> dict:
        """Extract coffee fields from a Shopify product dict."""
        result = {}
        # Name from title
        title = product.get("title", "")
        if title:
            result["name"] = title

        # Price and weight from first variant
        variants = product.get("variants", [])
        if variants:
            v = variants[0]
            price = v.get("price")
            if price:
                result["price"] = f"{price} SEK"
            # Weight: use the option title (e.g. "250g") rather than grams field
            title_v = v.get("title", "")
            if title_v and title_v.lower() != "default title":
                result["weight"] = title_v

        # Use Claude Haiku to extract coffee details from body_html
        body_html = product.get("body_html", "")
        if body_html:
            body_text = _strip_html(body_html)
            if body_text:
                extracted = self._extract_with_haiku(body_text)
                if extracted:
                    # Merge: Haiku results fill in, but don't overwrite name/price/weight
                    for key, val in extracted.items():
                        if val and key not in result:
                            result[key] = val

        return result

    def _extract_with_haiku(self, description_text: str) -> dict | None:
        """Send product description to Claude Haiku for structured extraction."""
        try:
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY_FOR_LOOKUP"))
            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=512,
                messages=[{
                    "role": "user",
                    "content": (
                        "Extract coffee details from this product description. "
                        "Keep values in their original language (often Swedish). "
                        "Respond with ONLY valid JSON, no markdown:\n"
                        '{"name": "...", "country_grown": "...", "bean_type": "...", '
                        '"process": "...", "tasting_notes": "...", "roast_level": "..."}\n'
                        "country_grown: country/region where beans were grown. "
                        "bean_type: species or variety (e.g. Arabica, Bourbon, Catuai). "
                        "process: processing method (e.g. Washed, Natural, Honey). "
                        "tasting_notes: comma-separated flavor notes. "
                        "roast_level: roast level if mentioned. "
                        "Use null for fields you can't determine.\n\n"
                        f"Description:\n{description_text[:4000]}"
                    ),
                }],
            )
            text = message.content[0].text
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            data = json.loads(text.strip())
            # Filter out null values
            return {k: v for k, v in data.items() if v is not None}
        except Exception:
            return None

    def lookup(self, coffee_name: str) -> dict | None:
        """Full lookup: search → fetch → extract."""
        handle = self.search(coffee_name)
        if not handle:
            return None
        product = self.fetch_product(handle)
        if not product:
            return None
        return self.extract(product)


# ── WooCommerce Provider ────────────────────────────────────────────────────

class _LinkExtractor(HTMLParser):
    """Extract product links from WooCommerce search results."""
    def __init__(self):
        super().__init__()
        self.links: list[tuple[str, str]] = []  # (url, text)
        self._current_link = None
        self._current_text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs_dict = dict(attrs)
            href = attrs_dict.get("href", "")
            if "/product/" in href:
                self._current_link = href
                self._current_text = ""

    def handle_data(self, data):
        if self._current_link is not None:
            self._current_text += data

    def handle_endtag(self, tag):
        if tag == "a" and self._current_link:
            self.links.append((self._current_link, self._current_text.strip()))
            self._current_link = None


class _JsonLdExtractor(HTMLParser):
    """Extract JSON-LD script contents from HTML."""
    def __init__(self):
        super().__init__()
        self.json_ld_blocks: list[str] = []
        self._in_jsonld = False
        self._current = ""

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            attrs_dict = dict(attrs)
            if attrs_dict.get("type") == "application/ld+json":
                self._in_jsonld = True
                self._current = ""

    def handle_data(self, data):
        if self._in_jsonld:
            self._current += data

    def handle_endtag(self, tag):
        if tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.json_ld_blocks.append(self._current)


class WooCommerceProvider:
    """Lookup provider for WooCommerce-based roasteries with JSON-LD data."""

    def __init__(self, base_url: str, field_map: dict[str, str]):
        self.base_url = f"https://www.{base_url}" if not base_url.startswith("http") else base_url
        self.field_map = field_map

    def search(self, coffee_name: str) -> str | None:
        """Search WooCommerce and return the best matching product URL."""
        url = f"{self.base_url}/?s={quote_plus(coffee_name)}&post_type=product"
        html = _fetch_html(url)
        if not html:
            return None
        extractor = _LinkExtractor()
        extractor.feed(html)
        if not extractor.links:
            return None
        # Pick best match by title similarity
        query_lower = coffee_name.lower()
        best_url = None
        best_ratio = 0.0
        for link_url, link_text in extractor.links:
            ratio = SequenceMatcher(None, query_lower, link_text.lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_url = link_url
        return best_url

    def fetch_and_extract(self, product_url: str) -> dict | None:
        """Fetch a product page and extract data from JSON-LD."""
        html = _fetch_html(product_url)
        if not html:
            return None
        extractor = _JsonLdExtractor()
        extractor.feed(html)

        # Find Product entity in JSON-LD blocks
        product = None
        for block in extractor.json_ld_blocks:
            try:
                data = json.loads(block)
            except (json.JSONDecodeError, ValueError):
                continue
            # Handle @graph arrays
            if isinstance(data, dict) and "@graph" in data:
                for item in data["@graph"]:
                    if isinstance(item, dict) and item.get("@type") == "Product":
                        product = item
                        break
            elif isinstance(data, dict) and data.get("@type") == "Product":
                product = data
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == "Product":
                        product = item
                        break
            if product:
                break

        if not product:
            return None

        result = {}

        # Extract name (clean roastery suffix like "- Gringo Nordic Coffee Roaster")
        raw_name = product.get("name", "")
        if " - " in raw_name:
            result["name"] = raw_name.split(" - ")[0].strip()
        elif raw_name:
            result["name"] = raw_name

        # Extract price from offers
        offers = product.get("offers")
        if isinstance(offers, dict):
            price = offers.get("price") or offers.get("lowPrice")
            currency = offers.get("priceCurrency", "SEK")
            if price:
                result["price"] = f"{price} {currency}"
        elif isinstance(offers, list) and offers:
            price = offers[0].get("price")
            currency = offers[0].get("priceCurrency", "SEK")
            if price:
                result["price"] = f"{price} {currency}"

        # Extract weight
        weight = product.get("weight")
        if isinstance(weight, dict):
            val = weight.get("value")
            unit = weight.get("unitCode", "")
            if val:
                unit_display = {"KGM": "kg", "GRM": "g"}.get(unit, unit)
                result["weight"] = f"{val} {unit_display}".strip()
        elif weight:
            result["weight"] = str(weight)

        # Extract additionalProperty fields via field_map
        for prop in product.get("additionalProperty", []):
            prop_name = prop.get("name", "")
            prop_value = prop.get("value", "")
            if prop_name in self.field_map and prop_value:
                result[self.field_map[prop_name]] = prop_value

        return result

    def lookup(self, coffee_name: str) -> dict | None:
        """Full lookup: search → fetch → extract."""
        product_url = self.search(coffee_name)
        if not product_url:
            return None
        return self.fetch_and_extract(product_url)


# ── Provider Registry ───────────────────────────────────────────────────────

PROVIDERS: dict[str, ShopifyProvider | WooCommerceProvider] = {
    "gringo": WooCommerceProvider(
        base_url="gringonordic.se",
        field_map={
            "land": "country_grown",
            "art-varietet": "bean_type",
            "processmetod": "process",
            "region": "region",
            "vaxthojd": "elevation",
        },
    ),
    "morgon": ShopifyProvider(base_url="morgoncoffeeroasters.com"),
    "kafferäven": ShopifyProvider(base_url="kafferaven.se"),
}


def _match_provider(roaster: str) -> ShopifyProvider | WooCommerceProvider | None:
    """Match a roaster name to a provider using case-insensitive substring matching."""
    if not roaster:
        return None
    roaster_lower = roaster.lower().strip()
    for key, provider in PROVIDERS.items():
        key_lower = key.lower()
        if key_lower in roaster_lower or roaster_lower in key_lower:
            return provider
    return None


def has_provider(roaster: str) -> bool:
    """Check if a lookup provider exists for the given roaster."""
    return _match_provider(roaster) is not None


def lookup_coffee(roaster: str, coffee_name: str) -> dict | None:
    """Look up coffee details from a roastery website.

    Returns a dict of CoffeeBean field names → values, or None if no provider
    or coffee not found.
    """
    provider = _match_provider(roaster)
    if provider is None:
        return None
    return provider.lookup(coffee_name)
