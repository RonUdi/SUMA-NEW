from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from ...resources.styles import SumaStyles
from ...core.signals import suma_signals

class SumaBaseWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = suma_signals
        self.setup_ui()
        self.apply_styles()
        self.connect_signals()
    
    def setup_ui(self):
        pass
    
    def apply_styles(self):
        pass
    
    def connect_signals(self):
        pass 