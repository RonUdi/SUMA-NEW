"""
SUMA GUI Main Window
Application main window and navigation controller
"""

from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication
from PyQt5.QtCore import Qt

from .startup_screen import StartupScreen
from .results_viewer import ResultsViewer
from ..dialogs.start_analysis_dialog import StartAnalysisDialog
from ..dialogs.view_results_dialog import ViewResultsDialog
from ...resources.styles import SumaStyles
from ...core.signals import suma_signals
from ...config.constants import WINDOW_TITLE, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT

class SumaMainWindow(QMainWindow):
    """חלון ראשי ובקר ניווט"""
    
    def __init__(self):
        super().__init__()
        self.signals = suma_signals
        self.setup_window()
        self.setup_ui()
        self.connect_signals()
    
    def setup_window(self):
        """הגדרת חלון"""
        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        
        # Apply main stylesheet
        self.setStyleSheet(SumaStyles.get_main_stylesheet())
    
    def setup_ui(self):
        """בניית ממשק"""
        # Stacked widget לניהול מסכים
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # יצירת מסכים
        self.startup_screen = StartupScreen()
        self.results_viewer = ResultsViewer()
        
        # הוספת מסכים לstack
        self.stacked_widget.addWidget(self.startup_screen)
        self.stacked_widget.addWidget(self.results_viewer)
        
        # התחלה במסך פתיחה
        self.stacked_widget.setCurrentWidget(self.startup_screen)
    
    def connect_signals(self):
        """חיבור signals"""
        # Navigation signals
        self.signals.show_startup_screen.connect(self.show_startup_screen)
        self.signals.show_analysis_dialog.connect(self.show_analysis_dialog)
        self.signals.show_results_dialog.connect(self.show_results_dialog)
        self.signals.show_results_viewer.connect(self.show_results_viewer)
        
        # Export signals
        self.signals.export_pdf_requested.connect(self.handle_export_pdf)
        
        # Application signals
        self.signals.app_exit_requested.connect(self.close)
    
    def show_startup_screen(self):
        """הצגת מסך פתיחה"""
        self.stacked_widget.setCurrentWidget(self.startup_screen)
    
    def show_analysis_dialog(self):
        """הצגת דיאלוג ניתוח"""
        dialog = StartAnalysisDialog(self)
        dialog.exec_()
    
    def show_results_dialog(self):
        """הצגת דיאלוג תוצאות"""
        dialog = ViewResultsDialog(self)
        dialog.exec_()
    
    def show_results_viewer(self, patient_id, treatment_id):
        """הצגת מציג תוצאות"""
        self.results_viewer.load_patient_data(patient_id, treatment_id)
        self.stacked_widget.setCurrentWidget(self.results_viewer)
    
    def handle_export_pdf(self):
        """טיפול בייצוא PDF"""
        print("Export PDF requested...")  # TODO: Implement actual export 