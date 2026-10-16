"""Add a phone-style device frame to each app screenshot.

Source screenshots are 1080x2400 (phone aspect). This script overlays:
  - dark bezel (rounded rectangle outside the screenshot)
  - screen with rounded corners (so the screenshot is "fitted" inside)
  - small notch (pill at top center)
  - home indicator (small bar at bottom center)
Output: same files, regenerated in place as JPEG.
"""
from PIL import Image, ImageDraw
from pathlib import Path

SRC_DIR = Path("docs/app-screenshots")

# Frame parameters — sized so the bezel reads ~12px on a 280px display.
BEZEL_TOP = 30       # status bar / notch region
BEZEL_BOTTOM = 80    # chin with home indicator
BEZEL_SIDE = 50      # left/right bezel
OUTER_RADIUS = 60    # outer corner radius
INNER_RADIUS = 50    # screen corner radius (where screenshot meets bezel)
PHONE_COLOR = (15, 15, 15)

NOTCH_W = 140
NOTCH_H = 28
NOTCH_COLOR = (0, 0, 0)

INDICATOR_W = 110
INDICATOR_H = 5
INDICATOR_COLOR = (140, 140, 140)


def frame_one(src_path: Path) -> None:
    img = Image.open(src_path).convert("RGB")
    w, h = img.size

    new_w = w + 2 * BEZEL_SIDE
    new_h = h + BEZEL_TOP + BEZEL_BOTTOM

    # Build the phone body as RGBA so we can composite the screen cleanly.
    body = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    body_draw = ImageDraw.Draw(body)
    body_draw.rounded_rectangle(
        (0, 0, new_w, new_h),
        radius=OUTER_RADIUS,
        fill=PHONE_COLOR + (255,),
    )

    # Round the screen so it sits inside the bezel with smooth corners.
    screen_mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(screen_mask).rounded_rectangle(
        (0, 0, w, h),
        radius=INNER_RADIUS,
        fill=255,
    )
    body.paste(img, (BEZEL_SIDE, BEZEL_TOP), screen_mask)

    # Notch (pill at top center).
    notch_x = (new_w - NOTCH_W) // 2
    body_draw.rounded_rectangle(
        (notch_x, 10, notch_x + NOTCH_W, 10 + NOTCH_H),
        radius=14,
        fill=NOTCH_COLOR,
    )

    # Home indicator.
    ind_x = (new_w - INDICATOR_W) // 2
    ind_y = new_h - 30
    body_draw.rounded_rectangle(
        (ind_x, ind_y, ind_x + INDICATOR_W, ind_y + INDICATOR_H),
        radius=2,
        fill=INDICATOR_COLOR,
    )

    body.convert("RGB").save(src_path, quality=92, optimize=True)


def main() -> None:
    for i in range(1, 12):
        path = SRC_DIR / f"{i}.jpg"
        if not path.exists():
            print(f"skip (missing): {path}")
            continue
        frame_one(path)
        print(f"framed: {path}")


if __name__ == "__main__":
    main()
