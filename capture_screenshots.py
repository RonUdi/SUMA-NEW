#!/usr/bin/env python3
"""
SUMA GUI Screenshot Capture
Script to capture screenshots of all application screens
"""

import sys
import os
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from suma_gui.ui.windows.main_window import SumaMainWindow
from suma_gui.ui.dialogs.start_analysis_dialog import StartAnalysisDialog
from suma_gui.ui.dialogs.view_results_dialog import ViewResultsDialog
from suma_gui.ui.windows.results_viewer import ResultsViewer

class ScreenshotCapture:
    def __init__(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        
        # Create screenshots directory
        self.screenshots_dir = "screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
        self.current_step = 0
        self.steps = [
            self.capture_startup_screen,
            self.capture_analysis_dialog,
            self.capture_results_dialog,
            self.capture_results_viewer,
            self.finish_capture
        ]
    
    def start_capture(self):
        """Start the screenshot capture process"""
        print("Starting screenshot capture...")
        self.next_step()
    
    def next_step(self):
        """Move to the next screenshot step"""
        if self.current_step < len(self.steps):
            self.steps[self.current_step]()
            self.current_step += 1
        
    def capture_startup_screen(self):
        """Capture the startup screen"""
        print("Capturing startup screen...")
        
        self.main_window = SumaMainWindow()
        self.main_window.show()
        
        # Wait for window to be fully rendered
        QTimer.singleShot(500, lambda: self.save_screenshot(
            self.main_window, "01_startup_screen.png", self.next_step
        ))
    
    def capture_analysis_dialog(self):
        """Capture the start analysis dialog"""
        print("Capturing analysis dialog...")
        
        self.analysis_dialog = StartAnalysisDialog(self.main_window)
        self.analysis_dialog.show()
        
        # Fill in some sample data
        self.analysis_dialog.patient_id_edit.setText("001")
        self.analysis_dialog.treatment_id_edit.setText("01")
        
        QTimer.singleShot(500, lambda: self.save_screenshot(
            self.analysis_dialog, "02_analysis_dialog.png", self.next_step
        ))
    
    def capture_results_dialog(self):
        """Capture the view results dialog"""
        print("Capturing results dialog...")
        
        self.analysis_dialog.close()
        
        self.results_dialog = ViewResultsDialog(self.main_window)
        self.results_dialog.show()
        
        QTimer.singleShot(500, lambda: self.save_screenshot(
            self.results_dialog, "03_results_dialog.png", self.next_step
        ))
    
    def capture_results_viewer(self):
        """Capture the results viewer"""
        print("Capturing results viewer...")
        
        self.results_dialog.close()
        
        self.results_viewer = ResultsViewer(self.main_window)
        self.results_viewer.load_patient_data("001", "01")
        self.results_viewer.show()
        
        QTimer.singleShot(500, lambda: self.save_screenshot(
            self.results_viewer, "04_results_viewer.png", self.next_step
        ))
    
    def save_screenshot(self, widget, filename, callback):
        """Save a screenshot of the given widget"""
        try:
            # Ensure widget is visible and rendered
            widget.repaint()
            
            # Capture the screenshot
            pixmap = widget.grab()
            
            # Save to file
            filepath = os.path.join(self.screenshots_dir, filename)
            pixmap.save(filepath, 'PNG')
            
            print(f"✅ Saved: {filepath}")
            
            # Continue to next step
            QTimer.singleShot(100, callback)
            
        except Exception as e:
            print(f"❌ Error capturing {filename}: {e}")
            QTimer.singleShot(100, callback)
    
    def finish_capture(self):
        """Finish the capture process"""
        print("\n🎉 Screenshot capture completed!")
        print(f"Screenshots saved in: {os.path.abspath(self.screenshots_dir)}")
        
        # Close all windows
        for widget in [self.main_window, getattr(self, 'analysis_dialog', None), 
                      getattr(self, 'results_dialog', None), getattr(self, 'results_viewer', None)]:
            if widget:
                widget.close()
        
        # Quit application
        QTimer.singleShot(1000, self.app.quit)

def main():
    """Main function to run screenshot capture"""
    capture = ScreenshotCapture()
    capture.start_capture()
    
    # Run the application
    sys.exit(capture.app.exec_())

if __name__ == "__main__":
    main() 