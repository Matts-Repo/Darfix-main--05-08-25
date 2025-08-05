# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Darfix is a Python application for data reduction and analysis of X-ray diffraction data. It provides both a graphical interface using Orange workflows (ewoksorange) and a Python API for processing scanning X-ray diffraction microscopy data.

## Architecture

### Core Components

1. **Data Processing Pipeline**
   - `core/dataset.py`: Main Dataset class for data management
   - `core/data.py`: Data structures and operations tracking
   - `core/dimension.py`: Handling acquisition dimensions
   - `decomposition/`: Blind source separation methods (PCA, NMF, NICA, IPCA)

2. **GUI Framework**
   - Built on Orange Canvas workflows (ewoksorange)
   - Widget-based architecture in `gui/` for different processing steps
   - Each widget corresponds to a task in `tasks/`

3. **Processing Tasks**
   - `tasks/`: Individual processing operations (ROI selection, noise removal, shift correction, etc.)
   - Each task can be used programmatically or through the GUI

## Key Commands

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_dataset.py

# Run with coverage
pytest --cov=darfix
```

### Running the Application
```bash
# Main entry point (requires ewoksorange)
python -m darfix

# Check version
python -m darfix --version
```

## Development Guidelines

### Testing Structure
- Tests are in `tests/` mirroring the source structure
- Fixtures in `tests/conftest.py` provide common test data
- Tests use pytest framework with silx resources for test data

### Data Formats
- Supports EDF (European Data Format) and HDF5 files
- Uses silx library for file I/O operations
- Metadata stored alongside detector data

### Important Dependencies
- silx: Scientific data visualization and I/O
- ewoksorange: Orange Canvas integration for workflows
- scikit-learn: Machine learning algorithms
- fabio: Image format I/O
- OpenCV: Image registration and processing

### Workflow System
- Orange workflow files (`.ows`) define processing pipelines
- Tasks can be chained together in workflows
- Workflows can be converted to ewoks graphs for execution