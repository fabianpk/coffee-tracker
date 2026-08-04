## 1. Backend API

- [x] 1.1 Add `GET /api/stats` route to `app.py` that joins `coffees` and `tastings`, groups by `(coffee_id, brew_type)`, and returns `roaster`, `name`, `brew_type`, `avg_score`, `tasting_count` ordered by roaster then score descending
- [x] 1.2 Support optional `?brew_type=` query parameter to filter results to a single brew type
- [x] 1.3 Return `brew_types` array alongside `entries` containing all distinct brew types from the tastings table

## 2. Frontend Stats View

- [x] 2.1 Add a "Stats" button to the top button bar in `templates/index.html`
- [x] 2.2 Add `#stats-view` HTML section with back button, brew type filter dropdown, and content container
- [x] 2.3 Implement `openStats()` JS function that fetches `/api/stats`, groups entries by roaster, and renders card-based layout with weighted roastery averages
- [x] 2.4 Wire brew type dropdown change event to re-fetch and re-render stats with filter applied
- [x] 2.5 Hide brew type display on individual entries when a brew type filter is active

## 3. Navigation Integration

- [x] 3.1 Wire stats back button to hide stats view and show home view
- [x] 3.2 Update `loadHomeScreen()` to hide stats view when returning to home
