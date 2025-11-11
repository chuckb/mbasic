#!/usr/bin/env python3
"""Direct test of array code generation"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ast_nodes import *
from src.semantic_analyzer import SemanticAnalyzer, VarType, VariableInfo
from src.codegen_backend import Z88dkCBackend

# Create a simple AST directly
var_node = VariableNode(name='b', type_suffix='%', subscripts=[
    NumberNode(value=0, literal=0),
    NumberNode(value=0, literal=0)
])

stmt = LetStatementNode(
    variable=var_node,
    expression=NumberNode(value=10, literal=10)
)

# Create analyzer with symbol table
analyzer = SemanticAnalyzer()
analyzer.symbols.variables['B%'] = VariableInfo(
    name='B%',
    var_type=VarType.INTEGER,
    is_array=True,
    dimensions=[5, 3],
    flattened_size=24
)

# Generate code
backend = Z88dkCBackend(analyzer.symbols)

print("Variable node has subscripts?", hasattr(var_node, 'subscripts'))
print("Variable subscripts value:", var_node.subscripts)
print("Variable subscripts type:", type(var_node.subscripts))
print("Subscripts bool:", bool(var_node.subscripts))
print("Len subscripts:", len(var_node.subscripts) if var_node.subscripts else 0)

# Generate assignment
result = backend._generate_assignment(stmt)
print("Generated:", result)