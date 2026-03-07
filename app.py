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
from PIL import Image
import pillow_heif

from models import CoffeeBean, Tasting

pillow_heif.register_heif_opener()

app = Flask(__name__)
DB_PATH = Path(__file__).parent / "coffees.db"

SUPPORTED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


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
            origin TEXT,
            process TEXT,
            roast_level TEXT,
            tasting_notes TEXT,
            weight TEXT,
            price TEXT,
            brew_score INTEGER,
            espresso_score INTEGER,
            other TEXT,
            notes TEXT,
            created_at TEXT NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS tastings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coffee_id INTEGER NOT NULL REFERENCES coffees(id),
            brew_type TEXT,
            dosage REAL,
            score INTEGER,
            notes TEXT,
            created_at TEXT NOT NULL
        )
    """)
    # Migrate old schema if needed
    columns = {row[1] for row in db.execute("PRAGMA table_info(coffees)").fetchall()}
    migrations = {
        "roaster": "TEXT",
        "country_grown": "TEXT",
        "country_roasted": "TEXT",
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
    db.commit()
    db.close()


MAX_DIMENSION = 1568  # Claude's optimal long-edge size
MAX_BYTES = 600 * 1024  # 600 KB
DEBUG_IMAGE_DIR = Path(__file__).parent / "debug_images"
DEBUG_IMAGE_DIR.mkdir(exist_ok=True)


def prepare_image(file_storage) -> tuple[str, str]:
    """Read uploaded image, downscale if needed, and return as JPEG under 600 KB."""
    raw = file_storage.read()
    img = Image.open(io.BytesIO(raw))
    img = img.convert("RGB")

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

    return base64.standard_b64encode(buf.getvalue()).decode("utf-8"), "image/jpeg"


def extract_coffee_details(image_data: str, media_type: str) -> dict:
    """Send image to Claude and extract coffee details as structured data."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY_FOR_LOOKUP"))
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
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
                            '{"roastery": "...", "name": "...", "origin": "...", "country_grown": "...", '
                            '"country_roasted": "...", "process": "...", "roast_level": "...", '
                            '"tasting_notes": "...", "weight": "...", "price": "...", "other": "..."}\n'
                            "For origin, list all countries/regions separated by commas if multiple (e.g. a blend). "
                            "country_grown is the country where the beans were grown. "
                            "country_roasted is the country where the beans were roasted. "
                            "For tasting_notes, copy the exact words from the bag (e.g. 'Björnbär / Röd Grapefrukt / Tranbär'). "
                            "Use null for fields you can't find. Be concise."
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
        image_data, media_type = prepare_image(f)
        app.logger.info(f"Prepared image, media_type: {media_type}, data length: {len(image_data)}")
        details = extract_coffee_details(image_data, media_type)
        # Match scanned roastery against known roasters
        matched_roaster = None
        scanned_roastery = details.get("roastery") or details.get("roaster")
        if scanned_roastery:
            db = get_db()
            matched_roaster = match_roaster(scanned_roastery, db)
            db.close()
            if matched_roaster:
                details["roastery"] = matched_roaster
        coffee = CoffeeBean.from_scan(details)
        result = coffee.to_dict()
        result["matched_roaster"] = matched_roaster
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Scan error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/coffees", methods=["GET"])
def list_coffees():
    db = get_db()
    rows = db.execute("SELECT * FROM coffees ORDER BY created_at DESC").fetchall()
    coffees = []
    for r in rows:
        avg = db.execute("SELECT ROUND(AVG(score), 1) FROM tastings WHERE coffee_id = ?", (r["id"],)).fetchone()[0]
        coffees.append(CoffeeBean.from_row(r).to_dict(average_score=avg))
    db.close()
    return jsonify(coffees)


@app.route("/api/coffees", methods=["POST"])
def save_coffee():
    data = request.json
    coffee = CoffeeBean(
        roaster=data.get("roaster"),
        name=data.get("name"),
        country_grown=data.get("country_grown"),
        country_roasted=data.get("country_roasted"),
        origin=data.get("origin"),
        process=data.get("process"),
        roast_level=data.get("roast_level"),
        tasting_notes=data.get("tasting_notes"),
        weight=data.get("weight"),
        price=data.get("price"),
        other=data.get("other"),
        notes=data.get("notes"),
    )
    row = coffee.to_row()
    columns = ", ".join(row.keys())
    placeholders = ", ".join("?" for _ in row)
    db = get_db()
    db.execute(f"INSERT INTO coffees ({columns}) VALUES ({placeholders})", list(row.values()))
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
        origin=data.get("origin"),
        process=data.get("process"),
        roast_level=data.get("roast_level"),
        tasting_notes=data.get("tasting_notes"),
        weight=data.get("weight"),
        price=data.get("price"),
        other=data.get("other"),
        notes=data.get("notes"),
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
        score=data.get("score"),
        notes=data.get("notes"),
    )
    row = tasting.to_row()
    columns = ", ".join(row.keys())
    placeholders = ", ".join("?" for _ in row)
    cursor = db.execute(f"INSERT INTO tastings ({columns}) VALUES ({placeholders})", list(row.values()))
    db.commit()
    tasting.id = cursor.lastrowid
    db.close()
    return jsonify(tasting.to_dict()), 201


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


init_db()

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5555, debug=debug)
