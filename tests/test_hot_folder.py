# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Said Mrigua
from smneg.hot_folder import HotFolder


def test_file_is_ready_only_after_its_size_is_stable(tmp_path):
    folder = HotFolder(tmp_path, (".nef",))
    photo = tmp_path / "a.nef"
    photo.write_bytes(b"123")
    assert folder.ready_files() == []          # first sighting
    assert folder.ready_files() == [photo]     # unchanged since the last poll
    photo.write_bytes(b"123456")               # still being written
    assert folder.ready_files() == []


def test_ignores_other_extensions_and_empty_files(tmp_path):
    folder = HotFolder(tmp_path, (".nef",))
    (tmp_path / "notes.txt").write_text("x")
    (tmp_path / "empty.nef").write_bytes(b"")
    folder.ready_files()
    assert folder.ready_files() == []
