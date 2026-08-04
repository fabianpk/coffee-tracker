## Why

Users have no way to get a quick overview of how they've rated their coffees across roasteries and brew methods. Currently, ratings are only visible by drilling into individual coffees within a roastery. A statistical summary view lets users compare coffees at a glance, spot favorites, and filter by brew type to see which coffees perform best for each preparation method.

## What Changes

- Add a new `/api/stats` backend endpoint that aggregates tasting scores per coffee and brew type, grouped by roastery
- Add a "Stats" view in the frontend accessible from a new top-level button alongside "Add Coffee to Database" and "Conduct Tasting"
- The stats view shows coffees grouped by roastery with average scores, filterable by brew type via a dropdown
- Each roastery section displays a weighted average score and lists individual coffees with their name, average score, brew type (when not filtered), and tasting count

## Capabilities

### New Capabilities
- `stats-api`: Backend API endpoint for aggregating and filtering tasting statistics by brew type
- `stats-view`: Frontend view showing rated coffees grouped by roastery with average scores and brew type filtering

### Modified Capabilities

## Impact

- **`app.py`**: New `/api/stats` route added before the lookup routes
- **`templates/index.html`**: New "Stats" button in top button bar, new `#stats-view` div with brew type filter dropdown, new JS functions for fetching/rendering stats and managing view visibility
- **Navigation**: `loadHomeScreen()` updated to hide stats view when returning to home
