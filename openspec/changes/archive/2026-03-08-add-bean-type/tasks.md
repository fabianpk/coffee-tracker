## 1. Model & Database

- [x] 1.1 Add `bean_type: str | None = None` field to `CoffeeBean` dataclass in `models.py` (after `country_roasted`)
- [x] 1.2 Add `bean_type TEXT` column to the `CREATE TABLE IF NOT EXISTS coffees` statement in `init_db()`
- [x] 1.3 Add `"bean_type": "TEXT"` to the `migrations` dict in `init_db()` for existing DB migration

## 2. Claude Vision Prompt

- [x] 2.1 Add `"bean_type": "..."` to the JSON template in the image scan prompt (around line 203)
- [x] 2.2 Add guidance text: "bean_type is the species or variety of the coffee bean (e.g. Arabica, Robusta, Bourbon, Gesha, SL28); list all if multiple; null if not stated"
- [x] 2.3 Add `"bean_type": "..."` to the JSON template in the URL/text scan prompt (around line 238)

## 3. API Routes

- [x] 3.1 Add `bean_type=data.get("bean_type")` to the `CoffeeBean(...)` constructor in `POST /api/coffees` (save route)
- [x] 3.2 Add `bean_type=data.get("bean_type")` to the `CoffeeBean(...)` constructor in the rescan/update route if applicable

## 4. Frontend

- [x] 4.1 Add "Bean Type" input field to the review form in `templates/index.html`
- [x] 4.2 Add bean type display to the coffee card in the list view
- [x] 4.3 Add "Bean Type" field to the detail/edit panel
- [x] 4.4 Wire up bean_type in the JavaScript save/load logic (populate from scan, include in POST body)
