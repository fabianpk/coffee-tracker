## Why

`CoffeeBean` currently holds `brew_score` and `espresso_score` as flat fields, making it impossible to track how the same coffee performs across multiple tasting sessions at different doses or brew methods. Separating tastings from the coffee record allows scores to accumulate over time and be averaged.

## What Changes

- New `Tasting` model with fields: `coffee_bean_id` (FK), `brew_type` (espresso/brew/etc.), `dosage` (e.g. "15g"), `score` (1–5), `notes`, `created_at`
- **BREAKING**: `CoffeeBean` drops `brew_score` and `espresso_score` — rating is now a computed average of associated `Tasting` records
- New `tastings` table in SQLite; database migration to remove old score columns
- UI top bar gains two buttons: **Scan Coffee** (existing flow) and **Conduct Tasting** (new flow)
- **Conduct Tasting** flow: pick a previously scanned coffee from the DB, enter brew type, dosage, score, and notes, then save

## Capabilities

### New Capabilities

- `tasting-model`: `Tasting` dataclass in `models.py` with DB serialization (`to_row`, `from_row`, `to_dict`) and the new `tastings` table schema
- `tasting-api`: API routes for creating and listing tastings (`POST /api/tastings`, `GET /api/tastings?coffee_id=<id>`) and updated `GET /api/coffees` to include computed average score per coffee
- `tasting-ui`: Frontend "Conduct Tasting" flow — coffee picker, brew type selector, dosage input, score picker, notes; plus tasting history shown per coffee

### Modified Capabilities

- `coffee-bean-model`: Remove `brew_score` and `espresso_score` fields; `to_dict()` gains a computed `average_score` derived from related tastings

## Impact

- `models.py`: new `Tasting` dataclass; updated `CoffeeBean`
- `app.py`: new routes, updated `init_db()` migration, updated scan/save handlers
- `templates/index.html`: redesigned top bar, new tasting modal/form, tasting history per coffee card
- SQLite schema: new `tastings` table; migration to drop `brew_score`/`espresso_score` from `coffees`
