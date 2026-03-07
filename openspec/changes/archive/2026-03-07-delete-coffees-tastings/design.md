## Context

`DELETE /api/coffees/<id>` exists but only deletes the coffee row — orphaning any tastings referencing it. No route exists to delete individual tastings. The `tastings` table has a `coffee_id` FK but SQLite doesn't enforce foreign key constraints by default.

## Goals / Non-Goals

**Goals:**
- Cascade-delete tastings when a coffee is deleted
- Allow deleting individual tastings via API and UI

**Non-Goals:**
- Enabling SQLite foreign key enforcement (would require `PRAGMA foreign_keys = ON` per connection — unnecessary since we handle cascading in application code)

## Decisions

### 1. Application-level cascade, not DB-level
Delete tastings explicitly before deleting the coffee in the same transaction. Simple and matches the existing pattern of not relying on SQLite FK enforcement.

### 2. Inline delete button in tasting history
Each tasting entry in the collapsible history section gets a small "delete" link. After deletion, the tasting list is refreshed and the coffee list is reloaded to update `average_score`.

## Risks / Trade-offs

- **No undo** — deletions are permanent. → Acceptable for a personal-use app; confirm dialogs are sufficient.
