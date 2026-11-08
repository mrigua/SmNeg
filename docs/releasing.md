<!-- SPDX-License-Identifier: Apache-2.0 | Copyright 2026 Said Mrigua -->
# Releasing a new version

Releases are built by GitHub Actions (`.github/workflows/release.yml`) when a tag `vX.Y.Z` is pushed.

## Checklist
1. Pick the version (semantic versioning): `MAJOR.MINOR.PATCH`.
2. Update it in **three** places: `pyproject.toml` (`version`), `src/smneg/__init__.py` (`__version__`) and
   `packaging/smneg.spec` (`version`).
3. Move the `Unreleased` section of [CHANGELOG.md](../CHANGELOG.md) under the new version with the date.
4. Run `pytest` and `python -m pyflakes src tests`; test the app by hand with a real roll (see
   [development.md](development.md)).
5. Commit and push to the default branch; wait for **CI** to pass on macOS and Windows.
6. Tag and push **from a terminal** (the tag must be `v` + the version):
   ```bash
   git checkout smneg-release && git pull
   git tag -a vX.Y.Z -m "SMneg X.Y.Z"
   git push origin vX.Y.Z
   ```
   Creating the tag in the GitHub web form works too, but you must click *Create new tag: vX.Y.Z on publish*;
   typing the name is not enough.
7. The *Release* workflow builds `SMneg-macOS.dmg`, `SMneg-Windows.zip`, a wheel and an sdist and publishes the
   Release (a few minutes). Check that all four files are attached.
8. Download the `.dmg` / `.zip` and open them on a clean machine if you can. They are not signed (see below).

## Fixing a failed release
Delete the Release and the tag on GitHub (*Releases* and *Tags* pages) and push the tag again. Never reuse a version
number for different content once people have downloaded it: bump the patch number instead.

## Signing (not done yet)
- macOS: needs an Apple Developer ID certificate and notarization (`codesign` + `notarytool`); then users no longer see
  the *unidentified developer* warning.
- Windows: needs a code-signing certificate for SmartScreen reputation.
- PyPI: the project publishes a wheel and an sdist on GitHub only. Publishing to PyPI (`twine upload dist/*`) needs a
  PyPI account and a free `smneg` project name; check availability first.
