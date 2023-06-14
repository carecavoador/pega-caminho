import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QClipboard
from ui_janela import Ui_MainWindow


class JanelaPrincipal(QMainWindow, Ui_MainWindow):
    """Janela principal do programa."""

    def __init__(self, local: str, clipboard: QClipboard) -> None:
        super().__init__()
        self.setupUi(self)
        self.clipboard = clipboard

        # Sinais
        qApp.focusChanged.connect(lambda: self.edit_original.setText(self.clipboard.text()))
        self.pushButton.clicked.connect(lambda: self.clipboard.setText(self.edit_novo.text()))
        self.edit_original.textChanged.connect(
            lambda: self.edit_novo.setText(self.atualiza_local(self.edit_original.text()))
        )

        if local:
            self.edit_original.setText(local)
            self.edit_novo.setText(self.atualiza_local(local))
        else:
            self.edit_original.setPlaceholderText("Cole aqui o caminho original...")

    def atualiza_local(self, original: str) -> str:
        try:
            caminho = Path(original).as_posix()
            if caminho:
                index = caminho.lower().find("server-bnu")
                if index != -1:
                    caminho_limpo = caminho[index:]
                    caminho_macos = "smb://fileserver/" + caminho_limpo
                    return caminho_macos
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
