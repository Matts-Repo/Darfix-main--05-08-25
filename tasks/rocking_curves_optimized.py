"""
Optimized rocking curves task with improved performance.
"""

from __future__ import annotations

import os.path
from typing import Literal, Optional

from ewokscore import Task
from ewokscore.missing_data import MISSING_DATA, MissingData
from ewokscore.model import BaseInputModel
from pydantic import ConfigDict
from silx.io.dictdump import dicttonx

from ..core.rocking_curves import generate_rocking_curves_nxdict
from ..core.rocking_curves_optimized import (
    fit_data_optimized,
    fit_2d_data_optimized,
    compute_residuals_optimized,
    select_optimal_fit_method
)
from ..dtypes import Dataset


class Inputs(BaseInputModel):
    model_config = ConfigDict(use_attribute_docstrings=True)
    dataset: Dataset
    """ Input dataset containing a stack of images """
    int_thresh: float | MissingData = MISSING_DATA
    """If provided, only the rocking curves with higher ptp (peak to peak) value > int_thresh are fitted, others are assumed to be noise and will be discarded"""
    method: Literal["trf", "lm", "dogbox", "auto"] = "auto"
    """Method to use for the rocking curves fit. 'auto' automatically selects the best method based on data characteristics."""
    output_filename: str | MissingData = MISSING_DATA
    """Output filename to save the rocking curves results. Result is not saved if not provided"""
    use_optimizations: bool = True
    """Enable performance optimizations including batching and shared memory"""


class RockingCurvesOptimized(
    Task,
    input_model=Inputs,
    output_names=["dataset", "maps"],
):
    """Optimized version of RockingCurves with improved performance through batching and shared memory.
    
    Analyze the rocking curve of each pixel of each image of the darfix dataset by fitting to a peak shape, e.g. a Gaussian.
    
    Performance improvements:
    - Batched processing to reduce multiprocessing overhead
    - Shared memory to eliminate data serialization costs
    - Single-threaded fallback for small datasets
    - Auto-selection of optimal fitting method
    
    Related article : https://pmc.ncbi.nlm.nih.gov/articles/PMC10161887/#sec3.3.1
    """

    def run(self):
        input_dataset: Dataset = self.inputs.dataset
        int_thresh: float | None = (
            float(self.inputs.int_thresh) if self.inputs.int_thresh else None
        )
        method: str = self.inputs.method
        use_optimizations: bool = self.inputs.use_optimizations
        
        default_filename = os.path.join(input_dataset.dataset._dir, "rocking_curves_optimized.h5")
        output_filename: str | None = self.get_input_value(
            "output_filename", default_filename
        )

        if output_filename and os.path.isfile(output_filename):
            raise OSError(
                f"""Cannot launch rocking curves fit: saving destination {output_filename} already exists.
                Change the `output_filename` input or set it to None to disable saving."""
            )

        dataset = input_dataset.dataset
        indices = input_dataset.indices
        
        # Get data for fitting
        data = dataset.get_data(indices)
        
        # Auto-select method if requested
        if method == "auto":
            method = select_optimal_fit_method(data)
            self.log.info(f"Auto-selected fitting method: {method}")
        
        # Prepare values for fitting based on dimensionality
        if dataset.dims.ndim == 1:
            dim = dataset.dims.get(0)
            values = dataset.get_metadata_values(key=dim.name, indices=indices)
            
            # Use optimized fitting
            if use_optimizations:
                curves, maps = fit_data_optimized(
                    data,
                    values=values,
                    int_thresh=int_thresh,
                    method=method
                )
            else:
                # Fallback to original implementation
                new_image_dataset, maps = dataset.apply_fit(
                    indices=indices, int_thresh=int_thresh, method=method
                )
                curves = new_image_dataset.get_data()
                
        elif dataset.dims.ndim == 2:
            xdim = dataset.dims.get(1)
            ydim = dataset.dims.get(0)
            values = [
                dataset.get_metadata_values(key=ydim.name),
                dataset.get_metadata_values(key=xdim.name),
            ]
            shape = (ydim.size, xdim.size)
            
            # Use optimized 2D fitting
            if use_optimizations:
                curves, maps = fit_2d_data_optimized(
                    data,
                    values=values,
                    shape=shape,
                    int_thresh=int_thresh,
                    method=method
                )
            else:
                # Fallback to original implementation
                new_image_dataset, maps = dataset.apply_fit(
                    indices=indices, int_thresh=int_thresh, method=method
                )
                curves = new_image_dataset.get_data()
        else:
            raise ValueError(f"Unsupported number of dimensions: {dataset.dims.ndim}")
        
        # Create new dataset with fitted curves
        new_image_dataset = dataset.copy()
        new_image_dataset.set_data(curves)

        if output_filename is not None:
            # Use optimized residuals calculation
            if use_optimizations:
                residuals = compute_residuals_optimized(new_image_dataset, dataset, indices)
            else:
                from ..core.rocking_curves import compute_residuals
                residuals = compute_residuals(new_image_dataset, dataset, indices)
                
            nxdict = generate_rocking_curves_nxdict(
                new_image_dataset,
                maps,
                residuals=residuals,
            )
            dicttonx(nxdict, output_filename)

        self.outputs.dataset = Dataset(
            dataset=new_image_dataset,
            indices=indices,
            bg_indices=input_dataset.bg_indices,
            bg_dataset=input_dataset.bg_dataset,
        )
        self.outputs.maps = maps