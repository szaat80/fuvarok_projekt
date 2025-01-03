# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QPushButton, QLabel, QLineEdit, QDateEdit, QTimeEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QApplication, QMessageBox, QDialog
)
from PySide6.QtCore import Qt, QDate, QTime, QTimer
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
import sys
import sqlite3
import os
from datetime import datetime

from work_hours_manager import WorkHoursManager
from delivery_manager import DeliveryManager 
from vacation_manager import VacationManager
from database_manager import DatabaseManager
from database_handler import DatabaseHandler
from driver_file_manager import DriverFileManager
from menu_manager import MenuBar
from ui_manager import UIManager
from security.enhanced_auth import EnhancedAuthManager  # Új import
from security.login_dialog import LoginDialog

class FuvarAdminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseHandler('fuvarok.db')
        self.auth_manager = EnhancedAuthManager(self.db)
        
        if not self.show_login():
            sys.exit()
            
        self.initManagers()
        self.initUI()
        self.setupConnections()
        self.loadInitialData()

    def saveWorkHoursAndExport(self):
        if hasattr(self, 'work_hours_manager'):
            self.work_hours_manager.saveWorkHours()
        
        # Remove direct sqlite connection, use DatabaseHandler instead
        self.db = DatabaseHandler()
        self.initManagers()
        self.initUI()
        self.setupConnections()
        self.loadInitialData()

    def saveDeliveryAndExport(self):
        if hasattr(self, 'delivery_manager'):
            self.delivery_manager.saveDeliveryData()
        # További exportálási logika itt

    def show_login(self):
        login_dialog = LoginDialog(self.auth_manager, self)
        # Mindig középen jelenjen meg
        login_dialog.move(
            self.frameGeometry().center() - login_dialog.frameGeometry().center()
        )
        result = login_dialog.exec()
        if result == QDialog.Accepted:
            self.current_token = login_dialog.token
            return True
        return False

    def initManagers(self):
        self.work_hours_manager = WorkHoursManager(self)
        self.delivery_manager = DeliveryManager(self)
        self.vacation_manager = VacationManager(self)
        self.ui_manager = UIManager(self)
        self.database_manager = DatabaseManager(self)
        self.driver_file_manager = DriverFileManager()
        
        # Sofőr mappák létrehozása
        os.makedirs('driver_records', exist_ok=True)

    def initUI(self):
        # UI előkészítése
        self.setWindowTitle("Fuvar Adminisztráció")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
    
        # Komponensek inicializálása
        self.initializeComponents()
    
        # Layout létrehozása
        top_frame = self.ui_manager.createTopFrame()
        bottom_frame = self.ui_manager.createBottomFrame()
    
        # Táblázatok beállítása
        self.work_hours_manager.setup_work_table(self.work_table)
        self.delivery_manager.setup_delivery_table(self.delivery_table)
    
        # Összeállítás
        main_layout.addWidget(top_frame)
        main_layout.addWidget(bottom_frame)
        main_widget.setLayout(main_layout)
    
        self.setMenuBar(MenuBar(self))

    def initializeComponents(self):
        # Komponensek létrehozása
        self.driver_combo = QComboBox()
        self.vehicle_combo = QComboBox()
        self.date_edit = QDateEdit()
        self.start_time = QTimeEdit()
        self.end_time = QTimeEdit()
        self.type_combo = QComboBox()
        self.km_combo = QComboBox()
        self.factory_combo = QComboBox()
        self.address_combo = QComboBox()  # Átnevezve address_input-ről
        self.delivery_input = QLineEdit()
        self.m3_input = QLineEdit()
        self.m3_sum = QLabel("(0)")
        self.vacation_label = QLabel("Szabadság: 0/0")
        self.work_table = QTableWidget()
        self.delivery_table = QTableWidget()

        # Set up component properties
        self.setupComponentProperties()

    def setupComponentProperties(self):
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        
        self.type_combo.addItems([
            "Sima munkanap", 
            "Műhely nap", 
            "Szabadság", 
            "Betegszabadság (TP)"
        ])
        
        self.km_combo.addItems([
            f"Övezet {i}-{i+5}" for i in range(0, 50, 5)
        ])

    def setupConnections(self):
        self.driver_combo.currentTextChanged.connect(self.onDriverChanged)
        self.type_combo.currentTextChanged.connect(self.onWorkTypeChanged)
        self.m3_input.returnPressed.connect(self.delivery_manager.handleM3Input)

    def loadInitialData(self):
        self.loadDrivers()
        self.loadVehicles()
        self.loadFactories()
        self.loadAddresses()
        self.vacation_manager.updateVacationDisplay()

    def loadFactories(self):
        try:
            factories = self.db.load_factories()
            self.factory_combo.clear()
            self.factory_combo.addItems([factory['name'] for factory in factories])
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Gyárak betöltési hiba: {str(e)}")

    def loadDrivers(self):
        try:
            drivers = self.db.execute_query("SELECT name FROM drivers ORDER BY name")
            self.driver_combo.clear()
            self.driver_combo.addItems([driver['name'] for driver in drivers])
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Sofőrök betöltési hiba: {str(e)}")

    def loadVehicles(self):
        try:
            vehicles = self.db.execute_query("SELECT plate_number FROM vehicles ORDER BY plate_number")
            self.vehicle_combo.clear()
            self.vehicle_combo.addItems([vehicle['plate_number'] for vehicle in vehicles])
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Járművek betöltési hiba: {str(e)}")

    def loadAddresses(self):
        try:
            addresses = self.db.execute_query("SELECT address FROM addresses ORDER BY address")
            self.address_combo.clear()
            self.address_combo.addItems([addr['address'] for addr in addresses])
        except Exception as e:
            QMessageBox.critical(self, "Hiba", f"Címek betöltési hiba: {str(e)}")

    def onDriverChanged(self, driver):
        if driver:
            # Betöltjük mindkét táblázat adatait
            self.work_hours_manager.loadWorkHours(driver)
            self.delivery_manager.loadDeliveryData(driver)
            self.vacation_manager.updateVacationDisplay()

    def onWorkTypeChanged(self, work_type):
        if work_type == "Szabadság":
            self.vacation_manager.updateVacationDays()