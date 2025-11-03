#!/usr/bin/env python3
"""
Cross-reference analyzer for Python code.
Finds unused variables, undefined references, and dead code.
"""

import ast
import os
import sys
from collections import defaultdict
from pathlib import Path


class CrossReferenceAnalyzer(ast.NodeVisitor):
    """Analyze Python code for unused/undefined variables and functions."""

    def __init__(self, filename):
        self.filename = filename
        self.defined_names = defaultdict(list)  # name -> [(line, type)]
        self.used_names = defaultdict(list)      # name -> [line, ...]
        self.imports = defaultdict(list)         # name -> [line, ...]
        self.current_scope = None
        self.scopes = []  # Stack of scope names

    def visit_FunctionDef(self, node):
        """Track function definitions."""
        self.defined_names[node.name].append((node.lineno, 'function'))
        # Enter function scope
        self.scopes.append(node.name)
        self.current_scope = '.'.join(self.scopes)
        self.generic_visit(node)
        self.scopes.pop()
        self.current_scope = '.'.join(self.scopes) if self.scopes else None

    def visit_ClassDef(self, node):
        """Track class definitions."""
        self.defined_names[node.name].append((node.lineno, 'class'))
        # Enter class scope
        self.scopes.append(node.name)
        self.current_scope = '.'.join(self.scopes)
        self.generic_visit(node)
        self.scopes.pop()
        self.current_scope = '.'.join(self.scopes) if self.scopes else None

    def visit_Assign(self, node):
        """Track variable assignments."""
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_names[target.id].append((node.lineno, 'variable'))
            elif isinstance(target, ast.Attribute):
                # Track self.attribute assignments
                if isinstance(target.value, ast.Name) and target.value.id == 'self':
                    self.defined_names[f'self.{target.attr}'].append((node.lineno, 'attribute'))
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        """Track annotated assignments (e.g., x: int = 5)."""
        if isinstance(node.target, ast.Name):
            self.defined_names[node.target.id].append((node.lineno, 'variable'))
        self.generic_visit(node)

    def visit_Import(self, node):
        """Track imports."""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports[name].append(node.lineno)
            self.defined_names[name].append((node.lineno, 'import'))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Track from X import Y."""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            if name != '*':
                self.imports[name].append(node.lineno)
                self.defined_names[name].append((node.lineno, 'import'))
        self.generic_visit(node)

    def visit_Name(self, node):
        """Track name usage."""
        if isinstance(node.ctx, ast.Load):
            self.used_names[node.id].append(node.lineno)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Track attribute access (e.g., self.x)."""
        if isinstance(node.value, ast.Name) and node.value.id == 'self':
            if isinstance(node.ctx, ast.Load):
                self.used_names[f'self.{node.attr}'].append(node.lineno)
        self.generic_visit(node)

    def analyze(self):
        """Return analysis results."""
        # Find unused definitions
        unused = []
        for name, defs in self.defined_names.items():
            if name not in self.used_names:
                # Skip special names and imports (they might be used via module)
                if not name.startswith('_') and name not in self.imports:
                    for line, def_type in defs:
                        unused.append((name, line, def_type))

        # Find undefined references
        undefined = []
        builtins_names = dir(__builtins__)
        for name, uses in self.used_names.items():
            if name not in self.defined_names and name not in builtins_names:
                # Could be from import, module attribute, etc.
                if '.' not in name:  # Skip module.attribute patterns
                    for line in uses[:1]:  # Just first occurrence
                        undefined.append((name, line))

        return {
            'unused': sorted(unused, key=lambda x: x[1]),
            'undefined': sorted(undefined, key=lambda x: x[1]),
            'defined': dict(self.defined_names),
            'used': dict(self.used_names)
        }


def analyze_file(filepath):
    """Analyze a single Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source, filename=filepath)
        analyzer = CrossReferenceAnalyzer(filepath)
        analyzer.visit(tree)
        return analyzer.analyze()
    except SyntaxError as e:
        return {'error': f'Syntax error: {e}'}
    except Exception as e:
        return {'error': f'Error analyzing: {e}'}


def analyze_directory(dirpath, pattern='*.py', exclude_dirs=None):
    """Analyze all Python files in directory."""
    if exclude_dirs is None:
        exclude_dirs = {'__pycache__', '.git', 'venv', 'env', '.venv'}

    results = {}
    path = Path(dirpath)

    for pyfile in path.rglob(pattern):
        # Skip excluded directories
        if any(excluded in pyfile.parts for excluded in exclude_dirs):
            continue

        rel_path = pyfile.relative_to(path)
        results[str(rel_path)] = analyze_file(pyfile)

    return results


def print_results(results, show_undefined=True, show_unused=True):
    """Print analysis results."""
    total_unused = 0
    total_undefined = 0

    for filepath, analysis in sorted(results.items()):
        if 'error' in analysis:
            print(f"\n{filepath}: {analysis['error']}")
            continue

        unused = analysis.get('unused', [])
        undefined = analysis.get('undefined', [])

        if not unused and not undefined:
            continue

        print(f"\n{'='*70}")
        print(f"File: {filepath}")
        print(f"{'='*70}")

        if show_unused and unused:
            print(f"\nUnused definitions ({len(unused)}):")
            for name, line, def_type in unused:
                print(f"  Line {line:4d}: {def_type:10s} '{name}'")
                total_unused += 1

        if show_undefined and undefined:
            print(f"\nPossibly undefined ({len(undefined)}):")
            for name, line in undefined:
                print(f"  Line {line:4d}: '{name}'")
                total_undefined += 1

    print(f"\n{'='*70}")
    print(f"Summary: {total_unused} unused, {total_undefined} possibly undefined")
    print(f"{'='*70}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Cross-reference analysis for Python code')
    parser.add_argument('path', help='File or directory to analyze')
    parser.add_argument('--no-undefined', action='store_true', help='Hide undefined references')
    parser.add_argument('--no-unused', action='store_true', help='Hide unused definitions')
    parser.add_argument('--pattern', default='*.py', help='File pattern (default: *.py)')

    args = parser.parse_args()

    path = Path(args.path)

    if path.is_file():
        results = {str(path): analyze_file(path)}
    else:
        results = analyze_directory(path, pattern=args.pattern)

    print_results(results,
                 show_undefined=not args.no_undefined,
                 show_unused=not args.no_unused)
