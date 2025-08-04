#!/usr/bin/env python3
"""
PyTorch Integration Performance Benchmarks

Benchmarks UnderscoreC PyTorch integration against native PyTorch operations.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    print("❌ PyTorch not available - skipping PyTorch benchmarks")
    sys.exit(0)

from underscorec import __
from conftest import BenchmarkRunner, create_benchmark_data, format_benchmark_results, print_benchmark_summary

def run_tensor_arithmetic_benchmarks():
    """Benchmark PyTorch tensor arithmetic operations.""" 
    runner = BenchmarkRunner(iterations=5000)  # Fewer iterations for tensor ops
    data = create_benchmark_data()
    results = []
    
    print("\n🔥 PyTorch Tensor Arithmetic Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('torch_small', data['torch_small']),
        ('torch_medium', data['torch_medium']),
        ('torch_2d', data['torch_2d']),
    ]
    
    for name, tensor in test_cases:
        print(f"\nTensor: {name} ({tensor.numel():,} elements, shape: {tensor.shape})")
        
        # Pre-define UnderscoreC expressions to avoid reconstruction overhead
        add_5_underscore = __ + 5.0
        mul_2_5_underscore = __ * 2.5
        div_3_underscore = __ / 3.0
        
        # Addition
        baseline_func = lambda: tensor + 5.0
        underscorec_func = lambda: add_5_underscore(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Addition"))
        
        # Multiplication
        baseline_func = lambda: tensor * 2.5 
        underscorec_func = lambda: mul_2_5_underscore(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Multiplication"))
        
        # Division
        baseline_func = lambda: tensor / 3.0
        underscorec_func = lambda: div_3_underscore(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"  
        )
        results.append(result)
        print(format_benchmark_results(result, "Division"))
    
    return results

def run_tensor_comparison_benchmarks():
    """Benchmark PyTorch tensor comparison operations."""
    runner = BenchmarkRunner(iterations=5000)
    data = create_benchmark_data()
    results = []
    
    print(f"\n🔍 PyTorch Tensor Comparison Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('torch_small', data['torch_small']),
        ('torch_medium', data['torch_medium']),
    ]
    
    for name, tensor in test_cases:
        print(f"\nTensor: {name} ({tensor.numel():,} elements)")
        
        # Pre-define UnderscoreC expressions
        gt_0_underscore = __ > 0.0
        lt_1_underscore = __ < 1.0
        eq_0_underscore = __ == 0.0
        
        # Greater than
        baseline_func = lambda: tensor > 0.0
        underscorec_func = lambda: gt_0_underscore(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Greater Than"))
        
        # Less than
        baseline_func = lambda: tensor < 1.0
        underscorec_func = lambda: lt_1_underscore(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Less Than"))
        
        # Equality
        baseline_func = lambda: tensor == 0.0
        underscorec_func = lambda: eq_0_underscore(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Equality"))
    
    return results

def run_complex_tensor_expression_benchmarks():
    """Benchmark complex PyTorch tensor expressions."""
    runner = BenchmarkRunner(iterations=3000)
    data = create_benchmark_data()
    results = []
    
    print(f"\n🧮 Complex PyTorch Expression Benchmarks") 
    print("-" * 50)
    
    test_cases = [
        ('torch_medium', data['torch_medium']),
        ('torch_2d', data['torch_2d']),
    ]
    
    for name, tensor in test_cases:
        print(f"\nTensor: {name} ({tensor.numel():,} elements)")
        
        # Pre-define UnderscoreC expressions
        complex_arith_underscore = (__ * 2 + 1) ** 2 - __
        boolean_expr_underscore = (__ > -0.5) & (__ < 0.5)
        
        # Complex arithmetic expression
        baseline_func = lambda: (tensor * 2 + 1) ** 2 - tensor
        underscorec_func = lambda: complex_arith_underscore(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Complex Arithmetic"))
        
        # Expression with comparisons
        baseline_func = lambda: (tensor > -0.5) & (tensor < 0.5)
        underscorec_func = lambda: boolean_expr_underscore(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Boolean Expression"))
    
    return results

def run_tensor_multi_reference_benchmarks():
    """Benchmark tensor multi-reference expressions (__ op __)."""
    runner = BenchmarkRunner(iterations=4000)
    data = create_benchmark_data()
    results = []
    
    print(f"\n🔗 Tensor Multi-Reference Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('torch_small', data['torch_small']),
        ('torch_medium', data['torch_medium']),
    ]
    
    for name, tensor in test_cases:
        print(f"\nTensor: {name} ({tensor.numel():,} elements)")
        
        # Self addition (tensor + tensor)
        baseline_func = lambda: tensor + tensor
        underscorec_func = lambda: (__ + __)(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Self Addition"))
        
        # Self multiplication (tensor * tensor)
        baseline_func = lambda: tensor * tensor
        underscorec_func = lambda: (__ * __)(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Self Multiplication"))
    
    return results

def run_tensor_property_access_benchmarks():
    """Benchmark tensor property access performance."""
    runner = BenchmarkRunner(iterations=50000)  # Property access is very fast
    data = create_benchmark_data()
    results = []
    
    print(f"\n📏 Tensor Property Access Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('torch_small', data['torch_small']),
        ('torch_2d', data['torch_2d']),
    ]
    
    for name, tensor in test_cases:
        print(f"\nTensor: {name} (shape: {tensor.shape})")
        
        # Shape access
        baseline_func = lambda: tensor.shape
        underscorec_func = lambda: (__.shape)(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Shape Access"))
        
        # Dtype access
        baseline_func = lambda: tensor.dtype
        underscorec_func = lambda: (__.dtype)(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Dtype Access"))
    
    return results

def run_tensor_method_call_benchmarks():
    """Benchmark tensor method call performance."""
    runner = BenchmarkRunner(iterations=10000)
    data = create_benchmark_data()
    results = []
    
    print(f"\n📞 Tensor Method Call Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('torch_small', data['torch_small']),
        ('torch_medium', data['torch_medium']),
    ]
    
    for name, tensor in test_cases:
        print(f"\nTensor: {name} ({tensor.numel():,} elements)")
        
        # Size method
        baseline_func = lambda: tensor.size()
        underscorec_func = lambda: (__.size())(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Size Method"))
        
        # Contiguous method
        baseline_func = lambda: tensor.contiguous()
        underscorec_func = lambda: (__.contiguous())(tensor)
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_native", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Contiguous Method"))
    
    return results

def run_cuda_benchmarks():
    """Benchmark CUDA tensor operations if available."""
    if not torch.cuda.is_available():
        print("\n🚫 CUDA not available - skipping GPU benchmarks")
        return []
        
    runner = BenchmarkRunner(iterations=2000)  # Fewer iterations for GPU
    data = create_benchmark_data()
    results = []
    
    print(f"\n🚀 CUDA Tensor Benchmarks")
    print("-" * 50)
    
    if 'torch_cuda_small' in data:
        tensor = data['torch_cuda_small']
        print(f"\nCUDA Tensor: ({tensor.numel():,} elements)")
        
        # Ensure proper CUDA synchronization for timing
        def sync_cuda_func(func):
            def wrapper():
                result = func()
                torch.cuda.synchronize()  # Ensure completion
                return result
            return wrapper
        
        # Addition on GPU
        baseline_func = sync_cuda_func(lambda: tensor + 5.0)
        underscorec_func = sync_cuda_func(lambda: (__ + 5.0)(tensor))
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_cuda", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "CUDA Addition"))
        
        # Multiplication on GPU
        baseline_func = sync_cuda_func(lambda: tensor * 2.5)
        underscorec_func = sync_cuda_func(lambda: (__ * 2.5)(tensor))
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "torch_cuda", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "CUDA Multiplication"))
    
    return results

def main():
    """Run all PyTorch integration benchmarks."""
    if not HAS_TORCH:
        print("❌ PyTorch not available - cannot run PyTorch benchmarks")
        return []
        
    print("🔥 UnderscoreC PyTorch Integration Performance Benchmarks")
    print("=" * 70)
    
    all_results = []
    
    # Run all benchmark categories
    all_results.extend(run_tensor_arithmetic_benchmarks())
    all_results.extend(run_tensor_comparison_benchmarks())
    all_results.extend(run_complex_tensor_expression_benchmarks())
    all_results.extend(run_tensor_multi_reference_benchmarks())
    all_results.extend(run_tensor_property_access_benchmarks())
    all_results.extend(run_tensor_method_call_benchmarks())
    all_results.extend(run_cuda_benchmarks())
    
    # Print overall summary
    print_benchmark_summary(all_results, "PyTorch Integration")
    
    return all_results

if __name__ == "__main__":
    main()
