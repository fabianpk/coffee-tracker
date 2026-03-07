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
| `process` | `str \| None` |
| `roast_level` | `str \| None` |
| `tasting_notes` | `str \| None` |
| `weight` | `str \| None` |
| `price` | `str \| None` |
| `other` | `str \| None` |
| `notes` | `str \| None` |
| `created_at` | `str` |

`origin` is removed from the dataclass. The `origin` column remains in the database but is ignored by `from_row()`.

#### Scenario: Create a CoffeeBean with all fields
- **WHEN** a `CoffeeBean` is instantiated with all properties set
- **THEN** all properties SHALL be accessible as typed attributes

#### Scenario: Create a CoffeeBean with minimal fields
- **WHEN** a `CoffeeBean` is instantiated with only `created_at` set
- **THEN** all other fields (except `created_at`) SHALL default to `None`

#### Scenario: from_row ignores origin column
- **WHEN** `CoffeeBean.from_row(row)` is called on a row that contains an `origin` column
- **THEN** no error SHALL be raised and the `origin` value SHALL be ignored

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

### Requirement: Updated Claude vision prompt
The Claude vision prompt SHALL NOT request `origin`. The prompt SHALL request `country_grown` with the instruction: "country_grown is the country or region where the beans were grown; list all separated by commas if multiple (e.g. a blend)."

#### Scenario: Prompt does not ask for origin
- **WHEN** a coffee bag image is sent to the Claude API
- **THEN** the prompt JSON template SHALL NOT include an `origin` field

#### Scenario: Prompt asks for expanded country_grown
- **WHEN** a coffee bag image is sent to the Claude API
- **THEN** the prompt SHALL instruct Claude to put all countries/regions of origin into `country_grown`

### Requirement: Frontend supports new fields
The frontend review form and detail panel SHALL NOT include an `origin` input field. The coffee card list SHALL NOT display `origin`.

#### Scenario: Review form has no origin field
- **WHEN** a scan result populates the review form
- **THEN** the form SHALL NOT display an "Origin" input

#### Scenario: Coffee card has no origin line
- **WHEN** the coffee list renders an entry
- **THEN** the card SHALL NOT display an origin line
