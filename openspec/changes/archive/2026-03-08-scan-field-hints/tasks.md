## 1. Hints File

- [x] 1.1 Create `scan_hints.example.md` with example hints for process, bean_type, country_grown, roast_level, and other fields
- [x] 1.2 Add `scan_hints.md` to `.gitignore`

## 2. Load and Inject Hints

- [x] 2.1 Add a `load_scan_hints()` helper function in `app.py` that reads `scan_hints.md`, returns empty string if missing/empty, and truncates to 2000 chars
- [x] 2.2 Append loaded hints to the prompt in `extract_coffee_details()` (image scan)
- [x] 2.3 Append loaded hints to the prompt in `extract_coffee_from_text()` (text/URL scan)
