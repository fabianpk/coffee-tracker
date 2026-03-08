## Why

Coffee beans come in different species and varieties (e.g., Arabica, Robusta, Bourbon, Gesha) which significantly affect flavor and price. This information is often printed on coffee bags but isn't captured by the scanner or stored in the database, making it impossible to track or filter by bean type.

## What Changes

- Add a `bean_type` property to the `CoffeeBean` dataclass (`str | None`)
- Update the Claude vision prompt to extract bean type/variety from bag photos
- Add the `bean_type` column to the SQLite database (with auto-migration for existing DBs)
- Add a bean type input field to the frontend review form and detail panel
- Display bean type on coffee cards in the list view

## Capabilities

### New Capabilities

### Modified Capabilities
- `coffee-bean-model`: Add `bean_type` property to the CoffeeBean dataclass, update serialization methods, and update the Claude vision prompt to extract bean type

## Impact

- **`models.py`** — New `bean_type` field on `CoffeeBean` dataclass
- **`app.py`** — Updated Claude vision prompt to request `bean_type`; `init_db()` migration to add column to existing databases
- **`templates/index.html`** — New form field and display element for bean type
- **Database** — New `bean_type TEXT` column in the `coffees` table
