#!/usr/bin/env python3
"""Compute a secondary pixel-difference report for two rendered figures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("generated", type=Path)
    parser.add_argument("--pixel-threshold", type=int, default=0, choices=range(256))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--diff-image", type=Path)
    args = parser.parse_args()
    for path in (args.reference, args.generated):
        if not path.is_file():
            parser.error(f"file not found: {path}")
    try:
        from PIL import Image, ImageChops, ImageStat
    except ImportError as exc:
        raise SystemExit("Pillow is required to compare rendered figures") from exc

    reference = Image.open(args.reference).convert("RGBA")
    generated = Image.open(args.generated).convert("RGBA")
    report = {
        "reference": str(args.reference.resolve()),
        "generated": str(args.generated.resolve()),
        "reference_size": list(reference.size),
        "generated_size": list(generated.size),
        "same_dimensions": reference.size == generated.size,
    }
    if reference.size != generated.size:
        report["classification"] = "formatting_difference"
    else:
        diff = ImageChops.difference(reference, generated)
        stats = ImageStat.Stat(diff)
        grayscale = diff.convert("L")
        histogram = grayscale.histogram()
        changed = sum(histogram[args.pixel_threshold + 1 :])
        total = reference.width * reference.height
        report.update(
            {
                "mean_absolute_channel_difference": stats.mean,
                "max_channel_difference": [maximum for _, maximum in stats.extrema],
                "changed_pixel_fraction": changed / total if total else 0.0,
                "pixel_threshold": args.pixel_threshold,
                "classification": "exact_match" if diff.getbbox() is None else "formatting_difference",
            }
        )
        if args.diff_image:
            diff.save(args.diff_image)
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
