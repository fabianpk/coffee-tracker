## Purpose
Ensure project documentation (README.md and CLAUDE.md) accurately reflects the current architecture and setup instructions.

## Requirements

### Requirement: README.md exists with accurate project overview
The project SHALL have a `README.md` at the repository root containing: project description, prerequisites, setup instructions, usage instructions (web app and CLI), and a brief architecture overview.

#### Scenario: New contributor reads README
- **WHEN** a new user opens the repository
- **THEN** the README SHALL describe what Coffee Tracker does, how to install dependencies (`uv sync`), how to run the web app (`uv run python app.py`), and how to run the CLI scanner (`uv run python scan_coffee.py <image>`)

#### Scenario: README reflects current architecture
- **WHEN** the README lists project files
- **THEN** it SHALL mention `app.py`, `models.py`, `scan_coffee.py`, and `templates/index.html`

### Requirement: CLAUDE.md reflects current architecture
The `CLAUDE.md` Architecture section SHALL document `models.py` and the `CoffeeBean` dataclass. The Key Details section SHALL note the automatic database migration behavior.

#### Scenario: CLAUDE.md lists models.py
- **WHEN** a developer reads CLAUDE.md's Architecture section
- **THEN** `models.py` SHALL be listed with a description of the `CoffeeBean` dataclass and its serialization methods

#### Scenario: CLAUDE.md notes migration
- **WHEN** a developer reads CLAUDE.md's Key Details section
- **THEN** it SHALL mention that `init_db()` automatically migrates old schemas (adds missing columns, copies `rating` to `brew_score`)
