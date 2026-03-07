## Why

The project has no README.md, and the existing CLAUDE.md is outdated — it doesn't reflect the new `models.py` module, the `CoffeeBean` dataclass, the additional fields (country_grown, country_roasted, price, brew/espresso scores), or the database migration logic. New contributors and the project's public face need accurate documentation.

## What Changes

- **Create `README.md`** with project description, setup instructions, usage guide, and architecture overview reflecting the current codebase.
- **Update `CLAUDE.md`** to document `models.py` and the `CoffeeBean` model in the Architecture section, and note the database migration behavior in Key Details.

## Capabilities

### New Capabilities
- `project-docs`: README.md creation and CLAUDE.md updates to accurately reflect the current project state.

### Modified Capabilities
_(none)_

## Impact

- **`README.md`** — New file created at project root.
- **`CLAUDE.md`** — Architecture and Key Details sections updated.
