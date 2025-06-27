# Software Requirements Specification (SRS) - FINAL
## SUMA3 - Treatment Response Assessment System

---

**Document Information:**
- **Product Name:** SUMA3 - Treatment Response Assessment with Multi-Modal Imaging
- **Clinical Application:** PRE/POST treatment analysis with CT reference
- **Version:** 2.0 (Finalized Clinical Workflow)
- **FDA Device Class:** Class II Medical Device Software

---

## 1. Clinical Use Case - CLARIFIED

### 1.1 Primary Clinical Workflow
**For each patient treatment, the system SHALL analyze THREE imaging studies:**

1. **PRE Treatment MRI:**
   - MRI scan before treatment initiation
   - T2* multi-echo sequences for baseline iron assessment
   - Baseline tissue characterization

2. **POST Treatment MRI:** 
   - MRI scan after treatment completion
   - T2* multi-echo sequences for follow-up iron assessment
   - Treatment response evaluation

3. **CT Reference:**
   - CT scan (can be acquired at any timepoint)
   - Anatomical reference for spatial localization
   - Structural context for MRI findings

### 1.2 Analysis Objectives
- **Quantify treatment response** through PRE vs POST T2* changes
- **Calculate Delta T2*** (POST - PRE) maps
- **Overlay results on CT anatomy** for clinical interpretation
- **Generate comprehensive treatment assessment report**

---

## 2. Data Structure Requirements

### 2.1 Patient Study Organization
`
Patient_ID/
 Treatment_Session_001/
    PRE/
       T2_STAR_MULTI_ECHO/
          TE_2.5ms.dcm
          TE_5.0ms.dcm
          ...
          TE_25.0ms.dcm
    POST/
       T2_STAR_MULTI_ECHO/
          TE_2.5ms.dcm
          TE_5.0ms.dcm
          ...
          TE_25.0ms.dcm
    CT/
        CT_SERIES/
           slice_001.dcm
           slice_002.dcm
           ...
           slice_N.dcm
`

### 2.2 Study Matching Requirements
- **Patient ID matching** across all three studies
- **Anatomical region consistency** (same body region)
- **Temporal relationship tracking** (PRE  Treatment  POST)

---

## 3. Functional Requirements - UPDATED

### 3.1 Data Loading Requirements

#### REQ-F-001: PRE Treatment Data Loading
**Requirement:** The system SHALL load PRE treatment MRI T2* data.
- **Format:** DICOM multi-echo T2* sequence
- **Validation:** Verify baseline acquisition parameters
- **Quality Control:** SNR and artifact assessment
- **Priority:** Critical

#### REQ-F-002: POST Treatment Data Loading  
**Requirement:** The system SHALL load POST treatment MRI T2* data.
- **Format:** DICOM multi-echo T2* sequence
- **Validation:** Match PRE acquisition parameters
- **Quality Control:** Consistency with PRE scan
- **Priority:** Critical

#### REQ-F-003: CT Reference Data Loading
**Requirement:** The system SHALL load CT reference data.
- **Format:** DICOM CT series
- **Purpose:** Anatomical reference and overlay
- **Registration:** Prepare for MRI-CT alignment
- **Priority:** High

#### REQ-F-004: Study Association
**Requirement:** The system SHALL associate PRE/POST/CT studies for each patient.
- **Matching:** Automatic patient ID linking
- **Verification:** User confirmation of study matching
- **Workflow:** Guide user through study selection
- **Priority:** Critical

### 3.2 Analysis Pipeline

#### REQ-F-005: PRE Treatment Analysis
**Requirement:** The system SHALL calculate T2* maps from PRE treatment data.
- **Algorithm:** Mono-exponential fitting per voxel
- **Output:** Baseline T2* map (ms)
- **Quality:** R goodness of fit maps
- **Priority:** Critical

#### REQ-F-006: POST Treatment Analysis
**Requirement:** The system SHALL calculate T2* maps from POST treatment data.
- **Algorithm:** Identical to PRE analysis
- **Output:** Follow-up T2* map (ms)  
- **Consistency:** Same fitting parameters as PRE
- **Priority:** Critical

#### REQ-F-007: Treatment Response Calculation
**Requirement:** The system SHALL calculate treatment response metrics.
- **Delta T2*:** POST T2* - PRE T2* (voxel-wise)
- **Percent Change:** ((POST-PRE)/PRE) × 100%
- **Statistical Maps:** Significance testing
- **Priority:** Critical

#### REQ-F-008: Multi-Modal Registration
**Requirement:** The system SHALL register all three studies.
- **PRE-POST Registration:** Align MRI timepoints
- **MRI-CT Registration:** Align functional and anatomical
- **Quality Metrics:** Registration accuracy assessment
- **Priority:** High

### 3.3 Clinical Analysis Tools

#### REQ-F-009: ROI-Based Analysis
**Requirement:** The system SHALL support region-of-interest analysis.
- **ROI Definition:** On any of the three study types
- **Propagation:** ROI transfer between registered studies
- **Statistics:** Mean, SD, histogram for each ROI
- **Comparison:** PRE vs POST ROI statistics
- **Priority:** High

#### REQ-F-010: Treatment Response Quantification
**Requirement:** The system SHALL quantify treatment response.
- **Metrics:**
  - Mean Delta T2* in ROIs
  - Voxel-wise response maps
  - Response heterogeneity measures
  - Statistical significance maps
- **Thresholds:** Clinical significance criteria
- **Priority:** High

### 3.4 Visualization and Reporting

#### REQ-F-011: Multi-Study Viewer
**Requirement:** The system SHALL display all three studies simultaneously.
- **Layout:** PRE | POST | CT in synchronized viewers
- **Overlays:** T2* maps, Delta maps on CT anatomy
- **Navigation:** Linked slice scrolling
- **Priority:** Critical

#### REQ-F-012: Treatment Response Report
**Requirement:** The system SHALL generate treatment response reports.
- **Content:**
  - PRE/POST T2* comparison
  - Delta T2* maps overlaid on CT
  - ROI-based quantitative analysis
  - Statistical assessment of response
- **Format:** PDF with embedded images and tables
- **Priority:** High

---

## 4. Clinical Workflow - DETAILED

### 4.1 Study Loading Workflow
1. **Select Patient**  Choose patient ID
2. **Load PRE Study**  Select baseline MRI T2*
3. **Load POST Study**  Select follow-up MRI T2*  
4. **Load CT Study**  Select reference CT
5. **Verify Matching**  Confirm studies belong to same patient

### 4.2 Analysis Workflow
1. **Quality Control**  Review all three datasets
2. **Registration**  Align PRE-POST, then MRI-CT
3. **T2* Calculation**  Process PRE and POST separately
4. **Response Analysis**  Calculate Delta T2* maps
5. **ROI Analysis**  Define regions and extract statistics

### 4.3 Reporting Workflow  
1. **Review Results**  Examine Delta T2* maps
2. **Clinical Assessment**  Interpret treatment response
3. **Generate Report**  Create comprehensive PDF
4. **Export Data**  Save quantitative results

---

## 5. User Interface Requirements

### 5.1 Study Selection Interface
- **Patient Browser**  List available patients
- **Study Browser**  Show available studies per patient
- **Study Type Identification**  Clear PRE/POST/CT labeling
- **Drag-and-Drop**  Easy study assignment

### 5.2 Analysis Interface
- **Triple Viewer**  PRE | POST | CT synchronized display
- **Overlay Controls**  Show/hide T2* and Delta maps
- **ROI Tools**  Draw and edit regions of interest
- **Analysis Dashboard**  Real-time statistics display

### 5.3 Results Interface
- **Response Maps**  Interactive Delta T2* visualization
- **Quantitative Results**  Tables and plots
- **Comparison Tools**  Before/after sliders
- **Export Options**  Save results and reports

---

## 6. Technical Specifications

### 6.1 Data Processing Requirements
- **MRI Processing:** Handle 6-20 echo T2* sequences
- **CT Processing:** Process 200-500 slice CT series
- **Registration:** Sub-voxel accuracy for PRE-POST alignment
- **Memory Management:** Handle 3 concurrent large datasets

### 6.2 Performance Requirements
- **Loading Time:** <30 seconds for all three studies
- **T2* Calculation:** <2 minutes per MRI study
- **Registration:** <5 minutes for all alignments
- **Report Generation:** <1 minute for complete report

---

**זה יותר מדויק לצרכים שלך?**

המסמך המעודכן מתמקד בדיוק במה שביקשת:
- **שלושה קבצים לכל טיפול:** PRE/POST/CT
- **Workflow קליני ברור** 
- **Treatment response analysis**
- **Delta T2* calculation**
- **CT overlay for anatomical context**

**האם זה מתאים למה שחשבת?** 
