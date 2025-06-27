"""
Patient Entity - Data model for patient information
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Patient:
    """מודל נתוני מטופל"""
    patient_id: str
    age: Optional[int] = None
    gender: Optional[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @property
    def display_name(self) -> str:
        """שם להצגה - רק מזהה המטופל"""
        return self.patient_id
    
    def validate(self) -> bool:
        """בדיקת תקינות נתונים"""
        return bool(self.patient_id and len(self.patient_id.strip()) > 0) 