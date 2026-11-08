"""Application entry point."""
import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .settings import APPLICATION, ORGANIZATION, migrate_legacy_settings
from .window import SMnegWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setOrganizationName(ORGANIZATION)
    app.setApplicationName(APPLICATION)
    migrate_legacy_settings()
    icon = Path(__file__).with_name("assets") / "icon.png"
    if icon.is_file():
        app.setWindowIcon(QIcon(str(icon)))
    window = SMnegWindow()
    window.show()
    return app.exec()
