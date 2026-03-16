## Context

The tasting system currently tracks brew type, dosage, score, tasting notes, and comments. Grind level is a missing variable that significantly affects extraction quality. The UI already uses a `<select>` dropdown (spinning wheel on mobile) for dosage, so the same pattern can be reused for grind level.

The grind level needs smart defaults: reuse the last grind setting for a given coffee, or fall back to brew-type-specific defaults for first-time tastings.

## Goals / Non-Goals

**Goals:**
- Add grind level as an optional float field on tastings
- Provide a spinning-wheel selector with 0.2 step increments
- Auto-populate grind level based on previous tastings for the same coffee, or brew-type defaults
- Display grind level in tasting history

**Non-Goals:**
- Grinder-specific profiles or named presets
- Grind level validation against brew type (user may experiment)
- Grind level in scan output or coffee bean model

## Decisions

### Grind level range: 3.0 to 22.0 in 0.2 steps
Covers the practical range from fine espresso (3.0) to coarse French press (22.0). Step size of 0.2 matches common click-based grinder adjustments. This gives 96 options — comfortable in a spinning-wheel selector.

### Default values by brew type
- Espresso: 4.0 (fine grind)
- Brew (pour-over/drip): 14.0 (medium grind)
- Metal Brew (French press/moka): 18.0 (medium-coarse)
- Cappuccino: 4.0 (same as espresso, since it's espresso-based)

These are stored as a JS object in the frontend. No need for backend configuration since defaults are purely a UI concern.

### Smart default: last grind level for same coffee
When opening the tasting modal, if the selected coffee has previous tastings with a grind level, use the most recent one. This requires fetching tastings when a coffee is selected (already available via `GET /api/tastings?coffee_id=<id>`). If no prior grind level exists, fall back to the brew-type default.

The default updates when the user changes brew type (to the brew-type default) unless they've manually changed the grind level.

### DB column: `grind_level REAL`
Added via the existing `init_db()` migration pattern — check if column exists, add if missing. Nullable, consistent with other optional tasting fields.

## Risks / Trade-offs

- **[Grind scales vary across grinders]** → We store an abstract numeric value, not grinder-specific clicks. Users need to know their own mapping. This is acceptable for a personal tracker.
- **[Extra API call for smart defaults]** → Fetching tastings for the selected coffee when the modal opens. This is a lightweight query and the endpoint already exists.
