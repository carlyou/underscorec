#!/usr/bin/env python3
"""
Modular Benchmark Runner

Runs the new modular benchmark framework with comprehensive analysis.
"""

import sys
import os
import time
from datetime import datetime

# Add src to path for UnderscoreC imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_benchmark_module(module_name):
    """Import and run a benchmark module."""
    print(f"🚀 Running {module_name}...")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Import the module
        module = __import__(module_name)
        
        # Run the main function
        if hasattr(module, 'main'):
            results = module.main()
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"✅ {module_name} completed in {duration:.2f} seconds\n")
            return True, results, duration
        else:
            print(f"❌ {module_name} has no main() function")
            return False, [], time.time() - start_time
            
    except ImportError as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"⏭️  Skipping {module_name}: {e}")
        return False, [], duration
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"❌ Error running {module_name}: {e}")
        return False, [], duration

def generate_comprehensive_summary(all_results, module_results):
    """Generate comprehensive benchmark summary."""
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE BENCHMARK REPORT")
    print("=" * 80)
    
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total benchmark modules: {len(module_results)}")
    
    successful_modules = sum(1 for success, _, _ in module_results.values() if success)
    failed_modules = len(module_results) - successful_modules
    
    print(f"Successful modules: {successful_modules}")
    print(f"Failed/Skipped modules: {failed_modules}")
    
    total_time = sum(duration for _, _, duration in module_results.values())
    print(f"Total execution time: {total_time:.2f} seconds")
    
    print("\n📋 Module Results:")
    print("-" * 40)
    
    for module_name, (success, results, duration) in module_results.items():
        status = "✅ PASS" if success else "❌ FAIL/SKIP"
        test_count = len(results) if isinstance(results, list) else 0
        print(f"{module_name:<25} {status} ({test_count} tests, {duration:.2f}s)")
    
    # Aggregate performance analysis
    if all_results:
        print("\n🔍 Performance Analysis:")
        print("-" * 30)
        
        speedups = []
        categories = {}
        
        for result in all_results:
            if result and 'speedup' in result:
                speedup = result['speedup']
                speedups.append(speedup)
                
                # Categorize by baseline name
                baseline_name = result.get('baseline', {}).get('name', 'unknown')
                if baseline_name not in categories:
                    categories[baseline_name] = []
                categories[baseline_name].append(speedup)
        
        if speedups:
            import statistics
            
            total_tests = len(speedups)
            faster_tests = sum(1 for s in speedups if s > 1.0)
            
            avg_speedup = statistics.mean(speedups)
            max_speedup = max(speedups)
            min_speedup = min(speedups)
            
            print(f"📊 Total benchmark comparisons: {total_tests}")
            print(f"🚀 Faster than baseline: {faster_tests}/{total_tests} ({faster_tests/total_tests*100:.1f}%)")
            print(f"📈 Average speedup: {avg_speedup:.2f}x")
            print(f"🔝 Best speedup: {max_speedup:.2f}x")
            print(f"🔽 Worst speedup: {min_speedup:.2f}x")
            
            # Performance distribution
            excellent = sum(1 for s in speedups if s > 1.5)
            good = sum(1 for s in speedups if 1.1 < s <= 1.5)
            acceptable = sum(1 for s in speedups if 0.9 <= s <= 1.1)
            slow = sum(1 for s in speedups if s < 0.9)
            
            print(f"\n📋 Performance Distribution:")
            print(f"  Excellent (>1.5x): {excellent} ({excellent/total_tests*100:.1f}%)")
            print(f"  Good (1.1-1.5x): {good} ({good/total_tests*100:.1f}%)")
            print(f"  Acceptable (0.9-1.1x): {acceptable} ({acceptable/total_tests*100:.1f}%)")
            print(f"  Slow (<0.9x): {slow} ({slow/total_tests*100:.1f}%)")
            
            # Category breakdown
            if categories:
                print(f"\n📊 Performance by Category:")
                for category, cat_speedups in categories.items():
                    if cat_speedups:
                        cat_avg = statistics.mean(cat_speedups)
                        cat_faster = sum(1 for s in cat_speedups if s > 1.0)
                        print(f"  {category}: {cat_avg:.2f}x avg ({cat_faster}/{len(cat_speedups)} faster)")
    
    print("\n💡 Performance Notes:")
    print("  • Speedup > 1.0x means UnderscoreC is faster than baseline")
    print("  • Speedup < 1.0x means baseline approach is faster")
    print("  • Results may vary based on system performance and data size")
    print("  • Consider data size and operation complexity when interpreting results")

def save_results_to_file(all_results, module_results):
    """Save detailed benchmark results to file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"benchmark_results_modular_{timestamp}.txt"
    
    try:
        # Ensure results directory exists
        os.makedirs("benchmarks/results", exist_ok=True)
        filepath = f"benchmarks/results/{filename}"
        
        with open(filepath, 'w') as f:
            f.write(f"UnderscoreC Modular Benchmark Results - {datetime.now()}\n")
            f.write("=" * 80 + "\n\n")
            
            # Module summary
            f.write("Module Execution Summary:\n")
            f.write("-" * 30 + "\n")
            for module_name, (success, results, duration) in module_results.items():
                status = "SUCCESS" if success else "FAILED/SKIPPED"
                test_count = len(results) if isinstance(results, list) else 0
                f.write(f"{module_name}: {status} ({test_count} tests, {duration:.2f}s)\n")
            
            f.write("\n" + "=" * 80 + "\n\n")
            
            # Detailed results
            f.write("Detailed Benchmark Results:\n")
            f.write("-" * 30 + "\n")
            
            for result in all_results:
                if result and 'baseline' in result and 'test' in result:
                    baseline = result['baseline']
                    test = result['test']
                    speedup = result.get('speedup', 0)
                    
                    f.write(f"Comparison: {baseline['name']} vs {test['name']}\n")
                    f.write(f"  Baseline: {baseline['mean']:.3f}ms ± {baseline['stdev']:.3f}ms\n")
                    f.write(f"  Test: {test['mean']:.3f}ms ± {test['stdev']:.3f}ms\n")
                    f.write(f"  Speedup: {speedup:.2f}x\n")
                    f.write("-" * 40 + "\n")
        
        print(f"\n💾 Detailed results saved to {filepath}")
        return filepath
        
    except Exception as e:
        print(f"\n⚠️  Could not save results to file: {e}")
        return None

def main():
    """Main modular benchmark runner."""
    print("🏃 UnderscoreC Modular Benchmark Suite")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # List of modular benchmark modules to run
    benchmark_modules = [
        "bench_core_operations",
        "bench_numpy_integration", 
        "bench_torch_integration",
    ]
    
    module_results = {}
    all_results = []
    
    for module_name in benchmark_modules:
        success, results, duration = run_benchmark_module(module_name)
        module_results[module_name] = (success, results, duration)
        
        if success and isinstance(results, list):
            all_results.extend(results)
        
        # Add separator between modules
        print("\n" + "=" * 80 + "\n")
    
    # Generate comprehensive summary
    generate_comprehensive_summary(all_results, module_results)
    
    # Save results to file
    save_results_to_file(all_results, module_results)
    
    print(f"\n🎉 Benchmark suite completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return all_results, module_results

if __name__ == "__main__":
    main()
