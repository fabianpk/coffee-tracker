"""Coffee roastery lookup — fetch product details from roastery websites."""

import json
import re
from abc import ABC, abstractmethod
from difflib import SequenceMatcher
from html.parser import HTMLParser
from urllib.parse import quote_plus
from urllib.request import urlopen, Request


def _fetch_json(url: str) -> dict | list | None:
    """Fetch a URL and parse as JSON."""
    try:
        req = Request(url, headers={"User-Agent": "CoffeeTracker/1.0"})
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception:
        return None


def _fetch_html(url: str) -> tuple[str, str] | None:
    """Fetch a URL and return (final_url, html) tuple."""
    try:
        req = Request(url, headers={"User-Agent": "CoffeeTracker/1.0"})
        with urlopen(req, timeout=10) as resp:
            final_url = resp.url
            html = resp.read().decode("utf-8", errors="replace")
            return (final_url, html)
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


# ── Base Class ─────────────────────────────────────────────────────────────

class CoffeeSearcher(ABC):
    """Base class for roastery lookup plugins."""

    @abstractmethod
    def search(self, coffee_name: str) -> str | None:
        """Search for a product. Returns an identifier (handle, URL, etc.) or None."""

    @abstractmethod
    def fetch_product(self, identifier: str) -> dict | None:
        """Fetch product data using the identifier from search()."""

    @abstractmethod
    def extract(self, product_data: dict) -> dict:
        """Extract CoffeeBean fields from product data."""

    def lookup(self, coffee_name: str) -> dict | None:
        """Full lookup: search → fetch_product → extract."""
        identifier = self.search(coffee_name)
        if not identifier:
            return None
        product_data = self.fetch_product(identifier)
        if not product_data:
            return None
        return self.extract(product_data)


# ── Shopify Searcher ───────────────────────────────────────────────────────

FIELD_LABELS: dict[str, list[str]] = {
    "country_grown": [
        "Country", "Origin", "Region", "Land", "Ursprung", "Odlingsland",
        "Produced in", "Farm Location", "Growing Region",
    ],
    "bean_type": [
        "Variety", "Varietal", "Bean", "Sort", "Art", "Varieties",
        "Cultivar", "Species",
    ],
    "process": [
        "Process", "Processing", "Processmetod", "Förädling",
        "Processing Method",
    ],
    "roast_level": [
        "Roast", "Roast Level", "Rostning", "Rostgrad", "Roast Profile",
    ],
    "tasting_notes": [
        "Tasting Notes", "Tasting notes", "Notes", "Smaknoter", "Smaknot",
        "Flavor", "Flavour", "Flavors", "Flavours", "Cup Profile",
        "Smakprofil",
    ],
}


def _extract_labeled_fields(text: str, labels: dict[str, list[str]] | None = None) -> dict:
    """Extract field values from text by matching known labels.

    Looks for patterns like "Label: value" or "Label - value" where value
    extends to the next label, sentence boundary, or line break.
    """
    if labels is None:
        labels = FIELD_LABELS
    result = {}
    for field, label_list in labels.items():
        for label in label_list:
            # Match "Label:" or "Label -" followed by the value
            # Value ends at next known label, period+space, or double space
            pattern = re.compile(
                rf"(?:^|\s|>){re.escape(label)}\s*[:–\-]\s*(.+?)(?:\s{{2,}}|\n|$)",
                re.IGNORECASE,
            )
            m = pattern.search(text)
            if m:
                value = m.group(1).strip().rstrip(".")
                if value and len(value) < 200:
                    result[field] = value
                    break
    return result


class ShopifySearcher(CoffeeSearcher):
    """Deterministic lookup provider for Shopify-based roasteries."""

    def __init__(self, base_url: str, extra_labels: dict[str, list[str]] | None = None):
        self.base_url = f"https://www.{base_url}" if not base_url.startswith("http") else base_url
        self.labels = dict(FIELD_LABELS)
        if extra_labels:
            for field, extra in extra_labels.items():
                self.labels[field] = self.labels.get(field, []) + extra

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
        """Extract coffee fields from a Shopify product dict using pattern matching."""
        result = {}
        title = product.get("title", "")
        if title:
            result["name"] = title

        variants = product.get("variants", [])
        if variants:
            v = variants[0]
            price = v.get("price")
            if price:
                result["price"] = f"{price} SEK"
            title_v = v.get("title", "")
            if title_v and title_v.lower() != "default title":
                result["weight"] = title_v

        body_html = product.get("body_html", "")
        if body_html:
            body_text = _strip_html(body_html)
            if body_text:
                extracted = _extract_labeled_fields(body_text, self.labels)
                for key, val in extracted.items():
                    if val and key not in result:
                        result[key] = val

        return result


# ── WooCommerce Searcher ───────────────────────────────────────────────────

_PRODUCT_TITLE_CLASSES = {
    "jet-woo-builder-archive-product-title",
    "woocommerce-loop-product__title",
    "woocommerce-LoopProduct-link",
}


class _LinkExtractor(HTMLParser):
    """Extract product links from WooCommerce search result title elements only."""
    def __init__(self):
        super().__init__()
        self.links: list[tuple[str, str]] = []  # (url, text)
        self._in_title_container = 0
        self._current_link = None
        self._current_text = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = set(attrs_dict.get("class", "").split())
        if classes & _PRODUCT_TITLE_CLASSES:
            self._in_title_container += 1
        if tag == "a" and self._in_title_container > 0:
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
        if self._in_title_container > 0 and tag in ("div", "h2", "h3", "a", "span"):
            self._in_title_container -= 1


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


class WooCommerceSearcher(CoffeeSearcher):
    """Lookup provider for WooCommerce-based roasteries with JSON-LD data."""

    def __init__(self, base_url: str, field_map: dict[str, str]):
        self.base_url = f"https://www.{base_url}" if not base_url.startswith("http") else base_url
        self.field_map = field_map

    def search(self, coffee_name: str) -> str | None:
        """Search WooCommerce and return the best matching product URL."""
        url = f"{self.base_url}/?s={quote_plus(coffee_name)}&post_type=product"
        result = _fetch_html(url)
        if not result:
            return None
        final_url, html = result
        # WooCommerce redirects single-result searches to the product page
        if "/product/" in final_url:
            return final_url
        extractor = _LinkExtractor()
        extractor.feed(html)
        if not extractor.links:
            return None
        query_lower = coffee_name.lower()
        best_url = None
        best_ratio = 0.0
        for link_url, link_text in extractor.links:
            ratio = SequenceMatcher(None, query_lower, link_text.lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_url = link_url
        if best_ratio < 0.3:
            return None
        return best_url

    def fetch_product(self, product_url: str) -> dict | None:
        """Fetch a product page and extract JSON-LD Product entity."""
        result = _fetch_html(product_url)
        if not result:
            return None
        _, html = result
        extractor = _JsonLdExtractor()
        extractor.feed(html)

        for block in extractor.json_ld_blocks:
            try:
                data = json.loads(block)
            except (json.JSONDecodeError, ValueError):
                continue
            if isinstance(data, dict) and "@graph" in data:
                for item in data["@graph"]:
                    if isinstance(item, dict) and item.get("@type") == "Product":
                        return item
            elif isinstance(data, dict) and data.get("@type") == "Product":
                return data
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == "Product":
                        return item
        return None

    def extract(self, product: dict) -> dict:
        """Extract CoffeeBean fields from JSON-LD Product entity."""
        result = {}

        raw_name = product.get("name", "")
        if " - " in raw_name:
            result["name"] = raw_name.split(" - ")[0].strip()
        elif raw_name:
            result["name"] = raw_name

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

        weight = product.get("weight")
        if isinstance(weight, dict):
            val = weight.get("value")
            unit = weight.get("unitCode", "")
            if val:
                unit_display = {"KGM": "kg", "GRM": "g"}.get(unit, unit)
                result["weight"] = f"{val} {unit_display}".strip()
        elif weight:
            result["weight"] = str(weight)

        for prop in product.get("additionalProperty", []):
            prop_name = prop.get("name", "")
            prop_value = prop.get("value", "")
            if prop_name in self.field_map and prop_value:
                result[self.field_map[prop_name]] = prop_value

        return result


# ── Provider Registry ───────────────────────────────────────────────────────

PROVIDERS: dict[str, CoffeeSearcher] = {
    "gringo": WooCommerceSearcher(
        base_url="gringonordic.se",
        field_map={
            "land": "country_grown",
            "art-varietet": "bean_type",
            "processmetod": "process",
            "region": "region",
            "vaxthojd": "elevation",
        },
    ),
    "morgon": ShopifySearcher(base_url="morgoncoffeeroasters.com"),
    "kafferäven": ShopifySearcher(base_url="kafferaven.se"),
}


def _match_provider(roaster: str) -> CoffeeSearcher | None:
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
