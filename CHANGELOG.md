# Changelog

All notable changes are listed here. Format based on [Keep a Changelog](https://keepachangelog.com/),
versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]
### Fixed
- A manual crop now stays on the same part of the picture when you rotate or mirror the frame (before, the crop box
  stayed at the same place on screen and framed something else). The straighten angle follows too, also when frames
  receive rotation / mirror through Copy-Paste or Hold. Crops saved by earlier versions are read as they were.
- 16-bit TIFF input is decoded without being reduced to 8 bits first (the inversion formulas are unchanged;
  8-bit TIFF, JPEG, PNG and RAW inputs give the same results as before).
- Export no longer writes a preview-resolution image when the full-resolution decode fails: that frame is listed as
  *not exported* and nothing is written for it.
- Session files are validated (structure and types) before use; a file with valid JSON but the wrong structure now gives a
  clear error instead of failing later.
- Three remaining French status messages are now English.

### Added
- Release workflow: tests must pass on macOS and Windows before anything is built; each app runs a start-up
  self-test; the macOS app is labelled arm64 (`SMneg-macOS-arm64.dmg`) and the Windows app `SMneg-Windows-x64.zip`.
- CI installs the wheel and the sdist into a clean environment; `tests/test_versions.py` keeps version numbers in sync.
- Tests for 16-bit TIFF precision and orientation, session validation, exact parallel/sequential equality and unreadable files.

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
