## Context

The `CoffeeBean` dataclass currently has 12 optional properties covering roaster, origin, process, tasting notes, etc. Bean type/variety (e.g., Arabica, Robusta, Bourbon, Gesha) is a common attribute printed on specialty coffee bags but is not captured. The existing architecture follows a straightforward pattern: dataclass field → DB column → Claude prompt field → frontend form field.

## Goals / Non-Goals

**Goals:**
- Add `bean_type` as a new property on `CoffeeBean` that captures the species/variety of the coffee bean
- Auto-extract bean type from bag photos via the Claude vision prompt
- Allow manual entry/editing of bean type in the frontend
- Seamlessly migrate existing databases (new column, NULL for existing rows)

**Non-Goals:**
- No validation or enumeration of allowed bean types — free-text field, since varieties are numerous and often combined (e.g., "Arabica / Bourbon")
- No filtering or search by bean type (can be added later)
- No changes to the Tasting model or tasting workflow

## Decisions

**1. Free-text field, not an enum**
Bean types span species (Arabica, Robusta, Liberica) and varieties (Bourbon, Typica, Gesha, SL28, Catimor, etc.). Bags often list multiple or use non-standard names. A free-text `str | None` field is simplest and most flexible.
- *Alternative*: Predefined enum with "Other" option — rejected because it would require ongoing maintenance and limit scan accuracy.

**2. Add `bean_type` after `country_roasted` in field order**
Placing it after country fields and before process groups it logically with origin-related properties: where it's from → what variety → how it's processed.

**3. Use existing migration pattern in `init_db()`**
Add `"bean_type": "TEXT"` to the `migrations` dict in `init_db()`. This is the established pattern — it checks existing columns via `PRAGMA table_info` and adds missing ones. Zero risk to existing data.

**4. Include `bean_type` in the Claude vision prompt JSON template**
Add `"bean_type": "..."` to the JSON template string with a guidance note: "bean_type is the species or variety of the coffee bean (e.g. Arabica, Robusta, Bourbon, Gesha, SL28). List all if multiple." This follows the same pattern as `country_grown`.

## Risks / Trade-offs

- **[Scan accuracy]** Not all bags explicitly list bean type → Claude may return null or guess. Mitigation: field is optional and editable; prompt instructs to only extract if stated.
- **[Schema migration]** Adding a column to existing DBs → Mitigation: uses proven `ALTER TABLE ADD COLUMN` pattern already in place; new column defaults to NULL.
