"""
SUMA GUI Results Viewer
Results visualization with Napari integration
"""

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                           QFrame, QSlider, QWidget)
from PyQt5.QtCore import Qt

from ..components.base_widget import SumaBaseWidget
from ...resources.styles import SumaStyles
from ...resources.colors import SumaColors
from ...resources.layer_colors import LayerColormaps
from ...config.constants import ANALYSIS_LAYERS

class ResultsViewer(SumaBaseWidget):
    """מציג תוצאות עם ויזואליזציה 3D"""
    
    def __init__(self, parent=None):
        self.current_patient = None
        self.current_treatment = None
        super().__init__(parent)
    
    def setup_ui(self):
        """בניית מציג התוצאות"""
        layout = QVBoxLayout(self)
        
        # Top bar - מידע מטופל
        top_bar = self._create_top_bar()
        layout.addWidget(top_bar)
        
        # Main viewer area
        viewer_area = self._create_viewer_area()
        layout.addWidget(viewer_area)
        
        # Bottom controls
        controls = self._create_controls()
        layout.addWidget(controls)
    
    def _create_top_bar(self):
        """יצירת סרגל עליון"""
        top_bar = QFrame()
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {SumaColors.WHITE};
                border-bottom: 2px solid {SumaColors.BRAND_BLUE};
            }}
        """)
        
        layout = QHBoxLayout(top_bar)
        
        self.patient_info_label = QLabel("Patient: --- | Treatment: ---")
        self.patient_info_label.setStyleSheet(f"""
            QLabel {{
                color: {SumaColors.TEXT_PRIMARY};
                font-weight: bold;
                font-size: 16px;
            }}
        """)
        
        self.back_btn = QPushButton("← Back")
        self.back_btn.setStyleSheet(SumaStyles.get_primary_button_style())
        
        layout.addWidget(self.patient_info_label)
        layout.addStretch()
        layout.addWidget(self.back_btn)
        
        return top_bar
    
    def _create_viewer_area(self):
        """יצירת אזור הצגה"""
        viewer_widget = QWidget()
        viewer_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {SumaColors.IMAGE_DISPLAY_BG};
                border: 2px dashed {SumaColors.FIELD_BORDER};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(viewer_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Napari viewer area
        info_text = f"""
        Napari 3D Viewer
        
        Analysis Layers:
        {' • '.join(ANALYSIS_LAYERS)}
        
        Colormaps:
        • ΔTE₀: {LayerColormaps.DELTA_TE0}
        • Iron: {LayerColormaps.IRON}
        • PRE TE₁: {LayerColormaps.PRE_TE1}
        • POST TE₁: {LayerColormaps.POST_TE1}
        • CT: {LayerColormaps.CT}
        """
        
        info_label = QLabel(info_text)
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet(f"""
            QLabel {{
                color: {SumaColors.TEXT_SECONDARY};
                font-size: 14px;
                padding: 20px;
            }}
        """)
        
        layout.addWidget(info_label)
        
        return viewer_widget
    
    def _create_controls(self):
        """יצירת פקדים תחתונים"""
        controls_frame = QFrame()
        controls_frame.setFixedHeight(60)
        controls_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {SumaColors.WHITE};
                border-top: 1px solid {SumaColors.LIGHT_BORDER};
            }}
        """)
        
        layout = QHBoxLayout(controls_frame)
        
        # Slice slider
        slice_label = QLabel("Slice:")
        self.slice_slider = QSlider(Qt.Horizontal)
        self.slice_slider.setRange(0, 100)
        self.slice_slider.setValue(50)
        
        # 3D toggle
        self.toggle_3d_btn = QPushButton("3D View")
        self.toggle_3d_btn.setCheckable(True)
        
        # Export button
        self.export_btn = QPushButton("Export PDF")
        self.export_btn.setStyleSheet(SumaStyles.get_primary_button_style())
        
        layout.addWidget(slice_label)
        layout.addWidget(self.slice_slider)
        layout.addWidget(self.toggle_3d_btn)
        layout.addStretch()
        layout.addWidget(self.export_btn)
        
        return controls_frame
    
    def apply_styles(self):
        """החלת סגנונות - כבר מוחל ב-setup_ui"""
        pass
    
    def connect_signals(self):
        """חיבור signals"""
        self.back_btn.clicked.connect(self.signals.show_startup_screen.emit)
        self.export_btn.clicked.connect(self.signals.export_pdf_requested.emit)
    
    def load_patient_data(self, patient_id, treatment_id):
        """טעינת נתוני מטופל"""
        self.current_patient = patient_id
        self.current_treatment = treatment_id
        self.patient_info_label.setText(f"Patient: {patient_id} | Treatment: {treatment_id}") 