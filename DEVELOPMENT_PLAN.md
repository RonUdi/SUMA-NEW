
##  Phase 3: User Interface (שבועות 6-8)

### 3.1 Main Application Window
- [ ] **Main Window** - src/ui/main_window.py
  - [ ] תפריט ראשי
  - [ ] navigation בין screens
  - [ ] patient selection

### 3.2 Analysis Workflow Screens
- [ ] **Data Loading Screen** - src/ui/screens/data_loading.py
  - [ ] בחירת תיקיות PRE/POST/CT
  - [ ] preview של DICOM data
- [ ] **T2* Analysis Screen** - src/ui/screens/t2_analysis.py
  - [ ] הצגת T2* maps
  - [ ] ROI selection tools
- [ ] **Registration Screen** - src/ui/screens/registration.py
  - [ ] הצגת תוצאות alignment
  - [ ] manual adjustment tools
- [ ] **Results Screen** - src/ui/screens/results.py
  - [ ] הצגת Delta T2* על CT
  - [ ] iron concentration maps
  - [ ] export options

### 3.3 Clinical Tools
- [ ] **Report Generator** - src/reporting/clinical_report.py
  - [ ] PDF reports עם תמונות
  - [ ] statistical summaries
  - [ ] FDA-compliant format

---

##  Phase 4: Medical Device Compliance (שבועות 9-11)

### 4.1 FDA Documentation
- [ ] **Software Requirements Specification**
  - [ ] Functional requirements
  - [ ] Performance requirements
  - [ ] Safety requirements
- [ ] **Risk Management (ISO 14971)**
  - [ ] risk analysis
  - [ ] mitigation strategies
  - [ ] risk-benefit analysis

### 4.2 Validation & Verification
- [ ] **Algorithm Validation** - tests/validation/
  - [ ] phantom studies
  - [ ] clinical validation
  - [ ] accuracy/precision studies
- [ ] **Software Testing** - tests/
  - [ ] unit tests (coverage >90%)
  - [ ] integration tests
  - [ ] user acceptance tests

### 4.3 Quality System
- [ ] **Audit Trails** - src/utils/audit_logger.py
  - [ ] user action logging
  - [ ] data integrity tracking
- [ ] **Version Control** - src/utils/version_manager.py
  - [ ] software version tracking
  - [ ] change control

---

##  Success Criteria & Timeline

### Technical Requirements
- [ ] Accurate T2* calculation (error <5%)
- [ ] Robust image registration (TRE <2mm)
- [ ] Fast processing (<10 min per case)
- [ ] User-friendly interface

### Timeline Summary
| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| 1 | 2 weeks | Core architecture, DICOM loading |
| 2 | 3 weeks | T2* algorithms, registration |
| 3 | 3 weeks | Complete UI, workflow |
| 4 | 3 weeks | FDA documentation, validation |

**Total: 11 weeks**

### Next Steps:
1.  Project setup complete
2.  Ready to start Phase 1
3.  Create first task: Patient data model
