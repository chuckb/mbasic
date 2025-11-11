#!/usr/bin/env python3
"""Test compiler script to compile BASIC to C"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.codegen_backend import Z88dkCBackend

def compile_basic(input_file, output_file):
    """Compile a BASIC program to C"""
    # Read the input file
    with open(input_file, 'r') as f:
        code = f.read()

    # Lex and parse
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()

    # Semantic analysis
    analyzer = SemanticAnalyzer()
    if not analyzer.analyze(program):
        print("Semantic analysis failed:")
        for error in analyzer.errors:
            print(f"  {error}")
        return False

    # Code generation
    codegen = Z88dkCBackend(analyzer.symbols)
    c_code = codegen.generate(program)

    # Write output
    with open(output_file, 'w') as f:
        f.write(c_code)

    print(f"Compiled {input_file} to {output_file}")

    # Print warnings if any
    if codegen.warnings:
        print("Warnings:")
        for warning in codegen.warnings:
            print(f"  {warning}")

    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 test_compile.py input.bas output.c")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if compile_basic(input_file, output_file):
        sys.exit(0)
    else:
        sys.exit(1)