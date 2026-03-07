## 1. Drop origin field

- [x] 1.1 Remove `origin` from `CoffeeBean` dataclass in `models.py` (from_row already filters to known fields, so old DB rows are handled)
- [x] 1.2 Update `CoffeeBean.from_scan()`: if scan data has `origin` and `country_grown` is empty/null, map `origin` to `country_grown`
- [x] 1.3 Update Claude vision prompt in `app.py`: remove `origin` from JSON template; update `country_grown` instruction to include "country or region where the beans were grown; list all separated by commas if multiple"
- [x] 1.4 Remove origin from frontend: remove `f-origin` and `d-origin` inputs from review form and detail panel; remove origin from `fillForm()`, `DETAIL_TEXT_FIELDS`, coffee card display, and save/update handlers

## 2. Duplicate detection

- [x] 2.1 Add duplicate detection JS: after `fillForm()` populates the review form, check `coffeeCache` for a coffee matching `roaster`+`name` (case-insensitive, trimmed); store matched coffee ID if found
- [x] 2.2 Add duplicate banner HTML and conditional buttons: show info banner "A coffee with this name already exists" and replace "Save" with "Update Existing" / "Save as New" buttons when a duplicate is detected; show normal "Save" when no duplicate
- [x] 2.3 Wire "Update Existing" button: send `PUT /api/coffees/<matched_id>` with form data, close form, reload list
- [x] 2.4 Wire "Save as New" button: check that roaster or name differs from matched coffee before saving; alert if unchanged; otherwise save as normal POST
