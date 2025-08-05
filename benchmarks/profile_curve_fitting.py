#!/usr/bin/env python
"""
Profile curve fitting performance to establish baseline and measure optimizations.
"""

import time
import numpy as np
import cProfile
import pstats
from io import StringIO
from typing import Tuple, List
import multiprocessing

# Add the project root to the path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.rocking_curves import fit_data, fit_2d_data
from processing.rocking_curves import fit_rocking_curve, fit_2d_rocking_curve


class CurveFittingProfiler:
    """Profile curve fitting operations with various dataset sizes."""
    
    def __init__(self):
        self.results = {}
        
    def generate_test_data(self, shape: Tuple[int, int, int], noise_level: float = 0.1) -> np.ndarray:
        """Generate synthetic rocking curve data with Gaussian peaks."""
        nframes, height, width = shape
        data = np.zeros(shape)
        
        # Generate parameters for each pixel
        np.random.seed(42)  # For reproducibility
        amplitudes = np.random.uniform(100, 1000, (height, width))
        centers = np.random.uniform(nframes * 0.3, nframes * 0.7, (height, width))
        widths = np.random.uniform(nframes * 0.05, nframes * 0.15, (height, width))
        backgrounds = np.random.uniform(10, 50, (height, width))
        
        # Generate rocking curves
        x = np.arange(nframes)
        for i in range(height):
            for j in range(width):
                # Gaussian curve
                curve = amplitudes[i, j] * np.exp(-0.5 * ((x - centers[i, j]) / widths[i, j])**2)
                curve += backgrounds[i, j]
                # Add noise
                curve += np.random.normal(0, noise_level * amplitudes[i, j], nframes)
                data[:, i, j] = curve
                
        return data
    
    def profile_single_curve_fit(self, iterations: int = 1000):
        """Profile single curve fitting performance."""
        print(f"\nProfiling single curve fit ({iterations} iterations)...")
        
        # Generate test curve
        x = np.linspace(0, 10, 100)
        y = 50 * np.exp(-0.5 * ((x - 5) / 1.5)**2) + 10 + np.random.normal(0, 2, 100)
        
        start_time = time.time()
        for _ in range(iterations):
            fit_rocking_curve((y, None), x_values=x)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / iterations
        print(f"Average time per curve: {avg_time*1000:.3f} ms")
        self.results['single_curve_avg_ms'] = avg_time * 1000
        
    def profile_multiprocessing_overhead(self, shape: Tuple[int, int, int]):
        """Profile multiprocessing vs single-threaded performance."""
        print(f"\nProfiling multiprocessing with data shape {shape}...")
        
        data = self.generate_test_data(shape)
        total_curves = shape[1] * shape[2]
        
        # Profile with multiprocessing
        print("Running with multiprocessing...")
        mp_start = time.time()
        curves_mp, maps_mp = fit_data(data)
        mp_time = time.time() - mp_start
        
        print(f"Multiprocessing time: {mp_time:.2f}s")
        print(f"Time per curve: {mp_time/total_curves*1000:.3f} ms")
        
        self.results[f'mp_total_time_{shape}'] = mp_time
        self.results[f'mp_per_curve_ms_{shape}'] = mp_time/total_curves*1000
        
    def profile_data_transfer(self, shape: Tuple[int, int, int]):
        """Profile data transfer overhead in multiprocessing."""
        print(f"\nProfiling data transfer overhead for shape {shape}...")
        
        data = self.generate_test_data(shape)
        
        # Measure serialization time
        import pickle
        start = time.time()
        for i in range(shape[1]):
            for j in range(shape[2]):
                curve_data = data[:, i, j]
                _ = pickle.dumps(curve_data)
        serialization_time = time.time() - start
        
        total_curves = shape[1] * shape[2]
        print(f"Total serialization time: {serialization_time:.2f}s")
        print(f"Per-curve serialization: {serialization_time/total_curves*1000:.3f} ms")
        
        self.results[f'serialization_total_{shape}'] = serialization_time
        self.results[f'serialization_per_curve_ms_{shape}'] = serialization_time/total_curves*1000
        
    def profile_with_cprofile(self, shape: Tuple[int, int, int]):
        """Detailed profiling with cProfile."""
        print(f"\nDetailed profiling with cProfile for shape {shape}...")
        
        data = self.generate_test_data(shape)
        
        profiler = cProfile.Profile()
        profiler.enable()
        
        curves, maps = fit_data(data)
        
        profiler.disable()
        
        # Get profiling results
        s = StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats(20)  # Top 20 functions
        
        print("\nTop 20 time-consuming functions:")
        print(s.getvalue())
        
    def generate_report(self):
        """Generate performance report."""
        print("\n" + "="*60)
        print("CURVE FITTING PERFORMANCE REPORT")
        print("="*60)
        
        print("\nCPU Information:")
        print(f"  CPU Count: {multiprocessing.cpu_count()}")
        print(f"  Workers Used: {multiprocessing.cpu_count() - 1}")
        
        print("\nPerformance Metrics:")
        for key, value in self.results.items():
            print(f"  {key}: {value:.3f}")
            
        # Calculate efficiency
        if 'single_curve_avg_ms' in self.results:
            for key in self.results:
                if 'mp_per_curve_ms' in key:
                    shape = key.split('_')[-1]
                    efficiency = self.results['single_curve_avg_ms'] / self.results[key]
                    print(f"\nMultiprocessing efficiency for {shape}: {efficiency:.2f}x")
                    
                    # Account for serialization
                    serialization_key = f'serialization_per_curve_ms_{shape}'
                    if serialization_key in self.results:
                        overhead_pct = (self.results[serialization_key] / self.results[key]) * 100
                        print(f"  Serialization overhead: {overhead_pct:.1f}%")


def main():
    """Run profiling suite."""
    profiler = CurveFittingProfiler()
    
    # Test different data sizes
    test_shapes = [
        (50, 64, 64),    # Small dataset
        (100, 128, 128), # Medium dataset
        (200, 256, 256), # Large dataset
    ]
    
    # Profile single curve performance
    profiler.profile_single_curve_fit()
    
    # Profile multiprocessing for different sizes
    for shape in test_shapes:
        profiler.profile_multiprocessing_overhead(shape)
        profiler.profile_data_transfer(shape)
    
    # Detailed profiling for medium dataset
    profiler.profile_with_cprofile(test_shapes[1])
    
    # Generate report
    profiler.generate_report()


if __name__ == '__main__':
    main()