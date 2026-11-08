import numpy as np
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QScrollArea, QVBoxLayout


class ZoomDialog(QDialog):
    def __init__(self, image, filename, parent):
        super().__init__(parent)
        self.setWindowTitle(f"Zoom 100% — {filename}")
        pixels = np.ascontiguousarray(image)
        height, width = pixels.shape[:2]
        qimage = QImage(pixels.data, width, height, pixels.strides[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        pixmap.setDevicePixelRatio(parent.devicePixelRatioF())
        label = QLabel()
        label.setPixmap(pixmap)
        label.adjustSize()
        self.scroll = QScrollArea()
        self.scroll.setWidget(label)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"{width} × {height} px"))
        layout.addWidget(self.scroll)
        available = parent.screen().availableGeometry()
        self.resize(min(1000, available.width()), min(720, available.height()))

    def showEvent(self, event):
        super().showEvent(event)
        for bar in (self.scroll.horizontalScrollBar(), self.scroll.verticalScrollBar()):
            bar.setValue(bar.maximum() // 2)
