### Requirement: CoffeeBean dataclass definition
The system SHALL provide a `CoffeeBean` dataclass in `models.py` with the following properties, all optional (nullable) except `id` and `created_at`:

| Property | Type |
|---|---|
| `id` | `int \| None` (None before DB insert) |
| `roaster` | `str \| None` |
| `name` | `str \| None` |
| `country_grown` | `str \| None` |
| `country_roasted` | `str \| None` |
| `origin` | `str \| None` |
| `process` | `str \| None` |
| `roast_level` | `str \| None` |
| `tasting_notes` | `str \| None` |
| `weight` | `str \| None` |
| `price` | `str \| None` |
| `other` | `str \| None` |
| `notes` | `str \| None` |
| `created_at` | `str` |

`brew_score` and `espresso_score` are removed from the dataclass. Scores are now tracked via `Tasting` records.

#### Scenario: Create a CoffeeBean with all fields
- **WHEN** a `CoffeeBean` is instantiated with all properties set
- **THEN** all properties SHALL be accessible as typed attributes

#### Scenario: Create a CoffeeBean with minimal fields
- **WHEN** a `CoffeeBean` is instantiated with only `created_at` set
- **THEN** all other fields (except `created_at`) SHALL default to `None`

### Requirement: CoffeeBean database serialization
The `CoffeeBean` class SHALL provide methods to convert to and from database rows.

- `to_row()` SHALL return a dict of column names to values suitable for SQL INSERT. It SHALL NOT include `brew_score` or `espresso_score`.
- `from_row(row)` SHALL be a classmethod that accepts a `sqlite3.Row` and returns a `CoffeeBean` instance. It SHALL silently ignore any `brew_score`/`espresso_score` columns present in old rows.
- `to_dict()` SHALL return a dict suitable for JSON serialization. It SHALL include `average_score` (passed in as a parameter or defaulting to `None`) but NOT `brew_score` or `espresso_score`.

#### Scenario: Round-trip through to_row and from_row
- **WHEN** a `CoffeeBean` is converted via `to_row()`, inserted into the database, read back as a `sqlite3.Row`, and converted via `CoffeeBean.from_row(row)`
- **THEN** the resulting `CoffeeBean` SHALL have identical property values to the original (except `id`, which is assigned by the database)

#### Scenario: to_dict produces JSON-safe output
- **WHEN** `to_dict()` is called on a `CoffeeBean`
- **THEN** the result SHALL be a plain dict with string keys, and all values SHALL be JSON-serializable

#### Scenario: from_row on old schema row with brew_score column
- **WHEN** `CoffeeBean.from_row(row)` is called on a row that contains `brew_score` and `espresso_score` columns
- **THEN** no error SHALL be raised and those column values SHALL be ignored

### Requirement: CoffeeBean from scan result
The `CoffeeBean` class SHALL provide a classmethod `from_scan(data: dict)` that maps Claude API scan output to a `CoffeeBean` instance. The scan dict uses key `roastery` which SHALL be mapped to the `roaster` property.

#### Scenario: Mapping scan output to CoffeeBean
- **WHEN** `CoffeeBean.from_scan({"roastery": "Square Mile", "name": "Red Brick", ...})` is called
- **THEN** the returned instance SHALL have `roaster` set to `"Square Mile"` and `name` set to `"Red Brick"`

#### Scenario: Missing fields in scan output
- **WHEN** `CoffeeBean.from_scan({})` is called with an empty dict
- **THEN** all properties SHALL be `None` (no KeyError raised)

### Requirement: Route handlers use CoffeeBean
All API route handlers (`POST /api/scan`, `GET /api/coffees`, `POST /api/coffees`, `DELETE /api/coffees/<id>`) SHALL use `CoffeeBean` instances for data handling instead of raw dicts.

#### Scenario: Scan endpoint returns CoffeeBean-shaped response
- **WHEN** a POST to `/api/scan` succeeds
- **THEN** the response JSON SHALL include the new fields (`country_grown`, `country_roasted`, `price`) alongside existing ones

#### Scenario: Save endpoint accepts new fields
- **WHEN** a POST to `/api/coffees` includes `brew_score`, `espresso_score`, `price`, `country_grown`, and `country_roasted`
- **THEN** all fields SHALL be persisted to the database

### Requirement: Updated Claude vision prompt
The Claude vision prompt SHALL request `country_grown`, `country_roasted`, and `price` in addition to the existing fields. The prompt SHALL request `roastery` (not `roaster`) to maintain backward compatibility with scan parsing.

#### Scenario: Prompt extracts new fields
- **WHEN** a coffee bag image is sent to the Claude API
- **THEN** the prompt SHALL ask for `country_grown`, `country_roasted`, and `price` fields in the expected JSON

### Requirement: Frontend supports new fields
The frontend review form SHALL include input fields for `country_grown`, `country_roasted`, `price`, `brew_score`, and `espresso_score`. The two score fields SHALL each use the existing star-button pattern (1-5).

#### Scenario: Review form shows all new fields
- **WHEN** a scan result populates the review form
- **THEN** the form SHALL display editable inputs for country_grown, country_roasted, and price
- **AND** the form SHALL display two separate sets of rating buttons labeled "Brew Score" and "Espresso Score"

#### Scenario: Coffee list displays scores
- **WHEN** the coffee list renders an entry with both brew_score and espresso_score set
- **THEN** both scores SHALL be displayed with labels distinguishing them
