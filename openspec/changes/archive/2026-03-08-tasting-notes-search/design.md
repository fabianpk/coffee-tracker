## Context

Tasting notes on `CoffeeBean` are stored as a single `tasting_notes TEXT` column in SQLite. The Claude scan prompt currently says "copy the exact words from the bag" which produces inconsistent formats (e.g. "Björnbär / Röd Grapefrukt / Tranbär" with `/` separators). The `Tasting` model has no `tasting_notes` field at all. This change assumes `rename-notes-to-comments` has been applied (so `notes` → `comments` is done).

## Goals / Non-Goals

**Goals:**
- Enable filtering the coffee list by individual tasting note
- Normalize tasting notes to a consistent comma-separated format via scan prompt
- Display notes as individual clickable tags in the UI
- Add `tasting_notes` to the Tasting model so individual tastings can record flavors
- Add tasting notes input to the Conduct Tasting modal

**Non-Goals:**
- Separate junction table for tasting notes
- Auto-correcting or deduplicating similar notes
- Full-text search across all fields
- Aggregating tasting-level tasting_notes back to the coffee level

## Decisions

### 1. Storage: Keep TEXT column, comma-separated

**Choice**: Keep `tasting_notes` as TEXT with comma-separated values on both CoffeeBean and Tasting. No junction table.

**Rationale**: Simple, sufficient for personal collection scale. SQLite LIKE queries work fine for hundreds of entries.

### 2. Search: SQL LIKE on GET /api/coffees

**Choice**: Add `?note=` query parameter using SQL pattern matching against individual notes in the comma-separated string.

**Rationale**: No new dependencies. Handles boundary matching (start of string, between commas, end of string).

### 3. Scan prompt: Request comma-separated output

**Choice**: Update both scan prompts to say "Return tasting notes as a comma-separated list" instead of "copy exact words."

**Rationale**: Produces consistent format directly usable for search.

### 4. Frontend: Clickable tag chips

**Choice**: Render tasting notes as individual clickable tag chips. Clicking a tag filters the list.

**Rationale**: Makes search discoverable — users click any note to find similar coffees.

### 5. Tasting model: Add tasting_notes field

**Choice**: Add `tasting_notes: str | None` to `Tasting` dataclass and `tasting_notes TEXT` column to `tastings` table.

**Rationale**: Individual brew tastings should record what flavors were detected, separate from general comments.

## Risks / Trade-offs

- **[Existing data inconsistency]** Old coffee entries may use `/` or other separators → Alpha project, DB can be wiped
- **[LIKE query performance]** Pattern matching on TEXT → Fine for hundreds of entries
- **[Case sensitivity]** → Use case-insensitive matching
