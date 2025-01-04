# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QSpinBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QMessageBox, QHeaderView, QComboBox)
from PySide6.QtCore import Qt
from database_handler import DatabaseHandler  # Change from uppercase to lowercase

class AddressManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseHandler()  # Inicializáljuk a DatabaseHandler példányt
        self.address_combo = QComboBox()
        self.address_combo.setEditable(True)  # Szerkeszthető legyen
        self.address_combo.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        self.initUI()  # Hívjuk meg az initUI metódust

    def initUI(self):
        self.setWindowTitle("Címek kezelése")
        layout = QVBoxLayout()

        # Beviteli mezők
        form_layout = QHBoxLayout()
        
        self.address = QLineEdit()
        self.address.setPlaceholderText("Cím")
        self.price = QSpinBox()
        self.price.setRange(0, 1000000)
        self.price.setSuffix(" Ft")
        
        form_layout.addWidget(QLabel("Cím:"))
        form_layout.addWidget(self.address)
        form_layout.addWidget(QLabel("Ár:"))
        form_layout.addWidget(self.price)
        
        layout.addLayout(form_layout)

        # Gombok
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Hozzáadás")
        delete_btn = QPushButton("Törlés")
        
        add_btn.clicked.connect(self.addAddress)
        delete_btn.clicked.connect(self.deleteAddress)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)
        layout.addLayout(btn_layout)

        # Táblázat
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Cím", "Ár"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.loadAddresses()

    def addAddress(self):
        address = self.address.text().strip()
        price = self.price.value()

        if not address:
            QMessageBox.warning(self, "Figyelmeztetés", "A cím megadása kötelező!")
            return

        try:
            data = {
                'address': address,
                'price': price
            }
            self.db.insert_record('addresses', data)
            
            self.address.clear()
            self.price.setValue(0)
            self.loadAddresses()
            
            QMessageBox.information(self, "Siker", "Cím sikeresen hozzáadva!")
        
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Hiba történt: {str(e)}")

    def deleteAddress(self):
        try:
            selected = self.table.selectedItems()
            if not selected:
                QMessageBox.warning(self, "Figyelmeztetés", "Válasszon ki egy címet!")
                return

            row = selected[0].row()
            address_id = int(self.table.item(row, 0).text())
        
            reply = QMessageBox.question(self, 'Megerősítés', 
                'Biztosan törli a kiválasztott címet?',
                QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.db.execute_query('DELETE FROM addresses WHERE id = ?', (address_id,))
                self.loadAddresses()
                QMessageBox.information(self, "Siker", "Cím törölve!")
    
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Hiba történt: {str(e)}")

    def loadAddresses(self):
        try:
            addresses = self.db.execute_query(
                "SELECT * FROM addresses ORDER BY address"
            )

            self.table.setRowCount(len(addresses))
            for row, address in enumerate(addresses):
                self.table.setItem(row, 0, QTableWidgetItem(str(address['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(address['address']))
                price_item = QTableWidgetItem(f"{address['price']:,} Ft")
                price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, 2, price_item)
                
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Betöltési hiba: {str(e)}")
