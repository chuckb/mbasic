# Enhanced Consistency Report (Code + Documentation)

Generated: 2025-11-08 13:18:52
Analyzed: Source code (.py, .json) and Documentation (.md)

## 🔧 Code vs Comment Conflicts


## 📋 General Inconsistencies

### 🔴 High Severity

#### code_vs_comment

**Description:** Critical inconsistency in negative zero handling comment vs implementation

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line ~268: Comment says "Determine sign BEFORE rounding (for negative zero handling)" and "original_negative was captured before rounding (see above)". However, original_negative is assigned at line ~268 AFTER the precision check but BEFORE rounding at line ~271. The comment at line ~275 says "This allows us to detect cases like -0.001 which round to 0 but should display as '-0'". But if value=-0.001, then original_negative=True is set before rounding, then rounded=0. The logic at line ~277-281 checks if rounded==0 AND original_negative, setting is_negative=True. This appears correct, but the comment placement "see above" is confusing since original_negative is set just 3 lines earlier, not "above" in a meaningful way.

---

#### Code vs Documentation inconsistency

**Description:** SandboxedFileIO methods documented as STUB but list_files() is IMPLEMENTED

**Affected files:**
- `src/file_io.py`

**Details:**
The SandboxedFileIO class docstring states:
"Implementation status:
- list_files(): IMPLEMENTED - delegates to backend.sandboxed_fs
- load_file(): STUB - raises IOError (requires async refactor)
- save_file(): STUB - raises IOError (requires async refactor)
- delete_file(): STUB - raises IOError (requires async refactor)
- file_exists(): STUB - raises IOError (requires async refactor)"

However, the actual implementation shows:
- list_files() is implemented and delegates to backend.sandboxed_fs
- load_file() raises IOError with message about async refactor
- save_file() raises IOError with message about async refactor
- delete_file() raises IOError with message about async refactor
- file_exists() raises IOError with message about async refactor

The documentation correctly describes the implementation status. This is actually consistent, not an inconsistency.

---

#### code_vs_comment

**Description:** Comment describes ERL renumbering behavior that contradicts MBASIC manual specification

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~570 states: 'MBASIC manual specifies: if ERL appears on left side of comparison operator (=, <>, <, >, <=, >=), the right-hand number is a line number reference.'

But then at line ~573: 'IMPORTANT: Current implementation renumbers for ANY binary operator with ERL on left, including arithmetic (ERL + 100, ERL * 2). This is broader than the manual specifies.'

The comment acknowledges the code intentionally deviates from the manual specification. The _renum_erl_comparison() method at line ~595 checks for 'BinaryOpNode' without filtering by operator type, confirming it handles ALL binary operators, not just comparisons. This is documented as intentional but creates a discrepancy between stated spec and implementation.

---

#### code_vs_comment

**Description:** Comment about CLEAR error handling contradicts actual behavior

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1240 states:
"# Close all open files
# Note: Errors during file close are silently ignored (bare except: pass)"

The code shows:
try:
    file_obj = self.runtime.files[file_num]
    if hasattr(file_obj, 'close'):
        file_obj.close()
except:
    pass

This matches the comment. However, later at line ~1890 in execute_reset, there's a contrasting comment:
"# Close all open files (errors propagate to caller)"

And the code:
for file_num in list(self.runtime.files.keys()):
    self.runtime.files[file_num]['handle'].close()
    del self.runtime.files[file_num]

The comment in CLEAR says errors are silently ignored, and the comment in RESET says errors propagate. This is an intentional difference between the two statements, but the CLEAR comment should clarify this is different from RESET's behavior.

---

#### code_vs_comment

**Description:** serialize_let_statement docstring describes LET keyword handling but the implementation doesn't emit LET keyword at all

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring says: 'Serialize LET or assignment statement.

LetStatementNode represents both:
- Explicit LET statements: LET A=5
- Implicit assignments: A=5 (without LET keyword)'

But the implementation code:
```python
def serialize_let_statement(self, stmt: ast_nodes.LetStatementNode) -> str:
    result = ""
    # Variable
    var_text = self.serialize_expression(stmt.variable)
    result += var_text
    # Equals sign
    result += self.emit_token("=", None, "LetOperator")
```

There is NO code that emits the 'LET' keyword. The function always serializes as implicit assignment (A=5) regardless of whether the original had LET or not. This is a significant behavior mismatch.

---

#### Code vs Documentation inconsistency

**Description:** The auto_save.py module is fully implemented with comprehensive autosave functionality, but there is no evidence in the other UI files (cli.py, curses_settings_widget.py, base.py) that this autosave functionality is actually integrated or used by any UI backend.

**Affected files:**
- `src/ui/auto_save.py`

**Details:**
auto_save.py provides:
- AutoSaveManager class with full implementation
- Emacs-style #filename# naming
- Recovery prompts
- Cleanup functionality

But none of the UI backend files (cli.py, base.py) show any imports or usage of AutoSaveManager. The feature appears to be implemented but not integrated into the actual UI backends.

---

#### code_vs_comment

**Description:** Comment says BASIC code can never start with digit, but this is incorrect

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _parse_line_numbers method:
"# FIRST: Check if line starts with a digit (raw pasted BASIC)
# Since BASIC code can never legally start with a digit, this must be a line number
if line[0].isdigit():"

This is FALSE. BASIC code CAN start with a digit in several cases:
1. Numeric constants: '123' as a statement (though unusual)
2. Numeric expressions in immediate mode
3. Line continuation or multi-statement lines

The code assumes any line starting with a digit is a line number, which could cause incorrect parsing of valid BASIC code. This is a potential code bug masked by an incorrect comment.

---

#### code_vs_comment

**Description:** Comment claims _sync_program_to_runtime resets PC when paused_at_breakpoint=True, but explanation contradicts typical breakpoint resume behavior

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _sync_program_to_runtime method:
"# Restore PC only if execution is running AND not paused at breakpoint
# When paused_at_breakpoint=True, we reset PC to halted because the breakpoint PC
# is stored separately and will be restored when continuing from the breakpoint."

This comment suggests breakpoint PC is stored separately and will be restored later, but there's no visible code in this method or nearby that shows where this separate storage happens or how restoration works. This needs clarification about the breakpoint resume mechanism.

---

#### code_vs_comment_conflict

**Description:** Comment claims help navigation keys are hardcoded and not loaded from keybindings, but the code actually does load keybindings via HelpMacros

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at line ~90 states:
"Note: Help navigation keys are hardcoded here and in keypress() method, not loaded from keybindings. The help widget uses fixed keys (U for back, / for search, ESC/Q to exit) to avoid dependency on keybinding configuration. HelpMacros does load the full keybindings from JSON (for {{kbd:action}} macro expansion in help content), but the help widget itself doesn't use those loaded keybindings."

However, HelpWidget.__init__ creates HelpMacros instance:
self.macros = HelpMacros('curses', help_root)

And HelpMacros._load_keybindings() does load keybindings from JSON:
keybindings_path = Path(__file__).parent / f"{self.ui_name}_keybindings.json"

The comment is technically correct that help_widget.py doesn't use the loaded keybindings for its own navigation (it uses hardcoded keys in keypress()), but the phrasing is confusing since HelpMacros is instantiated within HelpWidget.

---

#### code_vs_comment_conflict

**Description:** MAINTENANCE comment lists 3 places to update but implementation has more locations

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at line ~90:
"MAINTENANCE: If help navigation keys change, update:
1. This footer text (line below)
2. The keypress() method (handle_key mapping around line 150+)
3. Help documentation that mentions these keys"

But the footer text appears in multiple places:
1. Line ~92: Initial footer in __init__
2. Line ~127: Footer in _cancel_search()
3. Line ~138: Footer in _execute_search() when no results
4. Line ~165: Footer in _execute_search() with results

The maintenance comment only mentions 'this footer text' but there are 4 different footer text assignments with hardcoded keys.

---

#### code_vs_comment

**Description:** _ImmediateModeToken docstring references wrong line number for usage

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines 20-26 docstring states:
"""Token for variable edits from immediate mode or variable editor.

This class is instantiated when editing variables via the variable inspector
(see _on_variable_edit() around line 1194). Used to mark variable changes that
originate from the variable inspector or immediate mode, not from program
execution. The line=-1 signals to runtime.set_variable() that this is a
debugger/immediate mode edit.
"""

The comment references '_on_variable_edit() around line 1194' but the provided code only goes up to line 1194 (incomplete file). The method _on_variable_edit is not visible in the provided excerpt, so the line number cannot be verified. This is likely outdated after code refactoring.

---

#### code_vs_comment

**Description:** Comment claims control characters modify text via deletion, but backspace/delete are not control characters in the traditional sense

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1048: 'Allow control characters (backspace, delete) - these modify text via deletion, not by inserting printable characters, so they pass validation'
Code: 'if char_code in (8, 127):  # Backspace (0x08) or Delete (0x7F)'
Backspace (0x08) and Delete (0x7F) are technically control characters, but the comment's phrasing 'Allow control characters' is misleading since the function blocks OTHER control characters later. The comment should say 'Allow backspace and delete' rather than generalizing to 'control characters'.

---

#### code_vs_comment

**Description:** Comment claims blank line won't be saved but contradicts earlier behavior where _save_editor_to_program is called on key release

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1245: 'DON'T save to program yet - the line is blank and would be filtered out by _save_editor_to_program() which skips blank lines. Just position the cursor on the new line so user can start typing. The line will be saved to program when: 1. User types content and triggers _on_key_release -> _save_editor_to_program()'
However, earlier in _on_key_press (line ~1047), there's: 'self.root.after(10, self._remove_blank_lines)' which would remove this blank line. The comment suggests the blank line persists until user types, but _remove_blank_lines would delete it almost immediately after insertion.

---

#### code_vs_comment

**Description:** Complex comment about avoiding interpreter.start() may indicate fragile code design

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_immediate() method around line 1115:
"# Initialize interpreter state for execution
# NOTE: Don't call interpreter.start() because it calls runtime.setup()
# which resets PC to the first statement. The RUN command has already
# set PC to the correct line (e.g., RUN 120 sets PC to line 120).
# We only need to clear the halted flag and mark this as first line.
# This avoids the full initialization that start() does:
#   - runtime.setup() (rebuilds tables, resets PC)
#   - Creates new InterpreterState
#   - Sets up Ctrl+C handler
self.runtime.halted = False  # Clear halted flag to start execution
self.interpreter.state.is_first_line = True"

This comment describes working around the normal initialization flow, which suggests either:
1. The interpreter.start() API is not designed correctly for this use case
2. The code is bypassing proper initialization in a fragile way
3. There should be a separate API method for resuming vs starting

This needs architectural review.

---

#### code_vs_comment

**Description:** _parse_line_number() docstring and comment claim MBASIC 5.21 requires whitespace after line number, but regex allows end-of-string without whitespace

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment in _parse_line_number() says:
"# Match line number followed by whitespace OR end of string (both valid)
# Valid: "10 PRINT" (whitespace after), "10" (end after), "  10  REM" (leading whitespace ok)
# Invalid: "10REM" (no whitespace), "ABC10" (non-digit prefix), "" (empty after strip)
# MBASIC 5.21 requires whitespace (or end of line) between line number and statement"

The regex is: r'^(\d+)(?:\s|$)'

This matches either whitespace (\s) OR end-of-string ($). The comment says 'MBASIC 5.21 requires whitespace (or end of line)' which is consistent with the regex. However, the phrase 'or end of line' is ambiguous - does it mean end-of-string (which the regex checks) or a newline character? If MBASIC 5.21 truly requires whitespace between line number and statement, then a line like '10' with nothing after should be valid (just a line number, no statement), which the regex allows. This appears consistent, but needs verification that MBASIC 5.21 actually allows bare line numbers.

---

#### code_vs_comment

**Description:** Comment in serialize_statement() describes prevention strategy but the error handling doesn't prevent silent data corruption during all operations

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment states: "Prevention strategy: Explicitly fail (with ValueError) rather than silently omitting
statements during RENUM, which would corrupt the program.
All statement types must be handled above - if we reach here, serialization failed."

However, serialize_statement() is called from serialize_line(), which is used in multiple contexts:
1. renum_program() - where the ValueError would be raised
2. renumber_program_lines() - which returns (new_lines, line_mapping) and doesn't document that it can raise ValueError
3. Potentially other serialization contexts

The comment implies this is specifically for RENUM protection, but the function is general-purpose. The error handling strategy should either be documented as general serialization failure, or the function should be split into RENUM-specific and general variants.

---

#### code_vs_comment

**Description:** Duplicate comment about INPUT prompt handling in _execute_tick - same note appears twice with identical wording, suggesting copy-paste error or refactoring artifact.

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _execute_tick method, the following comment appears twice (around lines 1900 and 1930):
"# Note: We don't append the prompt to output here because the interpreter
# has already printed it via io.output() before setting input_prompt state.
# Verified: INPUT statement calls io.output(prompt) before awaiting user input."

This duplication suggests the code may have been refactored and the comment was not cleaned up properly.

---

#### documentation_inconsistency

**Description:** Help system documentation claims four UI backends exist, but web_help_launcher.py shows deprecated/legacy status and points to external URL instead of local help

**Affected files:**
- `docs/help/README.md`
- `src/ui/web_help_launcher.py`

**Details:**
README.md states: 'MBASIC supports four UI backends: CLI (command-line interface), Curses (terminal full-screen), Tk (desktop GUI), and Web (browser-based). The help system provides both common content (shared across all backends) and UI-specific documentation for each interface.'

However, web_help_launcher.py shows:
- HELP_BASE_URL = 'http://localhost/mbasic_docs' (external server, not local docs)
- WebHelpLauncher_DEPRECATED class marked as legacy
- Comments say: 'Legacy class kept for compatibility - new code should use direct web URL instead'
- Migration guide suggests using external URLs instead of local help system

---

#### documentation_inconsistency

**Description:** language.md references getting-started.md which doesn't exist in the provided documentation

**Affected files:**
- `docs/help/common/language.md`
- `docs/help/common/language/appendices/index.md`

**Details:**
In language.md: "**Note:** This is a quick reference guide. For a beginner-friendly tutorial, see [Getting Started](getting-started.md)."

The getting-started.md file is not provided in the documentation set, creating a broken reference. This is a high severity issue as it's a primary navigation link in the language reference.

---

#### documentation_inconsistency

**Description:** Contradictory information about loop termination timing

**Affected files:**
- `docs/help/common/language/statements/for-next.md`

**Details:**
The documentation states:
"Loop Termination:
The loop terminates when the variable passes the ending value, considering the STEP direction:
- Positive STEP (or no STEP): Loop terminates when variable > ending value
- Negative STEP: Loop terminates when variable < ending value

For example:
- FOR I = 1 TO 10 terminates when I > 10 (after I reaches 10 and increments to 11)
- FOR I = 10 TO 1 STEP -1 terminates when I < 1 (after I reaches 1 and decrements to 0)"

This is contradictory. The examples suggest the loop body executes when I=10 and I=1 respectively, THEN increments/decrements and tests. But standard BASIC behavior tests BEFORE executing the loop body. The loop should terminate when the test fails BEFORE execution, not after. This needs clarification about whether the test is before or after loop body execution.

---

#### documentation_inconsistency

**Description:** Keyboard shortcut placeholders not resolved

**Affected files:**
- `docs/help/common/shortcuts.md`
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/curses/editing.md`

**Details:**
shortcuts.md uses placeholder syntax like {{kbd:run:cli}}, {{kbd:run:curses}}, {{kbd:run_program:tk}}, etc. throughout the document. These placeholders are not resolved to actual key combinations. The documentation should either:
1. Replace placeholders with actual keys (e.g., 'F5', 'Ctrl+R')
2. Explain the placeholder system
3. Have a preprocessing step that resolves these before display

Similarly, cli/index.md uses {{kbd:stop:cli}} and curses/editing.md uses {{kbd:run:curses}}, {{kbd:parse:curses}}, {{kbd:new:curses}}, {{kbd:save:curses}}, {{kbd:continue:curses}} without resolution.

---

#### documentation_inconsistency

**Description:** Tk UI documentation claims Find and Replace functionality, but extensions.md states Find is Tk-only with no mention of Replace

**Affected files:**
- `docs/help/common/ui/tk/index.md`
- `docs/help/mbasic/extensions.md`

**Details:**
tk/index.md states:
- **Find and Replace** - Search and replace text (Ctrl+F/Ctrl+H)

But extensions.md states:
- **Find** - ❌ | ✅ (Tk) | Extension

And in the feature comparison table, only 'Find' is mentioned for Tk, not 'Replace'.

---

#### documentation_inconsistency

**Description:** Web UI debugging capabilities inconsistently documented

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/extensions.md`

**Details:**
features.md debugging section says features are 'available in all UIs' but extensions.md Web UI section only mentions:
- **Basic debugging** - Simple breakpoint support via menu

No mention of step execution, variable viewing, or stack viewer for Web UI in extensions.md, contradicting the 'all UIs' claim in features.md.

---

#### documentation_inconsistency

**Description:** Keyboard shortcut documentation uses placeholder syntax that was never replaced with actual keys

**Affected files:**
- `docs/help/ui/curses/editing.md`
- `docs/help/ui/cli/find-replace.md`

**Details:**
In curses/editing.md: 'Cut/Copy/Paste operations ({{kbd:stop:curses}}/C/V) are not available' and '{{kbd:continue:curses}}/V' - these {{kbd:...}} placeholders should be replaced with actual key names like 'Ctrl+X' or similar. The cli/find-replace.md correctly uses 'Ctrl+F', 'Ctrl+H', 'F3' format.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut documentation for Recent Files feature

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
feature-reference.md states Recent Files uses '{{kbd:save:curses}}hift+O' (appears to be a typo for Shift+O), but quick-reference.md does not list this shortcut at all in the Program Management section or anywhere else.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut documentation for Clear All Breakpoints

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
feature-reference.md states Clear All Breakpoints uses '{{kbd:save:curses}}hift+B' (appears to be Shift+B with typo), but quick-reference.md does not list this shortcut anywhere.

---

#### documentation_inconsistency

**Description:** Variables Window shortcut inconsistency

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
feature-reference.md states Variables Window uses 'Ctrl+W', but quick-reference.md lists it as 'Menu only' under Global Commands.

---

#### documentation_inconsistency

**Description:** Settings Widget shortcut inconsistency

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
feature-reference.md and settings.md state Settings Widget uses 'Ctrl+,', but quick-reference.md lists it as 'Menu only' under Global Commands.

---

#### documentation_inconsistency

**Description:** Execution Stack access method inconsistency

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
feature-reference.md states 'Via menu: Ctrl+U → Debug → Execution Stack' and 'Note: There is no dedicated keyboard shortcut', but quick-reference.md lists it as 'Menu only' under Global Commands without mentioning Ctrl+U menu access.

---

#### documentation_inconsistency

**Description:** Tk UI Stop/Interrupt shortcut conflict

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
Tk feature-reference.md states Stop/Interrupt uses '{{kbd:cut:tk}}' which is typically Ctrl+X, but this is also listed as the Cut operation shortcut in the Cut/Copy/Paste section. This creates a conflict where the same shortcut is documented for two different operations.

---

#### documentation_inconsistency

**Description:** Tk UI Search Help shortcut appears to be typo

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
Tk feature-reference.md shows Search Help uses '{{kbd:file_save:tk}}hift+F' which appears to be the same typo pattern as seen in Curses docs, likely should be 'Shift+F' or similar.

---

#### documentation_inconsistency

**Description:** Tk GUI features documented as implemented but settings.md indicates they are planned/not yet available

**Affected files:**
- `docs/help/ui/tk/features.md`
- `docs/help/ui/tk/getting-started.md`
- `docs/help/ui/tk/tips.md`
- `docs/help/ui/tk/workflows.md`

**Details:**
Multiple Tk docs describe features like Smart Insert ({{kbd:smart_insert}}), Variables Window ({{kbd:toggle_variables}}), Execution Stack ({{kbd:toggle_stack}}), and Renumber ({{kbd:renumber}}) as if they are currently available. However, settings.md states: 'Implementation Status: The Tk (Tkinter) desktop GUI is planned to provide the most comprehensive settings dialog. The features described in this document represent planned/intended implementation and are not yet available.' This creates confusion about what is actually implemented vs planned.

---

#### documentation_inconsistency

**Description:** Contradictory information about localStorage usage in Web UI

**Affected files:**
- `docs/help/ui/web/features.md`

**Details:**
Under 'Local Storage - Currently Implemented', features.md states:
'Programs stored in Python server memory (session-only, lost on page refresh)'
'Recent files list stored in browser localStorage'

But under 'Security Features - Data Protection - Currently Implemented', it states:
'Local storage only (browser localStorage)'

And under 'Session Management' it says:
'Programs are stored locally in browser storage only.'

These statements contradict each other - are programs stored in Python server memory OR in browser localStorage?

---

### 🟡 Medium Severity

#### documentation_inconsistency

**Description:** Version number inconsistency between setup.py and ast_nodes.py documentation

**Affected files:**
- `setup.py`
- `src/ast_nodes.py`

**Details:**
setup.py line 3: 'Setup script for MBASIC 5.21 Interpreter (version 0.99.0)'
setup.py line 5: 'Package version 0.99.0 reflects approximately 99% implementation status (core complete).'
setup.py line 16: 'version="0.99.0"'

ast_nodes.py line 3: 'Note: 5.21 refers to the Microsoft BASIC-80 language version, not this package version.'

The setup.py conflates MBASIC 5.21 (the language being interpreted) with package version 0.99.0 (the interpreter implementation). The ast_nodes.py correctly clarifies that 5.21 is the language version, not the package version. This creates confusion about what '5.21' means in different contexts.

---

#### code_vs_comment_conflict

**Description:** LineNode docstring claims no source_text field to avoid duplication, but design note contradicts actual regeneration mechanism

**Affected files:**
- `src/ast_nodes.py`

**Details:**
LineNode docstring lines 149-157:
'The AST is the single source of truth. Text is always regenerated from the AST using statement token information (each statement has char_start/char_end and tokens preserve original_case for keywords and identifiers).

Design note: This class intentionally does not have a source_text field to avoid maintaining duplicate copies that could get out of sync with the AST during editing. Text regeneration is handled by the position_serializer module which reconstructs source text from statement nodes and their token information. Each StatementNode has char_start/char_end offsets that indicate the character position within the regenerated line text.'

This claims text is regenerated from 'statement token information' and 'tokens preserve original_case', but PrintStatementNode comment (line 237) says 'keyword_token fields... are not currently used by position_serializer, which handles keyword case through case_keepy_string() instead'. This suggests tokens are NOT used for regeneration as the LineNode docstring claims.

---

#### code_vs_comment

**Description:** Comment in EOF() method describes mode 'I' as 'Input' but implementation comment says it's 'binary input mode'

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line ~570: Comment says "Mode 'I' means 'Input' in MBASIC syntax" but later says "Mode 'I' = binary input mode, where files are opened in binary mode ('rb')". The distinction between 'Input' (sequential text) vs 'binary input' is unclear. The code checks for ^Z (ASCII 26) which is CP/M binary EOF marker, suggesting 'I' is specifically binary mode, not general input.

---

#### code_vs_comment

**Description:** Comment about trailing_minus_only behavior is inconsistent with variable name and implementation

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line ~145: Comment says "trailing_minus_only: - at end, adds - for negative or space for non-negative (always 1 char)" but the spec parsing at line ~185 shows it's set when format_str[i] == '-'. The name 'trailing_minus_only' suggests it only adds minus, but comment says it adds space for non-negative. Implementation at line ~340 confirms it adds space for positive: "result_parts.append('-' if is_negative else ' ')". The 'only' in the name is misleading.

---

#### code_vs_comment

**Description:** EOF() docstring says it returns -1 for EOF but doesn't mention ^Z behavior for all file types

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line ~545: Docstring says "Returns -1 if at EOF, 0 otherwise" and mentions ^Z for mode 'I' files. However, the implementation only checks ^Z for mode 'I' (binary input). The docstring should clarify that ^Z is ONLY checked for mode 'I' files, not all files. Text mode files ignore ^Z.

---

#### code_vs_comment

**Description:** Comment about asterisk_fill counting as positions conflicts with padding logic

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line ~163: Comment says "spec['digit_count'] += 2  # Counts as 2 positions" for ** prefix. Line ~167 says "spec['digit_count'] += 2  # Counts as 2 positions" for $$ prefix. However, at line ~323 the code does "if spec['asterisk_fill']: result_parts.append('*' * max(0, padding_needed))" which fills with asterisks. The digit_count increment suggests ** reserves 2 positions, but the padding logic suggests it fills variable space. This is confusing about whether ** is fixed width or variable.

---

#### Documentation inconsistency

**Description:** Contradictory information about ProgramManager.load_from_file() return value

**Affected files:**
- `src/editing/manager.py`
- `src/file_io.py`

**Details:**
src/editing/manager.py docstring states:
"Note: ProgramManager.load_from_file() returns (success, errors) tuple where errors
is a list of (line_number, error_message) tuples for direct UI error reporting,
while FileIO.load_file() returns raw file text."

However, the actual implementation in manager.py shows:
def load_from_file(self, filename: str) -> Tuple[bool, List[Tuple[int, str]]]:
    """Load program from file.
    Returns:
        Tuple of (success, errors)
        success: True if at least one line loaded successfully
        errors: List of (line_number, error_message) for failed lines"""

The module docstring says errors is a list of tuples, but the function docstring says the same thing. Both are consistent with implementation. However, the module docstring creates confusion by contrasting with FileIO.load_file() which actually returns a string, not a tuple.

---

#### Code vs Comment conflict

**Description:** Comment about flush() behavior may be misleading about when content is saved

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
In InMemoryFileHandle.flush() method:

Comment states:
"""Flush write buffers (no-op for in-memory files).

Note: This calls StringIO/BytesIO flush() which are no-ops.
Content is only saved to the virtual filesystem on close().
Unlike standard file flush() which persists buffered writes to disk,
in-memory file writes are already in memory, so flush() has no effect."""

Code implementation:
def flush(self):
    if hasattr(self.file_obj, 'flush'):
        self.file_obj.flush()

The comment correctly describes that content is saved on close(), not flush(). However, it could be clearer that flush() is a no-op for persistence purposes but still calls the underlying StringIO/BytesIO flush() method (which itself does nothing). The comment is accurate but could be misread as saying flush() does absolutely nothing.

---

#### Documentation inconsistency

**Description:** Security warning about user_id validation appears in multiple places with slightly different wording

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
In SandboxedFileSystemProvider class docstring:
"Security:
- Per-user isolation via user_id keys in class-level storage
  IMPORTANT: Caller must ensure user_id is securely generated/validated
  to prevent cross-user access (e.g., use session IDs, not user-provided values)"

In __init__ docstring:
"Args:
    user_id: Unique identifier for this user/session
            SECURITY: Must be securely generated/validated (e.g., session IDs)
            to prevent cross-user access. Do NOT use user-provided values."

The warnings are consistent in meaning but use different phrasing ('ensure user_id is securely generated/validated' vs 'Must be securely generated/validated'). While not a major issue, standardizing the security warning language would improve clarity.

---

#### code_vs_comment

**Description:** Comment claims PC is not saved/restored, but this contradicts the documented behavior for control flow statements

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Comment at line ~200 states: 'Note: We do not save/restore the PC before/after execution. This allows statements like RUN to change execution position. Control flow statements (GOTO, GOSUB) can also modify PC but may produce unexpected results (see help text).'

However, the help text in _show_help() states: 'GOTO, GOSUB, and control flow statements are not recommended (they will execute but may produce unexpected results)'

The comment suggests this is intentional design to allow RUN to work, but doesn't explain why control flow produces 'unexpected results' or what those results are. The implementation executes statements at line 0, so GOTO/GOSUB would try to jump to other line numbers, which may not exist in the immediate context.

---

#### code_vs_comment

**Description:** Extensive documentation about numbered line editing feature requirements, but no validation that these requirements are actually enforced

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Lines ~100-110 contain detailed documentation:
'This feature requires the following UI integration:
- interpreter.interactive_mode must reference the UI object (checked with hasattr)
- UI.program must have add_line() and delete_line() methods (validated, errors if missing)
- UI._refresh_editor() method to update the display (optional, checked with hasattr)
- UI._highlight_current_statement() for restoring execution highlighting (optional, checked with hasattr)'

The code does check for these attributes with hasattr(), but the comment claims 'validated, errors if missing' for add_line/delete_line. However, the actual validation only happens AFTER checking if line_content exists (line ~125-130). If line_content is empty (delete case), it checks delete_line. If line_content exists (add case), it checks add_line. But it doesn't validate BOTH methods exist upfront as the documentation implies.

---

#### code_vs_comment

**Description:** Comment claims program line editing adds complete line with line number, but the code constructs it

**Affected files:**
- `src/immediate_executor.py`

**Details:**
At line ~130, comment states:
'# Add/update line - add_line expects complete line text with line number
complete_line = f"{line_num} {line_content}"
success, error = ui.program.add_line(line_num, complete_line)'

The comment says add_line 'expects complete line text with line number', but then the code passes BOTH line_num as first argument AND complete_line (which includes line_num) as second argument. This suggests either:
1. The comment is wrong about what add_line expects
2. The code is passing redundant information
3. add_line signature is: add_line(line_num, complete_line_text)

Without seeing the add_line implementation, it's unclear if passing line_num twice is intentional or if the comment is outdated.

---

#### code_vs_comment

**Description:** Comment claims EDIT command digits are 'silently ignored' but code doesn't implement this behavior

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~680 states: 'INTENTIONAL BEHAVIOR: When digits are entered, they are silently ignored (no output, no cursor movement, no error). This preserves MBASIC compatibility where digits are reserved for count prefixes in the full EDIT implementation.'

However, the cmd_edit() implementation has no code to handle digit input specially. The while loop at line ~720 only handles specific commands (Space, D, I, X, H, E, Q, L, A, C) and does not have any case for digit characters. Digits would fall through to no handler, which may cause unexpected behavior rather than being 'silently ignored'.

---

#### code_vs_documentation

**Description:** Docstring lists EDIT subcommands not fully implemented in code

**Affected files:**
- `src/interactive.py`

**Details:**
Docstring at line ~665 states: 'Note: Count prefixes ([n]D, [n]C) and search commands ([n]S, [n]K) are not yet implemented.'

This indicates the documentation lists commands (S, K with count prefixes) that are explicitly not implemented. The cmd_edit() method only handles: Space, D, C, I, X, H, L, E, Q, A, and CR. Commands S and K are not handled at all, and count prefixes (digits before commands) are not parsed.

---

#### code_vs_comment

**Description:** Comment about CONT failure condition doesn't match actual implementation check

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~350 states: 'IMPORTANT: CONT will fail with "?Can't continue" if the program has been edited (lines added, deleted, or renumbered) because editing clears the GOSUB/RETURN and FOR/NEXT stacks'

However, cmd_cont() at line ~360 only checks: 'if not self.program_runtime or not self.program_runtime.stopped:'

The code does NOT check if stacks have been cleared. It only checks if runtime exists and if stopped flag is set. If clear_execution_state() clears the stacks but leaves stopped=True, CONT would attempt to continue with empty stacks, potentially causing crashes rather than showing "?Can't continue". The comment describes a safety mechanism that isn't actually implemented in the check.

---

#### code_vs_comment_conflict

**Description:** Comment claims GOTO/GOSUB in immediate mode are 'not recommended' but code fully supports them with documented special semantics

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~235 says: 'This is the intended behavior but may be unexpected, hence "not recommended".' However, the code implements full support for GOTO/GOSUB with well-defined behavior (execute and jump, then restore PC). The comment suggests discouragement but the implementation is complete and intentional.

---

#### code_vs_comment_conflict

**Description:** Comment describes PC restoration behavior but doesn't explain why GOTO/GOSUB execution during execute_statement is useful if immediately reverted

**Affected files:**
- `src/interactive.py`

**Details:**
Comments at lines ~230-237 explain: 'They execute and jump during execute_statement(), but we restore the\noriginal PC afterward to preserve CONT functionality.' This creates confusion: if the PC is restored, what was the point of executing the GOTO/GOSUB? The comment doesn't explain that side effects (like GOSUB pushing return address) may still occur.

---

#### code_vs_comment

**Description:** Comment describes skip_next_breakpoint_check behavior incorrectly - says it's set AFTER returning state, but code sets it BEFORE returning

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line 62-65 says:
"Set to True AFTER halting at a breakpoint (set after returning state).
On next execution, if still True, allows stepping past the breakpoint once,
then clears itself to False. Prevents re-halting on same breakpoint."

But code at lines 449-452 shows:
if at_breakpoint:
    if not self.state.skip_next_breakpoint_check:
        self.runtime.halted = True
        self.state.skip_next_breakpoint_check = True
        return self.state

The flag is set to True BEFORE returning state (line 451), not after.

---

#### code_vs_comment

**Description:** Comment at line 1046 says 'return_stmt is 0-indexed offset' but then describes len(statements) as valid, which would be out of bounds for 0-indexed array

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at lines 1046-1054 says:
"return_stmt is 0-indexed offset into statements array.
Valid range: 0 to len(statements) (inclusive).
- 0 to len(statements)-1: Normal statement positions
- len(statements): Special sentinel - GOSUB was last statement on line, so RETURN
  continues at next line. This value is valid because PC can point one past the
  last statement to indicate 'move to next line' (handled by statement_table.next_pc).
Values > len(statements) indicate the statement was deleted (validation error)."

This is internally consistent but confusing terminology. If it's '0-indexed offset', then len(statements) is not a valid index (it's one past the end). The comment should say 'position' or 'offset that can be one past the end' rather than '0-indexed offset' which implies array indexing semantics.

---

#### code_vs_comment

**Description:** Comment describes RESUME 0 as distinct from RESUME, but code treats them identically

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1090 states:
"# RESUME or RESUME 0 - retry the statement that caused the error
# Note: MBASIC allows both 'RESUME' and 'RESUME 0' as equivalent syntactic forms.
# Parser preserves the distinction (None vs 0) for source text regeneration,
# but runtime execution treats both identically."

The code checks:
if stmt.line_number is None or stmt.line_number == 0:

This is consistent with the comment, but the comment's phrasing "Parser preserves the distinction (None vs 0)" suggests there might be a distinction that matters elsewhere. The comment is accurate but could be clearer about why the distinction is preserved if execution is identical.

---

#### code_vs_comment

**Description:** Comment about NEXT validation describes sentinel value incorrectly

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~950 states:
"# return_stmt is 0-indexed offset into statements array.
# Valid range:
#   - 0 to len(statements)-1: Normal statement positions (existing statements)
#   - len(statements): Special sentinel value - FOR was last statement on line,
#                      continue execution at next line (no more statements to execute on current line)
#   - > len(statements): Invalid - indicates the statement was deleted
#
# Validation: Check for strictly greater than (== len is OK as sentinel)"

The code checks:
if return_stmt > len(line_statements):
    raise RuntimeError(...)

This allows return_stmt == len(line_statements) as valid (sentinel). However, the comment describes this as "FOR was last statement on line" but doesn't explain why this would be stored as len(statements) rather than len(statements)-1. The comment may be describing implementation details that aren't obvious from the code alone.

---

#### code_vs_comment

**Description:** Comment about OPTION BASE enforcement mentions 'strictly enforced' but doesn't explain all edge cases

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1310 states:
"MBASIC 5.21 restrictions (strictly enforced):
- OPTION BASE can only be executed once per program run
- Must be executed BEFORE any arrays are dimensioned (implicit or explicit)
- Violating either condition raises 'Duplicate Definition' error"

The code checks:
if self.runtime.option_base_executed:
    raise RuntimeError("Duplicate Definition")
if len(self.runtime._arrays) > 0:
    raise RuntimeError("Duplicate Definition")

The comment is accurate, but the later comment at line ~1320 adds important clarification:
"# Note: The check len(self.runtime._arrays) > 0 catches all array creation because both
# explicit DIM and implicit array access (via set_array_element) update runtime._arrays."

This additional detail should be in the main docstring for completeness.

---

#### code_vs_comment

**Description:** Comment about CP/M encoding is technically incorrect about character meaning preservation

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1570 states:
"Encoding:
Uses latin-1 (ISO-8859-1) to preserve byte values 128-255 unchanged.
CP/M and MBASIC used 8-bit characters; latin-1 maps bytes 0-255 to
Unicode U+0000-U+00FF, allowing round-trip byte preservation.
Note: CP/M systems often used code pages like CP437 or CP850 for characters
128-255, which do NOT match latin-1. Latin-1 preserves the BYTE VALUES but
not necessarily the CHARACTER MEANING for non-ASCII CP/M text. Conversion
may be needed for accurate display of non-English CP/M files."

The comment correctly states that latin-1 preserves byte values but not character meaning. However, it says "Latin-1 preserves the BYTE VALUES but not necessarily the CHARACTER MEANING" which could be misread as "sometimes preserves meaning". It should say "Latin-1 preserves BYTE VALUES but NEVER preserves CHARACTER MEANING for CP437/CP850 encoded text" to be clearer.

---

#### code_vs_comment

**Description:** Comment claims STEP command is a placeholder and not functional, but the code does attempt to output a message and has a count parameter

**Affected files:**
- `src/interpreter.py`

**Details:**
execute_step() docstring says:
"STEP is intended to execute one or more statements, then pause.

IMPORTANT: This method is a placeholder and does NOT actually perform stepping."

But the code does:
```
count = stmt.count if stmt.count else 1
self.io.output(f"STEP {count} - Debug stepping not fully implemented")
```

The comment says it's a placeholder that does NOT perform stepping, but the code does parse a count and output a message. The comment should clarify that it's partially implemented (parses syntax, outputs message) but doesn't actually step through execution.

---

#### code_vs_comment

**Description:** Comment in execute_cont() mentions BreakException handler behavior but this code doesn't show that handler

**Affected files:**
- `src/interpreter.py`

**Details:**
execute_cont() docstring says:
"Note: execute_stop() moves NPC to PC for resume, while BreakException handler
does not update PC, which affects whether CONT can resume properly."

This comment references a BreakException handler that is not visible in this code file. The comment implies there's an inconsistency in how STOP vs Break (Ctrl+C) handle PC/NPC, but without seeing the BreakException handler code, we cannot verify if this is accurate or if it's outdated information from a refactoring.

---

#### code_vs_comment

**Description:** Comment in execute_list() warns about line_text_map sync issues but doesn't explain how to detect or handle them

**Affected files:**
- `src/interpreter.py`

**Details:**
execute_list() docstring says:
"Implementation note: Outputs from line_text_map (original source text), not regenerated from AST.
This preserves original formatting/spacing/case. The line_text_map is maintained by ProgramManager
and should be kept in sync with the AST during program modifications (add_line, delete_line, RENUM, MERGE).
If ProgramManager fails to maintain this sync, LIST output may show stale or incorrect line text."

The comment warns about potential sync issues but the code has no validation or error handling for this case. If line_text_map can get out of sync (as the comment warns), the code should either: (1) validate sync and raise an error, (2) fall back to regenerating from AST, or (3) the comment should explain why this is acceptable. Currently it just silently outputs potentially incorrect data.

---

#### Code vs Documentation inconsistency

**Description:** base.py documents input_char() with blocking parameter behavior, but web_io.py ignores the blocking parameter entirely

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/web_io.py`

**Details:**
base.py docstring: "Args:
    blocking: If True, wait for keypress. If False, return "" if no key ready."

web_io.py implementation: "Args:
    blocking: If True, wait for keypress. If False, return "" if no key ready.
             NOTE: This parameter is accepted for interface compatibility but
             is ignored in the web UI implementation."

The web implementation documents that it ignores the parameter, but this creates an API inconsistency where the method doesn't behave as the base interface promises.

---

#### Code vs Documentation inconsistency

**Description:** ConsoleIOHandler.input_char() has complex fallback logic for Windows without msvcrt that calls input(), but this defeats the purpose of single-character input

**Affected files:**
- `src/iohandler/console.py`

**Details:**
Code has extensive fallback:
"# Fallback for Windows without msvcrt: use input() with severe limitations
# WARNING: This fallback calls input() which:
# - Waits for Enter key (defeats the purpose of single-char input)
# - Returns the entire line, not just one character"

This fallback behavior is so different from the documented interface that it essentially breaks the contract of input_char(). The method is supposed to return a single character, but the fallback returns an entire line. This is documented in comments but creates a severe API inconsistency.

---

#### Code vs Comment conflict

**Description:** Comment claims SimpleKeywordCase validates policy strings and auto-corrects invalid values to force_lower, but this validation behavior is not visible in the lexer code itself

**Affected files:**
- `src/lexer.py`

**Details:**
In create_keyword_case_manager() docstring:
"Note: SimpleKeywordCase validates policy strings in its __init__ method. Invalid
policy values (not in: force_lower, force_upper, force_capitalize) are automatically
corrected to force_lower. See src/simple_keyword_case.py for implementation."

However, the actual SimpleKeywordCase class is not shown in the provided code, so we cannot verify this claim. The comment references external behavior that may or may not exist.

---

#### Code vs Comment conflict

**Description:** Inconsistent handling of # character: comment says it's part of identifier type suffix, but code has special logic to split it back out for file I/O keywords

**Affected files:**
- `src/lexer.py`

**Details:**
In read_identifier() docstring:
"Identifiers can contain letters, digits, and end with type suffix $ % ! #
In MBASIC, $ % ! # are considered part of the identifier."

But later in the same function, there's special case handling:
"# Special case: File I/O keywords followed by # (e.g., PRINT#1)
# MBASIC allows 'PRINT#1' with no space, which should tokenize as:
#   PRINT (keyword) + # (operator) + 1 (number)
# The read_identifier() method treated # as a type suffix and consumed it,
# so we now have 'PRINT#' as ident. For file I/O keywords, we split it back out"

This shows # is NOT always part of the identifier as the docstring claims - it depends on context.

---

#### Code vs Comment conflict

**Description:** Comment claims REM/REMARK are keywords but APOSTROPHE is a distinct token type, but the actual distinction and reasoning is unclear

**Affected files:**
- `src/lexer.py`

**Details:**
Comment in tokenize():
"# Apostrophe comment - distinct token type (unlike REM/REMARK which are keywords)"

This implies a meaningful distinction, but the code shows both are handled specially:
- Apostrophe: creates APOSTROPHE token with comment text
- REM/REMARK: creates REM/REMARK token (keyword type) but replaces value with comment text

The functional difference is minimal - both end up as tokens containing comment text. The comment suggests a more significant architectural difference than actually exists.

---

#### code_vs_comment

**Description:** Comment claims RND and INKEY$ are the only functions that can be called without parentheses in MBASIC 5.21, but this is contradicted by the code implementation

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line 11-12 states:
"Exception: Only RND and INKEY$ can be called without parentheses in MBASIC 5.21
  (this is specific to these two functions, not a general MBASIC feature)"

However, the code at lines 1044-1055 shows RND can be called without parentheses:
"# RND can be called without parentheses - MBASIC 5.21 compatibility feature"

And at lines 1057-1063 shows INKEY$ can be called without parentheses:
"# INKEY$ can be called without parentheses - MBASIC 5.21 compatibility feature"

But the comment says this is 'specific to these two functions', while the implementation treats them as special cases with explicit checks. The comment implies this is a documented MBASIC 5.21 feature, but the code comments suggest it's a 'compatibility feature' which may indicate it's an interpreter-specific extension rather than a standard MBASIC 5.21 feature.

---

#### code_vs_comment

**Description:** Comment about semicolon handling contradicts MBASIC standard behavior

**Affected files:**
- `src/parser.py`

**Details:**
In parse_line() at lines 267-274, there's a comment:
"# Allow trailing semicolon at end of line only (treat as no-op).
# Context matters: Semicolons WITHIN PRINT/LPRINT are item separators (parsed there),
# but semicolons BETWEEN statements are NOT valid in MBASIC.
# MBASIC uses COLON (:) to separate statements, not semicolon (;)."

This comment states that semicolons between statements are NOT valid in MBASIC, but then the code at line 270 allows a trailing semicolon:
"self.advance()"

And at lines 271-274, it checks if there's more after the semicolon and raises an error if so. This suggests the parser is being lenient by allowing trailing semicolons, which may not match actual MBASIC 5.21 behavior. The comment should clarify whether this is a compatibility extension or if MBASIC 5.21 actually allows trailing semicolons.

---

#### code_vs_comment

**Description:** Comment about PRINT USING semicolon requirement contradicts flexible parsing in parse_print_using

**Affected files:**
- `src/parser.py`

**Details:**
In parse_print_using() at lines 1327-1328, the comment states:
"Note: Semicolon after format string is required (separates format from value list)."

And at lines 1336-1338, the code enforces this:
"if not self.match(TokenType.SEMICOLON):
    raise ParseError(f"Expected ';' after PRINT USING format string at line {self.current().line}")"

However, in the expression parsing loop at lines 1343-1357, the code allows semicolons as optional separators between expressions:
"# Check for separator first (skip it)
if self.match(TokenType.SEMICOLON):
    self.advance()"

This suggests semicolons are treated as optional separators in the value list, which may not match MBASIC 5.21 behavior. The comment should clarify whether semicolons are required or optional between values in the PRINT USING value list.

---

#### code_vs_comment

**Description:** Comment describes INPUT; syntax behavior incorrectly

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line ~1050 states:
"Note: The semicolon immediately after INPUT keyword (INPUT;) suppresses
the default '?' prompt. The LINE modifier allows reading an entire line
including commas without treating them as delimiters."

However, the code at lines ~1060-1063 shows:
```
suppress_question = False
if self.match(TokenType.SEMICOLON):
    suppress_question = True
    self.advance()
```

Then at lines ~1078-1086, the comment contradicts itself:
"# Note: In MBASIC 5.21, the separator after prompt affects '?' display:
# - INPUT "Name"; X  displays "Name? " (semicolon AFTER prompt shows '?')
# - INPUT "Name", X  displays "Name " (comma AFTER prompt suppresses '?')
# Different behavior: INPUT; (semicolon IMMEDIATELY after INPUT keyword, no prompt)
# suppresses the default '?' prompt entirely (tracked by suppress_question flag above)."

The second comment clarifies that INPUT; suppresses the '?' prompt entirely, but the first comment says it "suppresses the default '?' prompt" without explaining the distinction between INPUT; (no prompt at all) vs INPUT "prompt"; (prompt with '?').

---

#### code_vs_comment

**Description:** MID$ assignment comment incorrectly describes lexer tokenization

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines ~1820-1826 states:
"Note: The lexer tokenizes 'MID$' in source as a single MID token (the $ is part
of the keyword, not a separate token)."

Then the code at line ~1828 shows:
```
token = self.current()  # MID token (represents 'MID$' from source)
```

This comment claims the lexer tokenizes 'MID$' as a MID token, but without seeing the lexer code, we cannot verify this. In many BASIC implementations, MID$ is tokenized as MID with $ as part of the keyword name. The comment should clarify whether the token type is literally 'MID' or 'MID$' or something else.

---

#### code_vs_comment

**Description:** IF statement ELSE clause parsing has complex lookahead logic that may not match all documented cases

**Affected files:**
- `src/parser.py`

**Details:**
The parse_if method has extensive lookahead logic for distinguishing :ELSE from statement separator colons (lines ~1530-1600). The comment at line ~1515 lists syntax variations:
"- IF condition THEN line_number ELSE line_number (or :ELSE with lookahead)"

However, the code shows multiple places where ELSE is checked:
1. After THEN line_number (lines ~1535-1560)
2. During statement parsing loop (lines ~1570-1595)
3. After GOTO line_number (lines ~1610-1625)

The complexity suggests the comment's simple list may not capture all the edge cases the code handles, particularly around when colons are required vs optional before ELSE.

---

#### code_vs_comment

**Description:** Comment claims CALL statement primarily uses numeric address form in MBASIC 5.21, but code fully implements extended syntax with arguments

**Affected files:**
- `src/parser.py`

**Details:**
Comment in parse_call() states:
"Note: MBASIC 5.21 primarily uses the simple numeric address form, but this
parser fully supports both forms for broader compatibility."

However, the implementation fully parses both forms:
- Simple numeric address: CALL 16384
- Extended with arguments: CALL ROUTINE(X,Y)

The code handles both equally, converting FunctionCallNode and VariableNode with subscripts into CallStatementNode with arguments. The comment suggests the extended form is for compatibility, but the code treats both as first-class features.

---

#### code_vs_comment

**Description:** PC class docstring describes stmt_offset as '0-based index' but also calls it 'offset' which is confusing terminology

**Affected files:**
- `src/pc.py`

**Details:**
Docstring says: 'The stmt_offset is a 0-based index into the statements list for a line...Note: stmt_offset is the list index (position in the statements array). The term "offset" is used for historical reasons but it\'s simply the array index.'

This acknowledges the terminology is misleading but doesn't fix it. Throughout the codebase it's consistently used as an index (0, 1, 2...) not an offset in the traditional sense.

---

#### code_vs_comment

**Description:** apply_keyword_case_policy implementation doesn't match its docstring regarding first_wins normalization

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring says: 'Note: The first_wins policy normalizes keywords to lowercase for lookup purposes. Other policies transform the keyword directly without normalization.'

But the code shows ALL policies receive the keyword as-is and transform it. The 'first_wins' policy does normalize to lowercase for lookup (keyword_lower = keyword.lower()) but this is an implementation detail, not a caller requirement. The docstring implies callers need to know about this normalization.

---

#### code_vs_comment

**Description:** emit_keyword caller responsibility comment contradicts apply_keyword_case_policy docstring about input case requirements

**Affected files:**
- `src/position_serializer.py`

**Details:**
emit_keyword says: 'Caller responsibility: The caller must pass the keyword in lowercase (e.g., "print", "for").'

apply_keyword_case_policy says: 'Args:
    keyword: The keyword to transform (may be any case)'

If emit_keyword requires lowercase input, but it calls apply_keyword_case_policy which accepts any case, there's a mismatch in the contract.

---

#### code_vs_comment_conflict

**Description:** Comment about MBASIC array sizing convention may not match actual implementation location

**Affected files:**
- `src/resource_limits.py`

**Details:**
In check_array_allocation() method, line ~165:

Comment states: '# Note: DIM A(N) creates N+1 elements (0 to N) in MBASIC 5.21'
Followed by: '# This implements the MBASIC array sizing convention (called by execute_dim() in interpreter.py)'

The code then does: 'total_elements *= (dim_size + 1)  # +1 for 0-based indexing (0 to N)'

The comment claims 'This implements the MBASIC array sizing convention' but the actual implementation is just calculating the size for limit checking. The actual array creation/initialization would be in interpreter.py's execute_dim(). The comment may be misleading about where the convention is 'implemented' vs where it's 'accounted for in size calculation'.

---

#### code_vs_comment

**Description:** Comment claims 'original_case' stores the original case, but code actually stores the canonical/resolved case

**Affected files:**
- `src/runtime.py`

**Details:**
Line 48-51 comment: "'original_case' stores the canonical case for display (determined by case_conflict policy).
Despite the name 'original_case', this field stores the resolved canonical case variant,
not necessarily the first case seen."

Line 265: "self._variables[full_name]['original_case'] = canonical_case  # Store canonical case for display (see _check_case_conflict)"

Line 283: "# Always update original_case to canonical (for prefer_upper/prefer_lower/prefer_mixed policies)
# Note: 'original_case' field name is misleading - it stores the canonical case, not the original"

Line 368: "self._variables[full_name]['original_case'] = canonical_case  # Store canonical case for display (see _check_case_conflict)"

Line 373: "# Always update original_case to canonical (for prefer_upper/prefer_lower/prefer_mixed policies)
# Note: 'original_case' field name is misleading - it stores the canonical case, not the original"

The field name 'original_case' is misleading throughout the codebase. It should be renamed to 'canonical_case' or 'display_case' to match its actual purpose.

---

#### code_vs_comment

**Description:** Comment about DIM tracking as both read and write may be misleading

**Affected files:**
- `src/runtime.py`

**Details:**
Line 685-693: "# Note: DIM is tracked as both read and write to provide consistent debugger display.
# While DIM is technically allocation/initialization (write-only operation), setting
# last_read to the DIM location ensures that debuggers/inspectors can show 'Last accessed'
# information even for arrays that have never been explicitly read. Without this, an
# unaccessed array would show no last_read info, which could be confusing. The DIM location
# provides useful context about where the array was created."

This comment justifies setting last_read for DIM as a debugger convenience, but this could be confusing for users who expect last_read to mean actual read access. The comment acknowledges this is not semantically correct but done for UI purposes. This design decision should be documented more prominently or reconsidered.

---

#### Code vs Documentation inconsistency

**Description:** get_variables() docstring claims to return array tracking info but implementation may return None for uninitialized fields

**Affected files:**
- `src/runtime.py`

**Details:**
Docstring states arrays include:
"'last_read': {'line': int, 'position': int, 'timestamp': float} or None"
"'last_write': {'line': int, 'position': int, 'timestamp': float} or None"

Code uses:
"'last_read': array_data.get('last_read')"
"'last_write': array_data.get('last_write')"

If these keys don't exist in array_data, .get() returns None (correct). However, the docstring doesn't document the additional fields 'last_read_subscripts', 'last_write_subscripts', 'last_accessed_value', and 'last_accessed_subscripts' that are also added to the result for arrays. These fields are implemented but not documented in the Returns section.

---

#### code_vs_comment

**Description:** Comment in load() method claims settings remain flat, but code shows settings can be both flat and nested

**Affected files:**
- `src/settings.py`

**Details:**
Comment in load() method states:
"Loaded settings remain flat; settings modified via set() become nested; both work."

However, the code shows:
1. Settings loaded from disk are flat (e.g., {'editor.auto_number': True})
2. Settings modified via set() become nested (e.g., {'editor': {'auto_number': True}})
3. _get_from_dict() handles both formats

The comment is accurate but could be clearer that this is intentional mixed-format support, not a bug.

---

#### code_vs_comment

**Description:** SettingsManager class has unused _get_global_settings_path and _get_project_settings_path methods

**Affected files:**
- `src/settings.py`

**Details:**
The SettingsManager class defines:
- _get_global_settings_path()
- _get_project_settings_path()

But these methods are never called in the class. The __init__ method comment says:
"# Paths (for backward compatibility, may not be used with Redis backend)
self.global_settings_path = getattr(backend, 'global_settings_path', None)
self.project_settings_path = getattr(backend, 'project_settings_path', None)"

The paths are retrieved from the backend, not from these methods. These methods appear to be dead code left over from refactoring.

---

#### code_vs_comment

**Description:** Token dataclass comment claims fields are mutually exclusive but implementation doesn't enforce it

**Affected files:**
- `src/tokens.py`

**Details:**
Token dataclass docstring states:
"Note: These fields serve different purposes and should be mutually exclusive
(identifiers use original_case, keywords use original_case_keyword):
- original_case: For identifiers (user variables) - preserves what user typed
- original_case_keyword: For keywords - stores policy-determined display case

The dataclass doesn't enforce exclusivity (both can be set) for implementation flexibility,
but the lexer/parser maintain this convention: only one field is populated per token."

This is a design decision documented in comments, but the comment acknowledges the code doesn't enforce what it describes. The comment says 'should be mutually exclusive' but then says 'both can be set'. This is internally contradictory documentation.

---

#### code_vs_comment

**Description:** get() method docstring describes precedence including file settings but implementation shows file_settings is always empty in normal usage

**Affected files:**
- `src/settings.py`

**Details:**
get() method docstring:
"Precedence: file > project > global > definition default > provided default

Note: File-level settings infrastructure is fully implemented and functional.
The file_settings dict can be set programmatically and is checked first in precedence.
However, no UI or command exists to manage per-file settings. In normal usage,
file_settings is empty and precedence falls through to project/global settings."

The docstring correctly describes the precedence order and notes file_settings is empty in normal usage. However, it's misleading to list 'file' first in the precedence when it's never populated. The precedence in practice is: project > global > definition default > provided default.

---

#### Code vs Documentation inconsistency

**Description:** CLI STEP command documentation claims it implements statement-level stepping like curses 'Step Statement' (Ctrl+T), but curses also has a separate 'Step Line' command (Ctrl+K) that is not available in CLI. The documentation acknowledges this but creates confusion about feature parity.

**Affected files:**
- `src/ui/cli_debug.py`
- `src/ui/curses_keybindings.json`

**Details:**
cli_debug.py docstring:
"This implements statement-level stepping similar to the curses UI 'Step Statement'
command (Ctrl+T). The curses UI also has a separate 'Step Line' command (Ctrl+K)
which is not available in the CLI."

curses_keybindings.json defines both:
"step_line": {"keys": ["Ctrl+K"], "description": "Step Line (execute all statements on current line)"}
"step": {"keys": ["Ctrl+T"], "description": "Step statement (execute one statement)"}

CLI only has STEP command with no line-level stepping equivalent.

---

#### Code vs Comment conflict

**Description:** The _execute_single_step() method's docstring claims it executes one statement and describes statement-level granularity, but includes a disclaimer that actual behavior depends on interpreter implementation. The comment admits the method might behave as line-level stepping if the interpreter doesn't support statement-level execution.

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
Method docstring:
"Execute a single statement (not a full line).

Uses the interpreter's tick() or execute_next() method to execute
one statement at the current program counter position.

Note: The actual statement-level granularity depends on the interpreter's
implementation of tick()/execute_next(). These methods are expected to
advance the program counter by one statement, handling colon-separated
statements separately. If the interpreter executes full lines instead,
this method will behave as line-level stepping rather than statement-level."

This creates uncertainty about whether STEP actually provides statement-level stepping as documented in cmd_step().

---

#### JSON configuration inconsistency

**Description:** The 'continue' command has different key bindings between CLI and curses: CLI uses 'CONT' command while curses uses 'Ctrl+C'. Additionally, curses uses 'Ctrl+C' for continue but 'Ctrl+X' for stop, which is inconsistent with typical terminal conventions where Ctrl+C stops execution.

**Affected files:**
- `src/ui/cli_keybindings.json`
- `src/ui/curses_keybindings.json`

**Details:**
cli_keybindings.json:
"continue": {"keys": ["CONT"], "primary": "CONT", "description": "Continue execution"}
"stop": {"keys": ["Ctrl+C"], "primary": "Ctrl+C", "description": "Stop program execution"}

curses_keybindings.json:
"continue": {"keys": ["Ctrl+C"], "primary": "Ctrl+C", "description": "Continue execution"}
"stop": {"keys": ["Ctrl+X"], "primary": "Ctrl+X", "description": "Stop program execution"}

This creates a confusing user experience where Ctrl+C has opposite meanings in different UIs.

---

#### Code vs Comment conflict

**Description:** The _create_body() method's footer comment claims 'All shortcuts use constants from keybindings module to ensure footer display matches actual key handling in keypress() method', but the footer only shows 4 shortcuts while keypress() handles 4 different actions. The comment implies complete coverage but implementation may be incomplete.

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
Comment in _create_body():
"# Create footer with keyboard shortcuts (instead of button widgets)
# Note: All shortcuts use constants from keybindings module to ensure
# footer display matches actual key handling in keypress() method"

Footer shows: ENTER_KEY, ESC_KEY, SETTINGS_KEY, SETTINGS_APPLY_KEY, SETTINGS_RESET_KEY
keypress() handles: ESC_KEY, SETTINGS_KEY, ENTER_KEY, SETTINGS_APPLY_KEY, SETTINGS_RESET_KEY

The comment's claim of ensuring display matches handling is accurate, but the phrasing 'All shortcuts' could be misleading if there are other possible actions not shown.

---

#### Code vs Documentation inconsistency

**Description:** The base.py UIBackend class defines execute_immediate() as an optional method with a docstring showing examples, but cli.py's CLIBackend implements it by delegating to interactive.execute_statement() without any validation or error handling, and there's no documentation about whether execute_statement() actually exists or what it does.

**Affected files:**
- `src/ui/cli.py`
- `src/ui/base.py`

**Details:**
base.py defines:
"def execute_immediate(self, statement: str) -> None:
    '''Execute immediate mode statement.
    
    Args:
        statement: BASIC statement to execute immediately
    
    Examples:
        PRINT 2+2
        A=5: PRINT A
        FOR I=1 TO 10: PRINT I: NEXT I
    '''
    pass"

cli.py implements:
"def execute_immediate(self, statement: str) -> None:
    '''Execute immediate mode statement.'''
    self.interactive.execute_statement(statement)"

No documentation confirms execute_statement() exists on InteractiveMode or what it does.

---

#### code_vs_comment

**Description:** Comment claims line numbers use 1-5 digits, but code supports variable width up to 99999

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Class docstring says:
"Display format: 'S<linenum> CODE' where:
- Field 2 (variable width): Line number (1-5 digits, no padding)"

But code in _on_auto_number_renumber_response and elsewhere uses 99999 as max:
"if next_num >= 99999 or attempts > 10:"

This is 5 digits max, but the comment '1-5 digits' suggests it could be 1, 2, 3, 4, OR 5 digits, which is correct. However, the implementation actually enforces a hard limit of 99999 (exactly 5 digits max), not a variable 1-5 digit range.

---

#### code_vs_comment

**Description:** Comment claims bug fix but code behavior doesn't match the described bug

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_display method:
"# DON'T increment counter here - that happens only on Enter
# Bug fix: Incrementing here caused next_auto_line_num to advance prematurely,
# displaying the wrong line number before the user typed anything"

However, the code never increments next_auto_line_num in _update_display at all - there's no code being prevented. The comment describes a bug that was fixed by removing code, but there's no evidence of that code ever being there (no commented-out increment). This suggests the comment is describing a historical bug fix but doesn't match current code structure.

---

#### code_vs_comment

**Description:** Comment claims empty lines are valid but code has special handling that contradicts this

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_syntax_errors method:
"# Clear error status for empty lines, but preserve breakpoints
# Note: line_number > 0 check handles edge case of line 0 (if present)
# Consistent with _check_line_syntax which treats all empty lines as valid"

But in _check_line_syntax:
"if not code_text or not code_text.strip():
    # Empty lines are valid
    return (True, None)"

The inconsistency: _update_syntax_errors has 'line_number > 0' check, suggesting line 0 is treated differently, but _check_line_syntax treats ALL empty lines as valid regardless of line number. The comment claims consistency but the implementations differ in their handling of line 0.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of line number changes between keypress and _on_enter_idle

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In keypress method, line number changes trigger immediate sorting:
"if current_line_num != self._saved_line_num:
    # Line number changed - sort lines
    self._sort_and_position_line(lines, line_num, target_column=col_in_line)"

But in _on_enter_idle, sorting is deferred and only happens if cursor is in line number area:
"if line_num_parsed is not None and 1 <= col_in_line < code_start:
    self._sort_and_position_line(lines, line_num, target_column=col_in_line)"

This creates two different code paths for sorting with different conditions, which could lead to inconsistent behavior.

---

#### code_vs_comment

**Description:** Comment claims editor_lines stores execution state while editor.lines stores editing state, but code shows they are synchronized and serve overlapping purposes

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~130 says:
# Note: self.editor_lines stores execution state (lines loaded from file for RUN)
# self.editor.lines (in ProgramEditorWidget) stores the actual editing state
# These serve different purposes and are synchronized as needed

However, _save_editor_to_program() (line ~230) syncs editor.lines -> program, and _refresh_editor() (line ~290) syncs program -> editor.lines. The _sync_program_to_editor() method would sync program -> editor_lines. This suggests they are redundant storage rather than serving truly different purposes.

---

#### code_vs_comment

**Description:** Comment about IO Handler lifecycle claims io_handler is created once and reused, but immediate_io is recreated in start()

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~165 says:
# IO Handler Lifecycle:
# 1. self.io_handler (CapturingIOHandler) - Used for RUN program execution
#    Created ONCE here, reused throughout session (NOT recreated in start())
# 2. immediate_io (OutputCapturingIOHandler) - Used for immediate mode commands
#    Created here temporarily, then RECREATED in start() with fresh instance each time

However, at line ~200, the code creates immediate_io temporarily in __init__, then the comment says it will be recreated in start(). This is confusing because it suggests the temporary creation in __init__ serves no purpose except to initialize the attribute.

---

#### code_vs_comment

**Description:** Comment in _on_insert_line_renumber_response says context is lost, but this could be preserved

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
At line ~1180, comment says:
# Note: We can't continue the insert here because we've lost the context
# (lines, line_index, insert_num variables). User will need to retry insert.

This suggests a design limitation, but the context could be preserved by storing it as instance variables or in a closure. The comment makes it sound like a technical impossibility when it's actually a design choice.

---

#### code_vs_comment

**Description:** Comment claims breakpoints are stored in editor as authoritative source and re-applied after reset, but code shows breakpoints are cleared during reset_for_run and then re-applied from editor.breakpoints

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1180 states:
"Note: reset_for_run() clears variables and resets PC. Breakpoints are STORED in
the editor (self.editor.breakpoints) as the authoritative source, not in runtime.
This allows them to persist across runs. After reset_for_run(), we re-apply them
to the interpreter below via set_breakpoint() calls so execution can check them."

This comment is accurate and matches the code implementation where breakpoints are re-applied after reset_for_run(). However, the phrasing could be clearer that breakpoints ARE cleared from the interpreter during reset but preserved in editor state.

---

#### code_vs_comment

**Description:** Comment about PC setting timing may be misleading about when start() resets PC

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1200 states:
"# If start_line is specified (e.g., RUN 100), set PC to that line
# This must happen AFTER interpreter.start() because start() calls setup()
# which resets PC to the first line in the program. By setting PC here,
# we override that default and begin execution at the requested line."

This comment accurately describes the behavior but could be clearer that the PC override happens after the interpreter is fully initialized, not just after start() is called.

---

#### code_vs_comment

**Description:** Comment claims ESC sets stopped=True similar to BASIC STOP, but code behavior differs from STOP semantics

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _get_input_for_interpreter method:
Comment says: "# Note: This sets stopped=True similar to a BASIC STOP statement, but the semantics
# differ - STOP is a deliberate program action, while ESC is user cancellation"

However, the code sets self.runtime.stopped = True and self.running = False, which prevents CONT from working (CONT checks self.runtime.stopped). But the comment acknowledges semantic differences without clarifying if CONT should work after ESC cancellation.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate says immediate executor already called interpreter.start(), but this may not always be true

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _execute_immediate method:
"# NOTE: Don't call interpreter.start() here - the immediate executor already
# called it if needed (e.g., 'RUN 120' called interpreter.start(start_line=120)
# to set PC to line 120). Calling it again would reset PC to the beginning."

This assumes the immediate executor always calls start() when needed, but the code then checks if InterpreterState exists and creates it if not. This suggests there are cases where start() wasn't called. The comment may be outdated or incomplete.

---

#### internal_inconsistency

**Description:** Inconsistent handling of program source of truth between methods

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
cmd_delete and cmd_renum comments say "Updates self.program immediately (source of truth), then syncs to runtime" and call _sync_program_to_runtime().

However, _execute_immediate updates self.program from editor_lines, then syncs to runtime.

But _list_program reads from self.editor_lines directly, not self.program.

This suggests confusion about whether self.program or self.editor_lines is the source of truth for the current program state.

---

#### code_vs_comment_conflict

**Description:** Comments in both files claim they serve different purposes, but they load identical JSON files for overlapping use cases

**Affected files:**
- `src/ui/help_macros.py`
- `src/ui/keybinding_loader.py`

**Details:**
help_macros.py comment at line ~35:
"Note: This is generic keybinding loading for macro expansion in help content (e.g., {{kbd:run}} -> '^R'). This is different from help_widget.py which uses hardcoded keys for its own navigation. HelpMacros needs full keybindings to expand {{kbd:action}} macros in documentation, not for actual event handling."

keybinding_loader.py comment at line ~30:
"Note: This loads keybindings for UI event handling (binding keys to actions). This is different from help_macros.py which loads the same JSON for macro expansion in help content (e.g., {{kbd:run}} -> '^R'). These serve different purposes: KeybindingLoader for runtime event handling, HelpMacros for documentation generation."

Both load from: Path(__file__).parent / f"{self.ui_name}_keybindings.json"

The distinction is valid but the comments overemphasize the difference when both are reading the same data structure for related purposes (one for display, one for binding).

---

#### documentation_inconsistency

**Description:** Docstring describes {{kbd:help}} format but implementation uses different search logic

**Affected files:**
- `src/ui/help_macros.py`

**Details:**
Module docstring states:
"{{kbd:help}} → looks up 'help' action in keybindings (searches all sections) and returns the primary keybinding for that action"

But _expand_kbd() implementation supports additional format:
"Formats:
- 'action' - searches current UI (e.g., 'help', 'save', 'run')
- 'action:ui' - searches specific UI (e.g., 'save:curses', 'run:tk')"

The module docstring doesn't mention the 'action:ui' format capability.

---

#### code_vs_comment_conflict

**Description:** Comment claims tier detection uses startswith('ui/') but code shows more complex tier mapping

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at line ~145:
"Note: UI tier (e.g., 'ui/curses', 'ui/tk') is detected via startswith('ui/') check below and gets '📘 UI' label. Other unrecognized tiers get '📙 Other'."

But the code shows a tier_labels dict with explicit mappings:
tier_labels = {
    'language': '📕 Language',
    'mbasic': '📗 MBASIC',
}

Then uses:
if tier_name.startswith('ui/'):
    tier_label = '📘 UI'
else:
    tier_label = tier_labels.get(tier_name, '📙 Other')

The comment is incomplete - it doesn't mention the 'language' and 'mbasic' tier mappings.

---

#### code_vs_comment_conflict

**Description:** Comment describes link format but doesn't match actual regex pattern

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment in _create_text_markup_with_links() at line ~230:
"Links are marked with [text] in the rendered output. This method finds ALL [text] patterns for display/navigation, but uses the renderer's links for target mapping when following links."

But the actual regex pattern is:
link_pattern = r'\[([^\]]+)\](?:\([^)]+\))?'

This matches both [text] AND [text](url) formats, not just [text]. The comment is incomplete.

---

#### Code vs Comment conflict

**Description:** Comment claims QUIT_KEY has no keyboard shortcut, but QUIT_ALT_KEY (Ctrl+C) is documented as an alternative quit method. The comment is misleading about quit functionality.

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Lines 138-145:
# Quit - No dedicated keyboard shortcut (most Ctrl keys intercepted by terminal or already assigned)
# Primary method: Use menu (Ctrl+U -> File -> Quit)
# Alternative: Ctrl+C (interrupt signal) will also quit - see QUIT_ALT_KEY below
QUIT_KEY = None  # No keyboard shortcut

# Alternative quit via interrupt signal (Ctrl+C)
# Note: This is not a standard keybinding but a signal handler, hence "alternative"
_quit_alt_from_json = _get_key('editor', 'quit')
QUIT_ALT_KEY = _ctrl_key_to_urwid(_quit_alt_from_json) if _quit_alt_from_json else 'ctrl c'

The comment says there's no keyboard shortcut, but then immediately defines QUIT_ALT_KEY as Ctrl+C. This is contradictory - either Ctrl+C is a quit shortcut or it isn't.

---

#### Documentation inconsistency

**Description:** CONTINUE_KEY is documented with dual purpose (Go to line / Continue execution) but the JSON key name 'goto_line' only reflects one purpose, creating confusion.

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Lines 180-185:
# Go to line (also used for Continue execution in debugger context)
# Note: This key serves dual purpose - "Go to line" in editor mode and
# "Continue execution (Go)" in debugger mode. The JSON key is 'goto_line'
# to reflect its primary function, but CONTINUE_KEY name reflects debugger usage.
_continue_from_json = _get_key('editor', 'goto_line')
CONTINUE_KEY = _ctrl_key_to_urwid(_continue_from_json) if _continue_from_json else 'ctrl g'

The variable name CONTINUE_KEY suggests debugger functionality, but the JSON key 'goto_line' suggests editor functionality. This naming mismatch makes the code harder to understand and maintain.

---

#### Code vs Documentation inconsistency

**Description:** In-page search keybindings documented in code comments but missing from tk_keybindings.json

**Affected files:**
- `src/ui/tk_help_browser.py`
- `src/ui/tk_keybindings.json`

**Details:**
tk_help_browser.py lines 113-117 document local widget bindings:
# Return key in search box navigates to next match (local widget binding)
# Note: This binding is specific to the in-page search entry widget and is not
# documented in tk_keybindings.json, which only documents global application
# keybindings. Local widget bindings are documented in code comments only.
self.inpage_search_entry.bind('<Return>', lambda e: self._inpage_find_next())
# ESC key closes search bar (local widget binding, not in tk_keybindings.json)
self.inpage_search_entry.bind('<Escape>', lambda e: self._inpage_search_close())

However, tk_keybindings.json only documents the global Ctrl+F binding under help_browser.inpage_search, but does not document the Return and Escape bindings that work within the in-page search bar. The comment explicitly states these are intentionally excluded, but this creates incomplete documentation of the help browser's keybindings.

---

#### Code vs Comment conflict

**Description:** Comment about failed restore tracking contradicts error handling approach

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Line 207 comment states:
# Track failed restores - user should know if settings couldn't be restored

However, the actual error handling (lines 207-220) only shows a warning if restores fail, but doesn't prevent the dialog from closing. This means the user is warned but the dialog still closes, potentially leaving the application in an inconsistent state. The comment suggests this is intentional ('user should know') but doesn't explain why closing the dialog is still the right action when restores fail.

---

#### code_vs_comment

**Description:** Comment states immediate_history and immediate_status are 'always None' but provides incorrect reasoning

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines 293-297 comment states:
# Set immediate_history and immediate_status to None
# These attributes are not currently used but are set to None for defensive programming
# in case future code tries to access them (will get None instead of AttributeError)

However, lines 141-143 in __init__ already set these to None with comment:
# Immediate mode widgets and executor
# Note: immediate_history and immediate_status are always None in Tk UI (see lines 293-297)

The comment at lines 141-143 references lines 293-297 as explanation, but lines 293-297 don't explain WHY they're always None in Tk UI - they just say it's for defensive programming. The real reason appears to be architectural: Tk UI uses immediate_entry (Entry widget) instead of history/status widgets.

---

#### code_vs_comment

**Description:** Comment about Ctrl+I binding location contradicts actual binding location

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line 455 comment states:
# Note: Ctrl+I is bound directly to editor text widget in start() (not root window)
# to prevent tab key interference - see editor_text.text.bind('<Control-i>', ...)

However, the actual binding at line 237 is:
self.editor_text.text.bind('<Control-i>', self._on_ctrl_i)

This is correct and matches the comment. But then line 455 says 'see editor_text.text.bind' as if pointing to a specific line, when it should reference line 237. The comment is technically correct but the cross-reference is vague.

---

#### code_vs_comment

**Description:** Comment about toolbar simplification references removed features but doesn't explain why

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines 571-576 comment states:
# Note: Toolbar has been simplified to show only essential execution controls.
# Additional features are accessible via menus:
# - List Program → Run > List Program
# - New Program (clear) → File > New
# - Clear Output → Run > Clear Output

This suggests the toolbar was previously more complex and was simplified, but doesn't explain the rationale. The comment lists where to find the removed features but doesn't document why they were removed from the toolbar. This is informational but incomplete historical context.

---

#### code_vs_comment

**Description:** Comment about INPUT row visibility control is incomplete

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines 267-269 comment states:
# INPUT row (hidden by default, shown when INPUT statement needs input)
# Visibility controlled via pack() when showing, pack_forget() when hiding
# Don't pack yet - will be packed when needed

This explains the visibility mechanism but doesn't reference where the show/hide logic is implemented. The comment should point to the methods that control this (likely _show_input_row() and _hide_input_row() or similar, but these aren't visible in the provided code).

---

#### code_vs_comment

**Description:** Comment about variable window heading click behavior doesn't match implementation complexity

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines 1113-1119 comment states:
Handle clicks on variable list column headings.

Only the Variable column (column #0) is sortable - clicking it cycles through
different sort modes (see _cycle_variable_sort() for the cycle order).
Type and Value columns are not sortable.

However, lines 1135-1152 show more complex logic:
- Left 20 pixels (arrow area) = toggle sort direction
- Rest of header = cycle/set sort column

The docstring doesn't mention the arrow click behavior at all, only mentioning cycling through sort modes. This is a significant omission of functionality.

---

#### code_vs_comment_conflict

**Description:** Comment claims formatting may occur elsewhere, but code explicitly avoids formatting to preserve MBASIC compatibility

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _refresh_editor method around line 1150:
Comment says: "(Note: 'formatting may occur elsewhere' refers to the Variables and Stack windows, which DO format data for display - not the editor/program text itself)"

This parenthetical note appears to be defending against a concern that doesn't exist - the code already preserves text exactly as stored. The comment creates confusion by mentioning formatting that occurs in other windows, which is irrelevant to this method's purpose.

---

#### code_vs_comment_conflict

**Description:** Comment about when _validate_editor_syntax is called doesn't match actual call sites

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _validate_editor_syntax method around line 1230:
Comment says: "Note: This method is called:
- With 100ms delay after cursor movement/clicks (to avoid excessive validation during rapid editing)
- Immediately when focus leaves editor (to ensure validation before switching windows)"

However, looking at actual call sites:
- _on_cursor_move: calls with 100ms delay (matches comment)
- _on_mouse_click: calls with 100ms delay (matches comment)
- _on_focus_out: calls immediately (matches comment)
- _on_enter_key: NOT mentioned in comment but calls immediately at line 1380

The comment is incomplete - it doesn't mention the call from _on_enter_key which validates syntax after Enter key press.

---

#### code_vs_comment_conflict

**Description:** Comment about when _remove_blank_lines is called contradicts potential future usage

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _remove_blank_lines method around line 1330:
Comment says: "Currently called only from _on_enter_key (after each Enter key press), not after pasting or other modifications. This provides cleanup when the user presses Enter to move to a new line."

The word 'Currently' suggests this may change in the future, but the method implementation doesn't have any guards or parameters to handle being called from different contexts. If it were called after pasting, the cursor position restoration logic might not work correctly. Either: (1) the comment should be more definitive about the single call site, or (2) the method should be made more robust for multiple call contexts.

---

#### code_vs_comment

**Description:** Comment claims blank lines are removed after key press, but code only schedules removal without guaranteeing execution

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1050: '# Schedule blank line removal after key is processed'
Code: 'self.root.after(10, self._remove_blank_lines)'
The comment implies blank lines WILL be removed, but after() only schedules it - if user types rapidly or other events occur, the removal may be delayed or skipped. The comment should clarify this is scheduled/asynchronous.

---

#### code_vs_comment

**Description:** Comment about cursor movement clearing highlight conflicts with actual trigger condition

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1042: 'Clear yellow statement highlight on any keypress when paused at breakpoint - Clears on ANY key (even arrows/function keys)'
Code at line ~1044: 'if self.paused_at_breakpoint: self._clear_statement_highlight()'
The comment emphasizes clearing on 'ANY key (even arrows/function keys)' but the actual condition only checks paused_at_breakpoint flag, not whether the key is an arrow or function key. The emphasis on 'ANY key' seems to suggest this was a design decision, but the code doesn't distinguish between key types.

---

#### code_vs_comment

**Description:** Comment about line change detection logic doesn't match actual implementation conditions

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1120: 'Determine if program needs to be re-sorted: 1. Line number changed on existing line (both old and new are not None), OR 2. Line number was removed (old was not None, new is None and line has content)'
Followed by: 'Don't trigger sort when: - old_line_num is None: First time tracking this line (cursor just moved here, no editing yet)'
However, the code at line ~1127 checks 'if old_line_num != new_line_num:' BEFORE checking if old_line_num is None. This means the condition structure doesn't exactly match the comment's description. The logic is correct but the comment could be clearer about the order of checks.

---

#### code_vs_comment

**Description:** Comment about paste behavior describes two cases but implementation treats them differently than described

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~920: 'Multi-line paste or single-line paste into blank line - use auto-numbering logic. Both cases use the same logic (split by \n, process each line): 1. Multi-line paste: sanitized_text contains \n → multiple lines to process 2. Single-line paste into blank line: current_line_text empty → one line to process'
However, the code at line ~905 already handled single-line paste into existing line with a return 'break', so case 2 (single-line paste into blank line) is actually a subset of the multi-line logic, not a separate case. The comment makes it sound like both cases are equivalent, but they're handled by different code paths.

---

#### code_vs_comment

**Description:** Comment claims immediate mode execution doesn't echo commands, but this contradicts typical BASIC behavior documentation

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_immediate() method around line 1090:
Comment states: "Execute without echoing (GUI design choice that deviates from typical BASIC behavior: command is visible in entry field, and 'Ok' prompt is unnecessary in GUI context - only results are shown. Traditional BASIC echoes to output.)"

This comment acknowledges a deviation from documented BASIC behavior but doesn't clarify if this is intentional or if documentation should be updated to reflect GUI-specific behavior.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation about INPUT vs LINE INPUT behavior strategy

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
TkIOHandler class docstring states:
"Input strategy:
- INPUT statement: Uses inline input field when backend available,
  otherwise uses modal dialog (not a preference, but availability-based)
- LINE INPUT statement: Always uses modal dialog for consistent UX"

But the input() method docstring states:
"Prefers inline input field below output pane when backend is available,
but falls back to modal dialog if backend is not available."

While the input_line() method docstring states:
"Unlike input() which prefers inline input field, this ALWAYS uses
a modal dialog regardless of backend availability."

The word 'prefers' vs 'uses when available' creates ambiguity about whether this is a preference or a hard requirement based on availability.

---

#### code_vs_comment

**Description:** Comment claims has_work() is only called in one location, but this is a maintenance assertion that could become outdated

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_immediate() method around line 1125:
"# Use has_work() to check if the interpreter is ready to execute (e.g., after RUN command).
# This is the only location in tk_ui.py that calls has_work()."

This type of comment creates a maintenance burden - if has_work() is called elsewhere in the future, this comment becomes incorrect. Such assertions should be verified by tooling, not comments.

---

#### code_vs_comment

**Description:** Comment about race condition prevention uses redundant checks that may indicate unclear state management

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _update_immediate_status() method around line 1020:
"# Check if safe to execute - use both can_execute_immediate() AND self.running flag
# The 'not self.running' check prevents immediate mode execution when a program is running,
# even if the tick hasn't completed yet. This prevents race conditions where immediate
# mode could execute while the program is still running but between tick cycles.
can_exec_immediate = self.immediate_executor.can_execute_immediate()
can_execute = can_exec_immediate and not self.running"

The comment suggests that can_execute_immediate() alone is insufficient and requires an additional self.running check. This indicates either:
1. can_execute_immediate() is not correctly checking all necessary conditions
2. There's unclear ownership of execution state between components
3. The state management design has race conditions that require defensive checks

---

#### code_vs_comment

**Description:** Docstring claims error takes priority and breakpoint becomes visible after fixing error, but _on_status_click() shows both error and breakpoint messages, suggesting they can coexist visually

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Class docstring says:
"Status priority (when both error and breakpoint):
- ? takes priority (error shown)
- After fixing error, ● becomes visible (automatically handled by set_error() method
  which checks has_breakpoint flag when clearing errors)"

But _on_status_click() docstring says:
"Displays informational messages about line status:
- For error markers (?): Shows error message in a message box
- For breakpoint markers (●): Shows confirmation message that breakpoint is set"

The code in _on_status_click() checks error_msg first, then checks has_breakpoint in else clause, confirming only one symbol shows at a time. However, the phrasing "automatically handled" is misleading - it's just standard if/elif logic in set_error(), not special automatic handling.

---

#### code_vs_comment

**Description:** _delete_line() docstring has confusing dual numbering explanation that may mislead developers

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Docstring says:
"Args:
    line_num: Tkinter text widget line number (1-based sequential index),
             not BASIC line number (e.g., 10, 20, 30).
             Note: This class uses dual numbering - editor line numbers for
             text widget operations, BASIC line numbers for line_metadata lookups."

This is accurate but the note about 'dual numbering' appears in _delete_line() which only uses editor line numbers. The note would be more appropriate in the class docstring or in methods that convert between the two (like _redraw() or _on_status_click()).

---

#### code_vs_comment

**Description:** _on_status_click() uses different regex pattern than _parse_line_number() for extracting BASIC line numbers

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
_parse_line_number() uses: r'^(\d+)(?:\s|$)'
This requires whitespace OR end-of-string after the line number.

_on_status_click() uses: r'^\s*(\d+)'
This only requires digits, with optional leading whitespace, but doesn't verify anything comes after.

This means _on_status_click() would match '10REM' and extract '10', while _parse_line_number() would reject it. This inconsistency could cause the status click handler to show info for lines that _parse_line_number() considers invalid.

---

#### code_vs_comment

**Description:** Comment in serialize_line() describes fallback behavior that doesn't match actual implementation logic

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment states: "Note: If source_text doesn't match pattern (or is unavailable), falls back to relative_indent=1.
When does this occur?
1. Programmatically inserted lines (no source_text attribute)
2. Lines where source_text doesn't start with line_number + spaces (edge case)"

However, the code only sets relative_indent=1 as initial default before checking source_text. If source_text exists but doesn't match the pattern, relative_indent remains 1 (the default), but the comment implies this is a deliberate fallback case. The code doesn't explicitly handle the 'doesn't match pattern' case separately from the 'no source_text' case.

---

#### documentation_inconsistency

**Description:** Module docstring claims 'No UI-framework dependencies' but doesn't mention the runtime/parser/AST dependencies that are allowed

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Module docstring states: "No UI-framework dependencies (Tk, curses, web)
are allowed. Standard library modules (os, glob, re) and core interpreter
modules (runtime, parser, AST nodes) are permitted."

However, the actual imports only show: from typing import Dict, List, Tuple, Optional, Set
import re

The module doesn't import runtime, parser, or AST nodes directly. These are passed as parameters or accessed via attributes. The docstring should clarify that these are 'accepted as parameters' rather than 'imported', or the docstring is outdated from a refactoring.

---

#### code_vs_comment

**Description:** Comment in update_line_references() describes pattern behavior that may not match actual regex behavior for edge cases

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment states: "Note: Pattern uses .+? (non-greedy) to match expression in ON statements,
which correctly handles edge cases like 'ON FLAG GOTO' (variable starting with 'G'),
'ON X+Y GOTO' (expressions), and 'ON A$ GOTO' (string variables)"

The pattern is: r'\b(GOTO|GOSUB|THEN|ELSE|ON\s+.+?\s+GOTO|ON\s+.+?\s+GOSUB)\s+(\d+)'

The .+? pattern will match any characters non-greedily, but the comment claims it 'correctly handles' these cases without explaining what 'correctly' means. For 'ON FLAG GOTO 10', the pattern would match 'ON FLAG GOTO' as the keyword group, which is correct. However, for nested expressions like 'ON X GOTO 10 : ON Y GOTO 20', the non-greedy match might not behave as expected if there are multiple GOTO keywords on the same line.

---

#### code_vs_documentation

**Description:** serialize_expression() docstring describes ERR/ERL special handling but doesn't explain why this is necessary or what the alternative would be

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring states: "Note:
ERR and ERL are special system variables that are serialized without
parentheses (e.g., 'ERR' not 'ERR()') when they appear as FunctionCallNode
with no arguments, matching MBASIC 5.21 syntax."

This note explains WHAT the code does but not WHY. The implementation shows:
if expr.name in ('ERR', 'ERL') and len(expr.arguments) == 0:
    return expr.name

The docstring should explain:
1. Why ERR/ERL are represented as FunctionCallNode instead of VariableNode in the AST
2. What would happen if they were serialized with parentheses
3. Whether this is a parser quirk or a BASIC language requirement

Without this context, maintainers might not understand why this special case exists.

---

#### Code vs Documentation inconsistency

**Description:** Comment in cmd_run() claims 'Runtime accesses program.line_asts directly, no need for program_ast variable' but this is misleading - the code does pass program.line_asts to Runtime constructor, so there IS a need to access it, just not to store it in a separate variable first.

**Affected files:**
- `src/ui/visual.py`

**Details:**
Comment says: '(Runtime accesses program.line_asts directly, no need for program_ast variable)'
Code shows: 'self.runtime = Runtime(self.program.line_asts, self.program.lines)'
The comment suggests Runtime accesses it directly without passing, but the code explicitly passes it as a constructor argument.

---

#### Code vs Comment conflict

**Description:** The value property getter has a comment 'Sometimes event args are dict - return empty string' suggesting defensive programming, but there's no explanation of why event args would be a dict when the setter and internal handler treat it as a string.

**Affected files:**
- `src/ui/web/codemirror5_editor.py`

**Details:**
Property getter:
        if isinstance(self._value, dict):
            # Sometimes event args are dict - return empty string
            return ''
        return self._value or ''

This suggests a known issue where _value can become a dict, but the setter and change handler both treat it as a string. This inconsistency is not explained.

---

#### code_vs_comment

**Description:** Comment claims input echoing happens naturally via editable textarea, but code shows input field is separate from output textarea

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~70 says:
# Note: Input echoing (displaying what user typed) happens naturally because
# the user types directly into the output textarea, which is made editable
# by _enable_inline_input() in the NiceGUIBackend class.

However, the UI structure shows separate elements:
- self.input_row (line ~1009)
- self.input_label (line ~1010)
- self.input_field (line ~1011)
- self.input_submit_btn (line ~1012)

These are separate UI elements for inline input, not making the output textarea editable.

---

#### code_vs_comment

**Description:** VariablesDialog sort defaults claim to match Tk UI but may differ

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~127:
# Sort state (matches Tk UI defaults: see sort_mode and sort_reverse in src/ui/tk_ui.py)
self.sort_mode = 'accessed'  # Current sort mode
self.sort_reverse = True  # Sort direction

This references tk_ui.py for verification, but without seeing that file, cannot confirm if defaults actually match. The comment suggests they should be identical.

---

#### code_vs_comment

**Description:** Comment claims output is NOT cleared on RUN, but Step commands DO clear output. However, examining the step command implementations (_menu_step_line and _menu_step_stmt), there is no code that clears output.

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~1845 states:
"# Note: Output is NOT cleared - continuous scrolling like ASR33 teletype"
and
"# Note: Step commands (Ctrl+T/Ctrl+K) DO clear output for clarity when debugging"

However, in _menu_step_line (around line 2050) and _menu_step_stmt (around line 2100), the code contains:
"# Note: Output is NOT cleared - continuous scrolling like ASR33 teletype"

There is no code in either step method that calls any clear/reset function on self.output or self._append_output. The comment claims step commands clear output, but the implementation does not.

---

#### code_vs_comment

**Description:** Comment about INPUT handling references line 1932, but the actual _execute_tick method appears to be at a different location in the provided excerpt.

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~1730 states:
"# INPUT handling: When INPUT statement executes, the immediate_entry input box
# is focused for user input (see _execute_tick() at line 1932)."

The _execute_tick method in the provided code is around line 1880-1990, not line 1932. This line number reference may be outdated from code refactoring.

---

#### code_vs_comment

**Description:** Comment in _menu_run claims RUN does NOT clear output, but the comment references 'line ~1845 below' which is confusing given the actual line numbers in the code.

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment in _menu_run (around line 1820) states:
"Note: This implementation does NOT clear output (see comment at line ~1845 below)."

The line reference '~1845 below' is vague and may be outdated. The actual comment about not clearing output appears to be at a different location.

---

#### code_vs_comment

**Description:** Comment in _handle_step_result claims to use 'microprocessor model' but the actual implementation checks multiple state properties in a specific order that may not align with a pure microprocessor model.

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~2150 states:
"# Use microprocessor model: check error_info, input_prompt, and runtime.halted"

However, the implementation checks state.input_prompt first, then state.error_info, then runtime.halted. A true microprocessor model would typically check error conditions first. This may be intentional design, but the comment could be misleading about the actual priority order.

---

#### code_vs_comment

**Description:** Comment claims PC is conditionally preserved based on exec_timer state, but code logic doesn't match the described behavior

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _sync_program_to_runtime() method:

Comment says:
"PC handling (conditional preservation):
- If exec_timer is active (execution in progress): Preserves PC and halted state,
  allowing program to resume from current position after rebuild.
- Otherwise (no active execution): Resets PC to halted state, preventing
  unexpected execution when LIST/edit commands modify the program."

But the code checks:
if self.exec_timer and self.exec_timer.active:
    # Preserve PC
else:
    # Reset to halted

The comment describes this as preventing "unexpected execution" but the actual purpose appears to be about state consistency during rebuilds. The comment's explanation about "preventing unexpected execution when LIST/edit commands run" is misleading because LIST/edit commands don't trigger execution - they just rebuild the statement table.

---

#### code_vs_comment

**Description:** Comment about paste detection threshold is arbitrary and may not match actual behavior

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _on_editor_change() method:

Comment says:
"Detect paste: large content change (threshold: >5 chars)
This heuristic helps clear auto-number prompts before paste content merges with them.
The 5-char threshold is arbitrary - balances detecting small pastes while avoiding
false positives from rapid typing (e.g., typing 'PRINT' quickly = 5 chars but not a paste)."

The comment admits the threshold is arbitrary and gives an example where typing 'PRINT' (5 chars) would NOT trigger paste detection, but the code uses >5 (greater than 5), meaning 'PRINT' (exactly 5 chars) wouldn't trigger it anyway. The comment's example doesn't match the actual threshold logic.

---

#### code_vs_comment

**Description:** Comment about architecture decision contradicts actual code behavior

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _execute_immediate() method:

Comment says:
"Architecture: We do NOT auto-sync editor from AST after immediate commands.
This preserves one-way data flow (editor → AST → execution) and prevents
losing user's formatting/comments. Commands that modify code (like RENUM)
update the editor text directly."

However, the code calls:
self._save_editor_to_program()
self._sync_program_to_runtime()

This IS syncing from editor to program/runtime, which contradicts the claim about "one-way data flow". The comment seems to be describing a different sync direction (AST → editor) than what the code does (editor → AST).

---

#### code_vs_comment

**Description:** Comment claims 'errors are caught and logged, won't crash the UI' but the timer callback save_state_periodic() could still raise exceptions that propagate

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~470: '# Save state periodically (errors are caught and logged, won't crash the UI)'

But the timer is set up as:
ui.timer(5.0, save_state_periodic)

The save_state_periodic function has try/except, but if ui.timer itself or the serialization in backend.serialize_state() raises an exception outside the try block, it could still crash. The comment overstates the error handling robustness.

---

#### code_internal_inconsistency

**Description:** Inconsistent error handling between save_state_periodic and save_on_disconnect callbacks

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Both callbacks have identical try/except blocks:

try:
    app.storage.client['session_state'] = backend.serialize_state()
except Exception as e:
    sys.stderr.write(f'Warning: Failed to save session state: {e}\n')
    sys.stderr.flush()

However, save_on_disconnect has a different error message: 'Failed to save final session state'

This is minor but shows slight inconsistency in error messaging approach. Both should probably use the same message or the distinction should be more meaningful.

---

#### code_vs_documentation

**Description:** Debugging documentation references keyboard shortcuts that vary by UI, but web_settings_dialog.py doesn't show any keyboard shortcut configuration

**Affected files:**
- `docs/help/common/debugging.md`
- `src/ui/web/web_settings_dialog.py`

**Details:**
debugging.md states: 'Debugging keyboard shortcuts vary by UI. See your UI-specific help for complete keyboard shortcut reference' and lists shortcuts like 'Ctrl+T' for Step.

However, web_settings_dialog.py only shows settings for:
- editor.auto_number (checkbox)
- editor.auto_number_step (number input)
- limits.* (read-only display)

No keyboard shortcut configuration is present in the settings dialog, despite web_keybindings.json defining shortcuts like F1, F5, F9, F10, Ctrl+R, etc.

---

#### code_vs_documentation

**Description:** Debugging documentation describes Variables Window and Execution Stack features, but session_state.py doesn't track this UI state

**Affected files:**
- `docs/help/common/debugging.md`
- `src/ui/web/session_state.py`

**Details:**
debugging.md describes:
- Variables Window with sorting, editing, array tracking
- Execution Stack Window showing FOR loops and GOSUB calls
- Statement highlighting with current statement index

But SessionState dataclass only tracks:
- running, paused, output_text (basic execution state)
- editor_content, editor_cursor (editor state)
- last_find_text, last_find_position (find/replace state)
- No variables_window_open, stack_window_open, or current_statement_index fields

This suggests either:
1. These windows are not persisted in session state (inconsistent with Redis-backed sessions)
2. Documentation describes features not yet implemented in web UI

---

#### documentation_inconsistency

**Description:** Compiler documentation describes 27 optimizations as 'implemented' but index.md says code generation is 'In Progress'

**Affected files:**
- `docs/help/common/compiler/optimizations.md`
- `docs/help/common/compiler/index.md`

**Details:**
optimizations.md states: '27 optimizations implemented in the semantic analysis phase. All optimizations preserve the original program behavior while improving performance or reducing resource usage.'

But index.md states: 'Code Generation - Status: In Progress - Documentation for the code generation phase will be added as the compiler backend is developed.'

This creates confusion about whether the compiler is functional or still under development. The optimizations are described as 'implemented' but code generation is 'in progress', suggesting the optimizations exist but can't generate actual code yet.

---

#### code_vs_documentation

**Description:** SessionState tracks auto_save_enabled and auto_save_interval but these settings are not mentioned in web_settings_dialog.py or debugging documentation

**Affected files:**
- `src/ui/web/session_state.py`
- `docs/help/common/debugging.md`

**Details:**
SessionState defines:
auto_save_enabled: bool = True
auto_save_interval: int = 30

But web_settings_dialog.py only shows:
- editor.auto_number
- editor.auto_number_step
- limits.* (read-only)

No auto-save settings are exposed in the UI, despite being tracked in session state. This suggests either:
1. Auto-save is implemented but not configurable
2. These fields are planned but not yet used
3. Settings dialog is incomplete

---

#### documentation_inconsistency

**Description:** ATN function documentation mentions precision limitation when computing PI, but the appendices/math-functions.md doesn't mention this important caveat when showing PI calculation examples

**Affected files:**
- `docs/help/common/language/functions/atn.md`
- `docs/help/common/language/appendices/math-functions.md`

**Details:**
In atn.md: "**Note:** When computing PI with `ATN(1) * 4`, the result is limited to single precision (~7 digits). For higher precision, use `ATN(CDBL(1)) * 4` to get double precision."

In math-functions.md under 'Computing Pi' section, it shows both methods but doesn't explain the precision difference or why you'd use CDBL.

---

#### documentation_inconsistency

**Description:** FIX documentation references INT but INT documentation is incomplete in the provided files

**Affected files:**
- `docs/help/common/language/functions/fix.md`
- `docs/help/common/language/functions/int.md`

**Details:**
In fix.md: "FIX(X) is equivalent to SGN(X)*INT(ABS(X)). The major difference between FIX and INT is that FIX does not return the next lower number for negative X."

The INT function documentation is referenced in 'See Also' sections but the actual int.md file content is not fully shown in the provided documentation. The relationship between FIX and INT is explained in FIX but may not be reciprocally explained in INT.

---

#### documentation_inconsistency

**Description:** data-types.md references getting-started.md in 'See Also' section but file doesn't exist

**Affected files:**
- `docs/help/common/language/data-types.md`

**Details:**
In data-types.md 'See Also' section: "- [Variables](../getting-started.md#variables) - Using variables"

This creates a broken link as getting-started.md is not in the provided documentation.

---

#### documentation_inconsistency

**Description:** index.md references shortcuts.md and examples.md which are not provided in the documentation set

**Affected files:**
- `docs/help/common/index.md`

**Details:**
In index.md under 'Topics' section:
[Keyboard Shortcuts](shortcuts.md)
[Examples](examples.md)

These files are not included in the provided documentation, creating broken links.

---

#### documentation_inconsistency

**Description:** EOF documentation references LINE INPUT# with incorrect link path

**Affected files:**
- `docs/help/common/language/functions/eof.md`

**Details:**
In eof.md 'See Also' section:
- [LINE INPUT#](../statements/inputi.md) - Read entire line from file

The link path is 'inputi.md' but based on naming conventions in other files, it should likely be 'line-input-hash.md' or 'line-input_hash.md'. The inconsistent naming makes this unclear.

---

#### documentation_inconsistency

**Description:** Contradictory information about Control-C behavior

**Affected files:**
- `docs/help/common/language/functions/inkey_dollar.md`
- `docs/help/common/language/functions/input_dollar.md`

**Details:**
INKEY$.md states: 'Note: Control-C behavior varied in original implementations. In MBASIC 5.21 interpreter, Control-C would terminate the program. In the BASIC Compiler, Control-C was passed through. This implementation follows compiler behavior and passes Control-C through (CHR$(3)) for program detection and handling.'

INPUT$.md states: 'Note: In MBASIC 5.21 interpreter, Control-C would interrupt INPUT$ and terminate the wait. This implementation passes Control-C through (CHR$(3)) for program detection and handling, matching compiler behavior.'

Both claim to match compiler behavior but describe different original MBASIC 5.21 behaviors (terminate program vs interrupt/terminate wait).

---

#### documentation_inconsistency

**Description:** Inconsistent implementation note formatting and terminology

**Affected files:**
- `docs/help/common/language/functions/inp.md`
- `docs/help/common/language/functions/peek.md`
- `docs/help/common/language/functions/lpos.md`

**Details:**
INP.md uses: '⚠️ **Not Implemented**: This feature requires direct hardware I/O port access and is not implemented in this Python-based interpreter. **Behavior**: Always returns 0'

PEEK.md uses: 'ℹ️ **Emulated with Random Values**: PEEK does NOT read actual memory. Instead, it returns a random value between 0-255 (inclusive). **Behavior**: Each call to PEEK returns a new random integer...'

LPOS.md uses: '⚠️ **Not Implemented**: This feature requires line printer hardware and is not implemented in this Python-based interpreter. **Behavior**: Function always returns 0 (because there is no printer to track position for)'

These implementation notes use different emoji (⚠️ vs ℹ️), different header styles, and different levels of detail. They should follow a consistent template.

---

#### documentation_inconsistency

**Description:** CLEAR documentation contains conflicting information about parameter meanings between MBASIC 5.21 and earlier versions

**Affected files:**
- `docs/help/common/language/statements/clear.md`

**Details:**
The CLEAR.md documentation states:

"**In MBASIC 5.21 (BASIC-80 release 5.0 and later):**
- **expression1**: If specified, sets the highest memory location available for BASIC to use
- **expression2**: Sets the stack space reserved for BASIC (default: 256 bytes or 1/8 of available memory, whichever is smaller)"

But then contradicts itself:

"**Historical note:** In earlier versions of BASIC-80 (before release 5.0), the parameters had different meanings:
- expression1 set the amount of string space
- expression2 set the end of memory

This behavior changed in release 5.0 to support dynamic string allocation."

The documentation should clarify which version's behavior is actually implemented in this interpreter.

---

#### documentation_inconsistency

**Description:** CLS is documented as 'Extended, Disk' version but index.md doesn't clarify version availability for statements

**Affected files:**
- `docs/help/common/language/index.md`
- `docs/help/common/language/statements/cls.md`

**Details:**
CLS.md states:
"**Versions:** Extended, Disk

**Note:** CLS is implemented in MBASIC and works in all UI backends."

However, the language index.md doesn't provide any guidance on version markers or what they mean in the context of this implementation. Users might be confused about whether 'Extended, Disk' means the feature is limited or fully available.

---

#### documentation_inconsistency

**Description:** Example code shows conflicting behavior for type precedence

**Affected files:**
- `docs/help/common/language/statements/defint-sng-dbl-str.md`

**Details:**
Line 60 shows: NAME1$ = "TEST"  ' String (starts with N, but $ suffix overrides DEFINT)
Line 70 shows: AMOUNT = "100"   ' String (starts with A, DEFSTR applies)

The comment on line 60 correctly states that $ suffix overrides DEFINT N-Z, making NAME1$ a string.
However, line 70 assigns a string literal "100" to AMOUNT, which would be a string regardless of DEFSTR A. The example should show AMOUNT without quotes to demonstrate DEFSTR behavior, or the comment should clarify that the literal is a string, not the variable type.

---

#### documentation_inconsistency

**Description:** Contradictory information about CONT behavior after END

**Affected files:**
- `docs/help/common/language/statements/end.md`
- `docs/help/common/language/statements/error.md`

**Details:**
end.md states: "Can be continued with CONT (execution resumes at next statement after END)"

However, this contradicts typical BASIC behavior where END closes files and terminates the program. If CONT can resume after END, it's unclear what state the program is in (are files still closed? does execution truly resume at the next statement?). This needs clarification or correction, as END is typically a terminal statement.

---

#### documentation_inconsistency

**Description:** Vague and potentially incorrect remark about CP/M behavior

**Affected files:**
- `docs/help/common/language/statements/files.md`

**Details:**
files.md states: "Note: CP/M automatically adds .BAS extension if none is specified for BASIC program files."

This is misleading. CP/M itself does not add extensions - this would be MBASIC's behavior when interpreting filenames. The note should clarify that MBASIC (not CP/M) may add .BAS extension in certain contexts, and specify which contexts (LOAD, SAVE, FILES, etc.).

---

#### documentation_inconsistency

**Description:** Incomplete description of semicolon behavior

**Affected files:**
- `docs/help/common/language/statements/input.md`

**Details:**
input.md states two different semicolon behaviors:
1. "A semicolon immediately after INPUT suppresses the carriage return/line feed after the user presses Enter"
2. "A semicolon after the prompt string causes the prompt to be displayed without a question mark"

These are two different positions for the semicolon (INPUT; vs "prompt";) but the documentation doesn't clearly distinguish between INPUT; "prompt" and INPUT "prompt"; and what happens with INPUT; "prompt";. The syntax line shows [;] only once, which is ambiguous.

---

#### documentation_inconsistency

**Description:** Incomplete information about overlapping range behavior

**Affected files:**
- `docs/help/common/language/statements/defint-sng-dbl-str.md`

**Details:**
The documentation states: "Note: When ranges overlap, the last declaration takes precedence. For example, if you declare both DEFDBL L-P and DEFINT I-N, variables starting with L, M, and N would be affected by both declarations, with the later declaration taking effect."

This note is helpful but incomplete. It doesn't specify:
1. Whether "last" means last in the program text or last executed at runtime
2. What happens if DEF statements are in different parts of the program
3. Whether the scope is global or can be changed mid-program

Typically in BASIC, DEF statements are global and order in source matters, but this should be explicit.

---

#### documentation_inconsistency

**Description:** Contradictory information about file closing behavior between LOAD and MERGE

**Affected files:**
- `docs/help/common/language/statements/load.md`
- `docs/help/common/language/statements/merge.md`

**Details:**
load.md states: "LOAD (without ,R): Closes all open files and deletes all variables and program lines currently in memory before loading" and "LOAD with ,R option: Program is RUN after loading, and all open data files are kept open for program chaining"

merge.md states: "File handling: Unlike LOAD (without ,R), MERGE does NOT close open files. Files that are open before MERGE remain open after MERGE completes. (Compare with LOAD which closes files except when using the ,R option.)"

The contradiction: load.md says LOAD without ,R closes files, but merge.md's comparison statement "Compare with LOAD which closes files except when using the ,R option" implies LOAD always closes files except with ,R, which matches load.md. However, the phrasing "Unlike LOAD (without ,R)" is confusing because it suggests LOAD without ,R has different behavior than what's being compared.

---

#### documentation_inconsistency

**Description:** Different terminology for string modification operations

**Affected files:**
- `docs/help/common/language/statements/lset.md`
- `docs/help/common/language/statements/mid-assignment.md`

**Details:**
lset.md describes: "To left-justify a string in a field for random file I/O operations" and explains it "assigns the string expression to the string variable, left-justified in the field."

mid-assignment.md describes: "To replace characters within a string variable without creating a new string" and explains "The MID$ assignment statement modifies a portion of an existing string variable by replacing characters"

Both modify strings in place, but LSET is described as "assigning" while MID$ is described as "replacing" or "modifying". The conceptual difference (LSET for file fields vs MID$ for general strings) is clear, but the terminology inconsistency could confuse users about whether these are fundamentally different operations.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation of file modes

**Affected files:**
- `docs/help/common/language/statements/open.md`
- `docs/help/common/language/statements/printi-printi-using.md`

**Details:**
open.md documents three modes:
- "O" - specifies sequential output mode
- "I" - specifies sequential input mode
- "R" - specifies random input/output mode

printi-printi-using.md mentions: "PRINT# writes data to a sequential file opened for output (mode "O") or append (mode "A")."

The OPEN documentation doesn't mention mode "A" for append, but PRINT# documentation references it. This is an incomplete mode list in the OPEN documentation.

---

#### documentation_inconsistency

**Description:** RESET not mentioned in OPEN's See Also section

**Affected files:**
- `docs/help/common/language/statements/reset.md`
- `docs/help/common/language/statements/open.md`

**Details:**
reset.md states: "The RESET statement closes all files that have been opened with OPEN statements. It performs the same function as executing CLOSE without any file numbers"

open.md See Also section includes CLOSE but not RESET, even though RESET is directly related to file operations initiated by OPEN.

This is a missing cross-reference that would help users discover the RESET command.

---

#### documentation_inconsistency

**Description:** Inconsistent 'Versions' field format across documentation files

**Affected files:**
- `docs/help/common/language/statements/rset.md`
- `docs/help/common/language/statements/run.md`
- `docs/help/common/language/statements/save.md`

**Details:**
Some files use 'Versions: Disk' (rset.md, run.md has '8K, Extended, Disk', save.md), while others use 'Versions: MBASIC Extension' (setsetting.md, showsettings.md). The format should be consistent across all documentation files.

---

#### documentation_inconsistency

**Description:** WIDTH documentation describes unsupported LPRINT syntax but doesn't clearly mark it in syntax section

**Affected files:**
- `docs/help/common/language/statements/width.md`

**Details:**
The Implementation Note says 'WIDTH LPRINT <integer expression>' is NOT SUPPORTED and will cause parse error, but the original Syntax section under 'Historical Reference' shows this syntax without clear warning. The unsupported syntax should be more prominently marked in the syntax section itself.

---

#### documentation_inconsistency

**Description:** Variable name significance documentation contradicts itself

**Affected files:**
- `docs/help/common/language/variables.md`
- `docs/help/common/settings.md`

**Details:**
variables.md states: 'In the original MBASIC 5.21, only the first 2 characters of variable names were significant (AB, ABC, and ABCDEF would be the same variable). This Python implementation uses the full variable name for identification, allowing distinct variables like COUNT and COUNTER.' However, it also states 'Variable names are not case-sensitive by default (Count = COUNT = count)', which seems to contradict the full name usage. The settings.md clarifies this is about case sensitivity, not character significance, but variables.md should be clearer.

---

#### documentation_inconsistency

**Description:** WAIT statement documentation formatting issue

**Affected files:**
- `docs/help/common/language/statements/wait.md`

**Details:**
The Remarks section contains malformed text: 'The data read at the port is exclusive OR~ed with the integer expression J, and then AND~ed with 1.' The tilde characters (~) appear to be formatting artifacts. Should be 'XORed' and 'ANDed' or 'exclusive-ORed' and 'ANDed'.

---

#### documentation_inconsistency

**Description:** Settings documentation references non-existent HELPSETTING command

**Affected files:**
- `docs/help/common/settings.md`

**Details:**
settings.md lists HELPSETTING as an available command under 'CLI (Command Line)' section: 'HELPSETTING editor.auto_number_step      ' Get help for a specific setting'. However, there is no helpsetting.md documentation file in the statements directory, and it's unclear if this command is actually implemented.

---

#### documentation_inconsistency

**Description:** RSET documentation references non-existent RESET statement

**Affected files:**
- `docs/help/common/language/statements/rset.md`

**Details:**
rset.md ends with: '**Note:** Do not confuse RSET with [RESET](reset.md), which closes all open files.' However, there is no reset.md file in the documentation. Either the RESET documentation is missing or this note is incorrect.

---

#### documentation_inconsistency

**Description:** WIDTH implementation note contradicts itself about supported syntax

**Affected files:**
- `docs/help/common/language/statements/width.md`

**Details:**
The Implementation Note states: 'The simple "WIDTH <number>" statement parses and executes successfully without errors' but also says 'The "WIDTH LPRINT" syntax is NOT supported and will cause a parse error.' However, under 'UNSUPPORTED SYNTAX' it shows the original MBASIC 5.21 also supported 'WIDTH LPRINT <integer expression>'. The note should clarify that the base WIDTH command existed in original MBASIC, but this implementation only accepts the simple form as a no-op.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut documentation for Stop/Break functionality in Tk UI

**Affected files:**
- `docs/help/common/ui/tk/index.md`
- `docs/help/mbasic/features.md`

**Details:**
tk/index.md states:
- **Stop** ({{kbd:toggle_breakpoint:tk}}reak) - Interrupt execution

This appears to be a template variable that wasn't properly rendered, suggesting 'toggle_breakpoint' key is used for 'Stop/Break'. However, features.md doesn't clarify this mapping.

---

#### documentation_inconsistency

**Description:** Contradictory information about Web UI file persistence and settings storage

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/extensions.md`

**Details:**
compatibility.md states:
- Files stored in server-side memory (sandboxed filesystem per session)
- Files persist during browser session but are lost on page refresh
- Note: Settings (not files) can persist via Redis if configured - see [Web UI Settings](../ui/web/settings.md)

But extensions.md states:
- **Session-based storage** - Files persist during browser session only (lost on page refresh)

The compatibility.md mentions Redis for settings persistence, but extensions.md makes no mention of any persistence mechanism. This creates confusion about what actually persists.

---

#### documentation_inconsistency

**Description:** Debugging features availability description differs between documents

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/extensions.md`

**Details:**
features.md states:
- **Breakpoints** - Set/clear breakpoints (available in all UIs; access method varies)
- **Step execution** - Execute one line at a time (available in all UIs; access method varies)
- **Variable viewing** - Monitor variables (available in all UIs; access method varies)
- **Stack viewer** - View call stack (available in all UIs; access method varies)

But extensions.md states:
**Availability:** CLI (command form), Curses (Ctrl+B), Tk (UI controls)

This suggests these features are NOT available in Web UI, contradicting features.md claim of 'available in all UIs'.

---

#### documentation_inconsistency

**Description:** Auto-save behavior documentation differs between documents

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/extensions.md`

**Details:**
features.md states:
- Auto-save behavior varies by UI:
  - **CLI, Tk, Curses:** Save to local filesystem (persistent)
  - **Web UI:** Files stored in server-side session memory only (not persistent across page refreshes)

But extensions.md states:
- **Auto-save** - ❌ | ✅ (Tk) | Extension

This suggests only Tk has auto-save, contradicting features.md which mentions CLI and Curses also save to local filesystem.

---

#### documentation_inconsistency

**Description:** PEEK/POKE behavior described differently in architecture vs compatibility docs

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/compatibility.md`

**Details:**
architecture.md states:
- PEEK: Returns random integer 0-255 (for RNG seeding compatibility)
- POKE: Parsed and executes successfully, but performs no operation (no-op)
- **PEEK does NOT return values written by POKE** - no memory state is maintained

compatibility.md states the same but adds:
- No access to actual system memory

The architecture.md should mention this security/design rationale as well for consistency.

---

#### documentation_inconsistency

**Description:** Missing Web UI settings documentation referenced in compatibility guide

**Affected files:**
- `docs/help/index.md`
- `docs/help/common/ui/tk/index.md`

**Details:**
compatibility.md references:
- see [Web UI Settings](../ui/web/settings.md)

But index.md lists UI-specific help as:
- [Tk (Desktop GUI)](ui/tk/index.md)
- [Curses (Terminal)](ui/curses/index.md)
- [Web Browser](ui/web/index.md)
- [CLI (Command Line)](ui/cli/index.md)

The path '../ui/web/settings.md' is referenced but not listed in the main index, suggesting missing documentation.

---

#### documentation_inconsistency

**Description:** Inconsistent UI count - getting-started mentions 4 UIs but index mentions 3

**Affected files:**
- `docs/help/mbasic/getting-started.md`
- `docs/help/mbasic/index.md`

**Details:**
getting-started.md states 'MBASIC supports four interfaces' and lists CLI, Curses, Tkinter, and Web UI. However, index.md under 'Key Features' only mentions 'Choice of user interfaces (CLI, Curses, Tkinter)' - omitting Web UI from the list.

---

#### documentation_inconsistency

**Description:** Inconsistent prompt format in code examples

**Affected files:**
- `docs/help/mbasic/getting-started.md`
- `docs/help/ui/cli/debugging.md`

**Details:**
getting-started.md uses bare prompt without 'Ready':
```
10 PRINT "Hello, World!"
20 END
RUN
```

But debugging.md consistently uses 'Ready' prompt:
```
Ready
BREAK 100
Breakpoint set at line 100
Ready
```

The actual MBASIC prompt behavior should be documented consistently.

---

#### documentation_inconsistency

**Description:** SHOWSETTINGS and SETSETTING commands not listed in CLI index

**Affected files:**
- `docs/help/ui/cli/settings.md`
- `docs/help/ui/cli/index.md`

**Details:**
cli/settings.md documents SHOWSETTINGS and SETSETTING as CLI commands with full syntax and examples. However, cli/index.md's 'Common Commands' section does not list these commands:
- LIST - Show program
- RUN - Execute program
- LOAD "file.bas" - Load program
- SAVE "file.bas" - Save program
- NEW - Clear program
- AUTO - Auto line numbering
- RENUM - Renumber lines
- SYSTEM - Exit MBASIC

The settings commands should be included in the common commands list or have a dedicated section.

---

#### documentation_inconsistency

**Description:** Variables inspection documentation exists but not linked from CLI index

**Affected files:**
- `docs/help/ui/cli/variables.md`
- `docs/help/ui/cli/index.md`

**Details:**
cli/variables.md provides comprehensive documentation on variable inspection in CLI mode, but cli/index.md does not link to it. The index shows:

**Debugging Commands:**
- [Debugging Guide](debugging.md) - Complete debugging reference
- BREAK - Set/clear breakpoints
- STEP - Single-step execution
- STACK - View call stack

Variable inspection is a debugging feature and should be linked here.

---

#### documentation_inconsistency

**Description:** Broken internal link to keyboard shortcuts

**Affected files:**
- `docs/help/ui/curses/editing.md`

**Details:**
curses/editing.md contains: 'See Also: [Keyboard Shortcuts](../../../user/keyboard-shortcuts.md)'

This path '../../../user/keyboard-shortcuts.md' would resolve to 'docs/user/keyboard-shortcuts.md' which is not in the provided documentation structure. The correct path is likely different or the file doesn't exist.

---

#### documentation_inconsistency

**Description:** Renumber feature has inconsistent shortcut documentation

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
feature-reference.md states Renumber uses 'Ctrl+E', but quick-reference.md states it is 'Menu only' with no keyboard shortcut listed.

---

#### documentation_inconsistency

**Description:** Inconsistent feature count claims

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/tk/feature-reference.md`

**Details:**
Curses feature-reference.md claims '7 features' for File Operations but only lists 6 features (New, Open, Save, Save As, Recent Files, Auto-Save, Merge Files = 7, correct). Tk feature-reference.md claims '8 features' for File Operations and lists 8 (New, Open, Save, Save As, Recent Files, Auto-Save, Delete Lines, Merge Files). Delete Lines appears in Tk but not in Curses File Operations section.

---

#### documentation_inconsistency

**Description:** Variable sorting modes inconsistency

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
variables.md states sort modes are 'Accessed → Written → Read → Name', but feature-reference.md describes them as:
- Accessed: Most recently accessed (read or written) - newest first
- Written: Most recently written to - newest first
- Read: Most recently read from - newest first
- Name: Alphabetically by variable name
Both agree on the modes but variables.md doesn't explain what each mode means.

---

#### documentation_inconsistency

**Description:** Variable window filter options inconsistency

**Affected files:**
- `docs/help/ui/curses/quick-reference.md`
- `docs/help/ui/curses/variables.md`

**Details:**
quick-reference.md states filter cycles through 'All → Scalars → Arrays → Modified', but variables.md only mentions 'All', 'Scalars', 'Arrays', 'Modified' without specifying the cycle order or if they match.

---

#### documentation_inconsistency

**Description:** Clear All Breakpoints shortcut inconsistency between UIs

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/tk/feature-reference.md`

**Details:**
Curses feature-reference.md shows '{{kbd:save:curses}}hift+B' (likely Shift+B with typo), while Tk feature-reference.md shows '{{kbd:file_save:tk}}hift+B' (likely Shift+B with typo). Both appear to have the same typo pattern but use different kbd template variables.

---

#### documentation_inconsistency

**Description:** Cut/Copy/Paste explanation has circular reference

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
Feature-reference.md states: '{{kbd:save:curses}} - Used for Save File (cannot be used for Paste; {{kbd:save:curses}} is reserved by terminal for flow control)' - this mentions {{kbd:save:curses}} twice with conflicting purposes (Save File vs terminal flow control).

---

#### documentation_inconsistency

**Description:** Delete Lines operation inconsistency

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
quick-reference.md states 'Delete/Backspace - Delete current line' under Editing section, but feature-reference.md lists 'Delete Lines (Ctrl+D)' as a separate feature. Unclear if these are the same feature or different operations.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation between Tk and Web UI docs

**Affected files:**
- `docs/help/ui/tk/features.md`
- `docs/help/ui/web/features.md`

**Details:**
Tk features.md uses notation like {{kbd:smart_insert}}, {{kbd:toggle_breakpoint}}, {{kbd:find:tk}}, {{kbd:replace:tk}} without the :tk suffix in most places, but then uses :tk suffix for find/replace. Web features.md consistently uses {{kbd:run:web}}, {{kbd:continue:web}}, {{kbd:step:web}}, {{kbd:find:web}}, {{kbd:replace:web}} with the :web suffix. The Tk docs should be consistent - either always use :tk suffix or never use it.

---

#### documentation_inconsistency

**Description:** Different keyboard shortcuts documented for same operations across UIs

**Affected files:**
- `docs/help/ui/tk/features.md`
- `docs/help/ui/web/debugging.md`

**Details:**
Tk features.md documents:
- {{kbd:step_statement}} - Execute next statement
- {{kbd:step_line}} - Execute next line
- {{kbd:continue_execution}} - Continue to next breakpoint

Web debugging.md documents:
- {{kbd:step:web}} - Step statement
- Ctrl+K - Step line
- {{kbd:continue:web}} - Continue

The naming is inconsistent (step_statement vs step, continue_execution vs continue) and it's unclear if these are meant to be the same operations with different shortcuts per UI, or if the documentation is using inconsistent terminology.

---

#### documentation_inconsistency

**Description:** Contradictory information about function key shortcuts in Web UI

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/debugging.md`

**Details:**
debugging.md states: 'Note: Function key shortcuts ({{kbd:continue:web}}, {{kbd:step:web}}, {{kbd:help:web}}1, etc.) are not implemented in the Web UI.'

However, features.md lists under 'Execution Control - Currently Implemented':
- Run ({{kbd:run:web}})
- Continue ({{kbd:continue:web}})
- Step statement ({{kbd:step:web}})
- Stop ({{kbd:stop:web}})

This is contradictory - either these shortcuts work or they don't.

---

#### documentation_inconsistency

**Description:** Contradictory information about settings storage implementation

**Affected files:**
- `docs/help/ui/tk/settings.md`
- `docs/help/ui/web/features.md`

**Details:**
tk/settings.md states at the end: 'Note: Settings storage is implemented, but the settings dialog itself is not yet available in the Tk UI.'

However, the entire document is marked as 'Implementation Status: ... The features described in this document represent planned/intended implementation and are not yet available.'

This is contradictory - if settings storage is implemented, that should be clearly separated from the planned dialog features.

---

#### documentation_inconsistency

**Description:** Inconsistent implementation status for breakpoint features

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/debugging.md`

**Details:**
features.md under 'Breakpoints - Currently Implemented' states:
- Line breakpoints (toggle via Run menu)
- Clear all breakpoints
- Visual indicators in editor

debugging.md under 'Setting Breakpoints - Currently Implemented' states:
1. Use Run → Toggle Breakpoint menu option
2. Enter the line number when prompted

But then debugging.md also says: 'Note: Advanced features like clicking line numbers to set breakpoints and a dedicated breakpoint panel are planned for future releases but not yet implemented.'

This suggests clicking line numbers doesn't work, but features.md doesn't mention this limitation.

---

#### documentation_inconsistency

**Description:** Inconsistent information about auto-save functionality for programs

**Affected files:**
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/settings.md`

**Details:**
getting-started.md states: "Auto-save of programs to browser localStorage is planned for a future release" (appears twice)

But settings.md describes auto-save as already implemented: "Settings ARE saved to localStorage" and provides detailed documentation about localStorage storage being the default method.

The distinction between program auto-save vs settings auto-save is unclear and potentially confusing to users.

---

#### documentation_inconsistency

**Description:** Missing 'Open Example' feature documentation inconsistency

**Affected files:**
- `docs/help/ui/web/web-interface.md`
- `docs/help/ui/web/index.md`

**Details:**
web-interface.md states: "Note: An 'Open Example' feature to choose from sample BASIC programs is planned for a future release."

However, index.md states: "Example programs - Load samples to learn" and "Load Examples - File → Load Example to see sample programs" suggesting the feature already exists.

This creates confusion about whether the feature is implemented or planned.

---

#### documentation_inconsistency

**Description:** Contradictory information about settings persistence in Redis mode

**Affected files:**
- `docs/help/ui/web/settings.md`

**Details:**
settings.md states about Redis storage: "Settings persist across browser tabs" and "Shared state in multi-instance deployments"

But then states: "Settings are session-based (cleared when session expires)"

This creates confusion - do settings persist or are they session-based? The document suggests both persistence and session-based clearing, which are contradictory concepts.

---

#### documentation_inconsistency

**Description:** Conflicting information about Calendar program location

**Affected files:**
- `docs/library/index.md`
- `docs/library/utilities/index.md`

**Details:**
docs/library/index.md lists 'Calendar' under Utilities featured programs: 'Featured programs: Calendar, Unit Converter, Sort, Search, Day of Week Calculator'

However, docs/library/utilities/index.md for the Calendar entry states: 'Note: A different calendar program is also available in the [Games Library](../games/index.md#calendar)'

This suggests there are TWO calendar programs - one in Utilities and one in Games. But the main index.md only mentions Calendar under Utilities, not Games. The Games section featured programs list is: 'Blackjack, Spacewar, Star Trek, Hangman, Roulette' - no Calendar mentioned.

---

#### documentation_inconsistency

**Description:** Missing cross-reference to case handling in quick reference

**Affected files:**
- `docs/user/CASE_HANDLING_GUIDE.md`
- `docs/user/QUICK_REFERENCE.md`

**Details:**
The CASE_HANDLING_GUIDE.md is a comprehensive 500+ line guide about an important feature (case handling for variables and keywords).

However, QUICK_REFERENCE.md makes no mention of:
- Case handling settings
- SET command for configuring case behavior
- SHOW SETTINGS command
- The existence of case conflict detection

The quick reference should at least mention these features exist and point to the detailed guide, as case handling affects how code appears in the editor.

---

#### documentation_inconsistency

**Description:** README.md lists CASE_HANDLING_GUIDE.md as a configuration document, but this file is not referenced or described in SETTINGS_AND_CONFIGURATION.md

**Affected files:**
- `docs/user/README.md`
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
README.md shows:
- **[CASE_HANDLING_GUIDE.md](CASE_HANDLING_GUIDE.md)** - Variable and keyword case handling

But SETTINGS_AND_CONFIGURATION.md only covers variables.case_conflict setting and mentions 'See docs/dev/KEYWORD_CASE_HANDLING_TODO.md for details on upcoming features' without referencing CASE_HANDLING_GUIDE.md

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation between documents

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
SETTINGS_AND_CONFIGURATION.md uses:
'({{kbd:toggle_variables}} in TK UI)'

TK_UI_QUICK_START.md uses:
'**{{kbd:run_program}}**' and '**{{kbd:file_save}}**'

Inconsistent use of bold formatting and parentheses for kbd placeholders

---

#### documentation_inconsistency

**Description:** Inconsistent boolean value notation in SET command examples

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
SETTINGS_AND_CONFIGURATION.md shows:
'SET "editor.auto_number" true'
and
'SET "editor.show_line_numbers" true'

But also states:
'- Booleans: `true` or `false` (lowercase, no quotes in commands; use true/false in JSON files)'

The phrase 'use true/false in JSON files' is confusing since it's already stated they should be lowercase without quotes in commands

---

#### documentation_inconsistency

**Description:** Conflicting information about Find/Replace availability in Web UI

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
The Feature Availability Matrix shows:
| **Find/Replace** | ❌ | ❌ | ✅ | ⚠️ | Tk: implemented, Web: planned |

But the Recently Added section states:
'### Recently Added (2025-10-29)
- ✅ Tk: Find/Replace functionality'

And Coming Soon section states:
'### Coming Soon
- ⏳ Find/Replace in Web UI'

The date '2025-10-29' appears to be in the future (assuming current date is before that), which is inconsistent

---

#### documentation_inconsistency

**Description:** Keyboard shortcuts table references shortcuts that may not exist

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
The Common Shortcuts table shows:
| **Run** | {{kbd:run:cli}} | {{kbd:run:curses}} | {{kbd:run_program:tk}} | {{kbd:run:web}} |

But keyboard-shortcuts.md (Curses UI) shows the actual shortcut is '^R' not a placeholder. The table uses placeholder notation that suggests these will be replaced, but it's unclear if this is correct or if actual key combinations should be shown

---

### 🟢 Low Severity

#### code_vs_comment_conflict

**Description:** Comment claims keyword_token fields are not used, but they exist in multiple statement nodes

**Affected files:**
- `src/ast_nodes.py`

**Details:**
PrintStatementNode line 237: 'keyword_token: Optional[Token] = None  # Token for PRINT keyword (legacy, not currently used)'

IfStatementNode lines 295-297:
'keyword_token: Optional[Token] = None  # Token for IF keyword
then_token: Optional[Token] = None     # Token for THEN keyword
else_token: Optional[Token] = None     # Token for ELSE keyword (if present)'

ForStatementNode lines 311-313:
'keyword_token: Optional[Token] = None  # Token for FOR keyword
to_token: Optional[Token] = None       # Token for TO keyword
step_token: Optional[Token] = None     # Token for STEP keyword (if present)'

The PrintStatementNode comment says these fields are 'legacy, not currently used' and explains they were 'intended for case-preserving keyword regeneration but are not currently used by position_serializer'. However, IfStatementNode and ForStatementNode have similar fields without the 'legacy' or 'not used' disclaimer, creating inconsistency about whether these fields are actually used.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation of INPUT statement semicolon behavior

**Affected files:**
- `src/ast_nodes.py`

**Details:**
InputStatementNode docstring lines 260-271:
'Note: The suppress_question field controls "?" display:
- suppress_question=False (default): Adds "?" after prompt
  Examples: INPUT var → "? ", INPUT "Name", var → "Name? "
- suppress_question=True: No "?" added (but custom prompt string still displays if present)
  Examples: INPUT; var → "" (no prompt), INPUT "Name"; var → "Name" (prompt without "?")

Semicolon position determines suppress_question value:
- INPUT "prompt"; var → semicolon after prompt is just separator (suppress_question=False, shows "?")
- INPUT; var → semicolon immediately after INPUT (suppress_question=True, no "?")'

The explanation is confusing: it says 'INPUT "prompt"; var' has 'suppress_question=False' and 'shows "?"', but earlier it says 'INPUT "Name"; var → "Name" (prompt without "?")'. These statements contradict each other about whether INPUT "prompt"; var shows the question mark.

---

#### code_vs_comment_conflict

**Description:** CallStatementNode has unused arguments field with conflicting documentation

**Affected files:**
- `src/ast_nodes.py`

**Details:**
CallStatementNode docstring lines 826-841:
'Implementation Note: The \'arguments\' field is currently unused (always empty list). It exists for potential future support of BASIC dialects that allow CALL with arguments (e.g., CALL ROUTINE(args)). Standard MBASIC 5.21 only accepts a single address expression in the \'target\' field. Code traversing the AST can safely ignore the \'arguments\' field for MBASIC 5.21 programs.'

CallStatementNode definition lines 842-845:
'target: \'ExpressionNode\'  # Memory address expression
arguments: List[\'ExpressionNode\']  # Reserved for future (parser always sets to empty list)'

The field exists but is documented as always empty and unused. This creates maintenance burden and potential confusion. The comment says 'parser always sets to empty list' but doesn't explain why the field exists at all if it's never used.

---

#### documentation_inconsistency

**Description:** ChainStatementNode delete_range type annotation inconsistency

**Affected files:**
- `src/ast_nodes.py`

**Details:**
ChainStatementNode definition line 545:
'delete_range: Optional[Tuple[int, int]] = None  # (start_line_number, end_line_number) for DELETE option - tuple of int line numbers'

The comment redundantly specifies 'tuple of int line numbers' when the type annotation 'Tuple[int, int]' already makes this clear. More importantly, the comment format '(start_line_number, end_line_number)' uses underscores while other similar comments use spaces (e.g., 'line_number' vs 'line number'), creating minor inconsistency in documentation style.

---

#### code_vs_comment_conflict

**Description:** VariableNode type_suffix documentation is verbose and potentially confusing

**Affected files:**
- `src/ast_nodes.py`

**Details:**
VariableNode docstring lines 1027-1038:
'Type suffix handling:
- type_suffix: The actual suffix character ($, %, !, #) - always set to indicate variable type
- explicit_type_suffix: Boolean indicating the origin of type_suffix:
    * True: suffix appeared in source code (e.g., "X%" in "X% = 5")
    * False: suffix inferred from DEFINT/DEFSNG/DEFDBL/DEFSTR (e.g., "X" with DEFINT A-Z)

Example: In "DEFINT A-Z: X=5", variable X has type_suffix=\'%\' and explicit_type_suffix=False.
The suffix must be tracked for type checking but not regenerated in source code.
Both fields must always be examined together to correctly handle variable typing.'

VariableNode definition lines 1040-1044:
'name: str  # Normalized lowercase name for lookups
type_suffix: Optional[str] = None  # $, %, !, # - The actual suffix (see explicit_type_suffix for origin)
subscripts: Optional[List[\'ExpressionNode\']] = None  # For array access
original_case: Optional[str] = None  # Original case as typed by user (for display)
explicit_type_suffix: bool = False  # True if type_suffix was in original source, False if inferred from DEF'

The docstring says 'type_suffix... always set to indicate variable type' but the field definition has 'Optional[str] = None', meaning it can be None. This is contradictory.

---

#### documentation_inconsistency

**Description:** Inconsistent comment style for statement nodes with keyword tokens

**Affected files:**
- `src/ast_nodes.py`

**Details:**
PrintStatementNode line 237: 'keyword_token: Optional[Token] = None  # Token for PRINT keyword (legacy, not currently used)'

IfStatementNode lines 295-297:
'keyword_token: Optional[Token] = None  # Token for IF keyword
then_token: Optional[Token] = None     # Token for THEN keyword
else_token: Optional[Token] = None     # Token for ELSE keyword (if present)'

ForStatementNode lines 311-313:
'keyword_token: Optional[Token] = None  # Token for FOR keyword
to_token: Optional[Token] = None       # Token for TO keyword
step_token: Optional[Token] = None     # Token for STEP keyword (if present)'

PrintStatementNode includes detailed explanation about legacy status and position_serializer, while IfStatementNode and ForStatementNode have minimal comments. This inconsistency makes it unclear whether the keyword_token fields in IF and FOR statements are also legacy/unused.

---

#### code_vs_comment

**Description:** Comment says identifier_table exists but is not used for identifiers

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line ~100 in case_string_handler.py: Comment states "An identifier_table infrastructure exists (see get_identifier_table) but is not currently used for identifiers". This suggests dead code or incomplete implementation. The get_identifier_table() method exists but serves no purpose if identifiers always return original_text.

---

#### documentation_inconsistency

**Description:** Module docstring references tokens.py for MBASIC 5.21 specification but tokens.py is not included in provided files

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line 6: "See tokens.py for complete MBASIC 5.21 specification reference." - tokens.py is not in the provided source files, making this reference unverifiable.

---

#### code_vs_comment

**Description:** Comment about leading sign not adding to digit_count contradicts implementation

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line ~172: Comment says "Note: leading sign doesn't add to digit_count, it's a format modifier" but at line ~313 the code adds 1 to field_width for leading_sign: "if spec['leading_sign'] or spec['trailing_sign'] or spec['trailing_minus_only']: field_width += 1". This suggests leading sign DOES consume a position in the field width calculation.

---

#### code_vs_comment

**Description:** Comment says identifiers preserve original case but implementation returns original_text without using table

**Affected files:**
- `src/case_string_handler.py`

**Details:**
Lines ~47-55: Long comment explains that identifiers preserve original case and mentions identifier_table exists but is not used. The code then returns original_text directly. This suggests the identifier_table infrastructure (get_identifier_table method) is dead code that should be removed or the comment should explain why it exists.

---

#### documentation_inconsistency

**Description:** INPUT() docstring shows conflicting syntax examples

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line ~710: Docstring shows "INPUT$(n, #filenum)" in BASIC syntax but then says "INPUT(n, filenum)" in Python call syntax and "Note: The # prefix in BASIC syntax is stripped by the parser". This is confusing because it suggests # is part of BASIC syntax but then says it's stripped. Should clarify that # is a BASIC file number prefix, not part of INPUT$ syntax itself.

---

#### Documentation inconsistency

**Description:** Inconsistent terminology for filesystem abstraction purposes

**Affected files:**
- `src/file_io.py`
- `src/filesystem/base.py`

**Details:**
src/file_io.py states:
"1. FileIO (this file) - Program management operations
   - Purpose: Load .BAS programs into memory, save from memory to storage"

src/filesystem/base.py states:
"1. FileIO (src/file_io.py) - Program management operations
   - Purpose: Load .BAS programs into memory, save from memory to disk"

One says 'storage', the other says 'disk'. While semantically similar, the inconsistency could confuse readers, especially since the web UI uses memory-based storage, not disk.

---

#### Code vs Documentation inconsistency

**Description:** Documentation mentions duplicate two-letter codes but doesn't list which codes are duplicated

**Affected files:**
- `src/error_codes.py`

**Details:**
The module docstring states:
"Note: Some two-letter codes are duplicated (e.g., DD, CN, DF) across different
numeric error codes. This matches the original MBASIC 5.21 specification where
the two-letter codes alone are ambiguous - the numeric code is authoritative."

Looking at ERROR_CODES dictionary:
- DD appears at codes 10 and 68
- CN appears at codes 17 and 69
- DF appears at codes 25 and 61

The documentation correctly identifies the duplicate codes. However, it says '(e.g., DD, CN, DF)' which implies there might be more duplicates. A complete list or clarification that these are the only duplicates would be helpful.

---

#### Documentation inconsistency

**Description:** Module docstring has redundant explanation about ProgramManager file I/O methods

**Affected files:**
- `src/editing/manager.py`

**Details:**
The module docstring contains a long section titled 'Why ProgramManager has its own file I/O methods:' that explains the separation between ProgramManager's direct file I/O and the FileIO abstraction. However, this explanation is somewhat redundant with the earlier 'FILE I/O ARCHITECTURE:' section which already explains the separation. The two sections could be consolidated for clarity.

---

#### Code vs Documentation inconsistency

**Description:** RealFileSystemProvider.__init__ docstring mentions base_path restriction but implementation allows None for unrestricted access

**Affected files:**
- `src/filesystem/real_fs.py`

**Details:**
The __init__ docstring states:
"Args:
    base_path: Optional base directory to restrict access.
              If None, allows access to entire filesystem."

The implementation correctly handles both cases:
- When base_path is set, _resolve_path() restricts access
- When base_path is None, _resolve_path() returns filename as-is

This is consistent. However, the security implications of allowing None (unrestricted filesystem access) could be more prominently documented, especially since this is used by local UIs where users have legitimate filesystem access.

---

#### documentation_inconsistency

**Description:** Help text mentions 'Ctrl+H (UI help)' but this is UI-specific and may not be available in all contexts

**Affected files:**
- `src/immediate_executor.py`

**Details:**
In _show_help() method:
'Press Ctrl+H (UI help) for keyboard shortcuts and UI features.'

This assumes a specific UI implementation with Ctrl+H bound to help, but ImmediateExecutor is designed to be UI-agnostic. The help text should either be generic or note that this is specific to certain UIs.

---

#### code_vs_comment

**Description:** Comment about INPUT statement behavior is split between two locations with slightly different wording

**Affected files:**
- `src/immediate_executor.py`

**Details:**
In execute() method docstring (line ~80):
'Examples:
>>> executor.execute("PRINT 2 + 2")
(True, " 4\\n")'

But in help text LIMITATIONS section:
'• INPUT statement will fail at runtime in immediate mode (use direct assignment instead)'

And in OutputCapturingIOHandler.input() method:
'"""Input not supported in immediate mode.

Note: INPUT statements are parsed and executed normally, but fail
at runtime when the interpreter calls this input() method."""'

The wording is inconsistent - 'will fail at runtime' vs 'not supported' vs 'not allowed'. All mean the same thing but should use consistent terminology.

---

#### documentation_inconsistency

**Description:** Module docstring mentions Python version requirement but doesn't specify minimum version consistently

**Affected files:**
- `src/input_sanitizer.py`

**Details:**
Module docstring states:
'Implementation note: Uses standard Python type hints (e.g., tuple[str, bool])
which require Python 3.9+. For earlier Python versions, use Tuple[str, bool] from typing.'

This is informational but doesn't indicate whether the code actually supports Python <3.9 or if it's a hard requirement. The code uses tuple[str, bool] syntax, which means it REQUIRES Python 3.9+, but the note suggests there's a workaround for earlier versions (which isn't implemented).

---

#### code_vs_comment

**Description:** Docstring example shows escaped backslash in output but actual output would have single backslash

**Affected files:**
- `src/immediate_executor.py`

**Details:**
In execute() method docstring:
'Examples:
>>> executor.execute("PRINT 2 + 2")
(True, " 4\\n")'

The double backslash (\\n) is correct for showing the literal string representation in Python docstring, but might be confusing. The actual return value would be the string ' 4\n' (with actual newline character), and repr() would show it as ' 4\\n'. This is technically correct but could be clearer.

---

#### code_vs_comment

**Description:** Comment says 'bare except' but code uses specific exception handling

**Affected files:**
- `src/interactive.py`

**Details:**
At line ~800, comment states: '# Fallback for non-TTY/piped input or any terminal errors (bare except)'

But the code uses 'except:' which is indeed a bare except. However, the comment's phrasing suggests this might be unintentional or a code smell that should be documented as intentional. The comment acknowledges it but doesn't explain why bare except is acceptable here.

---

#### code_vs_comment

**Description:** Comment about readline Ctrl+A binding may be misleading

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at lines ~90-95 states: 'Bind Ctrl+A to insert the character instead of moving cursor to beginning-of-line. This overrides default Ctrl+A (beginning-of-line) behavior. When user presses Ctrl+A, the terminal sends ASCII 0x01, and 'self-insert' tells readline to insert it as-is instead of interpreting it as a command.'

However, this conflicts with the typical readline behavior where 'self-insert' would insert a visible character. The code at line ~135 checks for '\x01' (Ctrl+A) to trigger edit mode, which suggests Ctrl+A should NOT be inserted as a character but should be intercepted. The readline binding may not work as described since the input() call would receive the character before the start() method can check for it.

---

#### documentation_inconsistency

**Description:** Module docstring lists commands that are not directly handled in execute_command()

**Affected files:**
- `src/interactive.py`

**Details:**
Module docstring at line ~7 lists: 'Direct commands (RUN, LIST, SAVE, LOAD, NEW, MERGE, FILES, SYSTEM, DELETE, RENUM, AUTO, EDIT, etc.)'

However, execute_command() at line ~220 only directly handles AUTO, EDIT, and HELP. The comment at line ~227 states: 'Everything else (including LIST, DELETE, RENUM, FILES, RUN, LOAD, SAVE, MERGE, SYSTEM, NEW, PRINT, etc.) goes through the real parser as immediate mode statements'

This means commands like RUN, LIST, SAVE, LOAD, NEW, MERGE, FILES, SYSTEM, DELETE, RENUM are NOT handled as 'direct commands' but as parsed immediate mode statements. The module docstring is misleading about the architecture.

---

#### code_vs_comment

**Description:** Comment says 'Note: program_runtime object persists' but clear_execution_state() doesn't verify this

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~440 in cmd_new() states: 'Note: program_runtime object persists, only its stacks are cleared'

However, clear_execution_state() at line ~185 only operates on self.program_runtime if it exists, and cmd_new() doesn't ensure program_runtime persists. If program_runtime is None, clear_execution_state() does nothing. The comment implies program_runtime always exists after NEW, but the code doesn't guarantee this.

---

#### code_vs_comment_conflict

**Description:** Comment about empty line_text_map is overly detailed and potentially misleading

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~220 states: 'Pass empty line_text_map since immediate mode uses temporary line 0\n(no source line text available for error reporting, but this is fine\nfor immediate mode where the user just typed the statement)'. However, the statement WAS just typed and IS available in the 'statement' parameter. The comment implies source text is unavailable when it actually is available, just not being passed.

---

#### documentation_inconsistency

**Description:** cmd_help docstring says 'HELP - Show help information about commands' but implementation shows 'Debugging Commands' which is narrower scope

**Affected files:**
- `src/interactive.py`

**Details:**
Docstring: 'HELP - Show help information about commands'
Implementation prints: 'MBASIC-2025 Debugging Commands:'
The help output focuses on debugging commands but also includes general commands like LOAD, SAVE, NEW, etc. The title is misleading.

---

#### code_vs_comment_conflict

**Description:** Comment about Runtime initialization mentions 'no source line text available' but doesn't explain why this is acceptable

**Affected files:**
- `src/interactive.py`

**Details:**
Comment says 'no source line text available for error reporting, but this is fine\nfor immediate mode where the user just typed the statement'. The justification is weak - if the user just typed it, we DO have the text (in 'statement' variable) and could pass it. The comment doesn't explain why we choose not to.

---

#### code_vs_comment

**Description:** Comment says 'clears itself to False' but code shows it's cleared by the else branch, not by itself

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line 64-65 says:
"then clears itself to False. Prevents re-halting on same breakpoint."

But code at lines 454-455 shows:
else:
    self.state.skip_next_breakpoint_check = False

The flag doesn't clear 'itself' - it's explicitly cleared by the else branch when the breakpoint is skipped.

---

#### documentation_inconsistency

**Description:** InterpreterState docstring lists execution order but doesn't mention error_info can be set during statement execution (step 6), only in error handling (step 7)

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring at lines 44-52 lists:
"Internal execution order in tick_pc() (for developers understanding control flow):
1. pause_requested check - pauses if pause() was called
2. halted check - stops if already halted
3. break_requested check - handles Ctrl+C breaks
4. breakpoints check - pauses at breakpoints
5. trace output - displays [line] or [line.stmt] if TRON is active
6. statement execution - where input_prompt may be set
7. error handling - where error_info is set via exception handlers"

But code at lines 476-490 shows error_info is set DURING statement execution (step 6) in the except block, before invoking the error handler. The docstring implies it's only set in step 7 (error handling).

---

#### code_vs_comment

**Description:** Comment says NEXT I, J, K differs from separate statements, but the described behavior is actually the same for loop completion

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at lines 1113-1119 says:
"NEXT I, J, K processes variables left-to-right: I first, then J, then K.
For each variable, _execute_next_single() is called to increment it and check if
the loop should continue. If _execute_next_single() returns True (loop continues),
execution jumps back to the FOR body and remaining variables are not processed.
If it returns False (loop finished), that loop is popped and the next variable is processed.

This differs from separate statements (NEXT I: NEXT J: NEXT K) which would
always execute sequentially, processing all three NEXT statements."

The claim about 'differs from separate statements' is misleading. If NEXT I loops back, control returns to FOR I body, so NEXT J and NEXT K wouldn't execute anyway (they're after NEXT I). The behavior is the same whether combined or separate, except for the case where I's loop completes - then J is processed immediately in combined form, vs requiring another iteration in separate form.

---

#### code_vs_comment

**Description:** Comment about WEND timing is verbose and potentially confusing about when pop occurs

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1050 states:
"# Pop the loop from the stack (after setting npc above, before WHILE re-executes).
# Timing: We pop NOW so the stack is clean before WHILE condition re-evaluation.
# The WHILE will re-push if its condition is still true, or skip the loop body
# if false. This ensures clean stack state and proper error handling if the
# WHILE condition evaluation fails (loop already popped, won't corrupt stack)."

The code pops AFTER setting npc, which is correct. However, the comment's emphasis on "before WHILE re-executes" could be misread as "before the jump" when it actually means "before the WHILE statement executes on the next tick". The comment is technically correct but could be clearer.

---

#### code_vs_comment

**Description:** Comment about RUN behavior describes halted flag inconsistently

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1470 states:
"# Note: RUN without args sets halted=True to stop current execution.
# The caller (e.g., UI tick loop) should detect halted=True and restart
# execution from the beginning if desired. This is different from
# RUN line_number which sets halted=False to continue execution inline."

The code shows:
if stmt.target:
    # RUN line_number path
    self.runtime.npc = PC.from_line(line_num)
    self.runtime.halted = False
else:
    # RUN without args path
    self.runtime.clear_variables()
    self.runtime.halted = True

The comment is accurate, but it's unusual that RUN without args sets halted=True (stopping execution) while RUN line_number sets halted=False (continuing execution). This asymmetry should be explained more clearly in the comment - why does RUN without args halt instead of jumping to the first line?

---

#### code_vs_comment

**Description:** Comment about INPUT state machine mentions input_file_number but doesn't explain its purpose clearly

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1640 states:
"# Set input prompt - execution will pause
# Sets: input_prompt (prompt text), input_variables (var list),
#       input_file_number (None for keyboard input, file # for file input)"

The code sets:
self.state.input_file_number = None  # None indicates keyboard input (not file)

However, the comment doesn't explain WHY input_file_number is needed when file input is synchronous (as stated in the docstring: "File input bypasses the state machine and reads synchronously"). If file input is synchronous, why store input_file_number at all? This suggests either the comment is outdated or there's a use case not explained.

---

#### code_vs_comment

**Description:** Comment about string length limit mentions len() counts characters and discusses encoding, but doesn't clarify behavior for multi-byte characters

**Affected files:**
- `src/interpreter.py`

**Details:**
In evaluate_binaryop(), the comment states:
"Also note: len() counts characters. For ASCII and latin-1 (both single-byte encodings),
character count equals byte count. Field buffers (LSET/RSET) use latin-1 encoding."

This comment is technically correct but potentially misleading. Python's len() on strings always counts Unicode code points (characters), not bytes. The comment seems to imply this is specific to ASCII/latin-1, but it's true for all Python strings. The relevant point is that field buffers use latin-1 encoding when converting to bytes, which means each character becomes one byte. The comment could be clearer about this distinction.

---

#### code_vs_comment

**Description:** Comment about LSET/RSET fallback behavior claims it's for compatibility but may be misleading

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_lset() and execute_rset(), the comments state:
"Compatibility note: In strict MBASIC 5.21, LSET/RSET are only for field
variables (used with FIELD statement for random file access). This fallback
is a deliberate extension for compatibility with code that uses LSET for
general string formatting. This is documented behavior, not a bug."

The comment says the fallback is for "compatibility with code that uses LSET for general string formatting" but then also says "In strict MBASIC 5.21, LSET/RSET are only for field variables." This is contradictory - if MBASIC 5.21 doesn't support LSET for general strings, then supporting it isn't "compatibility" with MBASIC 5.21, it's an extension beyond MBASIC 5.21. The comment should clarify this is compatibility with other BASIC dialects or user expectations, not MBASIC 5.21.

---

#### code_vs_comment

**Description:** Comment about debugger_set parameter usage is inconsistent with actual parameter name

**Affected files:**
- `src/interpreter.py`

**Details:**
In evaluate_functioncall(), the comment says:
"Note: get_variable_for_debugger() and debugger_set=True are used to avoid
triggering variable access tracking."

But the actual code uses:
```
self.runtime.set_variable(base_name, type_suffix, saved_value, debugger_set=True)
```

The comment correctly describes the parameter name (debugger_set=True), so this is actually consistent. However, the comment could be clearer about why this specific mechanism exists and what would happen if debugger_set=False was used instead.

---

#### Documentation inconsistency

**Description:** Module docstring states WebIOHandler is not exported due to nicegui dependency, but web_io.py imports nicegui at module level, making it fail on import if nicegui is not installed

**Affected files:**
- `src/iohandler/__init__.py`
- `src/iohandler/web_io.py`

**Details:**
__init__.py says: "WebIOHandler are not exported here because they have dependencies on their respective UI frameworks (tkinter, nicegui). They should be imported directly from their modules when needed"

But web_io.py has: "from nicegui import ui" at the top level, which will fail immediately on import if nicegui is not installed, defeating the purpose of not exporting it.

---

#### Code vs Comment conflict

**Description:** Backward compatibility comment for print() method says it was renamed to avoid conflicts with Python's built-in, but output() is the standard IOHandler method name

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Comment says: "This method was renamed from print() to output() to avoid conflicts with Python's built-in print function."

However, output() is the standard method name defined in IOHandler base class (base.py). The comment implies print() was the original name, but base.py has always defined output() as the interface method. The comment is misleading about the reason for the naming.

---

#### Code vs Comment conflict

**Description:** get_char() backward compatibility comment claims it preserves non-blocking behavior, but always calls input_char(blocking=False) which is ignored anyway

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Comment says: "Note: Always calls input_char(blocking=False) for non-blocking behavior. The original get_char() implementation was non-blocking, so this preserves that behavior for backward compatibility."

But input_char() in web_io.py ignores the blocking parameter entirely and always returns "" immediately. The comment suggests the blocking parameter matters, but it doesn't in this implementation.

---

#### Documentation inconsistency

**Description:** get_screen_size() method exists in web_io.py but is not part of IOHandler base interface, creating API inconsistency

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
web_io.py has get_screen_size() method with note: "Note: This is a web_io-specific method, not part of the IOHandler base interface. Other implementations (console, curses, gui) do not provide this method."

This creates an inconsistent API where code using WebIOHandler can call get_screen_size() but code using other IOHandler implementations cannot. This violates the abstraction principle of the IOHandler interface.

---

#### Documentation inconsistency

**Description:** Module docstring references SimpleKeywordCase in src/simple_keyword_case.py but this file is not provided in the source code listing

**Affected files:**
- `src/keyword_case_manager.py`

**Details:**
Docstring says: "For simpler force-based policies in the lexer, see SimpleKeywordCase (src/simple_keyword_case.py) which only supports force_lower, force_upper, and force_capitalize."

The file src/simple_keyword_case.py is not included in the provided source code files, making this reference unverifiable and potentially incorrect.

---

#### Code vs Documentation inconsistency

**Description:** ConsoleIOHandler.input_char() non-blocking mode uses select on Unix but warns about msvcrt unavailability on Windows, creating asymmetric error handling

**Affected files:**
- `src/iohandler/console.py`

**Details:**
Unix path: "if select.select([sys.stdin], [], [], 0.0)[0]: return sys.stdin.read(1) else: return """

Windows path: "except ImportError: import warnings; warnings.warn("msvcrt not available on Windows - non-blocking input_char() not supported", RuntimeWarning); return """

The Unix implementation silently returns "" when no input is available (expected behavior), but Windows warns when msvcrt is unavailable even though it also returns "" (same result). This creates inconsistent user experience across platforms.

---

#### Code vs Comment conflict

**Description:** Comment in read_identifier() claims 'Old BASIC with NEXTI instead of NEXT I should be preprocessed' but no preprocessing mechanism is shown or referenced

**Affected files:**
- `src/lexer.py`

**Details:**
Comment states:
"This lexer parses properly-formed MBASIC 5.21 which generally requires spaces
between keywords and identifiers. Exception: PRINT# and INPUT# where # is part
of the keyword. Old BASIC with NEXTI instead of NEXT I should be preprocessed."

And later:
"NOTE: We do NOT handle old BASIC where keywords run together (NEXTI, FORI).
This is properly-formed MBASIC 5.21 which requires spaces.
Exception: PRINT# and similar file I/O keywords (handled above) support # without space.
Other old BASIC syntax should be preprocessed with conversion scripts."

No preprocessing scripts or mechanisms are referenced elsewhere in the code, making this claim unverifiable.

---

#### Documentation inconsistency

**Description:** Module docstring claims 'Extended BASIC features' are always enabled with no option to disable, but no configuration or toggle mechanism is shown anywhere

**Affected files:**
- `src/lexer.py`

**Details:**
Module docstring states:
"MBASIC 5.21 Extended BASIC features: This implementation always enables Extended BASIC
features (e.g., periods in identifiers like 'RECORD.FIELD') as they are part of MBASIC 5.21.
There is no option to disable them."

This statement about 'no option to disable' is unnecessary if there's no configuration system shown. It implies there might have been or could be such an option, creating confusion.

---

#### Code vs Comment conflict

**Description:** Comment in tokenize() method mentions 'CP/M BASIC' but module docstring specifies 'MBASIC 5.21 (CP/M era MBASIC-80)' - inconsistent terminology

**Affected files:**
- `src/lexer.py`

**Details:**
Module docstring: "Lexer for MBASIC 5.21 (CP/M era MBASIC-80)"

Comment in tokenize(): "# In CP/M BASIC, \r (carriage return) can be used as statement separator"

While these refer to the same thing, the terminology is inconsistent. Should use 'MBASIC 5.21' or 'MBASIC-80' consistently.

---

#### Code internal inconsistency

**Description:** Inconsistent handling of original case: identifiers use 'original_case' field, keywords use 'original_case_keyword' field, but this distinction is only explained in one comment

**Affected files:**
- `src/lexer.py`

**Details:**
In read_identifier() for identifiers:
"token.original_case = ident"

In read_identifier() for keywords:
"token.original_case_keyword = display_case"

Comment explains:
"# Preserve original case for display. Identifiers use the original_case field
# to store the exact case as typed. Keywords use original_case_keyword to store
# the case determined by the keyword case policy (see Token class in tokens.py)."

This distinction is only documented in this one location and references an external file (tokens.py) not provided for verification.

---

#### code_vs_comment

**Description:** Inconsistent terminology for 'end of line' vs 'end of statement' in method documentation

**Affected files:**
- `src/parser.py`

**Details:**
The method at_end_of_line() at line 163 has documentation:
"Check if at end of logical line (NEWLINE or EOF)

Note: This method does NOT check for comment tokens (REM, REMARK, APOSTROPHE)
or statement separators (COLON). Use at_end_of_statement() when parsing statements
that should stop at comments/colons. Use at_end_of_line() for line-level parsing
where colons separate multiple statements on the same line."

However, the implementation at line 172 checks:
"return token.type in (TokenType.NEWLINE, TokenType.EOF)"

The method at_end_of_statement() at line 174 checks:
"return token.type in (TokenType.NEWLINE, TokenType.EOF, TokenType.COLON,
                      TokenType.REM, TokenType.REMARK, TokenType.APOSTROPHE)"

The documentation is clear and correct, but the usage throughout the code may be inconsistent. For example, in parse_print() at line 1296, it checks 'not self.at_end_of_line()' but also checks for COLON, ELSE, and REM tokens separately, which suggests at_end_of_statement() might be more appropriate.

---

#### documentation_inconsistency

**Description:** Incomplete documentation of expression parsing precedence levels

**Affected files:**
- `src/parser.py`

**Details:**
The parse_expression() method documentation at lines 598-611 lists precedence levels:
"Precedence (lowest to highest):
1. Logical: IMP
2. Logical: EQV
3. Logical: XOR
4. Logical: OR
5. Logical: AND
6. Logical: NOT
7. Relational: =, <>, <, >, <=, >=
8. Additive: +, -
9. Multiplicative: *, /, \\, MOD
10. Unary: -, +
11. Power: ^
12. Primary: numbers, strings, variables, functions, parentheses"

However, this list shows 'Unary: -, +' at level 10 and 'Power: ^' at level 11, but in standard mathematical precedence, unary operators typically have higher precedence than binary operators. The implementation at parse_unary() (line 779) calls parse_power() (line 791), which means unary operators are parsed BEFORE power operators, giving them HIGHER precedence. This contradicts the documentation which lists unary at level 10 and power at level 11 (where higher numbers should mean higher precedence).

---

#### code_vs_comment

**Description:** Comment about MID$ lookahead strategy may not match actual implementation complexity

**Affected files:**
- `src/parser.py`

**Details:**
At lines 527-548, there's a detailed comment about MID$ statement detection:
"# Detect MID$ used as statement: MID$(var, start, len) = value
# Look ahead to distinguish MID$ statement from MID$ function call
# MID$ statement has pattern: MID$ ( ... ) =
# MID$ function has pattern: MID$ ( ... ) in expression context
# Note: The lexer tokenizes 'MID$' (including the $) as a single token with type TokenType.MID
# Lookahead strategy: scan past balanced parentheses, check for = sign"

The implementation uses a try-except block with 'bare except' at line 543:
"except:
    # Bare except intentionally catches all exceptions during lookahead"

The comment at lines 544-547 justifies this:
"# (IndexError if we run past end, any parsing errors from malformed syntax)
# This is safe because position is restored below and proper error reported later"

However, using bare except is generally considered bad practice in Python, and the comment's justification that 'proper error reported later' may not be accurate if the lookahead fails for reasons other than 'not a MID$ statement'. This could mask genuine parsing errors.

---

#### code_vs_comment

**Description:** Comment about LINE modifier tokenization may be misleading

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines ~1090-1092 states:
"# Check for LINE modifier (e.g., INPUT "prompt";LINE var$)
# LINE allows input of entire line including commas
# Note: The lexer tokenizes standalone LINE keyword as LINE_INPUT token.
# This is distinct from the LINE INPUT statement which is parsed separately."

The comment says "standalone LINE keyword as LINE_INPUT token" but in the context of INPUT statement, LINE is not standalone - it's part of the INPUT syntax. The comment could be clearer about when LINE is tokenized as LINE_INPUT vs when it's part of INPUT...LINE syntax.

---

#### code_vs_comment

**Description:** LPRINT comment about trailing separator logic is confusing

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines ~1010-1015 states:
"# Add newline if there's no trailing separator
# For N expressions: N-1 separators (between items) = no trailing separator
#                    N separators (between items + at end) = has trailing separator
# Note: If len(separators) > len(expressions) (e.g., "LPRINT ;"), the trailing
# separator is already in the list and will suppress the newline."

The logic described is correct but the phrasing "N-1 separators (between items)" could be clearer. The comment mixes the concept of separators "between items" with trailing separators, which might confuse readers about whether the trailing separator is counted in the N-1 or N case.

---

#### code_vs_comment

**Description:** DEFTYPE comment about mode behavior is incomplete

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines ~1850-1856 states:
"Note: This method always updates def_type_map during parsing, regardless of mode.
The type map is shared between parsing passes in batch mode and affects variable
type inference throughout the program. The AST node is created for program
serialization/documentation."

The comment mentions "regardless of mode" and "batch mode" but doesn't explain what modes exist or what the alternative behavior would be. This suggests there might be an interactive mode vs batch mode distinction that isn't fully documented in this comment.

---

#### code_vs_comment

**Description:** DIM statement comment about dimension expressions contradicts typical BASIC behavior

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines ~1730-1734 states:
"Dimension expressions: This implementation matches MBASIC 5.21 behavior by accepting
any expression for array dimensions (e.g., DIM A(X*2, Y+1)). Dimensions are evaluated
at runtime. Note: Some compiled BASICs (GW-BASIC, QuickBASIC) require constants only."

This comment claims the implementation matches MBASIC 5.21 by accepting expressions, but then notes that GW-BASIC and QuickBASIC require constants. However, GW-BASIC is often considered very similar to MBASIC. This suggests either:
1. The comment is incorrect about GW-BASIC requiring constants
2. The comment is incorrect about matching MBASIC 5.21 behavior
3. There's a version difference not explained

Without access to MBASIC 5.21 documentation, this cannot be verified.

---

#### code_vs_comment

**Description:** DEF FN comment about function name normalization placement

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines ~1895-1901 states:
"Function name normalization: All function names are normalized to lowercase with
'fn' prefix (e.g., "FNR" becomes "fnr", "FNA$" becomes "fna$") for consistent
lookup. This matches the lexer's identifier normalization and ensures function
calls match their definitions regardless of case."

This detailed normalization comment appears in the DEF FN parser but doesn't show the actual normalization code in the visible portion. The comment should either be moved to where normalization occurs or reference where it happens.

---

#### code_vs_comment

**Description:** Comment in parse_resume() says RESUME and RESUME 0 both retry error statement, but implementation stores actual value

**Affected files:**
- `src/parser.py`

**Details:**
Comment states:
"Note: RESUME and RESUME 0 both retry the statement that caused the error."

Code implementation:
```python
line_number = int(self.advance().value)
```

The comment suggests RESUME 0 has special meaning (retry error statement), and notes that interpreter treats 0 and None equivalently. However, the parser stores the actual value (0 or other line number) without special handling. This creates ambiguity about whether 0 is a sentinel value or an actual line number 0.

---

#### code_vs_comment

**Description:** parse_width() docstring describes device parameter as 'implementation-specific' but provides no guidance on what values are valid

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states:
"device: Optional device expression (implementation-specific; may support
file numbers, device codes, or other values depending on the interpreter)"

The code simply parses any expression:
```python
device = self.parse_expression()
```

The comment acknowledges the parameter is implementation-specific but provides no examples or constraints. This makes it unclear what valid device values are (file numbers like #1, device names like "LPT1:", numeric codes, etc.).

---

#### documentation_inconsistency

**Description:** parse_common() docstring says 'Non-empty parentheses are an error' but doesn't show error handling code

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states:
"The empty parentheses () indicate an array variable (all elements shared).
This is just a marker - no subscripts are specified or stored. Non-empty
parentheses are an error (parser enforces empty parens only)."

Code implementation:
```python
if self.match(TokenType.LPAREN):
    self.advance()
    if not self.match(TokenType.RPAREN):
        raise ParseError("Expected ) after ( in COMMON array", self.current())
    self.advance()
```

The error message "Expected ) after ( in COMMON array" doesn't clearly communicate that subscripts are not allowed. A user might interpret this as a syntax error rather than understanding that COMMON arrays cannot have subscripts specified.

---

#### code_vs_comment

**Description:** parse_def_fn() comment about function name normalization is inconsistent with actual behavior

**Affected files:**
- `src/parser.py`

**Details:**
Comment states:
"function_name = 'fn' + raw_name  # Use lowercase 'fn' to match function calls"

And later:
"# raw_name already starts with lowercase 'fn' from lexer normalization
function_name = raw_name"

The first comment suggests adding 'fn' prefix, while the second suggests it's already there. The code handles two cases:
1. DEF FN R (space): adds 'fn' prefix
2. DEF FNR (no space): already has 'fn' from lexer

The comments don't clearly explain why these two paths exist or that they're handling different tokenization scenarios.

---

#### code_vs_comment

**Description:** apply_keyword_case_policy docstring says 'Callers may pass keywords in any case' but emit_keyword docstring says 'keyword MUST be normalized lowercase by caller'

**Affected files:**
- `src/position_serializer.py`

**Details:**
apply_keyword_case_policy docstring: 'Callers may pass keywords in any case.'

emit_keyword docstring: 'Args:
    keyword: The keyword to emit (MUST be normalized lowercase by caller)'

These are contradictory requirements for the same parameter type.

---

#### documentation_inconsistency

**Description:** Module docstring claims 'No need to track current_line/current_stmt/next_line/next_stmt separately' but doesn't explain what system it replaced

**Affected files:**
- `src/pc.py`

**Details:**
The module docstring lists benefits of the PC design including 'No need to track current_line/current_stmt/next_line/next_stmt separately' but there's no context about what the previous system was or why this is better. This makes the claim hard to verify.

---

#### code_vs_comment

**Description:** preserve policy docstring describes defensive fallback but doesn't explain when this incorrect usage would occur

**Affected files:**
- `src/position_serializer.py`

**Details:**
In apply_keyword_case_policy for 'preserve' policy:

'# The "preserve" policy means callers should pass keywords already in the correct case
# and this function returns them as-is. However, since we can\'t know the original case
# here, we provide a defensive fallback (capitalize) for robustness in case this
# function is called incorrectly with "preserve" policy.'

This suggests the function might be called incorrectly but doesn't explain the scenario. If callers should never call this with 'preserve', why have the fallback?

---

#### documentation_inconsistency

**Description:** Module docstrings have asymmetric cross-references

**Affected files:**
- `src/resource_limits.py`
- `src/resource_locator.py`

**Details:**
resource_limits.py states: 'Note: This is distinct from resource_locator.py which finds package data files.'

resource_locator.py states: 'Note: This is distinct from resource_limits.py which enforces runtime execution limits.'

Both files correctly distinguish themselves from each other, but the phrasing is slightly different. resource_limits.py says resource_locator 'finds package data files' while resource_locator.py says resource_limits 'enforces runtime execution limits'. This is consistent in meaning but could be more parallel in structure.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for string length limits

**Affected files:**
- `src/resource_limits.py`

**Details:**
The parameter is named 'max_string_length' and documented as 'Maximum length for a string variable (bytes)' in multiple places.

However, in check_string_length() method, the error message says: 'String too long: {byte_length} bytes (limit: {self.max_string_length} bytes)'

While in estimate_size() method, the comment says: 'String: UTF-8 byte length + 4-byte length prefix'

The term 'length' is used but it's actually measuring 'byte length' or 'size'. This could be confusing since string 'length' often refers to character count, not byte count. The code is consistent in using bytes, but the terminology could be clearer.

---

#### code_vs_comment_conflict

**Description:** Comment about MBASIC 5.21 compatibility in unlimited limits may be misleading

**Affected files:**
- `src/resource_limits.py`

**Details:**
In create_unlimited_limits() function:

The code sets: 'max_string_length=1024*1024'  # 1MB strings (for testing/development - not MBASIC compatible)

However, the other two preset functions (create_web_limits and create_local_limits) both set max_string_length=255 with comment '# 255 bytes (MBASIC 5.21 compatibility)'

The comment in create_unlimited_limits() correctly notes it's 'not MBASIC compatible', but this creates an inconsistency where the 'unlimited' preset actually breaks MBASIC compatibility. This may be intentional for testing, but could cause confusion if someone uses unlimited limits expecting MBASIC-compatible behavior.

---

#### code_vs_comment

**Description:** Comment about line=-1 usage is inconsistent between different locations

**Affected files:**
- `src/runtime.py`

**Details:**
Line 47-53 in __init__ comment: "Note: line -1 in last_write indicates non-program execution sources:
1. System/internal variables (ERR%, ERL%) via set_variable_raw() with FakeToken(line=-1)
2. Debugger/interactive prompt via set_variable() with debugger_set=True and token.line=-1
Both use line=-1, making them indistinguishable from each other in last_write alone.
However, line=-1 distinguishes these special sources from normal program execution (line >= 0)."

Line 430-437 in set_variable_raw() comment: "The line=-1 marker in last_write indicates system/internal variables.
However, debugger sets also use line=-1 (via debugger_set=True),
making them indistinguishable from system variables in last_write alone.
Both are distinguished from normal program execution (line >= 0)."

These comments are consistent, but the explanation is repeated in multiple places. Consider consolidating into a single authoritative comment location.

---

#### documentation_inconsistency

**Description:** Incomplete docstring for get_all_variables() method

**Affected files:**
- `src/runtime.py`

**Details:**
Line 1009-1023: The docstring for get_all_variables() is incomplete:

"""Export all variables with structured type information.

Returns detailed information about each variable including:
- Base name (without type suffix)
- Type suffix character
- For scalars: current value
- For arrays: dimensions and base
- Access tracking: last_read and last_write info

Returns:
    list: List of dictionaries with variable information
          Each dict contains:
"""

The docstring ends abruptly with "Each dict contains:" without listing what the dict actually contains. The implementation is present but the documentation is incomplete.

---

#### code_vs_comment

**Description:** Comment about token.line fallback behavior is inconsistent with ValueError check

**Affected files:**
- `src/runtime.py`

**Details:**
Line 234-243 in get_variable() docstring: "token: REQUIRED - Token object for tracking (ValueError raised if None).

Token object is required but its attributes are optional:
- token.line: Preferred for tracking, falls back to self.pc.line_num if missing
- token.position: Preferred for tracking, falls back to None if missing

This allows robust handling of tokens from various sources (lexer, parser,
fake tokens) while enforcing that some token object must be provided.
For debugging without token requirements, use get_variable_for_debugger()."

Line 248-249: "if token is None:
    raise ValueError('get_variable() requires token parameter. Use get_variable_for_debugger() instead.')"

The comment describes fallback behavior for missing token.line attribute, but the code raises ValueError if token itself is None. The comment should clarify that token object is required (not None) but its attributes can be missing.

---

#### Code vs Comment conflict

**Description:** Comment claims default type suffix fallback should not occur in practice, but code implements it as defensive programming

**Affected files:**
- `src/runtime.py`

**Details:**
In parse_name() helper function within get_variables():

Comment says: "Note: In normal operation, all names in _variables have resolved type suffixes from _resolve_variable_name() which applies DEF type rules. This fallback is defensive programming for robustness - it should not occur in practice, but protects against potential edge cases in legacy code or future changes."

Code implements: "return full_name, '!'" as fallback when no type suffix present.

The comment suggests this is purely defensive and shouldn't happen, but doesn't explain if this is truly unreachable or if there are legitimate edge cases.

---

#### Documentation inconsistency

**Description:** Redundant field documentation acknowledges redundancy but doesn't explain why it exists

**Affected files:**
- `src/runtime.py`

**Details:**
In get_execution_stack() docstring for GOSUB calls:

"Note: 'from_line' is redundant with 'return_line' - both contain the same value (the line number to return to after RETURN). The 'from_line' field exists for backward compatibility with code that expects it. Use 'return_line' for new code as it more clearly indicates the field's purpose."

This documents the redundancy but doesn't specify what code depends on 'from_line' or when it might be safe to remove. The deprecation policy is unclear compared to get_loop_stack() which has explicit deprecation dates.

---

#### Documentation inconsistency

**Description:** Inconsistent terminology for statement offset indexing explanation

**Affected files:**
- `src/runtime.py`

**Details:**
Multiple docstrings explain 0-based indexing differently:

get_gosub_stack(): "Note: stmt_offset uses 0-based indexing (offset 0 = 1st statement, offset 1 = 2nd statement, etc.)"

set_breakpoint(): "Note: Uses 0-based indexing (offset 0 = 1st statement, offset 1 = 2nd statement, offset 2 = 3rd statement, etc.)"

get_execution_stack() example: "This shows: FOR I at line 100, statement offset 0 (1st statement)..."

While all are technically correct, the varying levels of detail (some show 2 examples, some show 3) and placement (some in Notes, some inline) create minor inconsistency in documentation style.

---

#### Documentation inconsistency

**Description:** Deprecation notice uses inconsistent date format

**Affected files:**
- `src/runtime.py`

**Details:**
In get_loop_stack() deprecation notice:
"Deprecated since: 2025-10-25 (commit cda25c84)"

This date (October 25, 2025) is in the future relative to typical development timelines, suggesting either:
1. The date format is incorrect (should be 2024-10-25)
2. This is placeholder documentation
3. The year is a typo

The removal date "No earlier than 2026-01-01" would only give 2 months notice if the deprecation date is correct, which seems short for a compatibility feature.

---

#### documentation_inconsistency

**Description:** Duplicate documentation of settings file paths in two files

**Affected files:**
- `src/settings.py`
- `src/settings_backend.py`

**Details:**
Both settings.py and settings_backend.py document the same file paths:

settings.py docstring:
"- Global: ~/.mbasic/settings.json (Linux/Mac) or %APPDATA%/mbasic/settings.json (Windows)
- Project: .mbasic/settings.json in project directory"

settings_backend.py FileSettingsBackend docstring:
"Stores settings in JSON files:
- Global: ~/.mbasic/settings.json (Linux/Mac) or %APPDATA%/mbasic/settings.json (Windows)
- Project: .mbasic/settings.json in project directory"

This duplication could lead to maintenance issues if paths change.

---

#### code_vs_comment

**Description:** Comment about file-level settings infrastructure being 'fully implemented' is misleading

**Affected files:**
- `src/settings.py`

**Details:**
Multiple comments state file-level settings are 'fully implemented':

In SettingsManager docstring:
"Note: File-level settings infrastructure is fully implemented (file_settings dict,
FILE scope support in get/set/reset methods), but currently unused."

In get() method:
"Note: File-level settings infrastructure is fully implemented and functional.
The file_settings dict can be set programmatically and is checked first in precedence."

However, the infrastructure is only partially implemented:
- file_settings dict exists
- get() checks it
- set() can write to it
- reset_to_defaults() can clear it
- BUT: load() never populates it from any source
- BUT: save() never persists it anywhere

So it's not 'fully implemented' - it's a runtime-only dict with no persistence.

---

#### code_vs_documentation

**Description:** Comments mention settings not included but don't explain why

**Affected files:**
- `src/settings_definitions.py`

**Details:**
Two comments mention excluded settings:

"# Note: editor.tab_size setting not included - BASIC uses line numbers for program structure,
# not indentation, so tab size is not a meaningful setting for BASIC source code"

"# Note: Line numbers are always shown - they're fundamental to BASIC!
# editor.show_line_numbers setting not included - makes no sense for BASIC"

These are good explanatory comments, but they reference settings that don't exist anywhere in the codebase. This could confuse developers looking for these settings. The comments are defensive documentation against expected but non-existent features.

---

#### code_vs_comment

**Description:** Module docstring references src/lexer.py but doesn't verify the relationship

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
Module docstring states:
"This is a simplified keyword case handler used by the lexer (src/lexer.py)."

And later:
"The lexer (src/lexer.py) uses SimpleKeywordCase because keywords only need
force-based policies in the tokenization phase."

However, src/lexer.py is not provided in the source files, so this relationship cannot be verified. The comment makes claims about how another module uses this code, but that module isn't available for verification.

---

#### documentation_inconsistency

**Description:** RedisSettingsBackend comment mentions 'nicegui or redis-py' but only redis-py is imported

**Affected files:**
- `src/settings_backend.py`

**Details:**
RedisSettingsBackend.__init__ docstring says:
"Args:
    redis_client: Redis client instance (from nicegui or redis-py)"

But in create_settings_backend(), only redis-py is used:
"import redis
redis_client = redis.from_url(redis_url, decode_responses=True)"

No nicegui Redis client is ever used. The comment suggests two possible sources but only one is implemented.

---

#### code_vs_comment

**Description:** RedisSettingsBackend TTL comment says '24 hours (matches NiceGUI session expiry)' but this is hardcoded assumption

**Affected files:**
- `src/settings_backend.py`

**Details:**
In RedisSettingsBackend._set_data():
"# Set with TTL of 24 hours (matches NiceGUI session expiry)
self.redis.setex(self.redis_key, 86400, data)"

The comment assumes NiceGUI session expiry is 24 hours, but this is not verified anywhere in the code. If NiceGUI's session expiry changes or is configurable, this hardcoded value would be incorrect. The comment makes an assertion about external behavior without verification.

---

#### Documentation inconsistency

**Description:** The UIBackend docstring mentions 'BatchBackend' as a potential future backend type but then includes a confusing note about 'headless' being contradictory. The comment seems to conflate batch/non-interactive execution with headless operation.

**Affected files:**
- `src/ui/base.py`

**Details:**
From base.py docstring:
"Future/potential backend types (not yet implemented):
- WebBackend: Browser-based interface
- BatchBackend: Non-interactive execution mode for running programs from command line
               (Note: 'headless' typically means no UI, which seems contradictory to UIBackend purpose;
               batch/non-interactive execution may be better handled outside the UIBackend abstraction)"

The parenthetical note creates confusion about whether batch execution should be a UIBackend or not.

---

#### Code vs Comment conflict

**Description:** Comment in _create_setting_widget() claims both removeprefix() and fallback [6:] 'only strip from the beginning', but this is redundant since slicing [6:] by definition only operates on the beginning of the string. The comment seems to over-explain obvious behavior.

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
Comment in _create_setting_widget():
"# Create display label (strip 'force_' prefix from beginning for cleaner display)
# Note: Both removeprefix() and the fallback [6:] only strip from the beginning,
# ensuring we don't modify 'force_' appearing elsewhere in the string"

The note about [6:] 'only strip from the beginning' is redundant - string slicing from the start always operates on the beginning.

---

#### Code vs Comment conflict

**Description:** Comment in _on_reset() states it compares 'actual value' not 'display label' and mentions 'force_' prefix stripping, but this explanation is overly detailed for what is simply setting a radio button state to match the default value.

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
Comment in _on_reset():
"# Set radio button to default value
# Note: Compares actual value (stored in _actual_value) not display label
# since display labels have 'force_' prefix stripped (see _create_setting_widget)"

The code simply does: rb.set_state(rb._actual_value == defn.default)

The comment over-explains the comparison when the code is self-evident.

---

#### Documentation inconsistency

**Description:** The cmd_break() docstring states 'Breakpoints can be set at any time (before or during execution)' and 'Use RUN to start the program', but there's no clear documentation about what happens if you set breakpoints during execution or how the breakpoint system integrates with the running program.

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
cmd_break() docstring:
"Breakpoints can be set at any time (before or during execution).
They are checked during program execution at each statement.
Use RUN to start the program, and it will pause when reaching breakpoints."

The enhance_run_command() method modifies RUN behavior, but there's no documentation about how breakpoints set during execution (after RUN) are handled.

---

#### code_vs_comment

**Description:** Comment about target_column default value is misleading

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _sort_and_position_line docstring:
"target_column: Column to position cursor at (default: 7). This value is an approximation for typical line numbers."

And in keypress method:
"Note: Methods like _sort_and_position_line use a default target_column of 7, which assumes typical line numbers (status=1 char + number=5 digits + space=1 char)."

But the math is wrong: 1 + 5 + 1 = 7 assumes ALL line numbers are exactly 5 digits (like 10000-99999). For typical line numbers like 10, 100, 1000, the code area starts at column 3, 4, or 5, not 7. The comment should say 'assumes 5-digit line numbers' not 'typical line numbers'.

---

#### code_vs_comment

**Description:** Comment about syntax error priority is redundant with code

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _get_status_char method:
"Get the status character for a line based on priority.

Priority order (highest to lowest):
1. Syntax error (?) - highest priority
2. Breakpoint (●) - medium priority
3. Normal ( ) - default"

The code implementation is:
"if has_syntax_error:
    return '?'
elif line_number in self.breakpoints:
    return '●'
else:
    return ' '"

The comment exactly mirrors the code structure with no additional information. This is not an inconsistency per se, but the comment adds no value and could become outdated if priorities change.

---

#### code_vs_comment

**Description:** Comment about 'use is None instead of not' is overly defensive

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _display_syntax_errors method:
"# Check if output walker is available (use 'is None' instead of 'not' to avoid false positive on empty walker)
if self._output_walker is None:"

This comment suggests that 'not self._output_walker' would give false positive on empty walker. However, an empty walker (ListWalker with no items) is still truthy in Python - only None is falsy. The comment implies a bug that doesn't exist. Using 'is None' is correct, but the justification is wrong.

---

#### code_vs_comment

**Description:** Comment about fast path optimization is misleading

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In keypress method:
"# FAST PATH: For normal printable characters, bypass all processing
# This is critical for responsive typing
if len(key) == 1 and key >= ' ' and key <= '~':
    return super().keypress(size, key)"

Comment claims this bypasses 'all processing', but super().keypress() still does significant processing (urwid's Edit widget processing, cursor movement, text insertion, etc.). The comment should say 'bypass editor-specific processing' or 'bypass syntax checking and column protection'.

---

#### code_vs_comment

**Description:** Comment says _create_toolbar is 'UNUSED' but provides detailed explanation that could be misleading

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
At line ~420, comment states:
STATUS: UNUSED - not called anywhere in current implementation.

The toolbar was removed from the UI in favor of Ctrl+U menu for better keyboard navigation. This fully-implemented method is retained for reference in case toolbar functionality is desired in the future. Can be safely removed if no plans to restore.

This is accurate documentation of unused code, but the phrase 'Can be safely removed' conflicts with 'retained for reference'. Should clarify intent.

---

#### code_vs_comment

**Description:** Comment about Interpreter lifecycle says it's never recreated, but this seems to conflict with the need to reset state between runs

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~180 says:
# Interpreter Lifecycle:
# Created ONCE here in __init__ and reused throughout the session.
# The interpreter object itself is NEVER recreated - the same instance is used
# for the lifetime of the UI session.

This raises the question of how state is reset between program runs. The comment doesn't explain how the interpreter is cleaned/reset, which could be important for understanding the architecture.

---

#### code_vs_comment

**Description:** Status bar update inconsistency in debug methods

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _debug_step() (line ~850) and _debug_step_line() (line ~920), comments say '(No status bar update - output will show in output window)' but later in the same methods, there ARE status bar updates:

Line ~880: self.status_bar.set_text(f"Paused at {pc_display} - ...")
Line ~950: self.status_bar.set_text(f"Paused at {pc_display} - ...")

The comment is misleading - it should say 'No initial status bar update' or remove the comment entirely.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for 'statement' vs 'stmt' in variable names and UI text

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
The code uses both 'stmt' and 'statement' inconsistently:
- highlight_stmt parameter (line ~870)
- 'step_statement' mode string (line ~860)
- STEP_KEY for 'Step Statement' (line ~750)
- stmt_offset in PC (line ~880)

While 'stmt' is a common abbreviation, mixing both forms in user-facing text and internal APIs could cause confusion.

---

#### code_vs_comment

**Description:** Comment about column positioning in _smart_insert_line is inconsistent with actual column numbers

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
At line ~1195, comment says:
# Position cursor on the new line, at the code area (column 7)

But the actual position calculation uses column 7 for a line number that could be variable width. The comment assumes fixed-width line numbers, but the code uses variable-width parsing elsewhere (e.g., _parse_line_number). This could be incorrect for line numbers with different digit counts.

---

#### code_vs_comment

**Description:** Comment about main widget storage strategy differs between methods but implementation is consistent

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple comments explain main widget storage:

1. _show_help (line ~520): "Main widget retrieval: Use self.base_widget (stored at UI creation time in __init__) rather than self.loop.widget (which reflects the current widget and might be a menu or other overlay)."

2. _activate_menu (line ~620): "Extract base widget from current loop.widget to unwrap any existing overlay. This differs from _show_help/_show_keymap/_show_settings which use self.base_widget directly, since menu needs to work even when other overlays are already present."

These comments accurately describe different strategies for different use cases, but the distinction could be confusing without understanding the full context.

---

#### code_vs_comment

**Description:** Comment about status bar behavior during errors is inconsistent across methods

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple locations have comments about status bar behavior:

1. Line ~1165: "# Status bar stays at default - error is displayed in output"
2. Line ~1220: "# Status bar stays at default (STATUS_BAR_SHORTCUTS) - error is in output"
3. Line ~1240: "# Status bar stays at default (STATUS_BAR_SHORTCUTS) - error is in output"
4. Line ~1260: "# Status bar stays at default - error is displayed in output"
5. Line ~1280: "# No status bar update - program output will show in output window"

Some comments specify STATUS_BAR_SHORTCUTS constant while others just say 'default'. The implementation appears consistent but comment wording varies.

---

#### code_internal_inconsistency

**Description:** Inconsistent error message formatting - some use box drawing characters, some don't specify format in comments

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Error formatting varies:

1. Parse errors (line ~1160): Use box with ┌─ Parse Error ────┐
2. Startup errors (line ~1230): Use box with ┌─ Startup Error ──┐
3. Runtime errors (line ~1320): Use box with ┌─ Runtime Error ──┐
4. Unexpected errors (line ~1270): Use box with ┌─ Unexpected Error ─┐

All use similar box formatting but the box widths and dash counts differ slightly. This is a minor visual inconsistency.

---

#### code_vs_comment

**Description:** Comment about statement-level precision for GOSUB uses 0-based indexing but may be confusing without context

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1090 states:
"# Show statement-level precision for GOSUB return address
# return_stmt is statement offset (0-based index): 0 = first statement, 1 = second, etc."

The comment is accurate but the display format 'line {entry['from_line']}.{return_stmt}' uses 0-based statement numbers which might be confusing to users expecting 1-based numbering.

---

#### code_vs_comment

**Description:** Comment says _sync_program_to_runtime doesn't start execution, but doesn't mention it can preserve running execution state

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _sync_program_to_runtime method docstring:
"Sync program to runtime without resetting PC.

Updates runtime's statement_table and line_text_map from self.program,
but preserves current PC/execution state. This allows LIST and other
commands to see the current program without starting execution."

The comment focuses on "without starting execution" but the implementation has complex logic to preserve PC when self.running=True and not paused_at_breakpoint. The docstring could be clearer about when PC is preserved vs reset.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate mentions syncing allows LIST to see current program, but LIST command implementation calls _list_program which doesn't use runtime

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _execute_immediate method:
"# Sync program to runtime (updates statement table and line text map).
# If execution is running, _sync_program_to_runtime preserves current PC.
# If not running, it sets PC to halted. Either way, this doesn't start execution,
# but allows commands like LIST to see the current program."

However, _list_program (called by cmd_list) uses self.editor_lines directly, not runtime's statement_table. The comment may be outdated or referring to a different LIST implementation.

---

#### code_vs_comment

**Description:** Comment in cmd_delete and cmd_renum says runtime=None but doesn't explain why

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In cmd_delete:
"delete_lines_from_program(self.program, args, runtime=None)"

In cmd_renum:
"renum_program(self.program, args, self.interpreter.interactive_mode._renum_statement, runtime=None)"

Both pass runtime=None to helper functions, then call _sync_program_to_runtime() afterward. The comment doesn't explain this pattern - it appears the helpers don't need runtime because sync happens separately, but this isn't documented.

---

#### code_vs_comment_conflict

**Description:** Comment about version.py conflicts with hardcoded version implementation

**Affected files:**
- `src/ui/help_macros.py`

**Details:**
Comment at line ~82:
"# Hardcoded MBASIC version for documentation
# Note: Project has internal implementation version (src/version.py) separate from this
return '5.21'  # MBASIC 5.21 language version"

The comment suggests there's a src/version.py file with a different version, but this file is not provided in the source code listing. The comment implies a separation between 'documentation version' and 'implementation version' but doesn't explain why they should differ or how to keep them in sync.

---

#### documentation_inconsistency

**Description:** Docstring says 'ESC/Q to exit' but implementation also accepts lowercase 'q'

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Module docstring states:
"Provides:
- Up/Down scrolling through help content
- Enter to follow links
- ESC/Q to exit"

But keypress() method handles:
if key in ('q', 'Q', 'esc'):

So both uppercase Q and lowercase q work, but docstring only mentions uppercase Q.

---

#### code_vs_comment_conflict

**Description:** Comment says 'QUIT_KEY is None (menu-only)' but keybindings module is not shown

**Affected files:**
- `src/ui/interactive_menu.py`

**Details:**
Comment at line ~37:
"('Quit', 'quit'),  # QUIT_KEY is None (menu-only)"

This references a QUIT_KEY constant from the keybindings module (kb), but we cannot verify this claim since the keybindings module source is not provided. The comment implies there's no keyboard shortcut for quit outside the menu.

---

#### code_vs_comment_conflict

**Description:** Comment says 'STACK_KEY is '' (menu-only)' but keybindings module is not shown

**Affected files:**
- `src/ui/interactive_menu.py`

**Details:**
Comment at line ~52:
"('Execution Stack', '_toggle_stack_window'),  # STACK_KEY is '' (menu-only)"

This references a STACK_KEY constant from the keybindings module (kb), but we cannot verify this claim since the keybindings module source is not provided. The comment implies there's no keyboard shortcut for stack window outside the menu.

---

#### documentation_inconsistency

**Description:** Search result path format inconsistency in comments

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at line ~370:
"# Check if target is already an absolute path (from search results)
# Absolute paths start with common/ or ui/"

But earlier in _search_indexes() at line ~165, search results store paths as:
results.append((
    tier_label,
    file_info.get('path', ''),
    ...
))

The comment describes these as 'absolute paths' but they're actually help-root-relative paths. The term 'absolute' is misleading since they're relative to help_root, not filesystem absolute.

---

#### Code vs Comment conflict

**Description:** Comment claims MAXIMIZE_OUTPUT_KEY is 'menu-only feature, not documented as keyboard shortcut', but the constant is defined with a keyboard shortcut value.

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Line 191: MAXIMIZE_OUTPUT_KEY = 'ctrl shift m'

Comment in KEYBINDINGS_BY_CATEGORY (lines 217-222) says:
# - MAXIMIZE_OUTPUT_KEY (Shift+Ctrl+M) - Menu-only feature, not documented as keyboard shortcut

If it's truly menu-only, why define it with a keyboard shortcut value? This suggests either the comment is outdated or the implementation doesn't match the intent.

---

#### Code vs Comment conflict

**Description:** Comment says STACK_KEY has no keyboard shortcut and is menu-only, but this contradicts the pattern of other constants that have actual key values.

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Line 156: STACK_KEY = ''  # No keyboard shortcut

Comment in KEYBINDINGS_BY_CATEGORY (lines 217-222) says:
# - STACK_KEY (empty string) - No keyboard shortcut assigned, menu-only

While technically consistent, using an empty string for 'no shortcut' is inconsistent with QUIT_KEY which uses None for the same purpose. This inconsistency could cause bugs.

---

#### Code vs Documentation inconsistency

**Description:** Inconsistent key display format between keybindings.py and keymap_widget.py for Shift+Ctrl combinations.

**Affected files:**
- `src/ui/keybindings.py`
- `src/ui/keymap_widget.py`

**Details:**
In keybindings.py, key_to_display() returns:
'shift ctrl b' -> '^Shift+B'

In keymap_widget.py, _format_key_display() converts:
'Shift+Ctrl+V' -> 'Shift+^V'

These two functions produce different formats for the same type of key combination. The keybindings.py version puts the caret before 'Shift', while keymap_widget.py puts it after.

---

#### Code vs Comment conflict

**Description:** Comment claims certain keys are not included in KEYBINDINGS_BY_CATEGORY, but doesn't explain why MENU_KEY is also excluded despite being a global command.

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Lines 217-222:
# Note: This dictionary contains keybindings shown in the help system.
# Some defined constants are not included here:
# - CLEAR_BREAKPOINTS_KEY (Shift+Ctrl+B) - Available in menu under Edit > Clear All Breakpoints
# - STOP_KEY (Ctrl+X) - Shown in debugger context in the Debugger category
# - MAXIMIZE_OUTPUT_KEY (Shift+Ctrl+M) - Menu-only feature, not documented as keyboard shortcut
# - STACK_KEY (empty string) - No keyboard shortcut assigned, menu-only
# - Dialog-specific keys (DIALOG_YES_KEY, DIALOG_NO_KEY, SETTINGS_APPLY_KEY, SETTINGS_RESET_KEY) - Shown in dialog prompts
# - Context-specific keys (VARS_SORT_MODE_KEY, VARS_SORT_DIR_KEY, etc.) - Shown in Variables Window category

However, STOP_KEY (Ctrl+X) IS included in the 'Debugger (when program running)' category (line 253), contradicting the comment. Also, MENU_KEY is defined (line 135) but not listed in the exclusions comment, yet it IS included in KEYBINDINGS_BY_CATEGORY (line 230).

---

#### Code inconsistency

**Description:** Inconsistent handling of missing JSON keys - some use if/else with defaults, others just use defaults in the else clause.

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Some keys use this pattern:
_run_from_json = _get_key('editor', 'run')
RUN_KEY = _ctrl_key_to_urwid(_run_from_json) if _run_from_json else 'ctrl r'

But QUIT_ALT_KEY uses the same pattern even though the comment suggests Ctrl+C is always the fallback:
_quit_alt_from_json = _get_key('editor', 'quit')
QUIT_ALT_KEY = _ctrl_key_to_urwid(_quit_alt_from_json) if _quit_alt_from_json else 'ctrl c'

This inconsistency suggests uncertainty about whether these defaults should ever be used or if they're just safety fallbacks.

---

#### Documentation inconsistency

**Description:** Module docstring claims 'Not thread-safe (no locking mechanism)' but doesn't explain why this matters or what the consequences are.

**Affected files:**
- `src/ui/recent_files.py`

**Details:**
Lines 1-22 (module docstring):
"""Recent Files Manager - Shared module for tracking recently opened files
...
Features:
- Stores last 10 recently opened files
- Records full path and last access timestamp
- Automatically creates config directory if needed
- Cross-platform (uses pathlib)
- Note: Not thread-safe (no locking mechanism)
"""

This warning about thread-safety is mentioned but not explained. Given that the module is used across multiple UIs (Tk, Curses, Web), it's unclear if this is a real concern or just a theoretical limitation.

---

#### Code vs Comment conflict

**Description:** Comment describes path normalization duplication but implementation details differ slightly

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Line 267 comment states:
Note: Path normalization logic is duplicated in _open_link_in_new_window().
Both methods use similar approach: resolve relative paths, normalize to help_root,
handle path separators. If modification needed, update both methods consistently.

However, comparing _follow_link() (lines 267-298) and _open_link_in_new_window() (lines 682-710), the implementations have subtle differences:
- _follow_link checks for absolute paths with: if target.startswith('/') or target.startswith('common/') or ':/' in target or ':\\' in target
- _open_link_in_new_window checks: if not url.startswith('.')

These are different conditions that may not handle all cases identically. The comment suggests they use 'similar approach' but the actual logic differs in how absolute vs relative paths are detected.

---

#### Code vs Comment conflict

**Description:** Comment about table formatting duplication references non-existent file

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Line 714 comment in _format_table_row() states:
Note: This implementation may be duplicated in src/ui/markdown_renderer.py.
If both implementations exist and changes are needed to table formatting logic,
consider extracting to a shared utility module to maintain consistency.

However, src/ui/markdown_renderer.py is not provided in the source files, so we cannot verify if this duplication actually exists. The comment suggests uncertainty ('may be duplicated') but provides no way to verify this claim.

---

#### Code vs Comment conflict

**Description:** Comment about link tag prefixes is incomplete

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Line 632 comment states:
Note: Both 'link_' (from _render_line_with_links) and 'result_link_'
(from _execute_search) prefixes are checked. Both types are stored
identically in self.link_urls, but the prefixes distinguish their origin.

However, the code also creates tags with prefix 'result_link_' in _execute_search (line 449), but the actual tag binding in _render_line_with_links uses 'link_{counter}' format (line 234). The comment correctly identifies both prefixes but doesn't mention that there's also a plain 'link' tag used for styling (line 161) which is different from the clickable link tags.

---

#### Documentation inconsistency

**Description:** Module docstring lists features not fully explained in implementation comments

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Module docstring (lines 1-10) lists:
- Table formatting for markdown tables

But the _format_table_row() method (lines 714-732) has minimal documentation about how table formatting works. The docstring promises 'table formatting' as a feature but doesn't explain that separator rows are skipped, columns are padded to 15 chars, or that markdown formatting in cells is cleaned up.

---

#### Code vs Documentation inconsistency

**Description:** Comment about modal behavior is misleading

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Line 48 comment states:
# Make modal (prevents interaction with parent, but doesn't block code execution - no wait_window())

This comment is technically correct but potentially misleading. The dialog uses transient() and grab_set() which do make it modal in the UI sense (blocking parent interaction), but the comment's emphasis on 'doesn't block code execution' might confuse readers about what 'modal' means in this context. The comment seems to be clarifying that it's not using wait_window() for synchronous blocking, but this level of detail might not be necessary or could be clearer.

---

#### Code vs Comment conflict

**Description:** Comment about help display mechanism is imprecise

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Line 147 comment states:
# Show short help as inline label (not a hover tooltip, just a gray label)

The comment clarifies it's 'not a hover tooltip' but this seems defensive - there's no code that would suggest it's a tooltip. The comment may be outdated from a previous implementation or design discussion where tooltips were considered. The parenthetical clarification adds no value to understanding the current code.

---

#### Code vs Comment conflict

**Description:** Comment about menu dismissal is overly detailed

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Line 649 comment states:
# Define dismiss_menu helper for ESC/FocusOut bindings (below)

Followed by line 658 comment:
# Release grab after menu is shown. Note: tk_popup handles menu interaction,
# but we explicitly release the grab to ensure clean state.

These comments provide implementation details about menu handling that are standard Tkinter patterns. The level of detail suggests these were added during debugging or as learning notes, but may not be necessary for maintenance. The second comment's note about tk_popup handling interaction is particularly verbose.

---

#### code_vs_comment

**Description:** Comment describes 3-pane layout with specific weights but implementation may differ

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring lines 48-54 states:
- 3-pane vertical layout (weights: 3:2:1 = total 6 units):
  * Editor with line numbers (top, ~50% = 3/6 - weight=3)
  * Output pane (middle, ~33% = 2/6 - weight=2)
    - Contains INPUT row (shown/hidden dynamically for INPUT statements)
  * Immediate mode input line (bottom, ~17% = 1/6 - weight=1)

Code at lines 218-220, 227-228, 234-235 shows:
paned.add(editor_frame, weight=3)
paned.add(output_frame, weight=2)
paned.add(immediate_frame, weight=1)

Weights match documentation. However, immediate_frame has height=40 forced (line 237: input_frame.pack_propagate(False)) which may override the weight-based sizing, making it not truly ~17% but a fixed 40 pixels.

---

#### code_vs_comment

**Description:** Variables window heading text comment doesn't match actual implementation detail

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines 1089-1090 comment states:
# Set initial heading text with down arrow (matches self.variables_sort_column='accessed', descending)
tree.heading('#0', text='↓ Variable (Last Accessed)')

The comment says 'descending' but the actual sort direction is controlled by self.variables_sort_reverse=True (line 127). While True typically means descending, the comment should reference the actual variable name for clarity.

---

#### documentation_inconsistency

**Description:** Docstring usage example references TkIOHandler but doesn't show its import or initialization details

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines 56-66 show usage example:
Usage:
    from src.ui.tk_ui import TkBackend, TkIOHandler
    from src.editing.manager import ProgramManager

    io = TkIOHandler()  # TkIOHandler created without backend reference initially
    def_type_map = {}  # Type suffix defaults for variables (DEFINT, DEFSNG, etc.)
    program = ProgramManager(def_type_map)
    backend = TkBackend(io, program)
    backend.start()  # Runs Tk mainloop until window closed

The comment says 'TkIOHandler created without backend reference initially' but doesn't explain that the backend reference is set later. Looking at line 318, the actual initialization is:
tk_io = TkIOHandler(self._add_output, self.root, backend=self)

The usage example is misleading - it shows TkIOHandler() with no arguments, but the actual code passes three arguments.

---

#### code_vs_comment

**Description:** Comment about immediate entry focus handling is overly detailed for implementation detail

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines 299-303 have extensive comments about focus handling:
# Initialize immediate mode entry to be enabled and focused
# (it will be enabled/disabled later based on program state via _update_immediate_status)
self.immediate_entry.config(state=tk.NORMAL)

# Ensure entry is above other widgets
self.immediate_entry.lift()

# Give initial focus to immediate entry for convenience
def set_initial_focus():
    # Ensure all widgets are fully laid out
    self.root.update_idletasks()
    # Set focus to immediate entry
    self.immediate_entry.focus_force()

# Try setting focus after a delay to ensure window is fully realized
self.root.after(500, set_initial_focus)

The comments explain every step but don't explain WHY the 500ms delay is needed or what problem it solves. This level of detail suggests a workaround for a Tk timing issue but doesn't document the root cause.

---

#### code_vs_comment_conflict

**Description:** Comment about OPTION BASE validation contradicts defensive else clause

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _edit_array_element method around line 680:
Comment says: "OPTION BASE only allows 0 or 1 (validated by OPTION statement parser). The else clause is defensive programming for unexpected values."

Code has:
if array_base == 0:
    default_subscripts = ','.join(['0'] * len(dimensions))
elif array_base == 1:
    default_subscripts = ','.join(['1'] * len(dimensions))
else:
    # Defensive fallback for invalid array_base (should not occur)
    default_subscripts = ','.join(['0'] * len(dimensions))

If OPTION BASE truly only allows 0 or 1 and this is validated, the else clause should never execute. The comment acknowledges this but the defensive code remains, suggesting either: (1) validation isn't complete, (2) array_base could be modified elsewhere, or (3) the else clause is unnecessary.

---

#### code_vs_comment_conflict

**Description:** Comment about clearing yellow highlight contradicts when highlight is actually restored

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_mouse_click method around line 1310:
Comment says: "Clear yellow statement highlight when clicking (allows text selection to be visible). The highlight is restored when execution resumes or when stepping to the next statement."

This comment describes when the highlight is restored, but there's no code visible in this file that shows the restoration logic. The comment makes a claim about behavior that isn't implemented in the visible code, suggesting either: (1) the restoration happens elsewhere and should be referenced, or (2) the comment is describing intended behavior that isn't fully implemented.

---

#### code_vs_comment_conflict

**Description:** Comment about showing error list contradicts simplicity claim

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _validate_editor_syntax method around line 1260:
Comment says: "Only show full error list in output if there are multiple errors. For single errors, the red ? icon in the editor is sufficient feedback. This avoids cluttering the output pane with repetitive messages during editing. Note: We don't track 'first time' - this is intentionally simple."

The comment claims the approach is 'intentionally simple' and doesn't track 'first time', but then immediately implements conditional logic based on error count (len(errors_found) > 1). This is not particularly simple - it's a specific UX decision. The comment seems to be defending against a criticism that wasn't made, suggesting it may be outdated from a code review discussion.

---

#### code_vs_comment

**Description:** Comment describes keyboard shortcut behavior but doesn't mention all modifier key handling

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1055: 'Allow keyboard shortcuts with modifier keys (Control, Alt, etc.) to propagate'
Code checks: 'if event.state & 0x000C:  # Control or Alt pressed'
Comment says 'etc.' but code only checks Control (0x0004) and Alt (0x0008), not other modifiers like Command/Meta. Comment should be more precise about which modifiers are handled.

---

#### code_vs_comment

**Description:** Comment about CONT command validation doesn't mention all actual validation checks

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1550: 'Validation: Requires runtime exists and runtime.stopped is True. Invalid if program was edited after stopping.'
Code at line ~1558: 'if not self.runtime or not self.runtime.stopped:'
The comment mentions 'Invalid if program was edited after stopping' but there's no code checking for program edits. Either the validation is incomplete or the comment is outdated.

---

#### code_vs_comment

**Description:** Method name _add_immediate_output() is misleading - docstring admits it's historical and just forwards to _add_output()

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Method at line 1145:
def _add_immediate_output(self, text):
    """Add text to main output pane.

    This method name is historical - it simply forwards to _add_output().
    In the Tk UI, immediate mode output goes to the main output pane.
    Note: self.immediate_history exists but is always None (see __init__). Code
    that references it (e.g., _setup_immediate_context_menu) guards against None.
    """
    self._add_output(text)

The method name suggests it adds to immediate output, but it actually adds to main output. This is a naming inconsistency that could confuse maintainers.

---

#### code_vs_comment

**Description:** Dead code retained with comment explaining it's unused, creating maintenance burden

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Method _setup_immediate_context_menu() at line 1213:
"""Setup right-click context menu for immediate history widget.

NOTE: This method is currently unused - immediate_history is always None
in the Tk UI (see __init__). This is dead code retained for potential
future use if immediate mode gets its own output widget.
"""

Also references dead code in _copy_immediate_selection() and _select_all_immediate() methods. The comment acknowledges these are unused but they remain in the codebase.

---

#### code_vs_comment

**Description:** CLS behavior documented as design decision but may conflict with user expectations

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In TkIOHandler.clear_screen() method:
"""Clear screen - no-op for Tk UI.

Design decision: GUI output is persistent for review. Users can manually
clear output via Run > Clear Output menu if desired. CLS command is ignored
to preserve output history during program execution.
"""

This documents that CLS is intentionally ignored, but this may conflict with BASIC program expectations. Programs that use CLS for screen management will not work as expected. This should be documented in user-facing documentation, not just code comments.

---

#### code_vs_comment

**Description:** Comment in _on_cursor_move says 'Schedule deletion after current event processing' but doesn't explain the specific technical reasons

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment says:
"# Schedule deletion after current event processing to avoid interfering
# with ongoing key/mouse event handling (prevents cursor position issues,
# undo stack corruption, and widget state conflicts during event processing)"

This is actually accurate and well-documented. The after_idle() call does prevent these issues. This is NOT an inconsistency - the comment correctly explains the implementation.

---

#### documentation_inconsistency

**Description:** Class docstring says 'BASIC line numbers are part of the text content (not drawn separately in the canvas)' but _redraw() docstring repeats this with slightly different wording

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Class docstring: "Note: BASIC line numbers are part of the text content (not drawn separately in the canvas)."

_redraw() docstring: "Note: BASIC line numbers are parsed from text content (not drawn in canvas)."

Both say the same thing but with different phrasing ('separately in the canvas' vs 'in canvas'). Minor inconsistency in documentation style.

---

#### code_vs_comment

**Description:** _redraw() docstring references _parse_line_number() validation but doesn't mention the specific regex pattern

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
_redraw() docstring says:
"Note: BASIC line numbers are parsed from text content (not drawn in canvas).
See _parse_line_number() for the regex-based extraction logic that validates
line number format (requires whitespace or end-of-line after the number)."

This correctly describes what _parse_line_number() does, but the phrase 'end-of-line' is ambiguous (could mean newline character or end-of-string). The actual regex uses $ which is end-of-string, not \n which would be a newline character.

---

#### code_vs_comment

**Description:** Comment in serialize_variable() mentions explicit_type_suffix attribute behavior but implementation uses getattr with default

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment states: "Note: explicit_type_suffix is not always set (depends on parser implementation),
so getattr defaults to False if missing, preventing incorrect suffix output"

This comment is accurate and matches the code: getattr(var, 'explicit_type_suffix', False). However, it's placed after the conditional check, making it read like an explanation of potential issues rather than documenting the defensive programming pattern. The comment is correct but could be clearer about being documentation of the getattr pattern.

---

#### code_vs_documentation

**Description:** update_line_references() docstring describes 'Two-pass approach' but implementation uses single regex substitution pass

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring states: "Two-pass approach using different regex patterns:
Pattern 1: Match keyword + first line number (GOTO/GOSUB/THEN/ELSE/ON...GOTO/ON...GOSUB)
Pattern 2: Match comma-separated line numbers (for ON...GOTO/GOSUB lists)"

The implementation does use two regex patterns (pattern and comma_pattern), but they're applied sequentially in a single pass through the code, not in two separate passes. The term 'two-pass' typically implies processing the entire input twice. This is more accurately a 'two-pattern single-pass approach'.

---

#### code_vs_documentation

**Description:** renum_program() docstring describes callback responsibility but doesn't specify what 'in-place' means for immutable AST nodes

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring states: "renum_callback: Function(stmt: StatementNode, line_map: Dict[int, int]) -> None
that updates statement line number references in-place."

The term 'in-place' typically means modifying the object directly. However, if StatementNode objects have immutable line number fields, 'in-place' would mean modifying attributes of the node object, not replacing the node itself. The docstring should clarify whether the callback should:
1. Modify attributes of the stmt object (true in-place)
2. Return a new statement object (not in-place)
3. Modify child nodes of stmt (partially in-place)

The example reference to curses_ui.py suggests it's true in-place modification, but this should be explicit.

---

#### code_vs_documentation

**Description:** cycle_sort_mode() docstring mentions 'Tk UI implementation' but this is supposed to be UI-agnostic code

**Affected files:**
- `src/ui/variable_sorting.py`

**Details:**
Docstring states: "The cycle order is: accessed -> written -> read -> name -> (back to accessed)
This matches the Tk UI implementation."

The module docstring claims this is 'Common variable sorting logic for all UIs (Tk, Curses, Web)' and should be UI-agnostic. Referencing a specific UI implementation (Tk) in the docstring suggests this might be copied code or that the Tk UI is considered the canonical implementation. The docstring should either:
1. Remove the Tk reference and just document the cycle order
2. Explain that this cycle order was chosen to match existing Tk behavior for consistency

The current phrasing makes it unclear whether this is a design decision or an implementation detail.

---

#### Code vs Comment conflict

**Description:** The get_cursor_position() method docstring says it 'always returns line 0, column 0' and is a 'placeholder implementation', but the actual return statement uses dict keys as integers {0, 0} instead of the documented string keys 'line' and 'column'.

**Affected files:**
- `src/ui/web/codemirror5_editor.py`

**Details:**
Docstring says: 'Returns:\n            Dict with \'line\' and \'column\' keys (placeholder: always {0, 0})'
Comment in method says: '# This would need async support, for now return placeholder\n        return {\'line\': 0, \'column\': 0}'
The docstring describes the return format correctly, but uses confusing notation '{0, 0}' which looks like a set literal rather than a dict with string keys.

---

#### Documentation inconsistency

**Description:** The cmd_delete() and cmd_renum() docstrings reference 'curses_ui.py or tk_ui.py' as example implementations, but these files are not present in the provided source code, making the references unhelpful.

**Affected files:**
- `src/ui/visual.py`

**Details:**
cmd_delete() docstring: 'See curses_ui.py or tk_ui.py for example implementations.'
cmd_renum() docstring: 'See ui_helpers.renum_program() for the shared implementation logic.'
These references assume files exist that are not in the provided codebase.

---

#### Code vs Documentation inconsistency

**Description:** The cmd_cont() docstring references 'tk_ui.cmd_cont()' as an example implementation, but tk_ui.py is not in the provided source code.

**Affected files:**
- `src/ui/visual.py`

**Details:**
Docstring says: 'See tk_ui.cmd_cont() for example implementation.'
This reference cannot be followed as the file is not provided.

---

#### Code vs Comment conflict

**Description:** The _internal_change_handler comment says 'CodeMirror sends new value as args' but this is ambiguous - it's unclear if 'args' means e.args specifically or a general term for arguments.

**Affected files:**
- `src/ui/web/codemirror5_editor.py`

**Details:**
Comment: '# CodeMirror sends new value as args'
Code: 'self._value = e.args'
The comment could be clearer that it means the e.args attribute specifically, not just 'as arguments'.

---

#### code_vs_comment

**Description:** Comment references _enable_inline_input() method that is not visible in the provided code

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~70 references:
# by _enable_inline_input() in the NiceGUIBackend class.

This method is not shown in the provided code snippet (part 1), suggesting either:
1. The method exists in part 2 (not shown)
2. The comment is outdated and references a removed method
3. The method was renamed

---

#### code_vs_comment

**Description:** Comment says prompt display is handled by _get_input via _enable_inline_input, but implementation details not visible

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~62-64:
# Don't print prompt here - the input_callback (backend._get_input) handles
# prompt display via _enable_inline_input() method in the NiceGUIBackend class

The _get_input method is not shown in the provided code, so cannot verify if this is accurate.

---

#### documentation_inconsistency

**Description:** Inconsistent version number references - hardcoded '5.21' vs imported VERSION

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Multiple locations reference version numbers:
1. Line ~558: # Note: '5.21' is the MBASIC language version (intentionally hardcoded)
2. Line ~560: ui.label('MBASIC 5.21 Web IDE').classes('text-lg')
3. Line ~561: ui.label(f'{VERSION}').classes('text-md text-gray-600 mb-4')
4. Line ~1000: self.output_text = f'MBASIC 5.21 Web IDE - {VERSION}\n'
5. Line ~1063: ui.page_title('MBASIC 5.21 - Web IDE')

The comment clarifies '5.21' is the language version and VERSION is the implementation version, but this distinction is not consistently documented throughout the file.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of editor placeholder clearing

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In OpenFileDialog._open_file() at line ~467:
# Clear placeholder once content is loaded
if content:
    self.backend.editor_has_been_used = True
    self.backend.editor.props('placeholder=""')

However, editor_has_been_used is set but never initialized in __init__ (line ~976-1024). This suggests either:
1. Missing initialization
2. Attribute is set elsewhere
3. Code relies on Python's dynamic attribute creation

---

#### code_vs_comment

**Description:** Comment claims _on_editor_change method is 'defined later in this class', but the actual location is not visible in the provided code excerpt.

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~1680 states:
"# The _on_editor_change method handles:
# - Removing blank lines
# - Auto-numbering
# - Placeholder clearing
# (Note: Method defined later in this class - search for 'def _on_editor_change')"

This is informational and not necessarily an inconsistency, but if the method is not actually defined in the class, this would be misleading.

---

#### code_vs_comment

**Description:** Comment claims breakpoints are stored in runtime.breakpoints and can be 'plain integers' for legacy compatibility, but the implementation exclusively uses PC objects in _toggle_breakpoint.

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment in _update_breakpoint_display (around line 1570) states:
"# Note: self.runtime.breakpoints is a set that can contain:
#   - PC objects (statement-level breakpoints, created by _toggle_breakpoint)
#   - Plain integers (line-level breakpoints, legacy/compatibility)
# This implementation uses PC objects exclusively, but handles both for robustness."

However, examining _toggle_breakpoint and _do_toggle_breakpoint, all breakpoints are created as PC objects with stmt_offset. The code does handle both types in _update_breakpoint_display, but the comment suggests plain integers might be added elsewhere, which is not evident in the provided code.

---

#### documentation_inconsistency

**Description:** Multiple comments reference 'ASR33 teletype' behavior for continuous scrolling output, but this historical context may not be clear to modern developers and could benefit from additional explanation.

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comments at multiple locations reference 'ASR33 teletype' behavior:
- Line ~1845: "# Don't clear output - continuous scrolling like ASR33 teletype"
- Line ~2050: "# Note: Output is NOT cleared - continuous scrolling like ASR33 teletype"

While technically not an inconsistency, this historical reference may be unclear without additional context about why this design choice was made.

---

#### code_vs_comment

**Description:** Comment describes dual input mechanism but doesn't explain why both are needed or when each is used

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _handle_output_enter() method:

Comment says:
"Provide input to interpreter via TWO mechanisms (both may be needed depending on code path):
1. interpreter.provide_input() - Used when interpreter is waiting synchronously
   (checked via interpreter.state.input_prompt). Stores input for retrieval.
2. input_future.set_result() - Used when async code is waiting via asyncio.Future
   (see _get_input_async method). Only one path is active at a time, but we
   attempt both to ensure the waiting code receives input regardless of which path it used."

The comment claims "only one path is active at a time" but then says "we attempt both" - this is contradictory. If only one is active, why attempt both? The comment should clarify the actual execution flow or race condition being handled.

---

#### code_vs_comment

**Description:** Comment describes auto-numbering behavior that may not match implementation

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _check_auto_number() method:

Comment says:
"Auto-numbers a line at most once per content state - tracks last snapshot to avoid
re-numbering lines while user is typing. However, if content changes significantly
(e.g., line edited after numbering, then un-numbered again), the line could be
re-numbered by this logic."

The comment describes a complex state tracking mechanism, but the actual code only checks:
- if i < len(old_lines) or len(lines) > len(old_lines)
- if not re.match(r'^\s*\d+', old_line)

This doesn't implement the "at most once per content state" guarantee described. The comment may be describing intended behavior rather than actual implementation.

---

#### code_vs_comment

**Description:** Comment about blank line preservation heuristic may not accurately describe behavior

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _remove_blank_lines() method:

Comment says:
"Remove blank lines from editor except the last line.

The last line is preserved even if blank to avoid removing it while the user
is actively typing on it. This is a heuristic that works well in practice but
may preserve some blank lines if the user edits earlier in the document."

The code preserves the last line unconditionally (if line.strip() or i == len(lines) - 1), but the comment's claim about "may preserve some blank lines if the user edits earlier" doesn't match the implementation - only the LAST line is preserved, not lines "earlier in the document".

---

#### code_vs_comment

**Description:** Comment describes _get_input behavior that relies on interpreter state transitions not shown in code

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _get_input() method:

Comment says:
"Return empty string - signals interpreter to transition to 'waiting_for_input'
state (state transition happens in interpreter when it receives empty string
from input()). Execution pauses until _submit_input() calls provide_input()."

The comment references _submit_input() method which doesn't exist in this file - the actual method is _handle_output_enter(). Also, the comment describes interpreter state transitions that aren't visible in this code, making it unclear if the described behavior is actually implemented.

---

#### code_vs_comment

**Description:** Comment about sys.stderr.write usage doesn't match actual error handling pattern

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _sync_program_from_editor() method:

Comment says:
"Using sys.stderr.write directly (not log_web_error) to avoid dependency on logging
infrastructure during critical serialization path."

However, throughout the rest of the file, log_web_error is used extensively in exception handlers, including in other serialization-related methods like _serialize_runtime(). The comment suggests a special case for this method, but it's unclear why this particular error path needs to avoid the logging infrastructure when others don't.

---

#### code_vs_comment

**Description:** Docstring for stop() method says 'disconnecting all clients' but app.shutdown() behavior is not verified in code

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Docstring: 'Stop the web UI server and shut down NiceGUI app.

Calls app.shutdown() to terminate the NiceGUI application,
disconnecting all clients and stopping the web server.'

Code: app.shutdown()

The docstring makes specific claims about disconnecting clients, but there's no verification that app.shutdown() actually does this. This could be accurate or could be an assumption.

---

#### documentation_inconsistency

**Description:** Comment about Redis storage mentions 'load-balanced instances' but no documentation about actual load balancing setup

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Lines ~481-488 mention:
'Session state will be shared across load-balanced instances'
and
'Set NICEGUI_REDIS_URL to enable Redis storage for load balancing'

But there's no documentation about:
- How to actually set up load balancing
- What load balancer to use
- Whether NiceGUI supports this natively
- Any caveats or requirements

This could mislead users into thinking Redis alone enables load balancing.

---

#### code_vs_comment

**Description:** Comment says 'Create default DEF type map (all SINGLE precision)' but this is creating a new map each time, not using a default

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~447: '# Create default DEF type map (all SINGLE precision)'

Code creates a new dict:
def_type_map = {}
for letter in 'abcdefghijklmnopqrstuvwxyz':
    def_type_map[letter] = TypeInfo.SINGLE

The word 'default' is misleading - this is creating a fresh type map, not using a pre-existing default. Better wording would be 'Create DEF type map with all letters as SINGLE precision' or 'Initialize DEF type map'.

---

#### documentation_inconsistency

**Description:** Debugging documentation mentions Ctrl+T for Step but web_keybindings.json doesn't define this shortcut

**Affected files:**
- `docs/help/common/debugging.md`
- `src/ui/web_keybindings.json`

**Details:**
debugging.md states: 'Shortcuts: Tk/Curses/Web: Ctrl+T or Step button'

But web_keybindings.json defines:
- 'step': {'keys': ['F10'], 'primary': 'F10', 'description': 'Step to next line'}
- No Ctrl+T binding is present

Also, web_keybindings.json shows 'continue' uses F5, but 'run' also uses F5, which could be confusing.

---

#### documentation_inconsistency

**Description:** editor-commands.md says shortcuts vary by UI and refers to UI-specific help, but debugging.md gives specific shortcuts like Ctrl+T, Ctrl+G, Ctrl+Q

**Affected files:**
- `docs/help/common/editor-commands.md`
- `docs/help/common/debugging.md`

**Details:**
editor-commands.md states: 'Important: Keyboard shortcuts vary by UI. See your UI-specific help for the exact keybindings' and 'Each UI uses different keys due to platform constraints (e.g., Curses can't use Ctrl+S for save as it's used for terminal flow control).'

But debugging.md gives specific shortcuts:
- 'Press Ctrl+T or click Step to advance one statement'
- 'Press Ctrl+G or click Continue to run to next breakpoint'
- 'Press Ctrl+Q or click Stop to halt execution'

This creates confusion about whether these shortcuts are universal or UI-specific.

---

#### code_comment_conflict

**Description:** Comment says 'Legacy class kept for compatibility' but the class is marked _DEPRECATED in the name, suggesting it should not be used at all

**Affected files:**
- `src/ui/web_help_launcher.py`

**Details:**
Class definition: 'class WebHelpLauncher_DEPRECATED:'
Docstring: 'Legacy class wrapper for compatibility.'
Comment above class: 'Legacy class kept for compatibility - new code should use direct web URL instead'

The _DEPRECATED suffix suggests the class should not be used, but 'kept for compatibility' suggests it's still supported. The migration guide implies all code should migrate away from it.

---

#### code_vs_documentation

**Description:** Version documentation says MBASIC 5.21 but version.py shows VERSION = '1.0.772' which is the project version, not the MBASIC version

**Affected files:**
- `src/version.py`
- `docs/help/common/getting-started.md`

**Details:**
version.py defines:
VERSION = '1.0.772'  # Project version
MBASIC_VERSION = '5.21'  # The MBASIC version we implement

getting-started.md states: 'MBASIC 5.21 is compatible with MBASIC from the 1980s.'

This is technically correct but could be clearer. The project version (1.0.772) vs MBASIC compatibility version (5.21) distinction should be documented.

---

#### documentation_inconsistency

**Description:** loops.md uses WEND statement but getting-started.md doesn't mention WHILE-WEND loops in basic concepts

**Affected files:**
- `docs/help/common/examples/loops.md`
- `docs/help/common/getting-started.md`

**Details:**
loops.md has extensive WHILE-WEND examples:
'10 WHILE SUM < 100
40   SUM = SUM + COUNT
60 WEND'

But getting-started.md only shows FOR-NEXT loops in the 'Program Flow' section:
'10 FOR I = 1 TO 10
20   PRINT I
30 NEXT I'

WHILE-WEND is a fundamental loop construct and should be mentioned in getting-started.md alongside FOR-NEXT.

---

#### documentation_inconsistency

**Description:** Inconsistent notation for mathematical constants between data-types.md and math-functions.md

**Affected files:**
- `docs/help/common/language/data-types.md`
- `docs/help/common/language/appendices/math-functions.md`

**Details:**
In data-types.md under 'Exponent Notation':
- Uses 'D notation (e.g., 1.5D+10)' and 'E notation (e.g., 1.5E+10)'

In math-functions.md under 'Constants':
- Shows PI# = 3.141592653589793 and E# = 2.718281828459045
- But doesn't show examples using D or E notation for these constants

The math-functions.md should demonstrate D/E notation usage for consistency with data-types.md teaching.

---

#### documentation_inconsistency

**Description:** Error code reference inconsistency - CVI/CVS/CVD mentions error code 'FC' but error-codes.md uses code '5' for Illegal function call

**Affected files:**
- `docs/help/common/language/appendices/error-codes.md`
- `docs/help/common/language/functions/cvi-cvs-cvd.md`

**Details:**
In cvi-cvs-cvd.md: "**Error:** Raises 'Illegal function call' (error code FC)"

In error-codes.md: "| **FC** | 5 | Illegal function call | ..."

Both 'FC' and '5' are shown in error-codes.md, but the cvi-cvs-cvd.md only mentions 'FC' without the numeric code. For consistency, both should be mentioned or a standard format should be used.

---

#### documentation_inconsistency

**Description:** character-set.md references character-set.md in its own 'See Also' section

**Affected files:**
- `docs/help/common/language/character-set.md`
- `docs/help/common/language/appendices/ascii-codes.md`

**Details:**
In character-set.md 'See Also' section:
- [Character Set](../character-set.md) - BASIC-80 character set overview

This is a self-reference that should probably point to ascii-codes.md or be removed.

---

#### documentation_inconsistency

**Description:** ascii-codes.md 'See Also' section has circular reference to character-set.md

**Affected files:**
- `docs/help/common/language/appendices/ascii-codes.md`

**Details:**
In ascii-codes.md 'See Also':
- [Character Set](../character-set.md) - BASIC-80 character set overview

And in character-set.md 'See Also':
- [ASCII Codes](appendices/ascii-codes.md) - Complete ASCII table

While cross-references are useful, the relationship should be clarified (one is overview, one is detailed reference).

---

#### documentation_inconsistency

**Description:** FRE documentation has inconsistent 'See Also' references mixing statements and functions

**Affected files:**
- `docs/help/common/language/functions/fre.md`

**Details:**
In fre.md 'See Also' section includes:
- [HELP SET](../statements/helpsetting.md)
- [LIMITS](../statements/limits.md)
- [NULL](../statements/null.md)
- [RANDOMIZE](../statements/randomize.md)
- [REM](../statements/rem.md)
- [SET (setting)](../statements/setsetting.md)
- [SHOW SETTINGS](../statements/showsettings.md)
- [TRON/TROFF](../statements/tron-troff.md)
- [WIDTH](../statements/width.md)

Mixed with functions like INP, PEEK, INKEY$, USR, VARPTR. The grouping seems arbitrary and some references (like HELP SET, SET, SHOW SETTINGS) may not be standard MBASIC-80 commands.

---

#### documentation_inconsistency

**Description:** HEX$ function description mismatch between index and detail page

**Affected files:**
- `docs/help/common/language/functions/index.md`
- `docs/help/common/language/functions/hex_dollar.md`

**Details:**
Index page says 'Number to hexadecimal' but detail page says 'Returns a string which represents the hexadecimal value of the decimal argument'. Both are correct but inconsistent in style - index uses brief descriptions while detail uses full sentences.

---

#### documentation_inconsistency

**Description:** OCT$ function description mismatch between index and detail page

**Affected files:**
- `docs/help/common/language/functions/index.md`
- `docs/help/common/language/functions/oct_dollar.md`

**Details:**
Index page says 'Number to octal' but detail page says 'Returns a string which represents the octal value of the decimal argument'. Both are correct but inconsistent in style.

---

#### documentation_inconsistency

**Description:** Cross-reference descriptions are inconsistent

**Affected files:**
- `docs/help/common/language/functions/lof.md`
- `docs/help/common/language/functions/loc.md`

**Details:**
In LOF.md See Also section: 'LOC - Returns current file POSITION/record number (LOF returns total SIZE in bytes)'
In LOC.md See Also section: 'LOF - Returns the total file SIZE in bytes (LOC returns current POSITION/record number)'
Both say the same thing but with different emphasis/capitalization.

---

#### documentation_inconsistency

**Description:** Inconsistent example formatting

**Affected files:**
- `docs/help/common/language/functions/hex_dollar.md`
- `docs/help/common/language/functions/oct_dollar.md`

**Details:**
HEX$.md shows two separate examples with 'RUN' commands:
'10 INPUT X
20 A$ = HEX$(X)
30 PRINT X; "DECIMAL IS "; A$; " HEXADECIMAL"
RUN
? 32
32 DECIMAL IS 20 HEXADECIMAL
Ok

10 PRINT HEX$(255)
RUN
FF
Ok'

OCT$.md shows similar examples but with slightly different formatting and comments. Both should follow the same style.

---

#### documentation_inconsistency

**Description:** Inconsistent error message formatting

**Affected files:**
- `docs/help/common/language/functions/instr.md`

**Details:**
INSTR.md note says: 'Note: If I=0 is specified, an "Illegal function call" error will occur.'
MID$.md note says: 'Note: If I=0 is specified, an "Illegal function call" error will occur.'
Both use quotes around the error message, but other documentation files may format error messages differently.

---

#### documentation_inconsistency

**Description:** SPACE$ description mentions STRING$ equivalence but STRING$ doesn't mention SPACE$

**Affected files:**
- `docs/help/common/language/functions/space_dollar.md`
- `docs/help/common/language/functions/string_dollar.md`

**Details:**
SPACE$.md says: 'This is equivalent to STRING$(I, 32) since 32 is the ASCII code for a space character.'
But STRING$.md doesn't mention that SPACE$ is a special case. Cross-references should be bidirectional.

---

#### documentation_inconsistency

**Description:** Inconsistent 'See Also' section ordering

**Affected files:**
- `docs/help/common/language/functions/int.md`
- `docs/help/common/language/functions/sin.md`

**Details:**
INT.md lists functions in one order (ABS, ATN, CDBL, CINT, COS, CSNG, EXP, FIX, LOG, RND, SGN, SIN, SQR, TAN) while SIN.md lists them in a different order (ABS, ATN, COS, EXP, FIX, INT, LOG, RND, SGN, SQR, TAN). The 'See Also' sections should follow a consistent ordering (alphabetical or by category).

---

#### documentation_inconsistency

**Description:** PEEK documentation has conflicting statements about POKE relationship

**Affected files:**
- `docs/help/common/language/functions/peek.md`

**Details:**
PEEK.md states in the implementation note: 'Important Limitations: **PEEK does NOT return values written by POKE** (POKE is a no-op that does nothing)'

But later in the Description section it says: 'PEEK is traditionally the complementary function to the POKE statement. However, in this implementation, PEEK returns random values and POKE is a no-op, so they are not functionally related.'

The second statement is more accurate and complete. The implementation note should be consistent with the description.

---

#### documentation_inconsistency

**Description:** Inconsistent 'See Also' references - TAB references READ and DATA, VAL does not reference TAB despite using it in example

**Affected files:**
- `docs/help/common/language/functions/tab.md`
- `docs/help/common/language/functions/val.md`

**Details:**
TAB.md example uses READ/DATA and lists them in 'See Also':
```basic
10 PRINT "NAME" TAB(25) "AMOUNT": PRINT
20 READ A$, B$
30 PRINT A$ TAB(25) B$
40 DATA "G. T. JONES", "$25.00"
```

VAL.md example uses TAB but doesn't reference it:
```basic
10 READ NAME$, CITY$, STATE$, ZIP$
20 IF VAL(ZIP$) < 90000 OR VAL(ZIP$) > 96699 THEN PRINT NAME$; TAB(25); "OUT OF STATE"
30 IF VAL(ZIP$) >= 90801 AND VAL(ZIP$) <= 90815 THEN PRINT NAME$; TAB(25); "LONG BEACH"
```
VAL.md 'See Also' includes SPC but not TAB, despite TAB being used in the example.

---

#### documentation_inconsistency

**Description:** DEF FN documentation describes extended multi-character function names as an extension but doesn't clearly mark compatibility implications

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`

**Details:**
DEF FN.md states:

"**Original MBASIC 5.21**: Function names were limited to a single character after FN:
- ✓ `FNA` - single character
- ✓ `FNB$` - single character with type suffix

**This implementation (extension)**: Function names can be multiple characters:
- ✓ `FNA` - single character (compatible with original)
- ✓ `FNABC` - multiple characters"

This is an extension beyond original MBASIC 5.21 behavior, but the documentation doesn't clearly indicate this could cause compatibility issues with original MBASIC programs that might have used 'FNABC' as separate tokens.

---

#### documentation_inconsistency

**Description:** CHAIN and COMMON documentation have slightly different descriptions of variable passing behavior

**Affected files:**
- `docs/help/common/language/statements/chain.md`
- `docs/help/common/language/statements/common.md`

**Details:**
CHAIN.md states:
"Variables are only passed to the chained program if they are declared in a COMMON statement. Without ALL, only COMMON variables are passed. With ALL, all variables are passed."

COMMON.md states:
"If all variables are to be passed, use CHAIN with the ALL option and omit the COMMON statement."

This creates ambiguity: Does CHAIN...ALL require COMMON statements or not? CHAIN.md says "With ALL, all variables are passed" (implying COMMON not needed), while COMMON.md says "omit the COMMON statement" (confirming COMMON not needed with ALL). The wording should be consistent.

---

#### documentation_inconsistency

**Description:** CONT documentation references non-existent example in Section 2.61

**Affected files:**
- `docs/help/common/language/statements/cont.md`

**Details:**
CONT.md Example section states:
```basic
See example Section 2.61, STOP.
```

This appears to be a reference to the original MBASIC manual's section numbering, which doesn't exist in this documentation structure. The reference should either be updated to point to the actual STOP.md file or the example should be included directly.

---

#### documentation_inconsistency

**Description:** DEF USR documentation references non-existent Appendix C

**Affected files:**
- `docs/help/common/language/statements/def-usr.md`

**Details:**
DEF USR.md states:
"See Appendix C, Assembly Language Subroutines, in the original MBASIC documentation for details on writing assembly language routines."

This appendix doesn't exist in the current documentation structure. Since DEF USR is not implemented, this reference should either be removed or updated to indicate it's from the original manual.

---

#### documentation_inconsistency

**Description:** Inconsistent implementation status descriptions for machine code features

**Affected files:**
- `docs/help/common/language/functions/usr.md`
- `docs/help/common/language/functions/varptr.md`
- `docs/help/common/language/statements/call.md`
- `docs/help/common/language/statements/def-usr.md`

**Details:**
Different wording is used across files for similar 'not implemented' features:

USR.md: "**Behavior**: Always returns 0"
VARPTR.md: "**Behavior**: Function is not available (runtime error when called)"
CALL.md: "**Behavior**: Statement is parsed but no operation is performed"
DEF USR.md: "**Behavior**: Statement is parsed but no operation is performed"

These should use consistent language to describe what happens when these features are used.

---

#### documentation_inconsistency

**Description:** DATA documentation example output doesn't match the code

**Affected files:**
- `docs/help/common/language/statements/data.md`

**Details:**
DATA.md shows this example:
```basic
10 DATA 12, 3.14159, "Hello", WORLD
20 DATA "Smith, John", 100, -5.5
30 READ A, B, C$, D$
40 PRINT A; B; C$; D$
50 READ NAME$, SCORE, ADJUSTMENT
60 PRINT NAME$, SCORE, ADJUSTMENT
```

Output:
```
 12  3.14159 Hello WORLD
Smith, John    100  -5.5
```

The output format suggests PRINT with semicolons produces spaces between values, and PRINT with commas produces tab-separated values. However, the spacing in the output doesn't clearly show this distinction, particularly the second line which should show tab-separated output but appears to have irregular spacing.

---

#### documentation_inconsistency

**Description:** Inconsistent cross-reference formatting in See Also sections

**Affected files:**
- `docs/help/common/language/statements/delete.md`
- `docs/help/common/language/statements/edit.md`
- `docs/help/common/language/statements/list.md`

**Details:**
delete.md uses: [RENUM](renum.md) - Renumber program lines and update line references
edit.md uses: [RENUM](renum.md) - Renumber program lines and update line references
list.md uses: [RENUM](renum.md) - Renumber program lines and update line references

All three files reference RENUM consistently, but the formatting style varies across other statements. Some use full descriptions, others use brief ones.

---

#### documentation_inconsistency

**Description:** Incomplete cross-reference list

**Affected files:**
- `docs/help/common/language/statements/field.md`

**Details:**
field.md See Also section lists:
- OPEN, LSET, RSET, GET, PUT, MKI$/MKS$/MKD$, CVI/CVS/CVD, CLOSE

But does not reference LOC or LOF functions which are commonly used with random files and are referenced in get.md's See Also section. This creates an inconsistent cross-reference network.

---

#### documentation_inconsistency

**Description:** Incomplete syntax description

**Affected files:**
- `docs/help/common/language/statements/get.md`

**Details:**
get.md syntax shows: GET [#]<file number>[,<record number>]

But the remarks state: "If <record number> is omitted, the next record (after the last GET) is read into the buffer."

The syntax should clarify that record number is optional by showing it in square brackets, which it does. However, the example only shows GET with a record number. An example showing GET without a record number (sequential reading) would be helpful for completeness.

---

#### documentation_inconsistency

**Description:** Duplicate note about CP/M extension behavior

**Affected files:**
- `docs/help/common/language/statements/kill.md`

**Details:**
kill.md contains the same note as files.md: "Note: CP/M automatically adds .BAS extension if none is specified when deleting BASIC program files."

This creates maintenance burden and potential for inconsistency. The note appears in multiple files (files.md, kill.md) and should either be centralized in a common reference or consistently applied across all file-related commands (LOAD, SAVE, MERGE, etc.).

---

#### documentation_inconsistency

**Description:** Incomplete Remarks section

**Affected files:**
- `docs/help/common/language/statements/list.md`

**Details:**
list.md has an empty Remarks section:
"## Remarks


## Example"

This should either contain remarks about LIST behavior (like LLIST does) or be removed if there are no special remarks to make.

---

#### documentation_inconsistency

**Description:** Inconsistent cross-reference lists in See Also sections

**Affected files:**
- `docs/help/common/language/statements/llist.md`
- `docs/help/common/language/statements/renum.md`

**Details:**
llist.md See Also includes: AUTO, DELETE, EDIT, LIST, RENUM
renum.md See Also includes: AUTO, DELETE, EDIT, LIST, LLIST

Both documents reference each other and share the same category (editing), but the cross-reference is symmetric. This is actually consistent, but worth noting that LLIST is marked as not implemented while still being cross-referenced.

---

#### documentation_inconsistency

**Description:** LPRINT documentation references PRINT USING but PRINT documentation doesn't fully document PRINT USING

**Affected files:**
- `docs/help/common/language/statements/lprint-lprint-using.md`
- `docs/help/common/language/statements/print.md`

**Details:**
lprint-lprint-using.md states: "LPRINT USING works exactly like PRINT USING except output goes to the line printer."

However, print.md only briefly mentions PRINT USING in the See Also section as "PRINT USING - Formatted output to the screen" but doesn't provide full documentation of the USING syntax in the main PRINT document. The LPRINT doc shows example syntax like "LPRINT USING "##: $$###.##"; ITEM, PRICE" but this format string syntax is not explained in the PRINT documentation.

---

#### documentation_inconsistency

**Description:** NEW documentation lacks detail compared to similar commands

**Affected files:**
- `docs/help/common/language/statements/new.md`
- `docs/help/common/language/statements/load.md`

**Details:**
new.md has an empty Remarks section and minimal documentation: "To delete the program currently in memory and clear all variables."

load.md provides detailed remarks about file handling: "LOAD (without ,R): Closes all open files and deletes all variables and program lines currently in memory before loading"

NEW performs similar operations (deleting program and clearing variables) but doesn't document whether it closes open files. Given that LOAD closes files, it's likely NEW does too, but this is not documented.

---

#### documentation_inconsistency

**Description:** NULL references obsolete hardware but LPRINT also references obsolete hardware with different implementation notes

**Affected files:**
- `docs/help/common/language/statements/null.md`
- `docs/help/common/language/statements/lprint-lprint-using.md`

**Details:**
null.md describes NULL for tape punches and teletypes without an implementation warning.

lprint-lprint-using.md has a prominent implementation note: "⚠️ **Not Implemented**: This feature requires line printer hardware and is not implemented in this Python-based interpreter."

Both reference obsolete hardware (tape punches/teletypes vs line printers), but only LPRINT has the implementation warning. NULL should probably also have a similar warning since tape punches and 10-character-per-second devices are equally obsolete.

---

#### documentation_inconsistency

**Description:** Array documentation doesn't cross-reference OPTION BASE

**Affected files:**
- `docs/help/common/language/statements/option-base.md`
- `docs/help/common/language/statements/read.md`

**Details:**
read.md states: "Variables in the list may be subscripted. Array elements must be dimensioned before being referenced in a READ statement."

However, it doesn't mention OPTION BASE in the See Also section, even though OPTION BASE affects array subscripting. option-base.md only references DIM and ERASE in its See Also section.

While not strictly an error, array-related documentation could benefit from consistent cross-referencing of OPTION BASE.

---

#### documentation_inconsistency

**Description:** Inconsistent implementation note formatting

**Affected files:**
- `docs/help/common/language/statements/out.md`
- `docs/help/common/language/statements/poke.md`

**Details:**
out.md states: "⚠️ **Emulated as No-Op**: This feature requires direct hardware I/O port access and is not implemented in this Python-based interpreter."

poke.md states: "⚠️ **Emulated as No-Op**: This feature requires direct memory access and cannot be implemented in a Python-based interpreter."

The wording differs slightly: "is not implemented" vs "cannot be implemented". While both convey similar meaning, consistency in implementation notes would be better.

---

#### documentation_inconsistency

**Description:** Print zone width inconsistency

**Affected files:**
- `docs/help/common/language/statements/print.md`
- `docs/help/common/language/statements/printi-printi-using.md`

**Details:**
print.md states: "When items are separated by commas, values are printed in zones of 14 columns each: Columns 1-14 (first zone), Columns 15-28 (second zone)..."

printi-printi-using.md states: "Items separated by commas are printed in print zones" but doesn't specify the zone width.

While PRINT# likely uses the same 14-column zones as PRINT, this is not explicitly documented, creating potential ambiguity.

---

#### documentation_inconsistency

**Description:** PUT documentation mentions PRINT# for random files but LSET doesn't

**Affected files:**
- `docs/help/common/language/statements/put.md`
- `docs/help/common/language/statements/lset.md`

**Details:**
put.md Note section states: "PRINT#, PRINT# USING, and WRITE# may be used to put characters in the random file buffer before a PUT statement."

lset.md states: "LSET is used with random access files to prepare data for writing with PUT" but doesn't mention that PRINT# can also be used.

This creates an incomplete picture in LSET documentation about alternative ways to prepare random file data.

---

#### documentation_inconsistency

**Description:** Inconsistent example output formatting

**Affected files:**
- `docs/help/common/language/statements/randomize.md`
- `docs/help/common/language/statements/read.md`

**Details:**
randomize.md shows example output with "Ok" prompt:
"RUN
Random Number Seed (-32768 to 32767)? 3
.88598 .484668 .586328 .119426 .709225
Ok"

read.md shows example output without "Ok" prompt:
"Output:
Student 100 John scored 85.5
Student 200 Mary scored 92.3"

Inconsistent formatting of example outputs across documentation makes it harder to understand what is actual program output vs interpreter prompts.

---

#### documentation_inconsistency

**Description:** Similar command names (RESTORE vs RESUME) with different purposes not cross-referenced

**Affected files:**
- `docs/help/common/language/statements/restore.md`
- `docs/help/common/language/statements/resume.md`

**Details:**
restore.md is about resetting DATA pointers for READ statements.
resume.md is about continuing execution after error handling.

These commands have similar names but completely different purposes. Neither document cross-references the other or includes a note warning about the name similarity, which could help prevent user confusion.

While not strictly required, a note like "Note: Do not confuse RESTORE with RESUME (error handling)" would be helpful.

---

#### documentation_inconsistency

**Description:** Different levels of detail in error handling documentation

**Affected files:**
- `docs/help/common/language/statements/resume.md`
- `docs/help/common/language/statements/on-error-goto.md`

**Details:**
resume.md provides extensive examples with 5 detailed scenarios, error code reference table, and testing notes: "Verified behavior against real MBASIC 5.21"

on-error-goto.md provides minimal example with basic error handling.

While RESUME is more complex and warrants more examples, the disparity in documentation depth is notable. The error code table in RESUME would be useful in ON ERROR GOTO as well.

---

#### documentation_inconsistency

**Description:** Inconsistent 'Versions' field values

**Affected files:**
- `docs/help/common/language/statements/rset.md`
- `docs/help/common/language/statements/swap.md`

**Details:**
rset.md shows 'Versions: Disk' while swap.md shows 'Versions: Extended, Disk'. Need to verify if RSET is available in Extended BASIC or only Disk BASIC.

---

#### documentation_inconsistency

**Description:** Inconsistent file extension documentation

**Affected files:**
- `docs/help/common/language/statements/save.md`
- `docs/help/common/language/statements/run.md`

**Details:**
save.md states '(With CP/M, the default extension .BAS is supplied.)' while run.md states 'File extension defaults to .BAS if not specified'. The phrasing should be consistent - either both mention CP/M or both use generic language.

---

#### documentation_inconsistency

**Description:** Inconsistent description of file closing behavior

**Affected files:**
- `docs/help/common/language/statements/stop.md`
- `docs/help/common/language/statements/system.md`

**Details:**
stop.md states 'Unlike the END statement, the STOP statement does not close files.' system.md states 'When SYSTEM is executed: All open files are closed'. However, the 'See Also' sections are inconsistent - stop.md references CHAIN, CLEAR, COMMON which are not directly related to file closing, while system.md has the same references. The relationship between these commands and file handling should be clarified consistently.

---

#### documentation_inconsistency

**Description:** Missing version information

**Affected files:**
- `docs/help/common/language/statements/tron-troff.md`

**Details:**
tron-troff.md does not include a 'Versions:' field in the frontmatter, unlike most other statement documentation files. Should specify which BASIC versions support TRON/TROFF.

---

#### documentation_inconsistency

**Description:** Inconsistent title formatting for WRITE statements

**Affected files:**
- `docs/help/common/language/statements/write.md`
- `docs/help/common/language/statements/writei.md`

**Details:**
write.md uses title 'WRITE (Screen)' while writei.md uses title 'WRITE# (File)'. The parenthetical descriptions are helpful but the formatting should be consistent. Consider using 'WRITE (Screen)' and 'WRITE# (File)' or 'WRITE - Screen' and 'WRITE# - File'.

---

#### documentation_inconsistency

**Description:** SETSETTING and SHOWSETTINGS reference HELPSETTING but no such doc exists

**Affected files:**
- `docs/help/common/language/statements/setsetting.md`
- `docs/help/common/language/statements/showsettings.md`

**Details:**
Both setsetting.md and showsettings.md list 'helpsetting' in their 'related' frontmatter field and reference it in 'See Also' sections. However, there is no helpsetting.md file in the documentation. Either the file is missing or the references should be removed.

---

#### documentation_inconsistency

**Description:** RUN documentation has inconsistent syntax description

**Affected files:**
- `docs/help/common/language/statements/run.md`

**Details:**
The Syntax section shows:
```basic
RUN [line number]
RUN "filename"
```
But the Remarks section describes three forms:
- RUN (no arguments)
- RUN line-number
- RUN "filename"

The syntax section should include all three forms explicitly:
```basic
RUN
RUN [line number]
RUN "filename"
```

---

#### documentation_inconsistency

**Description:** Curses editing documentation references undefined keyboard shortcuts

**Affected files:**
- `docs/help/common/ui/curses/editing.md`

**Details:**
The document uses placeholders like {{kbd:run:curses}}, {{kbd:parse:curses}}, {{kbd:new:curses}}, {{kbd:save:curses}}, {{kbd:continue:curses}} but states 'See your UI's keyboard shortcuts documentation for the complete list.' without providing a specific link. Should link to the actual curses keyboard shortcuts documentation.

---

#### documentation_inconsistency

**Description:** Inconsistent description of Web UI file uppercasing behavior

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/extensions.md`

**Details:**
compatibility.md states:
- Automatically uppercased by the virtual filesystem (CP/M style)
- The uppercasing is a programmatic transformation for CP/M compatibility, not evidence of persistent storage

This detailed explanation is missing from extensions.md, which only mentions 'simple filenames only' without explaining the uppercasing behavior.

---

#### documentation_inconsistency

**Description:** Incomplete keyboard shortcut table with template variables not rendered

**Affected files:**
- `docs/help/common/ui/tk/index.md`

**Details:**
The keyboard shortcuts table contains unrendered template variables:
| **{{kbd:file_new:tk}}** | New program |
| **{{kbd:file_open:tk}}** | Open file |
| **{{kbd:file_save:tk}}** | Save file |
| **{{kbd:run_program:tk}}** | Run program |
| **{{kbd:find:tk}}** | Find |

These should be replaced with actual keyboard shortcuts (e.g., Ctrl+N, Ctrl+O, etc.) or the template system should be documented.

---

#### documentation_inconsistency

**Description:** Menu item documentation contains unrendered template variable

**Affected files:**
- `docs/help/common/ui/tk/index.md`

**Details:**
In the Edit Menu section:
- **Select All** (Ctrl+A) - Select all text

This is the only shortcut with an actual key combination shown, while all others use template variables like {{kbd:cut:tk}}. This inconsistency suggests incomplete template rendering or documentation.

---

#### documentation_inconsistency

**Description:** LPRINT statement behavior unclear in features list

**Affected files:**
- `docs/help/mbasic/features.md`

**Details:**
features.md states:
- **LPRINT** - Line printer output (Note: Statement is parsed but produces no output - see [LPRINT](../common/language/statements/lprint-lprint-using.md) for details)

This note suggests LPRINT is a no-op, but it's listed under 'Console I/O' features as if it's functional. This should be clarified or moved to a 'Compatibility Stubs' section.

---

#### documentation_inconsistency

**Description:** Inconsistent command prompt representation

**Affected files:**
- `docs/help/mbasic/getting-started.md`
- `docs/help/ui/cli/index.md`

**Details:**
getting-started.md shows the MBASIC prompt as 'Ok' in examples:
```
10 PRINT "Hello, World!"
20 END
RUN
```

But cli/index.md shows it as 'Ok' with different formatting:
```
Ok
LOAD "MYPROGRAM.BAS"
RUN
```

The actual prompt format should be consistent across documentation.

---

#### documentation_inconsistency

**Description:** Self-contradictory statement about LINE command

**Affected files:**
- `docs/help/mbasic/not-implemented.md`

**Details:**
The document states: 'LINE - Draw line (GW-BASIC graphics version - not the LINE INPUT statement which IS implemented)'

This is confusing because it says LINE is not implemented, but then clarifies that LINE INPUT is implemented. The phrasing could be clearer that there are two different commands: LINE (graphics, not implemented) and LINE INPUT (file I/O, implemented).

---

#### documentation_inconsistency

**Description:** Document describes CP/M MBASIC implementation but unclear if this applies to the Python implementation

**Affected files:**
- `docs/help/mbasic/implementation/string-allocation-and-garbage-collection.md`

**Details:**
The string-allocation-and-garbage-collection.md document provides extensive detail about 'CP/M era Microsoft BASIC-80 (MBASIC)' and 'Intel 8080 assembly implementation'. However, the getting-started.md describes this project as 'a complete Python implementation of MBASIC-80'.

It's unclear whether:
1. The Python implementation replicates the exact O(n²) garbage collection algorithm
2. This is historical documentation only
3. The Python implementation uses modern garbage collection

The document should clarify its relevance to the current Python implementation.

---

#### documentation_inconsistency

**Description:** Placeholder documentation file that should be completed or removed

**Affected files:**
- `docs/help/ui/common/running.md`

**Details:**
running.md is marked as 'PLACEHOLDER - Documentation in progress' and contains minimal information. It references UI-specific docs but those paths may not all exist:
- CLI: `docs/help/ui/cli/` (exists)
- Curses: `docs/help/ui/curses/running.md` (referenced in other docs)
- TK: `docs/help/ui/tk/` (not seen in provided files)
- Web: `docs/help/ui/web/` (not seen in provided files)

Either complete this common documentation or remove it and ensure all UI-specific running docs exist.

---

#### documentation_inconsistency

**Description:** Installation instructions reference files that may not exist

**Affected files:**
- `docs/help/mbasic/getting-started.md`

**Details:**
getting-started.md installation section references:
- 'pip install -r requirements.txt' - but no requirements.txt file is shown in docs
- 'mbasic' command without .py extension - unclear if this is a shell script or Python module

Should clarify:
1. Whether requirements.txt exists and what it contains
2. How the 'mbasic' command is installed/configured
3. Whether it's 'python mbasic.py' or an installed command

---

#### documentation_inconsistency

**Description:** Typo in keyboard shortcut placeholder

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
Multiple instances of '{{kbd:save:curses}}hift+O' and '{{kbd:save:curses}}hift+B' appear to be typos where 'S' from 'Shift' got concatenated with the kbd template. Should likely be 'Shift+{{kbd:open:curses}}' and 'Shift+{{kbd:toggle_breakpoint:curses}}' or similar.

---

#### documentation_inconsistency

**Description:** Save shortcut explanation inconsistency

**Affected files:**
- `docs/help/ui/curses/files.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
files.md states 'Press {{kbd:save:curses}} to save (Ctrl+S unavailable - terminal flow control)' suggesting {{kbd:save:curses}} is NOT Ctrl+S. However, feature-reference.md states 'Note: Uses {{kbd:save:curses}} because {{kbd:save:curses}} is reserved for terminal flow control' which is circular and confusing. The actual shortcut key is unclear.

---

#### documentation_inconsistency

**Description:** UI comparison table shows conflicting debugger support

**Affected files:**
- `docs/help/ui/index.md`

**Details:**
The comparison table shows Web UI has 'Limited' debugger support, but doesn't specify what limitations exist compared to Curses and Tk which show full support (✓).

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut references for file operations

**Affected files:**
- `docs/help/ui/tk/features.md`
- `docs/help/ui/tk/getting-started.md`

**Details:**
getting-started.md uses {{kbd:save_file}} in the shortcuts table, but features.md uses {{kbd:file_save}} in the Tips section. These should be consistent - likely {{kbd:file_save}} is correct based on the pattern of file_new, file_save, etc.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut references within same document

**Affected files:**
- `docs/help/ui/web/debugging.md`

**Details:**
debugging.md uses both {{kbd:help:web}}1 and {{kbd:help:web}}2 for browser DevTools shortcuts, but earlier in the same document states that function key shortcuts are not implemented. This is internally inconsistent.

---

#### documentation_inconsistency

**Description:** Context Help shortcut not using template notation

**Affected files:**
- `docs/help/ui/tk/features.md`

**Details:**
features.md documents 'Context Help (Shift+F1)' with a hardcoded shortcut instead of using the {{kbd:...}} template notation. This should be {{kbd:context_help}} or similar for consistency with other shortcuts in the document.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation format

**Affected files:**
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
getting-started.md uses placeholder notation: {{kbd:run:web}}, {{kbd:stop:web}}, {{kbd:step:web}}, {{kbd:continue:web}}, {{kbd:help:web}}

web-interface.md uses actual keyboard shortcuts: Ctrl+V, Ctrl+A, Ctrl+C, Ctrl+K

The {{kbd:...}} placeholders appear to be template variables that should be replaced with actual shortcuts, but they're left unreplaced in the published documentation.

---

#### documentation_inconsistency

**Description:** Inconsistent description of Step Line keyboard shortcut

**Affected files:**
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
getting-started.md states: "Step Line - Execute all statements on current line, then pause (⏭️ button, Ctrl+K)"

web-interface.md does not mention Ctrl+K for Step Line in its keyboard shortcuts section, only listing Ctrl+V, Ctrl+A, Ctrl+C.

This creates ambiguity about whether Ctrl+K is actually implemented for Step Line.

---

#### documentation_inconsistency

**Description:** Inconsistent auto-numbering increment default values

**Affected files:**
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/settings.md`

**Details:**
getting-started.md states: "First line: Starts at 10 (configurable in Settings)"

settings.md states: "Line number increment (number input)
  - Range: 1-1000
  - Default: 10"

While both mention 10, getting-started.md refers to the 'starting line number' while settings.md refers to the 'increment'. These are different concepts - starting line vs increment between lines. The documentation conflates these two separate settings.

---

#### documentation_inconsistency

**Description:** Inconsistent game count in library

**Affected files:**
- `docs/help/ui/web/index.md`
- `docs/library/games/index.md`

**Details:**
index.md states: "Games Library - 113 classic CP/M era games to download and load!"

However, counting the games listed in docs/library/games/index.md shows exactly 113 games, which matches. But other library index files (business, data_management, demos, education, electronics, ham_radio) don't provide counts in their parent references.

This is actually consistent, but worth noting for completeness verification.

---

#### documentation_inconsistency

**Description:** Inconsistent Settings dialog access instructions

**Affected files:**
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/settings.md`

**Details:**
getting-started.md mentions: "Use the Settings dialog (⚙️ icon) to change the increment or disable auto-numbering entirely"

settings.md states: "Methods:
1. Click the ⚙️ Settings icon in the navigation bar
2. Click menu → Settings"

The first document only mentions the icon, while the second mentions both icon and menu. This is minor but creates incomplete information in getting-started.md.

---

#### documentation_inconsistency

**Description:** Duplicate calendar program references

**Affected files:**
- `docs/library/games/index.md`

**Details:**
The calendar.bas entry in games/index.md includes a note: "Note: A simpler calendar utility is also available in the [Utilities Library](../utilities/index.md#calendar)"

However, no utilities/index.md file is provided in the documentation files list, so this cross-reference cannot be verified. This may be a broken link or reference to non-existent documentation.

---

#### documentation_inconsistency

**Description:** Inconsistent program count in library statistics

**Affected files:**
- `docs/library/index.md`

**Details:**
The main library index states: 'Library Statistics: 202 programs from the 1970s-1980s'

However, counting the documented programs across all category index files would be needed to verify this number is accurate. The telecommunications category alone shows only 5 programs (Bmodem, Bmodem1, Command, Exitbbs1, Xtel), and utilities shows 18 programs. Without seeing all category files, this count cannot be verified but should be checked for accuracy.

---

#### documentation_inconsistency

**Description:** Program categorization inconsistency - games in utilities

**Affected files:**
- `docs/library/utilities/index.md`

**Details:**
The utilities/index.md file includes two programs that appear to be games rather than utilities:

1. 'Million' - 'Millionaire life simulation game - make financial decisions to accumulate wealth' with tags 'simulation, financial, game'

2. 'Rotate' - 'Letter rotation puzzle game - order letters A-P by rotating groups clockwise' with tags 'puzzle, game, logic'

These are explicitly described as games but are listed in the Utilities category rather than the Games category.

---

#### documentation_inconsistency

**Description:** Placeholder syntax in documentation not explained

**Affected files:**
- `docs/user/QUICK_REFERENCE.md`

**Details:**
The QUICK_REFERENCE.md uses placeholder syntax like {{kbd:new}}, {{kbd:open}}, {{kbd:save}}, {{kbd:run}}, {{kbd:help}}, {{kbd:quit}} throughout the document.

These appear to be template placeholders for actual keyboard shortcuts, but:
1. No explanation is provided for what these placeholders represent
2. The actual key bindings are not specified
3. Users cannot determine what keys to actually press

For example: '| {{kbd:new}} | New | Clear program, start fresh |'

This makes the quick reference unusable without knowing the actual key mappings.

---

#### documentation_inconsistency

**Description:** Contradictory information about CLI debugging capabilities

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
The CHOOSING_YOUR_UI.md document contains contradictory statements about CLI debugging:

In the CLI section 'Limitations': 'No visual debugging (text commands only)'

But then in 'Unique advantages': 'Command-line debugging (BREAK, STEP, STACK commands)'

And later a note clarifies: 'Note: CLI has full debugging capabilities through commands (BREAK, STEP, STACK), but lacks the visual debugging interface (Variables Window, clickable breakpoints, etc.) found in Curses, Tk, and Web UIs.'

The initial 'Limitations' statement is misleading - it should clarify that CLI has debugging commands but lacks visual debugging UI, not imply it has no debugging at all.

---

#### documentation_inconsistency

**Description:** Duplicate installation documentation with redirect

**Affected files:**
- `docs/user/INSTALL.md`
- `docs/user/INSTALLATION.md`

**Details:**
There are two installation documentation files:

1. docs/user/INSTALL.md - Contains the full installation guide
2. docs/user/INSTALLATION.md - A redirect file that says 'This is a redirect file. For complete installation instructions, see INSTALL.md'

While the redirect explains itself, having two files with similar names (INSTALL vs INSTALLATION) could cause confusion. The redirect file exists 'for compatibility with different documentation linking conventions' but this creates maintenance burden and potential for outdated links.

---

#### documentation_inconsistency

**Description:** Missing program descriptions in telecommunications category

**Affected files:**
- `docs/library/telecommunications/index.md`

**Details:**
The telecommunications/index.md file lists 5 programs but provides no descriptions for any of them:

- Bmodem: No description, empty tags
- Bmodem1: No description, empty tags
- Command: No description, empty tags
- Exitbbs1: No description, empty tags
- Xtel: No description, empty tags

All other category index files (utilities, etc.) provide descriptions and tags for their programs. This category appears incomplete compared to the documentation standard established elsewhere.

---

#### documentation_inconsistency

**Description:** Unclear program descriptions for xextract and xscan

**Affected files:**
- `docs/library/utilities/index.md`

**Details:**
Two utility programs have cryptic descriptions that don't explain their purpose:

1. Xextract: '0 -->END PAGE / 1-20 -->EXTRACT ITEM / 21 -->RESTART' with empty tags
2. Xscan: '0 -->END PAGE / 1-20 -->DELETE ITEM / 21 -->RESTART' with empty tags

These appear to be menu options or command descriptions rather than program descriptions. Users cannot determine what these programs actually do from these descriptions.

---

#### documentation_inconsistency

**Description:** TK_UI_QUICK_START.md references keyboard-shortcuts.md but that file only documents Curses UI shortcuts, not Tk shortcuts

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md states:
'### Learn More About...
- **Keyboard Shortcuts**: See [Tk Keyboard Shortcuts](keyboard-shortcuts.md)'

But keyboard-shortcuts.md title is '# MBASIC Curses UI Keyboard Shortcuts' and only documents Curses shortcuts

---

#### documentation_inconsistency

**Description:** UI_FEATURE_COMPARISON.md shows conflicting information about Save functionality

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
The table shows:
| **Save (interactive)** | ❌ | ✅ | ✅ | ✅ | Keyboard shortcut prompts for filename |
| **Save (command)** | ✅ | ✅ | ✅ | ✅ | SAVE "filename" command |

But later states:
'### Known Gaps
- CLI: No interactive save prompt (use SAVE "filename" command instead)'

This is redundant - the table already shows CLI has no interactive save

---

#### documentation_inconsistency

**Description:** Inconsistent reference to LINE INPUT# statement documentation

**Affected files:**
- `docs/user/sequential-files.md`

**Details:**
sequential-files.md references:
'[LINE INPUT#](../help/common/language/statements/inputi.md)'

The filename 'inputi.md' seems unusual - typically would expect 'line-input-hash.md' or similar. This may be correct but appears inconsistent with other statement naming like 'input_hash.md'

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut placeholder format

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
TK_UI_QUICK_START.md uses multiple formats:
- '**{{kbd:run_program}}**'
- '{{kbd:smart_insert}}'
- '**{{kbd:file_save}}**'

Some are bold, some are not, creating visual inconsistency

---

#### documentation_inconsistency

**Description:** Inconsistent status emoji usage

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
SETTINGS_AND_CONFIGURATION.md uses:
'**Status:** 🔧 PLANNED - Not yet implemented'

But the top-level status note uses:
'> **Status:** The settings system is implemented...'

without an emoji. Inconsistent formatting for status indicators

---


## Summary

- Total issues found: 682
- Code/Comment conflicts: 243
- Other inconsistencies: 439
