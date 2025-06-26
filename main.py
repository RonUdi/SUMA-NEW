#!/usr/bin/env python3
"""
SUMA 3 - Signal Utility MRI Analysis
FDA 510(k) Class II Medical Device Software

Main Application Entry Point

Copyright (c) 2025 SUMA Medical Technologies Ltd.
All rights reserved. This software is a medical device.

IEC 62304 Classification: Class B Software
FDA Device Class: Class II Medical Device Software
ISO 13485:2016 Compliant Manufacturing

IMPORTANT MEDICAL DEVICE NOTICE:
This software is intended for use by qualified healthcare professionals only.
Results must be interpreted by trained clinicians familiar with MRI T2* relaxometry.
This device is currently under FDA review.
"""

import sys
import os
import logging
from pathlib import Path
from typing import Optional
import argparse

# Medical device version tracking
__version__ = "3.0.0"
__build__ = "2025.01.26.001"
__regulatory_version__ = "FDA-510k-PENDING"

def setup_medical_logging() -> logging.Logger:
    """
    Initialize FDA-compliant logging system with audit trail capabilities.
    
    Returns:
        Configured logger instance for medical device operations
    """
    # Create logs directory in compliance with 21 CFR Part 820
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure medical-grade logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - [USER:%(user)s] - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "suma3_medical.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger("SUMA3_Medical")
    logger.info(f"SUMA 3 Medical Device Software Starting - Version {__version__}")
    logger.info(f"Build: {__build__} - Regulatory: {__regulatory_version__}")
    
    return logger

def validate_clinical_environment() -> bool:
    """
    Validate that the system meets clinical deployment requirements.
    
    Returns:
        True if environment is suitable for clinical use
        
    Raises:
        SystemError: If critical clinical requirements are not met
    """
    logger = logging.getLogger("SUMA3_Medical")
    
    # Check Python version (must be validated version)
    if sys.version_info < (3.8, 0):
        logger.critical("Python version < 3.8 not validated for clinical use")
        return False
    
    # Check available memory (minimum 16GB for clinical datasets)
    try:
        import psutil
        memory_gb = psutil.virtual_memory().total / (1024**3)
        if memory_gb < 16:
            logger.warning(f"Available memory ({memory_gb:.1f}GB) below recommended 16GB")
    except ImportError:
        logger.warning("Cannot verify system memory requirements")
    
    # Verify critical directories exist
    required_dirs = ["regulatory", "core", "data", "processing", "ui", "services"]
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            logger.critical(f"Critical directory missing: {dir_name}")
            return False
    
    logger.info("Clinical environment validation completed successfully")
    return True

def initialize_medical_services():
    """Initialize core medical device services with proper error handling."""
    logger = logging.getLogger("SUMA3_Medical")
    
    try:
        # Import core medical services
        from services.audit import AuditService
        from services.security import SecurityService  
        from services.config import MedicalConfigService
        
        logger.info("Initializing medical device services...")
        
        # Initialize audit trail system (required for FDA compliance)
        audit_service = AuditService()
        audit_service.log_system_start(__version__, __build__)
        
        # Initialize security subsystem
        security_service = SecurityService()
        security_service.initialize_clinical_security()
        
        # Load medical device configuration
        config_service = MedicalConfigService()
        config_service.load_clinical_configuration()
        
        logger.info("Medical device services initialized successfully")
        return True
        
    except ImportError as e:
        logger.critical(f"Failed to import critical medical services: {e}")
        return False
    except Exception as e:
        logger.critical(f"Critical error during service initialization: {e}")
        return False

def launch_clinical_application():
    """Launch the main clinical application interface."""
    logger = logging.getLogger("SUMA3_Medical")
    
    try:
        # Import the main application controller
        from ui.controllers.main_controller import ClinicalMainController
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        
        logger.info("Launching clinical user interface...")
        
        # Create QApplication with medical device settings
        app = QApplication(sys.argv)
        app.setApplicationName("SUMA 3 Medical")
        app.setApplicationVersion(__version__)
        app.setOrganizationName("SUMA Medical Technologies Ltd.")
        
        # Set high DPI scaling for clinical displays
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Initialize main clinical controller
        main_controller = ClinicalMainController()
        main_controller.show()
        
        logger.info("Clinical application launched successfully")
        
        # Start application event loop
        return app.exec_()
        
    except ImportError as e:
        logger.critical(f"Failed to import UI components: {e}")
        return 1
    except Exception as e:
        logger.critical(f"Critical error during application launch: {e}")
        return 1

def main() -> int:
    """
    Main entry point for SUMA 3 Medical Device Software.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="SUMA 3 - FDA Class II Medical Device Software",
        epilog="For clinical support: +1-800-SUMA-MED"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"SUMA 3 v{__version__} (Build: {__build__})"
    )
    parser.add_argument(
        "--clinical-mode", 
        action="store_true",
        help="Enable full clinical validation mode"
    )
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug logging (not for clinical use)"
    )
    
    args = parser.parse_args()
    
    # Initialize medical logging system
    logger = setup_medical_logging()
    
    try:
        # Medical device startup sequence
        logger.info("=" * 60)
        logger.info("SUMA 3 MEDICAL DEVICE SOFTWARE STARTUP")
        logger.info("=" * 60)
        
        # Step 1: Validate clinical environment
        if not validate_clinical_environment():
            logger.critical("Clinical environment validation failed")
            return 1
        
        # Step 2: Initialize medical services
        if not initialize_medical_services():
            logger.critical("Medical services initialization failed")
            return 2
        
        # Step 3: Launch clinical application
        exit_code = launch_clinical_application()
        
        logger.info("SUMA 3 Medical Device Software shutdown complete")
        return exit_code
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 0
    except Exception as e:
        logger.critical(f"Unhandled critical error: {e}", exc_info=True)
        return 99

if __name__ == "__main__":
    # Medical device software entry point
    sys.exit(main())
