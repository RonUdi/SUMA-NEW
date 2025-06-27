"""
Patient Entity - FDA Class II Medical Device Software
SUMA3 - T2* MRI Analysis for Iron Assessment

This module implements the Patient data model with FDA compliance
including HIPAA anonymization and audit trail requirements.
"""

from datetime import datetime, date
from typing import Optional, Dict, Any
import logging


# Configure medical device logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SUMA3.Patient')


class PatientValidationError(Exception):
    """Raised when patient data validation fails"""
    pass


class Patient:
    """
    Patient entity for medical device software
    
    Implements FDA requirements for:
    - Data validation
    - HIPAA compliance 
    - Audit trail
    - Anonymization
    """
    
    def __init__(
        self,
        patient_id: str,
        age: int,
        gender: str,
        study_date: Optional[date] = None,
        clinical_indication: Optional[str] = None
    ):
        """
        Initialize Patient object with validation
        
        Args:
            patient_id: Anonymized patient identifier (required)
            age: Patient age in years (0-150)
            gender: Patient gender ("M" or "F")
            study_date: Date of study (optional, defaults to today)
            clinical_indication: Clinical reason for study (optional)
            
        Raises:
            PatientValidationError: If validation fails
        """
        # Validate inputs
        self._validate_patient_data(patient_id, age, gender)
        
        # Set immutable patient ID
        self._patient_id = patient_id
        
        # Set patient data
        self.age = age
        self.gender = gender
        self.study_date = study_date or date.today()
        self.clinical_indication = clinical_indication
        
        # Audit trail
        self.created_at = datetime.now()
        
        # Log patient creation for audit
        logger.info(f"Patient created: {patient_id}, Age: {age}, Gender: {gender}")
    
    @property
    def patient_id(self) -> str:
        """Patient ID (immutable)"""
        return self._patient_id
    
    def _validate_patient_data(self, patient_id: str, age: int, gender: str) -> None:
        """
        Validate patient data according to FDA requirements
        
        Args:
            patient_id: Patient identifier
            age: Patient age
            gender: Patient gender
            
        Raises:
            PatientValidationError: If validation fails
        """
        # Validate patient ID
        if not patient_id or not isinstance(patient_id, str):
            raise PatientValidationError("Patient ID cannot be empty")
            
        if len(patient_id) < 4:
            raise PatientValidationError("Patient ID must be at least 4 characters")
            
        # Validate age
        if not isinstance(age, int) or age < 0 or age > 150:
            raise PatientValidationError("Age must be between 0 and 150 years")
            
        # Validate gender
        if gender not in ["M", "F"]:
            raise PatientValidationError("Gender must be 'M' or 'F'")
    
    def get_anonymized_age(self) -> str:
        """
        Get anonymized age for HIPAA compliance
        
        Returns:
            Age as string, with ">89" for elderly patients
        """
        if self.age > 89:
            return ">89"
        return str(self.age)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert patient to dictionary for serialization
        
        Returns:
            Dictionary with patient data
        """
        return {
            "patient_id": self.patient_id,
            "age": self.age,
            "gender": self.gender,
            "study_date": self.study_date.isoformat() if self.study_date else None,
            "clinical_indication": self.clinical_indication,
            "created_at": self.created_at.isoformat()
        }
    
    def __str__(self) -> str:
        """String representation of patient"""
        return f"Patient(ID: {self.patient_id}, Age: {self.age}, Gender: {self.gender})"
    
    def __repr__(self) -> str:
        """Developer representation of patient"""
        return (f"Patient(patient_id='{self.patient_id}', age={self.age}, "
                f"gender='{self.gender}', study_date={self.study_date})")
    
    def __eq__(self, other) -> bool:
        """Compare patients by patient ID"""
        if not isinstance(other, Patient):
            return False
        return self.patient_id == other.patient_id
    
    def __hash__(self) -> int:
        """Hash based on patient ID for set operations"""
        return hash(self.patient_id)


# Medical device software version tracking
__version__ = "1.0.0"
__medical_device_class__ = "II"
__fda_compliance__ = "510(k)"
