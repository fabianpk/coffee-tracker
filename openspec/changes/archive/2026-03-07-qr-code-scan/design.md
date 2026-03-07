## Context

The scan flow currently uploads a coffee bag photo, sends it to Claude Haiku for vision-based extraction, and returns structured coffee data. Many coffee bags include QR codes linking to product pages with richer information (altitude, varieties, detailed descriptions, pricing). The pyzbar library is already installed as a dependency.

During exploration, we confirmed that the product page at `https://kafferosterietkoppar.se/kop-espresso/papua-nya-guinea-jiwaka` contains significantly more detail than what's visible on the bag label.

## Goals / Non-Goals

**Goals:**
- Detect QR codes in uploaded images and extract URLs from them
- Fetch product page content from detected URLs
- Send page content to Claude for structured coffee data extraction
- Merge URL-sourced data with image-sourced data (URL data takes priority for non-null fields)
- Transparent to the user — no extra buttons or steps

**Non-Goals:**
- Supporting non-URL QR code data (e.g. plain text, vCards)
- Caching or storing fetched product pages
- Handling QR codes that require authentication or JavaScript rendering
- Supporting multiple QR codes per image (use first valid URL found)

## Decisions

### 1. QR detection runs on the already-processed image
**Decision:** Run pyzbar on the PIL Image object after it's opened but before JPEG compression, using the full-resolution RGB-converted image.
**Rationale:** The image is already loaded and converted to RGB in `prepare_image()`. QR detection works best on higher-resolution images, so we detect before downscaling. We'll extract QR detection into a separate function called before `prepare_image()` compresses the image.
**Alternative:** Detect QR on the raw upload bytes — rejected because we already handle HEIC→RGB conversion in the image pipeline.

### 2. Parallel-ish flow: image scan + QR fetch/extract
**Decision:** Run image scan first, then if a QR URL was found, fetch the page and extract data, then merge. Sequential rather than truly parallel since we're in a synchronous Flask handler.
**Rationale:** Simplicity. The image scan typically takes ~1-2s, the URL fetch + extraction another ~1-2s. Total time is acceptable for a user-initiated scan. True parallelism would require threading/async which adds complexity for marginal gain.

### 3. URL content extraction via Claude
**Decision:** Fetch the product page HTML, strip it to text content, and send to Claude Haiku with a prompt similar to the image scan prompt.
**Rationale:** Product pages have varied HTML structures. Using Claude to extract structured data from page text is more robust than writing per-site scrapers. Uses the same model (claude-haiku-4-5) and similar prompt as image extraction.
**Alternative:** HTML parsing with BeautifulSoup — rejected because it requires per-site selectors and is fragile.

### 4. Merge strategy: QR data wins for non-null fields
**Decision:** Start with image scan results as the base, then overwrite with QR-extracted fields where the QR value is not null/empty.
**Rationale:** The product page typically has more complete and accurate data. The image scan serves as a fallback for fields the page doesn't cover. The `matched_roaster` logic from fuzzy matching still applies to the final merged result.

### 5. Fetch page content using urllib
**Decision:** Use Python's built-in `urllib.request` to fetch page content. Parse HTML to extract text using a simple tag-stripping approach or html.parser.
**Rationale:** No new dependencies needed. The pages are simple product pages, not SPAs. We only need the text content for Claude to parse.
**Alternative:** `requests` library — adds a dependency for no significant benefit for this use case.

## Risks / Trade-offs

- **Slow product pages** → Set a short timeout (5s) on URL fetch. If it fails, fall back to image-only scan results.
- **JavaScript-rendered pages** → Won't work. Accept this limitation; most coffee roaster sites are static or server-rendered.
- **QR code points to non-product URL** → Claude will extract what it can; if nothing useful, image scan data is the fallback. No harm done.
- **Extra API cost** → One additional Claude Haiku call per scan when QR is detected. Cost is minimal (~$0.001 per call).
- **Privacy/security** → Only fetch URLs from QR codes the user photographed. Don't follow redirects beyond a reasonable limit. Validate URL scheme is http/https.
