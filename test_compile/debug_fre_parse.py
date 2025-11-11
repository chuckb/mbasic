#!/usr/bin/env python3
"""Debug FRE parsing"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import tokenize
from src.parser import Parser

# Test code
code = "10 F = FRE(0)"

# Tokenize
print("Tokenizing:", code)
tokens = tokenize(code)
print("\nTokens:")
for tok in tokens:
    print(f"  {tok.type.name:20} {tok.value!r}")

# Parse
print("\nParsing...")
parser = Parser(tokens)
ast = parser.parse()

print("\nAST:")
print(f"  Program has {len(ast.lines)} lines")
for line in ast.lines:
    print(f"  Line {line.line_number}:")
    for stmt in line.statements:
        print(f"    Statement type: {type(stmt).__name__}")
        print(f"    Statement.__dict__: {stmt.__dict__}")
        if hasattr(stmt, 'variable'):
            variable = stmt.variable
            print(f"      Variable: {variable}")
            print(f"      Variable type: {type(variable).__name__}")
        if hasattr(stmt, 'expression'):
            value = stmt.expression
            print(f"      Expression type: {type(value).__name__}")
            print(f"      Expression.__dict__: {value.__dict__}")
            if hasattr(value, 'name'):
                print(f"      Expression.name: {value.name}")
            if hasattr(value, 'arguments'):
                print(f"      Expression.arguments: {value.arguments}")
                for i, arg in enumerate(value.arguments):
                    print(f"        Arg {i}: {type(arg).__name__} = {arg}")
