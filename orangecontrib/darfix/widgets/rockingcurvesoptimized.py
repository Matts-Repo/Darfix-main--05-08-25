"""
Orange widget wrapper for optimized rocking curves.
"""

from typing import Optional
from ewoksorange.bindings import ewokstaskclass
from orangewidget.settings import Setting

from darfix.gui.rocking_curves.rockingCurvesWidgetOptimized import RockingCurvesWidgetOptimized
from darfix.tasks.rocking_curves_optimized import RockingCurvesOptimized


@ewokstaskclass(
    module="darfix.tasks.rocking_curves_optimized",
    task_class=RockingCurvesOptimized,
    name="Rocking Curves (Optimized)",
    description="Analyze rocking curves with performance optimizations",
    category="Darfix Processing",
    version="1.0",
    icon="icons/curves.png",
    keywords=["rocking curve", "fit", "gaussian", "optimization", "performance"],
)
class RockingCurvesOptimizedWidgetOW:
    """
    Orange widget for optimized rocking curves analysis.
    
    This widget provides:
    - Background processing with progress updates
    - Automatic method selection
    - Batched processing for improved performance
    - Shared memory to reduce overhead
    - Functional abort button
    """
    
    # Widget settings that persist between sessions
    int_thresh = Setting(15.0)
    method = Setting("auto")
    use_optimizations = Setting(True)
    auto_method = Setting(True)
    downsample_plots = Setting(True)
    max_plot_points = Setting(1000)
    
    # Widget name
    name = "Rocking Curves (Optimized)"
    description = "Analyze rocking curves with performance optimizations"
    icon = "icons/curves.png"
    priority = 11  # Higher priority than original widget
    
    # Input/Output definitions
    inputs = [
        ("dataset", "darfix.dtypes.Dataset", "set_input_dataset"),
    ]
    outputs = [
        ("dataset", "darfix.dtypes.Dataset"),
        ("maps", "numpy.ndarray"),
    ]
    
    def __init__(self):
        super().__init__()
        self.input_dataset = None
        self._widget = None
        self._task_outputs = {}
        self._setup_gui()
        
    def _setup_gui(self):
        """Set up the GUI with the optimized widget."""
        self._widget = RockingCurvesWidgetOptimized(parent=self)
        
        # Connect widget signals
        self._widget.sigFitClicked.connect(self._on_fit_clicked)
        
        # Apply saved settings
        self._widget.setIntensityThreshold(str(self.int_thresh))
        self._widget.setFitMethod(self.method)
        self._widget._autoMethodCheckbox.setChecked(self.auto_method)
        self._widget._downsampleCheckbox.setChecked(self.downsample_plots)
        self._widget._downsampleSpinBox.setValue(self.max_plot_points)
        
        # Set as central widget
        self.controlArea = self._widget
        
    def set_input_dataset(self, dataset):
        """Handle input dataset."""
        self.input_dataset = dataset
        if dataset is not None:
            self._widget.setDataset(dataset)
            
    def _on_fit_clicked(self):
        """Handle fit button click - prepare inputs for task."""
        if self.input_dataset is None:
            return
            
        # Update settings from widget
        self.int_thresh = float(self._widget.getIntensityThreshold())
        self.method = "auto" if self._widget._autoMethodCheckbox.isChecked() else self._widget.getFitMethod()
        self.auto_method = self._widget._autoMethodCheckbox.isChecked()
        self.downsample_plots = self._widget._downsampleCheckbox.isChecked()
        self.max_plot_points = self._widget._downsampleSpinBox.value()
        
    def get_task_inputs(self):
        """Get inputs for the ewoks task."""
        return {
            "dataset": self.input_dataset,
            "int_thresh": self.int_thresh,
            "method": self.method,
            "use_optimizations": self.use_optimizations,
            "output_filename": None,  # Let user save manually from widget
        }
        
    def set_task_outputs(self, dataset=None, maps=None):
        """Handle task outputs."""
        # Store outputs for retrieval
        if dataset is not None:
            self._task_outputs["dataset"] = dataset
        if maps is not None:
            self._task_outputs["maps"] = maps
            
        if dataset is not None and maps is not None:
            # Update widget with results
            self._widget.updateDataset(dataset.dataset, maps)
            
            # Send outputs
            self.send("dataset", dataset)
            self.send("maps", maps)
    
    def setDataset(self, dataset):
        """Compatibility method for tests."""
        self.set_input_dataset(dataset)
    
    def _execute_task(self):
        """Execute the task manually (for testing)."""
        self._on_fit_clicked()
        
    def get_task_output_value(self, output_name):
        """Get task output by name (for testing)."""
        return self._task_outputs.get(output_name)
            
    @classmethod
    def get_icon(cls):
        """Return widget icon."""
        import os
        from darfix import resources
        
        icons_dir = os.path.dirname(resources.gui.icons.__file__)
        return os.path.join(icons_dir, "curves.png")