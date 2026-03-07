## Context

Coffee Tracker currently handles all data as raw dicts — the Claude API returns JSON, route handlers pass dicts to SQLite, and the frontend sends/receives plain objects. There is no central definition of what a "coffee" is, making it error-prone to add fields and hard to validate data.

The SQLite schema has a single `rating` integer. The user wants two separate scores (brew and espresso) plus new fields: `price`, `country_grown`, `country_roasted`.

## Goals / Non-Goals

**Goals:**
- Introduce a `CoffeeBean` dataclass in a new `models.py` module
- Centralize field definitions, types, and defaults in one place
- Provide serialization methods for database and API boundaries
- Add new fields: `price`, `country_grown`, `country_roasted`, `brew_score`, `espresso_score`
- Migrate existing data (map `rating` → `brew_score`)

**Non-Goals:**
- A full ORM or database abstraction layer (planned for later)
- Changing the API contract shape significantly — the JSON keys stay similar
- Adding validation beyond basic types (no price parsing, no score range enforcement at model level)

## Decisions

### 1. Python dataclass in a new `models.py` file
**Choice:** Use `@dataclass` from stdlib, not Pydantic or SQLAlchemy.
**Rationale:** The project is intentionally lightweight (Flask + raw SQLite). A stdlib dataclass adds zero dependencies and is sufficient for a typed container with serialization helpers. Pydantic would be overkill for the current scope.

### 2. Scores as optional integers (1-5)
**Choice:** `brew_score: int | None` and `espresso_score: int | None`, replacing the single `rating`.
**Rationale:** Users may only brew filter or only pull espresso for a given bag. Both being optional allows scoring one or both. The 1-5 scale stays the same as the current rating.

### 3. Price as a text field
**Choice:** Store `price` as `TEXT` in SQLite and `str | None` on the model.
**Rationale:** Coffee prices come in various currencies and formats ("15.99 EUR", "$12", "120 SEK"). Parsing into a numeric + currency pair adds complexity with little immediate benefit. Text is flexible and matches what the Claude API will extract from bag photos.

### 4. Schema migration via `init_db()` column detection
**Choice:** On startup, check for missing columns with `PRAGMA table_info` and `ALTER TABLE ADD COLUMN` for each. Rename `rating` → `brew_score` by adding `brew_score`, copying data, and leaving `rating` in place (SQLite doesn't support DROP COLUMN in older versions cleanly).
**Rationale:** No migration framework to maintain. The app is single-user with a small SQLite DB. This is simple and robust for the current scale.

### 5. Keep `origin` alongside new country fields
**Choice:** Retain the existing `origin` free-text field and add `country_grown` and `country_roasted` as separate fields.
**Rationale:** `origin` captures region-level detail ("Yirgacheffe, Ethiopia") that doesn't fit neatly into just a country. The new country fields enable structured filtering later. The Claude prompt will populate all three.

## Risks / Trade-offs

- **[Migration edge case]** If the user has never run the old schema, migration code runs harmlessly (columns don't exist to copy). → Mitigation: check column existence before copying.
- **[Frontend complexity]** Two score inputs instead of one adds UI surface area. → Mitigation: keep the same star-button pattern, just side-by-side with labels.
- **[Prompt extraction quality]** Claude may not reliably extract `country_roasted` from bag photos (many bags don't show it). → Mitigation: all new fields are optional/nullable.
