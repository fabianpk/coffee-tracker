#!/usr/bin/env python3
"""Scan a coffee bag photo and extract details using Claude's vision."""

import io
import sys
import base64
import mimetypes
import anthropic
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

SUPPORTED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


def load_image(image_path: str) -> tuple[str, str]:
    """Load image and convert to a supported format if needed. Returns (base64_data, media_type)."""
    media_type, _ = mimetypes.guess_type(image_path)

    if media_type in SUPPORTED_TYPES:
        with open(image_path, "rb") as f:
            return base64.standard_b64encode(f.read()).decode("utf-8"), media_type

    # Convert unsupported formats (HEIC, TIFF, etc.) to JPEG
    img = Image.open(image_path)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=85)
    return base64.standard_b64encode(buf.getvalue()).decode("utf-8"), "image/jpeg"


def scan_coffee(image_path: str) -> str:
    image_data, media_type = load_image(image_path)

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
                            "This is a photo of a coffee bag. Extract the following details if visible:\n"
                            "- Roastery/Brand\n"
                            "- Coffee name\n"
                            "- Origin/Region\n"
                            "- Process (washed, natural, etc.)\n"
                            "- Roast level\n"
                            "- Tasting notes\n"
                            "- Weight\n"
                            "- Any other relevant details\n\n"
                            "If a field is not visible, skip it. Be concise."
                        ),
                    },
                ],
            }
        ],
    )
    return message.content[0].text


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scan_coffee.py <image_path>")
        sys.exit(1)

    print(scan_coffee(sys.argv[1]))
