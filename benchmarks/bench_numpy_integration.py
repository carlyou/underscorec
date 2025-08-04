#!/usr/bin/env python3
"""
NumPy Integration Performance Benchmarks

Benchmarks UnderscoreC NumPy integration against native NumPy operations.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("❌ NumPy not available - skipping NumPy benchmarks")
    sys.exit(0)

from underscorec import __
from conftest import BenchmarkRunner, create_benchmark_data, format_benchmark_results, print_benchmark_summary

def run_array_arithmetic_benchmarks():
    """Benchmark NumPy array arithmetic operations."""
    runner = BenchmarkRunner(iterations=10000)
    data = create_benchmark_data()
    results = []
    
    print("\n🔢 NumPy Array Arithmetic Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('small_array', data['small_array']),
        ('medium_array', data['medium_array']),
        ('large_array', data['large_array']),
        ('2d_small', data['2d_small']),
    ]
    
    for name, arr in test_cases:
        print(f"\nArray: {name} ({arr.size:,} elements, shape: {arr.shape})")
        
        # Pre-define UnderscoreC expressions to avoid reconstruction overhead
        add_5_underscore = __ + 5.0
        mul_2_5_underscore = __ * 2.5
        power_2_underscore = __ ** 2
        
        # Addition
        baseline_func = lambda: arr + 5.0
        underscorec_func = lambda: add_5_underscore(arr)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "numpy_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Addition"))
        
        # Multiplication  
        baseline_func = lambda: arr * 2.5
        underscorec_func = lambda: mul_2_5_underscore(arr)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "numpy_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Multiplication"))
        
        # Power operation
        baseline_func = lambda: arr ** 2
        underscorec_func = lambda: power_2_underscore(arr)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "numpy_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Power"))
    
    return results

def run_array_comparison_benchmarks():
    """Benchmark NumPy array comparison operations."""
    runner = BenchmarkRunner(iterations=10000)
    data = create_benchmark_data()
    results = []
    
    print(f"\n🔍 NumPy Array Comparison Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('small_array', data['small_array']),
        ('medium_array', data['medium_array']),
        ('2d_small', data['2d_small']),
    ]
    
    for name, arr in test_cases:
        print(f"\nArray: {name} ({arr.size:,} elements)")
        
        # Pre-define UnderscoreC expressions
        gt_05_underscore = __ > 0.5
        eq_05_underscore = __ == 0.5
        
        # Greater than
        baseline_func = lambda: arr > 0.5
        underscorec_func = lambda: gt_05_underscore(arr)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "numpy_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Greater Than"))
        
        # Equality
        baseline_func = lambda: arr == 0.5
        underscorec_func = lambda: eq_05_underscore(arr)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "numpy_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Equality"))
    
    return results

def run_complex_expression_benchmarks():
    """Benchmark complex NumPy expressions.""" 
    runner = BenchmarkRunner(iterations=5000)
    data = create_benchmark_data()
    results = []
    
    print(f"\n🧮 Complex NumPy Expression Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('medium_array', data['medium_array']),
        ('2d_medium', data['2d_medium']),
    ]
    
    for name, arr in test_cases:
        print(f"\nArray: {name} ({arr.size:,} elements)")
        
        # Pre-define UnderscoreC expressions
        complex_arith_underscore = (__ * 2 + 1) ** 2 - __
        boolean_expr_underscore = (__ > 0.3) & (__ < 0.7)
        
        # Complex arithmetic expression
        baseline_func = lambda: (arr * 2 + 1) ** 2 - arr
        underscorec_func = lambda: complex_arith_underscore(arr)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "numpy_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Complex Arithmetic"))
        
        # Expression with comparisons
        baseline_func = lambda: (arr > 0.3) & (arr < 0.7)
        underscorec_func = lambda: boolean_expr_underscore(arr)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "numpy_native", "underscorec"  
        )
        results.append(result)
        print(format_benchmark_results(result, "Boolean Expression"))
    
    return results

def run_multi_reference_benchmarks():
    """Benchmark multi-reference expressions (__ op __)."""
    runner = BenchmarkRunner(iterations=8000)
    data = create_benchmark_data()
    results = []
    
    print(f"\n🔗 Multi-Reference Expression Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('small_array', data['small_array']),
        ('medium_array', data['medium_array']),
    ]
    
    for name, arr in test_cases:
        print(f"\nArray: {name} ({arr.size:,} elements)")
        
        # Pre-define UnderscoreC expressions
        self_add_underscore = __ + __
        self_mul_underscore = __ * __
        complex_multi_underscore = (__ + __) * (__ - __)
        
        # Self addition (arr + arr)
        baseline_func = lambda: arr + arr
        underscorec_func = lambda: self_add_underscore(arr)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "numpy_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Self Addition"))
        
        # Self multiplication (arr * arr)  
        baseline_func = lambda: arr * arr
        underscorec_func = lambda: self_mul_underscore(arr)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "numpy_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Self Multiplication"))
        
        # Complex multi-reference
        baseline_func = lambda: (arr + arr) * (arr - arr)
        underscorec_func = lambda: complex_multi_underscore(arr)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "numpy_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Complex Multi-Reference"))
    
    return results

def run_dtype_optimization_benchmarks():
    """Benchmark performance across different dtypes."""
    runner = BenchmarkRunner(iterations=10000)
    data = create_benchmark_data()
    results = []
    
    print(f"\n🎯 Data Type Optimization Benchmarks")
    print("-" * 50)
    
    # Test different data types
    test_arrays = {
        'int32': np.random.randint(1, 100, 10000).astype(np.int32),
        'int64': np.random.randint(1, 100, 10000).astype(np.int64),
        'float32': np.random.rand(10000).astype(np.float32),
        'float64': np.random.rand(10000).astype(np.float64),
    }
    
    for dtype_name, arr in test_arrays.items():
        print(f"\nData type: {dtype_name} ({arr.size:,} elements)")
        
        # Pre-define UnderscoreC expression
        add_10_underscore = __ + 10
        
        # Simple arithmetic
        baseline_func = lambda: arr + 10
        underscorec_func = lambda: add_10_underscore(arr)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "numpy_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, f"{dtype_name.title()} Addition"))
    
    return results

def main():
    """Run all NumPy integration benchmarks."""
    if not HAS_NUMPY:
        print("❌ NumPy not available - cannot run NumPy benchmarks")
        return []
        
    print("🔢 UnderscoreC NumPy Integration Performance Benchmarks")
    print("=" * 70)
    
    all_results = []
    
    # Run all benchmark categories
    all_results.extend(run_array_arithmetic_benchmarks())
    all_results.extend(run_array_comparison_benchmarks())
    all_results.extend(run_complex_expression_benchmarks()) 
    all_results.extend(run_multi_reference_benchmarks())
    all_results.extend(run_dtype_optimization_benchmarks())
    
    # Print overall summary
    print_benchmark_summary(all_results, "NumPy Integration")
    
    return all_results

if __name__ == "__main__":
    main()
