## Context

The Coffee Tracker home screen currently renders a flat list of all coffees ordered by date. Each coffee card shows roaster, name, origin, bean type, tasting notes, price, average score, and an expandable tasting history. This works for a small collection but becomes unwieldy at 30+ entries.

The app is a single-page Flask app with inline JS/CSS in `templates/index.html`. The backend uses SQLite with tables `coffees` and `tastings`. Roastery names already exist as a field on each coffee entry.

## Goals / Non-Goals

**Goals:**
- Make the home screen scannable at a glance for 30+ coffees
- Show recent tasting activity prominently (last 2 tastings across all coffees)
- Group coffees by roastery with emoji identifiers for visual appeal
- Provide a drill-down roastery view with beans and tastings
- Generate roastery emojis via Claude API and cache them persistently

**Non-Goals:**
- Search/filter within roastery views (existing note filter stays as-is)
- Pagination or infinite scroll
- Rewriting the detail panel or tasting modal
- Multi-user support

## Decisions

### 1. Roastery emoji storage: new `roastery_emojis` table

Store emoji mappings in a dedicated table `roastery_emojis(roaster TEXT UNIQUE, emoji TEXT)` rather than adding a column to `coffees`.

**Rationale:** A roaster name can appear on many coffee rows. A separate table avoids duplication and makes lookups/updates simple. The `init_db()` migration path handles table creation.

**Alternative considered:** Column on `coffees` — would require updating all rows for a roaster and complicates emoji retrieval.

### 2. Emoji generation: single Claude API call per roastery

When a new coffee is saved and its roaster has no cached emoji, make a lightweight Claude Haiku call asking for a single emoji that represents the roastery's vibe/origin/name. Cache the result immediately.

**Rationale:** Haiku is fast and cheap. One call per new roastery is negligible. Doing it at save-time means the emoji is ready by the time the home screen reloads.

**Alternative considered:** Batch generation on page load — adds latency and complexity for the user waiting to see results.

### 3. Home screen layout: two sections

Replace `loadCoffees()` rendering with:
1. **Recent Tastings** — fetch last 2 tastings (new API endpoint `GET /api/tastings/recent?limit=2`), render as compact tasting cards with coffee name + roaster context
2. **Roasteries** — fetch roasters + emojis (enhanced `GET /api/roasters` response), render as a button grid

The existing `loadCoffees()` flat list code is replaced entirely. The note filter feature is preserved and applied within the roastery detail view.

### 4. Roastery detail view: inline expansion

When a roastery button is tapped, replace the roastery grid with a back-navigable view showing that roastery's coffees and their tastings inline. Reuses existing coffee card and tasting rendering logic.

**Rationale:** Keeps the single-page feel without adding route navigation. A simple state variable tracks whether we're in "home" or "roastery detail" mode.

**Alternative considered:** Modal/overlay — would feel heavy for a list view; inline replacement is more mobile-friendly.

### 5. API shape for recent tastings

New endpoint `GET /api/tastings/recent?limit=N` returns the N most recent tastings across all coffees, each including `coffee_name` and `coffee_roaster` fields joined from the coffees table.

**Rationale:** The frontend needs coffee context to render recent tastings meaningfully. Joining server-side avoids N+1 fetches.

## Risks / Trade-offs

- **Emoji quality**: Claude may pick suboptimal emojis for some roastery names → Users can live with it; no critical impact. Could add manual override later.
- **API cost**: One Haiku call per new roastery → Negligible cost, and it's cached permanently.
- **Migration**: Existing users see the new layout immediately → No data migration needed, just schema addition for the emoji table. The flat list is gone — this is a deliberate UX change.
