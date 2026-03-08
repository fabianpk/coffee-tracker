## MODIFIED Requirements

### Requirement: CoffeeBean dataclass definition
The system SHALL provide a `CoffeeBean` dataclass in `models.py` with the following properties, all optional (nullable) except `id` and `created_at`:

| Property | Type |
|---|---|
| `id` | `int \| None` (None before DB insert) |
| `roaster` | `str \| None` |
| `name` | `str \| None` |
| `country_grown` | `str \| None` |
| `country_roasted` | `str \| None` |
| `bean_type` | `str \| None` |
| `process` | `str \| None` |
| `roast_level` | `str \| None` |
| `tasting_notes` | `str \| None` |
| `weight` | `str \| None` |
| `price` | `str \| None` |
| `comments` | `str \| None` |
| `created_at` | `str` |

`origin` is removed from the dataclass. The `origin` column remains in the database but is ignored by `from_row()`.

#### Scenario: Create a CoffeeBean with all fields including comments
- **WHEN** a `CoffeeBean` is instantiated with `comments="Great coffee from a Tokyo cafe"` and all other properties set
- **THEN** `comments` SHALL be accessible as a `str | None` attribute with value `"Great coffee from a Tokyo cafe"`

#### Scenario: Create a CoffeeBean with minimal fields
- **WHEN** a `CoffeeBean` is instantiated with only `created_at` set
- **THEN** all other fields (except `created_at`) SHALL default to `None`, including `comments`

#### Scenario: from_row ignores origin column
- **WHEN** `CoffeeBean.from_row(row)` is called on a row that contains an `origin` column
- **THEN** no error SHALL be raised and the `origin` value SHALL be ignored

### Requirement: Route handlers use CoffeeBean
All API route handlers (`POST /api/scan`, `GET /api/coffees`, `POST /api/coffees`, `DELETE /api/coffees/<id>`) SHALL use `CoffeeBean` instances for data handling instead of raw dicts. The `comments` field SHALL be read from `data.get("comments")` in save and update routes.

#### Scenario: Scan endpoint returns CoffeeBean-shaped response
- **WHEN** a POST to `/api/scan` succeeds
- **THEN** the response JSON SHALL include `comments` (not `notes`) alongside other fields

#### Scenario: Save endpoint accepts comments field
- **WHEN** a POST to `/api/coffees` includes `comments`
- **THEN** the `comments` value SHALL be persisted to the database
