# Implementation Guide: Creating a New Widget in Darfix

This document explains the steps and requirements for implementing a new Orange widget in the Darfix codebase, using the Noise Removal and Curve Fitting widgets as reference. It is intended for an AI developer (Claude) to follow for consistent integration.

---

## 1. Widget Architecture Overview

Darfix widgets are typically built for the Orange data analysis platform. Each widget consists of:
- A GUI class (usually in `gui/<widget_name>/<WidgetName>Widget.py`)
- Core processing logic (in `core/<functionality>.py`)
- Supporting modules (e.g., utility functions, enums, configuration)
- Registration and metadata (for Orange compatibility)

### Example: Noise Removal Widget
- **GUI:** `gui/noise_removal/noiseRemovalWidget.py`
- **Core Logic:** `core/noiseremoval.py`
- **Supporting:** `core/dataset.py`, `core/utils.py`, etc.

### Example: Curve Fitting Widget
- **GUI:** `gui/rocking_curves/rockingCurvesWidget.py`
- **Core Logic:** `core/rocking_curves.py`
- **Supporting:** `core/dataset.py`, `core/utils.py`, etc.

---

## 2. File Structure and Interactions

### Required Files for a New Widget

1. **GUI File**
   - Location: `gui/<widget_name>/<WidgetName>Widget.py`
   - Contains: Orange widget class, input/output signals, UI elements, event handlers.

2. **Core Logic File**
   - Location: `core/<functionality>.py`
   - Contains: Processing functions, algorithms, data manipulation routines.

3. **Supporting Modules**
   - Commonly used: `core/dataset.py`, `core/utils.py`, `core/enums.py`
   - Purpose: Data loading, saving, utility functions, configuration.

4. **Widget Registration**
   - Location: `gui/widgets.json` or similar
   - Purpose: Register the widget with Orange, provide metadata (name, category, icon).

---

## 3. Implementation Steps

### Step 1: Define Widget Functionality
- Specify the purpose and expected inputs/outputs.
- Example: "Resource Assessment Widget" scans system resources and suggests optimal processing mode.

### Step 2: Create Core Logic
- Implement main algorithms in `core/<functionality>.py`.
- Ensure functions are modular and testable.
- Example: For resource assessment, use `psutil` for CPU/RAM, `cupy`/`torch` for GPU detection.

### Step 3: Develop GUI Class
- Create `gui/<widget_name>/<WidgetName>Widget.py`.
- Inherit from Orange widget base class.
- Define input/output signals, settings, and UI layout.
- Connect UI actions to core logic functions.

### Step 4: Integrate Supporting Modules
- Use or extend existing modules for data handling.
- Import necessary enums, utility functions, and dataset classes.

### Step 5: Register the Widget
- Add entry to widget registry (e.g., `widgets.json`).
- Provide metadata: name, description, category, icon path.

### Step 6: Testing and Validation
- Write unit tests for core logic.
- Test GUI interactions and Orange integration.
- Validate with sample datasets.

---

## 4. Example Mapping: Curve Fitting Widget

- **gui/rocking_curves/rockingCurvesWidget.py**
  - Handles UI, user input, progress bar, abort button.
  - Calls functions from `core/rocking_curves.py`.

- **core/rocking_curves.py**
  - Implements curve fitting algorithms, multiprocessing logic.
  - Uses NumPy, SciPy, and possibly GPU libraries.

- **core/dataset.py**
  - Loads and manages data for fitting.

- **core/utils.py**
  - Provides helper functions (e.g., chunking, progress updates).

---

## 5. Implementation Checklist

- [ ] Define widget purpose and expected workflow.
- [ ] Implement core logic in `core/<functionality>.py`.
- [ ] Create GUI class in `gui/<widget_name>/<WidgetName>Widget.py`.
- [ ] Integrate with supporting modules as needed.
- [ ] Register widget for Orange compatibility.
- [ ] Write and run unit tests.
- [ ] Document usage and configuration.

---

## 6. Additional Notes

- Follow existing code style and structure for consistency.
- Use signals/slots for UI responsiveness.
- Ensure error handling and user feedback are implemented.
- Design for extensibility (future hardware, new features).

---

## 7. References

- See `gui/noise_removal/noiseRemovalWidget.py` and `core/noiseremoval.py` for noise removal widget example.
- See `gui/rocking_curves/rockingCurvesWidget.py` and `core/rocking_curves.py` for curve fitting widget example.

---

This guide provides a clear roadmap for implementing a new widget in Darfix. For further details, refer to the referenced files and Orange