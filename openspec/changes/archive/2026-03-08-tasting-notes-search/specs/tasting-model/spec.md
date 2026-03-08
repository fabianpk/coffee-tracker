## MODIFIED Requirements

### Requirement: Tasting dataclass definition
The system SHALL provide a `Tasting` dataclass in `models.py` with the following properties:

| Property | Type |
|---|---|
| `id` | `int \| None` (None before DB insert) |
| `coffee_id` | `int` |
| `brew_type` | `str \| None` (e.g. "espresso", "brew") |
| `dosage` | `float \| None` (10.0–20.0, stored as number; UI displays with "gr" suffix) |
| `score` | `int \| None` (1–5) |
| `tasting_notes` | `str \| None` |
| `comments` | `str \| None` |
| `created_at` | `str` |

#### Scenario: Create a Tasting with tasting_notes
- **WHEN** a `Tasting` is instantiated with `tasting_notes="Chocolate, Berry"` and other properties set
- **THEN** `tasting_notes` SHALL be accessible as a `str | None` attribute

#### Scenario: Create a Tasting with minimal fields
- **WHEN** a `Tasting` is instantiated with only `coffee_id` and `created_at`
- **THEN** all other optional fields SHALL default to `None`, including `tasting_notes`

### Requirement: tastings database table
The SQLite database SHALL have a `tastings` table with columns: `id` (PK), `coffee_id` (INTEGER NOT NULL, FK to `coffees.id`), `brew_type`, `dosage`, `score`, `tasting_notes`, `comments`, `created_at`.

#### Scenario: Fresh database initialization
- **WHEN** the app starts with no existing `coffees.db`
- **THEN** the `tastings` table SHALL include a `tasting_notes TEXT` column

#### Scenario: Existing database without tasting_notes column
- **WHEN** the app starts with an existing `tastings` table that has no `tasting_notes` column
- **THEN** `init_db()` SHALL add the column via `ALTER TABLE`
