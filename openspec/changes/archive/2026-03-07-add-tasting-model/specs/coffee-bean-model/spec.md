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

## REMOVED Requirements

### Requirement: Database schema includes all CoffeeBean fields
**Reason**: `brew_score` and `espresso_score` are no longer part of `CoffeeBean`. They remain as unused columns in the `coffees` table (not dropped) but are no longer referenced by the model or API.
**Migration**: Existing values in `brew_score`/`espresso_score` columns are orphaned. No data migration is performed. New scores are recorded via `Tasting` records in the `tastings` table.
