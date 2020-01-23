#!/usr/bin/env python3
from PyQt5.QtCore import pyqtSignal as signal
from PyQt5.QtWidgets import QSpinBox, QFrame


class AlphabetSpinBox(QSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximum(25)  # only A-Y to simplify

    def textFromValue(self, num):
        return chr(64 + num)


class DragDropFrame(QFrame):
    dropFile = signal(str, name='dropFile')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def setOverlay(self, overlay):
        self.overlay = overlay
        self.overlay.hide()

    def setContent(self, icon, text):
        self.iconLabel.setPixmap(icon)
        self.textLabel.setText(text)

    def hide(self):
        super().hide()
        self.overlay.show()

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if len(urls) == 1:
            url = urls[0].url()
            if url.startswith('file://') and url.endswith('.xlsx'):
                self.dropFile.emit(url[7:])  # len('file://') == 7
                event.accept()
        event.ignore()
