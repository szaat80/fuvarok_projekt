# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Beállítások")
        self.setModal(True)
        self.layout = QVBoxLayout()

        # Téma kiválasztása
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Világos téma", "Sötét téma"])
        self.layout.addWidget(QLabel("Téma kiválasztása:"))
        self.layout.addWidget(self.theme_combo)

        # Színek kiválasztása
        self.color_label = QLabel("Alapszín:")
        self.color_input = QLineEdit()
        self.layout.addWidget(self.color_label)
        self.layout.addWidget(self.color_input)

        self.font_label = QLabel("Betűtípus:")
        self.font_input = QLineEdit()
        self.layout.addWidget(self.font_label)
        self.layout.addWidget(self.font_input)

        # Mentés gomb
        self.save_button = QPushButton("Mentés")
        self.save_button.clicked.connect(self.saveSettings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def saveSettings(self):
        theme = self.theme_combo.currentText()
        color = self.color_input.text()
        font = self.font_input.text()
        self.parent().applySettings(theme, color, font)
        self.accept()