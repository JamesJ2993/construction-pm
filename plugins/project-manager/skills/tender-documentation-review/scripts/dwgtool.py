"""Render and crop drawing sheets for review and for register snapshots.

Set SRC and NAME for the job, then call with the full python path:

  python dwgtool.py overview <page>              whole sheet, 2400px wide - start here
  python dwgtool.py tiles    <page> [cols] [rows] overlapping tiles for reading small text
  python dwgtool.py zoom     <page> <x0> <y0> <x1> <y1> [name]
  python dwgtool.py snap     <page> <x0> <y0> <x1> <y1> <REF>

x0..y1 are FRACTIONS of sheet width/height (0-1), so they are independent of source resolution.
Locate text precisely first with PyMuPDF rather than guessing coordinates:

    page.search_for('HUMPER')  ->  rect; divide by page.rect.x1 / .y1 for fractions

Outputs land in <script dir>/img (overview, tiles, zoom) and <script dir>/snaps (snap).
Paths are printed so they can be Read straight after.
"""
import os
import sys

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

# --- set these for the job ---------------------------------------------------
SRC = r"<folder of page images>"
NAME = "<prefix>_page-%04d.jpg"      # %04d is the 1-based page number
# -----------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img")
SNAPS = os.path.join(HERE, "snaps")
os.makedirs(IMG, exist_ok=True)
os.makedirs(SNAPS, exist_ok=True)

TARGET_W = 2400


def load(page):
    return Image.open(os.path.join(SRC, NAME % int(page)))


def save(im, path, max_w=TARGET_W):
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * max_w / im.width)), Image.LANCZOS)
    im.convert("RGB").save(path, "JPEG", quality=88, optimize=True)
    print(path)


def main():
    cmd, page = sys.argv[1], int(sys.argv[2])
    im = load(page)
    W, H = im.size

    if cmd == "overview":
        save(im, os.path.join(IMG, f"p{page:02d}-overview.jpg"))

    elif cmd == "tiles":
        cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        rows = int(sys.argv[4]) if len(sys.argv) > 4 else 2
        ov = 0.06                      # overlap so nothing is lost on a seam
        for r in range(rows):
            for c in range(cols):
                box = (max(0, int((c / cols - ov) * W)),
                       max(0, int((r / rows - ov) * H)),
                       min(W, int(((c + 1) / cols + ov) * W)),
                       min(H, int(((r + 1) / rows + ov) * H)))
                save(im.crop(box), os.path.join(IMG, f"p{page:02d}-r{r+1}c{c+1}.jpg"))

    elif cmd in ("zoom", "snap"):
        x0, y0, x1, y1 = (float(v) for v in sys.argv[3:7])
        crop = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
        if cmd == "snap":
            save(crop, os.path.join(SNAPS, f"{sys.argv[7]}.jpg"), max_w=1400)
        else:
            nm = sys.argv[7] if len(sys.argv) > 7 else f"z{int(x0*100)}-{int(y0*100)}"
            save(crop, os.path.join(IMG, f"p{page:02d}-{nm}.jpg"))
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
