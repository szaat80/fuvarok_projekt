# -*- coding: utf-8 -*-
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class ThemeManager:
    def __init__(self):
        # Előre definiált témák
        self.dark_theme = {
            'background': '#2d2d2d',
            'text': '#ffffff',
            'button': '#3d3d3d',
            'button_text': '#ffffff',
            'window': '#1e1e1e'
        }
        
        self.light_theme = {
        'background': '#ffffff',
        'text': '#000000',          # Fekete betűszín
        'button': '#f0f0f0',
        'button_text': '#000000',   # Fekete gombszöveg
        'window': '#f0f0f0'
}

    def apply_theme(self, window, theme_type, custom_theme=None):
        """Téma alkalmazása az ablakra"""
        try:
            if theme_type == "Sötét téma":
                colors = self.dark_theme
            elif theme_type == "Világos téma":
                colors = self.light_theme
            elif theme_type == "Egyedi téma" and custom_theme:
                colors = custom_theme
            else:
                return False

            # Új paletta létrehozása
            palette = QPalette()
            
            # Háttérszínek beállítása
            palette.setColor(QPalette.Window, QColor(colors['window']))
            palette.setColor(QPalette.WindowText, QColor(colors['text']))
            palette.setColor(QPalette.Base, QColor(colors['background']))
            palette.setColor(QPalette.AlternateBase, QColor(colors['background']))
            palette.setColor(QPalette.Text, QColor(colors['text']))
            palette.setColor(QPalette.Button, QColor(colors['button']))
            palette.setColor(QPalette.ButtonText, QColor(colors['button_text']))

            # Alkalmazzuk a palettát az ablakra
            window.setPalette(palette)
            
            # Stíluslap alkalmazása további finomításokhoz
            if theme_type == "Sötét téma":
                window.setStyleSheet("""
                    QDialog, QMainWindow {
                        background-color: #2d2d2d;
                        color: #ffffff;
                    }
                    QPushButton {
                        background-color: #3d3d3d;
                        color: #ffffff;
                        border: 1px solid #5e5e5e;
                        padding: 5px;
                        border-radius: 3px;
                    }
                    QLabel {
                        color: #ffffff;
                    }
                    QListWidget {
                        background-color: #2d2d2d;
                        color: #ffffff;
                        border: 1px solid #5e5e5e;
                    }
                    QRadioButton {
                        color: #ffffff;
                    }
                """)
            elif theme_type == "Világos téma":
                window.setStyleSheet("""
                    QDialog, QMainWindow {
                        background-color: #ffffff;
                        color: #000000;
                    }
                    QPushButton {
                        background-color: #f0f0f0;
                        color: #000000;
                        border: 1px solid #cccccc;
                        padding: 5px;
                        border-radius: 3px;
                    }
                    QLabel {
                        color: #000000;
                    }
                    QListWidget {
                        background-color: #ffffff;
                        color: #000000;
                        border: 1px solid #cccccc;
                    }
                    QRadioButton {
                        color: #000000;
                    }
                """)

            return True
            
        except Exception as e:
            print(f"Hiba a téma alkalmazásakor: {str(e)}")
            raise