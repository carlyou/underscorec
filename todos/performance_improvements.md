# Performance Improvements

## Critical Priority (High Impact)

### 1. Optimize Function Call Overhead
- **Issue**: 40-70% slower than native Python operations due to function call stack overhead
- **Current Impact**: 2.1x-2.4x slower for list comprehensions, 1.4x-1.6x slower for lambda+map
- **Location**: `src/underscorec/underscorec.cpp:276` - `underscore_call` function
- **Solution**:
  - Implement fast-path detection for simple operations
  - Bypass proxy object creation for trivial cases
  - Consider inline C extensions for critical operations
  - Cache expression compilation results
- **Expected Impact**: 2-3x performance improvement for small operations

### 2. Fix PyTorch GPU Transfer Issues
- **Issue**: Some PyTorch operations show 0.12x performance (8x slower)
- **Current Impact**: Critical performance degradation in ML workflows
- **Location**: `src/underscorec/underscorec_torch.cpp` - GPU operation handling
- **Solution**:
  - Implement device-aware operation dispatching
  - Avoid unnecessary GPU/CPU transfers
  - Add tensor device consistency checks
  - Optimize tensor transfer patterns
- **Expected Impact**: Critical for ML/deep learning adoption

## Medium Priority

### 3. Expression Tree Optimization
- **Issue**: Complex expressions have evaluation overhead, some NumPy ops drop to 0.34x
- **Location**: `src/underscorec/underscorec.cpp:230` - `underscore_eval` function
- **Solution**:
  - Implement expression fusion for chained operations
  - Add specialized handlers for common patterns (add+multiply, etc.)
  - Consider lazy evaluation optimizations
  - Optimize expression tree traversal
- **Expected Impact**: Better performance for complex data pipelines

### 4. Small Operation Fast-Path
- **Issue**: Fixed costs dominate small operations (0.02ms becomes 0.05ms)
- **Solution**:
  - Detect trivial operations and use optimized path
  - Reduce proxy object overhead for simple cases
  - Implement operation-specific optimizations
- **Expected Impact**: Significant improvement for micro-operations

## Low Priority

### 5. Memory Layout Optimization
- **Issue**: Potential cache locality issues in larger operations
- **Solution**:
  - Profile memory access patterns
  - Optimize for cache locality in expression evaluation
  - Consider memory pooling for expression objects
- **Expected Impact**: Marginal improvements for large-scale operations