#!/usr/bin/env python3
"""Generate C code for FRE test"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import tokenize
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.codegen_backend import Z88dkCBackend

# Read the test program
with open("test_compile/test_fre_complete.bas", "r") as f:
    source = f.read()

# Tokenize
tokens = tokenize(source)

# Parse
parser = Parser(tokens)
program = parser.parse()

# Semantic analysis
analyzer = SemanticAnalyzer()
analyzer.analyze(program)

# Code generation
backend = Z88dkCBackend(analyzer.symbols)
c_code = backend.generate(program)

# Print the C code
print(c_code)

# Print warnings
if backend.warnings:
    print("\n\n=== Warnings ===", file=sys.stderr)
    for warning in backend.warnings:
        print(f"  {warning}", file=sys.stderr)
