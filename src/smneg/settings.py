# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Said Mrigua
"""Application settings, with a one-time import of settings saved by earlier (pre-rename) versions."""
from PySide6.QtCore import QSettings

ORGANIZATION = "SMneg"
APPLICATION = "SMneg"
LEGACY_ORGANIZATION = "Frontier"
LEGACY_APPLICATION = "SP-500"
MIGRATION_KEY = "migrated_from_legacy"


def app_settings() -> QSettings:
    return QSettings(ORGANIZATION, APPLICATION)


def migrate_legacy_settings() -> int:
    """Copy every key from the old settings store once. Returns the number of keys copied."""
    current = app_settings()
    if current.value(MIGRATION_KEY, False, type=bool):
        return 0
    legacy = QSettings(LEGACY_ORGANIZATION, LEGACY_APPLICATION)
    copied = 0
    for key in legacy.allKeys():
        if not current.contains(key):
            current.setValue(key, legacy.value(key))
            copied += 1
    current.setValue(MIGRATION_KEY, True)
    current.sync()
    return copied
