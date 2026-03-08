## Context

The scan endpoint converts Claude's raw response through `CoffeeBean.from_scan(details)` then `coffee.to_dict()`. Since `other` was removed from the CoffeeBean model, `from_scan()` drops it. The frontend reads `data.other` from the response to populate the read-only "Other (from scan)" textarea.

## Goals / Non-Goals

**Goals:**
- Pass `other` from Claude's raw scan response through to the frontend

**Non-Goals:**
- Adding `other` back to the CoffeeBean model or database

## Decisions

### 1. Preserve before conversion, inject after

**Choice**: Capture `details.get("other")` before calling `from_scan()`, then set `result["other"]` after `to_dict()`.

**Rationale**: Same pattern already used for `matched_roaster` and `qr_url` — transient response metadata that isn't part of the model.
