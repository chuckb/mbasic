#!/usr/bin/env python3
"""
Benchmark the semantic analyzer performance

Tests analysis speed on programs of various sizes
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from lexer import tokenize
from parser import Parser
from semantic_analyzer import SemanticAnalyzer


def generate_test_program(lines):
    """Generate a test BASIC program with specified number of lines"""
    program = []
    program.append("10 REM Test Program")

    line_num = 20
    for i in range(lines // 5):
        program.append(f"{line_num} A = {i}")
        line_num += 10
        program.append(f"{line_num} B = {i * 2}")
        line_num += 10
        program.append(f"{line_num} C = A + B")
        line_num += 10
        program.append(f"{line_num} PRINT C")
        line_num += 10
        program.append(f"{line_num} REM Comment line {i}")
        line_num += 10

    program.append(f"{line_num} END")
    return "\n".join(program)


def benchmark_analysis(code):
    """Benchmark semantic analysis"""
    # Tokenize
    start = time.time()
    tokens = tokenize(code)
    tokenize_time = time.time() - start

    # Parse
    start = time.time()
    parser = Parser(tokens)
    program = parser.parse()
    parse_time = time.time() - start

    # Analyze
    start = time.time()
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(program)
    analyze_time = time.time() - start

    return {
        'tokenize': tokenize_time,
        'parse': parse_time,
        'analyze': analyze_time,
        'total': tokenize_time + parse_time + analyze_time,
        'success': success,
        'variables': len(analyzer.symbols.variables),
        'line_numbers': len(analyzer.symbols.line_numbers),
        'optimizations': len(analyzer.folded_expressions) + len(analyzer.common_subexpressions),
    }


def main():
    print("=" * 70)
    print("MBASIC SEMANTIC ANALYZER BENCHMARK")
    print("=" * 70)
    print()

    test_sizes = [10, 50, 100, 500, 1000]

    print(f"{'Lines':<10} {'Tokenize':<12} {'Parse':<12} {'Analyze':<12} {'Total':<12} {'Opts':<8}")
    print("-" * 70)

    for size in test_sizes:
        code = generate_test_program(size)
        result = benchmark_analysis(code)

        print(f"{size:<10} "
              f"{result['tokenize']*1000:>8.2f} ms  "
              f"{result['parse']*1000:>8.2f} ms  "
              f"{result['analyze']*1000:>8.2f} ms  "
              f"{result['total']*1000:>8.2f} ms  "
              f"{result['optimizations']:>6}")

    print()
    print("=" * 70)
    print()

    # Test with actual demo program
    print("Analyzing demo_all_optimizations.bas...")
    try:
        with open('demo_all_optimizations.bas', 'r') as f:
            code = f.read()

        result = benchmark_analysis(code)
        print(f"  Time: {result['total']*1000:.2f} ms")
        print(f"  Variables: {result['variables']}")
        print(f"  Lines: {result['line_numbers']}")
        print(f"  Optimizations: {result['optimizations']}")
        print()
    except FileNotFoundError:
        print("  demo_all_optimizations.bas not found")

    print("=" * 70)


if __name__ == '__main__':
    main()
