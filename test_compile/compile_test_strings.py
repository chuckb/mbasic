#!/usr/bin/env python3
"""
Test the compiler with string support
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.codegen_backend import Z88dkCBackend

def compile_basic_to_c(basic_code: str) -> str:
    """Compile BASIC code to C"""
    # Lex
    lexer = Lexer(basic_code)
    tokens = lexer.tokenize()

    # Parse
    parser = Parser(tokens)
    ast = parser.parse()

    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    # Code generation
    backend = Z88dkCBackend(analyzer.symbols)
    c_code = backend.generate(ast)

    # Print any warnings
    if backend.warnings:
        print("Warnings:", file=sys.stderr)
        for warning in backend.warnings:
            print(f"  {warning}", file=sys.stderr)

    return c_code

if __name__ == "__main__":
    # Read the test program
    with open("test_strings.bas", "r") as f:
        basic_code = f.read()

    print("=== BASIC Program ===")
    print(basic_code)
    print()
    print("=== Generated C Code ===")

    try:
        c_code = compile_basic_to_c(basic_code)
        print(c_code)

        # Save to file
        with open("test_strings.c", "w") as f:
            f.write(c_code)
        print("\nC code saved to test_strings.c")

    except Exception as e:
        print(f"Compilation error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()