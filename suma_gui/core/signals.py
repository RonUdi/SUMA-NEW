from PyQt5.QtCore import QObject, pyqtSignal

class SumaSignals(QObject):
    show_startup_screen = pyqtSignal()
    show_analysis_dialog = pyqtSignal()
    show_results_dialog = pyqtSignal()
    show_results_viewer = pyqtSignal(str, str)
    analysis_started = pyqtSignal(str, str)
    analysis_completed = pyqtSignal(str, str)
    analysis_progress = pyqtSignal(int, str)
    export_pdf_requested = pyqtSignal()
    app_exit_requested = pyqtSignal()

suma_signals = SumaSignals() 