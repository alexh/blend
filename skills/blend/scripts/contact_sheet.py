#!/usr/bin/env python3
"""Labelled contact sheet from frames.

    contact_sheet.py frames/ -o sheet.png                  # every PNG/JPG in the folder, name order
    contact_sheet.py a.png b.png c.png -o sheet.png --cols 3
    contact_sheet.py frames/ -o hands.png --crop 0.40,0.55,0.65,0.80 --scale 1
    contact_sheet.py frames/ -o sheet.png --every 3        # every third frame

--crop takes fractions (x0,y0,x1,y1) of each frame, for contact points (a hand on a body, a prop in a grip)
that a full-frame sheet is too small to show. --scale is the thumbnail size as a fraction of the (cropped)
frame. Labels are the file names, so name frames by time (shot-0.25s.png) or index.
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def frames(inputs: list[str], every: int) -> list[Path]:
    paths: list[Path] = []
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            paths += sorted(q for q in p.iterdir() if q.suffix.lower() in EXTS)
        elif p.suffix.lower() in EXTS:
            paths.append(p)
    return paths[::max(1, every)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--scale", type=float, default=0.25)
    ap.add_argument("--every", type=int, default=1)
    ap.add_argument("--crop", help="x0,y0,x1,y1 as fractions of each frame")
    ap.add_argument("--bg", default="#1a1a1a")
    ap.add_argument("--label", default="#ff8a3d")
    a = ap.parse_args()

    paths = frames(a.inputs, a.every)
    if not paths:
        print("no frames found", file=sys.stderr)
        return 1
    crop = [float(v) for v in a.crop.split(",")] if a.crop else None
    tiles = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        if crop:
            w, h = im.size
            im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
        tw, th = max(1, int(im.width * a.scale)), max(1, int(im.height * a.scale))
        tiles.append((p.name, im.resize((tw, th), Image.LANCZOS)))

    tw = max(t.width for _, t in tiles)
    th = max(t.height for _, t in tiles)
    pad, label_h = 4, 16
    cols = min(a.cols, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + label_h + pad) + pad), a.bg)
    draw = ImageDraw.Draw(sheet)
    for i, (name, tile) in enumerate(tiles):
        x = pad + (i % cols) * (tw + pad)
        y = pad + (i // cols) * (th + label_h + pad)
        draw.text((x + 2, y + 2), name, fill=a.label)
        sheet.paste(tile, (x, y + label_h))
    sheet.save(a.out)
    print(f"{a.out}: {len(tiles)} frames, {cols}x{rows}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
