#!/usr/bin/env python3
"""Debug script to check array handling in semantic analyzer"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import tokenize
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer

test_program = """
10 DIM A%(5)
20 LET A%(0) = 10
30 LET A%(1) = 20
40 LET X% = A%(0) + A%(1)
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

print("Symbol table:")
for var_name, var_info in analyzer.symbols.variables.items():
    print(f"  {var_name}: is_array={var_info.is_array}, type={var_info.var_type}, dimensions={var_info.dimensions}, flattened_size={var_info.flattened_size}")