"""
SUMA Core Entities
Data models for the SUMA system
"""

from .patient import Patient
from .treatment import Treatment
from .analysis_result import AnalysisResult

__all__ = ['Patient', 'Treatment', 'AnalysisResult'] 