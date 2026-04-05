#!/usr/bin/env python3
"""Coffee Tracker - Untappd for coffee."""

import io
import json
import os
import base64
import sqlite3
import mimetypes
from difflib import SequenceMatcher
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import anthropic
from flask import Flask, render_template, request, jsonify
from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib.error import URLError
from PIL import Image
import pillow_heif
from pyzbar.pyzbar import decode as decode_qr

from models import CoffeeBean, Tasting
from lookup import lookup_coffee, has_provider

pillow_heif.register_heif_opener()

app = Flask(__name__)
DB_PATH = Path(__file__).parent / "coffees.db"

SUPPORTED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
SCAN_HINTS_PATH = Path(__file__).parent / "scan_hints.md"
MAX_HINTS_CHARS = 2000


def load_scan_hints() -> str:
    """Load scan hints from scan_hints.md. Returns empty string if missing/empty."""
    try:
        text = SCAN_HINTS_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""
    return text[:MAX_HINTS_CHARS] if text else ""


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS coffees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roaster TEXT,
            name TEXT,
            country_grown TEXT,
            country_roasted TEXT,
            bean_type TEXT,
            origin TEXT,
            process TEXT,
            roast_level TEXT,
            tasting_notes TEXT,
            weight TEXT,
            price TEXT,
            brew_score INTEGER,
            espresso_score INTEGER,
            comments TEXT,
            created_at TEXT NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS tastings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coffee_id INTEGER NOT NULL REFERENCES coffees(id),
            brew_type TEXT,
            dosage REAL,
            grind_level REAL,
            score INTEGER,
            tasting_notes TEXT,
            comments TEXT,
            created_at TEXT NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS roastery_emojis (
            roaster TEXT UNIQUE,
            emoji TEXT
        )
    """)
    # Migrate old schema if needed
    columns = {row[1] for row in db.execute("PRAGMA table_info(coffees)").fetchall()}
    migrations = {
        "roaster": "TEXT",
        "country_grown": "TEXT",
        "country_roasted": "TEXT",
        "bean_type": "TEXT",
        "price": "TEXT",
        "brew_score": "INTEGER",
        "espresso_score": "INTEGER",
    }
    for col, col_type in migrations.items():
        if col not in columns:
            db.execute(f"ALTER TABLE coffees ADD COLUMN {col} {col_type}")
    # Migrate rating → brew_score
    if "rating" in columns and "brew_score" in migrations:
        db.execute("UPDATE coffees SET brew_score = rating WHERE brew_score IS NULL AND rating IS NOT NULL")
    # Migrate tastings table: add grind_level if missing
    tasting_columns = {row[1] for row in db.execute("PRAGMA table_info(tastings)").fetchall()}
    if "grind_level" not in tasting_columns:
        db.execute("ALTER TABLE tastings ADD COLUMN grind_level REAL")
    db.commit()
    db.close()


def detect_qr_url(img: Image.Image) -> str | None:
    """Detect QR codes in a PIL Image and return the first valid HTTP(S) URL."""
    try:
        results = decode_qr(img)
    except Exception:
        return None
    for result in results:
        try:
            text = result.data.decode("utf-8")
        except (UnicodeDecodeError, AttributeError):
            continue
        if text.startswith("http://") or text.startswith("https://"):
            return text
    return None


MAX_DIMENSION = 1568  # Claude's optimal long-edge size
MAX_BYTES = 600 * 1024  # 600 KB
DEBUG_IMAGE_DIR = Path(__file__).parent / "debug_images"
DEBUG_IMAGE_DIR.mkdir(exist_ok=True)


def prepare_image(file_storage) -> tuple[str, str, Image.Image]:
    """Read uploaded image, downscale if needed, and return (base64, media_type, full_res_image)."""
    raw = file_storage.read()
    img = Image.open(io.BytesIO(raw))
    img = img.convert("RGB")
    full_res = img.copy()

    if max(img.size) > MAX_DIMENSION:
        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.LANCZOS)

    for quality in (85, 75, 60, 50):
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        if buf.tell() <= MAX_BYTES:
            break

    # Save for debugging
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_path = DEBUG_IMAGE_DIR / f"{ts}_{quality}q_{buf.tell()//1024}kb.jpg"
    debug_path.write_bytes(buf.getvalue())
    app.logger.info(f"Debug image saved: {debug_path}")

    return base64.standard_b64encode(buf.getvalue()).decode("utf-8"), "image/jpeg", full_res


class _HTMLTextExtractor(HTMLParser):
    """Simple HTML-to-text converter."""
    def __init__(self):
        super().__init__()
        self._parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        self._skip = tag in ("script", "style", "noscript")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self._parts.append(data)

    def get_text(self) -> str:
        return " ".join(self._parts)


def fetch_page_text(url: str) -> str | None:
    """Fetch a URL and return stripped text content, or None on failure."""
    try:
        req = Request(url, headers={"User-Agent": "CoffeeTracker/1.0"})
        with urlopen(req, timeout=5) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        extractor = _HTMLTextExtractor()
        extractor.feed(html)
        text = extractor.get_text().strip()
        # Truncate to ~8000 chars to keep Claude prompt reasonable
        return text[:8000] if text else None
    except Exception as e:
        app.logger.warning(f"Failed to fetch QR URL {url}: {e}")
        return None


def extract_coffee_details(image_data: str, media_type: str) -> dict:
    """Send image to Claude and extract coffee details as structured data."""
    hints = load_scan_hints()
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY_FOR_LOOKUP"))
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "This is a photo of a coffee bag. Labels are often in Swedish — read all text carefully and transcribe it exactly as printed, do not translate or guess. "
                            "Respond with ONLY valid JSON, no markdown:\n"
                            '{"roastery": "...", "name": "...", "country_grown": "...", '
                            '"country_roasted": "...", "bean_type": "...", "process": "...", "roast_level": "...", '
                            '"tasting_notes": "...", "weight": "...", "price": "...", "other": "..."}\n'
                            "country_grown is the country or region where the beans were grown; list all separated by commas if multiple (e.g. a blend). "
                            "country_roasted is the country where the beans were roasted. "
                            "bean_type is the species or variety of the coffee bean (e.g. Arabica, Robusta, Bourbon, Gesha, SL28); list all if multiple; null if not stated on the bag. "
                            "For tasting_notes, return a comma-separated list of individual flavor notes (e.g. 'Björnbär, Röd Grapefrukt, Tranbär'). Preserve the original language but normalize separators to commas. "
                            "Use null for fields you can't find. Be concise."
                            + (f"\n\nAdditional context about expected values:\n{hints}" if hints else "")
                        ),
                    },
                ],
            }
        ],
    )
    text = message.content[0].text
    # Strip markdown code fences if present
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def extract_coffee_from_text(page_text: str) -> dict:
    """Send product page text to Claude and extract coffee details as structured data."""
    hints = load_scan_hints()
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY_FOR_LOOKUP"))
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "This is the text content of a coffee product page. Extract coffee details from it. "
                    "Text is often in Swedish — transcribe names and tasting notes exactly as written, do not translate. "
                    "Respond with ONLY valid JSON, no markdown:\n"
                    '{"roastery": "...", "name": "...", "country_grown": "...", '
                    '"country_roasted": "...", "bean_type": "...", "process": "...", "roast_level": "...", '
                    '"tasting_notes": "...", "weight": "...", "price": "...", "other": "..."}\n'
                    "country_grown is the country or region where the beans were grown; list all separated by commas if multiple. "
                    "country_roasted is the country where the beans were roasted. "
                    "bean_type is the species or variety of the coffee bean (e.g. Arabica, Robusta, Bourbon, Gesha, SL28); list all if multiple; null if not stated. "
                    "For tasting_notes, return a comma-separated list of individual flavor notes. Preserve the original language but normalize separators to commas. "
                    "Use null for fields you can't find. Be concise."
                    + (f"\n\nAdditional context about expected values:\n{hints}" if hints else "")
                    + f"\n\nPage text:\n{page_text}"
                ),
            }
        ],
    )
    text = message.content[0].text
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def merge_scan_results(image_data: dict, qr_data: dict) -> dict:
    """Merge image scan and QR/URL scan results. QR data takes priority for non-null fields."""
    merged = dict(image_data)
    for key, value in qr_data.items():
        if value is not None and value != "":
            merged[key] = value
    return merged


def match_roaster(scanned_name: str, db) -> str | None:
    """Match a scanned roastery name against known roasters in the database."""
    if not scanned_name:
        return None
    rows = db.execute("SELECT DISTINCT roaster FROM coffees WHERE roaster IS NOT NULL").fetchall()
    if not rows:
        return None
    scanned_lower = scanned_name.lower().strip()
    best_match = None
    best_ratio = 0.0
    for row in rows:
        known = row[0]
        known_lower = known.lower().strip()
        ratio = SequenceMatcher(None, scanned_lower, known_lower).ratio()
        # Substring check: if one contains the other and shorter is >= 4 chars
        shorter = min(len(scanned_lower), len(known_lower))
        is_substring = shorter >= 4 and (scanned_lower in known_lower or known_lower in scanned_lower)
        if (ratio >= 0.7 or is_substring) and ratio > best_ratio:
            best_ratio = ratio
            best_match = known
        elif is_substring and best_match is None:
            best_match = known
    return best_match


def generate_roastery_emoji(roaster_name: str) -> str:
    """Call Claude Haiku to generate a single emoji for a roastery name."""
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY_FOR_LOOKUP"))
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=10,
            messages=[{
                "role": "user",
                "content": (
                    f"Pick a single emoji that best represents a coffee roastery called \"{roaster_name}\". "
                    "Consider the name's meaning, origin, or character. "
                    "Respond with ONLY the emoji, nothing else."
                ),
            }],
        )
        emoji = message.content[0].text.strip()
        # Ensure we got something reasonable (single emoji-like response)
        if len(emoji) <= 4 and emoji:
            return emoji
        return "☕"
    except Exception as e:
        app.logger.warning(f"Emoji generation failed for {roaster_name}: {e}")
        return "☕"


def generate_roastery_emojis_batch(roaster_names: list[str]) -> dict[str, str]:
    """Generate emojis for multiple roasteries in a single API call."""
    if not roaster_names:
        return {}
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY_FOR_LOOKUP"))
        names_list = ", ".join(f'"{n}"' for n in roaster_names)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": (
                    f"For each coffee roastery name, pick a single emoji that represents it. "
                    f"Consider each name's meaning, origin, or character. "
                    f"Roasteries: {names_list}\n"
                    f"Respond with ONLY valid JSON mapping name to emoji, e.g. "
                    f'{{"Name": "🔥"}}. No markdown, no explanation.'
                ),
            }],
        )
        text = message.content[0].text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        result = json.loads(text)
        # Validate and fill missing
        final = {}
        for name in roaster_names:
            emoji = result.get(name, "☕")
            final[name] = emoji if len(emoji) <= 4 and emoji else "☕"
        return final
    except Exception as e:
        app.logger.warning(f"Batch emoji generation failed: {e}")
        return {name: "☕" for name in roaster_names}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scan", methods=["POST"])
def scan():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    f = request.files["image"]
    app.logger.info(f"Received file: {f.filename}, content_type: {f.content_type}")

    try:
        image_data, media_type, full_res_img = prepare_image(f)
        app.logger.info(f"Prepared image, media_type: {media_type}, data length: {len(image_data)}")

        # Detect QR code from full-resolution image
        qr_url = detect_qr_url(full_res_img)
        if qr_url:
            app.logger.info(f"QR code detected: {qr_url}")

        # Image-based extraction
        details = extract_coffee_details(image_data, media_type)

        # QR/URL-based extraction and merge
        if qr_url:
            page_text = fetch_page_text(qr_url)
            if page_text:
                app.logger.info(f"Fetched page text ({len(page_text)} chars)")
                qr_details = extract_coffee_from_text(page_text)
                details = merge_scan_results(details, qr_details)

        # Match scanned roastery against known roasters
        matched_roaster = None
        scanned_roastery = details.get("roastery") or details.get("roaster")
        if scanned_roastery:
            db = get_db()
            matched_roaster = match_roaster(scanned_roastery, db)
            db.close()
            if matched_roaster:
                details["roastery"] = matched_roaster
        scan_other = details.get("other")
        coffee = CoffeeBean.from_scan(details)
        result = coffee.to_dict()
        result["matched_roaster"] = matched_roaster
        result["qr_url"] = qr_url
        result["other"] = scan_other
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Scan error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/coffees", methods=["GET"])
def list_coffees():
    db = get_db()
    note_filter = request.args.get("note")
    roaster_filter = request.args.get("roaster")
    sort_mode = request.args.get("sort")

    if sort_mode == "last_tasting":
        query = """
            SELECT c.*, MAX(t.created_at) as last_tasting_at
            FROM coffees c
            LEFT JOIN tastings t ON c.id = t.coffee_id
            WHERE 1=1
        """
        params = []
        if roaster_filter:
            query += " AND c.roaster = ?"
            params.append(roaster_filter)
        if note_filter:
            query += " AND c.tasting_notes LIKE ? COLLATE NOCASE"
            params.append(f"%{note_filter}%")
        query += " GROUP BY c.id ORDER BY CASE WHEN MAX(t.created_at) IS NULL THEN 1 ELSE 0 END, MAX(t.created_at) DESC"
        rows = db.execute(query, params).fetchall()
        if note_filter:
            filtered = []
            for r in rows:
                notes = [n.strip() for n in (r["tasting_notes"] or "").split(",")]
                if any(n.lower() == note_filter.lower() for n in notes):
                    filtered.append(r)
            rows = filtered
    elif note_filter:
        pattern = f"%{note_filter}%"
        if roaster_filter:
            rows = db.execute(
                "SELECT * FROM coffees WHERE tasting_notes LIKE ? COLLATE NOCASE AND roaster = ? ORDER BY created_at DESC",
                (pattern, roaster_filter),
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT * FROM coffees WHERE tasting_notes LIKE ? COLLATE NOCASE ORDER BY created_at DESC",
                (pattern,),
            ).fetchall()
        filtered = []
        for r in rows:
            notes = [n.strip() for n in (r["tasting_notes"] or "").split(",")]
            if any(n.lower() == note_filter.lower() for n in notes):
                filtered.append(r)
        rows = filtered
    elif roaster_filter:
        rows = db.execute(
            "SELECT * FROM coffees WHERE roaster = ? ORDER BY created_at DESC",
            (roaster_filter,),
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM coffees ORDER BY created_at DESC").fetchall()

    coffees = []
    for r in rows:
        avg = db.execute("SELECT ROUND(AVG(score), 1) FROM tastings WHERE coffee_id = ?", (r["id"],)).fetchone()[0]
        coffees.append(CoffeeBean.from_row(r).to_dict(average_score=avg))
    db.close()
    return jsonify(coffees)


@app.route("/api/tasting-notes", methods=["GET"])
def list_tasting_notes():
    """Return sorted unique tasting notes across all coffees."""
    db = get_db()
    rows = db.execute("SELECT tasting_notes FROM coffees WHERE tasting_notes IS NOT NULL").fetchall()
    db.close()
    notes = set()
    for r in rows:
        for note in r["tasting_notes"].split(","):
            stripped = note.strip()
            if stripped:
                notes.add(stripped)
    return jsonify(sorted(notes, key=str.lower))


@app.route("/api/roasters", methods=["GET"])
def list_roasters():
    """Return distinct roaster names with emojis, sorted by tasting count descending."""
    db = get_db()
    rows = db.execute("""
        SELECT c.roaster, COUNT(t.id) as tasting_count
        FROM coffees c
        LEFT JOIN tastings t ON c.id = t.coffee_id
        WHERE c.roaster IS NOT NULL AND c.roaster != ''
        GROUP BY c.roaster
        ORDER BY CASE WHEN COUNT(t.id) = 0 THEN 1 ELSE 0 END,
                 COUNT(t.id) DESC,
                 c.roaster COLLATE NOCASE ASC
    """).fetchall()
    roaster_names = [r["roaster"] for r in rows]
    tasting_counts = {r["roaster"]: r["tasting_count"] for r in rows}
    q = request.args.get("q", "").strip().lower()
    if q:
        roaster_names = [r for r in roaster_names if r.lower().startswith(q)]

    # Fetch cached emojis
    emoji_rows = db.execute("SELECT roaster, emoji FROM roastery_emojis").fetchall()
    emoji_map = {r["roaster"]: r["emoji"] for r in emoji_rows}

    # Generate missing emojis in batch
    missing = [r for r in roaster_names if r not in emoji_map]
    if missing:
        new_emojis = generate_roastery_emojis_batch(missing)
        for name, emoji in new_emojis.items():
            db.execute(
                "INSERT OR REPLACE INTO roastery_emojis (roaster, emoji) VALUES (?, ?)",
                (name, emoji),
            )
            emoji_map[name] = emoji
        db.commit()

    db.close()
    result = [{"roaster": r, "emoji": emoji_map.get(r, "☕"), "tasting_count": tasting_counts.get(r, 0)} for r in roaster_names]
    return jsonify(result)


@app.route("/api/coffees", methods=["POST"])
def save_coffee():
    data = request.json
    coffee = CoffeeBean(
        roaster=data.get("roaster"),
        name=data.get("name"),
        country_grown=data.get("country_grown"),
        country_roasted=data.get("country_roasted"),
        bean_type=data.get("bean_type"),
        process=data.get("process"),
        roast_level=data.get("roast_level"),
        tasting_notes=data.get("tasting_notes"),
        weight=data.get("weight"),
        price=data.get("price"),
        comments=data.get("comments"),
    )
    row = coffee.to_row()
    columns = ", ".join(row.keys())
    placeholders = ", ".join("?" for _ in row)
    db = get_db()
    db.execute(f"INSERT INTO coffees ({columns}) VALUES ({placeholders})", list(row.values()))
    db.commit()
    # Generate emoji for roaster if not already cached
    roaster = data.get("roaster", "").strip()
    if roaster:
        existing = db.execute(
            "SELECT emoji FROM roastery_emojis WHERE roaster = ?", (roaster,)
        ).fetchone()
        if not existing:
            emoji = generate_roastery_emoji(roaster)
            db.execute(
                "INSERT OR REPLACE INTO roastery_emojis (roaster, emoji) VALUES (?, ?)",
                (roaster, emoji),
            )
            db.commit()
    db.close()
    return jsonify({"status": "saved"}), 201


@app.route("/api/coffees/<int:coffee_id>", methods=["GET"])
def get_coffee(coffee_id):
    db = get_db()
    row = db.execute("SELECT * FROM coffees WHERE id = ?", (coffee_id,)).fetchone()
    db.close()
    if row is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(CoffeeBean.from_row(row).to_dict())


@app.route("/api/coffees/<int:coffee_id>", methods=["PUT"])
def update_coffee(coffee_id):
    data = request.json
    coffee = CoffeeBean(
        id=coffee_id,
        roaster=data.get("roaster"),
        name=data.get("name"),
        country_grown=data.get("country_grown"),
        country_roasted=data.get("country_roasted"),
        bean_type=data.get("bean_type"),
        process=data.get("process"),
        roast_level=data.get("roast_level"),
        tasting_notes=data.get("tasting_notes"),
        weight=data.get("weight"),
        price=data.get("price"),
        comments=data.get("comments"),
        created_at=data.get("created_at", ""),
    )
    row = coffee.to_row()
    assignments = ", ".join(f"{k} = ?" for k in row)
    db = get_db()
    db.execute(f"UPDATE coffees SET {assignments} WHERE id = ?", [*row.values(), coffee_id])
    db.commit()
    updated = db.execute("SELECT * FROM coffees WHERE id = ?", (coffee_id,)).fetchone()
    db.close()
    return jsonify(CoffeeBean.from_row(updated).to_dict())


@app.route("/api/coffees/<int:coffee_id>", methods=["DELETE"])
def delete_coffee(coffee_id):
    db = get_db()
    db.execute("DELETE FROM tastings WHERE coffee_id = ?", (coffee_id,))
    db.execute("DELETE FROM coffees WHERE id = ?", (coffee_id,))
    db.commit()
    db.close()
    return jsonify({"status": "deleted"})


@app.route("/api/tastings", methods=["POST"])
def save_tasting():
    data = request.json
    coffee_id = data.get("coffee_id")
    if not coffee_id:
        return jsonify({"error": "coffee_id is required"}), 400
    db = get_db()
    exists = db.execute("SELECT id FROM coffees WHERE id = ?", (coffee_id,)).fetchone()
    if not exists:
        db.close()
        return jsonify({"error": "Coffee not found"}), 400
    tasting = Tasting(
        coffee_id=coffee_id,
        brew_type=data.get("brew_type"),
        dosage=data.get("dosage"),
        grind_level=data.get("grind_level"),
        score=data.get("score"),
        tasting_notes=data.get("tasting_notes"),
        comments=data.get("comments"),
    )
    row = tasting.to_row()
    columns = ", ".join(row.keys())
    placeholders = ", ".join("?" for _ in row)
    cursor = db.execute(f"INSERT INTO tastings ({columns}) VALUES ({placeholders})", list(row.values()))
    db.commit()
    tasting.id = cursor.lastrowid
    db.close()
    return jsonify(tasting.to_dict()), 201


@app.route("/api/tastings/<int:tasting_id>", methods=["PUT"])
def update_tasting(tasting_id):
    db = get_db()
    row = db.execute("SELECT * FROM tastings WHERE id = ?", (tasting_id,)).fetchone()
    if not row:
        db.close()
        return jsonify({"error": "Not found"}), 404
    data = request.json
    existing = Tasting.from_row(row)
    tasting = Tasting(
        id=tasting_id,
        coffee_id=existing.coffee_id,
        brew_type=data.get("brew_type", existing.brew_type),
        dosage=data.get("dosage", existing.dosage),
        grind_level=data.get("grind_level", existing.grind_level),
        score=data.get("score", existing.score),
        tasting_notes=data.get("tasting_notes", existing.tasting_notes),
        comments=data.get("comments", existing.comments),
        created_at=existing.created_at,
    )
    updates = tasting.to_row()
    assignments = ", ".join(f"{k} = ?" for k in updates)
    db.execute(f"UPDATE tastings SET {assignments} WHERE id = ?", [*updates.values(), tasting_id])
    db.commit()
    updated = db.execute("SELECT * FROM tastings WHERE id = ?", (tasting_id,)).fetchone()
    db.close()
    return jsonify(Tasting.from_row(updated).to_dict())


@app.route("/api/tastings/<int:tasting_id>", methods=["DELETE"])
def delete_tasting(tasting_id):
    db = get_db()
    row = db.execute("SELECT id FROM tastings WHERE id = ?", (tasting_id,)).fetchone()
    if not row:
        db.close()
        return jsonify({"error": "Not found"}), 404
    db.execute("DELETE FROM tastings WHERE id = ?", (tasting_id,))
    db.commit()
    db.close()
    return jsonify({"status": "deleted"})


@app.route("/api/tastings/recent", methods=["GET"])
def recent_tastings():
    limit = request.args.get("limit", 2, type=int)
    db = get_db()
    rows = db.execute(
        """SELECT t.*, c.name AS coffee_name, c.roaster AS coffee_roaster
           FROM tastings t
           JOIN coffees c ON t.coffee_id = c.id
           ORDER BY t.created_at DESC
           LIMIT ?""",
        (limit,),
    ).fetchall()
    db.close()
    result = []
    for r in rows:
        t = Tasting.from_row(r).to_dict()
        t["coffee_name"] = r["coffee_name"]
        t["coffee_roaster"] = r["coffee_roaster"]
        result.append(t)
    return jsonify(result)


@app.route("/api/tastings", methods=["GET"])
def list_tastings():
    coffee_id = request.args.get("coffee_id")
    db = get_db()
    rows = db.execute(
        "SELECT * FROM tastings WHERE coffee_id = ? ORDER BY created_at DESC",
        (coffee_id,),
    ).fetchall()
    db.close()
    return jsonify([Tasting.from_row(r).to_dict() for r in rows])


@app.route("/api/lookup", methods=["POST"])
def api_lookup():
    data = request.json or {}
    roaster = data.get("roaster", "").strip()
    coffee_name = data.get("coffee_name", "").strip()
    if not roaster or not coffee_name:
        return jsonify({"error": "roaster and coffee_name are required"}), 400
    result = lookup_coffee(roaster, coffee_name)
    if not result:
        return jsonify({"error": "Coffee not found"}), 404
    # Move internal _source key to public source field
    source = result.pop("_source", "roastery")
    result["source"] = source
    return jsonify(result)


@app.route("/api/lookup/available", methods=["GET"])
def api_lookup_available():
    roaster = request.args.get("roaster", "").strip()
    return jsonify({"available": has_provider(roaster)})


init_db()

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5555, debug=debug)
