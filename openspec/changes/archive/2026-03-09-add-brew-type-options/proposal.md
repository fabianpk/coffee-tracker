## Why

The tasting workflow currently only supports two brew types (Espresso and Brew), but users prepare coffee in more ways. Adding Metal Brew and Cappuccino covers common preparation methods and makes the tracker more useful. Emojis for each type improve visual recognition in the UI.

## What Changes

- Add two new brew type options: "Metal Brew" and "Cappuccino"
- Add an emoji icon to each brew type button (Espresso, Brew, Metal Brew, Cappuccino)
- Update the tasting display to show the emoji alongside the brew type name

## Capabilities

### New Capabilities

- `brew-type-options`: Defines the available brew types with their display names and emoji representations

### Modified Capabilities

- `tasting-ui`: Add new brew type buttons with emojis to the tasting modal and display

## Impact

- `templates/index.html` — brew type button markup, tasting display rendering
- No backend changes needed; `brew_type` is already a free-text field stored in SQLite
