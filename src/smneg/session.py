import json
from dataclasses import fields

from PySide6.QtCore import QSettings

from .settings import app_settings
from .models import FrameItem

SETTINGS_OK = QSettings.Status.NoError


FRAME_FIELDS = tuple(
    field.name for field in fields(FrameItem) if field.name not in {"index", "base_positive"}
)


def session_data(items, current_idx, view):
    return {
        "frames": [{key: getattr(item, key) for key in FRAME_FIELDS} for item in items],
        "current_idx": current_idx,
        "view": view,
    }


def save_session(items, current_idx, view, flat_reference="", info=None):
    settings = app_settings()
    data = session_data(items, current_idx, view)
    data["flat_field_reference"] = flat_reference
    data["session_info"] = info or {}
    settings.setValue("last_session", json.dumps(data))
    settings.sync()
    return settings.status() == SETTINGS_OK


def load_session():
    settings = app_settings()
    try:
        return json.loads(settings.value("last_session", "{}", type=str))
    except ValueError:
        return {}


def create_session_folder(parent):
    from datetime import date

    prefix = date.today().isoformat()
    for sequence in range(1, 10000):
        folder = parent / f"{prefix}_Session-{sequence:03d}"
        try:
            folder.mkdir()
        except FileExistsError:
            continue
        return folder
    raise OSError("Unable to create a unique session folder.")


PROJECT_FILE = "smneg-session.json"
LEGACY_PROJECT_FILE = "frontier-session.json"   # sessions created by earlier versions


def project_path(folder):
    legacy = folder / LEGACY_PROJECT_FILE
    return folder / PROJECT_FILE if (folder / PROJECT_FILE).is_file() or not legacy.is_file() else legacy


def write_project(folder, items, current_idx, view, camera_reference, flat_reference="", info=None):
    data = session_data(items, current_idx, view)
    data["camera_reference"] = camera_reference
    data["flat_field_reference"] = flat_reference
    data["session_info"] = info or {}
    temporary = folder / ".smneg-session.tmp"
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(folder / PROJECT_FILE)


def read_project(folder):
    return json.loads(project_path(folder).read_text(encoding="utf-8"))
