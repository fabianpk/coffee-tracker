## Context

The scan prompt is currently a hardcoded string in `app.py` with inline field descriptions. Users who know their coffee (common processes, varieties, origins) have no way to feed that knowledge into the scan without editing Python code.

## Goals / Non-Goals

**Goals:**
- Provide a single, user-editable markdown file (`scan_hints.md`) for domain knowledge
- Inject its contents into both scan prompts (image and text) as supplementary context
- Graceful degradation: if the file is missing or empty, scanning is unchanged

**Non-Goals:**
- No structured parsing of the markdown — the raw text is appended to the prompt as-is
- No web UI for editing hints — users edit the file directly (it lives alongside `app.py`)
- No per-field validation or schema enforcement

## Decisions

**1. Plain markdown file, appended as-is to the prompt**
The simplest approach: read the file and append its content after the existing prompt instructions. Claude is excellent at interpreting freeform context. No parsing, no YAML, no structured format needed.
- *Alternative*: Structured YAML/JSON with per-field keys — rejected because it adds complexity without clear benefit. Markdown is more natural to write and Claude handles it well.

**2. File location: `scan_hints.md` in the project root (next to `app.py`)**
Easy to find and edit. Gitignored so each user can have their own hints without conflicting.
- *Alternative*: Store in the database — rejected because it's harder to edit and version.

**3. Load at scan time, not at startup**
Read the file on each scan request so edits take effect immediately without restarting the service.
- *Alternative*: Load once at startup — rejected because it would require a restart after every edit.

**4. Create a starter template with common examples**
Ship a `scan_hints.example.md` that demonstrates the format and lists common values. Users copy it to `scan_hints.md` and customize.

## Risks / Trade-offs

- **[Prompt length]** Large hints files increase token usage → Mitigation: truncate to a reasonable limit (e.g., 2000 chars) and document the guideline.
- **[Prompt injection]** Malicious content in hints file → Not a real risk since only the local user edits this file.
