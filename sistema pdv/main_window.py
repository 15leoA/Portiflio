from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from PyQt6.QtGui import QPalette, QBrush, QPixmap
from ..tema_manager import TemaManager
from .pos_screen import PosScreen
from .product_editor import ProductEditor
from .settings_theme import ThemeSettings
import os

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("PDV - Mercadinho")
        self.resize(1000, 600)
        self.tema = TemaManager().get()
        self.init_ui()
        self.aplicar_tema()

    def init_ui(self):
        central = QWidget()
        layout = QHBoxLayout()

        menu = QVBoxLayout()
        btn_pdv = QPushButton("Tela de Vendas")
        btn_prod = QPushButton("Cadastro de Produtos")
        btn_tema = QPushButton("Tema / Personalização")

        menu.addWidget(btn_pdv)
        menu.addWidget(btn_prod)
        menu.addWidget(btn_tema)
        menu.addStretch()

        self.stack = QStackedWidget()
        self.stack.addWidget(PosScreen(self))
        self.stack.addWidget(ProductEditor(self))
        self.stack.addWidget(ThemeSettings(self))

        btn_pdv.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_prod.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_tema.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        layout.addLayout(menu, 1)
        layout.addWidget(self.stack, 5)
        central.setLayout(layout)
        self.setCentralWidget(central)

    def aplicar_tema(self):
        tema = TemaManager().get()
        paleta = self.palette()
        if os.path.exists(tema.get("papel_de_parede", "")):
            pixmap = QPixmap(tema["papel_de_parede"])
            paleta.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        else:
            paleta.setColor(QPalette.ColorRole.Window, tema["cor_primaria"])
        self.setPalette(paleta)
