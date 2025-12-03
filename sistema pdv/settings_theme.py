from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QColorDialog, QLabel, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap
from ..core import load_json, save_json
import os

class ThemeSettings(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tema = load_json("tema.json")
        layout = QVBoxLayout()

        self.lbl_preview = QLabel("Prévia do papel de parede:")
        self.lbl_preview.setFixedHeight(200)
        self.lbl_preview.setScaledContents(True)

        if os.path.exists(self.tema.get("papel_de_parede", "")):
            self.lbl_preview.setPixmap(QPixmap(self.tema["papel_de_parede"]))

        btn_cor = QPushButton("Alterar cor primária")
        btn_cor.clicked.connect(self.alterar_cor)

        btn_fundo = QPushButton("Escolher papel de parede")
        btn_fundo.clicked.connect(self.escolher_papel)

        btn_salvar = QPushButton("Salvar tema")
        btn_salvar.clicked.connect(self.salvar)

        layout.addWidget(self.lbl_preview)
        layout.addWidget(btn_cor)
        layout.addWidget(btn_fundo)
        layout.addWidget(btn_salvar)
        layout.addStretch()

        self.setLayout(layout)

    def alterar_cor(self):
        cor = QColorDialog.getColor()
        if cor.isValid():
            self.tema["cor_primaria"] = cor.name()

    def escolher_papel(self):
        caminho, _ = QFileDialog.getOpenFileName(
            self,
            "Escolher imagem de fundo",
            "",
            "Imagens (*.jpg *.png *.jpeg)"
        )
        if caminho:
            # Cria a pasta de wallpapers se não existir
            pasta = os.path.join(os.path.dirname(__file__), "..", "data", "wallpapers")
            os.makedirs(pasta, exist_ok=True)
            destino = os.path.join(pasta, os.path.basename(caminho))
            with open(caminho, "rb") as src, open(destino, "wb") as dst:
                dst.write(src.read())

            self.tema["papel_de_parede"] = destino
            self.lbl_preview.setPixmap(QPixmap(destino))

    def salvar(self):
        save_json("tema.json", self.tema)
        QMessageBox.information(self, "Sucesso", "Tema atualizado com sucesso!")
        self.parent.aplicar_tema()
