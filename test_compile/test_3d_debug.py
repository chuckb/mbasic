#!/usr/bin/env python3
"""Debug 3D array issue"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import tokenize
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

test_program = """
10 DIM D(2,2,2)
20 LET D(0, 0, 0) = 100
"""

# Tokenize
tokens = tokenize(test_program)

# Parse
parser = Parser(tokens)
ast = parser.parse()

# Semantic analysis
analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

print("Symbol table:")
for var_name, var_info in analyzer.symbols.variables.items():
    print(f"  {var_name}: is_array={var_info.is_array}, type={var_info.var_type}, dimensions={var_info.dimensions}")

# Check the AST
for line in ast.lines:
    for stmt in line.statements:
        if hasattr(stmt, 'variable'):
            print(f"Line {line.line_number}: Variable name={stmt.variable.name}, type_suffix={stmt.variable.type_suffix}, subscripts={stmt.variable.subscripts is not None}")