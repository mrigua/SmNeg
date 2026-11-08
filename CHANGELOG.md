# Changelog

## 0.1.0 - first public release
SMneg is the open-source release of an existing in-house film-negative inversion tool
(previously an unreleased "Frontier SP-500 Master v6" controller).

- Renamed to **SMneg**; removed third-party brand names from the UI. The English UI replaces the French one.
- Settings migrate automatically from the old settings store; sessions created by earlier versions still open.
- Windows support: capture is disabled outside macOS, keyboard hints show Ctrl/Alt/Shift.
- Export: pipelined (load next / render / write previous), "Current frame" button, session information
  filled in once at *New Session* and reused by the export dialog, filename templates with variables.
- 16-bit TIFF export with embedded XMP metadata (needs `tifffile`).
- Undo/redo, in-place zoom with full-resolution decoding, shortcuts help (F1).
- The negative inversion algorithm is unchanged; a regression test compares it with reference outputs.
