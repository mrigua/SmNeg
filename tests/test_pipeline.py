# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Said Mrigua
import numpy as np
import pytest

from smneg.engine import OfficialFilmEngine

RNG = np.random.default_rng(3)
BASE = RNG.random((40, 60, 3), dtype=np.float32)


def run(**overrides):
    args = dict(cyan_points=0, magenta_points=0, yellow_points=0, density_step=0, contrast=1.0,
                saturation=1.0, rotation=0, mirror=False, auto_crop=False, show_clipping=False)
    args.update(overrides)
    return OfficialFilmEngine.apply_pipeline(BASE.copy(), **args)


def test_output_is_uint8_rgb():
    out = run()
    assert out.dtype == np.uint8 and out.shape == (40, 60, 3)


def test_float_output_is_normalized():
    out = run(output_float=True)
    assert out.dtype == np.float32 and 0.0 <= out.min() and out.max() <= 1.0


def test_input_is_not_modified():
    before = BASE.copy()
    run(cyan_points=10, density_step=5, contrast=1.3, saturation=1.2)
    np.testing.assert_array_equal(BASE, before)


def test_density_up_brightens():
    assert run(density_step=15).mean() > run().mean()


def test_cyan_points_dim_the_red_channel_only():
    base, shifted = run(), run(cyan_points=10)
    assert shifted[:, :, 0].mean() < base[:, :, 0].mean()
    np.testing.assert_array_equal(shifted[:, :, 1:], base[:, :, 1:])


@pytest.mark.parametrize("rotation, shape", [(0, (40, 60)), (90, (60, 40)), (180, (40, 60)), (270, (60, 40))])
def test_rotation_shape(rotation, shape):
    assert run(rotation=rotation).shape[:2] == shape


def test_mirror_flips_horizontally():
    mirrored = run(mirror=True)
    np.testing.assert_array_equal(mirrored[:, ::-1], run())


def test_auto_crop_removes_5_percent_border():
    assert run(auto_crop=True).shape[:2] == (36, 54)


def test_clipping_preview_marks_pixels():
    out = OfficialFilmEngine.apply_pipeline(
        np.ones((10, 10, 3), np.float32), 0, 0, 0, 0, 1.0, 1.0, 0, False, False, True)
    assert (out == [255, 0, 0]).all()
