#!/usr/bin/env python
"""
Benchmark different curve fitting methods (trf, lm, dogbox) to determine optimal defaults.
"""

import time
import numpy as np
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt

# Add the project root to the path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from processing.rocking_curves import fit_rocking_curve, FitMethod


class FitMethodBenchmark:
    """Benchmark different scipy curve_fit methods."""
    
    def __init__(self):
        self.results: Dict[str, Dict[str, List[float]]] = {
            'trf': {'times': [], 'errors': [], 'failures': 0},
            'lm': {'times': [], 'errors': [], 'failures': 0},
            'dogbox': {'times': [], 'errors': [], 'failures': 0}
        }
        
    def generate_test_curves(self, n_curves: int = 100) -> List[Tuple[np.ndarray, np.ndarray, dict]]:
        """Generate various types of test curves with known parameters."""
        curves = []
        np.random.seed(42)
        
        for i in range(n_curves):
            # Vary curve characteristics
            n_points = np.random.choice([50, 100, 200])
            x = np.linspace(0, 10, n_points)
            
            # True parameters
            amplitude = np.random.uniform(50, 500)
            center = np.random.uniform(3, 7)
            width = np.random.uniform(0.5, 2.0)
            background = np.random.uniform(5, 50)
            
            # Generate curve
            y_true = amplitude * np.exp(-0.5 * ((x - center) / width)**2) + background
            
            # Add different noise levels
            noise_level = np.random.choice([0.01, 0.05, 0.1, 0.2])
            noise = np.random.normal(0, noise_level * amplitude, n_points)
            y_noisy = y_true + noise
            
            # Store true parameters
            true_params = {
                'amplitude': amplitude,
                'center': center,
                'width': width,
                'background': background
            }
            
            curves.append((x, y_noisy, true_params))
            
        return curves
    
    def benchmark_method(self, method: FitMethod, curves: List[Tuple[np.ndarray, np.ndarray, dict]]):
        """Benchmark a specific fitting method."""
        print(f"\nBenchmarking {method} method...")
        
        for x, y, true_params in curves:
            start_time = time.time()
            
            try:
                y_fit, fit_params = fit_rocking_curve((y, None), x_values=x, method=method)
                fit_time = time.time() - start_time
                
                # Calculate fitting error
                error = self._calculate_error(fit_params, true_params)
                
                self.results[method]['times'].append(fit_time)
                self.results[method]['errors'].append(error)
                
            except Exception as e:
                self.results[method]['failures'] += 1
                
    def _calculate_error(self, fit_params: np.ndarray, true_params: dict) -> float:
        """Calculate relative error between fitted and true parameters."""
        # fit_params: [amplitude, center, fwhm, background]
        # Convert width to FWHM for comparison
        true_fwhm = true_params['width'] * 2.355  # FWHM = 2.355 * sigma
        
        errors = [
            abs(fit_params[0] - true_params['amplitude']) / true_params['amplitude'],
            abs(fit_params[1] - true_params['center']) / abs(true_params['center']),
            abs(fit_params[2] - true_fwhm) / true_fwhm,
            abs(fit_params[3] - true_params['background']) / (true_params['background'] + 1e-6)
        ]
        
        return np.mean(errors)
    
    def analyze_results(self):
        """Analyze and display benchmark results."""
        print("\n" + "="*60)
        print("FIT METHOD BENCHMARK RESULTS")
        print("="*60)
        
        for method in ['trf', 'lm', 'dogbox']:
            data = self.results[method]
            
            if data['times']:
                avg_time = np.mean(data['times']) * 1000  # Convert to ms
                std_time = np.std(data['times']) * 1000
                avg_error = np.mean(data['errors']) * 100  # Convert to percentage
                std_error = np.std(data['errors']) * 100
                
                print(f"\n{method.upper()} Method:")
                print(f"  Average time: {avg_time:.3f} ± {std_time:.3f} ms")
                print(f"  Average error: {avg_error:.1f} ± {std_error:.1f} %")
                print(f"  Failure rate: {data['failures']}/{len(data['times']) + data['failures']}")
            else:
                print(f"\n{method.upper()} Method: No successful fits")
                
    def plot_results(self):
        """Create visualization of benchmark results."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        methods = ['trf', 'lm', 'dogbox']
        colors = ['blue', 'green', 'red']
        
        # Time comparison
        times_data = [np.array(self.results[m]['times']) * 1000 for m in methods]
        ax1.boxplot(times_data, labels=methods)
        ax1.set_ylabel('Fit Time (ms)')
        ax1.set_title('Fitting Speed Comparison')
        ax1.grid(True, alpha=0.3)
        
        # Error comparison
        errors_data = [np.array(self.results[m]['errors']) * 100 for m in methods]
        ax2.boxplot(errors_data, labels=methods)
        ax2.set_ylabel('Relative Error (%)')
        ax2.set_title('Fitting Accuracy Comparison')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('fit_method_comparison.png', dpi=150)
        print("\nPlot saved as 'fit_method_comparison.png'")
        
    def recommend_default(self) -> str:
        """Recommend the best default method based on results."""
        scores = {}
        
        for method in ['trf', 'lm', 'dogbox']:
            data = self.results[method]
            if not data['times']:
                scores[method] = float('inf')
                continue
                
            # Score based on speed (40%), accuracy (40%), and reliability (20%)
            avg_time = np.mean(data['times'])
            avg_error = np.mean(data['errors'])
            failure_rate = data['failures'] / (len(data['times']) + data['failures'])
            
            # Normalize scores (lower is better)
            time_score = avg_time / 0.001  # Normalize to 1ms baseline
            error_score = avg_error / 0.01  # Normalize to 1% baseline
            reliability_score = failure_rate / 0.01  # Normalize to 1% baseline
            
            scores[method] = 0.4 * time_score + 0.4 * error_score + 0.2 * reliability_score
            
        best_method = min(scores, key=scores.get)
        
        print(f"\n{'='*60}")
        print(f"RECOMMENDATION: Use '{best_method}' as default")
        print(f"Score breakdown (lower is better):")
        for method, score in sorted(scores.items(), key=lambda x: x[1]):
            print(f"  {method}: {score:.3f}")
            
        return best_method


def benchmark_problem_specific_selection():
    """Test auto-selection based on problem characteristics."""
    print("\n" + "="*60)
    print("PROBLEM-SPECIFIC METHOD SELECTION TEST")
    print("="*60)
    
    # Test different problem types
    problem_types = {
        'narrow_peaks': {
            'width_range': (0.1, 0.3),
            'noise': 0.05,
            'description': 'Narrow peaks (challenging convergence)'
        },
        'noisy_data': {
            'width_range': (1.0, 2.0),
            'noise': 0.3,
            'description': 'High noise data'
        },
        'standard': {
            'width_range': (0.5, 1.5),
            'noise': 0.1,
            'description': 'Standard conditions'
        }
    }
    
    for problem_name, config in problem_types.items():
        print(f"\n{config['description']}:")
        
        # Generate test data
        x = np.linspace(0, 10, 100)
        width = np.random.uniform(*config['width_range'])
        y_true = 100 * np.exp(-0.5 * ((x - 5) / width)**2) + 20
        y_noisy = y_true + np.random.normal(0, config['noise'] * 100, 100)
        
        # Test each method
        for method in ['trf', 'lm', 'dogbox']:
            try:
                start = time.time()
                y_fit, params = fit_rocking_curve((y_noisy, None), x_values=x, method=method)
                elapsed = time.time() - start
                
                # Calculate fit quality
                residual = np.mean((y_fit - y_true)**2)**0.5
                print(f"  {method}: {elapsed*1000:.1f}ms, RMSE: {residual:.2f}")
                
            except Exception as e:
                print(f"  {method}: FAILED - {str(e)}")


def main():
    """Run the complete benchmark suite."""
    # Create benchmark instance
    benchmark = FitMethodBenchmark()
    
    # Generate test curves
    print("Generating test curves...")
    test_curves = benchmark.generate_test_curves(n_curves=500)
    
    # Benchmark each method
    for method in ['trf', 'lm', 'dogbox']:
        benchmark.benchmark_method(method, test_curves)
        
    # Analyze results
    benchmark.analyze_results()
    
    # Create visualization
    try:
        benchmark.plot_results()
    except Exception as e:
        print(f"Could not create plot: {e}")
        
    # Get recommendation
    benchmark.recommend_default()
    
    # Test problem-specific selection
    benchmark_problem_specific_selection()


if __name__ == '__main__':
    main()