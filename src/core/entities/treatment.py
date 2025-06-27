"""
Treatment Entity - Data model for treatment sessions
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path

@dataclass
class Treatment:
    """מודל נתוני טיפול"""
    patient_id: str
    treatment_id: str
    date: Optional[datetime] = None
    notes: Optional[str] = None
    
    # נתיבי תיקיות DICOM
    mri_pre_folder: Optional[str] = None
    mri_post_folder: Optional[str] = None
    ct_folder: Optional[str] = None
    
    # מטא-דטה
    created_at: datetime = None
    status: str = "created"  # created, processing, completed, failed
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.date is None:
            self.date = datetime.now()
    
    @property
    def display_name(self) -> str:
        """שם להצגה"""
        return f"{self.patient_id}_{self.treatment_id}"
    
    @property
    def data_folder(self) -> Path:
        """תיקיית נתונים של הטיפול"""
        return Path("Patient_data") / self.patient_id / self.treatment_id
    
    def validate(self) -> bool:
        """בדיקת תקינות נתונים"""
        return bool(
            self.patient_id and 
            self.treatment_id and 
            len(self.patient_id.strip()) > 0 and 
            len(self.treatment_id.strip()) > 0
        )
    
    def has_required_folders(self) -> bool:
        """בדיקה האם יש את כל התיקיות הנדרשות"""
        return bool(
            self.mri_pre_folder and 
            self.mri_post_folder and 
            self.ct_folder and
            Path(self.mri_pre_folder).exists() and
            Path(self.mri_post_folder).exists() and
            Path(self.ct_folder).exists()
        ) 