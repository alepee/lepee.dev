#!/usr/bin/env python3
"""Build social preview images (1200x630 JPEG on the site's paper colour)
from each post's header illustration: src/assets/illustrations/<slug>/00-header.png
-> src/assets/og/<slug>.jpg. Transparent line art would render on black otherwise."""
from pathlib import Path
from PIL import Image

PAPER = (248, 247, 243)
W, H = 1200, 630
root = Path(__file__).resolve().parent.parent
out = root / "src/assets/og"
out.mkdir(parents=True, exist_ok=True)
for header in sorted((root / "src/assets/illustrations").glob("*/00-header.png")):
    art = Image.open(header).convert("RGBA")
    art.thumbnail((W - 80, H - 40))
    canvas = Image.new("RGBA", (W, H), PAPER + (255,))
    canvas.alpha_composite(art, ((W - art.width) // 2, (H - art.height) // 2))
    canvas.convert("RGB").save(out / f"{header.parent.name}.jpg", "JPEG", quality=85)
    print(header.parent.name)
