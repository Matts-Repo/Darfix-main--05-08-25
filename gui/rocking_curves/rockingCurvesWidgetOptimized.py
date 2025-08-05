"""
Optimized RockingCurvesWidget with background processing and proper cancellation.
"""

from __future__ import annotations

import logging
from typing import Optional, Tuple

import numpy as np
from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot import Plot2D, StackView

from .rockingCurvesWidget import RockingCurvesWidget, _get_option_label, MAPS_CB_OPTIONS_1D, MAPS_CB_OPTIONS_2D
from ...core.rocking_curves_optimized import (
    BatchedCurveFitter, 
    fit_data_optimized,
    compute_residuals_optimized,
    select_optimal_fit_method
)
from ...core.rocking_curves import Maps_1D, Maps_2D, generate_rocking_curves_nxdict
from ... import dtypes

_logger = logging.getLogger(__name__)


class FittingThread(qt.QThread):
    """Background thread for curve fitting with progress updates."""
    
    # Signals
    progressUpdate = qt.Signal(int, int)  # current, total
    finished = qt.Signal(np.ndarray, np.ndarray)  # curves, maps
    error = qt.Signal(str)
    
    def __init__(self, dataset: dtypes.ImageDataset, indices: Optional[np.ndarray] = None,
                 int_thresh: float = 15, method: Optional[str] = None, parent=None):
        super().__init__(parent)
        self.dataset = dataset
        self.indices = indices
        self.int_thresh = int_thresh
        self.method = method
        self._fitter = None
        self._cancelled = False
        
    def run(self):
        """Execute fitting in background thread."""
        try:
            data = self.dataset.get_data(self.indices)
            
            # Auto-select method if not specified
            if self.method is None or self.method == 'auto':
                self.method = select_optimal_fit_method(data)
                _logger.info(f"Auto-selected fitting method: {self.method}")
            
            # Prepare values for fitting
            if self.dataset.dims.ndim == 1:
                dim = self.dataset.dims.get(0)
                values = np.array(self.dataset.get_metadata_values(key=dim.name, indices=self.indices))
            else:
                values = None
                
            # Create fitter with cancellation support
            self._fitter = BatchedCurveFitter(
                data,
                values=values,
                int_thresh=self.int_thresh,
                method=self.method
            )
            
            # Perform fitting with progress callback
            curves, maps = self._fitter.fit(progress_callback=self._progress_callback)
            
            if not self._cancelled:
                self.finished.emit(curves, maps)
                
        except InterruptedError:
            _logger.info("Fitting cancelled by user")
        except Exception as e:
            _logger.error(f"Error during fitting: {e}")
            self.error.emit(str(e))
            
    def cancel(self):
        """Cancel the fitting operation."""
        self._cancelled = True
        if self._fitter:
            self._fitter.cancel()
            
    def _progress_callback(self, current: int, total: int):
        """Emit progress updates."""
        if not self._cancelled:
            self.progressUpdate.emit(current, total)


class RockingCurvesWidgetOptimized(RockingCurvesWidget):
    """
    Optimized widget with background processing and improved performance.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Add progress bar
        self._progressBar = qt.QProgressBar()
        self._progressBar.hide()
        
        # Add auto-method checkbox
        self._autoMethodCheckbox = qt.QCheckBox("Auto-select method")
        self._autoMethodCheckbox.setChecked(True)
        self._autoMethodCheckbox.stateChanged.connect(self._onAutoMethodChanged)
        
        # Add downsampling control for plotting
        self._downsampleCheckbox = qt.QCheckBox("Downsample large plots")
        self._downsampleCheckbox.setChecked(True)
        self._downsampleSpinBox = qt.QSpinBox()
        self._downsampleSpinBox.setRange(100, 10000)
        self._downsampleSpinBox.setValue(1000)
        self._downsampleSpinBox.setSuffix(" points")
        
        # Update layout
        layout = self.centralWidget().layout()
        layout.addWidget(self._autoMethodCheckbox, 3, 5, 1, 1)
        layout.addWidget(self._progressBar, 7, 0, 1, 5)
        layout.addWidget(self._downsampleCheckbox, 8, 0, 1, 2)
        layout.addWidget(self._downsampleSpinBox, 8, 2, 1, 1)
        
        # Threading
        self._fitting_thread = None
        
        # Enable abort button
        self._abortFit.clicked.disconnect()
        self._abortFit.clicked.connect(self._onAbortClicked)
        
    def _onAutoMethodChanged(self, state):
        """Handle auto-method checkbox state change."""
        self._fitMethodCB.setEnabled(state != qt.Qt.Checked)
        
    def _launchFit(self):
        """Launch fitting in background thread."""
        if self.dataset is None:
            qt.QMessageBox.warning(self, "Warning", "No dataset loaded")
            return
            
        # Update UI
        self._computeFit.hide()
        self._abortFit.show()
        self._progressBar.show()
        self._progressBar.setValue(0)
        
        # Get parameters
        int_thresh = float(self._intensityThresholdLE.text())
        method = None if self._autoMethodCheckbox.isChecked() else self._fitMethodCB.currentText()
        
        # Create and start thread
        self._fitting_thread = FittingThread(
            self.dataset,
            self.indices,
            int_thresh,
            method,
            parent=self
        )
        
        # Connect signals
        self._fitting_thread.progressUpdate.connect(self._onProgressUpdate)
        self._fitting_thread.finished.connect(self._onFittingFinished)
        self._fitting_thread.error.connect(self._onFittingError)
        
        # Start fitting
        self._fitting_thread.start()
        self.sigFitClicked.emit()
        
    def _onAbortClicked(self):
        """Handle abort button click."""
        if self._fitting_thread and self._fitting_thread.isRunning():
            self._fitting_thread.cancel()
            self._fitting_thread.wait()  # Wait for thread to finish
            
        self._onFittingComplete()
        
    def _onProgressUpdate(self, current: int, total: int):
        """Update progress bar."""
        progress = int((current / total) * 100)
        self._progressBar.setValue(progress)
        
    def _onFittingFinished(self, curves: np.ndarray, maps: np.ndarray):
        """Handle successful fitting completion."""
        # Update dataset with results
        self.dataset.set_data(curves)
        self.updateDataset(self.dataset, maps)
        
        self._onFittingComplete()
        
    def _onFittingError(self, error_msg: str):
        """Handle fitting error."""
        qt.QMessageBox.critical(self, "Fitting Error", f"An error occurred during fitting:\n{error_msg}")
        self._onFittingComplete()
        
    def _onFittingComplete(self):
        """Reset UI after fitting completes."""
        self._abortFit.hide()
        self._computeFit.show()
        self._progressBar.hide()
        self.onFitFinished()
        
    def compute_residuals_optimized(self) -> Optional[np.ndarray]:
        """Use optimized residuals calculation."""
        if self.dataset is None or self._update_dataset is None:
            return None
            
        if self._residuals_cache is not None:
            return self._residuals_cache
            
        self._residuals_cache = compute_residuals_optimized(
            self._update_dataset, 
            self.dataset, 
            self.indices
        )
        return self._residuals_cache
        
    def _plotRockingCurves(self, px: float, py: float):
        """Plot rocking curves with optional downsampling."""
        # Call parent implementation
        super()._plotRockingCurves(px, py)
        
        # Apply downsampling if enabled and needed
        if self._downsampleCheckbox.isChecked():
            max_points = self._downsampleSpinBox.value()
            
            # Check all curves in the plot
            for curve in self._plot.getAllCurves():
                x_data = curve.getXData()
                if len(x_data) > max_points:
                    # Downsample
                    y_data = curve.getYData()
                    indices = np.linspace(0, len(x_data) - 1, max_points, dtype=int)
                    
                    self._plot.addCurve(
                        x_data[indices],
                        y_data[indices],
                        legend=curve.getName(),
                        color=curve.getColor(),
                        linestyle=curve.getLineStyle(),
                        symbol=curve.getSymbol()
                    )
                    
    def exportMaps(self):
        """Export maps with optimized nexus generation."""
        if self.dataset is None or self.maps is None:
            qt.QMessageBox.warning(self, "Warning", "No fitting results to export")
            return
            
        fileDialog = qt.QFileDialog()
        fileDialog.setFileMode(fileDialog.AnyFile)
        fileDialog.setAcceptMode(fileDialog.AcceptSave)
        fileDialog.setOption(fileDialog.DontUseNativeDialog)
        fileDialog.setDefaultSuffix(".h5")
        
        if fileDialog.exec():
            try:
                # Use optimized residuals calculation
                residuals = self.compute_residuals_optimized()
                
                # Generate nexus dict
                nxdict = generate_rocking_curves_nxdict(
                    dataset=self.dataset,
                    maps=self.maps,
                    residuals=residuals
                )
                
                # Save to file
                from silx.io.dictdump import dicttonx
                dicttonx(nxdict, fileDialog.selectedFiles()[0])
                
                qt.QMessageBox.information(self, "Success", "Maps exported successfully")
                
            except Exception as e:
                qt.QMessageBox.critical(self, "Export Error", f"Failed to export maps:\n{str(e)}")


def create_optimized_widget(parent=None) -> RockingCurvesWidgetOptimized:
    """Factory function to create optimized widget."""
    return RockingCurvesWidgetOptimized(parent)