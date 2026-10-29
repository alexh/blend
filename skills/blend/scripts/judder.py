#!/usr/bin/env python3
"""Repeated frames and motion steadiness of a RAW clip (before grain, static or other overlays).

    judder.py frames/                       # a folder of frames in order (ffmpeg -i raw.mp4 frames/%05d.png)
    judder.py frames/ --from 40 --to 160    # only a steady move, e.g. a constant pan
    judder.py frames/ --repeat 0.5 --max-repeats 0.05 --max-swing 0.25

Per consecutive pair it measures the mean absolute difference on a downscaled greyscale copy. A pair under
--repeat counts as a repeated (frozen) frame. Over the moving pairs it reports the median motion and how far
the motion swings around it. Exits 1 when repeats exceed --max-repeats, or when the 10th–90th percentile
swing exceeds --max-swing of the median.

Run it on raw captures. Animated overlays change every frame and hide frozen footage underneath.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def load(p: Path, width: int) -> np.ndarray:
    im = Image.open(p).convert("L")
    h = max(1, round(im.height * width / im.width))
    return np.asarray(im.resize((width, h), Image.BILINEAR), dtype=np.float32)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--from", dest="start", type=int, default=0)
    ap.add_argument("--to", dest="end", type=int)
    ap.add_argument("--width", type=int, default=320)
    ap.add_argument("--repeat", type=float, default=0.5, help="mean abs diff (0-255) under which a frame is a repeat")
    ap.add_argument("--max-repeats", type=float, default=0.05)
    ap.add_argument("--max-swing", type=float, default=0.25)
    a = ap.parse_args()

    paths = sorted(p for p in Path(a.folder).iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
    paths = paths[a.start:a.end]
    if len(paths) < 3:
        print("need at least 3 frames", file=sys.stderr)
        return 2
    prev, diffs = load(paths[0], a.width), []
    for p in paths[1:]:
        cur = load(p, a.width)
        diffs.append(float(np.abs(cur - prev).mean()))
        prev = cur
    d = np.array(diffs)
    repeats = float((d < a.repeat).mean())
    moving = d[d >= a.repeat]
    print(f"frames {len(paths)}  pairs {len(d)}  repeated {repeats:.1%} (bar {a.max_repeats:.0%})")
    ok = repeats <= a.max_repeats
    if len(moving) >= 3:
        med = float(np.median(moving))
        lo, hi = np.percentile(moving, [10, 90])
        swing = max(med - lo, hi - med) / med if med > 0 else 0.0
        print(f"motion median {med:.2f}  p10 {lo:.2f}  p90 {hi:.2f}  swing ±{swing:.0%} (bar ±{a.max_swing:.0%})")
        ok = ok and swing <= a.max_swing
    else:
        print("too few moving pairs to judge steadiness")
    worst = np.argsort(d)[:5]
    print("lowest-motion pairs: " + ", ".join(f"{paths[i].name}->{paths[i + 1].name} ({d[i]:.2f})" for i in worst))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
