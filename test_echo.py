#!/usr/bin/env python3
"""
Comprehensive test suite for Echo module.
"""

import unittest
import tempfile
import os
import time
from unittest.mock import patch, mock_open
from io import StringIO

from echo import Echo, main


class TestEchoUnit(unittest.TestCase):
    """Unit tests for Echo class methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.echo = Echo()
        self.echo_with_prefix = Echo(prefix="[PREFIX] ", suffix=" [SUFFIX]")
    
    def test_simple_echo(self):
        """Test basic echo functionality."""
        result = self.echo.echo("Hello World")
        self.assertEqual(result, "Hello World")
    
    def test_echo_with_prefix_suffix(self):
        """Test echo with prefix and suffix."""
        result = self.echo_with_prefix.echo("Test")
        self.assertEqual(result, "[PREFIX] Test [SUFFIX]")
    
    def test_echo_list_input(self):
        """Test echo with list input."""
        result = self.echo.echo(["Hello", "World", "Test"])
        self.assertEqual(result, "Hello World Test")
    
    def test_echo_upper(self):
        """Test uppercase echo."""
        result = self.echo.echo_upper("hello world")
        self.assertEqual(result, "HELLO WORLD")
    
    def test_echo_lower(self):
        """Test lowercase echo."""
        result = self.echo.echo_lower("HELLO WORLD")
        self.assertEqual(result, "hello world")
    
    def test_echo_reverse(self):
        """Test reverse echo."""
        result = self.echo.echo_reverse("Hello")
        self.assertEqual(result, "olleH")
    
    def test_echo_repeat(self):
        """Test repeated echo."""
        result = self.echo.echo_repeat("Test", 3)
        self.assertEqual(result, "Test Test Test")
    
    def test_echo_repeat_custom_separator(self):
        """Test repeated echo with custom separator."""
        result = self.echo.echo_repeat("Test", 3, separator="-")
        self.assertEqual(result, "Test-Test-Test")
    
    def test_echo_repeat_zero_times(self):
        """Test echo repeat with zero repetitions."""
        result = self.echo.echo_repeat("Test", 0)
        self.assertEqual(result, "")
    
    def test_echo_repeat_negative_times(self):
        """Test echo repeat with negative repetitions raises error."""
        with self.assertRaises(ValueError):
            self.echo.echo_repeat("Test", -1)
    
    def test_history_storage(self):
        """Test echo history storage."""
        self.echo.echo("First")
        self.echo.echo("Second")
        self.echo.echo("Third")
        
        history = self.echo.get_history()
        self.assertEqual(history, ["First", "Second", "Third"])
    
    def test_history_no_store(self):
        """Test echo without storing in history."""
        self.echo.echo("First", store_history=True)
        self.echo.echo("Not stored", store_history=False)
        self.echo.echo("Second", store_history=True)
        
        history = self.echo.get_history()
        self.assertEqual(history, ["First", "Second"])
    
    def test_clear_history(self):
        """Test clearing echo history."""
        self.echo.echo("Test1")
        self.echo.echo("Test2")
        self.echo.clear_history()
        
        history = self.echo.get_history()
        self.assertEqual(history, [])
    
    def test_get_history_returns_copy(self):
        """Test that get_history returns a copy, not reference."""
        self.echo.echo("Test")
        history = self.echo.get_history()
        history.append("Modified")
        
        actual_history = self.echo.get_history()
        self.assertEqual(actual_history, ["Test"])


class TestEchoFileOperations(unittest.TestCase):
    """Test file-related echo operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.echo = Echo()
    
    def test_echo_file_success(self):
        """Test echoing file contents."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("File content test")
            temp_path = f.name
        
        try:
            result = self.echo.echo_file(temp_path)
            self.assertEqual(result, "File content test")
        finally:
            os.unlink(temp_path)
    
    def test_echo_file_not_found(self):
        """Test echoing non-existent file."""
        result = self.echo.echo_file("/nonexistent/file.txt")
        self.assertIsNone(result)
    
    def test_echo_file_with_prefix_suffix(self):
        """Test echoing file with prefix/suffix."""
        echo_formatted = Echo(prefix=">>> ", suffix=" <<<")
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Content")
            temp_path = f.name
        
        try:
            result = echo_formatted.echo_file(temp_path)
            self.assertEqual(result, ">>> Content <<<")
        finally:
            os.unlink(temp_path)


class TestEchoEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.echo = Echo()
    
    def test_empty_string_echo(self):
        """Test echoing empty string."""
        result = self.echo.echo("")
        self.assertEqual(result, "")
    
    def test_unicode_echo(self):
        """Test echoing Unicode characters."""
        result = self.echo.echo("Hello 世界 🌍")
        self.assertEqual(result, "Hello 世界 🌍")
    
    def test_special_characters_echo(self):
        """Test echoing special characters."""
        special = "!@#$%^&*()_+-=[]{}|;:',.<>?/`~"
        result = self.echo.echo(special)
        self.assertEqual(result, special)
    
    def test_newline_echo(self):
        """Test echoing with newlines."""
        result = self.echo.echo("Line1\nLine2\nLine3")
        self.assertEqual(result, "Line1\nLine2\nLine3")
    
    def test_very_long_string(self):
        """Test echoing very long string."""
        long_string = "A" * 10000
        result = self.echo.echo(long_string)
        self.assertEqual(result, long_string)
        self.assertEqual(len(result), 10000)
    
    def test_none_in_list(self):
        """Test handling None in list input."""
        result = self.echo.echo(["Hello", None, "World"])
        self.assertEqual(result, "Hello None World")


class TestEchoIntegration(unittest.TestCase):
    """Integration tests for Echo combinations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.echo = Echo(prefix="[", suffix="]")
    
    def test_chained_operations(self):
        """Test chaining multiple echo operations."""
        text = "Test"
        upper = self.echo.echo_upper(text)
        self.assertEqual(upper, "[TEST]")
        
        lower = self.echo.echo_lower(text)
        self.assertEqual(lower, "[test]")
        
        reverse = self.echo.echo_reverse(text)
        self.assertEqual(reverse, "[tseT]")
    
    def test_history_with_all_methods(self):
        """Test history tracking across different methods."""
        self.echo.echo("Normal")
        self.echo.echo_upper("upper")
        self.echo.echo_lower("LOWER")
        self.echo.echo_reverse("reverse")
        
        history = self.echo.get_history()
        expected = ["[Normal]", "[UPPER]", "[lower]", "[esrever]"]
        self.assertEqual(history, expected)
    
    def test_complex_workflow(self):
        """Test a complex workflow with multiple operations."""
        echo = Echo(prefix=">> ", suffix=" <<")
        
        echo.echo("First message")
        echo.echo_repeat("Important", 2, separator=" - ")
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("File content")
            temp_path = f.name
        
        try:
            echo.echo_file(temp_path)
            history = echo.get_history()
            
            self.assertEqual(len(history), 3)
            self.assertIn("First message", history[0])
            self.assertIn("Important - Important", history[1])
            self.assertIn("File content", history[2])
        finally:
            os.unlink(temp_path)


class TestEchoMain(unittest.TestCase):
    """Test the main CLI functionality."""
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_args(self, mock_stdout):
        """Test main function with arguments."""
        result = main(["Hello", "World"])
        self.assertEqual(result, 0)
        self.assertEqual(mock_stdout.getvalue().strip(), "Hello World")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_args(self, mock_stdout):
        """Test main function without arguments."""
        result = main([])
        self.assertEqual(result, 1)
        self.assertIn("Usage:", mock_stdout.getvalue())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_single_arg(self, mock_stdout):
        """Test main function with single argument."""
        result = main(["SingleWord"])
        self.assertEqual(result, 0)
        self.assertEqual(mock_stdout.getvalue().strip(), "SingleWord")


class TestEchoPerformance(unittest.TestCase):
    """Performance tests for Echo."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.echo = Echo()
    
    def test_large_history_performance(self):
        """Test performance with large history."""
        start_time = time.time()
        
        for i in range(10000):
            self.echo.echo(f"Message {i}")
        
        history = self.echo.get_history()
        elapsed_time = time.time() - start_time
        
        self.assertEqual(len(history), 10000)
        self.assertLess(elapsed_time, 1.0, "Operation took too long")
    
    def test_large_string_performance(self):
        """Test performance with large strings."""
        large_string = "X" * 1000000  # 1MB string
        
        start_time = time.time()
        result = self.echo.echo(large_string)
        elapsed_time = time.time() - start_time
        
        self.assertEqual(len(result), 1000000)
        self.assertLess(elapsed_time, 0.1, "Echo of large string too slow")
    
    def test_repeat_performance(self):
        """Test performance of repeat operation."""
        start_time = time.time()
        result = self.echo.echo_repeat("Test", 1000, separator="-")
        elapsed_time = time.time() - start_time
        
        self.assertIn("Test", result)
        self.assertEqual(result.count("Test"), 1000)
        self.assertLess(elapsed_time, 0.1, "Repeat operation too slow")


class TestEchoSecurity(unittest.TestCase):
    """Security tests for Echo."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.echo = Echo()
    
    def test_path_traversal_protection(self):
        """Test protection against path traversal."""
        dangerous_paths = [
            "../../../etc/passwd",
            "../../sensitive.txt",
            "/etc/shadow"
        ]
        
        for path in dangerous_paths:
            result = self.echo.echo_file(path)
            # Should return None for non-existent or inaccessible files
            self.assertIsNone(result)
    
    def test_command_injection_protection(self):
        """Test protection against command injection."""
        dangerous_inputs = [
            "; rm -rf /",
            "$(cat /etc/passwd)",
            "`ls -la`",
            "'; DROP TABLE users; --"
        ]
        
        for dangerous in dangerous_inputs:
            result = self.echo.echo(dangerous)
            # Should echo literally without executing
            self.assertEqual(result, dangerous)
    
    def test_memory_limit_protection(self):
        """Test protection against memory exhaustion."""
        # Try to create a string that would use excessive memory
        try:
            # This should handle gracefully without crashing
            result = self.echo.echo_repeat("X", 1000000)
            # If it succeeds, verify it's handled correctly
            self.assertIsNotNone(result)
        except MemoryError:
            # If memory error occurs, that's also acceptable protection
            pass


def run_tests_with_coverage():
    """Run tests with coverage reporting."""
    import coverage
    
    cov = coverage.Coverage()
    cov.start()
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    cov.stop()
    cov.save()
    
    print("\n" + "="*50)
    print("COVERAGE REPORT")
    print("="*50)
    cov.report()
    
    return result.wasSuccessful()


if __name__ == "__main__":
    try:
        success = run_tests_with_coverage()
        exit(0 if success else 1)
    except ImportError:
        # If coverage module not available, run tests normally
        unittest.main(verbosity=2)