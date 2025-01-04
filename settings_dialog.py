from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QColorDialog, QFontDialog, QStackedWidget, 
    QListWidget, QListWidgetItem, QWidget, QRadioButton, QButtonGroup, QMessageBox)
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt
from config_manager import ConfigManager
from theme_manager import ThemeManager

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Beállítások")
        self.setMinimumSize(600, 400)
        self.config_manager = ConfigManager()
        self.theme_manager = ThemeManager()

        # Fő vertikális layout létrehozása
        main_layout = QVBoxLayout()

        # Horizontális layout a lista és stackedWidget számára
        content_layout = QHBoxLayout()
        
        # Bal oldali kategória lista
        self.category_list = QListWidget()
        self.category_list.addItem("Téma")
        self.category_list.addItem("Nyelv")
        self.category_list.addItem("Értesítések")
        self.category_list.setFixedWidth(150)

        # StackedWidget létrehozása
        self.stackedWidget = QStackedWidget()
        self.category_list.currentRowChanged.connect(self.stackedWidget.setCurrentIndex)
        
        # Panelek létrehozása
        self.setupThemePanel()
        self.setupLanguagePanel()
        self.setupNotificationsPanel()

        # Lista és StackedWidget hozzáadása a horizontális layouthoz
        content_layout.addWidget(self.category_list)
        content_layout.addWidget(self.stackedWidget)

        # Gombok layout-ja
        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Alkalmaz")
        self.save_button = QPushButton("Mentés")
        
        # Események hozzáadása a gombokhoz
        self.apply_button.clicked.connect(self.applySettings)
        self.save_button.clicked.connect(self.saveSettings)
        
        button_layout.addStretch()
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.save_button)

        # Layout-ok összeállítása
        main_layout.addLayout(content_layout)  # Először a tartalom
        main_layout.addLayout(button_layout)   # Aztán a gombok
        
        # Fő layout beállítása
        self.setLayout(main_layout)

    def setupThemePanel(self):
        theme_panel = QWidget()
        layout = QVBoxLayout()

        # Téma választó gombok
        self.theme_group = QButtonGroup()
        
        # Sötét téma
        dark_theme = QRadioButton("Sötét téma")
        dark_theme.setStyleSheet("""
            QRadioButton {
                color: white;
                background-color: #2d2d2d;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        
        # Világos téma
        light_theme = QRadioButton("Világos téma")
        light_theme.setStyleSheet("""
            QRadioButton {
                color: black;
                background-color: #0078D7;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        
        # Egyedi téma
        custom_theme = QRadioButton("Egyedi téma")
        
        self.theme_group.addButton(dark_theme)
        self.theme_group.addButton(light_theme)
        self.theme_group.addButton(custom_theme)

        # Egyedi téma beállításai
        self.custom_settings = QWidget()
        custom_layout = QVBoxLayout()
        
        # Színválasztó
        color_button = QPushButton("Háttérszín választása")
        color_button.clicked.connect(self.chooseColor)
        
        # Betűszín választó
        font_color_button = QPushButton("Betűszín választása")
        font_color_button.clicked.connect(self.chooseFontColor)
        
        # Betűtípus választó
        font_button = QPushButton("Betűtípus választása")
        font_button.clicked.connect(self.chooseFont)
        
        custom_layout.addWidget(color_button)
        custom_layout.addWidget(font_color_button)
        custom_layout.addWidget(font_button)
        self.custom_settings.setLayout(custom_layout)
        self.custom_settings.hide()

        # Custom téma kapcsoló
        custom_theme.toggled.connect(self.custom_settings.setVisible)
        
        layout.addWidget(dark_theme)
        layout.addWidget(light_theme)
        layout.addWidget(custom_theme)
        layout.addWidget(self.custom_settings)
        layout.addStretch()
        
        theme_panel.setLayout(layout)
        self.stackedWidget.addWidget(theme_panel)

    def setupLanguagePanel(self):
        """Nyelvi beállítások panel létrehozása"""
        language_panel = QWidget()
        layout = QVBoxLayout()
    
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Magyar", "English"])
    
        layout.addWidget(QLabel("Válasszon nyelvet:"))
        layout.addWidget(self.language_combo)
        layout.addStretch()
    
        language_panel.setLayout(layout)
        self.stackedWidget.addWidget(language_panel)

    def setupNotificationsPanel(self):
        """Értesítési beállítások panel létrehozása"""
        notifications_panel = QWidget()
        layout = QVBoxLayout()
    
        # Email értesítések
        self.email_checkbox = QRadioButton("Email értesítések")
        self.push_checkbox = QRadioButton("Push értesítések")
    
        layout.addWidget(self.email_checkbox)
        layout.addWidget(self.push_checkbox)
        layout.addStretch()
    
        notifications_panel.setLayout(layout)
        self.stackedWidget.addWidget(notifications_panel)

    def chooseColor(self):
        """Háttérszín választó dialógus"""
        color_dialog = QColorDialog(self)
        color_dialog.setWindowTitle("Szín választása")
    
        if color_dialog.exec():
            selected_color = color_dialog.selectedColor()
            custom_theme = {
                'background': selected_color.name(),
                'text': '#000000' if selected_color.lightness() > 128 else '#ffffff',
                'button': selected_color.lighter().name(),
                'button_text': '#000000' if selected_color.lightness() > 128 else '#ffffff',
                'window': selected_color.name()
            }
        
            try:
                # Alkalmazzuk az egyedi témát
                self.theme_manager.apply_theme(self, "Egyedi téma", custom_theme)
                if self.parent():
                    self.theme_manager.apply_theme(self.parent(), "Egyedi téma", custom_theme)
            
                # Mentsük el az egyedi téma beállításait
                self.config_manager.set('custom_theme', custom_theme)
                QMessageBox.information(self, "Siker", "Egyedi téma sikeresen alkalmazva!")
            except Exception as e:
                QMessageBox.warning(self, "Hiba", f"Hiba történt az egyedi téma alkalmazásakor: {str(e)}")

    def chooseFontColor(self):
        """Betűszín választó dialógus"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.font_color = color.name()
            # El is menthetjük azonnal
            self.config_manager.set('font_color', self.font_color)

    def chooseFont(self):
        """Magyar nyelvű betűtípus választó dialógus"""
        font_dialog = QFontDialog(self)
        # Magyar feliratok beállítása
        font_dialog.setWindowTitle("Betűtípus választása")
    
        button_box = font_dialog.findChild(QWidget, "buttonBox")
        if button_box:
            ok_button = button_box.findChild(QPushButton, "OK")
            if ok_button:
                ok_button.setText("Rendben")
            else:
                print("OK gomb nem található")
        
            cancel_button = button_box.findChild(QPushButton, "Cancel")
            if cancel_button:
                cancel_button.setText("Mégse")
            else:
                print("Mégse gomb nem található")
        else:
            print("buttonBox nem található")
    
        # Magyar címkék beállítása
        labels = font_dialog.findChildren(QLabel)
        for label in labels:
            if label.text() == "Font":
                label.setText("Betűtípus")
            elif label.text() == "Font style":
                label.setText("Betűstílus")
            elif label.text() == "Size":
                label.setText("Méret")
            elif label.text() == "Effects":
                label.setText("Effektek")
            elif label.text() == "Sample":
                label.setText("Minta")
            elif label.text() == "Writing System":
                label.setText("Írásrendszer")
            elif label.text() == "Strikeout":
                label.setText("Áthúzott")
            elif label.text() == "Underline":
                label.setText("Aláhúzott")

        if font_dialog.exec():
            selected_font = font_dialog.selectedFont()
            self.font_family = selected_font.family()
            self.font_size = selected_font.pointSize()
            # Mentsük el a betűtípus beállításokat
            self.config_manager.set('font_family', self.font_family)
            self.config_manager.set('font_size', self.font_size)
            # Alkalmazzuk a betűtípus beállításokat
            self.applyFontSettings()

    def applyFontSettings(self):
        """Alkalmazza a betűtípus beállításokat az ablakra"""
        font = QFont(self.font_family, self.font_size)
        self.setFont(font)
        if self.parent():
            self.parent().setFont(font)



    # ... (többi meglévő függvény marad változatlan) ...

    # Ez a két új függvény, amit hozzáadunk a fájl végéhez:
    def applySettings(self):
        try:
            selected_theme = None
            for button in self.theme_group.buttons():
                if button.isChecked():
                    selected_theme = button.text()
                    break

            if selected_theme:
                print(f"Applying theme: {selected_theme}")  # Hibakeresési üzenet
                success = self.theme_manager.apply_theme(self, selected_theme)
                if success and self.parent():
                    self.theme_manager.apply_theme(self.parent(), selected_theme)
                    QMessageBox.information(self, "Siker", "A téma sikeresen alkalmazva!")
                    self.config_manager.set('theme', selected_theme)
        except Exception as e:
            print(f"Hiba történt a téma alkalmazásakor: {str(e)}")  # Hibakeresési üzenet
            QMessageBox.warning(self, "Hiba", f"Hiba történt a téma alkalmazásakor: {str(e)}")


    def saveSettings(self):
        # Menti a kiválasztott témát
        selected_theme = None
        for button in self.theme_group.buttons():
            if button.isChecked():
                selected_theme = button.text()
                break
        
        if selected_theme:
            self.config_manager.set('theme', selected_theme)
            QMessageBox.information(self, "Siker", "A beállítások sikeresen mentve!")

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    settings_dialog = SettingsDialog()
    settings_dialog.show()  # Vagy settings_dialog.exec() ha modális ablakot szeretnél
    sys.exit(app.exec())