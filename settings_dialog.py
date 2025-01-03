# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QColorDialog, QFontDialog

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Beállítások")
        self.setModal(True)
        self.layout = QVBoxLayout()

        # Téma kiválasztása
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Világos téma", "Sötét téma", "Egyedi téma"])
        self.layout.addWidget(QLabel("Téma kiválasztása:"))
        self.layout.addWidget(self.theme_combo)

        # Színek kiválasztása
        self.color_label = QLabel("Alapszín:")
        self.color_input = QLineEdit()
        self.color_button = QPushButton("Szín választása")
        self.color_button.clicked.connect(self.chooseColor)
        self.layout.addWidget(self.color_label)
        self.layout.addWidget(self.color_input)
        self.layout.addWidget(self.color_button)

        # Betűtípus kiválasztása
        self.font_label = QLabel("Betűtípus:")
        self.font_input = QLineEdit()
        self.font_button = QPushButton("Betűtípus választása")
        self.font_button.clicked.connect(self.chooseFont)
        self.layout.addWidget(self.font_label)
        self.layout.addWidget(self.font_input)
        self.layout.addWidget(self.font_button)

        # Mentés gomb
        self.save_button = QPushButton("Mentés")
        self.save_button.clicked.connect(self.saveSettings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def chooseColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_input.setText(color.name())

    def chooseFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.font_input.setText(font.family())

    def saveSettings(self):
        theme = self.theme_combo.currentText()
        color = self.color_input.text()
        font = self.font_input.text()
        self.parent().applySettings(theme, color, font)
        self.accept()

    def getSettings(self):
        return self.theme_combo.currentText(), self.color_input.text(), self.font_input.text()

