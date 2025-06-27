"""
SUMA GUI View Results Dialog
Dialog for viewing existing analysis results
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtCore import Qt

from ...resources.styles import SumaStyles
from ...core.signals import suma_signals

class ViewResultsDialog(QDialog):
    """דיאלוג צפייה בתוצאות קיימות"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_dialog()
        self.setup_ui()
        self.load_sample_data()
        self.connect_signals()
    
    def setup_dialog(self):
        """הגדרת דיאלוג"""
        self.setWindowTitle("View Analysis Results")
        self.setMinimumSize(600, 500)
        self.setModal(True)
    
    def setup_ui(self):
        """בניית ממשק"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # כותרת
        title = QLabel("Analysis Results")
        title.setStyleSheet(SumaStyles.get_title_style())
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Tree widget לתוצאות
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["Patient/Treatment", "Date", "Status"])
        self.results_tree.setStyleSheet(SumaStyles.get_tree_widget_style())
        
        # הגדרת יישור שמאל עבור כל העמודות
        header = self.results_tree.header()
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # הגדרת רוחב עמודות
        self.results_tree.setColumnWidth(0, 200)  # Patient/Treatment
        self.results_tree.setColumnWidth(1, 120)  # Date
        self.results_tree.setColumnWidth(2, 100)  # Status
        
        self.results_tree.itemSelectionChanged.connect(self._on_selection_changed)
        self.results_tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.results_tree)
        
        # כפתורים
        buttons_layout = self._create_buttons()
        layout.addLayout(buttons_layout)
    
    def _create_buttons(self):
        """יצירת כפתורים"""
        layout = QHBoxLayout()
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.reject)
        
        self.view_btn = QPushButton("View Selected")
        self.view_btn.setStyleSheet(SumaStyles.get_primary_button_style())
        self.view_btn.clicked.connect(self._view_selected)
        self.view_btn.setEnabled(False)
        
        layout.addStretch()
        layout.addWidget(self.close_btn)
        layout.addWidget(self.view_btn)
        
        return layout
    
    def load_sample_data(self):
        """טעינת נתונים לדוגמה"""
        sample_data = [
            {
                "patient_id": "001",
                "treatments": [
                    {"treatment_id": "01", "date": "2024-01-15", "status": "Complete"},
                    {"treatment_id": "02", "date": "2024-02-20", "status": "Complete"}
                ]
            },
            {
                "patient_id": "002", 
                "treatments": [
                    {"treatment_id": "01", "date": "2024-01-20", "status": "Complete"}
                ]
            },
            {
                "patient_id": "003",
                "treatments": [
                    {"treatment_id": "01", "date": "2024-03-10", "status": "In Progress"}
                ]
            }
        ]
        
        for patient_data in sample_data:
            # יצירת פריט מטופל
            patient_item = QTreeWidgetItem(self.results_tree)
            patient_item.setText(0, f"Patient {patient_data['patient_id']}")
            patient_item.setText(2, f"{len(patient_data['treatments'])} treatments")
            
            # הגדרת יישור שמאל לכל העמודות
            for col in range(3):
                patient_item.setTextAlignment(col, Qt.AlignLeft | Qt.AlignVCenter)
            
            patient_item.setData(0, Qt.UserRole, {
                "type": "patient", 
                "patient_id": patient_data['patient_id']
            })
            
            # הוספת טיפולים
            for treatment in patient_data['treatments']:
                treatment_item = QTreeWidgetItem(patient_item)
                treatment_item.setText(0, f"Treatment {treatment['treatment_id']}")
                treatment_item.setText(1, treatment['date'])
                treatment_item.setText(2, treatment['status'])
                
                # הגדרת יישור שמאל לכל העמודות
                for col in range(3):
                    treatment_item.setTextAlignment(col, Qt.AlignLeft | Qt.AlignVCenter)
                
                treatment_item.setData(0, Qt.UserRole, {
                    "type": "treatment",
                    "patient_id": patient_data['patient_id'],
                    "treatment_id": treatment['treatment_id']
                })
        
        # הרחבת כל הפריטים
        self.results_tree.expandAll()
        
        # וידוא יישור שמאל לכל הפריטים
        self._ensure_left_alignment()
    
    def _ensure_left_alignment(self):
        """וידוא יישור שמאל לכל הפריטים"""
        root = self.results_tree.invisibleRootItem()
        for i in range(root.childCount()):
            patient_item = root.child(i)
            # יישור שמאל לפריט המטופל
            for col in range(self.results_tree.columnCount()):
                patient_item.setTextAlignment(col, Qt.AlignLeft | Qt.AlignVCenter)
            
            # יישור שמאל לכל הטיפולים
            for j in range(patient_item.childCount()):
                treatment_item = patient_item.child(j)
                for col in range(self.results_tree.columnCount()):
                    treatment_item.setTextAlignment(col, Qt.AlignLeft | Qt.AlignVCenter)
    
    def connect_signals(self):
        """חיבור signals"""
        pass
    
    def _on_selection_changed(self):
        """טיפול בשינוי בחירה"""
        selected_items = self.results_tree.selectedItems()
        if selected_items:
            item = selected_items[0]
            data = item.data(0, Qt.UserRole)
            # אפשר כפתור View רק עבור טיפולים שהושלמו
            is_treatment = data and data.get("type") == "treatment"
            self.view_btn.setEnabled(is_treatment)
        else:
            self.view_btn.setEnabled(False)
    
    def _on_item_double_clicked(self, item, column):
        """טיפול בלחיצה כפולה"""
        data = item.data(0, Qt.UserRole)
        if data and data.get("type") == "treatment":
            self._view_selected()
    
    def _view_selected(self):
        """הצגת הטיפול הנבחר"""
        selected_items = self.results_tree.selectedItems()
        if selected_items:
            item = selected_items[0]
            data = item.data(0, Qt.UserRole)
            
            if data and data.get("type") == "treatment":
                patient_id = data["patient_id"]
                treatment_id = data["treatment_id"]
                
                # שליחת signal להצגת תוצאות
                suma_signals.show_results_viewer.emit(patient_id, treatment_id)
                self.accept() 