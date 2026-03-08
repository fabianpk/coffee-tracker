## Context

The detail panel currently supports viewing, editing, saving, and rescanning a coffee entry. Deletion is only available via a small "delete" text button on the list card. The backend `DELETE /api/coffees/<id>` endpoint already exists with cascade deletion of tastings.

## Goals / Non-Goals

**Goals:**
- Add a delete button to the detail panel so users can delete from the view they're already in
- Reuse the existing `DELETE /api/coffees/<id>` endpoint and confirmation pattern

**Non-Goals:**
- No backend changes needed — the delete API already exists
- No changes to the list card delete button (it stays as-is)

## Decisions

**1. Place delete button at the bottom of the detail panel, styled distinctly**
A destructive action should be visually separated from the save/rescan actions. A red-styled button at the bottom of the panel makes the action discoverable but not easy to hit accidentally.
- *Alternative*: Put it next to Save — rejected because save and delete are opposite actions and shouldn't be adjacent.

**2. Reuse the existing confirmation and deletion flow**
The `deleteCoffee()` JS function already handles confirmation, API call, and list refresh. The detail panel handler just needs to also close the panel after deletion.

## Risks / Trade-offs

- **[Accidental deletion]** → Mitigation: confirmation dialog already required by `deleteCoffee()`, plus visual distinction of the button.
