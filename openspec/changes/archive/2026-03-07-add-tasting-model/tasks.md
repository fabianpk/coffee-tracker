## 1. Database & Model

- [x] 1.1 Add `Tasting` dataclass to `models.py` with `id`, `coffee_id`, `brew_type`, `dosage`, `score`, `notes`, `created_at`; implement `to_row()`, `from_row()`, `to_dict()`
- [x] 1.2 Add `CREATE TABLE IF NOT EXISTS tastings` to `init_db()` in `app.py`
- [x] 1.3 Update `CoffeeBean` dataclass: remove `brew_score` and `espresso_score` fields
- [x] 1.4 Update `CoffeeBean.to_row()` to exclude `brew_score`/`espresso_score`
- [x] 1.5 Update `CoffeeBean.from_row()` to silently ignore `brew_score`/`espresso_score` columns
- [x] 1.6 Update `CoffeeBean.to_dict()` to accept and include `average_score`, remove `brew_score`/`espresso_score`

## 2. API Routes

- [x] 2.1 Add `POST /api/tastings` route: validate `coffee_id`, save `Tasting`, return 201 with tasting JSON
- [x] 2.2 Add `GET /api/tastings` route: accept `coffee_id` query param, return tastings ordered by `created_at` DESC
- [x] 2.3 Update `GET /api/coffees` to compute `average_score` per coffee via `SELECT AVG(score) FROM tastings WHERE coffee_id=?` and include it in each coffee's dict

## 3. Frontend

- [x] 3.1 Replace the single scan button in the header with two buttons: "Scan Coffee" and "Conduct Tasting"
- [x] 3.2 Add "Conduct Tasting" modal HTML: coffee dropdown, brew type selector (Espresso / Brew buttons), dosage dropdown (10.0–20.0gr in 0.1gr increments), score picker (1–5), notes textarea, Save and Cancel buttons
- [x] 3.3 Add JS to populate the coffee dropdown from `GET /api/coffees` when the modal opens
- [x] 3.4 Add JS to submit the tasting form to `POST /api/tastings` and close modal on success
- [x] 3.5 Update coffee card to display `average_score` (show "–" if null); remove individual `brew_score`/`espresso_score` display
- [x] 3.6 Add collapsible tasting history section to each coffee card; fetch from `GET /api/tastings?coffee_id=<id>` on expand; show brew type, dosage, score, notes, date per entry; show "No tastings yet" if empty
