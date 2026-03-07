## 1. QR Code Detection

- [x] 1.1 Add `detect_qr_url(image: Image) -> str | None` function in `app.py` that uses pyzbar to find QR codes in a PIL Image and returns the first valid HTTP/HTTPS URL found (or None)
- [x] 1.2 Update `prepare_image()` to also return the PIL Image object (before JPEG compression) so it can be used for QR detection

## 2. Product Page Fetching and Extraction

- [x] 2.1 Add `fetch_page_text(url: str) -> str | None` function that fetches a URL with urllib (5s timeout), strips HTML tags, and returns text content (or None on failure)
- [x] 2.2 Add `extract_coffee_from_text(text: str) -> dict` function that sends page text to Claude Haiku with a prompt requesting the same structured fields as the image scan

## 3. Merge and Scan Route Integration

- [x] 3.1 Add `merge_scan_results(image_data: dict, qr_data: dict) -> dict` function that merges two scan result dicts, with QR data taking priority for non-null/non-empty fields
- [x] 3.2 Update the `/api/scan` route to: detect QR URL from image, fetch page if URL found, extract data from page, merge with image scan results, and include `qr_url` in response

## 4. Frontend QR Enrichment Indicator

- [x] 4.1 Update the review form in `index.html` to show a small note when `qr_url` is present in the scan response (e.g. "Enriched from product page")
