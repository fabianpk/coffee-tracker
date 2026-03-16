## Why

The main coffee list will become cluttered and hard to navigate once 30+ coffees are scanned. Grouping by roastery with emoji identifiers makes the home screen scannable at a glance, while keeping recent tastings prominent for quick reference.

## What Changes

- Replace the flat coffee list on the home screen with a new layout:
  1. **Recent Tastings** section showing the last 2 tastings (across all coffees) at the top
  2. **Roastery buttons** below, one per roastery, each with an LLM-generated emoji
- Clicking a roastery button opens a view showing that roastery's beans and their associated tastings
- New backend endpoint to generate/cache roastery emojis via Claude API
- Roastery emoji is generated once when a roastery first appears and stored for reuse

## Capabilities

### New Capabilities
- `roastery-home-view`: Home screen layout with recent tastings section and roastery button grid replacing the flat coffee list
- `roastery-emoji`: LLM-based emoji assignment for roasteries, cached in the database
- `roastery-detail-view`: Drill-down view showing a roastery's beans and their tastings when a roastery button is tapped

### Modified Capabilities
- `tasting-api`: Add endpoint for fetching recent tastings across all coffees (not filtered by coffee_id)

## Impact

- **`templates/index.html`** — Major rewrite of coffee list rendering JS; new roastery view section and CSS
- **`app.py`** — New API endpoints: recent tastings, roastery emoji generation/retrieval
- **SQLite schema** — New `roastery_emojis` table (or column on coffees) to cache emoji assignments
- **Claude API** — Additional (small) API calls for emoji generation on new roasteries
