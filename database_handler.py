import sqlite3
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

class DatabaseHandler:
    """Adatbázis kezelő osztály a fuvar adminisztrációs rendszerhez"""
    
    def __init__(self, db_path: str = 'fuvarok.db'):
        """
        Inicializálja az adatbázis kapcsolatot.
        
        Args:
            db_path: Az adatbázis fájl elérési útja
        """
        self.db_path = db_path
        self.conn = None
        self._create_connection()
        self._initialize_database()
        
    def _create_connection(self) -> None:
        """Létrehozza az adatbázis kapcsolatot"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except Exception as e:
            logging.error(f"Adatbázis kapcsolódási hiba: {str(e)}")
            raise

    def _initialize_database(self) -> None:
        """Létrehozza az összes szükséges táblát"""
        try:
            # Sofőrök tábla
            self.execute_query('''
                CREATE TABLE IF NOT EXISTS drivers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    birth_date TEXT,
                    birth_place TEXT,
                    address TEXT,
                    mothers_name TEXT,
                    tax_number TEXT,
                    social_security_number TEXT,
                    bank_name TEXT,
                    bank_account TEXT,
                    drivers_license_number TEXT,
                    drivers_license_expiry TEXT,
                    vacation_days INTEGER DEFAULT 29,
                    used_vacation_days INTEGER DEFAULT 0
                )
            ''')

            # Járművek tábla
            self.execute_query('''
                CREATE TABLE IF NOT EXISTS vehicles (
                    id INTEGER PRIMARY KEY,
                    plate_number TEXT NOT NULL,
                    type TEXT,
                    brand TEXT,
                    model TEXT,
                    year_of_manufacture INTEGER,
                    chassis_number TEXT,
                    engine_number TEXT,
                    engine_type TEXT,
                    fuel_type TEXT,
                    max_weight INTEGER,
                    own_weight INTEGER,
                    payload_capacity INTEGER,
                    seats INTEGER,
                    technical_review_date TEXT,
                    tachograph TEXT,
                    tachograph_calibration_date TEXT,
                    fire_extinguisher_expiry TEXT
                )
            ''')

            # Gyárak és kapcsolódó táblák
            self.execute_query('''
                CREATE TABLE IF NOT EXISTS factories (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.execute_query('''
                CREATE TABLE IF NOT EXISTS factory_zone_prices (
                    id INTEGER PRIMARY KEY,
                    factory_id INTEGER,
                    zone_name TEXT,
                    price INTEGER DEFAULT 0,
                    FOREIGN KEY (factory_id) REFERENCES factories(id)
                )
            ''')

            self.execute_query('''
                CREATE TABLE IF NOT EXISTS factory_waiting_fees (
                    id INTEGER PRIMARY KEY,
                    factory_id INTEGER NOT NULL,
                    price_per_15_min INTEGER DEFAULT 0,
                    FOREIGN KEY (factory_id) REFERENCES factories(id)
                )
            ''')

            # Címek tábla
            self.execute_query('''
                CREATE TABLE IF NOT EXISTS addresses (
                    id INTEGER PRIMARY KEY,
                    address TEXT NOT NULL UNIQUE,
                    price INTEGER DEFAULT 0
                )
            ''')

            # Fuvarok tábla
            self.execute_query('''
                CREATE TABLE IF NOT EXISTS deliveries (
                    id INTEGER PRIMARY KEY,
                    delivery_date TEXT NOT NULL,
                    driver_id INTEGER,
                    vehicle_id INTEGER,
                    factory_id INTEGER,
                    zone_id INTEGER,
                    address_id INTEGER,
                    delivery_number TEXT NOT NULL,
                    amount REAL,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (driver_id) REFERENCES drivers(id),
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
                    FOREIGN KEY (factory_id) REFERENCES factories(id),
                    FOREIGN KEY (zone_id) REFERENCES factory_zone_prices(id),
                    FOREIGN KEY (address_id) REFERENCES addresses(id)
                )
            ''')

            # Szabadság nyilvántartás
            self.execute_query('''
                CREATE TABLE IF NOT EXISTS vacation_allowance (
                    id INTEGER PRIMARY KEY,
                    year INTEGER NOT NULL,
                    total_days INTEGER DEFAULT 29,
                    used_days INTEGER DEFAULT 0,
                    UNIQUE(year)
                )
            ''')

            # Üzemanyag fogyasztás
            self.execute_query('''
                CREATE TABLE IF NOT EXISTS fuel_consumption (
                    id INTEGER PRIMARY KEY,
                    vehicle_id INTEGER,
                    date TEXT,
                    odometer_reading INTEGER,
                    fuel_amount REAL,
                    fuel_price REAL,
                    total_cost REAL,
                    location TEXT,
                    full_tank BOOLEAN,
                    avg_consumption REAL,
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
                )
            ''')

        except Exception as e:
            logging.error(f"Adatbázis inicializálási hiba: {str(e)}")
            raise

    def execute_query(self, query: str, params: tuple = ()) -> Any:
        """
        SQL lekérdezés végrehajtása
        
        Args:
            query: SQL lekérdezés szövege
            params: Lekérdezés paraméterei
            
        Returns:
            Lekérdezés eredménye vagy None
        """
        try:
            if not self.conn:
                self._create_connection()
            
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            
            if query.lower().strip().startswith(('insert', 'update', 'delete')):
                self.conn.commit()
                return cursor.lastrowid
            
            return cursor.fetchall()
            
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logging.error(f"SQL végrehajtási hiba: {str(e)}")
            raise

    def insert_record(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        Új rekord beszúrása
        
        Args:
            table_name: Tábla neve
            data: Beszúrandó adatok dictionary formában
            
        Returns:
            Az új rekord ID-ja
        """
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            return self.execute_query(query, tuple(data.values()))
            
        except Exception as e:
            logging.error(f"Beszúrási hiba: {str(e)}")
            raise

    def load_factories(self) -> List[sqlite3.Row]:
        """Betölti az összes gyárat"""
        try:
            return self.execute_query("SELECT * FROM factories ORDER BY name")
        except Exception as e:
            logging.error(f"Gyárak betöltési hiba: {str(e)}")
            return []

    def __del__(self):
        """Destruktor - lezárja az adatbázis kapcsolatot"""
        if self.conn:
            try:
                self.conn.close()
            except:
                pass