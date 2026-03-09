## 1. Brew Type Registry

- [x] 1.1 Define a `BREW_TYPES` JS object in `templates/index.html` mapping keys (`espresso`, `brew`, `metal_brew`, `cappuccino`) to `{ emoji, label }` objects
- [x] 1.2 Choose appropriate emojis for each brew type that render well cross-platform

## 2. Tasting Modal Buttons

- [x] 2.1 Replace the two hardcoded brew type buttons with a loop over `BREW_TYPES` that generates buttons showing emoji + label
- [x] 2.2 Update `.brew-type-buttons` CSS to handle four buttons cleanly on mobile (allow wrapping or reduce padding)

## 3. Tasting History Display

- [x] 3.1 Update the tasting history rendering to look up brew type in `BREW_TYPES` and display emoji + label (fall back to raw value for unknown types)

## 4. Verification

- [x] 4.1 Manually verify all four buttons appear and are selectable in the tasting modal
- [x] 4.2 Verify tasting history displays emojis for both new and existing tastings
