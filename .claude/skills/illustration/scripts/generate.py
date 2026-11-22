#!/usr/bin/env python3
"""Generate one illustration with the OpenAI Images API.

Writes a transparent "pure ink" PNG: black strokes whose opacity follows the
drawing's density, nothing else. The site can then invert it in dark mode. Reads OPENAI_API_KEY from the environment.

  generate.py --prompt-file p.txt --out img.png [--size 1536x1024] [--draft]
              [--reference style.png] [--complexity medium]

--draft      fast model, low quality (for the visual script round).
--reference  an existing illustration whose line style must be matched;
             switches to the edits endpoint with that image as reference.
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

API = "https://api.openai.com/v1/images"
MODEL_FINAL = "gpt-image-2.6-sunburst"
MODEL_DRAFT = "gpt-image-2.6-flare"


def call(endpoint: str, payload: dict, key: str) -> dict:
    req = urllib.request.Request(
        f"{API}/{endpoint}",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        sys.exit(f"OpenAI API error {err.code}: {err.read().decode(errors='replace')}")


def to_ink(png: bytes) -> Image.Image:
    """Flatten on white, then turn darkness into alpha over pure black.

    The model fills the inside of shapes with semi-opaque white; inverted in
    dark mode those fills would become black blobs. Pure ink has no fills.
    """
    src = Image.open(BytesIO(png)).convert("RGBA")
    flat = Image.new("RGBA", src.size, (255, 255, 255, 255))
    flat.alpha_composite(src)
    ink = Image.new("RGBA", src.size, (0, 0, 0, 0))
    ink.putalpha(ImageOps.invert(flat.convert("L")))
    return ink


def trim_vertical(img: Image.Image, margin: float = 0.04) -> Image.Image:
    """Crop the empty bands above and below the drawing, keeping the full width."""
    bbox = img.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
    if not bbox:
        return img
    pad = int(margin * img.height)
    return img.crop((0, max(0, bbox[1] - pad), img.width, min(img.height, bbox[3] + pad)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-file", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--size", default="1536x1024")
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--complexity", default="medium", choices=["low", "medium", "high"])
    parser.add_argument("--trim", action="store_true", help="crop empty space above and below the drawing (inline images)")
    args = parser.parse_args()

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY is not set (it lives in the user's shell profile).")

    payload = {
        "model": MODEL_DRAFT if args.draft else MODEL_FINAL,
        "prompt": args.prompt_file.read_text(),
        "size": args.size,
        "quality": "low" if args.draft else "high",
        "complexity": args.complexity,
        "background": "transparent",
        "output_format": "png",
        "n": 1,
    }

    if args.reference:
        ref = base64.b64encode(args.reference.read_bytes()).decode()
        payload["images"] = [{"image_url": f"data:image/png;base64,{ref}"}]
        payload["prompt"] = (
            "Draw a NEW image described below. The attached image is only a style reference: "
            "match its line weight, hatching and stippling exactly, not its subject.\n\n"
            + payload["prompt"]
        )
        result = call("edits", payload, key)
    else:
        result = call("generations", payload, key)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    ink = to_ink(base64.b64decode(result["data"][0]["b64_json"]))
    if args.trim:
        ink = trim_vertical(ink)
    ink.save(args.out, optimize=True)
    usage = result.get("usage", {})
    print(f"{args.out} ({payload['model']}, {payload['quality']}, tokens out: {usage.get('output_tokens', '?')})")


if __name__ == "__main__":
    main()
