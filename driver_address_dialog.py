from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, 
                             QLineEdit, QPushButton, QHBoxLayout)

class DriverAddressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lakcím megadása")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Címmezők létrehozása
        self.zip_code = QLineEdit()
        self.zip_code.setMaxLength(4)
        self.zip_code.setPlaceholderText("pl.: 1234")
        
        self.city = QLineEdit()
        self.city.setPlaceholderText("pl.: Budapest")
        
        self.street = QLineEdit()
        self.street.setPlaceholderText("pl.: Kossuth utca")
        
        self.house_number = QLineEdit()
        self.house_number.setPlaceholderText("pl.: 1")
        
        self.floor = QLineEdit()
        self.floor.setPlaceholderText("pl.: 3")
        
        self.door = QLineEdit()
        self.door.setPlaceholderText("pl.: 12")
        
        # Mezők hozzáadása
        form_layout.addRow("Irányítószám:", self.zip_code)
        form_layout.addRow("Város:", self.city)
        form_layout.addRow("Utca:", self.street)
        form_layout.addRow("Házszám:", self.house_number)
        form_layout.addRow("Emelet:", self.floor)
        form_layout.addRow("Ajtó:", self.door)
        
        # Gombok
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Mentés")
        cancel_btn = QPushButton("Mégsem")
        
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_address(self):
        """Visszaadja a formázott címet"""
        address_parts = [
            f"{self.zip_code.text()} {self.city.text()}",
            self.street.text(),
            self.house_number.text()
        ]
        
        # Ha van emelet/ajtó, hozzáadjuk
        if self.floor.text() or self.door.text():
            floor_door = f"{self.floor.text()}/{self.door.text()}"
            address_parts.append(floor_door.rstrip('/'))
            
        return ", ".join(part for part in address_parts if part)
    
    def set_address(self, address):
        """Kitölti a mezőket egy meglévő címből"""
        try:
            # Alap szétválasztás
            parts = address.split(', ')
            if len(parts) >= 1:
                zip_city = parts[0].split(' ', 1)
                if len(zip_city) == 2:
                    self.zip_code.setText(zip_city[0])
                    self.city.setText(zip_city[1])
            
            if len(parts) >= 2:
                self.street.setText(parts[1])
            
            if len(parts) >= 3:
                house_parts = parts[2].split('/')
                self.house_number.setText(house_parts[0])
                
                if len(house_parts) > 1:
                    floor_door = house_parts[1].split('.')
                    if len(floor_door) == 2:
                        self.floor.setText(floor_door[0])
                        self.door.setText(floor_door[1])
                    else:
                        self.floor.setText(floor_door[0])
                        
        except Exception as e:
            print(f"Hiba a cím feldolgozása során: {str(e)}")