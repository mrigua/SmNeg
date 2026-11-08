# SMneg

*SMneg = Said Mrigua negative.*

Invert camera-scanned film negatives (RAW or TIFF) into positives, adjust them with a
printer-lights style color workflow, and export to JPEG or 16-bit TIFF with proper metadata.

Built for photographers who scan film with a digital camera. The workflow will feel familiar to people
who have used Frontier-style scanning controllers. SMneg is an independent project, not affiliated
with FUJIFILM or Nikon (see [NOTICE](NOTICE)).

## Features
- Density-based negative inversion engine (`engine.py`), RAW (`.raf .nef .nrw .dng`), TIFF and JPEG sources
- CMY / RGB color keys, density, contrast, saturation, tone profiles, sharpness, rotation, mirror, auto and manual crop
- In-place zoom with full-resolution decoding, flat-field (diffuser) correction, clipping preview
- Undo / redo, copy-paste settings, 6-frame navigation, keyboard help on `F1`
- Sessions: enter client / film / copyright information once at *New Session*; it pre-fills the export dialog
- Export to JPEG or 16-bit TIFF, Photo Mechanic style filename templates (`{filenamebase}_{seqn}`), embedded XMP/EXIF
  metadata, `metadata.json` sidecar, pipelined for speed
- Hot Folder watching; on macOS, optional capture trigger for Nikon NX Tether

## Install
Requires Python 3.10 or newer.
```bash
git clone <your-repo-url> smneg && cd smneg
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[tiff]"        # "tiff" adds XMP metadata in 16-bit TIFF
```

## Run
```bash
smneg                 # or: python -m smneg   or: python smneg.py
```

## Configuration
Settings (last folders, export options, presets, autocomplete history) are stored with Qt's `QSettings`
under the name *SMneg*; nothing is sent over the network and no API keys are used. Settings saved
by the pre-release version are imported automatically on first launch. Each session stores its data in
`smneg-session.json` inside the session folder (older `frontier-session.json` files still open).

## Platform notes
| | macOS | Windows |
|---|---|---|
| Inversion, zoom, export | yes | expected to work, see limits |
| Nikon NX Tether capture button | yes (needs Accessibility permission) | disabled |

## Known limits
- Developed and used on macOS. Windows support has not been tested on real hardware yet; CI runs the
  non-GUI tests on both systems.
- Full-resolution (45 MP class) frames need several GB of RAM (zoom caches the last full frame).
- RAW demosaicing speed is bounded by LibRaw. The inversion itself is parallelized.
- Version bounds in `pyproject.toml` are conservative; the app was tested with PySide6 6.8, NumPy 2.2,
  Pillow 12, rawpy 0.27, OpenCV 5.0 on Python 3.10.
- `window.py` is large; splitting it is planned.

## Tests
```bash
pip install -e ".[tiff,dev]" && pytest
```
`tests/test_engine_golden.py` guards the inversion math against reference results.

## License
Apache License 2.0, Copyright 2026 Said Mrigua. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
