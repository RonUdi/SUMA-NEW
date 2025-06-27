from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QLineEdit, QProgressBar, QGroupBox,
                           QFileDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from ...resources.styles import SumaStyles
from ...resources.colors import SumaColors
from ...core.signals import suma_signals

class AnalysisWorker(QThread):
    progress_updated = pyqtSignal(int, str)
    analysis_completed = pyqtSignal(str, str)
    
    def __init__(self, patient_id, treatment_id):
        super().__init__()
        self.patient_id = patient_id
        self.treatment_id = treatment_id
    
    def run(self):
        steps = [
            ("Loading DICOM files...", 15),
            ("Calculating TE₀ maps...", 25), 
            ("Performing image alignment...", 20),
            ("Computing ΔTE₀ and ΔIron...", 25),
            ("Generating reports...", 15),
            ("Analysis complete!", 0)
        ]
        
        current_progress = 0
        
        for step_name, step_duration in steps:
            self.progress_updated.emit(current_progress, step_name)
            
            for progress_increment in range(step_duration):
                current_progress += 1
                if current_progress <= 100:
                    self.progress_updated.emit(current_progress, step_name)
                    self.msleep(50)
        self.progress_updated.emit(100, "Analysis complete!")
        self.analysis_completed.emit(self.patient_id, self.treatment_id)

class StartAnalysisDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.setup_dialog()
        self.setup_ui()
        self.connect_signals()
    
    def setup_dialog(self):
        self.setWindowTitle("Start New Analysis")
        self.setMinimumSize(500, 400)
        self.setModal(True)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("Start New Analysis")
        title.setStyleSheet(SumaStyles.get_title_style())
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        patient_group = self._create_patient_group()
        layout.addWidget(patient_group)
        
        folders_group = self._create_folders_group()
        layout.addWidget(folders_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)
        
        buttons_layout = self._create_buttons()
        layout.addLayout(buttons_layout)
    
    def _create_patient_group(self):
        group = QGroupBox("Patient Information")
        layout = QVBoxLayout(group)
        
        patient_layout = QHBoxLayout()
        patient_layout.addWidget(QLabel("Patient ID:"))
        self.patient_id_edit = QLineEdit()
        self.patient_id_edit.setPlaceholderText("e.g., 001")
        patient_layout.addWidget(self.patient_id_edit)
        layout.addLayout(patient_layout)
        
        treatment_layout = QHBoxLayout()
        treatment_layout.addWidget(QLabel("Treatment ID:"))
        self.treatment_id_edit = QLineEdit()
        self.treatment_id_edit.setPlaceholderText("e.g., 01")
        treatment_layout.addWidget(self.treatment_id_edit)
        layout.addLayout(treatment_layout)
        
        return group
    
    def _create_folders_group(self):
        """יצירת קבוצת בחירת תיקיות"""
        group = QGroupBox("Data Folders")
        layout = QVBoxLayout(group)
        
        # MRI PRE folder
        pre_layout = QHBoxLayout()
        pre_layout.addWidget(QLabel("MRI PRE:"))
        self.pre_folder_btn = QPushButton("Select Folder")
        self.pre_folder_btn.clicked.connect(lambda: self._select_folder("PRE"))
        pre_layout.addWidget(self.pre_folder_btn)
        layout.addLayout(pre_layout)
        
        # MRI POST folder  
        post_layout = QHBoxLayout()
        post_layout.addWidget(QLabel("MRI POST:"))
        self.post_folder_btn = QPushButton("Select Folder")
        self.post_folder_btn.clicked.connect(lambda: self._select_folder("POST"))
        post_layout.addWidget(self.post_folder_btn)
        layout.addLayout(post_layout)
        
        # CT folder
        ct_layout = QHBoxLayout()
        ct_layout.addWidget(QLabel("CT:"))
        self.ct_folder_btn = QPushButton("Select Folder")
        self.ct_folder_btn.clicked.connect(lambda: self._select_folder("CT"))
        ct_layout.addWidget(self.ct_folder_btn)
        layout.addLayout(ct_layout)
        
        return group
    
    def _create_buttons(self):
        """יצירת כפתורים"""
        layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.analyze_btn = QPushButton("Load & Analyze")
        self.analyze_btn.setStyleSheet(SumaStyles.get_primary_button_style())
        self.analyze_btn.clicked.connect(self.start_analysis)
        self.analyze_btn.setEnabled(False)
        
        layout.addStretch()
        layout.addWidget(self.cancel_btn)
        layout.addWidget(self.analyze_btn)
        
        return layout
    
    def connect_signals(self):
        """חיבור signals"""
        # Enable analyze button when patient ID is entered
        self.patient_id_edit.textChanged.connect(self._check_inputs)
        self.treatment_id_edit.textChanged.connect(self._check_inputs)
    
    def _select_folder(self, folder_type):
        """בחירת תיקייה"""
        folder = QFileDialog.getExistingDirectory(self, f"Select {folder_type} Folder")
        if folder:
            print(f"Selected {folder_type} folder: {folder}")
            self._check_inputs()
    
    def _check_inputs(self):
        """בדיקת תקינות קלטים"""
        patient_id = self.patient_id_edit.text().strip()
        treatment_id = self.treatment_id_edit.text().strip()
        
        # Enable analyze button if basic info is filled
        self.analyze_btn.setEnabled(bool(patient_id and treatment_id))
    
    def start_analysis(self):
        """התחלת ניתוח"""
        patient_id = self.patient_id_edit.text().strip()
        treatment_id = self.treatment_id_edit.text().strip()
        
        if not patient_id or not treatment_id:
            return
        
        # השבתת כל הכפתורים והשדות במהלך הניתוח
        self.analyze_btn.setEnabled(False)
        self.patient_id_edit.setEnabled(False)
        self.treatment_id_edit.setEnabled(False)
        self.pre_folder_btn.setEnabled(False)
        self.post_folder_btn.setEnabled(False)
        self.ct_folder_btn.setEnabled(False)
        
        self.cancel_btn.setText("Cancel Analysis")
        self.progress_bar.setVisible(True)
        self.status_label.setVisible(True)
        
        # התחלת worker thread
        self.worker = AnalysisWorker(patient_id, treatment_id)
        self.worker.progress_updated.connect(self._update_progress)
        self.worker.analysis_completed.connect(self._analysis_completed)
        self.worker.start()
    
    def _update_progress(self, progress, status):
        """עדכון progress"""
        self.progress_bar.setValue(progress)
        self.status_label.setText(status)
    
    def _analysis_completed(self, patient_id, treatment_id):
        """סיום ניתוח"""
        self.status_label.setText("Analysis completed successfully!")
        
        # הצגת כפתור View Results
        self.cancel_btn.setText("Close")
        
        view_results_btn = QPushButton("View Results")
        view_results_btn.setStyleSheet(SumaStyles.get_primary_button_style())
        view_results_btn.clicked.connect(lambda: self._view_results(patient_id, treatment_id))
        
        # הוספת כפתור לlayout
        buttons_layout = self.layout().itemAt(self.layout().count() - 1).layout()
        buttons_layout.addWidget(view_results_btn)
    
    def _view_results(self, patient_id, treatment_id):
        """הצגת תוצאות"""
        suma_signals.show_results_viewer.emit(patient_id, treatment_id)
        self.accept() 