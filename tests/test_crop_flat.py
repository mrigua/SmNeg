# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Said Mrigua
import numpy as np
import pytest

from smneg.crop import apply_crop, straighten_image
from smneg.flat_field import apply_flat_field, build_flat_field


def test_crop_none_returns_same_image():
    image = np.zeros((10, 20, 3), np.float32)
    assert apply_crop(image, None) is image


def test_crop_bounds_are_fractions():
    image = np.arange(100 * 200 * 3, dtype=np.float32).reshape(100, 200, 3)
    assert apply_crop(image, (0.25, 0.1, 0.75, 0.9)).shape[:2] == (80, 100)


def test_crop_never_returns_empty():
    assert apply_crop(np.zeros((10, 10, 3), np.float32), (0.999, 0.999, 1.0, 1.0)).size > 0


def test_straighten_zero_keeps_shape():
    image = np.random.default_rng(0).random((30, 40, 3), dtype=np.float32)
    assert straighten_image(image, 0.0).shape == image.shape


def test_flat_field_corrects_vignetting():
    y, x = np.mgrid[0:64, 0:96]
    vignette = (1.0 - 0.3 * (((x - 48) / 48) ** 2 + ((y - 32) / 32) ** 2) / 2).astype(np.float32)
    reference = np.dstack([vignette] * 3) * 0.6
    gain = build_flat_field(reference)
    flat = apply_flat_field(reference.copy(), gain)
    assert flat.std() < reference.std() * 0.2


def test_flat_field_rejects_overexposed_reference():
    with pytest.raises(ValueError, match="overexposed"):
        build_flat_field(np.ones((32, 32, 3), np.float32))


def test_flat_field_rejects_mismatched_framing():
    gain = build_flat_field(np.full((32, 48, 3), 0.5, np.float32))
    with pytest.raises(ValueError, match="framing"):
        apply_flat_field(np.zeros((48, 48, 3), np.float32), gain)
