# Coffee Tracker

A web app for scanning coffee bag photos with Claude's vision API and tracking them in a personal collection. Think "Untappd for coffee."

## Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/) package manager
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

```bash
uv sync
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

## Usage

### Web app

```bash
uv run python app.py
```

Opens at `http://localhost:5555`. Scan a coffee bag photo to extract details (roaster, origin, tasting notes, etc.), review and edit the results, then save to your collection. Supports brew and espresso scoring.

### CLI scanner

```bash
uv run python scan_coffee.py <image_path>
```

Extracts coffee details from a bag photo and prints them to stdout.

## Architecture

- **`app.py`** — Flask web app with all routes, database setup, image processing, and Claude vision integration. SQLite database (`coffees.db`) stores entries.
- **`models.py`** — `CoffeeBean` dataclass representing a coffee entry. Handles serialization to/from database rows, API dicts, and scan results.
- **`scan_coffee.py`** — Standalone CLI tool for vision extraction.
- **`templates/index.html`** — Single-page frontend with inline CSS/JS. Dark theme, mobile-first.
