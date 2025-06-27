"""
Unit tests for Patient entity
FDA Class II Medical Device Software - SUMA3
Test Driven Development approach
"""

import pytest
from datetime import datetime, date
from src.core.entities.patient import Patient, PatientValidationError


class TestPatientCreation:
    """Test patient object creation and validation"""
    
    def test_create_valid_patient(self):
        """Test creating a patient with valid data"""
        patient = Patient(
            patient_id="SUMA_001",
            age=45,
            gender="M",
            study_date=date.today()
        )
        
        assert patient.patient_id == "SUMA_001"
        assert patient.age == 45
        assert patient.gender == "M"
        assert patient.study_date == date.today()
        assert patient.created_at is not None
        
    def test_patient_id_anonymization(self):
        """Test that patient ID is properly anonymized"""
        patient = Patient(
            patient_id="SUMA_001",
            age=45,
            gender="M"
        )
        
        # Patient ID should not contain personal information
        assert patient.patient_id.startswith("SUMA_")
        assert len(patient.patient_id) >= 8
        
    def test_invalid_age_raises_error(self):
        """Test that invalid age raises validation error"""
        with pytest.raises(PatientValidationError):
            Patient(
                patient_id="SUMA_001",
                age=-5,  # Invalid age
                gender="M"
            )
            
        with pytest.raises(PatientValidationError):
            Patient(
                patient_id="SUMA_001", 
                age=150,  # Invalid age
                gender="M"
            )
            
    def test_invalid_gender_raises_error(self):
        """Test that invalid gender raises validation error"""
        with pytest.raises(PatientValidationError):
            Patient(
                patient_id="SUMA_001",
                age=45,
                gender="X"  # Invalid gender
            )
            
    def test_empty_patient_id_raises_error(self):
        """Test that empty patient ID raises validation error"""
        with pytest.raises(PatientValidationError):
            Patient(
                patient_id="",  # Empty ID
                age=45,
                gender="M"
            )


class TestPatientMethods:
    """Test patient methods and properties"""
    
    def test_patient_string_representation(self):
        """Test patient string representation"""
        patient = Patient(
            patient_id="SUMA_001",
            age=45,
            gender="M"
        )
        
        str_repr = str(patient)
        assert "SUMA_001" in str_repr
        assert "45" in str_repr
        assert "M" in str_repr
        
    def test_patient_equality(self):
        """Test patient equality comparison"""
        patient1 = Patient(
            patient_id="SUMA_001",
            age=45,
            gender="M"
        )
        
        patient2 = Patient(
            patient_id="SUMA_001",
            age=45,
            gender="M"
        )
        
        # Same patient ID should be equal
        assert patient1 == patient2
        
    def test_patient_to_dict(self):
        """Test converting patient to dictionary"""
        patient = Patient(
            patient_id="SUMA_001",
            age=45,
            gender="M",
            clinical_indication="Iron overload assessment"
        )
        
        patient_dict = patient.to_dict()
        
        assert patient_dict["patient_id"] == "SUMA_001"
        assert patient_dict["age"] == 45
        assert patient_dict["gender"] == "M"
        assert patient_dict["clinical_indication"] == "Iron overload assessment"
        assert "created_at" in patient_dict
