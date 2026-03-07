## Why

Coffee bags often include QR codes linking to product pages with much richer information than what's printed on the label (altitude, varieties, detailed tasting notes, pricing). Currently the scan flow only uses Claude vision on the bag photo, missing this valuable data source. By detecting and following QR codes during the existing scan flow, we can extract significantly more detailed coffee information without any extra user effort.

## What Changes

- Detect QR codes in uploaded coffee bag photos using pyzbar (already a dependency)
- If a QR code containing a URL is found, fetch the linked product page content
- Send the page content to Claude for structured extraction (same fields as image scan)
- Merge QR-sourced data with image scan results, with QR/URL data taking priority for fields it provides
- No UI changes — QR detection is integrated into the existing "Scan Coffee" button flow

## Capabilities

### New Capabilities
- `qr-code-scan`: Detecting QR codes in uploaded images, fetching linked product pages, extracting coffee details from page content, and merging with image-based scan results

### Modified Capabilities
- `scan-dedup`: The scan endpoint response may now include a `qr_url` field indicating data was enriched from a product page

## Impact

- **`app.py`**: New functions for QR detection, URL fetching, and page content extraction. Modified `/api/scan` route to orchestrate the combined flow.
- **Dependencies**: `pyzbar` (already installed), no new dependencies needed. System library `libzbar0` must be available.
- **Claude API**: Additional API call when a QR code URL is found (page content extraction alongside image extraction).
