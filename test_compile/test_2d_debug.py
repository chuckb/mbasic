#!/usr/bin/env python3
"""Debug 2D array assignment"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import tokenize
from src.parser import Parser

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

for line in ast.lines:
    print(f"Line {line.line_number}:")
    for stmt in line.statements:
        print(f"  Statement type: {type(stmt).__name__}")
        if hasattr(stmt, 'variable'):
            print(f"  Variable name: {stmt.variable.name}")
            print(f"  Variable subscripts: {stmt.variable.subscripts}")
            if stmt.variable.subscripts:
                print(f"  Number of subscripts: {len(stmt.variable.subscripts)}")