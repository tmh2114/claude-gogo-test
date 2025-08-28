#!/usr/bin/env python3
"""
Performance benchmarking for Echo module.
"""

import time
import statistics
from echo import Echo


def benchmark_operation(operation, iterations=1000):
    """Benchmark an operation over multiple iterations.
    
    Args:
        operation: Function to benchmark
        iterations: Number of iterations to run
        
    Returns:
        Dictionary with timing statistics
    """
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        operation()
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'min': min(times),
        'max': max(times),
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'total': sum(times)
    }


def format_time(seconds):
    """Format time in appropriate units."""
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    else:
        return f"{seconds:.2f} s"


def print_benchmark_results(name, stats):
    """Print formatted benchmark results."""
    print(f"\n{name}")
    print("-" * 50)
    print(f"Mean:   {format_time(stats['mean'])}")
    print(f"Median: {format_time(stats['median'])}")
    print(f"Min:    {format_time(stats['min'])}")
    print(f"Max:    {format_time(stats['max'])}")
    print(f"StdDev: {format_time(stats['stdev'])}")
    print(f"Total:  {format_time(stats['total'])}")


def main():
    """Run performance benchmarks."""
    print("="*50)
    print("ECHO MODULE PERFORMANCE BENCHMARKS")
    print("="*50)
    
    echo = Echo()
    echo_with_formatting = Echo(prefix="[PREFIX] ", suffix=" [SUFFIX]")
    
    # Benchmark 1: Simple echo
    stats = benchmark_operation(
        lambda: echo.echo("Hello World"),
        iterations=10000
    )
    print_benchmark_results("Simple Echo (10,000 iterations)", stats)
    
    # Benchmark 2: Echo with formatting
    stats = benchmark_operation(
        lambda: echo_with_formatting.echo("Hello World"),
        iterations=10000
    )
    print_benchmark_results("Echo with Prefix/Suffix (10,000 iterations)", stats)
    
    # Benchmark 3: List echo
    test_list = ["Word"] * 100
    stats = benchmark_operation(
        lambda: echo.echo(test_list),
        iterations=1000
    )
    print_benchmark_results("Echo List of 100 words (1,000 iterations)", stats)
    
    # Benchmark 4: Large string echo
    large_string = "X" * 10000
    stats = benchmark_operation(
        lambda: echo.echo(large_string),
        iterations=1000
    )
    print_benchmark_results("Echo 10KB String (1,000 iterations)", stats)
    
    # Benchmark 5: Repeat operation
    stats = benchmark_operation(
        lambda: echo.echo_repeat("Test", 100, separator=" "),
        iterations=1000
    )
    print_benchmark_results("Echo Repeat 100 times (1,000 iterations)", stats)
    
    # Benchmark 6: History operations
    echo_history = Echo()
    for i in range(1000):
        echo_history.echo(f"Message {i}")
    
    stats = benchmark_operation(
        lambda: echo_history.get_history(),
        iterations=1000
    )
    print_benchmark_results("Get History (1000 items, 1000 iterations)", stats)
    
    # Benchmark 7: String transformations
    stats = benchmark_operation(
        lambda: echo.echo_upper("hello world test string"),
        iterations=10000
    )
    print_benchmark_results("Echo Upper (10,000 iterations)", stats)
    
    stats = benchmark_operation(
        lambda: echo.echo_reverse("hello world test string"),
        iterations=10000
    )
    print_benchmark_results("Echo Reverse (10,000 iterations)", stats)
    
    print("\n" + "="*50)
    print("Benchmark completed successfully!")
    print("="*50)


if __name__ == "__main__":
    main()