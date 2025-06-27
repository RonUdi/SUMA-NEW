#!/usr/bin/env python3
"""
SUMA GUI - Main Application Entry Point
Professional GUI for SUMA 3 analysis workflow
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from suma_gui.ui.windows.main_window import SumaMainWindow
from suma_gui.config.constants import APP_NAME, APP_VERSION, COMPANY_NAME

def main():
    """נקודת כניסה ראשית"""
    # יצירת אפליקציה
    app = QApplication(sys.argv)
    
    # הגדרות אפליקציה
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(COMPANY_NAME)
    
    # Enable high DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    try:
        # יצירת חלון ראשי
        main_window = SumaMainWindow()
        main_window.show()
        
        # הרצת אפליקציה
        return app.exec_()
        
    except Exception as e:
        print(f"Error starting {APP_NAME}: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 