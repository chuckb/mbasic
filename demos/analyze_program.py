#!/usr/bin/env python3
"""
MBASIC Program Analyzer

Analyzes a BASIC program and produces a comprehensive optimization report.
Shows all detected optimization opportunities without running the program.

Usage:
    python3 analyze_program.py <program.bas>
    python3 analyze_program.py <program.bas> --summary
    python3 analyze_program.py <program.bas> --json
"""

import sys
import json
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from lexer import tokenize
from parser import Parser
from semantic_analyzer import SemanticAnalyzer


def analyze_file(filename, output_format='full'):
    """Analyze a BASIC file and return optimization report"""
    try:
        with open(filename, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    try:
        # Tokenize
        tokens = tokenize(code)

        # Parse
        parser = Parser(tokens)
        program = parser.parse()

        # Analyze
        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(program)

        if not success:
            print("Semantic analysis failed with errors:")
            for error in analyzer.errors:
                print(f"  {error}")
            return None

        # Generate report based on format
        if output_format == 'json':
            return generate_json_report(analyzer)
        elif output_format == 'summary':
            return generate_summary_report(analyzer)
        else:
            return analyzer.get_report()

    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_summary_report(analyzer):
    """Generate a concise summary of optimizations"""
    lines = []
    lines.append("=" * 70)
    lines.append("OPTIMIZATION SUMMARY")
    lines.append("=" * 70)
    lines.append("")

    # Count loop invariants
    loop_invariant_count = 0
    for loop in analyzer.loops.values():
        loop_invariant_count += len(loop.invariants)

    # Count optimizations
    counts = {
        "Constant Folding": len(analyzer.folded_expressions),
        "Common Subexpressions": len(analyzer.common_subexpressions),
        "Strength Reductions": len(analyzer.strength_reductions),
        "Copy Propagations": len([cp for cp in analyzer.copy_propagations if cp.propagation_count > 0]),
        "Forward Substitutions": len([fs for fs in analyzer.forward_substitutions if fs.can_substitute]),
        "Dead Stores": len([fs for fs in analyzer.forward_substitutions if fs.use_count == 0]),
        "Branch Optimizations": len([bo for bo in analyzer.branch_optimizations if bo.is_constant]),
        "Loop Invariants": loop_invariant_count,
        "Induction Variables": len([iv for iv in analyzer.induction_variables if iv.is_primary]),
        "Strength Reduction (IV)": sum(iv.strength_reduction_opportunities for iv in analyzer.induction_variables),
        "Uninitialized Warnings": len(analyzer.uninitialized_warnings),
        "Expression Reassociations": len(analyzer.expression_reassociations),
        "Algebraic Simplifications": len([sr for sr in analyzer.strength_reductions
                                          if 'identity' in sr.reduction_type or
                                          'AND' in sr.reduction_type or
                                          'OR' in sr.reduction_type or
                                          'NOT' in sr.reduction_type]),
    }

    lines.append("Optimization Opportunities Found:")
    lines.append("")

    total = 0
    for name, count in counts.items():
        if count > 0:
            lines.append(f"  {name:.<50} {count:>3}")
            total += count

    lines.append("  " + "-" * 54)
    lines.append(f"  {'TOTAL':.<50} {total:>3}")
    lines.append("")

    # Program statistics
    lines.append("Program Statistics:")
    lines.append("")
    lines.append(f"  Variables: {len(analyzer.symbols.variables)}")
    lines.append(f"  Functions: {len(analyzer.symbols.functions)}")
    lines.append(f"  Line Numbers: {len(analyzer.symbols.line_numbers)}")
    lines.append(f"  Loops Detected: {len(analyzer.loops)}")
    lines.append(f"  Subroutines: {len(analyzer.subroutines)}")
    lines.append("")

    # Recommendations
    if total > 0:
        lines.append("Recommendations:")
        lines.append("")

        if counts["Dead Stores"] > 0:
            lines.append(f"  • Remove {counts['Dead Stores']} unused assignment(s)")

        if counts["Forward Substitutions"] > 0:
            lines.append(f"  • Eliminate {counts['Forward Substitutions']} temporary variable(s)")

        if counts["Common Subexpressions"] > 0:
            lines.append(f"  • Reuse {counts['Common Subexpressions']} repeated computation(s)")

        if counts["Loop Invariants"] > 0:
            lines.append(f"  • Hoist {counts['Loop Invariants']} loop-invariant expression(s)")

        if counts["Strength Reduction (IV)"] > 0:
            lines.append(f"  • Apply {counts['Strength Reduction (IV)']} strength reduction(s) in loops")

        if counts["Uninitialized Warnings"] > 0:
            lines.append(f"  ⚠ Initialize {counts['Uninitialized Warnings']} variable(s) before use")

        lines.append("")

    lines.append("=" * 70)

    return "\n".join(lines)


def generate_json_report(analyzer):
    """Generate JSON-formatted report for programmatic use"""
    report = {
        "success": True,
        "statistics": {
            "variables": len(analyzer.symbols.variables),
            "functions": len(analyzer.symbols.functions),
            "line_numbers": len(analyzer.symbols.line_numbers),
            "loops": len(analyzer.loops),
            "subroutines": len(analyzer.subroutines),
        },
        "optimizations": {
            "constant_folding": [
                {"line": line, "expression": expr, "value": value}
                for line, expr, value in analyzer.folded_expressions
            ],
            "common_subexpressions": [
                {
                    "expression": cse.expression_desc,
                    "first_line": cse.first_line,
                    "occurrences": cse.occurrences,
                    "variables_used": list(cse.variables_used),
                    "temp_var": cse.temp_var_name
                }
                for cse in analyzer.common_subexpressions.values()
            ],
            "strength_reductions": [
                {
                    "line": sr.line,
                    "original": sr.original_expr,
                    "reduced": sr.reduced_expr,
                    "type": sr.reduction_type,
                    "savings": sr.savings
                }
                for sr in analyzer.strength_reductions
            ],
            "copy_propagations": [
                {
                    "line": cp.line,
                    "copy_var": cp.copy_var,
                    "source_var": cp.source_var,
                    "propagation_count": cp.propagation_count,
                    "propagated_lines": cp.propagated_lines
                }
                for cp in analyzer.copy_propagations
                if cp.propagation_count > 0
            ],
            "forward_substitutions": {
                "substitutable": [
                    {
                        "line": fs.line,
                        "variable": fs.variable,
                        "expression": fs.expression,
                        "use_line": fs.use_line
                    }
                    for fs in analyzer.forward_substitutions
                    if fs.can_substitute
                ],
                "dead_stores": [
                    {
                        "line": fs.line,
                        "variable": fs.variable,
                        "expression": fs.expression
                    }
                    for fs in analyzer.forward_substitutions
                    if fs.use_count == 0
                ]
            },
            "branch_optimizations": [
                {
                    "line": bo.line,
                    "condition": bo.condition,
                    "is_constant": bo.is_constant,
                    "always_true": bo.always_true,
                    "always_false": bo.always_false,
                    "unreachable_branch": bo.unreachable_branch
                }
                for bo in analyzer.branch_optimizations
                if bo.is_constant
            ],
            "uninitialized_warnings": [
                {
                    "line": w.line,
                    "variable": w.variable,
                    "context": w.context
                }
                for w in analyzer.uninitialized_warnings
            ],
        }
    }

    return json.dumps(report, indent=2)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    filename = sys.argv[1]

    # Check for output format flag
    output_format = 'full'
    if '--summary' in sys.argv:
        output_format = 'summary'
    elif '--json' in sys.argv:
        output_format = 'json'

    # Analyze the file
    report = analyze_file(filename, output_format)

    if report:
        print(report)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
