# Changelog

All notable changes are listed here. Format based on [Keep a Changelog](https://keepachangelog.com/),
versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]
### Planned
- Split `window.py` into smaller modules (needs GUI testing).
- Code signing / notarization of the macOS app and signing of the Windows app.
- Real-hardware testing on Windows.

## [0.1.0] - 2026-11-08
First public release. SMneg is the open-source version of an existing in-house film-negative inversion tool
(previously an unreleased "Frontier SP-500 Master v6" controller).

### Added
- Tests (44) including a golden test that pins the inversion engine to reference outputs; CI on macOS and Windows.
- Documentation (`docs/`), screenshots, GitHub Release with macOS `.dmg`, Windows `.zip`, wheel and sdist.
- Session information at *New Session*, with presets, autocomplete and validation; it pre-fills the export dialog.
- Export: JPEG (8-bit) and TIFF (16-bit, XMP), filename templates with variables, `metadata.json`, a pipelined
  exporter, a *Current frame* button.
- Undo/redo, in-place zoom with full-resolution decoding, flat-field correction, shortcuts help (F1).

### Changed
- Renamed to **SMneg**; the UI is now English and brand names were removed from it.
- A larger, centered **PASS** mark on skipped frames.
- Settings migrate automatically from the old settings store; sessions from earlier versions still open.
- Windows support: capture is disabled outside macOS and keyboard hints show Ctrl/Alt/Shift.

### Unchanged
- The negative inversion algorithm (`load_negative_base`) is identical to the original.

[Unreleased]: https://github.com/saidmrigua/SmNeg/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/saidmrigua/SmNeg/releases/tag/v0.1.0
