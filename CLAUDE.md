# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UnderscoreC is a C-based functional programming library for Python that provides `__` (underscore) placeholder syntax. It integrates deeply with NumPy, PyTorch, and Pandas through C/C++ extensions for optimized performance. The library supports function composition, method calls, and mathematical operations with smart type detection.

## Development Commands

### Setup and Installation
```bash
# Install dependencies and set up development environment
uv sync

# Build C extension for development (required after C++ changes)
uv run python setup.py build_ext --inplace

# Verify installation
uv run python -c "from underscorec import __; print('Setup successful!')"
```

### Testing
```bash
# Run all tests with coverage
uv run pytest

# Run specific test modules
uv run pytest tests/test_core_operations.py
uv run pytest tests/test_numpy_integration.py
uv run pytest tests/test_torch_integration.py

# Run tests excluding slow benchmarks
uv run pytest -m "not slow"

# Generate HTML coverage report
uv run pytest --cov-report=html

# Run modular test suite (alternative runner)
uv run python tests/run_modular_tests.py
```

### Benchmarking
```bash
# Run performance benchmarks
uv run python benchmarks/run_modular_benchmarks.py

# Run specific benchmark types
uv run python benchmarks/bench_numpy_integration.py
uv run python benchmarks/bench_torch_integration.py
```

### Building and Publishing
```bash
# Build source distribution and wheels
uv build

# Publish to PyPI (requires credentials)
uv publish

# Publish to Test PyPI
uv publish --repository testpypi
```

## Code Architecture

### Core C++ Extension Structure
The project uses a modular C++ extension design with clear separation of concerns:

- **`underscorec.cpp`**: Main extension module with unified functionality
- **`underscorec_types.h`**: Shared type definitions and enums (UnderscoreOperation, UnderscoreObject)
- **`underscorec_numpy.h/.cpp`**: NumPy integration with cached ufuncs for performance
- **`underscorec_torch.h/.cpp`**: PyTorch tensor operations and GPU acceleration

### Key Components

#### UnderscoreObject Structure (`underscorec_types.h:51`)
The core data structure supporting:
- Basic operations (identity, arithmetic, comparison, bitwise)
- Multi-reference expressions (`__ OP __`)
- Method calls with args/kwargs (`__.method(args)`)
- Function composition chains (`__ >> func`)

#### Deep Copy System (`underscorec.cpp:23`)
Prevents shallow copy bugs in composition chains by recursively copying all expression nodes with proper reference counting.

#### Type Detection and Dispatching
Smart routing system that automatically detects input types (NumPy arrays, PyTorch tensors, native Python objects) and routes to optimized implementations.

### Integration Modules

#### NumPy Integration (`underscorec_numpy.cpp`)
- Cached ufuncs system for performance (`initialize_numpy_ufuncs`)
- Vectorized operations on arrays
- Support for all NumPy dtypes and broadcasting

#### PyTorch Integration (`underscorec_torch.cpp`)
- CPU and GPU tensor operations
- AutoGrad compatibility for gradient computation
- MPS (Apple Silicon) acceleration support
- Memory-efficient tensor chaining

## File Organization

- **`src/underscorec/`**: Core C++ extension source code
- **`tests/`**: Comprehensive test suite with fixtures and parametrized tests
- **`benchmarks/`**: Performance evaluation suite comparing against native operations  
- **`examples/`**: Usage examples and correct implementation patterns
- **`archive/`**: Historical performance analysis and research
- **`debug/`**: Development debugging tools and analysis scripts
- **`anecdotes/`**: Performance insights and implementation decisions

## Testing Strategy

### Test Structure (`tests/conftest.py`)
- Fixtures for NumPy/PyTorch data with conditional skipping
- Parametrized test data for comprehensive coverage
- Binary operations, comparison operations, and method call test data
- Conditional test markers (`numpy_only`, `torch_only`, `slow_test`)

### Coverage Requirements
- Minimum 95% coverage enforced (`pyproject.toml:45`)
- Branch coverage enabled for thorough testing
- HTML reports generated in `htmlcov/`

## Build System Details

### C++ Compilation (`setup.py`)
- C++17 standard required for PyTorch compatibility
- Automatic detection of PyTorch include paths and libraries
- NumPy C API integration with proper include directories
- Multi-source compilation (main + NumPy + PyTorch modules)

### Dependencies
- **Runtime**: `numpy>=2.2.6`, `torch>=2.0.0`, `pandas>=2.3.1`
- **Build**: `setuptools>=61.0`, `wheel`, `numpy`, `torch`
- **Development**: `pytest>=7.0.0`, `pytest-cov>=6.2.1`, `coverage>=7.10.1`

## Performance Considerations

### Optimization Strategies
- Cached ufuncs for NumPy operations to avoid lookup overhead
- Smart type detection to route to fastest implementation
- Deep copy system prevents reference bugs while maintaining performance
- C-level composition chains reduce Python call overhead

### Benchmark Methodology (`benchmarks/README.md:72`)
- Multiple iterations with warmup periods
- GPU synchronization for accurate PyTorch timing
- Various data sizes (1K to 1M+ elements) for scaling analysis
- Comparison against native library operations and lambda functions

## Common Development Patterns

### Adding New Operations
1. Add operation enum to `UnderscoreOperation` in `underscorec_types.h:17`
2. Implement operation handling in main evaluation loop
3. Add NumPy/PyTorch specific optimizations in respective modules
4. Create comprehensive tests with multiple data types
5. Add benchmark comparisons for performance validation

### Debugging C Extension Issues
- Use debug tools in `debug/` directory for step-by-step analysis
- Enable verbose compilation with `setup.py build_ext --inplace --debug`
- Reference counting debugging with `Py_XINCREF`/`Py_XDECREF` tracking
- Memory leak detection through systematic testing

## Important Implementation Notes

### Reference Counting
All PyObject* fields in UnderscoreObject require proper reference management. The deep_copy system handles this automatically for composition chains.

### Multi-Reference Operations
Operations like `__ + __` create special multi-reference expressions that are resolved when called with input data.

### GPU Memory Management
PyTorch GPU operations require careful synchronization and memory management, especially with MPS backend on Apple Silicon.