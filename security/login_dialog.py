from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

class LoginDialog(QDialog):
    def __init__(self, auth_manager, parent=None):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.token = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Bejelentkezés")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Logo/cím
        title = QLabel("Fuvar Adminisztráció")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        # Form layout
        form = QFormLayout()
        form.setSpacing(15)

        self.username = QLineEdit()
        self.username.setPlaceholderText("👤 Felhasználónév")
        self.username.setMinimumHeight(40)
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("🔒 Jelszó")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(40)
        
        form.addRow(self.username)
        form.addRow(self.password)

        # Login gomb
        login_btn = QPushButton("Bejelentkezés")
        login_btn.setMinimumHeight(45)
        login_btn.clicked.connect(self.handle_login)

        # Layout összeállítása
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(login_btn)
        
        self.setLayout(layout)

        # Stílus
        self.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                border-radius: 10px;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                padding: 10px;
                background: #3d3d3d;
                border: 2px solid #4d4d4d;
                border-radius: 5px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #ff4400;
            }
            QPushButton {
                background-color: #ff4400;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff5511;
            }
        """)

    def handle_login(self):
        success, token = self.auth_manager.authenticate(
            self.username.text(), 
            self.password.text(),
            "127.0.0.1"
        )
        if success:
            self.token = token
            self.accept()
        else:
            self.password.clear()
            self.username.setFocus()