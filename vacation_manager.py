# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QLabel, QMessageBox
from PySide6.QtCore import QDate
import sqlite3

class VacationManager:
    def __init__(self, db):
        self.db = db

    def updateVacationDisplay(self):
        try:
            current_year = QDate.currentDate().year()
            result = self.db.execute_query(
                "SELECT total_days, used_days FROM vacation_allowance WHERE year = ?",
                (current_year,)
            )
            if result:
                return result[0]['total_days'], result[0]['used_days']
            return 29, 0  # alapértelmezett értékek
        except Exception as e:
            print(f"Hiba: {str(e)}")
            return 29, 0
                
        except Exception as e:
            print(f"Hiba a szabadság megjelenítésekor: {str(e)}")

    def getVacationData(self, year):
        try:
            results = self.db.execute_query(
                "SELECT total_days, used_days FROM vacation_allowance WHERE year = ?",
                (year,)
            )
            if results:
                return results[0]
            return {'total_days': 29, 'used_days': 0}
        except Exception as e:
            print(f"Error getting vacation data: {str(e)}")
            return {'total_days': 29, 'used_days': 0}