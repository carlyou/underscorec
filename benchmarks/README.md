# UnderscoreC Benchmarks

This directory contains comprehensive performance benchmarks comparing UnderscoreC against native Python operations and popular libraries.

## Overview

The benchmark suite evaluates UnderscoreC performance across different use cases:

- **NumPy Integration**: Array operations, vectorization, mathematical expressions
- **PyTorch Integration**: Tensor operations, gradient computation, GPU/CPU performance  
- **Pandas Integration**: Series/DataFrame operations, data manipulation
- **Functional Programming**: Map/filter operations, composition patterns

## Benchmark Scripts

### 1. `numpy_benchmarks.py`
Tests UnderscoreC against pure NumPy operations:
- Simple arithmetic (addition, multiplication, power)
- Complex compositions like `(x * 2 + 1) ** 2`
- Comparison operations (`>`, `==`, etc.)
- Functional programming patterns with NumPy arrays
- Performance across different array sizes (1K, 10K, 100K, 1M elements)

### 2. `pytorch_benchmarks.py`  
Evaluates PyTorch tensor integration:
- CPU vs GPU performance comparison
- Gradient computation benchmarks
- Complex tensor operations
- Memory efficiency with Apple Silicon MPS support
- AutoGrad compatibility testing

### 3. `pandas_benchmarks.py`
Compares Pandas Series/DataFrame operations:
- Series arithmetic and comparisons
- DataFrame column operations
- Apply vs direct operation performance
- Data transformation pipelines
- Mixed data type handling

### 4. `functional_benchmarks.py`
Tests functional programming patterns:
- Map operations vs lambda functions vs partial
- Filter operations and combinations
- List comprehension comparisons
- Complex function composition chains
- Performance with different data sizes

### 5. `run_all_benchmarks.py`
Comprehensive benchmark runner:
- Executes all benchmark suites
- Generates summary performance reports
- Saves results to timestamped files
- Provides performance insights and recommendations

## Running Benchmarks

### Individual Benchmarks
```bash
# Run specific benchmark
uv run python benchmarks/numpy_benchmarks.py
uv run python benchmarks/pytorch_benchmarks.py
uv run python benchmarks/pandas_benchmarks.py
uv run python benchmarks/functional_benchmarks.py
```

### Full Benchmark Suite
```bash
# Run all benchmarks with summary report
uv run python benchmarks/run_all_benchmarks.py
```

## Benchmark Methodology

### Timing
- Each operation is run multiple times (100-1000 iterations)
- Warmup iterations to stabilize performance
- Average execution time calculated in milliseconds
- GPU synchronization points for accurate PyTorch timing

### Data Sizes
- **Small**: 1K elements - tests overhead and function call costs
- **Medium**: 10K elements - typical data processing workloads  
- **Large**: 100K+ elements - heavy computational workloads
- **2D Arrays**: Various matrix sizes for multidimensional operations

### Metrics Reported
- **Execution Time**: Average time per operation in milliseconds
- **Speedup Factor**: Ratio of native operation time to UnderscoreC time
- **Memory Usage**: Implicit through operation complexity
- **Error Handling**: Graceful degradation for unsupported operations

## Expected Performance Characteristics

### Where UnderscoreC Excels
- **Complex Compositions**: Multi-step operations benefit from C-level optimization
- **Functional Patterns**: Cleaner syntax without performance penalty
- **Type Dispatching**: Smart routing to optimized library functions
- **GPU Operations**: Efficient tensor operation chaining

### Where Native Approaches May Be Faster  
- **Simple Operations**: Single arithmetic operations may have call overhead
- **Very Small Data**: Function call costs dominate for tiny datasets
- **Specialized Optimizations**: Highly tuned library-specific operations

## Performance Tips

1. **Use Composition**: Complex expressions like `(x * 2 + 1) ** 2` benefit most
2. **Leverage Type Detection**: Let UnderscoreC automatically choose optimal paths
3. **Batch Operations**: Work with larger datasets to amortize function call costs
4. **GPU Acceleration**: PyTorch GPU operations show significant improvements

## System Dependencies

- **NumPy**: Required for array operation benchmarks
- **PyTorch**: Required for tensor and GPU benchmarks  
- **Pandas**: Required for data manipulation benchmarks
- **Python 3.8+**: Required for all benchmarks

## Interpreting Results

### Speedup Values
- `> 1.0x`: UnderscoreC is faster than native approach
- `< 1.0x`: Native approach is faster than UnderscoreC  
- `~1.0x`: Performance is roughly equivalent

### Typical Results
Results vary by system, but typical patterns:
- NumPy: 0.8x - 2.5x speedup depending on operation complexity
- PyTorch: 0.9x - 3.0x speedup, higher on GPU workloads
- Pandas: 0.7x - 2.0x speedup for Series operations
- Functional: 0.5x - 1.8x compared to lambda/comprehensions

Results are highly dependent on:
- System architecture (x86_64 vs ARM)
- Available GPU acceleration  
- Memory bandwidth and CPU cache
- Python version and library versions
- Dataset size and operation complexity