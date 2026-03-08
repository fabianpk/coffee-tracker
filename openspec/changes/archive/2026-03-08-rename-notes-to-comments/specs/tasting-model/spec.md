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
| `comments` | `str \| None` |
| `created_at` | `str` |

#### Scenario: Create a Tasting with all fields
- **WHEN** a `Tasting` is instantiated with all properties set including `comments`
- **THEN** all properties SHALL be accessible as typed attributes

#### Scenario: Create a Tasting with minimal fields
- **WHEN** a `Tasting` is instantiated with only `coffee_id` and `created_at`
- **THEN** all other optional fields SHALL default to `None`

### Requirement: tastings database table
The SQLite database SHALL have a `tastings` table with columns: `id` (PK), `coffee_id` (INTEGER NOT NULL, FK to `coffees.id`), `brew_type`, `dosage`, `score`, `comments`, `created_at`.

#### Scenario: Fresh database initialization
- **WHEN** the app starts with no existing `coffees.db`
- **THEN** both the `coffees` table and the `tastings` table SHALL be created with `comments` columns

#### Scenario: Existing database without tastings table
- **WHEN** the app starts with an existing `coffees.db` that has no `tastings` table
- **THEN** `init_db()` SHALL create the `tastings` table without modifying the `coffees` table
