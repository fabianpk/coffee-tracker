## Why

All coffee data logic (field definitions, validation, serialization) is scattered across `app.py` — inlined in route handlers, SQL statements, and the Claude prompt. Introducing a `CoffeeBean` model class centralizes this, making it easier to add new fields (like the requested price, brew/espresso scores, and country-level origin tracking) and sets the foundation for a future database abstraction layer.

## What Changes

- **Introduce a `CoffeeBean` dataclass** with typed properties: roaster, name, country_grown, country_roasted, origin (free-text), process, roast_level, tasting_notes, weight, price, brew_score, espresso_score, other, notes.
- **Replace the single `rating` field** with two separate scores: `brew_score` and `espresso_score` (both optional integers). **BREAKING** — existing `rating` column will be migrated to `brew_score`.
- **Add new fields**: `price` (text, e.g. "15.99 EUR"), `country_grown`, `country_roasted`.
- **Add `CoffeeBean` methods** for database serialization (`to_row()` / `from_row()`) so the model owns its own persistence mapping.
- **Update the Claude vision prompt** to extract the new fields (country_grown, country_roasted, price, weight).
- **Update the frontend** to display and edit the new fields (brew score, espresso score, price, country fields).
- **Migrate the SQLite schema** to add new columns and rename `rating` → `brew_score`.

## Capabilities

### New Capabilities
- `coffee-bean-model`: The `CoffeeBean` dataclass with all properties, type annotations, and database serialization methods (`to_row`, `from_row`, `to_dict`).

### Modified Capabilities
_(none — no existing specs)_

## Impact

- **`app.py`** — Route handlers refactored to use `CoffeeBean` instead of raw dicts. DB schema updated with new columns and migration logic.
- **`scan_coffee.py`** — Updated to use `CoffeeBean` for output.
- **`templates/index.html`** — Form fields added/changed for new properties (brew/espresso scores, price, country fields). Display updated accordingly.
- **Database** — Schema migration needed: add columns (`price`, `country_grown`, `country_roasted`, `espresso_score`), rename `rating` → `brew_score`. Existing data preserved.
