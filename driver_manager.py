# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QMessageBox, QHeaderView, QFormLayout)
from PySide6.QtCore import Qt
from database_handler import DatabaseHandler
from driver_address_dialog import DriverAddressDialog

class DriverManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseHandler()
        self.initUI()
        self.loadDrivers()  # Betöltjük az adatokat

    def initUI(self):
        self.setWindowTitle("Sofőrök kezelése")
        self.setMinimumWidth(1200)
        self.setMinimumHeight(800)
        
        # Fő layout
        main_layout = QVBoxLayout()

        # Beviteli mezők form layout
        form_layout = QFormLayout()
    
        # Alapadatok mezői
        self.driver_name = QLineEdit()
        self.birth_date = QLineEdit()
        self.birth_place = QLineEdit()

        # Lakcím szerkesztés
        address_layout = QHBoxLayout()
        self.driver_address = QLineEdit()
        self.driver_address.setReadOnly(True)  # Csak a dialóguson keresztül szerkeszthető
        edit_address_btn = QPushButton("Szerkesztés")
        edit_address_btn.clicked.connect(self.edit_address)
        address_layout.addWidget(self.driver_address)
        address_layout.addWidget(edit_address_btn)
    
        # Többi adat
        self.mothers_name = QLineEdit()
        self.tax_number = QLineEdit()
        self.social_security_number = QLineEdit()
        self.bank_name = QLineEdit()
        self.bank_account = QLineEdit()

        # Form feltöltése
        form_layout.addRow("Név:", self.driver_name)
        form_layout.addRow("Születési idő:", self.birth_date)
        form_layout.addRow("Születési hely:", self.birth_place)
        form_layout.addRow("Lakcím:", address_layout)
        form_layout.addRow("Anyja neve:", self.mothers_name)
        form_layout.addRow("Adószám:", self.tax_number)
        form_layout.addRow("TAJ szám:", self.social_security_number)
        form_layout.addRow("Bank neve:", self.bank_name)
        form_layout.addRow("Bankszámlaszám:", self.bank_account)

        # Gombok layout
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Hozzáadás")
        save_btn = QPushButton("Mentés")
        delete_btn = QPushButton("Törlés")
        
        # Gombok összekötése
        add_btn.clicked.connect(self.addDriver)
        save_btn.clicked.connect(self.saveDriver)
        delete_btn.clicked.connect(self.deleteDriver)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(delete_btn)

        # Táblázat létrehozása
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Név", "Születési idő", "Születési hely", "Lakcím",
            "Anyja neve", "Adószám", "TAJ szám", "Bank neve", "Bankszámlaszám"
        ])
        
        # Táblázat beállítások
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.itemClicked.connect(self.onDriverSelected)

        # Fő layout összeállítása
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)

    def edit_address(self):
        """Lakcím szerkesztése"""
        dialog = DriverAddressDialog(self)
    
        # Ha van már cím, betöltjük
        current_address = self.driver_address.text()
        if current_address:
            dialog.set_address(current_address)
    
        # Ha a felhasználó az OK gombra kattint
        if dialog.exec() == QDialog.Accepted:
            new_address = dialog.get_address()
            self.driver_address.setText(new_address)

    def addDriver(self):
        """Új sofőr hozzáadása"""
        try:
            # Adatok összegyűjtése
            driver_data = {
                'name': self.driver_name.text(),
                'birth_date': self.birth_date.text(),
                'birth_place': self.birth_place.text(),
                'address': self.driver_address.text(),  # Közvetlenül a mezőből
                'mothers_name': self.mothers_name.text(),
                'tax_number': self.tax_number.text(),
                'social_security_number': self.social_security_number.text(),
                'bank_name': self.bank_name.text(),
                'bank_account': self.bank_account.text()
            }
        
            # Rekord beszúrása
            self.db.insert_record('drivers', driver_data)
        
            # Mezők törlése
            self.clearFields()
        
            # Táblázat frissítése
            self.loadDrivers()
        
            QMessageBox.information(self, "Siker", "Sofőr sikeresen hozzáadva!")
        
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Hiba történt a mentés során: {str(e)}")

    def saveDriver(self):
        """Kiválasztott sofőr módosítása"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Figyelmeztetés", "Válasszon ki egy sofőrt!")
            return
        
        try:
            driver_id = int(self.table.item(selected[0].row(), 0).text())
        
            # Adatok összegyűjtése
            driver_data = {
                'name': self.driver_name.text(),
                'birth_date': self.birth_date.text(),
                'birth_place': self.birth_place.text(),
                'address': self.driver_address.text(),  # Közvetlenül a mezőből
                'mothers_name': self.mothers_name.text(),
                'tax_number': self.tax_number.text(),
                'social_security_number': self.social_security_number.text(),
                'bank_name': self.bank_name.text(),
                'bank_account': self.bank_account.text()
            }
        
            # Rekord frissítése
            self.db.update_record('drivers', driver_data, driver_id)
        
            # Táblázat frissítése
            self.loadDrivers()
        
            QMessageBox.information(self, "Siker", "Sofőr adatai sikeresen módosítva!")
        
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Hiba történt a mentés során: {str(e)}")

    def deleteDriver(self):
        """Kiválasztott sofőr törlése"""
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Figyelmeztetés", "Válasszon ki egy sofőrt!")
            return
            
        driver_id = int(self.table.item(selected[0].row(), 0).text())
        name = self.table.item(selected[0].row(), 1).text()
        
        reply = QMessageBox.question(self, 'Megerősítés', 
            f'Biztosan törli a következő sofőrt: {name}?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
        if reply == QMessageBox.Yes:
            try:
                self.db.execute_query('DELETE FROM drivers WHERE id = ?', (driver_id,))
                self.loadDrivers()
                self.clearFields()
                QMessageBox.information(self, "Siker", "Sofőr sikeresen törölve!")
                
            except Exception as e:
                QMessageBox.critical(self, "Hiba", f"Hiba történt a törlés során: {str(e)}")

    def onDriverSelected(self, item):
        """Kiválasztott sofőr betöltése"""
        try:
            row = item.row()
        
            # Alapadatok betöltése
            self.driver_name.setText(self.table.item(row, 1).text())
            self.birth_date.setText(self.table.item(row, 2).text())
            self.birth_place.setText(self.table.item(row, 3).text())
            self.driver_address.setText(self.table.item(row, 4).text())  # Közvetlenül a címmezőbe
            self.mothers_name.setText(self.table.item(row, 5).text())
            self.tax_number.setText(self.table.item(row, 6).text())
            self.social_security_number.setText(self.table.item(row, 7).text())
            self.bank_name.setText(self.table.item(row, 8).text())
            self.bank_account.setText(self.table.item(row, 9).text())
        
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Hiba történt az adatok betöltése során: {str(e)}")

    def loadDrivers(self):
        """Sofőrök betöltése a táblázatba"""
        try:
            drivers = self.db.execute_query("""
                SELECT id, name, birth_date, birth_place, address,
                       mothers_name, tax_number, social_security_number,
                       bank_name, bank_account, drivers_license_number,
                       drivers_license_expiry
                FROM drivers 
                ORDER BY name""")

            self.table.setRowCount(len(drivers))
            for row, driver in enumerate(drivers):
                for col, key in enumerate([
                    'id', 'name', 'birth_date', 'birth_place', 'address',
                    'mothers_name', 'tax_number', 'social_security_number',
                    'bank_name', 'bank_account', 'drivers_license_number',
                    'drivers_license_expiry'
                ]):
                    item = QTableWidgetItem(str(driver[key] if driver[key] else ""))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row, col, item)
                    
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Hiba történt az adatok betöltése során: {str(e)}")

    def clearFields(self):
        """Beviteli mezők törlése"""
        self.driver_name.clear()
        self.birth_date.clear()
        self.birth_place.clear()
        self.driver_address.clear()  # Csak egy címmező van
        self.mothers_name.clear()
        self.tax_number.clear()
        self.social_security_number.clear()
        self.bank_name.clear()
        self.bank_account.clear()