import numpy as np
import pytest

from smneg.export import save_tiff16

tifffile = pytest.importorskip("tifffile")


def test_16bit_tiff_roundtrip_with_xmp(tmp_path):
    pixels = (np.random.default_rng(1).random((30, 40, 3)) * 65535).astype(np.uint16)
    path = tmp_path / "out.tif"
    width, height = save_tiff16(path, pixels, {"film": "Portra 400", "first_name": "Ana", "last_name": "B"})
    assert (width, height) == (40, 30)
    with tifffile.TiffFile(path) as tif:
        assert tif.pages[0].dtype == np.uint16
        assert b"Portra 400" in tif.pages[0].tags["XMP"].value
    np.testing.assert_array_equal(tifffile.imread(path), pixels)
