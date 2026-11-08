<!-- SPDX-License-Identifier: Apache-2.0 | Copyright 2026 Said Mrigua -->
# Releasing a new version

Releases are built by GitHub Actions (`.github/workflows/release.yml`) when a tag `vX.Y.Z` is pushed.

## What the workflow does
1. **validate**: `pyflakes` and `pytest` on macOS and Windows for the tagged revision, and a check that the tag equals the
   package version. Nothing is built or published if this fails.
2. **python-package**: wheel and sdist (`twine check`).
3. **macos-app** (Apple Silicon runner, so the app is arm64 only) and **windows-app**: PyInstaller bundles. Each bundle runs
   `SMneg --self-test` (imports every module, finds the assets, decodes and inverts a sample TIFF, builds the main window
   offscreen) before it is packaged.
4. **publish**: attaches `SMneg-macOS-arm64.dmg`, `SMneg-Windows-x64.zip`, the wheel and the sdist to the Release.

CI (`ci.yml`) additionally installs the built wheel and sdist into a clean virtual environment outside the checkout.

## Checklist
1. Pick the version (semantic versioning): `MAJOR.MINOR.PATCH`.
2. Update it in **four** places: `pyproject.toml`, `src/smneg/__init__.py`, `packaging/smneg.spec` and `CITATION.cff`
   (`tests/test_versions.py` fails if they disagree), and move the *Unreleased* section of [CHANGELOG.md](../CHANGELOG.md)
   under the new version with the date.
3. Run `pytest` and `python -m pyflakes src tests packaging`; test the app by hand with a real roll (see
   [development.md](development.md)).
4. Commit and push to the default branch; wait for **CI** to pass on macOS and Windows.
5. Optional rehearsal: GitHub → Actions → *Release* → *Run workflow* builds and smoke-tests everything without publishing.
6. Tag and push **from a terminal** (the tag must be `v` + the version):
   ```bash
   git checkout smneg-release && git pull
   git tag -a vX.Y.Z -m "SMneg X.Y.Z"
   git push origin vX.Y.Z
   ```
   Creating the tag in the GitHub web form works too, but you must click *Create new tag: vX.Y.Z on publish*;
   typing the name is not enough.
7. Check that all four files are attached to the Release, then download the `.dmg` / `.zip` and open them on a clean machine
   if you can. They are not signed (see below).

## Fixing a failed release
Delete the Release and the tag on GitHub (*Releases* and *Tags* pages) and push the tag again. Never reuse a version
number for different content once people have downloaded it: bump the patch number instead.

## Signing (not done yet)
- macOS: needs an Apple Developer ID certificate and notarization (`codesign` + `notarytool`); then users no longer see
  the *unidentified developer* warning.
- Windows: needs a code-signing certificate for SmartScreen reputation.
- PyPI: the project publishes a wheel and an sdist on GitHub only. Publishing to PyPI (`twine upload dist/*`) needs a
  PyPI account and a free `smneg` project name; check availability first.
