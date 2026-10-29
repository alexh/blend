#!/usr/bin/env python3
"""Alpha bounding-box margins: catches subjects cropped at an image edge.

    edge_check.py renders/*.png --min 3
    edge_check.py renders/ --min 3 --alpha 8 --checker review.png

For each image, prints its size and the clear (fully transparent) pixels left, top, right and bottom of the
opaque content. Exits 1 if any image has fewer than --min clear pixels on any side, which means something
touches or runs off the edge: a crop. Images without alpha are reported and treated as failing, because
there's nothing to measure. --checker writes all images on a contrasting checkerboard, to show halos and
fringes.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def margins(im: Image.Image, threshold: int) -> tuple[int, int, int, int] | None:
    a = np.asarray(im.getchannel("A"))
    ys, xs = np.nonzero(a > threshold)
    if len(xs) == 0:
        return None
    h, w = a.shape
    return int(xs.min()), int(ys.min()), int(w - 1 - xs.max()), int(h - 1 - ys.max())


def checker(images: list[tuple[str, Image.Image]], out: str, cell: int = 8) -> None:
    pad = 12
    W = sum(im.width for _, im in images) + pad * (len(images) + 1)
    H = max(im.height for _, im in images) + pad * 2
    yy, xx = np.mgrid[0:H, 0:W]
    board = np.where(((xx // cell) + (yy // cell)) % 2 == 0, 200, 90).astype(np.uint8)
    sheet = Image.fromarray(np.stack([board, np.full_like(board, 60), board], axis=-1), "RGB")
    x = pad
    for _, im in images:
        sheet.paste(im, (x, pad), im)
        x += im.width + pad
    sheet.save(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--min", type=int, default=3, help="minimum clear pixels on every side")
    ap.add_argument("--alpha", type=int, default=0, help="alpha above this counts as opaque")
    ap.add_argument("--checker", help="write a checkerboard preview of every image here")
    a = ap.parse_args()

    paths: list[Path] = []
    for item in a.inputs:
        p = Path(item)
        paths += sorted(p.glob("*.png")) if p.is_dir() else [p]
    failed, shown = 0, []
    for p in paths:
        im = Image.open(p)
        if "A" not in im.getbands():
            print(f"{p.name:32} {im.width}x{im.height}  no alpha channel  FAIL")
            failed += 1
            continue
        im = im.convert("RGBA")
        m = margins(im, a.alpha)
        if m is None:
            print(f"{p.name:32} {im.width}x{im.height}  fully transparent  FAIL")
            failed += 1
            continue
        ok = min(m) >= a.min
        failed += not ok
        print(f"{p.name:32} {im.width}x{im.height}  clear px: left {m[0]:3} top {m[1]:3} right {m[2]:3} bottom {m[3]:3}  "
              + ("OK" if ok else "FAIL"))
        shown.append((p.name, im))
    if a.checker and shown:
        checker(shown, a.checker)
        print(f"checker preview: {a.checker}")
    print(f"{len(paths) - failed}/{len(paths)} pass (min {a.min} px)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
