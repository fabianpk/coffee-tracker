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
| `other` | `str \| None` |
| `notes` | `str \| None` |
| `created_at` | `str` |

`origin` is removed from the dataclass. The `origin` column remains in the database but is ignored by `from_row()`.

#### Scenario: Create a CoffeeBean with all fields including bean_type
- **WHEN** a `CoffeeBean` is instantiated with `bean_type="Bourbon"` and all other properties set
- **THEN** `bean_type` SHALL be accessible as a `str | None` attribute with value `"Bourbon"`

#### Scenario: Create a CoffeeBean with minimal fields
- **WHEN** a `CoffeeBean` is instantiated with only `created_at` set
- **THEN** all other fields (except `created_at`) SHALL default to `None`, including `bean_type`

#### Scenario: from_row ignores origin column
- **WHEN** `CoffeeBean.from_row(row)` is called on a row that contains an `origin` column
- **THEN** no error SHALL be raised and the `origin` value SHALL be ignored

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
The `CoffeeBean` class SHALL provide a classmethod `from_scan(data: dict)` that maps Claude API scan output to a `CoffeeBean` instance. The scan dict uses key `roastery` which SHALL be mapped to the `roaster` property. If the scan data contains an `origin` key and `country_grown` is empty/null, `origin` SHALL be mapped to `country_grown` as a fallback.

#### Scenario: Mapping scan output to CoffeeBean
- **WHEN** `CoffeeBean.from_scan({"roastery": "Square Mile", "name": "Red Brick", ...})` is called
- **THEN** the returned instance SHALL have `roaster` set to `"Square Mile"` and `name` set to `"Red Brick"`

#### Scenario: Origin fallback to country_grown
- **WHEN** `CoffeeBean.from_scan({"origin": "Ethiopia, Kenya", "country_grown": null})` is called
- **THEN** `country_grown` SHALL be set to `"Ethiopia, Kenya"`

#### Scenario: Origin ignored when country_grown is set
- **WHEN** `CoffeeBean.from_scan({"origin": "Ethiopia", "country_grown": "Kenya"})` is called
- **THEN** `country_grown` SHALL remain `"Kenya"` and `origin` SHALL be discarded

### Requirement: Route handlers use CoffeeBean
All API route handlers (`POST /api/scan`, `GET /api/coffees`, `POST /api/coffees`, `DELETE /api/coffees/<id>`) SHALL use `CoffeeBean` instances for data handling instead of raw dicts.

#### Scenario: Scan endpoint returns CoffeeBean-shaped response
- **WHEN** a POST to `/api/scan` succeeds
- **THEN** the response JSON SHALL include the new fields (`country_grown`, `country_roasted`, `price`) alongside existing ones

#### Scenario: Save endpoint accepts new fields
- **WHEN** a POST to `/api/coffees` includes `brew_score`, `espresso_score`, `price`, `country_grown`, and `country_roasted`
- **THEN** all fields SHALL be persisted to the database

### Requirement: Updated Claude vision prompt
The Claude vision prompt SHALL NOT request `origin`. The prompt SHALL request `country_grown` with the instruction: "country_grown is the country or region where the beans were grown; list all separated by commas if multiple (e.g. a blend)." The prompt SHALL request `bean_type` in the JSON template with guidance: "bean_type is the species or variety of the coffee bean (e.g. Arabica, Robusta, Bourbon, Gesha, SL28); list all separated by commas if multiple; null if not stated on the bag."

#### Scenario: Prompt does not ask for origin
- **WHEN** a coffee bag image is sent to the Claude API
- **THEN** the prompt JSON template SHALL NOT include an `origin` field

#### Scenario: Prompt asks for expanded country_grown
- **WHEN** a coffee bag image is sent to the Claude API
- **THEN** the prompt SHALL instruct Claude to put all countries/regions of origin into `country_grown`

#### Scenario: Prompt requests bean_type
- **WHEN** a coffee bag image is sent to the Claude API
- **THEN** the prompt JSON template SHALL include a `bean_type` field

#### Scenario: Scan extracts bean_type from bag
- **WHEN** a coffee bag image showing "100% Arabica" is scanned
- **THEN** the scan result SHALL include `bean_type` with value `"Arabica"` (or similar extraction)

#### Scenario: Scan returns null bean_type when not on bag
- **WHEN** a coffee bag image that does not mention bean type/variety is scanned
- **THEN** the scan result SHALL include `bean_type` with value `null`

### Requirement: Database schema includes bean_type
The `coffees` table SHALL include a `bean_type TEXT` column. The `init_db()` migration SHALL add this column to existing databases that lack it.

#### Scenario: New database includes bean_type column
- **WHEN** `init_db()` creates a fresh `coffees` table
- **THEN** the table SHALL include a `bean_type TEXT` column

#### Scenario: Existing database is migrated to include bean_type
- **WHEN** `init_db()` runs on an existing database without a `bean_type` column
- **THEN** the column SHALL be added via `ALTER TABLE` and existing rows SHALL have `bean_type` set to `NULL`

### Requirement: Frontend supports new fields
The frontend review form and detail panel SHALL NOT include an `origin` input field. The coffee card list SHALL NOT display `origin`.

#### Scenario: Review form has no origin field
- **WHEN** a scan result populates the review form
- **THEN** the form SHALL NOT display an "Origin" input

#### Scenario: Coffee card has no origin line
- **WHEN** the coffee list renders an entry
- **THEN** the card SHALL NOT display an origin line

### Requirement: Frontend supports bean_type field
The frontend review form and detail panel SHALL include a `bean_type` input field. The coffee card list SHALL display bean type when present.

#### Scenario: Review form includes bean_type
- **WHEN** a scan result populates the review form
- **THEN** the form SHALL display a "Bean Type" input field populated with the scanned value

#### Scenario: Bean type displayed on coffee card
- **WHEN** the coffee list renders an entry that has a non-null `bean_type`
- **THEN** the card SHALL display the bean type value

#### Scenario: Bean type editable in detail view
- **WHEN** a user opens the detail/edit view for a coffee entry
- **THEN** the user SHALL be able to edit the `bean_type` field and save changes
