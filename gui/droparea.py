# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PySide6.QtCore import QMimeData, Qt, Slot, Signal
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QFrame, QLabel


TEXTO_PADRAO = "<Arraste o arquivo ou pasta até aqui>"


class DropArea(QLabel):

    changed = Signal(QMimeData)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(640, 64)
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)
        self.clear()

    def dragEnterEvent(self, event):
        self.setText(TEXTO_PADRAO)
        self.setBackgroundRole(QPalette.Highlight)

        event.acceptProposedAction()
        self.changed.emit(event.mimeData())

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            self.setText(mime_data.urls()[0].path())
        else:
            self.setText("Caminho inválido!")

        self.setBackgroundRole(QPalette.Dark)
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.clear()
        event.accept()

    @Slot()
    def clear(self):
        self.setText(TEXTO_PADRAO)
        self.setBackgroundRole(QPalette.Dark)

        self.changed.emit(None)
