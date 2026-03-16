## 1. Model & Database

- [x] 1.1 Add `grind_level: float | None = None` field to the `Tasting` dataclass in `models.py` (between `dosage` and `score`)
- [x] 1.2 Add `grind_level REAL` column to the `CREATE TABLE tastings` statement in `init_db()`
- [x] 1.3 Add migration in `init_db()` to add `grind_level` column to existing `tastings` tables

## 2. API

- [x] 2.1 Update `save_tasting()` to read `grind_level` from request JSON and pass to `Tasting` constructor
- [x] 2.2 Update `update_tasting()` to read `grind_level` from request JSON and include in update

## 3. Frontend - Tasting Modal

- [x] 3.1 Add grind-level `<select>` element to tasting modal HTML (same style as dosage), with values 3.0–22.0 in 0.2 steps
- [x] 3.2 Define `GRIND_DEFAULTS` object mapping brew types to default grind levels (espresso: 4.0, brew: 14.0, metal_brew: 18.0, cappuccino: 4.0)
- [x] 3.3 Implement smart default logic: on coffee selection, fetch tastings and set grind level from most recent tasting's `grind_level`; if none, use brew-type default
- [x] 3.4 Update brew-type button handler to set grind-level default when no prior grind level exists and user hasn't manually changed it
- [x] 3.5 Reset grind-level selector when opening the modal in create mode
- [x] 3.6 Include `grind_level` in the tasting save payload (POST and PUT)

## 4. Frontend - Tasting History & Edit

- [x] 4.1 Display grind level in tasting history entries (e.g., "grind 6.4") when present
- [x] 4.2 Pre-populate grind-level selector when editing an existing tasting
