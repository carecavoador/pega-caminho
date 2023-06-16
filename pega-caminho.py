import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import QMimeData
from PySide6.QtGui import QClipboard

from gui.droparea import DropArea


VERSAO = "0.2.1"


class JanelaPrincipal(QMainWindow):
    """Janela principal do programa."""

    def __init__(self, local: str, clipboard: QClipboard) -> None:
        super().__init__()
        self.setWindowTitle(f"Pega Caminho v{VERSAO}")
        self.clipboard = clipboard

        self.widget_central = QWidget()
        self.layout = QVBoxLayout(self.widget_central)

        # Drop area
        self.drop_area = DropArea()
        self.drop_area.changed.connect(self.dropou_na_area)
        self.layout.addWidget(self.drop_area)

        # Caminho original
        self.label_original = QLabel("Caminho original:")
        self.layout.addWidget(self.label_original)

        self.edit_original = QLineEdit()
        self.edit_original.setPlaceholderText("Cole aqui o caminho original...")
        self.layout.addWidget(self.edit_original)

        # Caminho novo
        self.label_novo = QLabel("Novo caminho:")
        self.layout.addWidget(self.label_novo)
        self.edit_novo = QLineEdit()
        self.layout.addWidget(self.edit_novo)

        # Botão copiar
        self.btn_copiar = QPushButton(text="Copiar")
        self.layout.addWidget(self.btn_copiar)

        # Sinais
        self.btn_copiar.clicked.connect(self.copia_caminho)
        self.edit_original.textChanged.connect(self.atualiza_caminho)

        if local:
            self.edit_original.setText(local)
            self.edit_novo.setText(self.formata_local(local))
        else:
            self.edit_original.setPlaceholderText("Cole aqui o caminho original...")

        self.setCentralWidget(self.widget_central)

    def atualiza_caminho(self) -> None:
        caminho_novo = self.formata_local(self.edit_original.text())
        self.edit_novo.setText(caminho_novo)

    def copia_caminho(self) -> None:
        self.clipboard.setText(self.edit_novo.text())

    def dropou_na_area(self, mime_data: QMimeData) -> None:
        if mime_data.hasUrls():
            self.edit_original.setText(mime_data.urls()[0].path())
        else:
            self.edit_original.setText("Caminho inválido!")

    @staticmethod
    def formata_local(original: str) -> str:
        try:
            caminho = Path(original).as_posix()
            if caminho:
                index = caminho.lower().find("server-bnu")
                if index != -1:
                    caminho_limpo = caminho[index:]
                    caminho_macos = "smb://fileserver/" + caminho_limpo
                    return caminho_macos.replace(" ", "%20")
        except ValueError:
            pass
        return "Caminho inválido!"


def main() -> None:
    """Início do programa"""

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        local = sys.argv[1]
        if Path(local).is_absolute():
            local = Path(local).as_uri()
    except IndexError:
        local = None

    janela = JanelaPrincipal(local=local, clipboard=app.clipboard())
    janela.show()

    app.exec()


if __name__ == "__main__":
    main()
