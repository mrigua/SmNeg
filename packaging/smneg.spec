# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Said Mrigua
# PyInstaller spec:  pyinstaller packaging/smneg.spec --noconfirm
import sys
from pathlib import Path

root = Path(SPECPATH).parent
assets = root / "src" / "smneg" / "assets"
icon = str(assets / ("icon.icns" if sys.platform == "darwin" else "icon.ico"))
version = "0.1.0"

analysis = Analysis(
    [str(root / "packaging" / "launcher.py")],
    pathex=[str(root / "src")],
    datas=[(str(assets), "smneg/assets")],
    excludes=["tkinter"],
)
pyz = PYZ(analysis.pure)
exe = EXE(pyz, analysis.scripts, [], exclude_binaries=True, name="SMneg", console=False, icon=icon)
collected = COLLECT(exe, analysis.binaries, analysis.datas, name="SMneg")
if sys.platform == "darwin":
    app = BUNDLE(
        collected, name="SMneg.app", icon=icon, bundle_identifier="com.saidmrigua.smneg",
        info_plist={
            "CFBundleShortVersionString": version,
            "NSHighResolutionCapable": True,
            "NSHumanReadableCopyright": "Copyright 2026 Said Mrigua",
        },
    )
