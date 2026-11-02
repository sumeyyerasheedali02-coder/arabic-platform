"""Convert numbered unit PNG banners to responsive WebP assets (requires Pillow)."""
import argparse
import re
from pathlib import Path

from PIL import Image, ImageOps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "public/images/units")
    args = parser.parse_args()
    sources = {}
    for path in args.source.glob("*.png"):
        match = re.match(r"unit_(\d+)(?:_|\.)", path.name)
        if match:
            number = int(match[1])
            if number in sources:
                parser.error(f"Duplicate unit number: {number}")
            sources[number] = path
    if set(sources) != set(range(1, 49)):
        parser.error("Expected exactly one PNG for each unit 01–48")
    args.output.mkdir(parents=True, exist_ok=True)
    total = 0
    for number, path in sorted(sources.items()):
        with Image.open(path) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
            for width, suffix in ((1800, ""), (960, "-small")):
                banner = image.copy()
                banner.thumbnail((width, round(width * image.height / image.width)), Image.Resampling.LANCZOS)
                target = args.output / f"unit-{number:02d}{suffix}.webp"
                # Keep every source pixel in the full-size banner. Mobile uses
                # a high-quality downsample, never a heavily enlarged crop.
                if width == 1800:
                    banner.save(target, "WEBP", lossless=True, method=6)
                else:
                    banner.save(target, "WEBP", quality=94, method=6)
                total += target.stat().st_size
    original = sum(path.stat().st_size for path in sources.values())
    print(f"48 banners, 96 WebP files: {original:,} source bytes -> {total:,} output bytes (both sizes)")


if __name__ == "__main__":
    main()
