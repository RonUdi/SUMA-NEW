"""
Analysis Result Entity - Data model for analysis results
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
import numpy as np

@dataclass
class AnalysisResult:
    """מודל תוצאות ניתוח"""
    patient_id: str
    treatment_id: str
    
    # תוצאות ניתוח
    te0_pre_map: Optional[np.ndarray] = None
    te0_post_map: Optional[np.ndarray] = None
    delta_te0_map: Optional[np.ndarray] = None
    iron_pre_map: Optional[np.ndarray] = None
    iron_post_map: Optional[np.ndarray] = None
    delta_iron_map: Optional[np.ndarray] = None
    r2_pre_map: Optional[np.ndarray] = None
    r2_post_map: Optional[np.ndarray] = None
    
    # נתוני CT ו-alignment
    ct_data: Optional[np.ndarray] = None
    alignment_matrix: Optional[np.ndarray] = None
    
    # מטא-דטה
    analysis_date: datetime = None
    analysis_duration: Optional[float] = None  # בשניות
    analysis_version: str = "1.0.0"
    
    # סטטיסטיקות
    stats: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.analysis_date is None:
            self.analysis_date = datetime.now()
        if self.stats is None:
            self.stats = {}
    
    @property
    def display_name(self) -> str:
        """שם להצגה"""
        return f"{self.patient_id}_{self.treatment_id}_results"
    
    @property
    def results_folder(self) -> Path:
        """תיקיית תוצאות"""
        return Path("Patient_data") / self.patient_id / self.treatment_id
    
    @property
    def is_complete(self) -> bool:
        """בדיקה האם הניתוח הושלם"""
        return bool(
            self.te0_pre_map is not None and
            self.te0_post_map is not None and
            self.delta_te0_map is not None and
            self.ct_data is not None
        )
    
    def get_summary_stats(self) -> Dict[str, float]:
        """חישוב סטטיסטיקות סיכום"""
        if not self.is_complete:
            return {}
            
        stats = {}
        
        if self.delta_te0_map is not None:
            valid_mask = ~np.isnan(self.delta_te0_map)
            if np.sum(valid_mask) > 0:
                stats['delta_te0_mean'] = float(np.mean(self.delta_te0_map[valid_mask]))
                stats['delta_te0_std'] = float(np.std(self.delta_te0_map[valid_mask]))
                stats['delta_te0_min'] = float(np.min(self.delta_te0_map[valid_mask]))
                stats['delta_te0_max'] = float(np.max(self.delta_te0_map[valid_mask]))
        
        if self.delta_iron_map is not None:
            valid_mask = ~np.isnan(self.delta_iron_map)
            if np.sum(valid_mask) > 0:
                stats['delta_iron_mean'] = float(np.mean(self.delta_iron_map[valid_mask]))
                stats['delta_iron_std'] = float(np.std(self.delta_iron_map[valid_mask]))
                
        return stats
    
    def save_to_file(self, filepath: Path) -> bool:
        """שמירת תוצאות לקובץ"""
        try:
            # נשמור כ-npz file עם כל המערכים
            data_to_save = {}
            
            if self.te0_pre_map is not None:
                data_to_save['te0_pre_map'] = self.te0_pre_map
            if self.te0_post_map is not None:
                data_to_save['te0_post_map'] = self.te0_post_map
            if self.delta_te0_map is not None:
                data_to_save['delta_te0_map'] = self.delta_te0_map
            if self.iron_pre_map is not None:
                data_to_save['iron_pre_map'] = self.iron_pre_map
            if self.iron_post_map is not None:
                data_to_save['iron_post_map'] = self.iron_post_map
            if self.delta_iron_map is not None:
                data_to_save['delta_iron_map'] = self.delta_iron_map
            if self.ct_data is not None:
                data_to_save['ct_data'] = self.ct_data
            if self.alignment_matrix is not None:
                data_to_save['alignment_matrix'] = self.alignment_matrix
                
            np.savez_compressed(filepath, **data_to_save)
            return True
            
        except Exception as e:
            print(f"Error saving analysis results: {e}")
            return False
    
    @classmethod
    def load_from_file(cls, filepath: Path, patient_id: str, treatment_id: str):
        """טעינת תוצאות מקובץ"""
        try:
            data = np.load(filepath)
            
            result = cls(patient_id=patient_id, treatment_id=treatment_id)
            
            result.te0_pre_map = data.get('te0_pre_map', None)
            result.te0_post_map = data.get('te0_post_map', None)
            result.delta_te0_map = data.get('delta_te0_map', None)
            result.iron_pre_map = data.get('iron_pre_map', None)
            result.iron_post_map = data.get('iron_post_map', None)
            result.delta_iron_map = data.get('delta_iron_map', None)
            result.ct_data = data.get('ct_data', None)
            result.alignment_matrix = data.get('alignment_matrix', None)
            
            return result
            
        except Exception as e:
            print(f"Error loading analysis results: {e}")
            return None 