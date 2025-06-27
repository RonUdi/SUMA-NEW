"""
Data Manager - Handles data persistence for SUMA system
"""

import json
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from .entities import Patient, Treatment, AnalysisResult

class SumaDataManager:
    """מנהל נתונים של SUMA"""
    
    def __init__(self, data_root: str = "Patient_data"):
        self.data_root = Path(data_root)
        self.reports_folder = self.data_root / "Reports"
        self.ensure_directories()
    
    def ensure_directories(self):
        """יצירת תיקיות נדרשות"""
        self.data_root.mkdir(exist_ok=True)
        self.reports_folder.mkdir(exist_ok=True)
    
    # ======== Patient Management ========
    
    def save_patient(self, patient: Patient) -> bool:
        """שמירת נתוני מטופל"""
        try:
            patient_folder = self.data_root / patient.patient_id
            patient_folder.mkdir(exist_ok=True)
            
            patient_file = patient_folder / "patient_info.json"
            patient_data = {
                'patient_id': patient.patient_id,
                'age': patient.age,
                'gender': patient.gender,
                'created_at': patient.created_at.isoformat() if patient.created_at else None
            }
            
            with open(patient_file, 'w', encoding='utf-8') as f:
                json.dump(patient_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving patient {patient.patient_id}: {e}")
            return False
    
    def load_patient(self, patient_id: str) -> Optional[Patient]:
        """טעינת נתוני מטופל"""
        try:
            patient_file = self.data_root / patient_id / "patient_info.json"
            
            if not patient_file.exists():
                # יצירת מטופל בסיסי אם הקובץ לא קיים
                return Patient(patient_id=patient_id)
            
            with open(patient_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            created_at = None
            if data.get('created_at'):
                created_at = datetime.fromisoformat(data['created_at'])
            
            return Patient(
                patient_id=data['patient_id'],
                age=data.get('age'),
                gender=data.get('gender'),
                created_at=created_at
            )
            
        except Exception as e:
            print(f"Error loading patient {patient_id}: {e}")
            return None
    
    def get_all_patient_ids(self) -> List[str]:
        """קבלת רשימת כל מזהי המטופלים"""
        try:
            if not self.data_root.exists():
                return []
            
            patient_ids = []
            for folder in self.data_root.iterdir():
                if folder.is_dir() and folder.name != "Reports":
                    patient_ids.append(folder.name)
            
            return sorted(patient_ids)
            
        except Exception as e:
            print(f"Error getting patient IDs: {e}")
            return []
    
    # ======== Treatment Management ========
    
    def save_treatment(self, treatment: Treatment) -> bool:
        """שמירת נתוני טיפול"""
        try:
            treatment_folder = self.data_root / treatment.patient_id / treatment.treatment_id
            treatment_folder.mkdir(parents=True, exist_ok=True)
            
            treatment_file = treatment_folder / "treatment_info.json"
            treatment_data = {
                'patient_id': treatment.patient_id,
                'treatment_id': treatment.treatment_id,
                'date': treatment.date.isoformat() if treatment.date else None,
                'notes': treatment.notes,
                'mri_pre_folder': treatment.mri_pre_folder,
                'mri_post_folder': treatment.mri_post_folder,
                'ct_folder': treatment.ct_folder,
                'created_at': treatment.created_at.isoformat() if treatment.created_at else None,
                'status': treatment.status
            }
            
            with open(treatment_file, 'w', encoding='utf-8') as f:
                json.dump(treatment_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving treatment {treatment.display_name}: {e}")
            return False
    
    def load_treatment(self, patient_id: str, treatment_id: str) -> Optional[Treatment]:
        """טעינת נתוני טיפול"""
        try:
            treatment_file = self.data_root / patient_id / treatment_id / "treatment_info.json"
            
            if not treatment_file.exists():
                return None
            
            with open(treatment_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            date = None
            if data.get('date'):
                date = datetime.fromisoformat(data['date'])
                
            created_at = None
            if data.get('created_at'):
                created_at = datetime.fromisoformat(data['created_at'])
            
            return Treatment(
                patient_id=data['patient_id'],
                treatment_id=data['treatment_id'],
                date=date,
                notes=data.get('notes'),
                mri_pre_folder=data.get('mri_pre_folder'),
                mri_post_folder=data.get('mri_post_folder'),
                ct_folder=data.get('ct_folder'),
                created_at=created_at,
                status=data.get('status', 'created')
            )
            
        except Exception as e:
            print(f"Error loading treatment {patient_id}_{treatment_id}: {e}")
            return None
    
    def get_patient_treatments(self, patient_id: str) -> List[str]:
        """קבלת רשימת טיפולים של מטופל"""
        try:
            patient_folder = self.data_root / patient_id
            if not patient_folder.exists():
                return []
            
            treatments = []
            for folder in patient_folder.iterdir():
                if folder.is_dir():
                    treatments.append(folder.name)
            
            return sorted(treatments)
            
        except Exception as e:
            print(f"Error getting treatments for patient {patient_id}: {e}")
            return []
    
    def get_all_treatments(self) -> List[Dict[str, str]]:
        """קבלת רשימת כל הטיפולים במערכת"""
        try:
            treatments = []
            for patient_id in self.get_all_patient_ids():
                for treatment_id in self.get_patient_treatments(patient_id):
                    treatments.append({
                        'patient_id': patient_id,
                        'treatment_id': treatment_id,
                        'display_name': f"{patient_id}_{treatment_id}"
                    })
            
            return treatments
            
        except Exception as e:
            print(f"Error getting all treatments: {e}")
            return []
    
    # ======== Analysis Results Management ========
    
    def save_analysis_result(self, result: AnalysisResult) -> bool:
        """שמירת תוצאות ניתוח"""
        try:
            results_folder = self.data_root / result.patient_id / result.treatment_id
            results_folder.mkdir(parents=True, exist_ok=True)
            
            # שמירת המערכים
            results_file = results_folder / "analyzed_maps.npz"
            if not result.save_to_file(results_file):
                return False
            
            # שמירת מטאדטה
            metadata_file = results_folder / "analysis_metadata.json"
            metadata = {
                'patient_id': result.patient_id,
                'treatment_id': result.treatment_id,
                'analysis_date': result.analysis_date.isoformat() if result.analysis_date else None,
                'analysis_duration': result.analysis_duration,
                'analysis_version': result.analysis_version,
                'stats': result.stats,
                'is_complete': result.is_complete
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving analysis result {result.display_name}: {e}")
            return False
    
    def load_analysis_result(self, patient_id: str, treatment_id: str) -> Optional[AnalysisResult]:
        """טעינת תוצאות ניתוח"""
        try:
            results_folder = self.data_root / patient_id / treatment_id
            results_file = results_folder / "analyzed_maps.npz"
            metadata_file = results_folder / "analysis_metadata.json"
            
            if not results_file.exists():
                return None
            
            # טעינת המערכים
            result = AnalysisResult.load_from_file(results_file, patient_id, treatment_id)
            if result is None:
                return None
            
            # טעינת מטאדטה אם קיימת
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                if metadata.get('analysis_date'):
                    result.analysis_date = datetime.fromisoformat(metadata['analysis_date'])
                result.analysis_duration = metadata.get('analysis_duration')
                result.analysis_version = metadata.get('analysis_version', '1.0.0')
                result.stats = metadata.get('stats', {})
            
            return result
            
        except Exception as e:
            print(f"Error loading analysis result {patient_id}_{treatment_id}: {e}")
            return None
    
    def has_analysis_result(self, patient_id: str, treatment_id: str) -> bool:
        """בדיקה האם קיימות תוצאות ניתוח"""
        results_file = self.data_root / patient_id / treatment_id / "analyzed_maps.npz"
        return results_file.exists()
    
    # ======== Utility Methods ========
    
    def create_treatment_folder_structure(self, patient_id: str, treatment_id: str) -> Path:
        """יצירת מבנה תיקיות לטיפול"""
        treatment_folder = self.data_root / patient_id / treatment_id
        treatment_folder.mkdir(parents=True, exist_ok=True)
        
        # יצירת תת-תיקיות
        (treatment_folder / "raw_dicom").mkdir(exist_ok=True)
        
        return treatment_folder
    
    def get_report_filepath(self, patient_id: str, treatment_id: str) -> Path:
        """קבלת נתיב קובץ הדוח"""
        return self.reports_folder / f"{patient_id}_{treatment_id}_report.pdf"

# אינסטנס גלובלי
data_manager = SumaDataManager() 