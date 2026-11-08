# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Said Mrigua
import json
from dataclasses import fields

from PySide6.QtCore import QSettings

from .settings import app_settings
from .models import FrameItem

SETTINGS_OK = QSettings.Status.NoError


FRAME_FIELDS = tuple(
    field.name for field in fields(FrameItem) if field.name not in {"index", "base_positive"}
)


_FRAME_TYPES = {
    "cyan": int, "magenta": int, "yellow": int, "density": int, "rotation": int, "sharpness": int,
    "contrast": float, "saturation": float, "straighten": float,
    "mirror": bool, "auto_crop": bool, "show_clipping": bool, "is_passed": bool,
    "processed_date": str, "tone_profile": str,
}


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check(condition, message):
    if not condition:
        raise ValueError(f"Invalid session file: {message}")


def validate_session(data):
    """Check the structure and types of a session before it is used; raises ValueError with a clear message.
    Unknown keys are ignored so that newer files still open."""
    _check(isinstance(data, dict), "the top level must be an object")
    frames = data.get("frames", [])
    _check(isinstance(frames, list), '"frames" must be a list')
    for number, frame in enumerate(frames, start=1):
        _check(isinstance(frame, dict), f"frame {number} must be an object")
        _check(isinstance(frame.get("path"), str) and frame["path"], f'frame {number} needs a "path" text')
        for key, kind in _FRAME_TYPES.items():
            if key not in frame:
                continue
            value = frame[key]
            ok = (_is_number(value) if kind is float
                  else isinstance(value, int) and not isinstance(value, bool) if kind is int
                  else isinstance(value, kind))
            _check(ok, f'frame {number}: "{key}" has the wrong type')
        _check(frame.get("rotation", 0) % 90 == 0, f'frame {number}: "rotation" must be a multiple of 90')
        crop = frame.get("manual_crop")
        _check(crop is None or (isinstance(crop, (list, tuple)) and len(crop) == 4 and all(map(_is_number, crop))),
               f'frame {number}: "manual_crop" must be four numbers')
    current = data.get("current_idx", 0)
    _check(isinstance(current, int) and not isinstance(current, bool), '"current_idx" must be an integer')
    for key in ("session_info", "camera_reference"):
        _check(isinstance(data.get(key, {}), dict), f'"{key}" must be an object')
    reference = data.get("flat_field_reference")
    _check(reference is None or isinstance(reference, str), '"flat_field_reference" must be text')
    return data


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
        return validate_session(json.loads(settings.value("last_session", "{}", type=str)))
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
    return validate_session(json.loads(project_path(folder).read_text(encoding="utf-8")))
