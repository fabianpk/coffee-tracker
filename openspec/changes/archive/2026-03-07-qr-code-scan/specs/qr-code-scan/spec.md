## ADDED Requirements

### Requirement: QR code detection from uploaded image
The system SHALL attempt to detect QR codes in the uploaded coffee bag image during the scan flow. Detection SHALL use pyzbar on the RGB-converted PIL Image before JPEG compression. Only QR codes containing HTTP or HTTPS URLs SHALL be considered valid.

#### Scenario: Image contains a QR code with a URL
- **WHEN** a coffee bag photo is uploaded that contains a QR code encoding `https://example.com/coffee/123`
- **THEN** the system SHALL extract the URL and proceed to fetch the product page

#### Scenario: Image contains a QR code without a URL
- **WHEN** a coffee bag photo contains a QR code encoding plain text (not a URL)
- **THEN** the QR code SHALL be ignored and the scan SHALL proceed with image-only extraction

#### Scenario: Image contains no QR code
- **WHEN** a coffee bag photo contains no detectable QR code
- **THEN** the scan SHALL proceed with image-only extraction as before

#### Scenario: Image contains multiple QR codes
- **WHEN** a coffee bag photo contains multiple QR codes
- **THEN** the system SHALL use the first QR code that contains a valid HTTP/HTTPS URL

### Requirement: Product page fetching
The system SHALL fetch the HTML content of the URL extracted from a QR code. The fetch SHALL use a timeout of 5 seconds. Only `http` and `https` URL schemes SHALL be followed.

#### Scenario: Product page fetches successfully
- **WHEN** the QR code URL points to an accessible product page
- **THEN** the system SHALL retrieve the page HTML content for extraction

#### Scenario: Product page fetch times out
- **WHEN** the QR code URL does not respond within 5 seconds
- **THEN** the system SHALL fall back to image-only scan results without error

#### Scenario: Product page fetch fails
- **WHEN** the QR code URL returns an HTTP error or connection fails
- **THEN** the system SHALL fall back to image-only scan results without error

### Requirement: Coffee data extraction from product page
The system SHALL send the text content of the fetched product page to Claude Haiku for structured data extraction. The extraction prompt SHALL request the same fields as the image scan prompt (roastery, name, country_grown, country_roasted, process, roast_level, tasting_notes, weight, price, other).

#### Scenario: Product page contains coffee details
- **WHEN** a product page with coffee information is sent to Claude
- **THEN** Claude SHALL return structured JSON with the same fields as an image scan

#### Scenario: Product page contains no useful coffee data
- **WHEN** a product page with no recognizable coffee information is sent to Claude
- **THEN** Claude SHALL return null for fields it cannot determine

### Requirement: Merge image and QR scan results
When both image scan and QR/URL scan produce results, the system SHALL merge them. For each field, the QR/URL-sourced value SHALL take priority over the image-sourced value when the QR/URL value is not null or empty. The merged result SHALL then go through existing roastery matching logic.

#### Scenario: QR data supplements image data
- **WHEN** image scan returns `tasting_notes: null` and QR scan returns `tasting_notes: "Blackberry, Citrus"`
- **THEN** the merged result SHALL have `tasting_notes: "Blackberry, Citrus"`

#### Scenario: QR data overrides image data
- **WHEN** image scan returns `price: "120 kr"` and QR scan returns `price: "139 kr"`
- **THEN** the merged result SHALL have `price: "139 kr"` (QR data takes priority)

#### Scenario: Image data used as fallback
- **WHEN** QR scan returns `roastery: null` and image scan returns `roastery: "Koppar"`
- **THEN** the merged result SHALL have `roastery: "Koppar"`

### Requirement: Scan response includes QR URL
When a QR code URL is detected and used for extraction, the scan API response SHALL include a `qr_url` field with the URL value. When no QR code is detected, `qr_url` SHALL be null.

#### Scenario: QR URL included in response
- **WHEN** a scan detects a QR code with URL `https://example.com/coffee`
- **THEN** the API response SHALL include `"qr_url": "https://example.com/coffee"`

#### Scenario: No QR URL in response
- **WHEN** a scan detects no QR code
- **THEN** the API response SHALL include `"qr_url": null`
