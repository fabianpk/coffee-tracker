## 1. Rename in Models

- [x] 1.1 Rename `notes` → `comments` on `CoffeeBean` dataclass in `models.py`
- [x] 1.2 Rename `notes` → `comments` on `Tasting` dataclass in `models.py`

## 2. Rename in Database Schema

- [x] 2.1 Rename `notes` → `comments` in `CREATE TABLE coffees` in `init_db()` in `app.py`
- [x] 2.2 Rename `notes` → `comments` in `CREATE TABLE tastings` in `init_db()` in `app.py`

## 3. Rename in API Routes

- [x] 3.1 Update `save_coffee()` and `update_coffee()` to read `comments` from request payload
- [x] 3.2 Update `save_tasting()` to read `comments` from request payload

## 4. Rename in Frontend

- [x] 4.1 Rename `f-notes` → `f-comments` in review form HTML and JS; update label to "General Comments" and placeholder to "General comments"
- [x] 4.2 Rename `d-notes` → `d-comments` in detail panel HTML and JS; update label to "General Comments" and placeholder to "General comments"
- [x] 4.3 Rename `t-notes` → `t-comments` in tasting modal HTML and JS; update label to "General Comments"
- [x] 4.4 Update `DETAIL_TEXT_FIELDS` array: `notes` → `comments`
- [x] 4.5 Update `getFormCoffee()` to use `comments` key
- [x] 4.6 Update coffee card rendering to use `c.comments` instead of `c.notes`
- [x] 4.7 Update tasting history rendering to use `t.comments` instead of `t.notes`
