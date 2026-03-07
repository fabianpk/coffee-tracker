# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Coffee Tracker is a web app for scanning coffee bag photos with Claude's vision API and tracking them in a personal collection. Think "Untappd for coffee."

## Commands

- **Install dependencies:** `uv sync`
- **Run web app:** `uv run python app.py` (serves on `http://0.0.0.0:5555`)
- **Run CLI scanner:** `uv run python scan_coffee.py <image_path>`

No test suite exists yet.

## Architecture

- **`app.py`** — Flask web app. Contains all routes, database setup, and image processing. Uses Claude Haiku 4.5 vision to extract structured JSON from coffee bag photos. SQLite database (`coffees.db`) stores entries. Key routes:
  - `POST /api/scan` — accepts image upload, returns extracted coffee details as JSON
  - `GET/POST /api/coffees` — list and save coffee entries
  - `DELETE /api/coffees/<id>` — delete an entry
- **`models.py`** — `CoffeeBean` dataclass representing a coffee entry with properties: roaster, name, country_grown, country_roasted, origin, process, roast_level, tasting_notes, weight, price, brew_score, espresso_score, other, notes. Provides `to_row()`, `from_row()`, `to_dict()`, and `from_scan()` methods for serialization.
- **`scan_coffee.py`** — Standalone CLI tool that does the same vision extraction, returns structured `CoffeeBean` output. Takes an image path as argument.
- **`templates/index.html`** — Single-page frontend with inline CSS/JS (no build step). Dark theme, mobile-first. Handles camera input, review form, and coffee list display.

## Key Details

- Python 3.13, managed with **uv** (not pip)
- `ANTHROPIC_API_KEY` must be set in `.env` (loaded via python-dotenv)
- HEIC/HEIF image support via `pillow-heif`; unsupported formats are auto-converted to JPEG before sending to the API
- The SQLite DB file (`coffees.db`) is gitignored and auto-created on startup via `init_db()`
- `init_db()` automatically migrates old schemas: adds missing columns and copies `rating` → `brew_score` for backward compatibility
