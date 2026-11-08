# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Said Mrigua
from pathlib import Path

from PIL import Image


CAMERA_TAGS = {
    271: "make", 272: "model", 33434: "exposure_time", 33437: "aperture",
    34855: "iso", 36867: "captured_at", 37386: "focal_length", 42036: "lens",
}
COMPARABLE_FIELDS = ("make", "model", "exposure_time", "aperture", "iso", "focal_length", "lens")


def read_camera_reference(path):
    reference = {"source": Path(path).name}
    try:
        with Image.open(path) as image:
            exif = image.getexif()
            capture = exif.get_ifd(34665)
            for tag, name in CAMERA_TAGS.items():
                value = capture.get(tag, exif.get(tag))
                if value is not None:
                    reference[name] = value if isinstance(value, (str, int, float)) else str(value)
    except (OSError, ValueError, SyntaxError, TypeError):
        pass
    return reference


def camera_differences(reference, current):
    return [
        key for key in COMPARABLE_FIELDS
        if key in reference and key in current and reference[key] != current[key]
    ]
