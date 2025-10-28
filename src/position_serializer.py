"""
Position-Aware AST Serialization

Serializes AST nodes back to source text while preserving the original
token positions and spacing. Includes debug tracking for position conflicts.
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass
import ast_nodes


@dataclass
class PositionConflict:
    """Represents a position conflict during serialization"""
    token_text: str
    expected_column: int  # Where token says it should be
    actual_column: int    # Where we actually are in output
    node_type: str        # Type of AST node
    line_num: int         # Line number

    def __str__(self):
        return (f"Position conflict at line {self.line_num}: "
                f"'{self.token_text}' expects column {self.expected_column} "
                f"but output is at column {self.actual_column} "
                f"(node: {self.node_type})")


class PositionSerializer:
    """Serializes AST with position preservation and conflict tracking"""

    def __init__(self, debug=False):
        """Initialize serializer.

        Args:
            debug: If True, collect and report position conflicts
        """
        self.debug = debug
        self.conflicts: List[PositionConflict] = []
        self.current_column = 0
        self.current_line = 0

    def reset(self):
        """Reset serializer state for new line"""
        self.current_column = 0
        self.conflicts = []

    def emit_token(self, text, expected_column: Optional[int],
                   node_type: str = "unknown") -> str:
        """Emit a token at the expected column position.

        Args:
            text: Token text to emit (will be converted to string)
            expected_column: Column where token should appear (from original source)
            node_type: Type of AST node for debugging

        Returns:
            String with appropriate spacing + token text
        """
        # Convert to string if needed
        text = str(text)

        if expected_column is None:
            # No position info - use pretty printing (single space)
            result = " " + text if self.current_column > 0 else text
            self.current_column += len(result)
            return result

        # Calculate spacing needed
        if expected_column < self.current_column:
            # CONFLICT: Token expects to be earlier than current position
            if self.debug:
                conflict = PositionConflict(
                    token_text=text,
                    expected_column=expected_column,
                    actual_column=self.current_column,
                    node_type=node_type,
                    line_num=self.current_line
                )
                self.conflicts.append(conflict)

            # Strategy: Add single space to separate from previous token
            result = " " + text
            self.current_column += len(result)
            return result

        # Normal case: Add spaces to reach expected column
        spaces_needed = expected_column - self.current_column
        result = " " * spaces_needed + text
        self.current_column = expected_column + len(text)
        return result

    def serialize_line(self, line_node: ast_nodes.LineNode) -> Tuple[str, List[PositionConflict]]:
        """Serialize a complete line with position preservation.

        Args:
            line_node: LineNode to serialize

        Returns:
            Tuple of (serialized_text, list_of_conflicts)
        """
        self.reset()
        self.current_line = line_node.line_number

        # FAST PATH: If we have the original source text, use it directly!
        # This perfectly preserves all spacing, case, etc.
        if hasattr(line_node, 'source_text') and line_node.source_text:
            return line_node.source_text.strip(), []

        # FALLBACK: Reconstruct from AST (for generated/modified lines)
        # Start with line number
        line_num_text = str(line_node.line_number)
        output = self.emit_token(line_num_text, 0, "LineNumber")

        # Serialize each statement
        for stmt in line_node.statements:
            stmt_text = self.serialize_statement(stmt)
            output += stmt_text

        return output, self.conflicts.copy()

    def serialize_statement(self, stmt) -> str:
        """Serialize a statement node.

        Args:
            stmt: Statement node to serialize

        Returns:
            Serialized statement text (without leading spaces)
        """
        stmt_type = type(stmt).__name__

        if stmt_type == 'LetStatementNode':
            return self.serialize_let_statement(stmt)
        elif stmt_type == 'PrintStatementNode':
            return self.serialize_print_statement(stmt)
        elif stmt_type == 'IfStatementNode':
            return self.serialize_if_statement(stmt)
        elif stmt_type == 'GotoStatementNode':
            return self.serialize_goto_statement(stmt)
        elif stmt_type == 'GosubStatementNode':
            return self.serialize_gosub_statement(stmt)
        elif stmt_type == 'ForStatementNode':
            return self.serialize_for_statement(stmt)
        elif stmt_type == 'NextStatementNode':
            return self.serialize_next_statement(stmt)
        elif stmt_type == 'RemarkStatementNode':
            return self.serialize_rem_statement(stmt)
        else:
            # Fallback: Use pretty printing from ui_helpers
            from ui.ui_helpers import serialize_statement
            return " " + serialize_statement(stmt)

    def serialize_let_statement(self, stmt: ast_nodes.LetStatementNode) -> str:
        """Serialize LET or assignment statement"""
        result = ""

        # Variable
        var_text = self.serialize_expression(stmt.variable)
        result += var_text

        # Equals sign (TODO: track operator position)
        result += self.emit_token("=", None, "LetOperator")

        # Expression
        expr_text = self.serialize_expression(stmt.expression)
        result += expr_text

        return result

    def serialize_print_statement(self, stmt: ast_nodes.PrintStatementNode) -> str:
        """Serialize PRINT statement"""
        result = self.emit_token("PRINT", stmt.column, "PrintKeyword")

        # File number if present
        if stmt.file_number:
            result += self.emit_token("#", None, "FileSigil")
            result += self.serialize_expression(stmt.file_number)
            result += self.emit_token(",", None, "Comma")

        # Expressions with separators
        for i, expr in enumerate(stmt.expressions):
            result += self.serialize_expression(expr)
            if i < len(stmt.separators) and stmt.separators[i]:
                result += self.emit_token(stmt.separators[i], None, "Separator")

        return result

    def serialize_if_statement(self, stmt: ast_nodes.IfStatementNode) -> str:
        """Serialize IF statement"""
        result = self.emit_token("IF", stmt.column, "IfKeyword")
        result += self.serialize_expression(stmt.condition)
        result += self.emit_token("THEN", None, "ThenKeyword")

        # Direct THEN line number (e.g., IF X>5 THEN 100)
        if stmt.then_line_number is not None:
            result += self.emit_token(str(stmt.then_line_number), None, "LineNumber")
        # THEN statements
        elif stmt.then_statements:
            for i, then_stmt in enumerate(stmt.then_statements):
                if i > 0:
                    result += self.emit_token(":", None, "StatementSep")
                result += self.serialize_statement(then_stmt)

        # ELSE statements or line number
        if stmt.else_line_number is not None:
            result += self.emit_token("ELSE", None, "ElseKeyword")
            result += self.emit_token(str(stmt.else_line_number), None, "LineNumber")
        elif stmt.else_statements:
            result += self.emit_token("ELSE", None, "ElseKeyword")
            for i, else_stmt in enumerate(stmt.else_statements):
                if i > 0:
                    result += self.emit_token(":", None, "StatementSep")
                result += self.serialize_statement(else_stmt)

        return result

    def serialize_goto_statement(self, stmt: ast_nodes.GotoStatementNode) -> str:
        """Serialize GOTO statement"""
        result = self.emit_token("GOTO", stmt.column, "GotoKeyword")
        result += self.emit_token(str(stmt.line_number), None, "LineNumber")
        return result

    def serialize_gosub_statement(self, stmt: ast_nodes.GosubStatementNode) -> str:
        """Serialize GOSUB statement"""
        result = self.emit_token("GOSUB", stmt.column, "GosubKeyword")
        result += self.emit_token(str(stmt.line_number), None, "LineNumber")
        return result

    def serialize_for_statement(self, stmt: ast_nodes.ForStatementNode) -> str:
        """Serialize FOR statement"""
        result = self.emit_token("FOR", stmt.column, "ForKeyword")
        result += self.serialize_expression(stmt.variable)
        result += self.emit_token("=", None, "Equals")
        result += self.serialize_expression(stmt.start_expr)
        result += self.emit_token("TO", None, "ToKeyword")
        result += self.serialize_expression(stmt.end_expr)
        if stmt.step_expr:
            result += self.emit_token("STEP", None, "StepKeyword")
            result += self.serialize_expression(stmt.step_expr)
        return result

    def serialize_next_statement(self, stmt: ast_nodes.NextStatementNode) -> str:
        """Serialize NEXT statement"""
        result = self.emit_token("NEXT", stmt.column, "NextKeyword")
        if stmt.variables:
            for i, var in enumerate(stmt.variables):
                if i > 0:
                    result += self.emit_token(",", None, "Comma")
                result += self.serialize_expression(var)
        return result

    def serialize_rem_statement(self, stmt: ast_nodes.RemarkStatementNode) -> str:
        """Serialize REM statement"""
        result = self.emit_token("REM", stmt.column, "RemKeyword")
        if stmt.comment:
            # Preserve original comment spacing
            result += " " + stmt.comment
        return result

    def serialize_expression(self, expr) -> str:
        """Serialize an expression node.

        Args:
            expr: Expression node to serialize

        Returns:
            Serialized expression text
        """
        expr_type = type(expr).__name__

        if expr_type == 'NumberNode':
            return self.emit_token(expr.literal if hasattr(expr, 'literal') else str(expr.value),
                                  expr.column, "Number")

        elif expr_type == 'StringNode':
            return self.emit_token(f'"{expr.value}"', expr.column, "String")

        elif expr_type == 'VariableNode':
            # Use original case if available, otherwise fall back to normalized name
            text = getattr(expr, 'original_case', expr.name) or expr.name
            # Only add type suffix if explicit
            if expr.type_suffix and getattr(expr, 'explicit_type_suffix', False):
                text += expr.type_suffix
            # Add subscripts if present
            if expr.subscripts:
                text += "("
                for i, sub in enumerate(expr.subscripts):
                    if i > 0:
                        text += ","
                    text += self.serialize_expression(sub).strip()
                text += ")"
            return self.emit_token(text, expr.column, "Variable")

        elif expr_type == 'BinaryOpNode':
            result = ""
            result += self.serialize_expression(expr.left)

            # Operator token
            from tokens import TokenType
            op_map = {
                TokenType.PLUS: '+',
                TokenType.MINUS: '-',
                TokenType.MULTIPLY: '*',
                TokenType.DIVIDE: '/',
                TokenType.POWER: '^',
                TokenType.EQUAL: '=',
                TokenType.LESS_THAN: '<',
                TokenType.GREATER_THAN: '>',
                TokenType.LESS_EQUAL: '<=',
                TokenType.GREATER_EQUAL: '>=',
                TokenType.NOT_EQUAL: '<>',
                TokenType.AND: 'AND',
                TokenType.OR: 'OR',
                TokenType.XOR: 'XOR',
                TokenType.MOD: 'MOD',
                TokenType.BACKSLASH: '\\',
            }
            op_str = op_map.get(expr.operator, str(expr.operator))
            result += self.emit_token(op_str, None, "Operator")

            result += self.serialize_expression(expr.right)
            return result

        elif expr_type == 'UnaryOpNode':
            op_str = '-' if expr.operator == TokenType.MINUS else str(expr.operator)
            result = self.emit_token(op_str, expr.column, "UnaryOp")
            result += self.serialize_expression(expr.operand)
            return result

        elif expr_type == 'FunctionCallNode':
            result = self.emit_token(expr.name, expr.column, "FunctionName")
            if expr.arguments:
                result += self.emit_token("(", None, "LParen")
                for i, arg in enumerate(expr.arguments):
                    if i > 0:
                        result += self.emit_token(",", None, "Comma")
                    result += self.serialize_expression(arg)
                result += self.emit_token(")", None, "RParen")
            return result

        else:
            # Fallback: use pretty printing
            from ui.ui_helpers import serialize_expression
            return " " + serialize_expression(expr)


def serialize_line_with_positions(line_node: ast_nodes.LineNode, debug=False) -> Tuple[str, List[PositionConflict]]:
    """Convenience function to serialize a line with position preservation.

    Args:
        line_node: LineNode to serialize
        debug: If True, collect position conflict information

    Returns:
        Tuple of (serialized_text, list_of_conflicts)
    """
    serializer = PositionSerializer(debug=debug)
    return serializer.serialize_line(line_node)


def renumber_with_spacing_preservation(program_lines: dict, start: int, step: int, debug=False):
    """Renumber program lines while preserving spacing by surgically editing source_text.

    This implementation preserves exact spacing by finding and replacing line numbers
    in the source text, then adjusting all token positions accordingly.

    Args:
        program_lines: Dict of line_number -> LineNode
        start: New starting line number
        step: Increment between lines
        debug: If True, print debug information

    Returns:
        Dict of new_line_number -> LineNode (with updated source_text and positions)
    """
    import re

    # Build mapping of old -> new line numbers
    old_line_nums = sorted(program_lines.keys())
    line_num_map = {}
    new_num = start

    for old_num in old_line_nums:
        line_num_map[old_num] = new_num
        new_num += step

    # Process each line
    new_program_lines = {}

    for old_num in old_line_nums:
        line_node = program_lines[old_num]
        new_num = line_num_map[old_num]

        # Get original source text
        source = line_node.source_text if hasattr(line_node, 'source_text') else ""
        if not source:
            # No source text? Fall back to AST serialization
            line_node.line_number = new_num
            _update_line_refs_in_node(line_node, line_num_map)
            serializer = PositionSerializer(debug=debug)
            new_source_text, _ = serializer.serialize_line(line_node)
            line_node.source_text = new_source_text
            new_program_lines[new_num] = line_node
            continue

        # Strategy: Find all line numbers in source_text and replace them
        # Track replacements: [(start_pos, old_text, new_text), ...]
        replacements = []

        # 1. Replace line number at start
        old_line_str = str(old_num)
        new_line_str = str(new_num)

        # Line number is at the start, followed by space or statement
        match = re.match(r'^(\d+)(\s+)', source)
        if match:
            replacements.append((0, match.group(1), new_line_str))

        # 2. Find all line number references in the code BEFORE updating AST
        # Collect (old_line_num, new_line_num) pairs from the line_num_map
        line_num_refs_old = _collect_line_refs_before_update(line_node)

        # Update line number references in AST
        _update_line_refs_in_node(line_node, line_num_map)

        # For each old reference found, replace it in source text
        code_part = source[match.end():] if match else source
        code_start = match.end() if match else 0

        for ref_old in line_num_refs_old:
            if ref_old in line_num_map:
                ref_new = line_num_map[ref_old]
                # Find this line number in the code part
                # Use word boundary to avoid matching partial numbers
                pattern = r'\b' + str(ref_old) + r'\b'
                for m in re.finditer(pattern, code_part):
                    pos = code_start + m.start()
                    replacements.append((pos, str(ref_old), str(ref_new)))

        # Apply replacements from right to left to preserve positions
        replacements.sort(key=lambda x: x[0], reverse=True)

        new_source = source
        total_offset = 0  # Track cumulative offset for position adjustment

        for pos, old_text, new_text in replacements:
            new_source = new_source[:pos] + new_text + new_source[pos + len(old_text):]
            offset_change = len(new_text) - len(old_text)
            total_offset += offset_change

        # Update line node
        line_node.line_number = new_num
        line_node.source_text = new_source

        # Adjust all token positions in AST if line number at start changed length
        if match:
            line_num_offset = len(new_line_str) - len(old_line_str)
            if line_num_offset != 0:
                _adjust_token_positions(line_node, line_num_offset)

        new_program_lines[new_num] = line_node

    return new_program_lines


def _collect_line_refs_before_update(line_node):
    """Collect all line number references from a LineNode BEFORE updating.

    Returns set of line numbers that are referenced in this line.
    """
    refs = set()

    for stmt in line_node.statements:
        _collect_refs_from_statement(stmt, refs)

    return refs


def _collect_refs_from_statement(stmt, refs):
    """Recursively collect line number references from a statement.

    Args:
        stmt: Statement node to scan
        refs: Set to add line number references to
    """
    stmt_type = type(stmt).__name__

    if stmt_type == 'GotoStatementNode':
        refs.add(stmt.line_number)

    elif stmt_type == 'GosubStatementNode':
        refs.add(stmt.line_number)

    elif stmt_type == 'OnGotoStatementNode':
        refs.update(stmt.line_numbers)

    elif stmt_type == 'OnGosubStatementNode':
        refs.update(stmt.line_numbers)

    elif stmt_type == 'OnErrorStatementNode':
        if stmt.line_number:
            refs.add(stmt.line_number)

    elif stmt_type == 'RestoreStatementNode':
        if stmt.line_number:
            refs.add(stmt.line_number)

    elif stmt_type == 'ResumeStatementNode':
        if stmt.line_number:
            refs.add(stmt.line_number)

    elif stmt_type == 'IfStatementNode':
        # Direct THEN/ELSE line numbers
        if hasattr(stmt, 'then_line_number') and stmt.then_line_number:
            refs.add(stmt.then_line_number)
        if hasattr(stmt, 'else_line_number') and stmt.else_line_number:
            refs.add(stmt.else_line_number)

        # Recurse into THEN/ELSE statements
        if stmt.then_statements:
            for then_stmt in stmt.then_statements:
                _collect_refs_from_statement(then_stmt, refs)
        if stmt.else_statements:
            for else_stmt in stmt.else_statements:
                _collect_refs_from_statement(else_stmt, refs)

        # TODO: Handle ERL comparisons in condition
        # This is complex - would need to traverse expressions looking for ERL function calls


def _adjust_token_positions(line_node, offset):
    """Adjust all token column positions in a LineNode by the given offset.

    Args:
        line_node: The LineNode to adjust
        offset: Amount to shift columns (positive = right, negative = left)
    """
    # Adjust positions in all statements
    for stmt in line_node.statements:
        _adjust_statement_positions(stmt, offset)


def _adjust_statement_positions(stmt, offset):
    """Recursively adjust token positions in a statement.

    Args:
        stmt: Statement node to adjust
        offset: Amount to shift columns
    """
    # Adjust column if present
    if hasattr(stmt, 'column'):
        stmt.column += offset

    # Recurse into sub-structures
    stmt_type = type(stmt).__name__

    if stmt_type == 'AssignmentStatementNode':
        _adjust_expression_positions(stmt.variable, offset)
        _adjust_expression_positions(stmt.expression, offset)

    elif stmt_type in ['PrintStatementNode', 'InputStatementNode']:
        if hasattr(stmt, 'expressions'):
            for expr in stmt.expressions:
                _adjust_expression_positions(expr, offset)

    elif stmt_type == 'IfStatementNode':
        _adjust_expression_positions(stmt.condition, offset)
        if stmt.then_statements:
            for then_stmt in stmt.then_statements:
                _adjust_statement_positions(then_stmt, offset)
        if stmt.else_statements:
            for else_stmt in stmt.else_statements:
                _adjust_statement_positions(else_stmt, offset)

    elif stmt_type == 'ForStatementNode':
        _adjust_expression_positions(stmt.variable, offset)
        _adjust_expression_positions(stmt.start_expr, offset)
        _adjust_expression_positions(stmt.end_expr, offset)
        if stmt.step_expr:
            _adjust_expression_positions(stmt.step_expr, offset)

    elif stmt_type == 'NextStatementNode':
        if stmt.variables:
            for var in stmt.variables:
                _adjust_expression_positions(var, offset)

    elif stmt_type == 'DimStatementNode':
        for var in stmt.variables:
            _adjust_expression_positions(var, offset)

    elif stmt_type == 'OnGotoStatementNode' or stmt_type == 'OnGosubStatementNode':
        _adjust_expression_positions(stmt.expression, offset)


def _adjust_expression_positions(expr, offset):
    """Recursively adjust token positions in an expression.

    Args:
        expr: Expression node to adjust
        offset: Amount to shift columns
    """
    if not expr:
        return

    # Adjust column if present
    if hasattr(expr, 'column'):
        expr.column += offset

    expr_type = type(expr).__name__

    if expr_type == 'BinaryOpNode':
        _adjust_expression_positions(expr.left, offset)
        _adjust_expression_positions(expr.right, offset)

    elif expr_type == 'UnaryOpNode':
        _adjust_expression_positions(expr.operand, offset)

    elif expr_type == 'FunctionCallNode':
        if expr.arguments:
            for arg in expr.arguments:
                _adjust_expression_positions(arg, offset)

    elif expr_type == 'VariableNode':
        if expr.subscripts:
            for sub in expr.subscripts:
                _adjust_expression_positions(sub, offset)


def _update_line_refs_in_node(line_node, line_num_map):
    """Update all line number references in a LineNode's statements.

    Args:
        line_node: LineNode to update
        line_num_map: Dict mapping old line numbers to new ones
    """
    for stmt in line_node.statements:
        _update_line_refs_in_statement(stmt, line_num_map)


def _update_line_refs_in_statement(stmt, line_num_map):
    """Recursively update line number references in a statement.

    Args:
        stmt: Statement node to update
        line_num_map: Dict mapping old line numbers to new ones
    """
    stmt_type = type(stmt).__name__

    if stmt_type == 'GotoStatementNode':
        if stmt.line_number in line_num_map:
            stmt.line_number = line_num_map[stmt.line_number]

    elif stmt_type == 'GosubStatementNode':
        if stmt.line_number in line_num_map:
            stmt.line_number = line_num_map[stmt.line_number]

    elif stmt_type == 'OnGotoStatementNode':
        stmt.line_numbers = [line_num_map.get(ln, ln) for ln in stmt.line_numbers]

    elif stmt_type == 'OnGosubStatementNode':
        stmt.line_numbers = [line_num_map.get(ln, ln) for ln in stmt.line_numbers]

    elif stmt_type == 'OnErrorStatementNode':
        if stmt.line_number in line_num_map:
            stmt.line_number = line_num_map[stmt.line_number]

    elif stmt_type == 'RestoreStatementNode':
        if stmt.line_number and stmt.line_number in line_num_map:
            stmt.line_number = line_num_map[stmt.line_number]

    elif stmt_type == 'ResumeStatementNode':
        if stmt.line_number and stmt.line_number in line_num_map:
            stmt.line_number = line_num_map[stmt.line_number]

    elif stmt_type == 'IfStatementNode':
        # Handle THEN line_number (direct branch)
        if hasattr(stmt, 'then_line_number') and stmt.then_line_number:
            if stmt.then_line_number in line_num_map:
                stmt.then_line_number = line_num_map[stmt.then_line_number]
        # Handle ELSE line_number (direct branch)
        if hasattr(stmt, 'else_line_number') and stmt.else_line_number:
            if stmt.else_line_number in line_num_map:
                stmt.else_line_number = line_num_map[stmt.else_line_number]
        # Recurse into THEN/ELSE statements
        if hasattr(stmt, 'then_statements') and stmt.then_statements:
            for then_stmt in stmt.then_statements:
                _update_line_refs_in_statement(then_stmt, line_num_map)
        if hasattr(stmt, 'else_statements') and stmt.else_statements:
            for else_stmt in stmt.else_statements:
                _update_line_refs_in_statement(else_stmt, line_num_map)

        # Handle ERL comparisons in condition
        if hasattr(stmt, 'condition'):
            _update_erl_in_expression(stmt.condition, line_num_map)


def _update_erl_in_expression(expr, line_num_map):
    """Update ERL comparisons in expressions (e.g., IF ERL = 10 THEN).

    Args:
        expr: Expression node to check
        line_num_map: Dict mapping old line numbers to new ones
    """
    expr_type = type(expr).__name__

    if expr_type == 'BinaryOpNode':
        # Check if this is ERL comparison: ERL = line_number
        left_type = type(expr.left).__name__
        right_type = type(expr.right).__name__

        # ERL = number or number = ERL
        if left_type == 'FunctionCallNode' and expr.left.name.lower() == 'erl':
            if right_type == 'NumberNode':
                line_num = int(expr.right.value)
                if line_num in line_num_map:
                    expr.right.value = float(line_num_map[line_num])
        elif right_type == 'FunctionCallNode' and expr.right.name.lower() == 'erl':
            if left_type == 'NumberNode':
                line_num = int(expr.left.value)
                if line_num in line_num_map:
                    expr.left.value = float(line_num_map[line_num])

        # Recurse
        _update_erl_in_expression(expr.left, line_num_map)
        _update_erl_in_expression(expr.right, line_num_map)

    elif expr_type == 'UnaryOpNode':
        _update_erl_in_expression(expr.operand, line_num_map)
