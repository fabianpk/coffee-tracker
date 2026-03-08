## 1. Update Scan Prompts

- [x] 1.1 Update tasting_notes instruction in `extract_coffee_details()` to request comma-separated list instead of "copy exact words"
- [x] 1.2 Update tasting_notes instruction in `extract_coffee_from_text()` to request comma-separated list
- [x] 1.3 Update tasting_notes instruction in `scan_coffee.py` CLI to match

## 2. Add tasting_notes to Tasting Model

- [x] 2.1 Add `tasting_notes: str | None` to `Tasting` dataclass in `models.py`
- [x] 2.2 Add `tasting_notes TEXT` column to `CREATE TABLE tastings` in `init_db()`
- [x] 2.3 Update `save_tasting()` route to read `tasting_notes` from request payload

## 3. Add Filter API

- [x] 3.1 Add `?note=` query parameter support to `GET /api/coffees` with case-insensitive matching of individual notes
- [x] 3.2 Add `GET /api/tasting-notes` endpoint that returns sorted unique tasting notes across all coffees

## 4. Frontend: Tag Display

- [x] 4.1 Render tasting notes as individual tag chips on coffee cards instead of a single text line
- [x] 4.2 Style tags with the coffee theme (brown tones, pill shape)

## 5. Frontend: Filter by Note

- [x] 5.1 Make tasting note tags clickable — clicking filters the coffee list via `?note=` API parameter
- [x] 5.2 Add active filter indicator bar with note name and clear button
- [x] 5.3 Clear filter restores full coffee list

## 6. Frontend: Tasting Modal Update

- [x] 6.1 Add tasting notes input to Conduct Tasting modal with placeholder "e.g. Chocolate, Berry, Citrus"
- [x] 6.2 Display tasting notes as tags in tasting history entries
