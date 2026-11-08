# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Said Mrigua
import uuid

from PySide6.QtCore import QSettings

from smneg import settings


def test_legacy_settings_are_imported_once(tmp_path, monkeypatch):
    # isolate from any real settings: private INI files and unique names
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(tmp_path))
    unique = uuid.uuid4().hex
    monkeypatch.setattr(settings, "ORGANIZATION", f"new-{unique}")
    monkeypatch.setattr(settings, "APPLICATION", f"new-{unique}")
    monkeypatch.setattr(settings, "LEGACY_ORGANIZATION", f"old-{unique}")
    monkeypatch.setattr(settings, "LEGACY_APPLICATION", f"old-{unique}")

    legacy = QSettings(settings.LEGACY_ORGANIZATION, settings.LEGACY_APPLICATION)
    legacy.setValue("export/photographer", "Said")
    legacy.sync()

    assert settings.migrate_legacy_settings() == 1
    assert settings.app_settings().value("export/photographer", "", type=str) == "Said"

    legacy.setValue("export/photographer", "Changed")
    legacy.sync()
    assert settings.migrate_legacy_settings() == 0
    assert settings.app_settings().value("export/photographer", "", type=str) == "Said"
