#!/usr/bin/env python3
"""Debug 2D array code generation"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import tokenize
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.codegen_backend import Z88dkCBackend

test_program = """
10 DIM B%(5,3)
20 LET B%(0, 0) = 10
"""

print("Processing:", test_program.strip())
print()

# Tokenize
tokens = tokenize(test_program)

# Parse
parser = Parser(tokens)
ast = parser.parse()

# Semantic analysis
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

print("After semantic analysis:")
for line in ast.lines:
    print(f"Line {line.line_number}:")
    for stmt in line.statements:
        print(f"  Statement type: {type(stmt).__name__}")
        if hasattr(stmt, 'variable'):
            print(f"  Variable name: {stmt.variable.name}")
            print(f"  Variable subscripts: {stmt.variable.subscripts}")
            print(f"  Variable type: {type(stmt.variable)}")
            if stmt.variable.subscripts:
                print(f"  First subscript type: {type(stmt.variable.subscripts[0])}")

# Code generation
backend = Z88dkCBackend(analyzer.symbols)
output = backend.generate(ast)

print("\nGenerated code:")
print(output)