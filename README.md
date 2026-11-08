# SMneg

*SMneg = Said Mrigua negative.*

[![CI](https://github.com/saidmrigua/SmNeg/actions/workflows/ci.yml/badge.svg)](https://github.com/saidmrigua/SmNeg/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Platforms](https://img.shields.io/badge/platforms-macOS%20%7C%20Windows-lightgrey)

Invert camera-scanned film negatives (RAW or TIFF) into positives, adjust them with a printer-lights style
color workflow, and export to JPEG or 16-bit TIFF with proper metadata.

![Before and after: a color negative photographed with a digital camera, and the SMneg result](docs/images/harbour-before-after.jpg)

<sub>Left: the negative as photographed (Nikon NEF, linear data). Right: SMneg result with default settings, no manual correction.
Photographs © 2026 Said Mrigua, all rights reserved (the code is Apache-2.0, the photographs are not).</sub>

More examples: [crates](docs/images/crates-before-after.jpg) · [building](docs/images/building-before-after.jpg)

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

## Screenshots

![Grid view with six frames, two of them marked PASS](docs/images/ui-grid.png)

<sub>Grid view: six frames per page, printer-lights keys, density and tone controls. Frames marked PASS are skipped at export.</sub>

| Enlarged view | Export |
|---|---|
| ![Enlarged view](docs/images/ui-enlarged.png) | ![Export dialog](docs/images/ui-export.png) |

| Session information | Keyboard shortcuts |
|---|---|
| ![Session information dialog](docs/images/ui-session-info.png) | ![Keyboard shortcuts](docs/images/ui-shortcuts.png) |

## Download
Pre-built apps (macOS `.dmg`, Windows `.zip`), a wheel and an sdist are attached to every
[GitHub Release](https://github.com/saidmrigua/SmNeg/releases). The apps are not code-signed: on macOS right-click the app
and choose *Open* the first time; on Windows choose *More info → Run anyway* in SmartScreen.

## Install from source
Requires Python 3.10 or newer.
```bash
git clone https://github.com/saidmrigua/SmNeg.git smneg && cd smneg
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

## Documentation
- [How it works](docs/how-it-works.md): decoding, density inversion, color pipeline, module map
- [Using SMneg: a typical session](docs/workflow.md)
- [Keyboard shortcuts](docs/shortcuts.md)

## Tests
```bash
pip install -e ".[tiff,dev]" && pytest
```
`tests/test_engine_golden.py` guards the inversion math against reference results; the other tests cover
the color pipeline, crop, flat-field, filename templates, sessions, settings migration, TIFF/XMP and the hot folder.

## License
Code: Apache License 2.0, Copyright 2026 Said Mrigua. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

Photographs in `docs/images/` are © 2026 Said Mrigua, all rights reserved. They are included to illustrate the
software and may not be reused without permission.
