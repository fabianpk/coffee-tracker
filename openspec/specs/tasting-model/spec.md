## Purpose
Define the Tasting dataclass with serialization methods and the tastings database table schema including grind level support.

## Requirements

### Requirement: Tasting dataclass definition
The system SHALL provide a `Tasting` dataclass in `models.py` with the following properties:

| Property | Type |
|---|---|
| `id` | `int \| None` (None before DB insert) |
| `coffee_id` | `int` |
| `brew_type` | `str \| None` (e.g. "espresso", "brew") |
| `dosage` | `float \| None` (10.0-20.0, stored as number; UI displays with "gr" suffix) |
| `grind_level` | `float \| None` (3.0-22.0, step 0.2) |
| `score` | `int \| None` (1-5) |
| `tasting_notes` | `str \| None` |
| `comments` | `str \| None` |
| `created_at` | `str` |

#### Scenario: Create a Tasting with tasting_notes
- **WHEN** a `Tasting` is instantiated with `tasting_notes="Chocolate, Berry"` and other properties set
- **THEN** `tasting_notes` SHALL be accessible as a `str | None` attribute

#### Scenario: Create a Tasting with all fields
- **WHEN** a `Tasting` is instantiated with all properties set including `grind_level` and `comments`
- **THEN** all properties SHALL be accessible as typed attributes

#### Scenario: Create a Tasting with minimal fields
- **WHEN** a `Tasting` is instantiated with only `coffee_id` and `created_at`
- **THEN** all other optional fields SHALL default to `None`, including `grind_level`

### Requirement: Tasting database serialization
The `Tasting` class SHALL provide methods to convert to and from database rows.

- `to_row()` SHALL return a dict of column names to values suitable for SQL INSERT.
- `from_row(row)` SHALL be a classmethod that accepts a `sqlite3.Row` and returns a `Tasting` instance.
- `to_dict()` SHALL return a dict suitable for JSON serialization.

#### Scenario: Round-trip through to_row and from_row
- **WHEN** a `Tasting` is converted via `to_row()`, inserted into the database, read back as a `sqlite3.Row`, and converted via `Tasting.from_row(row)`
- **THEN** the resulting `Tasting` SHALL have identical property values to the original (except `id`, which is assigned by the database)

#### Scenario: to_dict produces JSON-safe output
- **WHEN** `to_dict()` is called on a `Tasting`
- **THEN** the result SHALL be a plain dict with string keys and all values SHALL be JSON-serializable

### Requirement: tastings database table
The SQLite database SHALL have a `tastings` table with columns: `id` (PK), `coffee_id` (INTEGER NOT NULL, FK to `coffees.id`), `brew_type`, `dosage`, `grind_level` (REAL), `score`, `tasting_notes`, `comments`, `created_at`.

#### Scenario: Fresh database initialization
- **WHEN** the app starts with no existing `coffees.db`
- **THEN** both the `coffees` table and the `tastings` table SHALL be created with all columns including `grind_level`

#### Scenario: Existing database without tastings table
- **WHEN** the app starts with an existing `coffees.db` that has no `tastings` table
- **THEN** `init_db()` SHALL create the `tastings` table without modifying the `coffees` table

#### Scenario: Existing database without grind_level column
- **WHEN** the app starts with an existing `tastings` table missing the `grind_level` column
- **THEN** `init_db()` SHALL add the `grind_level REAL` column to the `tastings` table
