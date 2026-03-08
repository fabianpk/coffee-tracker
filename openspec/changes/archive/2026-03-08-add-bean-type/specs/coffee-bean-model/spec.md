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

### Requirement: Updated Claude vision prompt
The Claude vision prompt SHALL request `bean_type` in the JSON template. The prompt SHALL include guidance: "bean_type is the species or variety of the coffee bean (e.g. Arabica, Robusta, Bourbon, Gesha, SL28); list all separated by commas if multiple; null if not stated on the bag."

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
