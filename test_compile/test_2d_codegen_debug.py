#!/usr/bin/env python3
"""Debug 2D array code generation with detailed output"""

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

# Code generation - override _generate_assignment to add debug output
class DebugBackend(Z88dkCBackend):
    def _generate_assignment(self, stmt):
        print(f"DEBUG: In _generate_assignment")
        print(f"  Variable name: {stmt.variable.name}")
        print(f"  Variable subscripts: {stmt.variable.subscripts}")
        print(f"  Subscripts type: {type(stmt.variable.subscripts)}")
        if stmt.variable.subscripts:
            print(f"  Len subscripts: {len(stmt.variable.subscripts)}")
            print(f"  Subscripts bool: {bool(stmt.variable.subscripts)}")

        # Call parent and see what it returns
        result = super()._generate_assignment(stmt)
        print(f"  Result: {result}")
        return result

backend = DebugBackend(analyzer.symbols)
output = backend.generate(ast)

print("\nGenerated code:")
print(output)