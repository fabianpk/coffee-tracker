## Context

The tasting modal currently has two brew type buttons: "Espresso" and "Brew". The `brew_type` field is stored as free-text in SQLite, so no backend or schema changes are needed. The buttons are hardcoded in `templates/index.html`.

## Goals / Non-Goals

**Goals:**
- Add "Metal Brew" and "Cappuccino" as brew type options
- Display an emoji alongside each brew type in the selector buttons and tasting history
- Keep the UI clean with four options in a responsive button row

**Non-Goals:**
- Making brew types user-configurable or stored in the database
- Changing the backend API or data model
- Adding icons/images beyond native Unicode emojis

## Decisions

**Hardcoded emoji mapping in the frontend**: Define a JS object mapping brew type values to their emoji+label. This keeps all brew type config in one place and avoids backend changes. The same mapping is used for both the button rendering and tasting history display.

**Emoji choices**: Use widely-supported Unicode emojis that visually represent each method:
- Espresso → coffee emoji (representing a shot)
- Brew → pour-over/filter emoji
- Metal Brew → a metallic/industrial representation
- Cappuccino → a milk-based drink representation

Final emoji selection will be determined during implementation based on what renders well across platforms.

**Store display name as brew_type value**: Store values like `"espresso"`, `"brew"`, `"metal_brew"`, `"cappuccino"` (lowercase, underscore-separated) so they remain stable identifiers. The emoji is purely a display concern, looked up from the mapping at render time.

## Risks / Trade-offs

- **Emoji rendering varies by platform** → Using common, widely-supported emojis minimizes this. All target emojis are in Unicode 6.0+.
- **Four buttons may be tight on small screens** → The existing flex layout handles wrapping; buttons can shrink. May need slightly smaller font or allow wrapping to two rows.
- **Existing tastings with "espresso"/"brew" values** → These match the new mapping keys exactly, so no migration needed.
