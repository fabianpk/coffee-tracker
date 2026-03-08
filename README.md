# Coffee Tracker

A web app for scanning coffee bag photos with Claude's vision API and tracking them in a personal collection. Think "Untappd for coffee."

## Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/) package manager
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

```bash
uv sync
echo "ANTHROPIC_API_KEY_FOR_LOOKUP=your-key-here" > .env
```

## Usage

### Web app

The app runs as a systemd service and starts automatically on boot:

```bash
sudo systemctl start coffee-tracker   # start
sudo systemctl stop coffee-tracker    # stop
sudo systemctl restart coffee-tracker # restart after code changes
sudo journalctl -u coffee-tracker -f  # follow logs
```

Opens at `http://localhost:5555`. Scan a coffee bag photo to extract details (roaster, origin, bean type, process, tasting notes, etc.), review and edit the results, then save to your collection. Tap any entry to open the detail panel where you can edit fields, rescan another side of the bag, or delete the entry. Conduct tastings with brew type, dosage, and scoring. QR codes on bags are automatically detected and used to enrich scan results from the product page.

To run manually during development:

```bash
uv run python app.py
```

### CLI scanner

```bash
uv run python scan_coffee.py <image_path>
```

Extracts coffee details from a bag photo and prints them to stdout.

### Scan hints

You can improve scan accuracy by providing domain knowledge in a `scan_hints.md` file. Copy the example template and customize it:

```bash
cp scan_hints.example.md scan_hints.md
```

Add common values for process types, bean varieties, origin countries, roast levels, etc. The hints are appended to the Claude prompt on every scan. Edits take effect immediately without restarting.

## Architecture

- **`app.py`** — Flask web app with all routes, database setup, image processing, and Claude vision integration. SQLite database (`coffees.db`) stores entries.
- **`models.py`** — `CoffeeBean` and `Tasting` dataclasses. Handles serialization to/from database rows, API dicts, and scan results.
- **`scan_coffee.py`** — Standalone CLI tool for vision extraction.
- **`scan_hints.example.md`** — Example template for scan hints. Copy to `scan_hints.md` to customize.
- **`templates/index.html`** — Single-page frontend with inline CSS/JS. Dark theme, mobile-first.
