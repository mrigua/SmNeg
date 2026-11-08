# Contributing

Thanks for helping! SMneg is a small PySide6 application.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[tiff,dev]"
pytest
```

## Ground rules
- **Do not change the inversion math** in `engine.py` (`OfficialFilmEngine.load_negative_base`) without discussion.
  `tests/test_engine_golden.py` compares its output with reference results; it must keep passing.
- Keep changes small and focused; add or update a test when you fix a bug.
- UI text is English. Run `python -m pyflakes src tests` before opening a pull request.
- By contributing you agree that your contribution is licensed under Apache-2.0.
