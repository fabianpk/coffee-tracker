## Context

Coffee Tracker is a single-page Flask app with an inline JS frontend. The home screen shows roasteries, and drilling into a roastery shows individual coffees with their tastings. There is no cross-roastery summary of ratings. The app uses SQLite with `coffees` and `tastings` tables, where tastings have `brew_type` and `score` fields.

## Goals / Non-Goals

**Goals:**
- Provide a single-screen overview of all rated coffees grouped by roastery with average scores
- Allow filtering by brew type to compare coffees within a specific preparation method
- Keep the UI consistent with the existing dark theme, card-based layout

**Non-Goals:**
- Advanced charting or graphing (simple list/card layout is sufficient)
- Sorting controls or custom ordering
- Export functionality
- Per-tasting drill-down from the stats view

## Decisions

1. **Single SQL query with GROUP BY coffee + brew type** — Aggregation happens server-side in one query joining `coffees` and `tastings`, grouped by `(coffee_id, brew_type)`. This keeps the frontend simple and avoids N+1 queries. Alternative: client-side aggregation from existing endpoints — rejected because it would require fetching all tastings.

2. **Brew type filter via query parameter** — The `/api/stats?brew_type=espresso` pattern keeps filtering server-side for efficiency. The frontend populates a dropdown from available brew types returned alongside the data.

3. **View toggling pattern** — Follows the existing `home-view` / `roastery-detail-view` show/hide pattern rather than introducing a router. The stats view is a peer-level div that hides the others when active.

4. **Weighted roastery average** — Each roastery header shows a weighted average (by tasting count) rather than a simple mean of per-coffee averages, giving more weight to frequently tasted coffees.

## Risks / Trade-offs

- **[No pagination]** → Acceptable for personal use; unlikely to have thousands of rated coffees.
- **[Brew type shown per row when unfiltered]** → When viewing all brew types, the same coffee may appear multiple times (once per brew type). This is intentional to show how a coffee performs differently across methods.
