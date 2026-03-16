## ADDED Requirements

### Requirement: Roastery emoji generation via Claude API
The system SHALL generate a single emoji for each roastery by calling the Claude API (Haiku model) with the roastery name. The prompt SHALL ask for a single emoji that visually represents the roastery based on its name, origin, or character. The response SHALL be a single emoji character.

#### Scenario: Generate emoji for a new roastery
- **WHEN** a coffee is saved with roaster "Koppi" and no emoji exists for "Koppi"
- **THEN** the system SHALL call the Claude API to generate an emoji and store the result in the `roastery_emojis` table

#### Scenario: Existing roastery already has emoji
- **WHEN** a coffee is saved with roaster "Koppi" and an emoji already exists for "Koppi"
- **THEN** the system SHALL NOT make a Claude API call and SHALL use the cached emoji

### Requirement: Roastery emoji persistence
The system SHALL store roastery emoji mappings in a `roastery_emojis` table with columns `roaster TEXT UNIQUE` and `emoji TEXT`. The table SHALL be created by `init_db()` if it does not exist.

#### Scenario: Table creation on startup
- **WHEN** the application starts and the `roastery_emojis` table does not exist
- **THEN** `init_db()` SHALL create the table

#### Scenario: Table already exists
- **WHEN** the application starts and the `roastery_emojis` table already exists
- **THEN** `init_db()` SHALL not error or duplicate the table

### Requirement: GET /api/roasters returns emojis
The existing `GET /api/roasters` endpoint SHALL be enhanced to return an array of objects `[{"roaster": "...", "emoji": "..."}]` instead of a plain string array. Each object SHALL include the cached emoji for that roaster, or a default fallback emoji "☕" if none is cached.

#### Scenario: Roasters with emojis
- **WHEN** a GET to `/api/roasters` is made and roasteries have cached emojis
- **THEN** the response SHALL be a JSON array of objects with `roaster` and `emoji` fields

#### Scenario: Roaster without cached emoji
- **WHEN** a GET to `/api/roasters` is made and one roaster has no cached emoji
- **THEN** that roaster's object SHALL have `"emoji": "☕"` as fallback

### Requirement: Emoji generation for existing roasteries on first load
When the enhanced `GET /api/roasters` endpoint is called and any roaster lacks a cached emoji, the system SHALL generate emojis for all missing roasters in a single batch Claude API call and cache them before returning the response.

#### Scenario: First load after upgrade with existing coffees
- **WHEN** `GET /api/roasters` is called and 3 roasters exist but none have emojis
- **THEN** the system SHALL generate emojis for all 3, cache them, and return the complete response with emojis
