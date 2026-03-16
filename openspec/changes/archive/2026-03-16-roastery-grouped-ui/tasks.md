## 1. Database & Schema

- [x] 1.1 Add `roastery_emojis` table creation (`roaster TEXT UNIQUE, emoji TEXT`) to `init_db()` in `app.py`

## 2. Backend API

- [x] 2.1 Add `GET /api/tastings/recent` endpoint that returns the N most recent tastings (default 2) with `coffee_name` and `coffee_roaster` joined from the coffees table
- [x] 2.2 Add emoji generation helper function that calls Claude Haiku with a roastery name and returns a single emoji
- [x] 2.3 Enhance `GET /api/roasters` to return `[{"roaster": "...", "emoji": "..."}]` objects; batch-generate missing emojis on first call
- [x] 2.4 Add emoji generation trigger in `POST /api/coffees` — after saving a coffee, generate and cache emoji for the roaster if not already cached

## 3. Frontend — Home Screen Layout

- [x] 3.1 Add CSS styles for recent tastings section, roastery button grid, and roastery detail view
- [x] 3.2 Replace `loadCoffees()` with new `loadHomeScreen()` function that fetches recent tastings and roastery list, renders the two-section layout
- [x] 3.3 Render recent tastings section with compact tasting cards showing brew type, dosage, grind, score, coffee name, and roaster

## 4. Frontend — Roastery Detail View

- [x] 4.1 Add roastery detail view HTML container with back button header
- [x] 4.2 Implement `openRoastery(roasterName)` that fetches coffees filtered by roaster and renders coffee cards with inline tastings
- [x] 4.3 Implement back navigation from roastery detail to home screen
- [x] 4.4 Wire coffee card taps in roastery view to open existing detail panel

## 5. Integration

- [x] 5.1 Update `loadRoasters()` calls after save/update/delete to refresh home screen instead of flat list
- [x] 5.2 Preserve tasting note filter functionality within the roastery detail view
