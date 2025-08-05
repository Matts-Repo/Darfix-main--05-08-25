"""
Orange widget wrapper for standard rocking curves.
"""

from ewoksorange.bindings import ewokstaskclass
from orangewidget.settings import Setting

from darfix.gui.rocking_curves.rockingCurvesWidget import RockingCurvesWidget
from darfix.tasks.rocking_curves import RockingCurves


@ewokstaskclass(
    module="darfix.tasks.rocking_curves",
    task_class=RockingCurves,
    name="Rocking Curves",
    description="Analyze rocking curves by fitting to peak shapes",
    category="Darfix Processing",
    version="1.0",
    icon="icons/curves.png",
    keywords=["rocking curve", "fit", "gaussian"],
)
class RockingCurvesWidgetOW:
    """
    Orange widget for rocking curves analysis.
    
    Analyzes the rocking curve of each pixel by fitting to a peak shape (e.g., Gaussian).
    """
    
    # Widget settings
    int_thresh = Setting(15.0)
    method = Setting("trf")
    
    # Widget metadata
    name = "Rocking Curves"
    description = "Analyze rocking curves by fitting to peak shapes"
    icon = "icons/curves.png"
    priority = 10
    
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
        """Set up the GUI with the standard widget."""
        self._widget = RockingCurvesWidget(parent=self)
        
        # Connect widget signals
        self._widget.sigFitClicked.connect(self._on_fit_clicked)
        
        # Apply saved settings
        self._widget.setIntensityThreshold(str(self.int_thresh))
        self._widget.setFitMethod(self.method)
        
        # Set as central widget
        self.controlArea = self._widget
        
    def set_input_dataset(self, dataset):
        """Handle input dataset."""
        self.input_dataset = dataset
        if dataset is not None:
            self._widget.setDataset(dataset)
            
    def _on_fit_clicked(self):
        """Handle fit button click."""
        if self.input_dataset is None:
            return
            
        # Update settings from widget
        self.int_thresh = float(self._widget.getIntensityThreshold())
        self.method = self._widget.getFitMethod()
        
    def get_task_inputs(self):
        """Get inputs for the ewoks task."""
        return {
            "dataset": self.input_dataset,
            "int_thresh": self.int_thresh,
            "method": self.method,
            "output_filename": None,
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