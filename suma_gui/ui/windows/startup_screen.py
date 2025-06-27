"""
SUMA GUI Startup Screen
Welcome screen with main action buttons
"""

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

from ..components.base_widget import SumaBaseWidget
from ...resources.styles import SumaStyles
from ...config.constants import APP_NAME

class StartupScreen(SumaBaseWidget):
    """מסך פתיחה עם כפתורי פעולה ראשיים"""
    
    def setup_ui(self):
        """בניית מסך הפתיחה"""
        layout = QVBoxLayout(self)
        layout.setSpacing(40)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # כותרת ראשית - SUMA בגדול
        main_title = QLabel("SUMA")
        main_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(main_title)
        
        # כותרת משנה - Wellcome to
        welcome_label = QLabel("Wellcome to Signal Utility MRI Analysis")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Spacer גדול יותר
        layout.addItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Spacer נוסף כדי לדחוף את הכפתורים למטה
        layout.addItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # כפתורי פעולה
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        
        self.start_analysis_btn = QPushButton("Start Analysis")
        self.view_results_btn = QPushButton("View Results")
        
        button_layout.addWidget(self.start_analysis_btn)
        button_layout.addWidget(self.view_results_btn)
        
        layout.addLayout(button_layout)
        
        # Spacer תחתון קטן יותר
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Footer
        footer = QLabel("© 2025 New Phase Ltd. - For internal research use only")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        
        # שמירת references
        self.main_title_label = main_title
        self.welcome_label = welcome_label
        self.footer_label = footer
    
    def apply_styles(self):
        """החלת סגנונות"""
        self.main_title_label.setStyleSheet(SumaStyles.get_main_title_style())
        self.welcome_label.setStyleSheet(SumaStyles.get_title_style())
        self.start_analysis_btn.setStyleSheet(SumaStyles.get_primary_button_style())
        self.view_results_btn.setStyleSheet(SumaStyles.get_primary_button_style())
    
    def connect_signals(self):
        """חיבור signals"""
        self.start_analysis_btn.clicked.connect(self.signals.show_analysis_dialog.emit)
        self.view_results_btn.clicked.connect(self.signals.show_results_dialog.emit) 