# -*- coding: utf-8 -*-
from PySide6.QtGui import QColor, QFont
import json
import os

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        
        # Alapértelmezett beállítások
        self.defaults = {
            'theme': 'Világos téma',
            'background_color': '#0078D7',  # Windows kék
            'font_color': '#000000',        # Fekete
            'font_family': 'Arial',
            'font_size': 10,
            'language': 'Magyar',
            'email_notifications': False,
            'push_notifications': False
        }

    def load_config(self):
        """Beállítások betöltése fájlból"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                print(f"Hiba a konfiguráció betöltésekor: {e}")
                return self.get_defaults()
        return self.get_defaults()

    def save_config(self):
        """Beállítások mentése fájlba"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as file:
                json.dump(self.config, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Hiba a konfiguráció mentésekor: {e}")

    def get(self, key, default=None):
        """Beállítás lekérése"""
        return self.config.get(key, self.defaults.get(key, default))

    def set(self, key, value):
        """Beállítás módosítása és mentése"""
        self.config[key] = value
        self.save_config()

    def get_defaults(self):
        """Alapértelmezett beállítások"""
        return self.defaults.copy()

    def reset_to_defaults(self):
        """Visszaállítás alapértelmezettre"""
        self.config = self.get_defaults()
        self.save_config()

    def get_theme_settings(self):
        """Téma beállítások lekérése"""
        return {
            'theme': self.get('theme'),
            'background_color': self.get('background_color'),
            'font_color': self.get('font_color'),
            'font_family': self.get('font_family'),
            'font_size': self.get('font_size')
        }

    def save_theme_settings(self, settings):
        """Téma beállítások mentése"""
        for key, value in settings.items():
            self.set(key, value)

    def get_color(self, key, default='#000000'):
        """Szín beállítás lekérése QColor objektumként"""
        color_str = self.get(key, default)
        return QColor(color_str)

    def get_font(self):
        """Betűtípus beállítások lekérése QFont objektumként"""
        font = QFont()
        font.setFamily(self.get('font_family'))
        font.setPointSize(self.get('font_size'))
        return font