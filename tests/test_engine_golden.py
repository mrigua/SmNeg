"""The inversion math must not change: compare with outputs produced by the original implementation."""
from pathlib import Path

import numpy as np
import pytest

from smneg import engine

DATA = np.load(Path(__file__).parent / "data" / "engine_golden.npz")
CASES = sorted(name[:-3] for name in DATA.files if name.endswith("_in"))


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("force_parallel", [False, True])
def test_inversion_matches_reference(case, force_parallel, monkeypatch):
    source = DATA[f"{case}_in"]
    monkeypatch.setattr(engine, "decode_negative", lambda path, full_resolution: source.copy())
    if force_parallel:
        monkeypatch.setattr(engine.OfficialFilmEngine, "PARALLEL_MIN_PIXELS", 0)
    result = engine.OfficialFilmEngine.load_negative_base("unused.tif")
    expected = DATA[f"{case}_out"]
    assert result.dtype == expected.dtype and result.shape == expected.shape
    np.testing.assert_allclose(result, expected, rtol=1e-5, atol=1e-6)
