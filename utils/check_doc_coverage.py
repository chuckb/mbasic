#!/usr/bin/env python3
"""
Check documentation coverage for MBASIC language features.

Compares implemented functions, statements, and operators against
help documentation to identify missing docs.

Usage:
    python3 utils/check_doc_coverage.py
"""

import re
from pathlib import Path


def get_implemented_functions():
    """Extract all function names from basic_builtins.py."""
    builtin_file = Path('src/basic_builtins.py')
    if not builtin_file.exists():
        print(f"Error: {builtin_file} not found")
        return []

    content = builtin_file.read_text()
    # Match: def FUNCTION_NAME(self, ...)
    pattern = r'^\s+def ([A-Z_]+)\(self'
    functions = []
    for match in re.finditer(pattern, content, re.MULTILINE):
        func_name = match.group(1)
        # Convert internal names to BASIC names
        if func_name.endswith('_DOLLAR'):
            func_name = func_name[:-7] + '$'
        functions.append(func_name)

    return sorted(set(functions))


def get_implemented_statements():
    """Extract statement names from interpreter.py."""
    interp_file = Path('src/interpreter.py')
    if not interp_file.exists():
        print(f"Error: {interp_file} not found")
        return []

    content = interp_file.read_text()
    # Match: def execute_STATEMENT(self, ...)
    pattern = r'def execute_([a-z_]+)\(self'
    statements = []
    for match in re.finditer(pattern, content, re.MULTILINE):
        stmt = match.group(1).upper()
        # Skip internal methods
        if stmt not in ['STATEMENT', 'PROGRAM']:
            statements.append(stmt)

    return sorted(set(statements))


def get_documented_functions():
    """Get list of documented functions from help/common/language/functions/."""
    func_dir = Path('docs/help/common/language/functions')
    if not func_dir.exists():
        print(f"Error: {func_dir} not found")
        return []

    functions = []
    for md_file in func_dir.glob('*.md'):
        if md_file.name == 'index.md':
            continue
        func_name = md_file.stem.upper()
        # Convert filename conventions back to BASIC names
        func_name = func_name.replace('_DOLLAR', '$')

        # Handle multi-function docs (e.g., "cvi-cvs-cvd.md")
        if '-' in func_name:
            for part in func_name.split('-'):
                functions.append(part)
        else:
            functions.append(func_name)

    return sorted(set(functions))


def get_documented_statements():
    """Get list of documented statements from help/common/language/statements/."""
    stmt_dir = Path('docs/help/common/language/statements')
    if not stmt_dir.exists():
        print(f"Error: {stmt_dir} not found")
        return []

    statements = []
    for md_file in stmt_dir.glob('*.md'):
        if md_file.name == 'index.md':
            continue
        # Handle compound statement names like "for-next.md"
        stmt_name = md_file.stem.upper().replace('-', '/')
        statements.append(stmt_name)

    return sorted(set(statements))


def main():
    print("=" * 80)
    print("MBASIC Documentation Coverage Report")
    print("=" * 80)
    print()

    # Check functions
    print("📊 FUNCTIONS")
    print("-" * 80)
    impl_funcs = get_implemented_functions()
    doc_funcs = get_documented_functions()

    print(f"Implemented functions: {len(impl_funcs)}")
    print(f"Documented functions:  {len(doc_funcs)}")
    print()

    missing_docs = set(impl_funcs) - set(doc_funcs)
    extra_docs = set(doc_funcs) - set(impl_funcs)

    if missing_docs:
        print(f"❌ Missing documentation ({len(missing_docs)} functions):")
        for func in sorted(missing_docs):
            print(f"   - {func}")
        print()
    else:
        print("✅ All implemented functions are documented!")
        print()

    if extra_docs:
        print(f"⚠️  Documentation without implementation ({len(extra_docs)} functions):")
        for func in sorted(extra_docs):
            print(f"   - {func}")
        print()

    # Check statements
    print("📊 STATEMENTS")
    print("-" * 80)
    impl_stmts = get_implemented_statements()
    doc_stmts = get_documented_statements()

    print(f"Implemented statements: {len(impl_stmts)}")
    print(f"Documented statements:  {len(doc_stmts)}")
    print()

    # For statements, we need fuzzy matching because file names may not match exactly
    missing_stmt_docs = []
    for stmt in impl_stmts:
        # Check if any doc file matches this statement
        found = False
        for doc in doc_stmts:
            if stmt in doc or doc.replace('/', '_') == stmt:
                found = True
                break
        if not found:
            missing_stmt_docs.append(stmt)

    if missing_stmt_docs:
        print(f"❌ Missing documentation ({len(missing_stmt_docs)} statements):")
        for stmt in sorted(missing_stmt_docs):
            print(f"   - {stmt}")
        print()
    else:
        print("✅ All implemented statements are documented!")
        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total_missing = len(missing_docs) + len(missing_stmt_docs)
    if total_missing == 0:
        print("✅ Documentation is complete!")
    else:
        print(f"❌ {total_missing} items need documentation")
        print(f"   - {len(missing_docs)} functions")
        print(f"   - {len(missing_stmt_docs)} statements")
    print()


if __name__ == '__main__':
    main()
