"""
Benchmark configuration and fixtures.

Provides common benchmarking utilities, data fixtures, and configuration.
"""

import time
import statistics
import numpy as np
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

class BenchmarkRunner:
    """Utility class for running and timing benchmark functions."""
    
    def __init__(self, iterations=1000, warmup=10):
        self.iterations = iterations
        self.warmup = warmup
        
    def run_benchmark(self, func, name="benchmark"):
        """Run a function multiple times and return timing statistics."""
        # Warmup runs to stabilize performance
        for _ in range(self.warmup):
            try:
                func()
            except Exception:
                pass
        
        times = []
        for _ in range(self.iterations):
            start = time.perf_counter()
            try:
                result = func()
            except Exception as e:
                return {
                    'name': name,
                    'error': str(e),
                    'success': False
                }
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to milliseconds
        
        return {
            'name': name,
            'success': True,
            'times': times,
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times),
            'result': result
        }
    
    def compare_benchmarks(self, baseline_func, test_func, baseline_name="baseline", test_name="test"):
        """Compare two functions and return relative performance."""
        baseline_results = self.run_benchmark(baseline_func, baseline_name)
        test_results = self.run_benchmark(test_func, test_name)
        
        if not (baseline_results['success'] and test_results['success']):
            return None
            
        speedup = baseline_results['mean'] / test_results['mean']
        
        return {
            'baseline': baseline_results,
            'test': test_results,
            'speedup': speedup,
            'faster': speedup > 1.0
        }

def create_benchmark_data():
    """Create common benchmark datasets."""
    import random
    random.seed(42)  # For reproducible benchmarks
    np.random.seed(42)  # For NumPy/PyTorch data
    
    # Core Python data types for core operations benchmarks
    data = {
        'list_small': list(range(1000)),
        'list_medium': list(range(10000)),
        'list_large': list(range(100000)),
        'list_float_small': [random.random() for _ in range(1000)],
        'list_float_medium': [random.random() for _ in range(10000)],
        'list_int_small': [random.randint(1, 1000) for _ in range(1000)],
        'list_int_medium': [random.randint(1, 1000) for _ in range(10000)],
        'list_strings': [f"item_{i}" for i in range(1000)],
        'tuple_small': tuple(range(1000)),
        'tuple_medium': tuple(range(10000)),
    }
    
    # Add NumPy arrays for NumPy-specific benchmarks
    data.update({
        'small_array': np.random.rand(1000),
        'medium_array': np.random.rand(10000), 
        'large_array': np.random.rand(100000),
        'int_array': np.random.randint(1, 100, 5000),
        'float_array': np.random.rand(5000).astype(np.float32),
        '2d_small': np.random.rand(100, 100),
        '2d_medium': np.random.rand(316, 316),
    })
    
    if HAS_TORCH:
        torch.manual_seed(42)
        data.update({
            'torch_small': torch.randn(1000),
            'torch_medium': torch.randn(10000),
            'torch_large': torch.randn(100000),
            'torch_int': torch.randint(1, 100, (5000,)),
            'torch_float': torch.randn(5000).float(),
            'torch_2d': torch.randn(316, 316),
        })
        
        if torch.cuda.is_available():
            data.update({
                'torch_cuda_small': torch.randn(1000).cuda(),
                'torch_cuda_medium': torch.randn(10000).cuda(),
            })
    
    if HAS_PANDAS:
        data.update({
            'pandas_series_small': pd.Series(np.random.rand(1000)),
            'pandas_series_medium': pd.Series(np.random.rand(10000)),
            'pandas_df_small': pd.DataFrame({
                'A': np.random.rand(1000),
                'B': np.random.rand(1000),
                'C': np.random.randint(1, 10, 1000)
            }),
        })
    
    return data

def format_benchmark_results(comparison_results, title="Benchmark Results"):
    """Format benchmark comparison results for display."""
    if not comparison_results:
        return f"{title}: FAILED"
    
    baseline = comparison_results['baseline']
    test = comparison_results['test']
    speedup = comparison_results['speedup']
    
    faster_symbol = "🚀" if speedup > 1.0 else "🐌"
    
    return (
        f"{title}:\n"
        f"  {baseline['name']}: {baseline['mean']:.3f}ms ± {baseline['stdev']:.3f}ms\n"
        f"  {test['name']}: {test['mean']:.3f}ms ± {test['stdev']:.3f}ms\n"
        f"  Speedup: {speedup:.2f}x {faster_symbol}"
    )

def print_benchmark_summary(results_list, category="Benchmark"):
    """Print a summary of multiple benchmark results."""
    print(f"\n{'='*60}")
    print(f"{category} Performance Summary")
    print(f"{'='*60}")
    
    total_tests = len(results_list)
    successful_tests = sum(1 for r in results_list if r and r.get('speedup', 0) > 0)
    faster_tests = sum(1 for r in results_list if r and r.get('speedup', 0) > 1.0)
    
    if successful_tests == 0:
        print("❌ No successful benchmarks")
        return
    
    speedups = [r['speedup'] for r in results_list if r and 'speedup' in r]
    if speedups:
        avg_speedup = statistics.mean(speedups)
        max_speedup = max(speedups)
        min_speedup = min(speedups)
        
        print(f"📊 Results: {successful_tests}/{total_tests} successful")
        print(f"🚀 Faster than baseline: {faster_tests}/{successful_tests} ({faster_tests/successful_tests*100:.1f}%)")
        print(f"📈 Average speedup: {avg_speedup:.2f}x")
        print(f"🔝 Best speedup: {max_speedup:.2f}x")
        print(f"🔽 Worst speedup: {min_speedup:.2f}x")
        
        # Performance tiers
        excellent = sum(1 for s in speedups if s > 1.5)
        good = sum(1 for s in speedups if 1.1 < s <= 1.5)
        acceptable = sum(1 for s in speedups if 0.9 <= s <= 1.1)
        slow = sum(1 for s in speedups if s < 0.9)
        
        print(f"\n📋 Performance Distribution:")
        print(f"  Excellent (>1.5x): {excellent}")
        print(f"  Good (1.1-1.5x): {good}")  
        print(f"  Acceptable (0.9-1.1x): {acceptable}")
        print(f"  Slow (<0.9x): {slow}")