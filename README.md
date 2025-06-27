# SUMA GUI

**Signal Utility MRI Analysis - Graphical User Interface**

A modern, professional desktop GUI application for analyzing MRI and CT scans according to the SUMA 3 Software Requirements Specification.

## Overview

SUMA GUI provides an intuitive interface for clinical researchers to:
- Start new MRI/CT analysis workflows
- View and manage analysis results
- Visualize medical imaging data with 3D support
- Export analysis reports

## Features

- **Modern Material Design UI** - Professional, clean interface
- **Startup Screen** - Welcome screen with clear action options
- **Analysis Workflow** - Guided process for new analysis
- **Results Viewer** - Advanced visualization with Napari integration
- **Export Capabilities** - PDF report generation
- **Multiple Layer Support** - CT, MRI PRE/POST, ΔTE₀, Iron maps

## Application Flow

1. **Startup Screen**: Welcome with [Start Analysis] and [View Results] buttons
2. **Start Analysis Dialog**: Patient/Treatment input and data folder selection
3. **Progress Tracking**: Real-time analysis progress with detailed status
4. **Results Viewer**: Interactive 3D visualization with layer controls
5. **Export Options**: PDF report generation

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd suma3_project

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Requirements

- **Python 3.8+**
- **PyQt5** - GUI framework
- **Napari** (optional) - 3D visualization
- **Windows 10+** (recommended)

## Project Structure

```
suma3_project/
├── src/
│   ├── config/           # Application constants and configuration
│   ├── core/             # Central signal system
│   ├── resources/        # Color palette and style management
│   └── ui/
│       ├── components/   # Base UI components
│       ├── dialogs/      # Dialog boxes (analysis, results selection)
│       └── windows/      # Main windows (startup, results viewer)
├── main.py               # Main application entry point
├── README.md             # Project documentation
└── requirements.txt      # Dependencies
```

## Development

### UI Design

The interface follows the Software Requirements Specification (SRS) exactly:
- Startup screen with logo and action buttons
- Modal dialogs for analysis and results
- Embedded Napari viewer for 3D visualization
- Professional medical application styling

### Qt Designer Integration

Use Qt Designer for creating new UI components:
1. Create .ui files in `src/ui/ui_files/`
2. Use the UI loader utilities for integration
3. Follow the established styling system

### Color Scheme

- **Brand Blue**: #004466
- **Light Blue**: #007acc
- **White**: #FFFFFF
- **Text Primary**: #333333
- **Text Secondary**: #999999

## Usage

1. **Launch Application**: Run `python main.py`
2. **Start New Analysis**: Click "Start Analysis" and follow the workflow
3. **View Previous Results**: Click "View Results" to browse existing analyses
4. **3D Visualization**: Use the results viewer for interactive data exploration
5. **Export Reports**: Generate PDF reports from the results viewer

## Architecture

- **Modular Design**: Separate components for different UI elements
- **Signal-Slot Architecture**: PyQt5 event handling
- **Responsive Layout**: Adapts to different screen sizes
- **Theme System**: Centralized styling and color management

## Contributing

1. Follow the established code structure
2. Use the provided styling system
3. Test UI responsiveness
4. Maintain SRS compliance

## License

© 2025 New Phase Ltd. - For internal research use only.

---

**Note**: This is a GUI-only implementation. For full analysis capabilities, integrate with the SUMA 3 backend analysis engine.




---

## Software Requirements Specification Summary

**SUMA 3** is a desktop software tool for analyzing MRI and CT scans of clinical trial patients. It automatically computes TE₀, iron accumulation, and their changes over time, using multi-echo MRI data. The results are spatially aligned and overlaid on CT images for clear anatomical visualization and export.

### Clinical Workflow

Each treatment involves analysis of:
- **MRI PRE-treatment** (baseline, T2* multi-echo)
- **MRI POST-treatment** (follow-up, same sequence) 
- **CT** (anatomical reference)

The system calculates and compares:
- **TE₀** (T2* fit)
- **R²** (fit quality)
- **Iron accumulation** (1 / TE₀)
- **ΔTE₀ and ΔIron** (POST − PRE)

The main result is a **ΔTE₀ map overlaid on the CT scan** to visualize localized tissue changes after treatment.

### Analysis Pipeline

1. **DICOM Parsing** - Reads EchoTime and SliceLocation, groups by Z and TE
2. **TE₀ Calculation** - First 4 TE ≥ 1.0 ms → fit S(TE) = S₀ · exp(−TE / TE₀)  
3. **Image Alignment** - PRE→POST (rigid/affine), MRI→CT
4. **ΔTE₀ and ΔIron** - Calculates relative and absolute changes
5. **Report Generation** - PDF with CT overlay and ΔTE₀ maps

### System Requirements

- **OS**: Windows 10+
- **RAM**: Min 4 GB (8 GB recommended)
- **GPU**: Optional (for 3D visualization)
- **Processing time**: Up to 30 minutes per case
- **Storage**: ~300 MB per case

### Data Structure

```
Patient_data/
├── 001/
│   ├── 01/
│   │   ├── raw_dicom/ (PRE/POST/CT)
│   │   ├── Mri_pre_analyzed.json
│   │   ├── Mri_post_analyzed.json
│   │   ├── Aligned_data.json
│   │   └── analyzed_maps.npz
├── Reports/
│   └── 001_01_report.pdf
```

---

**⚠️ RESEARCH USE ONLY**

SUMA 3 is for internal research use only by New Phase Ltd. No diagnosis or clinical action should be based on results.

**© 2025 New Phase Ltd. All rights reserved.** 