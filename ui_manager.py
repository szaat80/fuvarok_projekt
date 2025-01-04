# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, QDate

class UIManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.styles = self.setupStyles()

    def setupStyles(self):
        return {
            'main_frame': """
                QFrame {
                    background-color: #2d2d2d;
                    border: 3px solid #3e3e3e;
                    border-radius: 15px;
                    margin: 5px;
                }
            """,
            'sub_frame': """
                QFrame {
                    background-color: #d9d9d9;
                    border: 2px solid #4d4d4d;
                    border-radius: 15px;
                    margin: 5px;
                }
            """,
            'table_frame': """
                QFrame {
                    background-color: #d9d9d9;
                    border: 3px solid #ff2800;
                    border-radius: 15px;
                    padding: 10px;
                }
            """,
            'label': """
                QLabel {
                    color: black;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 5px;
                }
            """,
            'input': """
                QLineEdit, QDateEdit, QTimeEdit, QComboBox {
                    background-color: white; 
                    padding: 5px;
                    border: 2px solid #a0a0a0;
                    border-radius: 5px;
                    color: black;
                    min-width: 150px;
                    max-width: 150px;
                    min-height: 30px;
                    max-height: 30px;
                    font-size: 14px;
                }
            """,
            'button': """
                QPushButton {
                    background-color: #4a90e2;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: #357abd;
                }
            """
        }

    def createInputGroup(self, label_text, widget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet(self.styles['label'])
        layout.addWidget(label)
        widget.setStyleSheet(self.styles['input'])
        layout.addWidget(widget)
        layout.addStretch()
        return layout

    def createTopFrame(self):
        top_frame = QFrame()
        top_frame.setStyleSheet(self.styles['main_frame'])
        top_layout = QHBoxLayout()
        
        left_panel = self.createLeftPanel()
        middle_panel = self.createMiddlePanel()
        right_panel = self.createRightPanel()
        
        top_layout.addWidget(left_panel)
        top_layout.addWidget(middle_panel)
        top_layout.addWidget(right_panel)
        
        top_frame.setLayout(top_layout)
        return top_frame

    def createLeftPanel(self):
        panel = QFrame()
        panel.setStyleSheet(self.styles['sub_frame'])
        layout = QVBoxLayout()
        
        layout.addLayout(self.createInputGroup("Sofőr:", self.parent.driver_combo))
        layout.addLayout(self.createInputGroup("Rendszám:", self.parent.vehicle_combo))
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel

    def createMiddlePanel(self):
        panel = QFrame()
        panel.setStyleSheet(self.styles['sub_frame'])
        layout = QVBoxLayout()
        
        layout.addLayout(self.createInputGroup("Dátum:", self.parent.date_edit))
        layout.addLayout(self.createInputGroup("Kezdés:", self.parent.start_time))
        layout.addLayout(self.createInputGroup("Végzés:", self.parent.end_time))
        layout.addLayout(self.createInputGroup("Munka típusa:", self.parent.type_combo))
        
        self.parent.vacation_label.setStyleSheet(self.styles['label'])
        layout.addWidget(self.parent.vacation_label)
        
        workhours_button_layout = QHBoxLayout()
        save_workhours_btn = QPushButton("Munkaórák Mentése")
        save_workhours_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF2800;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #CC2000;
            }
        """)
        save_workhours_btn.clicked.connect(self.parent.work_hours_manager.saveWorkHours)
        workhours_button_layout.addWidget(save_workhours_btn)
        workhours_button_layout.addStretch()
        layout.addLayout(workhours_button_layout)
        
        panel.setLayout(layout)
        return panel

    def createRightPanel(self):
        panel = QFrame()
        panel.setStyleSheet(self.styles['sub_frame'])
        layout = QVBoxLayout()
    
        delivery_button_layout = QHBoxLayout()
        save_delivery_btn = QPushButton("Fuvar Adatok Mentése")
        save_delivery_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF2800;
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #CC2000;
            }
        """)
        save_delivery_btn.clicked.connect(lambda: self.parent.saveDeliveryAndExport)
        delivery_button_layout.addWidget(save_delivery_btn)
        delivery_button_layout.addStretch()
        layout.addLayout(delivery_button_layout)
    
        layout.addLayout(self.createInputGroup("Kilométer sáv:", self.parent.km_combo))
        layout.addLayout(self.createInputGroup("Gyár:", self.parent.factory_combo))
        layout.addLayout(self.createInputGroup("Cím:", self.parent.address_combo))  # Javítva
        layout.addLayout(self.createInputGroup("Szállítószám:", self.parent.delivery_input))
    
        m3_layout = QHBoxLayout()
        m3_label = QLabel("M3:")
        m3_label.setStyleSheet(self.styles['label'])
        m3_layout.addWidget(m3_label)
        m3_layout.addWidget(self.parent.m3_input)
        m3_layout.addWidget(self.parent.m3_sum)
        m3_layout.addStretch()
        layout.addLayout(m3_layout)
    
        panel.setLayout(layout)
        return panel

    def createBottomFrame(self):
        bottom_frame = QFrame()
        bottom_frame.setStyleSheet(self.styles['main_frame'])
        bottom_layout = QHBoxLayout()
        
        work_frame = self.createWorkFrame()
        delivery_frame = self.createDeliveryFrame()
        
        bottom_layout.addWidget(work_frame)
        bottom_layout.addWidget(delivery_frame)
        
        bottom_frame.setLayout(bottom_layout)
        return bottom_frame

    def createWorkFrame(self):
        frame = QFrame()
        frame.setStyleSheet(self.getTableFrameStyle())
        layout = QVBoxLayout()
        
        self.setupWorkTable()
        layout.addWidget(self.parent.work_table)
        
        frame.setLayout(layout)
        return frame

    def createDeliveryFrame(self):
        frame = QFrame()
        frame.setStyleSheet(self.getTableFrameStyle())
        layout = QVBoxLayout()
        
        self.setupDeliveryTable()
        layout.addWidget(self.parent.delivery_table)
        
        frame.setLayout(layout)
        return frame

    def getTableFrameStyle(self):
        return """
            QFrame {
                background-color: white;
                border: 3px solid #ff2800;
                border-radius: 15px;
                padding: 10px;
            }
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #808080;
                border: 1px solid #808080;
                border-radius: 0px;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #808080;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: black;
                padding: 5px;
                border: 1px solid #808080;
                font-weight: bold;
                font-size: 12px;
            }
            QHeaderView::section:selected {
                background-color: #e0e0e0;
            }
        """

    def setupWorkTable(self):
        self.parent.work_table = QTableWidget()
        self.setupTableHeader(self.parent.work_table, [
            "Dátum", "Nap", 
            "Sima Munkanap\nKezdés", "Sima Munkanap\nVégzés", "Ledolgozott\nÓrák",
            "Műhely\nKezdés", "Műhely\nVégzés", "Ledolgozott\nÓrák",
            "Szabadság", "Betegszabadság\n(TP)"
        ])
        self.setupTableRows(self.parent.work_table)

    def setupDeliveryTable(self):
        self.parent.delivery_table = QTableWidget()
        headers = ["Dátum"] + [f"Övezet {i}-{i+5}" for i in range(0, 45, 5)]
        self.setupTableHeader(self.parent.delivery_table, headers)
        self.setupTableRows(self.parent.delivery_table)

    def setupTableHeader(self, table, headers):
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setMinimumHeight(80)
        table.verticalHeader().setVisible(False)

    def setupTableRows(self, table):
        current_date = QDate.currentDate()
        first_day = QDate(current_date.year(), current_date.month(), 1)
        days_in_month = first_day.daysInMonth()
        
        day_names = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']
        
        table.setRowCount(days_in_month)
        
        for i in range(days_in_month):
            current_day = first_day.addDays(i)
            date_str = current_day.toString('yyyy-MM-dd')
            
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 0, date_item)
            
            if table == self.parent.work_table:
                day_name = day_names[current_day.dayOfWeek() - 1]
                day_item = QTableWidgetItem(day_name)
                day_item.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, 1, day_item)
            
            # Initialize empty cells
            for col in range(2 if table == self.parent.work_table else 1, table.columnCount()):
                empty_item = QTableWidgetItem("")
                empty_item.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, col, empty_item)

    def setupTableStyles(self):
        # Egységes táblázat stílus
        table_style = """
            QTableWidget {
                background-color: white;
                border: 2px solid #a0a0a0;
            }
            QTableWidget::item {
                border: 1px solid #d0d0d0;
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #4a90e2;
                color: white;
                padding: 8px;
                border: 1px solid #2171c7;
                font-weight: bold;
                min-height: 25px;
            }
        """
    
        # Stílus alkalmazása mindkét táblázatra
        self.billing_table.setStyleSheet(table_style)
        self.billing_table.verticalHeader().setVisible(False)
        self.billing_table.horizontalHeader().setStretchLastSection(True)
        self.billing_table.setShowGrid(True)
        self.billing_table.setGridStyle(Qt.SolidLine)
    
        # Oszlopok beállítása
        headers = ["Dátum", "Sofőr", "Gyár", "Övezet", "Fuvarok száma", 
                  "Mennyiség (m³)", "Egységár", "Összeg", "Státusz"]
        self.billing_table.setColumnCount(len(headers))
        self.billing_table.setHorizontalHeaderLabels(headers)
    
        # Oszlopok méretezése
        for i in range(len(headers)):
            self.billing_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)