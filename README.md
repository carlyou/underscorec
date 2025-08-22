# UnderscoreC

A C-based library focused on functional programming and mathematical computation, providing `__` (underscore) placeholder syntax for Python. Currently integrated with lower-level NumPy/PyTorch C/C++ extensions for optimized performance.

## Examples

### Mathematical Computing
```python
from underscorec import __
import numpy as np
import torch

arr = np.array([1, 2, 3, 4, 5])

# Create reusable mathematical expressions
normalize = (__ - __.mean()) / __.std()
result = normalize(arr)  # Normalized array

# Simple transformations
mul_add = __ * 2 + 1
result = mul_add(arr)

# PyTorch integration  
tensor = torch.tensor([1., 2., 3., 4., 5.])
tensor.apply_(__ * 2 + 1)

# Pipeline operators for immediate evaluation
result = 5 >> (__ * 2 + 1)  # 11 (reverse pipeline)
result = (__ * 2 + 1) >> 5  # 11 (forward pipeline)
```

### Method Calls and Attribute Access
```python
# String processing
process_text = __.strip().lower()
clean = process_text("  Hello World  ")  # "hello world"

# Attribute access
numel_2d = __.shape >> __[0] * __[1]
numel_2d(matrix)
```

### Function Composition and Pipeline Operators

The `>>` operator provides flexible composition and pipeline functionality with three distinct behaviors:

#### 1. Expression Composition (`expr >> expr` or `expr >> callable`)
```python
# Chain expressions for later evaluation
pipeline = (__ * 2) >> (__ - 5) >> abs
result = map(pipeline, data)  # Apply transformations in sequence

# Compose with built-in functions
text_processor = __.strip() >> __.split(',') >> len
length = text_processor("  Hello, World!  ")  # 2

# Compose with lambda functions
transform = (__ + 1) >> (lambda x: x * 2) >> str
result = transform(5)  # "12"
```

#### 2. Forward Pipeline (`expr >> data`)
```python
# Immediately evaluate expression with data (left-to-right)
result = (__ * 2 + 1) >> 5  # Evaluates to 11
result = __.upper() >> "hello"  # Evaluates to "HELLO"

# Useful for one-off transformations
processed = (__ - __.mean()) / __.std() >> np.array([1, 2, 3, 4, 5])
```

#### 3. Reverse Pipeline (`data >> expr`)
```python
# Immediately evaluate expression with data (right-to-left)
result = 5 >> (__ * 2 + 1)  # Evaluates to 11  
result = "hello" >> __.upper()  # Evaluates to "HELLO"

# Natural data flow for chaining operations
result = data >> (__ * 2) >> (__ + 1) >> (__ / 3)
```

**Performance Note**: Forward pipelines (`expr >> expr >> data`) enable optimization through expression composition before evaluation, while reverse pipelines (`data >> expr >> expr`) evaluate step-by-step.

## Why use it

**Good for:**
- Functional programming patterns
- Mathematical expressions in scientific computing

**Performance:**
- Lightweight wrapper that delivers similar performance to common operations
- May be fractionally slower for simple native Python operations

## Contributing

### Development Setup

UnderscoreC uses [uv](https://docs.astral.sh/uv/) for dependency management and development workflows.

```bash
# Clone the repository
git clone https://github.com/yourusername/underscorec
cd underscorec

# Install dependencies
uv sync

# Build the C extension for development
uv run python setup.py build_ext --inplace

# Verify installation works
uv run python -c "from underscorec import __; print('Setup successful!')"
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test modules
uv run pytest tests/test_core_operations.py

# Run with coverage report
uv run pytest --cov-report=html
```

### Running Performance Benchmark

```bash
# Run performance benchmarks
uv run python benchmarks/run_modular_benchmarks.py
```

### Building and Publishing

```bash
# Build source distribution and wheel
uv build

# The built packages will be in dist/
# - underscorec-0.1.0.tar.gz (source distribution)
# - underscorec-0.1.0-cp310-cp310-macosx_15_0_arm64.whl (binary wheel)

# Publish to PyPI (requires PyPI credentials)
uv publish

# Or publish to Test PyPI first
uv publish --repository testpypi
```

**Note**: The `MANIFEST.in` file ensures that C++ header files are included in the source distribution for proper building on different platforms.

## Future Improvements

This project is experimental and under development. More functionalities and performance improvements will be added as needed, including:

- Expression compilation for better performance
- Enhanced functional programming features
- Broader ecosystem integrations
