#!/usr/bin/env python3
"""Coffee Tracker - Untappd for coffee."""

import io
import json
import os
import base64
import sqlite3
import mimetypes
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import anthropic
from flask import Flask, render_template, request, jsonify
from PIL import Image
import pillow_heif

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
            roastery TEXT,
            name TEXT,
            origin TEXT,
            process TEXT,
            roast_level TEXT,
            tasting_notes TEXT,
            weight TEXT,
            other TEXT,
            rating INTEGER,
            notes TEXT,
            created_at TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()


def prepare_image(file_storage) -> tuple[str, str]:
    """Read uploaded image and convert to supported format if needed."""
    raw = file_storage.read()
    media_type = file_storage.content_type or mimetypes.guess_type(file_storage.filename)[0]

    if media_type in SUPPORTED_TYPES:
        return base64.standard_b64encode(raw).decode("utf-8"), media_type

    img = Image.open(io.BytesIO(raw))
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=85)
    return base64.standard_b64encode(buf.getvalue()).decode("utf-8"), "image/jpeg"


def extract_coffee_details(image_data: str, media_type: str) -> dict:
    """Send image to Claude and extract coffee details as structured data."""
    client = anthropic.Anthropic()
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
                            "This is a photo of a coffee bag. Extract details and respond with ONLY valid JSON, no markdown:\n"
                            '{"roastery": "...", "name": "...", "origin": "...", "process": "...", '
                            '"roast_level": "...", "tasting_notes": "...", "weight": "...", "other": "..."}\n'
                            "For origin, list all countries/regions separated by commas if multiple (e.g. a blend). "
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
        return jsonify(details)
    except Exception as e:
        app.logger.error(f"Scan error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/coffees", methods=["GET"])
def list_coffees():
    db = get_db()
    rows = db.execute("SELECT * FROM coffees ORDER BY created_at DESC").fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/coffees", methods=["POST"])
def save_coffee():
    data = request.json
    db = get_db()
    db.execute(
        """INSERT INTO coffees (roastery, name, origin, process, roast_level,
           tasting_notes, weight, other, rating, notes, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            data.get("roastery"),
            data.get("name"),
            data.get("origin"),
            data.get("process"),
            data.get("roast_level"),
            data.get("tasting_notes"),
            data.get("weight"),
            data.get("other"),
            data.get("rating"),
            data.get("notes"),
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    db.commit()
    db.close()
    return jsonify({"status": "saved"}), 201


@app.route("/api/coffees/<int:coffee_id>", methods=["DELETE"])
def delete_coffee(coffee_id):
    db = get_db()
    db.execute("DELETE FROM coffees WHERE id = ?", (coffee_id,))
    db.commit()
    db.close()
    return jsonify({"status": "deleted"})


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
