from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from typing import Dict, Any
import sqlite3

class AddressDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.parent = parent
        self.setWindowTitle("Cím bevitele")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.postal_code = QLineEdit()
        self.postal_code.textChanged.connect(self.update_city)
        self.city = QLineEdit()
        self.street = QLineEdit()
        self.house_number = QLineEdit()
        self.floor_door = QLineEdit()

        form_layout.addRow("Irányítószám:", self.postal_code)
        form_layout.addRow("Település:", self.city)
        form_layout.addRow("Közterület/utca:", self.street)
        form_layout.addRow("Házszám:", self.house_number)
        form_layout.addRow("Emelet/ajtó:", self.floor_door)

        self.save_button = QPushButton("Mentés")
        self.save_button.clicked.connect(self.save_address)

        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def update_city(self):
        postal_code = self.postal_code.text().strip()
        city = self.get_city_by_postal_code(postal_code)
        self.city.setText(city)

    def get_city_by_postal_code(self, postal_code: str) -> str:
        conn = sqlite3.connect('postal_codes.db')
        cursor = conn.cursor()
        cursor.execute('SELECT city FROM postal_codes WHERE postal_code = ?', (postal_code,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else ""

    def save_address(self):
        address_data = {
            'postal_code': self.postal_code.text().strip(),
            'city': self.city.text().strip(),
            'street': self.street.text().strip(),
            'house_number': self.house_number.text().strip(),
            'floor_door': self.floor_door.text().strip()
        }

        try:
            self.db.execute_query('''
                INSERT INTO addresses (postal_code, address, price)
                VALUES (?, ?, 0)
            ''', (address_data['postal_code'], f"{address_data['city']}, {address_data['street']} {address_data['house_number']}/{address_data['floor_door']}"))
            QMessageBox.information(self, "Siker", "Cím sikeresen mentve!")
            self.parent.loadAddresses()  # Frissítjük az adatokat a szülő osztályban
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Mentési hiba: {str(e)}")

    def get_address_data(self) -> Dict[str, Any]:
        return {
            'postal_code': self.postal_code.text().strip(),
            'city': self.city.text().strip(),
            'street': self.street.text().strip(),
            'house_number': self.house_number.text().strip(),
            'floor_door': self.floor_door.text().strip()
        }
