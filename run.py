# -*- coding: utf-8 -*-
import sys
import logging
from PySide6.QtWidgets import QApplication
from modified_main import FuvarAdminApp

logging.basicConfig(
   level=logging.DEBUG,
   format='%(asctime)s - %(levelname)s - %(message)s',
   filename='debug.log'
)

if __name__ == "__main__":
   try:
       app = QApplication(sys.argv)
       window = FuvarAdminApp()
       window.show()
       sys.exit(app.exec())
       
   except Exception as e:
       logging.error(f"Hiba: {str(e)}", exc_info=True)
       raise