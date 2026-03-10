## Context

The tasting modal already has all the form fields needed (brew type, dosage, score, tasting notes, comments). Currently it only supports creating new tastings. The tasting history renders entries with a delete button but no edit option.

## Goals / Non-Goals

**Goals:**
- Allow editing any field of an existing tasting
- Reuse the existing tasting modal (no new UI components)
- Preserve the original `created_at` timestamp when editing

**Non-Goals:**
- Editing from a different screen (always use the modal)
- Batch editing multiple tastings

## Decisions

### 1. Reuse the tasting modal for both create and edit

Track an `editingTastingId` variable (null = create mode, number = edit mode). When editing:
- Pre-populate all form fields with the existing tasting data
- Lock the coffee selector (since we're editing, not changing which coffee)
- Change button text to "Update Tasting"
- On save, PUT instead of POST

**Why**: The modal already has all needed fields. Building a separate edit UI would duplicate code.

### 2. PUT endpoint mirrors POST logic

`PUT /api/tastings/<id>` accepts the same JSON body as POST, validates the tasting exists, runs an UPDATE query, and returns the updated tasting.

**Why**: Consistent with the existing `PUT /api/coffees/<id>` pattern in the codebase.

### 3. Edit button next to delete button in tasting history

Add an "edit" link/button next to the existing "delete" button in each tasting entry. Clicking it opens the modal in edit mode with pre-populated fields.

**Why**: Discoverable placement alongside the existing delete action.

## Risks / Trade-offs

- **[Modal state complexity]** → Mitigated by a single `editingTastingId` variable that cleanly separates create vs edit paths.
