# Code Behavior Issues - v19

Generated: 2025-11-10
Source: docs_inconsistencies_report-v19.md
Category: Code behavior changes needed (bugs, incorrect logic, missing features)

## 🔴 High Severity

### Code vs Comment inconsistency

**Description:** The numbered line editing feature has extensive validation and error handling in comments, but the actual implementation may fail silently or with unclear errors if UI integration is incomplete

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Comment describes required UI integration:
"# This feature requires the following UI integration:
# - interpreter.interactive_mode must reference the UI object (checked with hasattr)
# - UI.program must have add_line() and delete_line() methods (validated, returns error tuple if missing)
# - UI._refresh_editor() method to update the display (optional, checked with hasattr)
# - UI._highlight_current_statement() for restoring execution highlighting (optional, checked with hasattr)
# If interactive_mode doesn't exist or is falsy, returns (False, error_message) tuple.
# If interactive_mode exists but required program methods are missing, returns (False, error_message) tuple."

Code implementation:
if hasattr(self.interpreter, 'interactive_mode') and self.interpreter.interactive_mode:
    ui = self.interpreter.interactive_mode
    if not hasattr(ui, 'program') or not ui.program:
        return (False, "Cannot edit program lines: UI program manager not available\n")
    if line_content and not hasattr(ui.program, 'add_line'):
        return (False, "Cannot edit program lines: add_line method not available\n")
    if not line_content and not hasattr(ui.program, 'delete_line'):
        return (False, "Cannot edit program lines: delete_line method not available\n")

The validation is thorough, but the comment claims validation happens for all required methods, yet _refresh_editor() and _highlight_current_statement() are only checked with hasattr before use, not validated upfront. This could lead to silent failures if these methods are missing.

---

### Code behavior issue

**Description:** CONT docstring says editing clears stopped flag, but clear_execution_state() explicitly does NOT clear stopped flag

**Affected files:**
- `src/interactive.py`

**Details:**
cmd_cont() docstring (line 330-342) says:
"IMPORTANT: CONT will fail with '?Can't continue' if the program has been edited (lines added, deleted, or renumbered) because editing clears the GOSUB/RETURN and FOR/NEXT stacks to prevent crashes from invalidated return addresses and loop contexts."

But clear_execution_state() (line 169-182) explicitly says:
"Note: We do NOT clear the stopped flag here. The stopped flag is checked by CONT to determine if there's anything to continue. When the program is edited, CONT will still see stopped=True but will fail because the PC and execution state are now invalid (this is the intended behavior documented in cmd_cont())."

The CONT docstring implies editing makes CONT fail, but the mechanism is NOT clearing the stopped flag - it's that the PC/stacks become invalid while stopped flag remains true.

---

### Code behavior issue

**Description:** Comment states CLEAR silently ignores file close errors, but code only catches OSError and IOError, not all exceptions

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1240 states:
# Close all open files
# Note: Errors during file close are silently ignored to match MBASIC behavior.
# This differs from RESET which allows errors to propagate to the caller.
# We catch OSError and IOError specifically to avoid hiding programming errors.

Code at line ~1245:
try:
    file_obj = self.runtime.files[file_num]
    if hasattr(file_obj, 'close'):
        file_obj.close()
except (OSError, IOError):
    # Silently ignore file close errors (e.g., already closed, permission denied)
    pass

The comment says 'Errors during file close are silently ignored' but then says 'We catch OSError and IOError specifically to avoid hiding programming errors'. This is contradictory - if we're avoiding hiding programming errors, then we're NOT silently ignoring all errors. The comment should clarify that only OS-level file errors are ignored, not programming errors like AttributeError.

---

### Code behavior issue

**Description:** Comment in execute_cont() describes inconsistent behavior between STOP and Break handling

**Affected files:**
- `src/interpreter.py`

**Details:**
The comment states:
'Note: execute_stop() moves NPC to PC for resume, while BreakException handler does not update PC, which affects whether CONT can resume properly.'

This indicates a behavioral inconsistency where STOP and Break (Ctrl+C) are supposed to behave the same (both set stopped=True and halted=True) but handle PC differently, potentially breaking CONT after Break. This is either a code bug or the comment is misleading about them having the same behavior.

---

### Code bug

**Description:** Comment claims _sync_program_to_editor() is called in start() but this method doesn't exist in the provided code

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In start() method around line ~315:
if self.program.has_lines():
    if not self.editor_lines:
        self._sync_program_to_editor()

The method _sync_program_to_editor() is called but never defined in the provided code. This would cause a runtime AttributeError.

---

### Code bug

**Description:** Comment in _sync_program_to_runtime claims PC is reset when paused at breakpoint to 'prevent accidental resumption', but _debug_continue() doesn't exist in this file

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1176:
# PC handling:
# - If running and not paused at breakpoint: Preserves PC and execution state
# - If paused at breakpoint: Resets PC to halted (prevents accidental resumption)
# - If not running: Resets PC to halted for safety
...
# When paused at a breakpoint, the PC is
# intentionally reset; when the user continues via _debug_continue(), the
# interpreter's state already has the correct PC.

The method _debug_continue() is referenced but does not appear anywhere in this file (part 4). This suggests either the comment is outdated or the implementation is incomplete.

---

### Code bug

**Description:** Comment claims lines match program manager's formatted output but char positions may not align

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1420 states: "Lines in the editor match the program manager's formatted output (see _refresh_editor). The char_start/char_end positions from runtime correspond to the displayed line text, so they are directly usable as Tk text indices."

This assumes perfect alignment between runtime's character positions and editor display positions. However, if the program manager adds any formatting (spacing, etc.) during _refresh_editor, the character positions from runtime may not match the editor's text indices. This could cause incorrect highlighting.

---

### Code issue

**Description:** Comment claims BASIC statements can start with digits but code treats digit-starting lines as numbered program lines during paste

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line ~1014 comment: "# In this context, we assume lines starting with digits are numbered program lines (e.g., '10 PRINT').
# Note: While BASIC statements can start with digits (numeric expressions), when pasting
# program code, lines starting with digits are conventionally numbered program lines."

This creates ambiguity: if a user pastes a line like '123+456' (a valid numeric expression), the code will treat '123' as a line number and '+456' as the code, which is incorrect. The comment acknowledges this issue but the code doesn't handle it.

---

### Code inconsistency

**Description:** Inconsistent handling of editor_lines: it's read for display but never populated, making those reads always return empty string

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _debug_step() around line ~770:
line_code = self.editor_lines.get(state.current_line, "")
self.output_buffer.append(f"→ Paused at {pc_display}: {line_code}")

In _debug_step_line() around line ~850:
line_code = self.editor_lines.get(state.current_line, "")
self.output_buffer.append(f"→ Paused at {pc_display}: {line_code}")

Since editor_lines is never populated (only initialized as {}), these will always show empty code. The code should likely be reading from self.editor.lines or self.program.lines instead.

---

### Code inconsistency

**Description:** Inconsistent handling of immediate mode status updates after errors

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _setup_program() at line ~1074, when parse error occurs:
"Don't update immediate status here - error is displayed in output"
return False

But at line ~1168, after startup error:
self._update_output()
"Don't update immediate status on exception - error is in output"
return False

Yet in _execute_tick() at lines ~1207, ~1224, ~1226, ~1243, immediate status IS updated after errors:
self._update_output()
"Don't update immediate status here - error is displayed in output"
self._update_immediate_status()  # <-- This contradicts the comment

This inconsistency suggests either the comments are wrong or the code behavior is inconsistent.

---

### Code behavior issue

**Description:** Comment describes ESC during INPUT as setting stopped=True and running=False, but code actually sets runtime.stopped=True and self.running=False, which are different semantics

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1047:
# Note: This sets stopped=True and running=False. While similar to a BASIC STOP
# statement, the semantics differ - STOP is a deliberate program action that can
# be continued with CONT, while ESC is user cancellation that stops the UI tick loop.

Code at line ~1053:
if result is None:
    # Stop execution - PC already contains the position for CONT to resume from
    self.runtime.stopped = True
    self.running = False

The comment says 'ESC is user cancellation that stops the UI tick loop' and 'semantics differ' from STOP, but the code sets runtime.stopped=True which is exactly what STOP does. The comment at line 1053 even says 'PC already contains the position for CONT to resume from', which contradicts the claim that semantics differ.

---

## 🟡 Medium Severity

### Code implementation issue

**Description:** InputStatementNode.suppress_question field is documented as parsed but not implemented

**Affected files:**
- `src/ast_nodes.py`

**Details:**
InputStatementNode docstring states: 'Note: The suppress_question field is parsed by the parser when INPUT; (semicolon immediately after INPUT) is used, but it is NOT currently checked by the interpreter. Current behavior: "?" is always displayed (either "? " alone or "prompt? ").' This indicates the field exists in the AST but the interpreter doesn't use it, creating a gap between parsed structure and runtime behavior.

---

### Code implementation issue

**Description:** execute_step() docstring claims 'PARTIALLY IMPLEMENTED' but provides no actual stepping functionality

**Affected files:**
- `src/interpreter.py`

**Details:**
The docstring states:
'STEP is intended to execute one or more statements, then pause.

CURRENT STATUS: This method outputs an informational message but does NOT actually perform stepping. It's a partial implementation that acknowledges the command but doesn't execute the intended behavior.'

The method only outputs a message and does nothing else. This is more accurately 'NOT IMPLEMENTED' or 'STUB' rather than 'PARTIALLY IMPLEMENTED'. The comment also mentions tick_pc() has working step infrastructure but this command isn't connected to it, suggesting incomplete integration.

---

### Code issue

**Description:** execute_list() comment warns about potential sync issues but provides no mechanism to detect or handle them

**Affected files:**
- `src/interpreter.py`

**Details:**
The comment states:
'Implementation note: Outputs from line_text_map (original source text), not regenerated from AST. This preserves original formatting/spacing/case. The line_text_map is maintained by ProgramManager and should be kept in sync with the AST during program modifications (add_line, delete_line, RENUM, MERGE). If ProgramManager fails to maintain this sync, LIST output may show stale or incorrect line text.'

The code has no validation to check if line_text_map is in sync with the AST, and no error handling for when they diverge. This is a potential silent data corruption issue that the comment acknowledges but the code doesn't address.

---

### Code implementation issue

**Description:** InMemoryFileHandle.flush() docstring claims it's a no-op and content is only saved on close(), but the code actually calls file_obj.flush() which could have side effects

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
Docstring says: "Note: This calls StringIO/BytesIO flush() which are no-ops.
Content is only saved to the virtual filesystem on close()."

Code implementation:
def flush(self):
    if hasattr(self.file_obj, 'flush'):
        self.file_obj.flush()

The comment is technically correct that StringIO/BytesIO flush() are no-ops, but the docstring's phrasing "Content is only saved to the virtual filesystem on close()" could be misleading since flush() does execute code (even if it's a no-op). The hasattr check also suggests defensive programming that contradicts the certainty of the comment.

---

### Code behavior issue

**Description:** cmd_chain() docstring says 'MERGE or ALL: saves all variables' but implementation shows they have different semantics in MBASIC

**Affected files:**
- `src/interactive.py`

**Details:**
cmd_chain() docstring (line 509-512) says:
"# Save variables based on CHAIN options:
# - MERGE or ALL: saves all variables (both flags have identical behavior for variable preservation)
# - Neither: passes only COMMON variables (resolves type suffixes if needed)"

This comment claims MERGE and ALL have 'identical behavior for variable preservation', but in MBASIC 5.21:
- MERGE means merge program lines (overlay)
- ALL means pass all variables

These are orthogonal options - you can have CHAIN MERGE without ALL (merge lines but only pass COMMON vars), or CHAIN with ALL but not MERGE (replace program but pass all vars).

The implementation (lines 514-520) treats them identically for variable preservation, which may not match MBASIC spec.

---

### Code behavior issue

**Description:** Comment about RUN without args says 'signal that restart is needed' but doesn't explain who should restart

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1680 states:
# In non-interactive context, signal that restart is needed
# Note: RUN without args sets halted=True to stop current execution,
# signaling the caller (e.g., UI tick loop) that it should restart
# execution from the beginning if desired. This is different from
# RUN line_number which sets halted=False to continue execution inline.
# The caller is responsible for actually restarting execution.

The comment says 'The caller is responsible for actually restarting execution' but doesn't explain how the caller knows to restart vs. just stopping. Is there a flag? Should the caller check if halted was set by RUN vs. END? This is unclear.

---

### Code implementation issue

**Description:** Comment about RENUM says 'TODO: Implement RENUM' but code delegates to interactive_mode

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1840 states:
TODO: Implement RENUM to modify AST directly.
This is complex because it needs to:
1. Renumber lines in line_asts
2. Update statement_table PC keys
3. Update GOTO/GOSUB/ON GOTO target line numbers in AST nodes
4. Update RESTORE line number references

For now, delegate to interactive_mode.cmd_renum if available.

The code then delegates to interactive_mode.cmd_renum, which suggests RENUM IS implemented (in interactive_mode), but the TODO comment suggests it's not. This is confusing - is the TODO about implementing it in the interpreter directly (not via delegation), or is it truly not implemented? The comment should clarify.

---

### Code behavior issue

**Description:** Module docstring claims only RND and INKEY$ can be called without parentheses, but code shows this is a general MBASIC feature for specific functions

**Affected files:**
- `src/parser.py`

**Details:**
Module docstring says:
"Exception: Only RND and INKEY$ can be called without parentheses in MBASIC 5.21
(this is specific to these two functions, not a general MBASIC feature)"

But in parse_builtin_function():
"# RND can be called without parentheses - MBASIC 5.21 compatibility feature"
"# INKEY$ can be called without parentheses - MBASIC 5.21 compatibility feature"

The phrasing suggests this is a special case for these two functions, but the implementation treats it as a compatibility feature. The distinction between 'specific to these functions' vs 'compatibility feature' is unclear.

---

### Code implementation issue

**Description:** apply_keyword_case_policy has 'preserve' policy that returns keyword.capitalize() as fallback, but the comment says 'This fallback shouldn\'t normally execute in correct usage.' This suggests the function may not fully implement the preserve policy.

**Affected files:**
- `src/position_serializer.py`

**Details:**
Code for preserve policy:
    elif policy == "preserve":
        # The "preserve" policy is typically handled at a higher level (keywords passed with
        # original case preserved). If this function is called with "preserve" policy, we
        # return the keyword as-is if already properly cased, or capitalize as a safe default.
        # Note: This fallback shouldn\'t normally execute in correct usage.
        return keyword.capitalize()

The comment admits this is a fallback that shouldn't execute, suggesting the preserve policy isn't fully implemented at this level. The function always returns keyword.capitalize() for preserve, which doesn't actually preserve anything.

---

### Code implementation issue

**Description:** BREAK command docstring says breakpoints can be set 'at any time' but implementation checks if line exists

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
cmd_break() docstring states: 'Breakpoints can be set at any time (before or during execution).'

However, the implementation includes:
if line_num in self.interactive.program.lines:
    self.breakpoints.add(line_num)
else:
    self.interactive.io_handler.output(f'Line {line_num} does not exist')

This means breakpoints can only be set on existing lines, not 'at any time'. If a user tries to set a breakpoint on line 100 before writing that line, it will fail. The docstring should clarify that breakpoints can only be set on existing program lines.

---

### Code implementation issue

**Description:** Code implementation shows SINGLE and DOUBLE types are supported but documentation claims only INTEGER

**Affected files:**
- `src/codegen_backend.py`

**Details:**
Class docstring for Z88dkCBackend says:
"Supports:
- Integer variables (BASIC ! suffix maps to C int)
- FOR/NEXT loops
- PRINT statements for integers

Future:
- String support (requires runtime library)
- Arrays
- More complex expressions"

But the code actually implements SINGLE and DOUBLE types in _generate_variable_declarations() with float and double C types, and get_compiler_command() includes '-lm' flag for math library. The documentation is outdated - floating point IS supported, not just integers.

---

### Code bug

**Description:** Backward compatibility alias comment claims get_char() was non-blocking, but input_char() is called with blocking=False which suggests the original may have had a blocking parameter

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Comment says: "The original get_char() implementation was non-blocking, so this preserves that behavior for backward compatibility."

But the method signature is:
def get_char(self):
    return self.input_char(blocking=False)

This suggests get_char() never had a blocking parameter, yet the comment emphasizes preserving non-blocking behavior as if there was a choice.

---

### Code bug

**Description:** Fallback warning for Windows without msvcrt says input() 'Returns the entire line, not just one character' but then the code only returns first character

**Affected files:**
- `src/iohandler/console.py`

**Details:**
Warning message: "msvcrt not available on Windows - input_char() falling back to input() (waits for Enter, not single character)"

But the code does:
line = input()
return line[:1] if line else ""

The warning says it returns the entire line, but the code explicitly returns only the first character with line[:1]. The warning is misleading.

---

## 🟢 Low Severity

### Code implementation gap

**Description:** CallStatementNode.arguments field documented as unused but present in implementation

**Affected files:**
- `src/ast_nodes.py`

**Details:**
CallStatementNode has an 'arguments' field with extensive documentation: 'Implementation Note: The \'arguments\' field is currently unused (always empty list). It exists for potential future support of BASIC dialects that allow CALL with arguments (e.g., CALL ROUTINE(args)). Standard MBASIC 5.21 only accepts a single address expression in the \'target\' field. Code traversing the AST can safely ignore the \'arguments\' field for MBASIC 5.21 programs.' This is future-proofing that may confuse current users.

---

### Code implementation issue

**Description:** Comment about GOSUB return stack size doesn't match potential usage

**Affected files:**
- `src/codegen_backend.py`

**Details:**
Line in _generate() method:
code.append(self.indent() + 'int gosub_stack[100];  /* Return line numbers */')

The stack is hardcoded to size 100, but there's no check in _generate_gosub() or _generate_return() to prevent stack overflow if a program has deeply nested GOSUBs. The comment says it stores return line numbers, but the code actually stores return IDs (integers 0, 1, 2...) not actual BASIC line numbers. The comment is misleading.

---

### Code implementation issue

**Description:** Comment about GOSUB return mechanism is incomplete

**Affected files:**
- `src/codegen_backend.py`

**Details:**
In _generate_gosub() method:
code.append(self.indent() + f'gosub_stack[gosub_sp++] = {return_id};  /* Push return address */')

Comment says "Push return address" but it's pushing a return_id (integer counter), not an address. The actual return mechanism uses a switch statement in _generate_return() to jump to labels. The comment oversimplifies the implementation.

---

### Code implementation issue

**Description:** Comment about FOR loop comparison operator is incomplete

**Affected files:**
- `src/codegen_backend.py`

**Details:**
In _generate_for() method:
# Determine comparison operator based on step
if stmt.step_expr:
    # If step is negative, use >= instead of <=
    # For now, assume positive step (TODO: handle negative steps)
    comp = '<='
else:
    comp = '<='

The comment says "If step is negative, use >= instead of <=" but the code always uses '<=' regardless. The TODO indicates this is known incomplete functionality, but the comment is misleading about what the code actually does.

---

### Code inconsistency

**Description:** Inconsistent handling of missing JSON keys - some use if/else with defaults, others just use defaults

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Most keybindings use pattern:
_key_from_json = _get_key('editor', 'action')
KEY = _ctrl_key_to_urwid(_key_from_json) if _key_from_json else 'ctrl x'

But some keys like CLEAR_BREAKPOINTS_KEY, DELETE_LINE_KEY, RENUMBER_KEY, INSERT_LINE_KEY, STOP_KEY, SETTINGS_KEY, MAXIMIZE_OUTPUT_KEY are hardcoded without checking JSON at all. This creates inconsistency in which keys can be configured via JSON.

---

### Code duplication

**Description:** CONTROL_CHARS dictionary at end of file is never used and duplicates logic already in key_to_char() function

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
At line ~320:
CONTROL_CHARS = {
    f'Ctrl+{chr(ord("A") + i)}': chr(i + 1)
    for i in range(26)
}

This dictionary is marked as 'for testing and documentation' but is never imported or used anywhere. The same conversion logic exists in key_to_char() and _ctrl_key_to_char() functions.

---

### Code implementation issue

**Description:** Comment about array_base validation contradicts defensive else clause

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _edit_array_element method around line 680:
Comment says: '# OPTION BASE only allows 0 or 1 (validated by OPTION statement parser).\n# The else clause is defensive programming for unexpected values.'

Then the code has:
if array_base == 0:
    default_subscripts = ','.join(['0'] * len(dimensions))
elif array_base == 1:
    default_subscripts = ','.join(['1'] * len(dimensions))
else:
    # Defensive fallback for invalid array_base (should not occur)
    default_subscripts = ','.join(['0'] * len(dimensions))

The comment claims OPTION BASE validation ensures only 0 or 1, making the else clause unreachable. However, if validation is truly complete, the else clause is dead code. If the else clause is needed for defensive programming, then validation might not be complete. This creates logical inconsistency about whether the else clause can ever execute.

---

## Summary

- Total code behavior issues: 30
- High severity: 14
- Medium severity: 13
- Low severity: 3
