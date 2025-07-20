import argparse

import numpy as np
from PIL import Image


def main(img_path: str, tile_size: int = 6, output_path: str | None = None) -> None:
    with Image.open(img_path).convert("L") as img:
        pixels = np.asarray(img)
        height, width = pixels.shape

        dotted = np.full_like(pixels, 255)

        for y in range(0, height, tile_size):
            for x in range(0, width, tile_size):
                tile = pixels[y:y + tile_size, x:x + tile_size]
                tile_height, tile_width = tile.shape

                avg_grayness = int(tile.mean())

                cx, cy = tile_width // 2, tile_height // 2
                radius = min(tile_width, tile_height) // 2
                r2 = radius ** 2

                for dy in range(tile_height):
                    for dx in range(tile_width):
                        if (dx - cx) ** 2 + (dy - cy) ** 2 <= r2:
                            dotted[y + dy, x + dx] = avg_grayness

        result = Image.fromarray(dotted)

        if output_path is not None:
            result.save(output_path)
        else:
            result.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert an image into a dotted grayscale version"
    )
    parser.add_argument("image_path", type=str, help="Path to the input image")
    parser.add_argument(
        "--tile-size",
        type=int,
        default=6,
        help="Tile size for dots (default-6)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Optional path to save the dotted image"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(img_path=args.image_path, tile_size=args.tile_size, output_path=args.output)
