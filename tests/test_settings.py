from PySide6.QtCore import QSettings

from smneg import settings


def test_legacy_settings_are_imported_once(tmp_path):
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(tmp_path))
    legacy = QSettings(settings.LEGACY_ORGANIZATION, settings.LEGACY_APPLICATION)
    legacy.setValue("export/photographer", "Said")
    legacy.sync()

    assert settings.migrate_legacy_settings() >= 1
    assert settings.app_settings().value("export/photographer", "", type=str) == "Said"

    legacy.setValue("export/photographer", "Changed")
    legacy.sync()
    assert settings.migrate_legacy_settings() == 0
    assert settings.app_settings().value("export/photographer", "", type=str) == "Said"
