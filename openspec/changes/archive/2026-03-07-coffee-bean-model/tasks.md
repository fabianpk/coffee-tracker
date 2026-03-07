## 1. CoffeeBean Model

- [x] 1.1 Create `models.py` with `CoffeeBean` dataclass — all properties from spec, defaults to `None`
- [x] 1.2 Add `to_row()` method returning a dict of column names to values (excluding `id`)
- [x] 1.3 Add `from_row(row)` classmethod accepting a `sqlite3.Row` and returning a `CoffeeBean`
- [x] 1.4 Add `to_dict()` method returning a JSON-serializable dict (including `id`)
- [x] 1.5 Add `from_scan(data)` classmethod mapping scan output dict to `CoffeeBean` (map `roastery` → `roaster`)

## 2. Database Migration

- [x] 2.1 Update `init_db()` in `app.py` to create the `coffees` table with all new columns (use `roaster` instead of `roastery`, add `country_grown`, `country_roasted`, `price`, `brew_score`, `espresso_score`)
- [x] 2.2 Add migration logic: detect old schema via `PRAGMA table_info`, add missing columns with `ALTER TABLE`, copy `rating` → `brew_score` if applicable

## 3. Route Handlers

- [x] 3.1 Update `extract_coffee_details()` prompt to request `country_grown`, `country_roasted`, and `price` fields
- [x] 3.2 Refactor `POST /api/scan` to return scan result through `CoffeeBean.from_scan()` → `to_dict()`
- [x] 3.3 Refactor `POST /api/coffees` to construct `CoffeeBean` from request JSON and use `to_row()` for insert
- [x] 3.4 Refactor `GET /api/coffees` to use `CoffeeBean.from_row()` → `to_dict()` for each row
- [x] 3.5 Update `scan_coffee.py` CLI to use `CoffeeBean` for output

## 4. Frontend

- [x] 4.1 Add form fields for `country_grown`, `country_roasted`, and `price` in the review form
- [x] 4.2 Replace single rating buttons with two sets: "Brew Score" and "Espresso Score" (both 1-5 star buttons)
- [x] 4.3 Update `fillForm()` to populate new fields from scan response
- [x] 4.4 Update save handler to send new fields (`brew_score`, `espresso_score`, `price`, `country_grown`, `country_roasted`)
- [x] 4.5 Update coffee list display to show both scores with labels and price
