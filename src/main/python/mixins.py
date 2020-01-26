#!/usr/bin/env python3
from PyQt5.QtCore import pyqtSignal as signal


class DropableWidget:
    dropped = signal(str, name='dropped')

    def __init__(self, parent=None):
        # Mixin for QWidget
        self.setAcceptDrops(True)

    def isFileDropable(self, url):
        return NotImplemented

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if len(urls) == 1:
            url = urls[0].url()
            if url.startswith('file://') and self.isFileDropable(url):
                self.dropped.emit(url[7:])  # len('file://') == 7
                event.accept()
        event.ignore()
