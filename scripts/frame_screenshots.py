"""Add a thin device frame to each app screenshot.

Source screenshots are 1080x2400 (phone aspect). This script:
  - rounds the screenshot corners
  - pads with a small transparent/white margin
  - draws a thin gray rounded-rectangle outline around the screenshot
No notch, no home indicator, no dark bezel — just a clean outline.
"""
from PIL import Image, ImageDraw
from pathlib import Path

SRC_DIR = Path("docs/app-screenshots")

MARGIN = 32            # padding around the screenshot (becomes the border zone)
BORDER_W = 8           # thickness of the visible border line
BORDER_COLOR = (60, 60, 60)  # dark gray for clear visibility
RADIUS = 50            # corner radius of the screenshot itself
BG = (255, 255, 255)   # background color (white, matches GitHub README)


def frame_one(src_path: Path) -> None:
    img = Image.open(src_path).convert("RGB")
    w, h = img.size

    # Round the screenshot corners
    screen_mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(screen_mask).rounded_rectangle(
        (0, 0, w, h), radius=RADIUS, fill=255
    )

    # New image with margin (white background)
    new_w = w + 2 * MARGIN
    new_h = h + 2 * MARGIN
    new_img = Image.new("RGB", (new_w, new_h), BG)

    # Paste rounded screenshot onto white background
    new_img.paste(img, (MARGIN, MARGIN), screen_mask)

    # Draw thin border around outer edge
    draw = ImageDraw.Draw(new_img)
    draw.rounded_rectangle(
        (0, 0, new_w - 1, new_h - 1),
        radius=RADIUS + MARGIN,
        outline=BORDER_COLOR,
        width=BORDER_W,
    )

    new_img.save(src_path, quality=92, optimize=True)


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
