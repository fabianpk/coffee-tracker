## 1. Vision Model Upgrade

- [x] 1.1 Change model from `claude-haiku-4-5-20251001` to `claude-sonnet-4-6` in `extract_coffee_details()` in `app.py`
- [x] 1.2 Change model from `claude-haiku-4-5-20251001` to `claude-sonnet-4-6` in `extract_coffee_from_text()` in `app.py`

## 2. Remove "Other" from Model and Database

- [x] 2.1 Remove `other` property from `CoffeeBean` dataclass in `models.py`
- [x] 2.2 Remove `other` column from the `CREATE TABLE coffees` statement in `init_db()` in `app.py`
- [x] 2.3 Remove `other` from `save_coffee()` and `update_coffee()` in `app.py` (stop reading it from request payload)

## 3. Remove "Other" from Frontend

- [x] 3.1 Remove `other` from the review form save payload and remove the `other` key from the scan-fill loop in `templates/index.html`
- [x] 3.2 Remove the "Other (markdown)" textarea and its display from the detail/edit panel
- [x] 3.3 Remove `other` rendering (the `other-md` div) from the coffee list cards
- [x] 3.4 Keep the "Other (from scan)" readonly textarea in the review form as ephemeral scan reference

## 4. Update Notes Placeholder Text

- [x] 4.1 Change placeholder on `f-notes` textarea in the review form from "How was it?" to "Other notes"
- [x] 4.2 Change placeholder on `d-notes` textarea in the detail/edit panel from "How was it?" to "Other notes"
