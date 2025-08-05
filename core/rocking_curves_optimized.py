"""
Optimized curve fitting implementation with batching and shared memory support.
"""

from __future__ import annotations

import multiprocessing as mp
from functools import partial
from typing import Any, List, Tuple, Union, Optional
import numpy as np
from multiprocessing import shared_memory
import psutil
import tqdm

from ..processing.rocking_curves import FitMethod, fit_rocking_curve, fit_2d_rocking_curve
from .rocking_curves import Maps_1D, Maps_2D, Indices, DataLike, fit_2d_data

# Determine optimal batch size based on system resources
def get_optimal_batch_size(total_curves: int, data_shape: tuple) -> int:
    """Calculate optimal batch size based on available memory and CPU count."""
    # Get available memory
    available_memory = psutil.virtual_memory().available
    
    # Estimate memory per curve (assuming float64)
    memory_per_curve = data_shape[0] * 8 * 2  # x2 for processing overhead
    
    # Use 50% of available memory for safety
    max_curves_by_memory = int((available_memory * 0.5) / memory_per_curve)
    
    # Balance with CPU count
    cpu_count = mp.cpu_count()
    optimal_batch = min(
        max(total_curves // (cpu_count * 4), 10),  # At least 10 curves per batch
        max_curves_by_memory,
        1000  # Maximum batch size
    )
    
    return optimal_batch


def create_shared_array(data: np.ndarray) -> Tuple[shared_memory.SharedMemory, np.ndarray]:
    """Create a shared memory array from numpy array."""
    # Create shared memory
    shm = shared_memory.SharedMemory(create=True, size=data.nbytes)
    
    # Create numpy array backed by shared memory
    shared_array = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
    shared_array[:] = data[:]
    
    return shm, shared_array


def fit_batch_1d(args: Tuple[int, int, tuple, np.dtype, str, Optional[List[np.ndarray]], 
                             Optional[float], Optional[FitMethod]]) -> List[Tuple[np.ndarray, np.ndarray]]:
    """Fit a batch of 1D rocking curves using shared memory."""
    start_idx, end_idx, data_shape, dtype, shm_name, values, int_thresh, method = args
    
    # Attach to shared memory
    existing_shm = shared_memory.SharedMemory(name=shm_name)
    data = np.ndarray(data_shape, dtype=dtype, buffer=existing_shm.buf)
    
    results = []
    for idx in range(start_idx, end_idx):
        i = idx // data_shape[2]
        j = idx % data_shape[2]
        
        curve_data = data[:, i, j]
        curve, pars = fit_rocking_curve(
            (curve_data, None),
            x_values=values,
            int_thresh=int_thresh,
            method=method
        )
        results.append((curve, pars))
    
    # Detach from shared memory (don't unlink)
    existing_shm.close()
    
    return results


def fit_data_optimized(
    data: DataLike,
    moments: Optional[np.ndarray] = None,
    values: Optional[Union[List[np.ndarray], np.ndarray]] = None,
    shape: Any = None,
    indices: Optional[Indices] = None,
    int_thresh: float = 15,
    method: Optional[FitMethod] = None,
    use_single_thread_for_small: bool = True,
) -> Tuple[np.ndarray, np.ndarray]:
    """Optimized version of fit_data with batching and shared memory."""
    
    total_curves = data.shape[1] * data.shape[2]
    
    # For small datasets, use single-threaded approach
    if use_single_thread_for_small and total_curves < 100:
        curves, maps = [], []
        for i in range(data.shape[1]):
            for j in range(data.shape[2]):
                curve_data = data[:, i, j]
                curve, pars = fit_rocking_curve(
                    (curve_data, None),
                    x_values=values,
                    int_thresh=int_thresh,
                    method=method
                )
                curves.append(list(curve))
                maps.append(list(pars))
        
        return np.array(curves).T.reshape(data.shape), np.array(maps).T.reshape(
            (4, data.shape[-2], data.shape[-1])
        )
    
    # Create shared memory for data
    shm, shared_data = create_shared_array(data)
    
    try:
        # Calculate batch size
        batch_size = get_optimal_batch_size(total_curves, data.shape)
        
        # Create batches
        batches = []
        for i in range(0, total_curves, batch_size):
            batches.append((
                i, 
                min(i + batch_size, total_curves),
                data.shape,
                data.dtype,
                shm.name,
                values,
                int_thresh,
                method
            ))
        
        # Process batches in parallel
        cpus = mp.cpu_count() - 1
        curves, maps = [], []
        
        with mp.Pool(cpus) as pool:
            # Use imap for progress tracking
            for batch_results in tqdm.tqdm(
                pool.imap(fit_batch_1d, batches),
                total=len(batches),
                desc="Fitting curves (batched)"
            ):
                for curve, pars in batch_results:
                    curves.append(list(curve))
                    maps.append(list(pars))
        
        return np.array(curves).T.reshape(data.shape), np.array(maps).T.reshape(
            (4, data.shape[-2], data.shape[-1])
        )
        
    finally:
        # Clean up shared memory
        shm.close()
        shm.unlink()


def compute_residuals_optimized(
    target_dataset,
    original_dataset,
    indices: Optional[np.ndarray],
) -> np.ndarray:
    """Optimized residuals calculation using vectorized operations."""
    # Use numpy.abs instead of sqrt(square) for better performance
    # If true RMS is needed, use: np.sqrt(np.square(target - original))
    return np.abs(target_dataset.zsum(indices) - original_dataset.zsum(indices))


class BatchedCurveFitter:
    """Helper class for managing batched curve fitting with cancellation support."""
    
    def __init__(self, data: DataLike, **kwargs):
        self.data = data
        self.kwargs = kwargs
        self._cancelled = mp.Event()
        self._pool = None
        
    def cancel(self):
        """Cancel the fitting operation."""
        self._cancelled.set()
        if self._pool:
            self._pool.terminate()
            
    def fit(self, progress_callback=None) -> Tuple[np.ndarray, np.ndarray]:
        """Perform fitting with optional progress callback."""
        total_curves = self.data.shape[1] * self.data.shape[2]
        
        # Create shared memory
        shm, shared_data = create_shared_array(self.data)
        
        try:
            batch_size = get_optimal_batch_size(total_curves, self.data.shape)
            batches = self._create_batches(total_curves, batch_size, shm.name)
            
            cpus = mp.cpu_count() - 1
            self._pool = mp.Pool(cpus)
            
            curves, maps = [], []
            completed = 0
            
            try:
                for batch_results in self._pool.imap(fit_batch_1d, batches):
                    if self._cancelled.is_set():
                        break
                        
                    for curve, pars in batch_results:
                        curves.append(list(curve))
                        maps.append(list(pars))
                    
                    completed += len(batch_results)
                    if progress_callback:
                        progress_callback(completed, total_curves)
                        
            finally:
                self._pool.close()
                self._pool.join()
                
            if self._cancelled.is_set():
                raise InterruptedError("Fitting cancelled by user")
                
            return (
                np.array(curves).T.reshape(self.data.shape),
                np.array(maps).T.reshape((4, self.data.shape[-2], self.data.shape[-1]))
            )
            
        finally:
            shm.close()
            shm.unlink()
            
    def _create_batches(self, total_curves: int, batch_size: int, shm_name: str) -> List[tuple]:
        """Create batch arguments for parallel processing."""
        batches = []
        for i in range(0, total_curves, batch_size):
            batches.append((
                i,
                min(i + batch_size, total_curves),
                self.data.shape,
                self.data.dtype,
                shm_name,
                self.kwargs.get('values'),
                self.kwargs.get('int_thresh', 15),
                self.kwargs.get('method')
            ))
        return batches


# Auto-selection of fit method based on data characteristics
def select_optimal_fit_method(data: np.ndarray, sample_size: int = 100) -> FitMethod:
    """Automatically select the best fitting method based on data characteristics."""
    # Sample random curves for analysis
    total_curves = data.shape[1] * data.shape[2]
    sample_indices = np.random.choice(total_curves, min(sample_size, total_curves), replace=False)
    
    # Analyze noise level and curve characteristics
    noise_levels = []
    curve_widths = []
    
    for idx in sample_indices:
        i = idx // data.shape[2]
        j = idx % data.shape[2]
        curve = data[:, i, j]
        
        # Estimate noise as std of high-frequency components
        if len(curve) > 10:
            diff = np.diff(curve)
            noise_levels.append(np.std(diff))
            
            # Estimate curve width
            if np.ptp(curve) > 0:
                normalized = (curve - np.min(curve)) / np.ptp(curve)
                above_half = np.where(normalized > 0.5)[0]
                if len(above_half) > 0:
                    curve_widths.append(above_half[-1] - above_half[0])
    
    avg_noise = np.mean(noise_levels) if noise_levels else 0
    avg_width = np.mean(curve_widths) if curve_widths else data.shape[0] / 4
    
    # Select method based on characteristics
    if avg_noise > 0.1 * np.mean([np.ptp(data[:, i, j]) for i in range(min(10, data.shape[1])) 
                                   for j in range(min(10, data.shape[2]))]):
        # High noise - use robust method
        return 'trf'
    elif avg_width < data.shape[0] * 0.1:
        # Narrow peaks - use dogbox for better convergence
        return 'dogbox'
    else:
        # Default to Levenberg-Marquardt for speed
        return 'lm'


def fit_batch_2d(args: Tuple[int, int, tuple, np.dtype, str, List[np.ndarray], 
                             Tuple[int, int], Optional[float], Optional[FitMethod]]) -> List[Tuple[np.ndarray, np.ndarray]]:
    """Fit a batch of 2D rocking curves using shared memory."""
    start_idx, end_idx, data_shape, dtype, shm_name, values, shape, int_thresh, method = args
    
    # Attach to shared memory
    existing_shm = shared_memory.SharedMemory(name=shm_name)
    data = np.ndarray(data_shape, dtype=dtype, buffer=existing_shm.buf)
    
    results = []
    for idx in range(start_idx, end_idx):
        i = idx // data_shape[2]
        j = idx % data_shape[2]
        
        # Extract 2D curve data
        curve_data = data[:, i, j]
        curve, pars = fit_2d_rocking_curve(
            (curve_data, None),
            x_values=values,
            shape=shape,
            int_thresh=int_thresh,
            method=method
        )
        results.append((curve, pars))
    
    # Detach from shared memory
    existing_shm.close()
    
    return results


def fit_2d_data_optimized(
    data: DataLike,
    values: List[np.ndarray],
    shape: Tuple[int, int],
    moments: Optional[np.ndarray] = None,
    int_thresh: float = 15,
    indices: Optional[Indices] = None,
    method: Optional[FitMethod] = None,
    use_single_thread_for_small: bool = True,
) -> Tuple[np.ndarray, np.ndarray]:
    """Optimized version of fit_2d_data with batching and shared memory."""
    
    total_curves = data.shape[1] * data.shape[2]
    
    # For small datasets, use original implementation
    if use_single_thread_for_small and total_curves < 100:
        return fit_2d_data(data, values, shape, moments, int_thresh, indices, method)
    
    # Create shared memory for data
    shm, shared_data = create_shared_array(data)
    
    try:
        # Calculate batch size
        batch_size = get_optimal_batch_size(total_curves, data.shape)
        
        # Create batches
        batches = []
        for i in range(0, total_curves, batch_size):
            batches.append((
                i, 
                min(i + batch_size, total_curves),
                data.shape,
                data.dtype,
                shm.name,
                values,
                shape,
                int_thresh,
                method
            ))
        
        # Process batches in parallel
        cpus = mp.cpu_count() - 1
        curves, maps = [], []
        
        with mp.Pool(cpus) as pool:
            for batch_results in tqdm.tqdm(
                pool.imap(fit_batch_2d, batches),
                total=len(batches),
                desc="Fitting 2D curves (batched)"
            ):
                for curve, pars in batch_results:
                    curves.append(list(curve))
                    maps.append(list(pars))
        
        curves = np.array(curves).T
        if indices is not None:
            curves = curves[indices]
        return curves.reshape(data[indices].shape), np.array(maps).T.reshape(
            (7, data.shape[-2], data.shape[-1])
        )
        
    finally:
        # Clean up shared memory
        shm.close()
        shm.unlink()