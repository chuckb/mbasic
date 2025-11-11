#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.lexer import Lexer
from src.parser import Parser

code = '10 FIRST$ = LEFT$(NAME$, 3)'
lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

print('AST:', ast)
if ast and ast.lines:
    line = ast.lines[0]
    if line.statements:
        stmt = line.statements[0]
        print('Statement type:', type(stmt).__name__)
        if hasattr(stmt, 'expression'):
            print('Expression type:', type(stmt.expression).__name__)
            if hasattr(stmt.expression, 'name'):
                print('Function name:', repr(stmt.expression.name))