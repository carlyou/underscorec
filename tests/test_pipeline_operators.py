"""
Test pipeline operators for immediate evaluation.

These tests cover the three cases of the >> operator:
1. expr >> expr2 (composition)
2. expr >> data (normal pipeline - evaluate expression with data)
3. data >> expr (reverse pipeline - evaluate expression with data)
"""
import pytest
import numpy as np
import torch
from underscorec import __


class TestPipelineOperators:
    """Test pipeline operators for immediate evaluation."""
    
    def test_normal_pipeline_basic(self):
        """Test normal pipeline: expr >> data"""
        # Basic arithmetic operations
        assert (__ + 1) >> 5 == 6
        assert (__ * 2) >> 3 == 6
        assert (__ - 4) >> 10 == 6
        assert (__ / 2) >> 8 == 4.0
        assert (__ ** 2) >> 3 == 9
        
    def test_reverse_pipeline_basic(self):
        """Test reverse pipeline: data >> expr"""
        # Basic arithmetic operations
        assert 5 >> (__ + 1) == 6
        assert 3 >> (__ * 2) == 6
        assert 10 >> (__ - 4) == 6
        assert 8 >> (__ / 2) == 4.0
        assert 3 >> (__ ** 2) == 9
        
    def test_pipeline_equivalence(self):
        """Test that normal and reverse pipelines are equivalent."""
        expr = __ + 10
        data = 5
        
        # These should give the same result
        normal_result = expr >> data
        reverse_result = data >> expr
        traditional_result = expr(data)
        
        assert normal_result == reverse_result == traditional_result == 15
        
    def test_pipeline_vs_composition(self):
        """Test that expr >> expr creates composition, not pipeline."""
        # This should create a composition, not evaluate immediately
        comp = (__ + 1) >> (__ * 2)
        assert isinstance(comp, type(__))  # Should be an underscore object
        assert comp(5) == 12  # (5 + 1) * 2 = 12
        
        # String representation should show composition
        assert " >> " in repr(comp)
        
    def test_normal_pipeline_complex_expressions(self):
        """Test normal pipeline with complex expressions."""
        # Comparison operations
        assert (__ > 5) >> 10 is True
        assert (__ < 5) >> 3 is True
        assert (__ == 5) >> 5 is True
        
        # Bitwise operations
        assert (__ & 3) >> 7 == 3  # 7 & 3 = 3
        assert (__ | 3) >> 5 == 7  # 5 | 3 = 7
        assert (__ ^ 3) >> 5 == 6  # 5 ^ 3 = 6
        
        # Unary operations
        assert (-__) >> 5 == -5
        assert abs(__) >> -5 == 5
        assert (~__) >> 5 == -6
        
    def test_reverse_pipeline_complex_expressions(self):
        """Test reverse pipeline with complex expressions."""
        # Comparison operations
        assert 10 >> (__ > 5) is True
        assert 3 >> (__ < 5) is True
        assert 5 >> (__ == 5) is True
        
        # Bitwise operations
        assert 7 >> (__ & 3) == 3  # 7 & 3 = 3
        assert 5 >> (__ | 3) == 7  # 5 | 3 = 7
        assert 5 >> (__ ^ 3) == 6  # 5 ^ 3 = 6
        
        # Unary operations
        assert 5 >> (-__) == -5
        assert -5 >> abs(__) == 5
        assert 5 >> (~__) == -6
        
    def test_pipeline_with_method_calls(self):
        """Test pipeline operators with method calls."""
        # Normal pipeline with method calls
        assert (__.upper()) >> "hello" == "HELLO"
        assert (__.split(",")) >> "a,b,c" == ["a", "b", "c"]
        assert (__.strip()) >> "  hello  " == "hello"
        
        # Reverse pipeline with method calls
        assert "hello" >> (__.upper()) == "HELLO" 
        assert "a,b,c" >> (__.split(",")) == ["a", "b", "c"]
        assert "  hello  " >> (__.strip()) == "hello"
        
    def test_pipeline_with_attribute_access(self):
        """Test pipeline operators with attribute access."""
        # Test with list
        test_list = [1, 2, 3, 4]
        assert (__.real) >> 5 == 5  # int.real
        assert test_list >> (__.copy()) == [1, 2, 3, 4]
        
        # Test with string
        assert "hello" >> (__.upper()) == "HELLO"
        
    def test_pipeline_with_indexing(self):
        """Test pipeline operators with indexing operations."""
        # Normal pipeline with indexing
        assert (__[0]) >> [1, 2, 3] == 1
        assert (__[1:3]) >> [1, 2, 3, 4] == [2, 3]
        assert (__["key"]) >> {"key": "value"} == "value"
        
        # Reverse pipeline with indexing
        assert [1, 2, 3] >> (__[0]) == 1
        assert [1, 2, 3, 4] >> (__[1:3]) == [2, 3]
        assert {"key": "value"} >> (__["key"]) == "value"
        
    @pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA not available")
    def test_pipeline_with_torch_tensors(self):
        """Test pipeline operators with PyTorch tensors."""
        tensor = torch.tensor([1, 2, 3, 4], dtype=torch.float32)
        
        # Normal pipeline
        result = (__ + 1) >> tensor
        expected = torch.tensor([2, 3, 4, 5], dtype=torch.float32)
        assert torch.equal(result, expected)
        
        # Reverse pipeline
        result = tensor >> (__ + 1)
        assert torch.equal(result, expected)
        
        # Complex operations
        result = (__ * 2 + 1) >> tensor
        expected = torch.tensor([3, 5, 7, 9], dtype=torch.float32)
        assert torch.equal(result, expected)
        
    def test_pipeline_with_numpy_arrays(self):
        """Test pipeline operators with NumPy arrays."""
        arr = np.array([1, 2, 3, 4])
        
        # Normal pipeline
        result = (__ + 1) >> arr
        expected = np.array([2, 3, 4, 5])
        np.testing.assert_array_equal(result, expected)
        
        # Reverse pipeline - NOTE: This currently has limitations due to NumPy's __array_struct__
        # For now, test only normal pipeline with NumPy
        # TODO: Fix NumPy reverse pipeline support
        
        # Complex operations with normal pipeline
        result = (__ * 2 + 1) >> arr
        expected = np.array([3, 5, 7, 9])
        np.testing.assert_array_equal(result, expected)
        
    def test_pipeline_error_handling(self):
        """Test error handling in pipeline operators."""
        # Type errors should propagate
        with pytest.raises(TypeError):
            "hello" >> (__ + 1)  # Can't add int to string
            
        with pytest.raises(TypeError):
            (__ + "world") >> 5  # Can't add string to int
            
        # Division by zero
        with pytest.raises(ZeroDivisionError):
            (__ / 0) >> 5
            
        with pytest.raises(ZeroDivisionError):
            5 >> (__ / 0)
            
        # Index errors
        with pytest.raises(IndexError):
            (__[10]) >> [1, 2, 3]
            
        with pytest.raises(IndexError):
            [1, 2, 3] >> (__[10])
            
    def test_pipeline_with_multi_reference_expressions(self):
        """Test pipeline operators with multi-reference expressions."""
        # Multi-reference in normal pipeline
        result = (__ + __) >> 5
        assert result == 10  # 5 + 5 = 10
        
        # Multi-reference in reverse pipeline
        result = 5 >> (__ + __)
        assert result == 10  # 5 + 5 = 10
        
        # Complex multi-reference
        result = (__ * __ - 1) >> 4
        assert result == 15  # 4 * 4 - 1 = 15
        
        result = 4 >> (__ * __ - 1)
        assert result == 15  # 4 * 4 - 1 = 15
        
    def test_pipeline_chaining_behavior(self):
        """Test behavior when chaining pipeline operations."""
        # Case 2: expr1 >> expr2 >> data
        # This should create composition first, then evaluate
        result = (__ + 1) >> (__ * 2) >> 5
        assert result == 12  # Composition: (5 + 1) * 2 = 12
        
        # Case 3: data >> expr1 >> expr2
        # This evaluates step by step (less optimal)
        result = 5 >> (__ + 1) >> (__ * 2)
        assert result == 12  # Step by step: 5 >> (__ + 1) = 6, then 6 >> (__ * 2) = 12
        
    def test_pipeline_with_different_data_types(self):
        """Test pipeline operators with various data types."""
        # Strings
        assert "hello" >> (__.upper()) == "HELLO"
        assert (__.upper()) >> "hello" == "HELLO"
        
        # Lists
        assert [1, 2, 3] >> (__.reverse()) is None  # reverse() returns None
        assert (__.copy()) >> [1, 2, 3] == [1, 2, 3]
        
        # Dictionaries
        d = {"a": 1, "b": 2}
        assert d >> (__["a"]) == 1
        assert (__["a"]) >> d == 1
        
        # Numbers - Note: Python float doesn't define __rshift__, so reverse pipeline fails
        # assert 3.14 >> (__ + 1) == 4.14  # This fails because float doesn't support >>
        result = (__ + 1) >> 3.14
        assert abs(result - 4.14) < 1e-10  # Account for floating point precision
        
        # Booleans
        assert True >> (__ & False) is False
        assert (__ | True) >> False is True
        
    def test_pipeline_performance_characteristics(self):
        """Test performance characteristics of different pipeline patterns."""
        # This is more of a sanity check
        # Case 2 (composition) should be more efficient than Case 3 (step-by-step)
        
        # Large data for testing
        data = list(range(1000))
        
        # Case 2: expr >> expr >> data (composition)
        comp_expr = (__.copy()) >> (__.reverse())
        result1 = comp_expr >> data
        
        # Case 3: data >> expr >> expr (step-by-step)
        result2 = data >> (__.copy()) >> (__.reverse())
        
        # Results should be equivalent (both None since reverse() returns None)
        assert result1 == result2
        
    def test_pipeline_with_callable_objects(self):
        """Test pipeline operators with callable objects."""
        # Test with built-in callables
        comp = (__ + 1) >> str  # This creates composition  
        assert comp(5) == "6"  # (5 + 1) = 6 -> "6"
        
        # Test with lambda functions
        double = lambda x: x * 2
        comp = (__ + 1) >> double  # This is composition
        assert comp(5) == 12  # (5 + 1) * 2 = 12
        
        # Test callable >> expr (should create composition)
        comp = double >> (__ + 1)  # This creates composition: callable first, then expr
        assert comp(5) == 11  # double(5) + 1 = 10 + 1 = 11
        
        # Test step-by-step evaluation (data >> expr)
        result = 5 >> (__ + 1)  # This evaluates to 6
        assert result == 6
        
    def test_pipeline_edge_cases(self):
        """Test edge cases for pipeline operators."""
        # Empty containers
        assert [] >> (__.copy()) == []
        assert (__.copy()) >> [] == []
        
        # Zero values
        assert 0 >> (__ + 1) == 1
        assert (__ + 1) >> 0 == 1
        
        # None values - Test expressions that work with None
        identity_expr = lambda x: x  # Identity function
        comp = identity_expr >> __ # This creates composition
        assert comp(None) is None  # Identity of None is None
        
        # Very large numbers
        big_num = 10**100
        assert big_num >> (__ + 1) == big_num + 1
        assert (__ + 1) >> big_num == big_num + 1