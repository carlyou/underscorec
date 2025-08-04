#!/usr/bin/env python3
"""
Core Operations Performance Benchmarks

Benchmarks basic UnderscoreC operations against equivalent Python operations.
"""

import sys
import os
import operator
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from underscorec import __
from conftest import BenchmarkRunner, create_benchmark_data, format_benchmark_results, print_benchmark_summary

def run_multi_approach_comparison(runner, operation_name, test_data, approaches):
    """Run multiple approaches against UnderscoreC and return results."""
    results = []
    underscorec_func = approaches.pop('underscorec')  # Remove underscorec to compare others against it
    
    print(f"  {operation_name}:")
    for approach_name, approach_func in approaches.items():
        result = runner.compare_benchmarks(
            approach_func, underscorec_func,
            approach_name, "underscorec"
        )
        results.append(result)
        
        if result:
            baseline = result['baseline']
            test_result = result['test']
            speedup = result['speedup']
            symbol = "🚀" if speedup > 1.0 else "🐌"
            print(f"    vs {approach_name}: {speedup:.2f}x {symbol} ({baseline['mean']:.3f}ms vs {test_result['mean']:.3f}ms)")
        else:
            print(f"    vs {approach_name}: FAILED")
    
    return results

def run_arithmetic_benchmarks():
    """Benchmark arithmetic operations."""
    runner = BenchmarkRunner(iterations=2000)
    data = create_benchmark_data()
    results = []
    
    print("\n🧮 Arithmetic Operations Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('list_int_small', data['list_int_small']),
        ('list_int_medium', data['list_int_medium']),
        ('list_float_small', data['list_float_small']),
        ('list_float_medium', data['list_float_medium']),
    ]
    
    for name, test_data in test_cases:
        print(f"\nDataset: {name} ({len(test_data):,} elements)")
        
        # Addition - Pre-define reusable functions
        from functools import partial
        
        # Pre-define functions to avoid reconstruction overhead
        add_5_lambda = lambda x: x + 5
        add_5_partial = partial(operator.add, 5)
        add_5_underscore = __ + 5
        
        addition_approaches = {
            'list_comprehension': lambda: [x + 5 for x in test_data],
            'lambda+map': lambda: list(map(add_5_lambda, test_data)),
            'operator+partial': lambda: list(map(add_5_partial, test_data)),
            'underscorec': lambda: list(map(add_5_underscore, test_data))
        }
        results.extend(run_multi_approach_comparison(runner, "Addition", test_data, addition_approaches))
        
        # Multiplication - Pre-define reusable functions
        mul_3_lambda = lambda x: x * 3
        mul_3_partial = partial(operator.mul, 3)
        mul_3_underscore = __ * 3
        
        multiplication_approaches = {
            'list_comprehension': lambda: [x * 3 for x in test_data],
            'lambda+map': lambda: list(map(mul_3_lambda, test_data)),
            'operator+partial': lambda: list(map(mul_3_partial, test_data)),
            'underscorec': lambda: list(map(mul_3_underscore, test_data))
        }
        results.extend(run_multi_approach_comparison(runner, "Multiplication", test_data, multiplication_approaches))
        
        # Complex expression - Pre-define reusable functions
        complex_lambda = lambda x: (x * 2 + 1) ** 2
        complex_underscore = (__ * 2 + 1) ** 2
        
        complex_approaches = {
            'list_comprehension': lambda: [(x * 2 + 1) ** 2 for x in test_data],
            'lambda+map': lambda: list(map(complex_lambda, test_data)),
            'underscorec': lambda: list(map(complex_underscore, test_data))
        }
        results.extend(run_multi_approach_comparison(runner, "Complex Expression", test_data, complex_approaches))
    
    return results

def run_comparison_benchmarks():
    """Benchmark comparison operations."""
    runner = BenchmarkRunner(iterations=2000)
    data = create_benchmark_data()
    results = []
    
    print(f"\n🔍 Comparison Operations Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('list_int_small', data['list_int_small']),
        ('list_int_medium', data['list_int_medium']),
        ('list_float_small', data['list_float_small']),
        ('list_float_medium', data['list_float_medium']),
    ]
    
    for name, test_data in test_cases:
        print(f"\nDataset: {name} ({len(test_data):,} elements)")
        
        # Greater than - Pre-define reusable functions
        from functools import partial
        
        gt_500_lambda = lambda x: x > 500
        gt_500_partial = partial(operator.gt, 500)
        gt_500_underscore = __ > 500
        
        gt_approaches = {
            'list_comprehension': lambda: [x > 500 for x in test_data],
            'lambda+map': lambda: list(map(gt_500_lambda, test_data)),
            'operator+partial': lambda: list(map(gt_500_partial, test_data)),
            'underscorec': lambda: list(map(gt_500_underscore, test_data))
        }
        results.extend(run_multi_approach_comparison(runner, "Greater Than", test_data, gt_approaches))
        
        # Less than or equal - Pre-define reusable functions
        le_100_lambda = lambda x: x <= 100
        le_100_partial = partial(operator.le, 100)  # Fixed: should be le, not ge
        le_100_underscore = __ <= 100
        
        le_approaches = {
            'list_comprehension': lambda: [x <= 100 for x in test_data],
            'lambda+map': lambda: list(map(le_100_lambda, test_data)),
            'operator+partial': lambda: list(map(le_100_partial, test_data)),
            'underscorec': lambda: list(map(le_100_underscore, test_data))
        }
        results.extend(run_multi_approach_comparison(runner, "Less Than or Equal", test_data, le_approaches))
        
        # Equality - Pre-define reusable functions
        eq_500_lambda = lambda x: x == 500
        eq_500_partial = partial(operator.eq, 500)
        eq_500_underscore = __ == 500
        
        eq_approaches = {
            'list_comprehension': lambda: [x == 500 for x in test_data],
            'lambda+map': lambda: list(map(eq_500_lambda, test_data)),
            'operator+partial': lambda: list(map(eq_500_partial, test_data)),
            'underscorec': lambda: list(map(eq_500_underscore, test_data))
        }
        results.extend(run_multi_approach_comparison(runner, "Equality", test_data, eq_approaches))
    
    return results

def run_function_composition_benchmarks():
    """Benchmark function composition."""
    runner = BenchmarkRunner(iterations=1000)
    data = create_benchmark_data()
    results = []
    
    print(f"\n🔗 Function Composition Benchmarks")
    print("-" * 50)
    
    test_cases = [
        ('list_int_small', data['list_int_small']),
        ('list_int_medium', data['list_int_medium']),
    ]
    
    for name, test_data in test_cases:
        print(f"\nDataset: {name} ({len(test_data):,} elements)")
        
        # Multi-step composition - Pre-define reusable functions
        multi_step_underscore = __ - 500 >> abs >> str
        
        baseline_func = lambda: [str(abs(x - 500)) for x in test_data]
        underscorec_func = lambda: list(map(multi_step_underscore, test_data))
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "list_comprehension", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Multi-step Composition"))
        
        # Arithmetic composition - Pre-define reusable functions
        arithmetic_underscore = __ * 2 + 10
        
        baseline_func = lambda: [x * 2 + 10 for x in test_data]
        underscorec_func = lambda: list(map(arithmetic_underscore, test_data))
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "list_comprehension", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Arithmetic Composition"))
        
        # Complex composition with functions - Pre-define reusable functions
        max_0 = lambda x: max(x, 0)
        min_1000 = lambda x: min(x, 1000)
        complex_underscore = __ >> max_0 >> min_1000
        
        baseline_func = lambda: [min(max(x, 0), 1000) for x in test_data]
        underscorec_func = lambda: list(map(complex_underscore, test_data))
        
        result = runner.compare_benchmarks(
            baseline_func, underscorec_func,
            "list_comprehension", "underscorec"
        )
        results.append(result)
        print(format_benchmark_results(result, "Function Composition"))
    
    return results

def run_method_call_benchmarks():
    """Benchmark method calls."""
    runner = BenchmarkRunner(iterations=1000) 
    data = create_benchmark_data()
    results = []
    
    print(f"\n📞 Method Call Benchmarks")
    print("-" * 50)
    
    # String operations
    test_strings = data['list_strings']
    
    print(f"\nDataset: strings ({len(test_strings):,} elements)")
    
    # String upper - Pre-define reusable functions
    upper_underscore = __.upper()
    
    baseline_func = lambda: [s.upper() for s in test_strings]
    underscorec_func = lambda: list(map(upper_underscore, test_strings))
    
    result = runner.compare_benchmarks(
        baseline_func, underscorec_func,
        "list_comprehension", "underscorec"
    )
    results.append(result)
    print(format_benchmark_results(result, "String Upper"))
    
    # String replace - Pre-define reusable functions
    replace_underscore = __.replace("item", "element")
    
    baseline_func = lambda: [s.replace("item", "element") for s in test_strings]
    underscorec_func = lambda: list(map(replace_underscore, test_strings))
    
    result = runner.compare_benchmarks(
        baseline_func, underscorec_func,
        "list_comprehension", "underscorec"
    )
    results.append(result)
    print(format_benchmark_results(result, "String Replace"))
    
    # String split - Pre-define reusable functions
    test_split_strings = [f"word_{i} another_{i} final_{i}" for i in range(1000)]
    split_underscore = __.split()
    
    baseline_func = lambda: [s.split() for s in test_split_strings]
    underscorec_func = lambda: list(map(split_underscore, test_split_strings))
    
    result = runner.compare_benchmarks(
        baseline_func, underscorec_func,
        "list_comprehension", "underscorec"
    )
    results.append(result)
    print(format_benchmark_results(result, "String Split"))
    
    return results

def main():
    """Run all core operations benchmarks."""
    print("🚀 UnderscoreC Core Operations Performance Benchmarks")
    print("=" * 70)
    
    all_results = []
    
    # Run all benchmark categories
    all_results.extend(run_arithmetic_benchmarks())
    all_results.extend(run_comparison_benchmarks()) 
    all_results.extend(run_function_composition_benchmarks())
    all_results.extend(run_method_call_benchmarks())
    
    # Print overall summary
    print_benchmark_summary(all_results, "Core Operations")
    
    return all_results

if __name__ == "__main__":
    main()