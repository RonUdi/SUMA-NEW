# Software Requirements Specification (SRS) - UPDATED
## SUMA3 - Multi-Modal Medical Imaging Analysis System

---

**Document Information:**
- **Product Name:** SUMA3 - Multi-Modal Iron Assessment System (CT + MRI)
- **Document Type:** Software Requirements Specification  
- **Version:** 1.1 (Updated for CT + MRI support)
- **Date:** 2025-06-26
- **FDA Device Class:** Class II Medical Device Software
- **Regulatory Pathway:** FDA 510(k) Premarket Notification

---

## 1. Introduction - CORRECTED

### 1.1 Purpose
This Software Requirements Specification (SRS) defines requirements for SUMA3, a medical device software for:
- **CT imaging analysis** with tissue characterization
- **MRI T2* relaxometry** for iron quantification  
- **Multi-modal registration** between CT and MRI
- **Comprehensive reporting** with combined analysis

### 1.2 Scope - UPDATED
SUMA3 is a multi-modal medical device software that:
- **CT Analysis:**
  - Processes CT DICOM images
  - Anatomical structure identification
  - Density measurements (HU values)
  - 3D volume rendering

- **MRI Analysis:**  
  - Processes multi-echo T2* MRI sequences
  - Calculates T2* relaxation time maps
  - Iron concentration quantification
  - Tissue characterization

- **Multi-Modal Integration:**
  - CT  MRI image registration
  - Combined analysis workflows
  - Overlay capabilities
  - Comparative reporting

### 1.3 Intended Use - REVISED
**Intended Use Statement:**
SUMA3 is intended for use by qualified healthcare professionals to assist in:
1. **CT-based tissue analysis** for anatomical assessment
2. **MRI T2* relaxometry analysis** for tissue iron quantification  
3. **Multi-modal image registration** for comprehensive evaluation
4. **Combined CT-MRI reporting** for clinical decision support

---

## 2. System Overview - UPDATED

### 2.1 Imaging Modalities Support
- **CT Imaging:**
  - Single and multi-phase CT
  - Contrast-enhanced CT
  - High-resolution CT protocols
  - Hounsfield unit analysis

- **MRI Imaging:**
  - T2* multi-echo sequences
  - Single-echo T2* (if available)
  - Other MRI sequences (T1, T2, FLAIR)
  - Quantitative mapping

### 2.2 Input Data Requirements
- **CT DICOM Format:**
  - Axial, coronal, sagittal reconstructions
  - Slice thickness: 0.5-5.0mm
  - Matrix size: 512x512 minimum
  - Pixel spacing: 0.5-2.0mm

- **MRI DICOM Format:**
  - T2* multi-echo (minimum 6 echoes)
  - Echo times: 2-50ms range
  - Matrix size: 256x256 minimum  
  - Slice thickness: 2-8mm

---

## 3. Functional Requirements - UPDATED

### 3.1 CT Data Processing

#### REQ-F-001: CT DICOM Loading
**Requirement:** The system SHALL load CT DICOM files and series.
- **Support:** Single/multi-phase CT studies
- **Validation:** DICOM conformance checking
- **Priority:** Critical

#### REQ-F-002: CT Image Processing
**Requirement:** The system SHALL provide CT image processing tools.
- **Features:** 
  - Window/level adjustment
  - Multiplanar reconstruction (MPR)
  - 3D volume rendering
  - Density measurements (HU)
- **Priority:** High

#### REQ-F-003: CT ROI Analysis
**Requirement:** The system SHALL support CT region-of-interest analysis.
- **Measurements:** Mean HU, standard deviation, volume
- **ROI Types:** 2D/3D regions
- **Statistics:** Histogram analysis
- **Priority:** High

### 3.2 MRI Data Processing

#### REQ-F-004: MRI DICOM Loading  
**Requirement:** The system SHALL load MRI DICOM files with T2* sequences.
- **Multi-echo:** Support 6-20 echo times
- **Validation:** T2* sequence parameter checking
- **Priority:** Critical

#### REQ-F-005: T2* Relaxometry Calculation
**Requirement:** The system SHALL calculate T2* maps from multi-echo data.
- **Algorithm:** Mono-exponential fitting: S(TE) = S0 * exp(-TE/T2*)
- **Accuracy:** 5% vs reference standard
- **Output:** T2* maps in milliseconds
- **Priority:** Critical

#### REQ-F-006: Iron Quantification
**Requirement:** The system SHALL convert T2* to iron concentration.
- **Calibration:** Validated conversion factors
- **Units:** mg Fe/g tissue or mg Fe/mL
- **Uncertainty:** Confidence intervals
- **Priority:** High

### 3.3 Multi-Modal Registration

#### REQ-F-007: CT-MRI Registration
**Requirement:** The system SHALL perform automatic CT-MRI registration.
- **Methods:** Rigid, affine, deformable
- **Accuracy:** Target Registration Error <3mm
- **Validation:** Visual and quantitative assessment
- **Priority:** Critical

#### REQ-F-008: Registration Quality Control
**Requirement:** The system SHALL provide registration quality metrics.
- **Metrics:** Mutual information, normalized cross-correlation
- **Visualization:** Checkerboard, difference images
- **Manual Adjustment:** Fine-tuning capability
- **Priority:** High

### 3.4 Multi-Modal Analysis

#### REQ-F-009: Combined Analysis Workflow
**Requirement:** The system SHALL integrate CT and MRI analysis.
- **Workflow:** CT loading  MRI loading  Registration  Analysis
- **Synchronization:** Linked viewing and navigation
- **Overlay:** T2* maps on CT anatomy
- **Priority:** High

#### REQ-F-010: Comparative Analysis
**Requirement:** The system SHALL support comparative analysis tools.
- **Pre/Post Studies:** Temporal comparison
- **Multi-Modal:** CT vs MRI comparison
- **Quantitative:** Statistical comparisons
- **Priority:** High

### 3.5 Data Management

#### REQ-F-011: Multi-Modal Data Organization
**Requirement:** The system SHALL organize multi-modal studies.
- **Structure:** Patient  Study  Series (CT/MRI)
- **Linking:** Automatic study association
- **Storage:** Efficient data management
- **Priority:** High

#### REQ-F-012: Data Export
**Requirement:** The system SHALL export multi-modal results.
- **Formats:** DICOM, NIfTI, CSV, PDF
- **Content:** CT measurements, T2* maps, iron maps
- **Anonymization:** Patient de-identification
- **Priority:** Medium

---

## 4. Clinical Workflow - NEW SECTION

### 4.1 Typical Clinical Workflow
1. **Data Import:**
   - Load CT study
   - Load corresponding MRI study
   - Verify patient matching

2. **Image Registration:**
   - Automatic CT-MRI alignment
   - Quality assessment
   - Manual refinement if needed

3. **Analysis:**
   - CT: Anatomical assessment, HU measurements
   - MRI: T2* calculation, iron quantification
   - Combined: Overlay analysis

4. **Reporting:**
   - Multi-modal report generation
   - Clinical findings summary
   - Quantitative measurements

### 4.2 User Interface Requirements

#### REQ-UI-001: Multi-Modal Viewer
**Requirement:** The system SHALL provide synchronized multi-modal viewing.
- **Layout:** Side-by-side CT and MRI display
- **Synchronization:** Linked slice navigation
- **Overlay:** T2*/iron maps on CT
- **Priority:** Critical

#### REQ-UI-002: Analysis Tools Integration
**Requirement:** The system SHALL integrate CT and MRI analysis tools.
- **ROI Tools:** Consistent across modalities
- **Measurements:** Unified measurement display
- **Workflow:** Seamless modality switching
- **Priority:** High

---

## 5. Technical Specifications - UPDATED

### 5.1 Supported File Formats
- **CT:** DICOM 3.0, enhanced DICOM
- **MRI:** DICOM 3.0, enhanced DICOM with T2* extensions
- **Export:** NIfTI, DICOM-SR, PDF, CSV, Excel

### 5.2 Performance Requirements
- **CT Processing:** <30 seconds for 500 slice CT
- **MRI T2* Calculation:** <2 minutes for multi-echo
- **Registration:** <5 minutes for CT-MRI alignment
- **Memory Usage:** <8GB for typical datasets

### 5.3 Validation Requirements
- **CT Accuracy:** HU measurement accuracy 5 HU
- **MRI Accuracy:** T2* measurement accuracy 5%
- **Registration:** Spatial accuracy <3mm TRE
- **Clinical Validation:** Multi-site validation study

---

**הערות חשובות:**
1. **CT + MRI:** המערכת תתמוך בשני סוגי הדמיה
2. **Registration:** יישור אוטומטי בין CT ל-MRI
3. **Iron Assessment:** כמת ברזל מMRI על רקע אנטומי של CT
4. **Clinical Workflow:** זרימת עבודה משולבת

**האם זה מה שהתכוונת? או שצריך לתקן עוד משהו?**
