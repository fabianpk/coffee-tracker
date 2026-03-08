## MODIFIED Requirements

### Requirement: Updated Claude vision prompt
The Claude vision prompt SHALL NOT request `origin`. The prompt SHALL request `country_grown` with the instruction: "country_grown is the country or region where the beans were grown; list all separated by commas if multiple (e.g. a blend)." The prompt SHALL request `bean_type` in the JSON template with guidance: "bean_type is the species or variety of the coffee bean (e.g. Arabica, Robusta, Bourbon, Gesha, SL28); list all separated by commas if multiple; null if not stated on the bag." The prompt SHALL instruct Claude to return `tasting_notes` as a comma-separated list of individual notes (e.g. "Chocolate, Strawberry, Peach") rather than copying raw text with arbitrary separators.

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

#### Scenario: Tasting notes returned as comma-separated list
- **WHEN** a coffee bag with tasting notes "Björnbär / Röd Grapefrukt / Tranbär" is scanned
- **THEN** the scan result SHALL return tasting_notes as "Björnbär, Röd Grapefrukt, Tranbär" (comma-separated, preserving original language)
