# Enhanced Consistency Report (Code + Documentation)

Generated: 2025-11-06 04:33:42
Analyzed: Source code (.py, .json) and Documentation (.md)

## 🔧 Code vs Comment Conflicts


## 📋 General Inconsistencies

### 🔴 High Severity

#### code_vs_comment

**Description:** Comment claims identifiers preserve case but implementation returns original_text without using identifier_table

**Affected files:**
- `src/case_string_handler.py`

**Details:**
Lines 60-68 contain a long comment explaining:
# Identifiers always preserve their original case in display.
# Unlike keywords, which can be forced to a specific case policy,
# identifiers (variable/function names) retain their case as typed.
# This matches MBASIC 5.21 behavior where identifiers are case-insensitive
# for matching but preserve display case.
# Note: We return original_text directly without using an identifier_table.
# A future enhancement could track identifiers for conflict detection.

The comment says 'A future enhancement could track identifiers' but the code at line 52 already calls get_identifier_table(policy), suggesting the infrastructure exists but isn't being used. This is inconsistent.

---

#### documentation_inconsistency

**Description:** Contradictory documentation about ProgramManager file I/O methods and their relationship to FileIO abstraction

**Affected files:**
- `src/editing/manager.py`
- `src/file_io.py`

**Details:**
src/editing/manager.py docstring states:
"Note: ProgramManager.load_from_file() returns (success, lines) tuple for direct UI integration, while FileIO.load_file() returns raw file text. These serve different purposes: ProgramManager integrates with the editor, FileIO provides raw file content for the LOAD command to parse."

However, ProgramManager.load_from_file() actually returns (success, errors) where errors is List[Tuple[int, str]], NOT a lines tuple. The actual implementation:
"Returns:
    Tuple of (success, errors)
    success: True if at least one line loaded successfully
    errors: List of (line_number, error_message) for failed lines"

---

#### code_vs_comment

**Description:** Comment describes validation behavior that doesn't exist in the code

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Lines 157-165 comment states:
'# This feature requires the following UI integration:
# - interpreter.interactive_mode must reference the UI object (checked with hasattr)
# - UI.program must have add_line() and delete_line() methods (validated, errors if missing)
# - UI._refresh_editor() method to update the display (optional, checked with hasattr)
# - UI._highlight_current_statement() for restoring execution highlighting (optional, checked with hasattr)
# If interactive_mode doesn't exist, line editing silently continues without UI update.
# If interactive_mode exists but required program methods are missing, returns error message.'

However, the actual code (lines 175-182) validates UI.program and its methods:
'if not hasattr(ui, 'program') or not ui.program:
    return (False, "Cannot edit program lines: UI program manager not available\n")
if line_content and not hasattr(ui.program, 'add_line'):
    return (False, "Cannot edit program lines: add_line method not available\n")
if not line_content and not hasattr(ui.program, 'delete_line'):
    return (False, "Cannot edit program lines: delete_line method not available\n")'

The comment says 'If interactive_mode doesn't exist, line editing silently continues without UI update', but the code at line 173 checks 'if hasattr(self.interpreter, 'interactive_mode') and self.interpreter.interactive_mode:' and if this is False, it falls through to line 210 which returns an error: 'return (False, "Cannot edit program lines in this mode\n")'. This contradicts the 'silently continues' claim.

---

#### code_vs_comment

**Description:** RENUM documentation claims conservative behavior for ERL expressions but implementation may incorrectly renumber arithmetic operations

**Affected files:**
- `src/interactive.py`

**Details:**
Docstring at line ~862 states:
'Conservative behavior: ERL expressions with ANY binary operators (ERL+100, ERL*2, ERL=100)
have all right-hand numbers conservatively renumbered, even for arithmetic operations.
This is intentionally broader than the MBASIC manual (which only specifies comparison
operators) to avoid missing line references.'

But then at line ~952 the comment says:
'Known limitation: Arithmetic like "IF ERL+100 THEN..." will incorrectly renumber
the 100 if it happens to be an old line number. This is rare in practice.'

The docstring calls this 'conservative' and 'intentional', while the implementation comment calls it a 'known limitation' and 'incorrect'. These are contradictory characterizations of the same behavior.

---

#### code_vs_comment

**Description:** CONT command docstring describes state management but doesn't mention GOSUB/FOR stack clearing on edit

**Affected files:**
- `src/interactive.py`

**Details:**
The cmd_cont docstring at line ~476 describes state management:
'State management:
- Clears stopped/halted flags in runtime
- Restores PC from stop_pc (saved execution position)
- Resumes tick-based execution loop
- Handles input prompts and errors during execution'

However, the clear_execution_state() method at line ~143 clears GOSUB and FOR stacks when lines are edited, which would make CONT fail or behave incorrectly. The docstring doesn't mention this interaction or warn that editing lines invalidates CONT state.

---

#### code_vs_comment

**Description:** Comment about error_info being set before _invoke_error_handler contradicts the actual flow

**Affected files:**
- `src/interpreter.py`

**Details:**
In _invoke_error_handler, the comment says:
"Note: error_info is set by the exception handler in tick_pc() that caught
the error before calling this method. We're now ready to invoke the error handler."

But in tick_pc(), the code shows:
```python
except Exception as e:
    # Check if we're already in an error handler (prevent recursive errors)
    already_in_error_handler = (self.state.error_info is not None)

    # Set ErrorInfo for both handler and no-handler cases (needed by RESUME)
    error_code = self._map_exception_to_error_code(e)
    self.state.error_info = ErrorInfo(
        error_code=error_code,
        pc=pc,
        error_message=str(e)
    )

    # Check if we have an error handler and not already handling an error
    if self.runtime.has_error_handler() and not already_in_error_handler:
        self._invoke_error_handler(error_code, pc)
```

The comment in _invoke_error_handler is correct - error_info IS set before calling _invoke_error_handler. However, the comment could be clearer that error_info is set in the same exception handler block, not by a separate handler.

---

#### code_vs_comment

**Description:** Comment in execute_clear says 'Errors during file close are silently ignored (bare except: pass below)' but the code shows 'except: pass' without any comment marker indicating where this is

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment in execute_clear:
# Close all open files
# Note: Errors during file close are silently ignored (bare except: pass below)
for file_num in list(self.runtime.files.keys()):
    try:
        file_obj = self.runtime.files[file_num]
        if hasattr(file_obj, 'close'):
            file_obj.close()
    except:
        pass

The comment says '(bare except: pass below)' but the except: pass is right there in the visible code, not 'below'. This is a minor wording issue but could confuse readers.

---

#### code_vs_comment

**Description:** Comment in execute_cont describes behavior distinction but the actual check doesn't verify the distinction works as described

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment says: "Behavior distinction (MBASIC 5.21 compatibility):
- STOP statement: Sets both runtime.stopped=True AND runtime.halted=True
  The stopped flag allows CONT to resume from the saved position
- Break (Ctrl+C): Sets runtime.halted=True but NOT stopped=True, so CONT fails
This is intentional: CONT only works after STOP, not after Break interruption."

The code checks: if not self.runtime.stopped: raise RuntimeError("Can't continue - no program stopped")

However, there's no verification in this file that execute_stop actually sets both flags, or that Break only sets halted. The comment describes a contract but we can't verify it's upheld from this code alone.

---

#### code_vs_comment

**Description:** Docstring describes behavior that code doesn't fully implement for INPUT statement

**Affected files:**
- `src/parser.py`

**Details:**
In parse_input() docstring:
"Syntax:
    INPUT var1, var2           - Read from keyboard
    INPUT "prompt"; var1       - Read with prompt
    INPUT #filenum, var1       - Read from file"

However, the code also handles:
- INPUT; (semicolon immediately after INPUT to suppress ? prompt)
- INPUT "prompt";LINE var$ (LINE modifier)

These syntaxes are implemented in the code but not documented in the docstring, creating an incomplete documentation of the parser's capabilities.

---

#### code_vs_comment

**Description:** Comment claims line numbers use fixed 5-character width, but code uses variable width

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Class docstring at line 149 states: "Note: This is NOT a true columnar layout with fixed column boundaries.
Line numbers use variable width for display (_format_line returns variable-width numbers).
However, when reformatting pasted content, _parse_line_numbers uses fixed 5-character width
for alignment consistency."

But _format_line() at line 449 uses: line_num_str = f"{line_num}" (variable width, no padding)

And _parse_line_numbers() at lines 991 and 1024 uses: line_num_formatted = f"{num_str:>5}" (fixed 5-char width)

This creates inconsistent formatting between display and paste handling.

---

#### internal_inconsistency

**Description:** Inconsistent line number formatting between _format_line and _parse_line_numbers methods

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
_format_line() at line 449 uses variable-width formatting:
line_num_str = f"{line_num}"
prefix = f"{status}{line_num_str} "

_parse_line_numbers() at lines 991 and 1024 uses fixed-width formatting:
line_num_formatted = f"{num_str:>5}"
new_line = f" {line_num_formatted} {rest}"

This means displayed lines have variable-width line numbers, but pasted/reformatted lines have fixed 5-character width, causing visual inconsistency.

---

#### code_vs_comment

**Description:** Comment about main widget storage contradicts between methods

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _show_help() at line ~850: 'Main widget retrieval: Use self.main_widget for consistency with _show_keymap and _show_settings (not self.loop.widget which might be a menu or other overlay at this moment)'

But in _activate_menu() at line ~920: 'Main widget storage: Extract base_widget from current loop.widget. This unwraps any existing overlay to get the actual main UI. This is different from _show_keymap/_show_settings which use self.main_widget directly.'

These comments describe different approaches - _show_help uses self.main_widget directly, while _activate_menu extracts base_widget from loop.widget. The comments acknowledge this difference but don't explain why the approaches differ.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate claims it syncs program to runtime but doesn't reset PC, yet the code shows _sync_program_to_runtime is called which may reset PC depending on implementation

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment says:
"# Sync program to runtime (but don't reset PC - keep current execution state)
# This allows LIST to work, but doesn't start execution
self._sync_program_to_runtime()"

The comment claims PC is not reset, but without seeing _sync_program_to_runtime implementation, we cannot verify this. The comment also contradicts itself by saying 'keep current execution state' while also noting that later code checks 'if self.runtime.npc is not None' and moves npc to pc, which IS modifying execution state.

---

#### code_vs_comment

**Description:** Comment claims interpreter.start() is not called to preserve PC, but then describes that immediate executor already called interpreter.start(start_line=120), which contradicts the preservation claim

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment in _execute_immediate:
"# NOTE: Don't call interpreter.start() because it resets PC!
# If the immediate command was 'RUN 120', the immediate executor has already
# set PC to line 120 via interpreter.start(start_line=120), so we need to
# preserve that PC value and not reset it."

This is contradictory: it says don't call interpreter.start() to preserve PC, but then says the immediate executor already called interpreter.start(start_line=120). If interpreter.start() was already called, the PC was already set/reset. The logic is unclear about what state is being preserved.

---

#### code_vs_comment_conflict

**Description:** Comment claims help navigation keys are hardcoded and not loaded from keybindings, but HelpMacros class does load keybindings from JSON

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment in help_widget.py lines 66-70 states:
"Note: Help navigation keys are hardcoded here and in keypress() method.
While HelpMacros loads keybindings for {{kbd:action}} macro expansion in help content,
the help widget's own navigation keys (U for back, / for search, etc.) are hardcoded
separately and not loaded from keybindings. If these change, update here and keypress()."

However, HelpMacros.__init__() in help_macros.py line 24 calls self._load_keybindings() which loads from JSON:
"keybindings_path = Path(__file__).parent / f"{self.ui_name}_keybindings.json""

The comment suggests HelpMacros only loads keybindings for macro expansion, but the class has full access to keybindings. The help widget navigation keys (U, /, ESC, Q, Tab, Enter) are indeed hardcoded in keypress() method rather than using the loaded keybindings.

---

#### code_vs_comment

**Description:** Comment about OPTION BASE behavior conflicts with code implementation for invalid values

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
At line ~380, comment states:
"# If no default subscripts, use first element based on array_base
# (OPTION BASE 0 uses zeros, OPTION BASE 1 uses ones, invalid values fallback to zeros)"

Then the code implements:
"if array_base == 0:
    # OPTION BASE 0: use all zeros
    default_subscripts = ','.join(['0'] * len(dimensions))
elif array_base == 1:
    # OPTION BASE 1: use all ones
    default_subscripts = ','.join(['1'] * len(dimensions))
else:
    # Invalid array_base (not 0 or 1) - fallback to 0
    default_subscripts = ','.join(['0'] * len(dimensions))"

This is correct, but the comment says "invalid values fallback to zeros" while BASIC standards typically only allow 0 or 1 for OPTION BASE. The code should validate array_base earlier or this comment should clarify that invalid values are a defensive programming measure, not an expected case.

---

#### code_vs_comment

**Description:** Comment in cmd_cont says stop_line and stop_stmt_index are optional extensions, but code uses them without checking if they exist

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1730 says:
# NOTE: This is a simplified implementation. The runtime.stop_line and
# runtime.stop_stmt_index attributes are optional extensions for better
# state restoration. If not present, execution continues from the current
# PC position maintained by the interpreter.

But code at line ~1750 uses:
if hasattr(self.runtime, 'stop_line') and hasattr(self.runtime, 'stop_stmt_index'):
    self.runtime.current_line = self.runtime.stop_line
    self.runtime.current_stmt_index = self.runtime.stop_stmt_index

The code correctly checks with hasattr(), but then assigns to current_line and current_stmt_index without checking if THOSE attributes exist. If stop_line/stop_stmt_index are optional, current_line/current_stmt_index might also not exist, causing AttributeError.

---

#### code_vs_comment

**Description:** Comment says 'Don't call interpreter.start()' but then manually replicates part of what start() would do

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment states: "NOTE: Don't call interpreter.start() because it resets PC! RUN 120 already set PC to line 120, so just clear halted flag"

But then the code does:
- self.runtime.halted = False
- self.interpreter.state.is_first_line = True

This is manually replicating initialization logic that might be in start(). If start() does more than just reset PC and set these flags, this could lead to incomplete initialization. The comment should clarify what other initialization start() does and why it's safe to skip it.

---

#### code_vs_comment

**Description:** Canvas width comment says '20 (pixels in Tkinter)' but this is misleading - the width parameter in Tkinter Canvas is in pixels by default, not a special Tkinter unit

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment: "# Width: 20 (pixels in Tkinter) for one status character (●, ?, or space)"

Code: self.canvas = tk.Canvas(self, width=20, bg='#e0e0e0', highlightthickness=0)

The phrase 'pixels in Tkinter' is redundant and potentially confusing. Tkinter Canvas width is measured in pixels by default (or screen units which are typically pixels). There's no special 'Tkinter pixel' unit - it's just pixels. The comment should simply say '20 pixels' or '20' without the parenthetical.

---

#### code_vs_comment

**Description:** serialize_statement() has a fallback that creates REM comments for unhandled statement types, with a WARNING comment about potential invalid code during RENUM, but no error handling or validation

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Code:
else:
    # Fallback for unhandled statement types: return a placeholder REM comment.
    # WARNING: This could create invalid BASIC code during RENUM if new statement
    # types are added but not handled here. Ensure all statement types are supported.
    return f"REM {stmt_type}"

This is a silent failure mode that could corrupt programs during RENUM. The function should either raise an error for unknown types or log a warning, rather than silently creating invalid code.

---

### 🟡 Medium Severity

#### code_vs_comment

**Description:** Fix script claims to modify src/runtime.py but the replacement pattern is incomplete/malformed

**Affected files:**
- `medium_severity_fixes.py`

**Details:**
Fix 6 in medium_severity_fixes.py:
count = fix_file('src/runtime.py', [
    ('_resolve_variable_name() docstring:',
     '_resolve_variable_name() is the standard method for variable resolution.'),
])

This replacement pattern is searching for '_resolve_variable_name() docstring:' which is unlikely to exist as literal text in the source. The pattern appears to be a placeholder or incomplete fix specification rather than actual text to replace.

---

#### code_vs_documentation

**Description:** InputStatementNode documentation contradicts itself on semicolon behavior

**Affected files:**
- `src/ast_nodes.py`

**Details:**
InputStatementNode docstring states:
"Note: The suppress_question field indicates whether to suppress the question mark prompt:
- suppress_question=False (default): INPUT var or INPUT "prompt", var → shows "? " or "prompt? "
- suppress_question=True: INPUT; var → suppresses "?" completely (no prompt at all)

Semicolon usage:
- After prompt string: INPUT "prompt"; var → semicolon is just a separator (shows "prompt? ")
- Immediately after INPUT: INPUT; var → semicolon signals suppress_question=True"

The first bullet under "Semicolon usage" says INPUT "prompt"; var shows "prompt? " (with question mark), but the suppress_question=True description says it "suppresses '?' completely (no prompt at all)". This creates ambiguity about when the question mark is actually suppressed.

---

#### code_vs_comment

**Description:** LineNode docstring claims no source_text field exists but doesn't explain char_start/char_end on StatementNode

**Affected files:**
- `src/ast_nodes.py`

**Details:**
LineNode docstring states:
"Design note: This class intentionally does not have a source_text field to avoid
maintaining duplicate copies that could get out of sync with the AST during editing.
Text regeneration is handled by the position_serializer module which reconstructs
source text from statement nodes and their token information."

However, StatementNode has char_start and char_end fields:
char_start: int = 0  # Character offset from start of line for highlighting
char_end: int = 0    # Character offset end position for highlighting

These fields reference "character offset from start of line" which implies there is a line text to offset from. The design note in LineNode should explain how char_start/char_end relate to the "no source_text" design, or clarify that these offsets are maintained separately from source text.

---

#### code_vs_comment

**Description:** Comment claims original_negative is captured at line 269, but that line number is incorrect in the actual code

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Comment at line 274 states:
# original_negative was captured before rounding (line 269 above)
But original_negative is actually captured at line 271, not 269. The comment references an incorrect line number.

---

#### code_vs_comment

**Description:** EOF function comment describes ^Z behavior but implementation details are unclear about when mode 'I' is set

**Affected files:**
- `src/basic_builtins.py`

**Details:**
The EOF function docstring states:
Note: For binary input files (mode 'I' from OPEN statement), respects ^Z (ASCII 26)
as EOF marker (CP/M style). Mode 'I' is set by the OPEN statement for binary input.

However, the code comment at line 738 states:
# Mode 'I' = binary input mode where ^Z checking is appropriate

But there's no code in this file showing how mode 'I' is actually set. The comment assumes the OPEN statement sets this mode, but that implementation is not visible here, making it unclear if the mode checking logic is correct.

---

#### code_vs_comment

**Description:** Comment about next_byte indexing assumes binary mode but doesn't verify it

**Affected files:**
- `src/basic_builtins.py`

**Details:**
At line 744, the comment states:
# File opened in binary mode ('rb') per mode 'I' check above
# read(1) returns bytes object; next_byte[0] accesses the first byte value as integer

However, the code at line 741 only checks if mode == 'I', but doesn't verify the file was actually opened in binary mode. If the file was opened in text mode despite mode being 'I', next_byte would be a string, not bytes, and next_byte[0] would return a character, not an integer. This could cause a type error when comparing to 26.

---

#### code_vs_documentation

**Description:** SandboxedFileIO documentation claims it delegates to backend.sandboxed_fs but implementation shows incomplete integration

**Affected files:**
- `src/file_io.py`
- `src/filesystem/sandboxed_fs.py`

**Details:**
src/file_io.py SandboxedFileIO docstring states:
"Acts as an adapter to backend.sandboxed_fs (SandboxedFileSystemProvider from src/filesystem/sandboxed_fs.py), which provides an in-memory virtual filesystem."

But only list_files() is implemented with delegation:
"if hasattr(self.backend, 'sandboxed_fs'):
    pattern = filespec.strip().strip('"').strip("'") if filespec else None
    files = self.backend.sandboxed_fs.list_files(pattern)"

All other methods (load_file, save_file, delete_file, file_exists) raise IOError with "not yet implemented" messages, contradicting the claim that it "acts as an adapter" to the sandboxed filesystem.

---

#### documentation_inconsistency

**Description:** Inconsistent explanation of overlap between FileIO and FileSystemProvider abstractions

**Affected files:**
- `src/file_io.py`
- `src/filesystem/base.py`

**Details:**
Both files claim there is "intentional overlap" for list_files() and delete() methods, but provide different justifications:

src/file_io.py states:
"Note: Both abstractions serve different purposes and are used at different times. There is intentional overlap: both provide list_files() and delete() methods. FileIO is for interactive commands (FILES/KILL), FileSystemProvider is for runtime access (though not all BASIC dialects support runtime file listing/deletion)."

src/filesystem/base.py states:
"Note: There is intentional overlap between the two abstractions. Both provide list_files() and delete() methods, but serve different contexts: FileIO is for interactive commands (FILES/KILL), FileSystemProvider is for runtime access (though not all BASIC dialects support runtime file operations)."

The explanations are nearly identical but use different wording ("different times" vs "different contexts", "runtime file listing/deletion" vs "runtime file operations"), suggesting copy-paste documentation that may not have been carefully reviewed for consistency.

---

#### code_vs_documentation

**Description:** ProgramManager.merge_from_file() return type documentation incomplete

**Affected files:**
- `src/editing/manager.py`

**Details:**
The docstring states:
"Returns:
    Tuple of (success, errors, lines_added, lines_replaced)
    success: True if at least one line loaded successfully
    errors: List of (line_number, error_message) for failed lines
    lines_added: Count of new lines added
    lines_replaced: Count of existing lines replaced"

However, the actual implementation shows that on failure, it returns (False, errors, 0, 0), which means the return type is always a 4-tuple. The docstring doesn't clarify that lines_added and lines_replaced will be 0 when success is False, which could lead to confusion about whether these counts include failed parse attempts.

---

#### code_vs_comment

**Description:** Comment claims INPUT statements are 'blocked when input() is called, not at parse time' but the help text says INPUT 'will fail at runtime'

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Line 154 comment: 'INPUT statement will fail at runtime in immediate mode (blocked when input() is called, not at parse time - use direct assignment instead)'

Help text (line 334): '• INPUT statement will fail at runtime in immediate mode (blocked when input() is called, not at parse time - use direct assignment instead)'

Both say the same thing, but the phrasing 'blocked when input() is called' vs 'will fail at runtime' could be clearer. The implementation in OutputCapturingIOHandler.input() raises RuntimeError, which is 'failing at runtime', not 'blocking'.

---

#### code_vs_comment

**Description:** Comment about PC save/restore contradicts actual behavior

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Line 244 comment states:
'# Note: We do not save/restore the PC before/after execution.
# This allows statements like RUN to change execution position.
# Normal statements (PRINT, LET, etc.) don't modify PC anyway.'

This comment suggests that the code intentionally doesn't save/restore PC to allow RUN to work. However, there's no code that would save/restore PC anyway - the comment describes what the code doesn't do, but doesn't explain why this matters or what the alternative would be. The comment seems to be explaining a design decision that isn't evident from the code itself.

---

#### code_vs_comment

**Description:** Help text claims INPUT is 'blocked' but implementation raises exception

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Help text line 334 states:
'• INPUT statement will fail at runtime in immediate mode (blocked when input() is called, not at parse time - use direct assignment instead)'

OutputCapturingIOHandler.input() method (lines 377-381) implementation:
'def input(self, prompt=""):
    """Input not supported in immediate mode.

    Note: INPUT statements are parsed and executed normally, but fail
    at runtime when the interpreter calls this input() method."""
    raise RuntimeError("INPUT not allowed in immediate mode")'

The term 'blocked' suggests the operation is prevented or waiting, but the code raises a RuntimeError exception. This is 'failing' not 'blocking'. The terminology is inconsistent.

---

#### code_vs_comment

**Description:** Comment claims EDIT command 'count prefixes and search commands are not yet implemented' but doesn't clarify what happens when digits are entered

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~1050 says:
'Note: Count prefixes ([n]D, [n]C) and search commands ([n]S, [n]K) are not yet implemented.
Digits fall through the command handling logic and produce no action (no output, no cursor movement).'

However, the actual edit command handler (cmd_edit) has no explicit handling for digit characters. The code will read the digit via _read_char() but then fall through all the if/elif branches without any action, which matches the comment. But this behavior is implicit rather than documented in code.

---

#### code_vs_documentation

**Description:** CHAIN command documentation incomplete regarding execution flow

**Affected files:**
- `src/interactive.py`

**Details:**
The cmd_chain docstring at line ~673 describes the CHAIN command parameters but doesn't mention that it raises ChainException to signal the interpreter to restart. The comment at line ~779 says:
'# Raise ChainException to signal run() loop to restart with new program
# This avoids recursive run() calls'

This is a critical implementation detail for understanding CHAIN behavior but is not documented in the main docstring.

---

#### code_vs_comment

**Description:** MERGE command comment about runtime update doesn't match actual implementation location

**Affected files:**
- `src/interactive.py`

**Details:**
The cmd_merge docstring at line ~598 says:
'- If program_runtime exists, updates runtime's statement_table (for CONT support)'

But the actual runtime update code at line ~635 is inside the 'if success:' block, meaning it only updates if the merge was successful. The docstring doesn't clarify this conditional behavior. Additionally, the update happens after the merge_from_file call, but the docstring makes it sound like it's part of the merge process itself.

---

#### code_vs_comment

**Description:** Comment about COMMON variable handling describes implementation that may not match actual behavior

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~697 says:
'# COMMON variable handling: common_vars stores base names (e.g., "i"), but
# actual variables may have type suffixes (e.g., "i%", "i$") based on DEF
# statements or explicit suffixes. We try all possible type suffixes
# (%, $, !, #, and no suffix) to find the actual variable in the runtime.'

This describes trying all suffixes, but the actual code at line ~710 only tries one suffix at a time and breaks on first match:
'for suffix in [\'%\', \'$\', \'!\', \'#\', \'\']:
    full_name = var_name + suffix
    if self.program_runtime.variable_exists(full_name):
        saved_variables[full_name] = self.program_runtime.get_variable_raw(full_name)
        found = True
        break'

The comment makes it sound like all suffixes are tried, but the code only saves the first match. This could be a problem if multiple type-suffixed versions of the same base name exist.

---

#### code_vs_comment_conflict

**Description:** Comment claims GOTO/GOSUB in immediate mode are 'not recommended' and behavior 'may be confusing', but then describes that they actually work functionally. The comment is contradictory about whether these commands work properly.

**Affected files:**
- `src/interactive.py`

**Details:**
Comment states: 'Note: GOTO/GOSUB in immediate mode are not recommended (see help text) because behavior may be confusing: they execute and jump during execute_statement(), but we restore the original PC afterward to preserve CONT functionality.'

Then explains: 'This means:
- The jump happens and target code runs during execute_statement()
- But the final PC change is reverted, preserving stopped position
- CONT will resume at the original stopped location, not the GOTO target
- So GOTO/GOSUB are functionally working but their PC effects are undone'

The comment describes working behavior but labels it as 'not recommended' and 'confusing' without clear justification.

---

#### code_vs_comment

**Description:** InterpreterState docstring describes checking order for UI code examining completed state, but the actual execution order in tick_pc() is different and more complex

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring says:
"For UI/callers checking completed state:
- error_info: Non-None if an error occurred (highest priority for display)
- input_prompt: Non-None if waiting for input (set during statement execution)
- runtime.halted: True if stopped (paused/done/at breakpoint)"

But tick_pc() execution order is:
1. pause_requested check
2. halted check
3. break_requested check
4. breakpoints check
5. statement execution (where input_prompt is set)
6. error handling (where error_info is set)

The docstring's suggested checking order for UI is reasonable but doesn't match the internal execution flow, which could confuse developers trying to understand the state machine.

---

#### code_vs_comment

**Description:** Comment in current_statement_char_end property describes logic that doesn't fully match the implementation

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment says:
"Uses max(char_end, next_char_start - 1) to handle string tokens correctly.
For the last statement on a line, uses line_text_map to get actual line length
(if available), otherwise falls back to stmt.char_end.
This works because:
- If there's a next statement, the colon is at next_char_start - 1
- If char_end is correct (most tokens), it will be >= next_char_start - 1
- If char_end is too short (string tokens), next_char_start - 1 is larger
- If no line_text_map entry exists, returns stmt.char_end as fallback"

But the code has three branches:
1. If next statement exists: return max(stmt_char_end, next_stmt.char_start - 1)
2. If no next statement AND line in line_text_map: return len(line_text)
3. If no next statement AND no line_text_map: return stmt_char_end

The comment doesn't clearly explain that branch 2 returns the full line length (not just char_end), which could be much larger than char_end if there are trailing spaces or comments.

---

#### code_vs_comment

**Description:** Comment about NEXT processing order conflicts with implementation details

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_next(), the docstring says:
"NEXT I, J, K processes variables left-to-right: I first, then J, then K.
For each variable, _execute_next_single() is called to increment it and check if
the loop should continue. If _execute_next_single() returns True (loop continues),
execution jumps back to the FOR body and remaining variables are not processed.
If it returns False (loop finished), that loop is popped and the next variable is processed."

But _execute_next_single() doesn't return True/False in the code shown. The code in execute_next() is:
```python
for var_node in var_list:
    var_name = var_node.name + (var_node.type_suffix or "")
    # Process this NEXT
    should_continue = self._execute_next_single(var_name, var_node=var_node)
    # If this loop continues (jumps back), don't process remaining variables
    if should_continue:
        return
```

The code expects a return value but _execute_next_single() signature shows:
"Returns:
    True if loop continues (jumped back), False if loop finished"

However, the implementation of _execute_next_single() is cut off in the provided code, so we can't verify if it actually returns these values. This is a potential inconsistency.

---

#### code_vs_comment

**Description:** Comment about return_stmt validation range is confusing

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_return(), the comment says:
"return_stmt is 0-indexed offset into statements array.
Valid range: 0 to len(statements) (inclusive).
- 0 to len(statements)-1: Normal statement positions
- len(statements): Special sentinel - GOSUB was last statement on line, so RETURN
  continues at next line. This value is valid because PC can point one past the
  last statement to indicate 'move to next line' (handled by statement_table.next_pc).
Values > len(statements) indicate the statement was deleted (validation error)."

But the validation code is:
```python
if return_stmt > len(line_statements):  # Check for strictly greater than (== len is OK)
    raise RuntimeError(f"RETURN error: statement {return_stmt} in line {return_line} no longer exists")
```

The comment correctly explains the logic, but the inline comment "Check for strictly greater than (== len is OK)" is redundant with the detailed comment above. The detailed comment is clear, but having both might confuse readers about which to trust.

---

#### code_vs_comment

**Description:** Comment describes WEND popping loop 'after setting npc above, before WHILE re-executes' but the actual pop happens after npc is set, which means the loop is popped before WHILE condition is re-evaluated, not 'before WHILE re-executes'

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment says: 'Pop the loop from the stack (after setting npc above, before WHILE re-executes). Timing: We pop NOW so the stack is clean before WHILE condition re-evaluation.'

Code shows:
self.runtime.npc = PC(loop_info['while_line'], loop_info['while_stmt'])
self.limits.pop_while_loop()
self.runtime.pop_while_loop()

The comment is internally contradictory - it says 'before WHILE re-executes' but then clarifies 'before WHILE condition re-evaluation', which are the same thing. The code pops after setting npc but before the next tick executes WHILE.

---

#### code_vs_comment

**Description:** Comment in execute_next describes return_stmt validation logic but the explanation of 'len(statements)' as sentinel is confusing given the actual validation

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment says:
# return_stmt is 0-indexed offset into statements array.
# Valid range:
#   - 0 to len(statements)-1: Normal statement positions (existing statements)
#   - len(statements): Special sentinel value - FOR was last statement on line,
#                      continue execution at next line (no more statements to execute on current line)
#   - > len(statements): Invalid - indicates the statement was deleted
#
# Validation: Check for strictly greater than (== len is OK as sentinel)
if return_stmt > len(line_statements):
    raise RuntimeError(f"NEXT error: FOR statement in line {return_line} no longer exists")

The comment describes len(statements) as a 'special sentinel value' but then the validation only checks for '> len(statements)', which means return_stmt == len(statements) is allowed. This is confusing because if it's truly a sentinel, it should be documented why this specific value is valid and what it means for the FOR loop continuation logic.

---

#### code_vs_comment

**Description:** Comment in execute_input describes state machine steps but step numbering doesn't match the actual flow

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment says:
State machine for keyboard input (file input is synchronous):
1. If state.input_buffer has data: Use buffered input (from provide_input())
2. Otherwise: Set state.input_prompt, input_variables, input_file_number and return (pauses execution)
3. UI calls provide_input() with user's input line
4. On next tick(), buffered input is used (step 1) and state vars are cleared

Step 4 says 'state vars are cleared' but looking at the code, state vars are cleared at the END of execute_input after successful assignment, not 'on next tick()'. The clearing happens in the same execution that uses the buffered input, not on a subsequent tick.

---

#### code_vs_comment

**Description:** Comment in _read_line_from_file describes latin-1 encoding but warns about CP/M code page mismatch without explaining the implications

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment says:
Encoding:
Uses latin-1 (ISO-8859-1) to preserve byte values 128-255 unchanged.
CP/M and MBASIC used 8-bit characters; latin-1 maps bytes 0-255 to
Unicode U+0000-U+00FF, allowing round-trip byte preservation.
Note: CP/M systems often used code pages like CP437 or CP850 for characters
128-255, which do NOT match latin-1. Latin-1 preserves the BYTE VALUES but
not necessarily the CHARACTER MEANING for non-ASCII CP/M text. Conversion
may be needed for accurate display of non-English CP/M files.

This comment warns about a potential issue but doesn't provide guidance on how to handle it. If conversion 'may be needed', when is it needed and how should it be done? This leaves the implementation incomplete.

---

#### code_vs_comment

**Description:** Comment in execute_optionbase describes 'Duplicate Definition' error conditions but the check logic comment is redundant

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment says:
# MBASIC 5.21 gives 'Duplicate Definition' if:
# 1. OPTION BASE has already been executed, OR
# 2. Any arrays have been created (both explicitly via DIM and implicitly via first use like A(5)=10)
#    This applies regardless of the current array base (0 or 1).
# Note: The check len(self.runtime._arrays) > 0 catches all array creation because both
# explicit DIM and implicit array access (via set_array_element) update runtime._arrays.

The 'Note' at the end is redundant - it explains that checking _arrays catches all array creation, but this is obvious from the code. The comment would be more useful if it explained WHY MBASIC has this restriction or what problems it prevents.

---

#### code_vs_comment

**Description:** Comment claims RSET truncates from left when value is too long, but code truncates from right

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment says: "Right-justify: pad on left if too short, truncate from left if too long"
But code does: value = value[-width:] which keeps rightmost characters (truncates from left is correct)
Actually, the code IS correct for right-justify (keeping rightmost chars), but the comment is ambiguous. For right-justify, you want to keep the rightmost characters when truncating, which value[-width:] does correctly.

---

#### code_vs_comment

**Description:** Comment claims string concatenation limit is 255 characters, but check uses len() which counts characters not bytes, inconsistent with field buffer encoding note

**Affected files:**
- `src/interpreter.py`

**Details:**
In evaluate_binaryop, comment says: "Enforce 255 character string limit for concatenation (MBASIC 5.21 compatibility)
Note: This check only applies to concatenation via PLUS operator.
Other string operations (MID$, LSET, RSET, INPUT) do not enforce this limit.
Also note: len() counts characters, not bytes. For ASCII this is equivalent.
Field buffers (LSET/RSET) explicitly use latin-1 encoding where byte count matters."

The comment acknowledges len() counts characters not bytes, and mentions field buffers use latin-1 where byte count matters. However, for the 255 limit on concatenation, if MBASIC 5.21 had a byte limit, using len() on potentially multi-byte strings could be incorrect. The comment suggests this is intentional but creates inconsistency with the field buffer approach.

---

#### code_vs_comment

**Description:** Comment in execute_step says 'not yet functional - no actual stepping occurs' but doesn't explain what the current implementation does

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: "STEP is intended to execute one or more statements, then pause.
Current implementation: Placeholder (not yet functional - no actual stepping occurs)."

But the code does: self.io.output(f"STEP {count} - Debug stepping not fully implemented")

So it IS functional in that it outputs a message, just not the intended stepping behavior. The comment should clarify that it outputs a message but doesn't perform stepping.

---

#### code_vs_comment

**Description:** execute_put docstring and code don't validate that record_num is positive

**Affected files:**
- `src/interpreter.py`

**Details:**
The code does: record_num = int(self.evaluate_expression(stmt.record_number))
Then: file_handle.seek((record_num - 1) * record_size)

If record_num is 0 or negative, this would seek to a negative position or position -1*record_size. The code doesn't validate record_num >= 1, which could cause unexpected behavior. MBASIC 5.21 likely requires record numbers to be >= 1.

---

#### Code vs Documentation inconsistency

**Description:** WebIOHandler has backward compatibility aliases print() and get_char() that are not documented in the base IOHandler interface or mentioned in the module-level documentation

**Affected files:**
- `src/iohandler/web_io.py`
- `src/iohandler/base.py`

**Details:**
web_io.py contains:
    def print(self, text="", end="\n"):
        """Deprecated: Use output() instead.

        This is a backward compatibility alias. New code should use output().
        """
        self.output(text, end)

    def get_char(self):
        """Deprecated: Use input_char() instead.

        This is a backward compatibility alias. New code should use input_char().
        """
        return self.input_char(blocking=False)

These methods are not part of the IOHandler base class interface and are not mentioned in any documentation about the iohandler module.

---

#### Code vs Documentation inconsistency

**Description:** Module docstring mentions SimpleKeywordCase and references src/simple_keyword_case.py, but this file is not included in the provided source code files, making it impossible to verify the relationship or consistency

**Affected files:**
- `src/keyword_case_manager.py`

**Details:**
keyword_case_manager.py docstring states:
Note: This class provides advanced case policies (first_wins, preserve, error) via
CaseKeeperTable and is used by parser.py and position_serializer.py. For simpler
force-based policies in the lexer, see SimpleKeywordCase (src/simple_keyword_case.py)
which only supports force_lower, force_upper, and force_capitalize.

The referenced file 'src/simple_keyword_case.py' is not provided in the source code files, so the relationship and consistency cannot be verified.

---

#### code_vs_comment

**Description:** Comment claims SimpleKeywordCase 'validates policy strings and defaults to force_lower for invalid values', but the actual SimpleKeywordCase class is not shown in the provided code, so this cannot be verified

**Affected files:**
- `src/lexer.py`

**Details:**
In create_keyword_case_manager() docstring:
"SimpleKeywordCase validates policy strings and defaults to force_lower for invalid values."

The SimpleKeywordCase class implementation is imported but not provided, so we cannot verify if it actually validates and defaults as claimed.

---

#### code_vs_comment

**Description:** Comment claims identifiers use 'original_case' field while keywords use 'original_case_keyword', but the code sets both fields inconsistently

**Affected files:**
- `src/lexer.py`

**Details:**
Comment in read_identifier() says:
"Preserve original case for display (identifiers always use original_case field,
unlike keywords which use original_case_keyword with policy-determined case)"

However, for keywords, the code sets:
token.original_case_keyword = display_case

But for identifiers, the code sets:
token.original_case = ident

This is consistent with the comment, but the Token class definition is not provided to verify these fields exist and are used correctly elsewhere.

---

#### code_vs_comment

**Description:** Comment claims 'MBASIC allows "PRINT#1" with no space' and describes special handling, but the implementation may not handle all file I/O keywords consistently

**Affected files:**
- `src/lexer.py`

**Details:**
Comment in read_identifier() says:
"Special case: File I/O keywords followed by # (e.g., PRINT#1)
MBASIC allows 'PRINT#1' with no space, which should tokenize as:
  PRINT (keyword) + # (operator) + 1 (number)"

The code checks:
if keyword_part in ['print', 'lprint', 'input', 'write', 'field', 'get', 'put', 'close']:

However, the comment earlier mentions 'PRINT# and INPUT#' specifically, but the list includes many more keywords. It's unclear if all these keywords actually support the # syntax in MBASIC 5.21.

---

#### code_vs_comment

**Description:** Comment claims RND and INKEY$ can be called without parentheses as MBASIC 5.21 behavior, but implementation only allows this for RND and INKEY$, not universally

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line 11-13 states:
"Exception: RND and INKEY$ can be called without parentheses (MBASIC 5.21 behavior)
Note: This is MBASIC-specific, not universal to all BASIC dialects"

Implementation at lines 1247-1258 shows:
- RND without parentheses: implemented (lines 1247-1254)
- INKEY$ without parentheses: implemented (lines 1256-1263)
- Other functions: require parentheses (line 1265)

This is consistent, but the comment placement in the module docstring suggests it's a general parsing note, when it's actually specific to these two functions.

---

#### code_vs_comment

**Description:** at_end_of_line() docstring contradicts its usage in statement parsing

**Affected files:**
- `src/parser.py`

**Details:**
Docstring at lines 373-378 states:
"Check if at end of logical line (NEWLINE or EOF)

Note: This method does NOT check for comment tokens (REM, REMARK, APOSTROPHE).
Comments are handled separately in parse_line() where they are parsed as
statements and can be followed by more statements when separated by COLON."

However, in parse_print() at line 1598 and parse_lprint() at line 1668, the method is used in conditions like:
"while not self.at_end_of_line() and not self.match(TokenType.COLON) and not self.match(TokenType.ELSE) and not self.match(TokenType.REM, TokenType.REMARK, TokenType.APOSTROPHE)"

This shows that at_end_of_line() does NOT check for comments, so they must be checked separately - which matches the docstring. But the docstring claim that "comments can be followed by more statements when separated by COLON" contradicts the parse_line() implementation at line 1493 which shows "break  # Comment ends the line".

---

#### code_vs_comment

**Description:** MID$ statement detection comment describes complex lookahead but implementation may have issues

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines 1004-1008 states:
"Look ahead to distinguish MID$ statement from MID$ function
MID$ statement has pattern: MID$ ( ... ) =
MID$ is tokenized as single MID token ($ is part of the keyword)
Complex lookahead: scan past parentheses (tracking depth) to find = sign"

The implementation at lines 1009-1034 saves position, advances past MID, checks for LPAREN, scans for matching RPAREN, then checks for EQUAL. However:
1. Line 1012 comment says "MID$ is a single token, no need to check for DOLLAR separately" but the code doesn't verify this
2. The lookahead advances position but on error (line 1031) it only restores position without proper error handling
3. Line 1035 comment says "If we get here, MID$ is being used in an unsupported way" but this could also be a MID$ function call in an expression context

---

#### code_vs_comment

**Description:** Comment describes incorrect field name for ShowSettingsStatementNode

**Affected files:**
- `src/parser.py`

**Details:**
In parse_showsettings() method:
Comment says: "Field name: 'pattern' (optional filter string)"
But the code creates: ShowSettingsStatementNode(pattern=pattern_expr, ...)
The comment is correct, but it's placed in a way that suggests documentation of the field name, which matches the code. However, the comment format is inconsistent with other methods that don't document field names this way.

---

#### code_vs_comment

**Description:** Comment describes incorrect field name for SetSettingStatementNode

**Affected files:**
- `src/parser.py`

**Details:**
In parse_setsetting() method:
Comment says: "Field name: 'setting_name' (string identifying setting)"
Code creates: SetSettingStatementNode(setting_name=setting_name_expr, ...)
The comment format suggests this is documentation, but it's inconsistent with other parse methods that don't include such field name documentation in comments.

---

#### code_vs_comment

**Description:** Comment describes MID token representation inconsistently with lexer behavior

**Affected files:**
- `src/parser.py`

**Details:**
In parse_mid_assignment() docstring:
"Note: The lexer tokenizes 'MID$' in source as a single MID token (the $ is part of the keyword, not a separate token)."

Then in the method body comment:
"token = self.current()  # MID token (represents 'MID$' from source)"

This suggests the lexer strips the $ from MID$, but the comment doesn't clarify whether the token value includes the $ or not. This could lead to confusion about token representation.

---

#### code_vs_comment

**Description:** Comment about LPRINT separators logic may have off-by-one confusion

**Affected files:**
- `src/parser.py`

**Details:**
In parse_lprint() method:
Comment says:
"# For N expressions: N-1 separators (between items) = no trailing separator
#                    N separators (between items + at end) = has trailing separator"

But the code that follows is:
if len(separators) < len(expressions):
    separators.append('\n')

This appends a newline when separators < expressions, which would be the N-1 case (no trailing separator). The logic seems correct but the comment's explanation of what constitutes 'trailing' vs 'no trailing' could be clearer about when the newline is added.

---

#### code_vs_comment

**Description:** Comment describes malformed FOR loop handling that changes semantics

**Affected files:**
- `src/parser.py`

**Details:**
In parse_for() docstring:
"Note: Some files may have malformed FOR loops like 'FOR 1 TO 100' (missing variable).
We handle this by creating a dummy variable 'I' to allow parsing to continue,
though this changes the semantics and may cause issues if variable I is referenced elsewhere."

This is a significant semantic change that could cause silent bugs. The comment acknowledges the issue but the code implements it anyway. This creates a situation where the parser accepts invalid syntax and silently changes program behavior, which could be considered a code bug rather than a feature.

---

#### code_vs_comment

**Description:** Comment claims COMMON statement stores variable names as strings, but code actually stores them as strings (consistent). However, the comment about array indicators is misleading.

**Affected files:**
- `src/parser.py`

**Details:**
In parse_common() method:
Comment says: "We consume the parentheses but don't need to store array dimension info (COMMON shares the entire array, not specific subscripts)"
Code does: variables.append(var_name) - stores just the name string

The comment is accurate about not storing dimension info, but the implementation doesn't distinguish between array and non-array variables in the stored list. The parentheses are consumed but the array nature is not preserved in the AST node.

---

#### code_vs_comment

**Description:** RESUME statement comment about RESUME 0 behavior may be misleading

**Affected files:**
- `src/parser.py`

**Details:**
Comment in parse_resume() says:
"# Note: RESUME 0 means 'retry error statement' (interpreter treats 0 and None equivalently)
# We store the actual value (0 or other line number) for the AST"

This suggests 0 and None are equivalent, but the code stores them differently (0 as integer, None as None). The comment claims the interpreter treats them equivalently, but this is parser code, not interpreter code. The distinction between storing 0 vs None in the AST could matter downstream.

---

#### code_vs_comment

**Description:** PC class docstring describes stmt_offset as '0-based index' but also calls it 'offset' which is confusing terminology

**Affected files:**
- `src/pc.py`

**Details:**
Docstring says: 'The stmt_offset is a 0-based index into the statements list for a line...Note: stmt_offset is the list index (position in the statements array). The term "offset" is used for historical reasons but it\'s simply the array index.'

This acknowledges the terminology is misleading but doesn't resolve it. The field is named 'stmt_offset' throughout the codebase but is actually an array index, not an offset in the traditional sense.

---

#### code_vs_documentation

**Description:** apply_keyword_case_policy docstring says 'Callers may pass keywords in any case' but implementation behavior varies by policy

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring states: 'Args:
    keyword: The keyword to transform (may be any case - function handles normalization internally)'

And: 'Note: The first_wins policy normalizes keywords to lowercase for lookup purposes. Other policies transform the keyword directly. Callers may pass keywords in any case.'

However, the 'first_wins' policy does normalize to lowercase for lookup (keyword_lower = keyword.lower()), while other policies like 'preserve' expect the caller to pass the correct case. The docstring claim that 'function handles normalization internally' is only partially true.

---

#### code_vs_comment

**Description:** emit_keyword docstring says 'Caller is responsible for normalizing keyword to lowercase' but apply_keyword_case_policy docstring says callers can pass any case

**Affected files:**
- `src/position_serializer.py`

**Details:**
emit_keyword docstring: 'Note: Caller is responsible for normalizing keyword to lowercase before calling.'

apply_keyword_case_policy docstring: 'Args:
    keyword: The keyword to transform (may be any case - function handles normalization internally)'

These two functions have contradictory expectations about who normalizes keywords.

---

#### code_vs_comment

**Description:** PositionSerializer.__init__ docstring says keyword_case_manager is 'from parser' but doesn't specify which parser attribute

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring: 'keyword_case_manager: KeywordCaseManager instance (from parser) with keyword case table'

And comment in code: '# Store reference to keyword case manager from parser'

But there's no indication of how to get this from the parser or what parser class is expected. This makes the API unclear for users of this class.

---

#### code_vs_comment

**Description:** Comment in check_array_allocation() states 'This calculation matches the array creation logic in src/interpreter.py execute_dim()' but the actual calculation uses (dim_size + 1) which may or may not match interpreter.py without verification

**Affected files:**
- `src/resource_limits.py`

**Details:**
Comment at line ~180: '# This calculation matches the array creation logic in src/interpreter.py execute_dim()'
Code calculates: total_elements *= (dim_size + 1)  # +1 for 0-based indexing

The comment claims this matches interpreter.py but we cannot verify this claim from the provided code. If interpreter.py uses different logic, memory tracking will be incorrect.

---

#### code_vs_documentation

**Description:** File system limits (max_open_files, max_file_size, max_total_files) are defined and documented but no tracking or enforcement methods are implemented

**Affected files:**
- `src/resource_limits.py`

**Details:**
Documented parameters:
- max_open_files: Maximum number of simultaneously open files
- max_file_size: Maximum size for a single file (bytes)
- max_total_files: Maximum number of files that can be created

These are initialized in __init__ and included in preset configurations, but there are no methods like:
- open_file() / close_file() to track current_open_files
- check_file_size() to enforce max_file_size
- check_total_files() to enforce max_total_files

Only current_open_files is tracked as an instance variable (line ~82) but never incremented or checked. This suggests incomplete implementation or that file tracking happens elsewhere.

---

#### code_vs_comment

**Description:** Comment claims line=-1 in last_write distinguishes system variables from debugger sets, but both use line=-1

**Affected files:**
- `src/runtime.py`

**Details:**
In __init__ docstring for _variables:
"Note: line -1 in last_write indicates non-program execution sources:
       1. System/internal variables (ERR%, ERL%) via set_variable_raw() with FakeToken(line=-1)
       2. Debugger/interactive prompt via set_variable() with debugger_set=True and token.line=-1
       Both use line=-1, making them indistinguishable in last_write alone."

But in set_variable_raw() docstring:
"The line=-1 marker in last_write distinguishes system variables from:
- Normal program execution (line >= 0)
- Debugger sets (also use line=-1, but via debugger_set=True)"

The first comment correctly states they are indistinguishable, but the second claims they are distinguished.

---

#### code_vs_comment

**Description:** get_variable() docstring says token is REQUIRED but allows fallback for missing attributes

**Affected files:**
- `src/runtime.py`

**Details:**
get_variable() docstring states:
"token: REQUIRED - Token object with line and position info for tracking.
       Must not be None (ValueError raised if None)."

But then continues:
"The token is expected to have 'line' and 'position' attributes.
If these attributes are missing, getattr() fallbacks are used:
- 'line' falls back to self.pc.line_num (or None if PC is halted)
- 'position' falls back to None"

This is contradictory - if the token is REQUIRED for tracking, why allow fallbacks for missing attributes? The fallback behavior suggests the token's attributes are optional, not the token itself.

---

#### code_vs_comment

**Description:** Docstring for get_execution_stack() contains misleading documentation about 'from_line' field

**Affected files:**
- `src/runtime.py`

**Details:**
The docstring states:
"For GOSUB calls:
{
    'type': 'GOSUB',
    'from_line': 60,      # DEPRECATED: Same as return_line (kept for compatibility)
    'return_line': 60,    # Line to return to after RETURN
    'return_stmt': 0      # Statement offset to return to
}

Note: 'from_line' is misleading and redundant with 'return_line'.
       Both contain the line number to return to (not where GOSUB was called from)."

However, the actual implementation shows:
result.append({
    'type': 'GOSUB',
    'from_line': entry.get('return_line', 0),  # Line to return to
    'return_line': entry.get('return_line', 0),
    'return_stmt': entry.get('return_stmt', 0)
})

The comment '# Line to return to' confirms both fields contain the return line, but the docstring's explanation that 'from_line' is "DEPRECATED" and "kept for compatibility" suggests it should perhaps be removed or that there's confusion about its purpose.

---

#### code_vs_comment

**Description:** reset_for_run() docstring claims it's 'like CLEAR + reload program' but implementation shows it preserves common_vars

**Affected files:**
- `src/runtime.py`

**Details:**
The docstring states:
"Reset runtime for RUN command - like CLEAR + reload program.

This preserves breakpoints but resets everything else, equivalent to:
- CLEAR (clear variables, arrays, files, DATA pointer, etc.)"

However, at the end of the implementation, there's a comment:
"# NOTE: self.common_vars is NOT cleared - preserved for CHAIN compatibility"

This means reset_for_run() does NOT reset "everything else" as claimed. The common_vars are preserved, which is not mentioned in the main docstring description. This could be intentional for CHAIN compatibility, but the docstring should explicitly mention this exception.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation about FILE scope settings availability

**Affected files:**
- `src/settings.py`
- `src/settings_definitions.py`

**Details:**
src/settings.py docstring says: 'Note: File-level settings infrastructure exists (file_settings dict, FILE scope), but there are currently no settings defined with FILE scope in settings_definitions.py, and there is no UI or command to manage per-file settings yet.'

However, src/settings.py get() method docstring says: 'Note: File-level settings infrastructure exists but is not yet fully implemented. The file_settings dict can be set programmatically and is checked first in precedence, but there is no UI or command to manage per-file settings. In normal usage, file_settings is empty and precedence falls through to project/global settings.'

The first says 'no settings defined with FILE scope', the second says 'can be set programmatically'. These statements are subtly different - one implies no definitions exist, the other implies programmatic use is possible.

---

#### code_vs_documentation_inconsistency

**Description:** Token.original_case_keyword field purpose conflicts with SimpleKeywordCase usage

**Affected files:**
- `src/tokens.py`
- `src/simple_keyword_case.py`

**Details:**
In src/tokens.py, Token dataclass has field 'original_case_keyword' documented as: 'Original case for keywords, determined by keyword case policy. Only set for keyword tokens (PRINT, IF, GOTO, etc.). Used by serializer to output keywords with consistent or preserved case style.'

However, src/simple_keyword_case.py docstring says: 'This is a simplified keyword case handler used by the lexer (src/lexer.py). It supports only three force-based policies: force_lower, force_upper, force_capitalize... For advanced policies (first_wins, preserve, error) via CaseKeeperTable, see KeywordCaseManager'

The Token field mentions 'preserved case style' but SimpleKeywordCase only supports force-based policies, not preservation. This suggests either:
1. The Token field documentation is too broad
2. SimpleKeywordCase should support preservation
3. KeywordCaseManager sets this field differently

---

#### documentation_inconsistency

**Description:** keywords.case_style setting choices don't match SimpleKeywordCase policies

**Affected files:**
- `src/settings_definitions.py`

**Details:**
In settings_definitions.py, keywords.case_style has:
'choices=["force_lower", "force_upper", "force_capitalize"]'

But the help_text says: 'lowercase (MBASIC 5.21), UPPERCASE (classic), or Capitalize (modern)'

The help text uses different terminology (lowercase/UPPERCASE/Capitalize) than the actual choice values (force_lower/force_upper/force_capitalize). While the meaning is clear, this inconsistency could confuse users who see 'lowercase' in help but need to type 'force_lower' as the value.

---

#### Documentation inconsistency

**Description:** CLI STEP command documentation claims it implements statement-level stepping 'similar to the curses UI Step Statement command (Ctrl+T)', but the curses keybindings show Ctrl+K is for 'Step Line' and Ctrl+T is for 'Step statement'. The CLI documentation mentions 'Step Line' (Ctrl+K) is not available in CLI, but doesn't acknowledge that CLI STEP is supposed to match Ctrl+T behavior.

**Affected files:**
- `src/ui/cli_debug.py`
- `src/ui/curses_keybindings.json`

**Details:**
cli_debug.py docstring says:
"This implements statement-level stepping similar to the curses UI 'Step Statement'
command (Ctrl+T). The curses UI also has a separate 'Step Line' command (Ctrl+K)
which is not available in the CLI."

curses_keybindings.json shows:
"step_line": { "keys": ["Ctrl+K"], "description": "Step Line (execute all statements on current line)" }
"step": { "keys": ["Ctrl+T"], "description": "Step statement (execute one statement)" }

The CLI doc correctly identifies Ctrl+T as statement-level and Ctrl+K as line-level, but the phrasing could be clearer.

---

#### Code vs Comment conflict

**Description:** The _execute_single_step() method's docstring claims it executes 'one statement at the current program counter position' and that tick()/execute_next() are 'expected to advance the program counter by one statement', but then contradicts itself by noting 'If the interpreter executes full lines instead, this method will behave as line-level stepping rather than statement-level.'

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
Docstring states:
"Execute a single statement (not a full line).

Uses the interpreter's tick() or execute_next() method to execute
one statement at the current program counter position.

Note: The actual statement-level granularity depends on the interpreter's
implementation of tick()/execute_next(). These methods are expected to
advance the program counter by one statement, handling colon-separated
statements separately. If the interpreter executes full lines instead,
this method will behave as line-level stepping rather than statement-level."

This is contradictory - it claims to execute one statement but admits it might execute a full line depending on implementation. The uncertainty suggests either the code doesn't guarantee statement-level stepping or the comment is outdated.

---

#### Code vs Documentation inconsistency

**Description:** The cmd_step() docstring says 'After each step, displays the current line number in format: [{line_num}]' but the implementation only displays this format when current_line exists. If current_line is None, no output is shown, which could be confusing to users.

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
Docstring claims:
"After each step, displays the current line number in format: [{line_num}]"

Implementation:
"# Show current position
if self.interactive.program_runtime.current_line:
    line_num = self.interactive.program_runtime.current_line.line_number
    self.interactive.io_handler.output(f'[{line_num}]')"

The conditional check means the format is not always displayed, contradicting the documentation.

---

#### code_vs_comment

**Description:** Comment describes 3-field format but implementation varies between methods

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Class docstring at line 142 describes format as: "S<linenum> CODE" with variable-width line numbers.

_format_line() at line 449 implements: prefix = f"{status}{line_num_str} " (variable width)

_parse_line_numbers() at line 991 implements: new_line = f" {line_num_formatted} {rest}" where line_num_formatted = f"{num_str:>5}" (fixed 5-char width)

The format is inconsistent between display and paste reformatting.

---

#### code_vs_comment

**Description:** Comment claims _parse_line_number extracts variable-width line numbers, but _parse_line_numbers reformats to fixed width

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
_parse_line_number() docstring at line 183: "Extract line number from display line.
Format: 'SNN CODE' where S=status, NN=line number (variable width)"

_parse_line_numbers() docstring at line 953: "Note: When reformatting pasted content, line numbers are right-justified to 5 characters
for consistent alignment. This differs from the variable-width formatting used in
_format_line() for display."

This creates a mismatch where display uses variable width but paste handling uses fixed width, potentially causing alignment issues.

---

#### code_vs_comment

**Description:** Comment claims ImmediateExecutor is recreated in start() but interpreter is reused, but code shows interpreter is also created once in __init__ and reused

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~180 says: 'ImmediateExecutor Lifecycle: Created here with temporary IO handler (to ensure attribute exists), then recreated in start() with a fresh OutputCapturingIOHandler. Note: The interpreter (self.interpreter) is created once here and reused. Only the executor and its IO handler are recreated in start().'

However, the code in start() method (line ~200) shows:
immediate_io = OutputCapturingIOHandler()
self.immediate_executor = ImmediateExecutor(self.runtime, self.interpreter, immediate_io)

This confirms the comment is accurate - interpreter is reused, only executor is recreated. But earlier comment at line ~170 says 'Interpreter Lifecycle: Created ONCE here in __init__ and reused throughout the session. The interpreter is NOT recreated in start()' which is redundant with the later comment.

---

#### code_vs_comment

**Description:** Comment about IO handler lifecycle mentions two handlers but describes three

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~150 says: 'IO Handler Lifecycle: 1. self.io_handler (CapturingIOHandler) - Used for RUN program execution... 2. immediate_io (OutputCapturingIOHandler) - Used for immediate mode commands...'

But the code also uses self.io_handler (passed to __init__ from parent class) which is a third IO handler. The comment only describes the two created locally (CapturingIOHandler for runs and OutputCapturingIOHandler for immediate mode) but doesn't mention the original self.io_handler parameter from the constructor signature at line ~90: 'def __init__(self, io_handler: IOHandler, program_manager: ProgramManager)'

---

#### code_vs_comment

**Description:** Comment about help widget lifecycle contradicts toggle support claim

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _show_help() docstring at line ~840: 'Note: Unlike _show_keymap and _show_settings which support toggling, help doesn't store overlay state so it can't be toggled off. The help widget handles its own close behavior via ESC/Q keys.'

But in _show_keymap() docstring at line ~870: 'This method supports toggling - calling it when keymap is already open will close it.'

The comment claims help doesn't support toggling while keymap does, but the implementation shows _show_help() doesn't check for existing overlay state (no hasattr check like _show_keymap has). This is consistent with the comment, but the comment in _show_help() also says 'Help closes via ESC/Q handled internally by HelpWidget' which suggests the widget manages its own lifecycle, making the comparison to keymap/settings potentially misleading.

---

#### code_vs_comment

**Description:** Comment claims breakpoints are stored in editor and NOT in runtime, but code shows breakpoints ARE cleared by reset_for_run() and must be re-applied

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1090 says:
"Note: reset_for_run() clears variables and resets PC. Breakpoints are stored in
the editor (self.editor.breakpoints), NOT in runtime, so they persist across runs
and are re-applied below via interpreter.set_breakpoint() calls."

But immediately after at line ~1110, code shows:
"# Re-apply breakpoints from editor
# Breakpoints are stored in editor UI state and must be re-applied to interpreter
# after reset_for_run (which clears them)
for line_num in self.editor.breakpoints:
    self.interpreter.set_breakpoint(line_num)"

The comment contradicts itself - it says breakpoints are NOT in runtime and persist, but then the code explicitly re-applies them BECAUSE reset_for_run() clears them from the interpreter/runtime.

---

#### code_vs_comment

**Description:** Docstring claims toggle behavior but implementation shows asymmetric open/close logic

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _show_settings() docstring at line ~770:
"Toggle settings editor.

This method supports toggling - calling it when settings is already open will close it."

However, the implementation shows complex overlay management with _settings_overlay and _settings_main_widget attributes, alarm-based signal checking, and custom input handlers. The 'toggle' behavior is not symmetric - opening involves creating overlays, setting alarms, and custom handlers, while closing just restores widgets. This is more of an 'open or close' method than a true toggle.

---

#### code_vs_comment

**Description:** Comment about PC preservation logic contradicts the actual condition check

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _sync_program_to_runtime() at line ~1260:
"# Restore PC only if execution is running AND not paused at breakpoint
# (paused programs need PC reset to current breakpoint location)
# Otherwise ensure halted (don't accidentally start execution)
if self.running and not self.paused_at_breakpoint:
    # Execution is running - preserve execution state
    self.runtime.pc = old_pc
    self.runtime.halted = old_halted
else:
    # No execution in progress - ensure halted
    self.runtime.pc = PC.halted_pc()
    self.runtime.halted = True"

The comment says 'paused programs need PC reset to current breakpoint location' but the else branch sets PC to halted_pc(), not to any breakpoint location. This suggests the comment is misleading about what happens when paused_at_breakpoint is True.

---

#### code_vs_comment

**Description:** Comment claims DELETE and RENUM update self.program immediately and runtime sync occurs automatically via _execute_immediate, but the code shows runtime=None is passed to helper functions, meaning runtime is never synced at all during these operations

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In cmd_delete docstring:
"Note: Updates self.program immediately (source of truth). Runtime sync occurs
automatically via _execute_immediate which calls _sync_program_to_runtime before
executing any immediate command. This ensures runtime is always in sync when needed."

But the code calls:
deleted = delete_lines_from_program(self.program, args, runtime=None)

And in cmd_renum:
old_lines, line_map = renum_program(
    self.program,
    args,
    self.interpreter.interactive_mode._renum_statement,
    runtime=None
)

Passing runtime=None means the runtime is never updated by these helper functions. The comment suggests _execute_immediate will sync later, but these commands are called directly via cmd_delete/cmd_renum, not necessarily through _execute_immediate.

---

#### code_internal_inconsistency

**Description:** Duplicate CapturingIOHandler class definition in _execute_immediate with comment acknowledging duplication but not fixing it

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _execute_immediate method:
"# Need to create the CapturingIOHandler class inline
# (duplicates definition in _run_program - consider extracting to shared location)
class CapturingIOHandler:"

The comment explicitly states this is a duplicate of code in _run_program and should be extracted, but the duplication remains. This violates DRY principle and creates maintenance burden.

---

#### code_internal_inconsistency

**Description:** Inconsistent output methods used: _write_output in cmd_* methods vs output_walker.append in _execute_immediate

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In cmd_save, cmd_delete, cmd_renum, cmd_merge, cmd_files, cmd_cont:
self._write_output("message\n")

But in _execute_immediate:
self.output_walker.append(make_output_line(f"> {command}"))
self.output_walker.append(make_output_line(line))

This inconsistency suggests different output mechanisms are used in different contexts, which could lead to output appearing in different places or with different formatting.

---

#### code_internal_inconsistency

**Description:** Autosave interval hardcoded to 30 seconds in multiple places instead of using a constant or configuration

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _save_program:
self.auto_save.start_autosave(
    filename,
    self._get_editor_content,
    interval=30
)

In _save_as_program:
self.auto_save.start_autosave(
    filename,
    self._get_editor_content,
    interval=30
)

In _load_program:
self.auto_save.start_autosave(
    filename,
    self._get_editor_content,
    interval=30
)

The magic number 30 is repeated three times. This should be a constant or configuration value.

---

#### code_vs_comment_conflict

**Description:** Docstring for _expand_kbd() describes searching across all sections, but implementation detail about 'action name' vs 'key name' terminology is inconsistent

**Affected files:**
- `src/ui/help_macros.py`

**Details:**
The _expand_kbd() method docstring (lines 77-91) uses inconsistent terminology:
- Parameter name: "key_name: Name of key action (e.g., 'help', 'save', 'run')"
- Description: "This is searched across all keybinding sections"
- Example: "_expand_kbd('help') searches all sections for an action named 'help'"

The parameter is called 'key_name' but the docstring describes it as 'action name' or 'key action'. This is confusing - it should consistently use 'action' terminology since that's what the keybindings JSON structure uses (actions within sections).

---

#### code_vs_comment_conflict

**Description:** Comment in fmt_key() function claims limitation only handles Ctrl+ prefix, but this may be intentional design rather than limitation

**Affected files:**
- `src/ui/interactive_menu.py`

**Details:**
The fmt_key() docstring (lines 33-46) states:
"Limitation: Only handles 'Ctrl+' prefix. Other formats like 'Alt+X',
'Shift+Ctrl+X', or 'F5' are returned unchanged. This is acceptable for
the curses menu which primarily uses Ctrl+ keybindings."

This is described as a 'Limitation' but the comment also says it's 'acceptable'. The function is working as designed for the curses menu's needs. The term 'limitation' suggests a deficiency, but the implementation is intentionally simple because the curses menu only uses Ctrl+ shortcuts. This should be clarified as intentional design rather than a limitation.

---

#### code_inconsistency

**Description:** HelpWidget hardcodes 'curses' UI name but HelpMacros is designed to be UI-agnostic

**Affected files:**
- `src/ui/help_widget.py`
- `src/ui/help_macros.py`

**Details:**
In help_widget.py line 48:
"# HelpWidget is curses-specific (uses urwid), so hardcode 'curses' UI name
self.macros = HelpMacros('curses', help_root)"

However, HelpMacros class in help_macros.py is designed to be UI-agnostic, accepting ui_name as a parameter (line 18). The HelpWidget could receive ui_name as a parameter instead of hardcoding it, making the code more flexible. While the comment explains why it's hardcoded (urwid is curses-specific), this creates tight coupling that could be avoided.

---

#### code_vs_comment

**Description:** Variable name LIST_KEY doesn't match its actual functionality

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Comment says: "Note: Variable named LIST_KEY for historical reasons (it was originally associated with BASIC's LIST command). This variable now implements step_line debugger functionality, which executes all statements on the current line before pausing again. The variable name doesn't match its current purpose but is retained for backward compatibility."

Code: LIST_KEY = _ctrl_key_to_urwid(_list_key)

The variable is loaded from 'step_line' action in JSON but named LIST_KEY, creating confusion.

---

#### code_vs_comment

**Description:** CONTINUE_KEY comment describes dual functionality but implementation doesn't show context-sensitivity

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Comment says: "Note: This key (typically Ctrl+G) is context-sensitive in the UI:
  - In debugger mode: Continue execution until next breakpoint or end
  - In editor mode: Go to line number (not yet implemented)
Loaded from 'goto_line' action in JSON since both uses share the same key."

Code: _continue_key = _get_key('editor', 'goto_line') or 'Ctrl+G'
CONTINUE_KEY = _ctrl_key_to_urwid(_continue_key)

The comment describes context-sensitive behavior, but the keybindings.py module only defines the key constant. The actual context-sensitive logic must be implemented elsewhere, but this isn't clear from the code.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation of Stack window access method

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
In constants section:
STACK_KEY = ''  # No keyboard shortcut
STACK_CHAR = ''
STACK_DISPLAY = 'Menu only'
Comment: "Note: No keyboard shortcut is assigned to avoid conflicts with editor typing. The stack window is accessed via the menu system (Ctrl+U -> Debug -> Execution Stack)."

In KEYBINDINGS_BY_CATEGORY:
(STACK_DISPLAY, 'Toggle execution stack window')

The description 'Toggle execution stack window' implies it can be toggled with a key, but STACK_DISPLAY is 'Menu only' and STACK_KEY is empty. The documentation should say 'Show/hide execution stack window (menu only)' for consistency.

---

#### code_vs_documentation

**Description:** keymap_widget.py converts Ctrl+ to ^ notation but keybindings.py already has STATUS_BAR_SHORTCUTS in ^ notation

**Affected files:**
- `src/ui/keybindings.py`
- `src/ui/keymap_widget.py`

**Details:**
In keybindings.py:
STATUS_BAR_SHORTCUTS = "MBASIC - ^F help  ^U menu  ^W vars  ^K step line  Tab cycle  ^Q quit"

In keymap_widget.py:
def _format_key_display(key_str):
    """Convert Ctrl+ notation to ^ notation for consistency."""
    if key_str.startswith('Ctrl+'):
        return '^' + key_str[5:]

This suggests there's inconsistency in the source data format. Some places use ^X notation, others use Ctrl+X notation. The conversion function exists to normalize this, but it would be cleaner to have consistent notation in the source.

---

#### Code vs Documentation inconsistency

**Description:** ESC key binding to close in-page search is implemented but not documented in keybindings

**Affected files:**
- `src/ui/tk_help_browser.py`
- `src/ui/tk_keybindings.json`

**Details:**
In tk_help_browser.py line 127-128:
# Note: ESC closes search bar - this is not documented in tk_keybindings.json
# as it's a local widget binding rather than a global application keybinding
self.inpage_search_entry.bind('<Escape>', lambda e: self._inpage_search_close())

The tk_keybindings.json file has a 'help_browser' section with 'search' and 'inpage_search' keys, but does not document the ESC key binding for closing the in-page search bar. While the comment explains this is intentional (local vs global binding), this creates an inconsistency where users looking at the keybindings file won't find this documented shortcut.

---

#### code_vs_comment

**Description:** Comment describes 4-pane layout but implementation has 3 panes plus conditional INPUT row

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring says:
"    - 4-pane vertical layout:
      * Editor with line numbers (top, ~50% - weight=3)
      * Output pane (middle, ~33% - weight=2)
      * INPUT row (shown only for INPUT statements, hidden otherwise)
      * Immediate mode input line (bottom, ~17% - weight=1)"

But code creates 3 PanedWindow panes:
1. editor_frame (weight=3)
2. output_frame (weight=2)
3. immediate_frame (weight=1)

The INPUT row is created inside output_frame and shown/hidden dynamically, not as a separate pane.

---

#### code_vs_comment

**Description:** Docstring describes syntax highlighting as 'optional' but no implementation or configuration for it exists

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring line ~50 says:
"    - Syntax highlighting (optional)"

But there is no code implementing syntax highlighting, no configuration option to enable/disable it, and no mention of it being a planned feature. This suggests either:
1. Feature was removed but docstring not updated
2. Feature is planned but not yet implemented
3. Feature exists elsewhere but not in this file

---

#### code_vs_comment

**Description:** Variables window heading initialization doesn't match comment about default sort column

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
At line ~138, instance variable is initialized:
self.variables_sort_column = 'accessed'  # Current sort column: 'accessed', 'written', 'read', 'name', 'type', or 'value'

But at line ~730, the tree heading is set:
tree.heading('#0', text='↓ Variable (Last Accessed)')

And comment at line ~729 says:
"# Set initial heading text with arrows (matches self.variables_sort_column default: 'accessed')"

This is actually consistent, but the comment lists 'written', 'read', 'name', 'type', 'value' as possible sort columns. However, the code only implements sorting by 'accessed' initially, and there's no visible implementation of the other sort modes in this file fragment. This suggests either incomplete implementation or the other modes are implemented elsewhere.

---

#### code_vs_comment

**Description:** Variables tree column headings comment describes sorting behavior but implementation is incomplete in provided code

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at lines ~751-754:
"Handle clicks on variable list column headings.

Arrow area (left ~20 pixels): Toggle sort direction
Rest of heading: Cycle sort column (for Variable) or set column (for Type/Value)"

Code at lines ~779-783 shows:
if column == '#0':  # Variable column - only sortable column
    self._cycle_variable_sort()
# Type and Value columns are not sortable

This conflicts with the comment saying 'set column (for Type/Value)' - the code explicitly says Type and Value are NOT sortable. The comment is misleading.

---

#### code_vs_comment

**Description:** Comment claims auto-numbering is only called from _on_enter_key, but this contradicts the purpose of the method

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1180 states:
"Currently called only from _on_enter_key (after each Enter key press), not
after pasting or other modifications."

However, the method _remove_blank_lines() is designed to clean up blank lines in general. The comment suggests it's intentionally limited to Enter key presses, but this seems like an implementation limitation rather than a design choice. The method's docstring says it removes blank lines to "keep program clean" which suggests it should be called more broadly.

---

#### code_vs_comment

**Description:** Comment about validation timing contradicts implementation details

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
At line ~1140, comment states:
"# Note: This method is called with a delay (100ms) after cursor movement/clicks
# to avoid excessive validation during rapid editing"

But looking at _on_cursor_move() at line ~1175:
"self.root.after(100, self._validate_editor_syntax)"

And _on_mouse_click() at line ~1185:
"self.root.after(100, self._validate_editor_syntax)"

The 100ms delay is implemented in the callers, not in _validate_editor_syntax itself. The comment in _validate_editor_syntax makes it sound like the delay is part of that method's implementation, when it's actually the responsibility of the callers. This could be misleading for future maintainers.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of yellow statement highlight clearing

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
At line ~1183 in _on_mouse_click():
"# Clear yellow statement highlight when clicking (allows text selection to be visible)
if self.paused_at_breakpoint:
    self._clear_statement_highlight()"

But in _on_cursor_move() at line ~1177, there is no similar clearing of the yellow highlight. This means:
- Mouse click clears yellow highlight
- Arrow keys/cursor movement does NOT clear yellow highlight

This inconsistency in behavior could be confusing to users. Either both should clear it, or neither should (or there should be a comment explaining why the behavior differs).

---

#### code_vs_comment

**Description:** Comment claims clearing statement highlight on ANY key prevents visual artifacts, but code only clears when paused_at_breakpoint is True

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1180 says:
# Clear yellow statement highlight on any keypress when paused at breakpoint
# This prevents visual artifact where statement highlight remains on part of a line
# after text is modified (occurs because highlight is tag-based and editing shifts positions).
# Note: This clears on ANY key including arrows/function keys, not just editing keys.

But code implementation:
if self.paused_at_breakpoint:
    self._clear_statement_highlight()

The comment emphasizes 'ANY key' but the clearing only happens when paused_at_breakpoint is True, which is a specific state condition not mentioned in the comment's emphasis.

---

#### code_vs_comment

**Description:** Comment claims DON'T save to program yet because blank lines would be filtered, but this contradicts the auto-numbering behavior where numbered blank lines should be valid

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1490 in _smart_insert_line says:
# DON'T save to program yet - the line is blank and would be filtered out by
# _save_editor_to_program() which skips blank lines. Just position the cursor on
# the new line so user can start typing.

However, the inserted line has a line number (f'{insert_num} \n'), so it's not truly blank - it's a numbered line with no code. The comment suggests _save_editor_to_program() would filter it, but numbered lines (even without code) might be handled differently than truly blank lines. This creates ambiguity about what constitutes a 'blank line' for filtering purposes.

---

#### code_vs_comment

**Description:** Comment describes line change detection logic but doesn't mention the critical 'old_line_num is None' check that prevents unnecessary sorting

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1340 says:
# Determine if program needs to be re-sorted:
# 1. Line number changed on existing line (both old and new are not None), OR
# 2. Line number was removed (old was not None, new is None and line has content)
#
# Don't trigger sort when:
# - old_line_num is None: First time tracking this line (cursor just moved here, no editing yet)
# - This prevents unnecessary re-sorting when user clicks around without making changes

The comment correctly describes the logic, but the emphasis on 'old_line_num is None' preventing sorts is buried in the 'Don't trigger' section. The actual code logic at line ~1350 shows this is a critical condition:

if old_line_num != new_line_num:
    if old_line_num is not None and new_line_num is not None:
        should_sort = True
    elif old_line_num is not None and new_line_num is None and current_text.strip():
        should_sort = True

The comment structure suggests cases 1 and 2 are the primary logic, but the 'old_line_num is None' check is actually the primary gate that prevents most false triggers.

---

#### code_vs_comment

**Description:** Comment in _update_immediate_status explains dual check for can_execute but the explanation about race conditions may be incomplete

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1780 says:
# Check if safe to execute - use both can_execute_immediate() AND self.running flag
# The 'not self.running' check prevents immediate mode execution when a program is running,
# even if the tick hasn't completed yet. This prevents race conditions where immediate
# mode could execute while the program is still running but between tick cycles.

The comment describes preventing execution 'between tick cycles', but the code is in _update_immediate_status which updates UI state. The actual prevention mechanism (disabling the input widget) happens after this check. The comment suggests this check prevents execution, but it only determines UI state - the actual execution prevention would need to be in the immediate mode execution handler.

---

#### code_vs_comment

**Description:** Comment claims immediate_history is always None but _setup_immediate_context_menu() and related methods reference it as if it could be a widget

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _add_immediate_output() docstring: "Note: self.immediate_history exists but is always None (see __init__) - it's a dummy attribute for compatibility with code that references it."

But _setup_immediate_context_menu() contains: "menu = tk.Menu(self.immediate_history, tearoff=0)" and "self.immediate_history.tag_ranges(tk.SEL)" which would fail if immediate_history is None.

Similarly, _copy_immediate_selection() and _select_all_immediate() call methods on self.immediate_history that would raise AttributeError if it's None.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation about immediate mode output destination

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
_add_immediate_output() docstring says: "This method name is historical - it simply forwards to _add_output(). In the Tk UI, immediate mode output goes to the main output pane."

But _execute_immediate() comment says: "Execute without echoing (GUI design choice: command is visible in entry field, and 'Ok' prompt is unnecessary in GUI context - only results are shown)"

This creates confusion about whether immediate mode has its own output area or shares the main output pane. The docstring says it goes to main output, but the existence of _add_immediate_output() as a separate method and the 'historical' comment suggests there may have been a separate immediate output area previously.

---

#### code_vs_comment

**Description:** Comment about has_work() usage doesn't match actual usage pattern in codebase

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment in _execute_immediate() states: "Use has_work() to check if the interpreter is ready to execute (e.g., after RUN command). This complements runtime flag checks (self.running, runtime.halted) used elsewhere."

However, the code immediately after checks has_work() and then checks 'if not self.running' to decide whether to start execution. This suggests has_work() is not complementing but rather preceding the runtime flag checks. The comment implies they work together, but the code shows has_work() is checked first, then runtime flags are used conditionally.

---

#### code_vs_comment

**Description:** Comment in _parse_line_number() states MBASIC 5.21 requires whitespace between line number and statement, but regex allows line number at end of string with no statement

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment says: "Note: '10REM' would not match (MBASIC 5.21 requires whitespace between line number and statement)"

But regex is: r'^(\d+)(?:\s|$)'

This regex matches '10' alone ($ = end of string) with no statement following, which contradicts the comment's implication that a statement must follow with whitespace. The comment suggests '10REM' is invalid due to missing whitespace, but doesn't clarify if '10' alone is valid.

---

#### code_vs_comment

**Description:** Comment in _delete_line() docstring describes parameter as 'Tkinter text widget line number (1-based sequential index)' but implementation uses it in f-string format that expects 1-based line numbers, while Tkinter text widget line numbers are actually 1-based

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Docstring says: "line_num: Tkinter text widget line number (1-based sequential index), not BASIC line number (e.g., 10, 20, 30)"

The clarification is correct that it's not a BASIC line number, and Tkinter text widget lines are indeed 1-based (line 1 is first line). However, the phrasing '1-based sequential index' might be confusing since 'index' often implies 0-based in programming contexts. The implementation correctly uses 1-based line numbers: self.text.get(f'{line_num}.0', f'{line_num}.end')

---

#### code_vs_comment

**Description:** Class docstring says 'automatic blank line removal' happens 'when cursor moves away from a blank line', but implementation in _on_cursor_move() uses after_idle() which delays deletion until after event processing

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Docstring: "When cursor moves away from a blank line, that line is automatically deleted"

Implementation: self.text.after_idle(self._delete_line, self.current_line)

The docstring implies immediate deletion when moving away, but the code schedules deletion for after idle time. This is a technical implementation detail that affects timing - the line isn't deleted 'when' the cursor moves, but 'shortly after' when the event loop is idle. This could matter for understanding behavior during rapid cursor movements or programmatic text changes.

---

#### code_vs_comment

**Description:** Comment in update_line_references() describes pattern as using non-greedy match for ON expressions, but warns about potential issues with expressions containing 'G'. However, the non-greedy match should handle this correctly.

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment states: "Note: Pattern uses .+? (non-greedy) to match expression in ON statements,
which allows expressions containing any characters including 'G' (e.g., ON FLAG GOTO)"

The comment suggests this is a workaround, but non-greedy matching is the correct approach. The comment could be clearer about why this works rather than suggesting it's a potential issue.

---

#### code_vs_comment

**Description:** serialize_line() comment warns about fallback behavior causing inconsistent indentation, but doesn't explain when this occurs or how to prevent it

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment states:
"# Note: If source_text doesn't match pattern, falls back to relative_indent=1
# This can cause inconsistent indentation for programmatically inserted lines"

This warning suggests a known issue but provides no guidance on how to handle programmatically inserted lines correctly. Should there be a way to set source_text for new lines?

---

#### code_vs_comment

**Description:** serialize_variable() comment about explicit_type_suffix uses getattr with False default, but doesn't explain when explicit_type_suffix attribute is set or missing

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Code comment:
"# Only add type suffix if it was explicit in the original source
# Don't add suffixes that were inferred from DEF statements
# Note: getattr defaults to False if explicit_type_suffix is missing, preventing suffix output"

The comment explains the behavior but doesn't document when/where explicit_type_suffix should be set during parsing. This makes it unclear how to properly construct VariableNode objects.

---

### 🟢 Low Severity

#### documentation_inconsistency

**Description:** Version number interpretation inconsistency

**Affected files:**
- `setup.py`
- `medium_severity_fixes.py`

**Details:**
setup.py states:
version="0.99.0",  # Reflects ~99% implementation status (core complete)

This comment suggests 0.99.0 means "approximately 99% complete", but semantic versioning convention would interpret 0.99.0 as major version 0, minor version 99, patch 0 - not a percentage. The comment creates confusion about whether this is semantic versioning or percentage-based versioning.

---

#### code_vs_comment

**Description:** CallStatementNode comment claims parser always sets arguments to empty list, but field exists

**Affected files:**
- `src/ast_nodes.py`

**Details:**
CallStatementNode docstring:
"Note: The 'arguments' field is reserved for potential future compatibility with
other BASIC dialects (e.g., CALL ROUTINE(args)). The parser does not currently
populate this field (always empty list). Standard MBASIC 5.21 only accepts
a single address expression in the 'target' field."

The comment states the parser "always" sets arguments to empty list, but the field definition is:
arguments: List['ExpressionNode']  # Reserved for future (parser always sets to empty list)

If the parser truly always sets it to empty list, the field should have a default value of field(default_factory=list) or the comment should clarify this is a runtime invariant that must be maintained by the parser, not enforced by the dataclass definition.

---

#### documentation_inconsistency

**Description:** VarType docstring uses inconsistent terminology for type specification methods

**Affected files:**
- `src/ast_nodes.py`

**Details:**
VarType docstring:
"Types are specified by suffix characters or DEF statements:
- INTEGER: % suffix (e.g., COUNT%) or DEFINT A-Z
- SINGLE: ! suffix (e.g., VALUE!) or DEFSNG A-Z (default type)
- DOUBLE: # suffix (e.g., TOTAL#) or DEFDBL A-Z
- STRING: $ suffix (e.g., NAME$) or DEFSTR A-Z"

The phrase "or DEF statements" in the first line is inconsistent with the examples which use "or DEFINT A-Z" format. It should either say "or DEF type statements" or the examples should say "or DEF statements (DEFINT A-Z)" to maintain parallel structure.

---

#### code_vs_comment

**Description:** VariableNode explicit_type_suffix field comment example may be confusing

**Affected files:**
- `src/ast_nodes.py`

**Details:**
VariableNode docstring:
"Type suffix handling:
- type_suffix: The actual suffix character ($, %, !, #)
- explicit_type_suffix: True if suffix appeared in source code, False if inferred from DEF

Example: In "DEFINT A-Z: X=5", variable X has type_suffix='%' and explicit_type_suffix=False.
The suffix must be tracked but not regenerated in source code."

The example says "The suffix must be tracked but not regenerated in source code" which could be interpreted as "never regenerate any suffix" or "don't regenerate implicit suffixes". The comment should clarify that explicit_type_suffix=True means the suffix SHOULD be regenerated, while False means it should NOT be regenerated.

---

#### documentation_inconsistency

**Description:** TypeInfo class docstring describes it as both a facade and a utilities class

**Affected files:**
- `src/ast_nodes.py`

**Details:**
TypeInfo docstring:
"Type information utilities for variables

Provides convenience methods for working with VarType enum and converting
between type suffixes, DEF statement tokens, and VarType enum values.

This class provides a facade over VarType with two purposes:
1. Static helper methods for type conversions
2. Class attributes (INTEGER, SINGLE, etc.) that expose VarType enum values
   for backward compatibility with code that uses TypeInfo.INTEGER instead
   of VarType.INTEGER"

The first paragraph calls it "utilities" while the third paragraph calls it a "facade". These are different design patterns. The description should be consistent - either it's a utility class with static methods, or it's a facade providing a simplified interface to VarType.

---

#### code_vs_comment

**Description:** Comment about trailing_minus_only behavior is redundant and potentially confusing

**Affected files:**
- `src/basic_builtins.py`

**Details:**
At line 237, the comment states:
# trailing_minus_only: - at end only (always adds 1 char: - or space)
This same information is repeated in the docstring at lines 227-229. The inline comment adds '(always 1 char)' which could be clearer as 'always adds exactly 1 character position'.

---

#### code_vs_comment

**Description:** Comment about file handle extraction is overly verbose and could be simplified

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Lines 825-828 contain a lengthy comment:
# self.runtime.files[file_num] returns a dict with 'handle', 'mode', 'eof' keys
# Extract the file handle from the file_info dict to perform read operations
# (this pattern is used by EOF(), LOC(), LOF(), and other file functions)

This is immediately followed by the exact code it describes (lines 829-830). The comment is redundant given the clear variable names used.

---

#### documentation_inconsistency

**Description:** Module docstring claims to document MBASIC 5.21 but doesn't specify what version features are included

**Affected files:**
- `src/basic_builtins.py`

**Details:**
The module docstring states:
Built-in functions for MBASIC 5.21.

But there's no documentation about which specific MBASIC 5.21 features are implemented vs. omitted, or how the implementation differs from the original. For example, PEEK returns random values rather than actual memory, but this deviation isn't mentioned in the module-level docs.

---

#### code_vs_comment

**Description:** Inconsistent comment style for sign behavior documentation

**Affected files:**
- `src/basic_builtins.py`

**Details:**
The parse_numeric_field function has a docstring at lines 226-231 explaining sign behavior:
Sign behavior:
- leading_sign: + at start, adds + or - sign
- trailing_sign: + at end, adds + or - sign
- trailing_minus_only: - at end, adds - for negative or space for non-negative (always 1 char)

But the spec dict at lines 233-247 has inline comments that partially repeat this information with slightly different wording. The inline comment at line 237 says 'always adds 1 char: - or space' while the docstring says 'always 1 char'. This inconsistency in terminology could cause confusion.

---

#### code_vs_comment

**Description:** InMemoryFileHandle.flush() comment describes behavior that differs from typical file semantics

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
The flush() method comment states:
"Note: This calls StringIO/BytesIO flush() which are no-ops. Content is only saved to the virtual filesystem on close(). This differs from file flush() semantics where flush() typically persists buffered writes. For in-memory files, all writes are already in memory, so flush() has no meaningful effect."

This is accurate documentation of the implementation, but creates an inconsistency with the FileHandle abstract interface which doesn't document this limitation. Code calling flush() on a FileHandle would expect standard flush semantics (immediate persistence), but InMemoryFileHandle silently defers until close(). This could cause data loss if the program crashes between flush() and close().

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for ProgramManager's relationship to Web UI

**Affected files:**
- `src/editing/manager.py`

**Details:**
The module docstring states:
"Note: Not suitable for Web UI due to direct filesystem access - Web UI uses FileIO abstraction in interactive.py instead."

But later in the same docstring:
"Why ProgramManager has its own file I/O methods:
...
- Web UI uses FileIO abstraction exclusively (no direct ProgramManager file access)"

The first statement says Web UI uses FileIO "in interactive.py" (specific file), while the second says Web UI uses FileIO "exclusively" (broader claim). The reference to "interactive.py" is also potentially confusing as that file is not included in the provided source files.

---

#### documentation_inconsistency

**Description:** Security warning about user_id validation is incomplete

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
The SandboxedFileSystemProvider docstring contains:
"Per-user isolation via user_id keys in class-level storage
  IMPORTANT: Caller must ensure user_id is securely generated/validated
  to prevent cross-user access (e.g., use session IDs, not user-provided values)"

This warning appears only in the class docstring but not in the __init__() method docstring where user_id is actually passed. Developers reading just the __init__() documentation would miss this critical security requirement. The __init__() docstring only says:
"Args:
    user_id: Unique identifier for this user/session"

without any security warnings.

---

#### code_vs_documentation

**Description:** Error code documentation mentions ambiguity but doesn't provide resolution guidance

**Affected files:**
- `src/error_codes.py`

**Details:**
The module docstring states:
"Note: Some two-letter codes are duplicated (e.g., DD, CN, DF) across different numeric error codes. This matches the original MBASIC 5.21 specification where the two-letter codes alone are ambiguous - the numeric code is authoritative."

However, the ERROR_CODES dictionary shows:
10: ("DD", "Duplicate definition"),
61: ("DF", "Disk full"),
68: ("DD", "Device unavailable"),

The documentation correctly notes the ambiguity but doesn't explain how the system handles it when displaying errors. Looking at format_error(), it uses the two-letter code in output, which means error 10 and error 68 would both display as "?DD Error", making them indistinguishable to users. The documentation should clarify whether this is intentional MBASIC-compatible behavior or a limitation.

---

#### documentation_inconsistency

**Description:** Help text formatting inconsistency in LIMITATIONS section

**Affected files:**
- `src/immediate_executor.py`

**Details:**
The LIMITATIONS section has inconsistent bullet point formatting:
- First bullet: '• INPUT statement will fail...'
- Second bullet: '• Multi-statement lines...'
- Third bullet: '• GOTO, GOSUB...'
- Fourth bullet: '• DEF FN works...'
- Fifth bullet: '• Cannot execute...'

All use bullet points consistently, but the descriptions vary in style (some are warnings, some are capabilities). This is minor but could be more uniform.

---

#### documentation_inconsistency

**Description:** Module docstring claims Python 3.9+ syntax but uses standard typing

**Affected files:**
- `src/input_sanitizer.py`

**Details:**
Module docstring states:
'Note: This module uses Python 3.9+ type hint syntax (tuple[str, bool] instead of Tuple[str, bool]).'

The code does use 'tuple[str, bool]' (line 127), which is indeed Python 3.9+ syntax. However, this note seems unnecessary since the code doesn't import from typing module at all, and the syntax is used consistently. The note might confuse readers into thinking there's a compatibility issue when there isn't one (as long as Python 3.9+ is used).

---

#### code_vs_comment

**Description:** Docstring example shows behavior that may not match implementation

**Affected files:**
- `src/immediate_executor.py`

**Details:**
ImmediateExecutor class docstring (lines 46-48) shows example:
'>>> executor.execute("SYNTAX ERROR")
(False, "Syntax error\n")'

However, 'SYNTAX ERROR' is not actually a syntax error in BASIC - it would be parsed as a statement with identifier 'SYNTAX' followed by identifier 'ERROR'. The actual error would likely be 'Undefined variable' or similar, not 'Syntax error'. The example is misleading about what constitutes a syntax error.

---

#### code_vs_comment

**Description:** Comment about readline Ctrl+A binding may be misleading

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~127 says:
'# Bind Ctrl+A to insert the character instead of moving cursor to beginning-of-line
# This overrides default Ctrl+A (beginning-of-line) behavior.
# When user presses Ctrl+A, the terminal sends ASCII 0x01, and 'self-insert'
# tells readline to insert it as-is instead of interpreting it as a command.
# The \x01 character in the input string triggers edit mode (see start() method)'

However, this binding makes Ctrl+A insert a literal 0x01 character which is then checked in the start() method. This is unusual - most implementations would use a custom readline command or key binding callback. The comment is accurate but the approach is unconventional and could confuse maintainers.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for 'program manager' vs 'ProgramManager'

**Affected files:**
- `src/interactive.py`

**Details:**
Line ~82 comment says '# Program manager for line/AST storage' but then imports 'from editing import ProgramManager'. The module name is 'editing' not 'program_manager', which could confuse readers about the actual module structure.

---

#### code_vs_comment_conflict

**Description:** Comment references 'see help text' for GOTO/GOSUB recommendation, but no help text is visible in the provided code to verify this claim.

**Affected files:**
- `src/interactive.py`

**Details:**
Comment line: 'Note: GOTO/GOSUB in immediate mode are not recommended (see help text)'

No help text is provided in the code snippet to verify what the help text actually says about GOTO/GOSUB in immediate mode.

---

#### code_vs_comment_conflict

**Description:** Comment describes PC restoration logic but the actual behavior may be misleading to users who expect GOTO/GOSUB to work normally in immediate mode.

**Affected files:**
- `src/interactive.py`

**Details:**
The code restores the old PC after executing immediate mode statements:

old_pc = runtime.pc
# Execute each statement on line 0
for stmt in line_node.statements:
    interpreter.execute_statement(stmt)
# Restore previous PC to maintain stopped program position
runtime.pc = old_pc

This means GOTO/GOSUB appear to work during execution but their effects are silently undone, which could confuse users who don't understand this internal behavior.

---

#### code_vs_comment

**Description:** Comment about skip_next_breakpoint_check timing is unclear about when it's set vs when it's checked

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment says: "Set to True AFTER halting at a breakpoint (set after returning state)."

But the code in tick_pc() sets it to True when halting:
```python
if at_breakpoint:
    if not self.state.skip_next_breakpoint_check:
        self.runtime.halted = True
        self.state.skip_next_breakpoint_check = True
        return self.state
```

The comment suggests it's set "after returning state" but it's actually set before returning. The parenthetical "(set after returning state)" is misleading.

---

#### code_vs_comment

**Description:** Comment about string variables in FOR loops is misleading

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_for(), the docstring says:
"The loop variable typically has numeric type suffixes (%, !, #). The variable
type determines how values are stored. String variables ($) in FOR loops
would cause a type error when set_variable() attempts to store the numeric
loop value, so they are effectively not supported despite being parsed."

This comment suggests string variables are parsed but will fail at runtime. However, it's unclear if the parser actually allows string variables in FOR statements. The comment says "despite being parsed" but doesn't clarify if this is a parser bug or intentional behavior. This needs clarification about whether the parser should reject string variables in FOR loops or if the runtime error is the intended behavior.

---

#### documentation_inconsistency

**Description:** Comment mentions 'internal implementation version' tracked in src/version.py but this file is not shown in the provided code

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment in interpreter.py says:
"# OLD EXECUTION METHODS REMOVED
# Note: The project has an internal implementation version (tracked in src/version.py)
# which is separate from the MBASIC 5.21 language version being implemented."

This references src/version.py which is not provided in the source files. Cannot verify if this file exists or what version information it contains.

---

#### code_vs_comment

**Description:** InterpreterState docstring mentions checking order but doesn't explain why input_prompt is checked during execution while error_info is set via exceptions

**Affected files:**
- `src/interpreter.py`

**Details:**
The docstring says:
"Note: The suggested checking order below is for UI code that examines state AFTER
execution completes. During execution (in tick_pc()), checks occur in this order:
1. pause_requested, 2. halted, 3. break_requested, 4. breakpoints,
5. statement execution (input_prompt set DURING execution, errors via exceptions)."

This mentions that input_prompt is set DURING execution and errors are via exceptions, but doesn't explain why this architectural difference exists. The comment could be clearer about the fact that input_prompt is set synchronously during statement execution (blocking the tick), while errors are caught and converted to error_info asynchronously.

---

#### code_vs_comment

**Description:** Comment in execute_resume says 'Parser preserves the distinction (None vs 0)' but this is implementation detail that may not be accurate

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment in execute_resume:
# RESUME or RESUME 0 - retry the statement that caused the error
# Note: Parser preserves the distinction (None vs 0) for accurate source
# text regeneration, but the interpreter treats both identically at runtime.

This comment makes a claim about parser behavior without verification in the provided code. The distinction between None and 0 for stmt.line_number may or may not be preserved by the parser.

---

#### code_vs_comment

**Description:** Comment in execute_reset says 'Unlike CLEAR (which silently ignores file close errors), RESET allows errors during file close to propagate' but this distinction may not be meaningful

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment in execute_reset:
Note: Unlike CLEAR (which silently ignores file close errors), RESET allows
errors during file close to propagate to the caller. This is intentional
different behavior between the two statements.

Both execute_clear and execute_reset close files in a loop. CLEAR uses try/except to ignore errors, RESET does not. However, the comment implies this is 'intentional different behavior' but doesn't explain WHY this difference exists or what the MBASIC specification says about error handling in these two statements.

---

#### code_vs_comment

**Description:** Comment in execute_run describes RUN without args behavior but the explanation is confusing about halted state

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment says:
# In non-interactive context, restart from beginning
# Note: RUN without args sets halted=True to stop current execution.
# The caller (e.g., UI tick loop) should detect halted=True and restart
# execution from the beginning if desired. This is different from
# RUN line_number which sets halted=False to continue execution inline.

This comment describes a complex interaction between the interpreter and the caller, but it's unclear why RUN without args sets halted=True instead of just restarting execution directly like RUN line_number does. The asymmetry is confusing.

---

#### code_vs_comment

**Description:** Comment in execute_midassignment says 'start_idx == len(current_value) is considered out of bounds' but this is standard behavior, not a special case

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: "Note: start_idx == len(current_value) is considered out of bounds (can't start replacement past end)"
This is just explaining that you can't start at position beyond the string length, which is obvious from the condition start_idx >= len(current_value). The comment is redundant but not incorrect.

---

#### code_vs_comment

**Description:** Comment about get_variable_for_debugger usage in evaluate_functioncall is verbose and could be clearer

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: "Note: get_variable_for_debugger() and debugger_set=True are used to avoid triggering variable access tracking. This save/restore is internal function call machinery, not user-visible variable access. The tracking system (if enabled) distinguishes between:
- User code variable access (tracked for debugging/variables window)
- Internal implementation details (not tracked)"

The code saves with: saved_vars[param_name] = self.runtime.get_variable_for_debugger(param.name, param.type_suffix)
But restores with: self.runtime.set_variable(base_name, type_suffix, saved_value, debugger_set=True)

The asymmetry (get_variable_for_debugger vs set_variable with debugger_set=True) is explained but could be confusing. The comment is accurate but the implementation pattern is inconsistent.

---

#### documentation_inconsistency

**Description:** execute_list docstring mentions ProgramManager maintaining line_text_map but doesn't specify which ProgramManager methods

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring says: "The line_text_map is maintained by ProgramManager and is kept in sync with the AST during program modifications (add_line, delete_line, RENUM, MERGE)."

This lists specific operations but doesn't reference the actual method names or verify they exist. If ProgramManager methods are named differently (e.g., add_program_line instead of add_line), this would be misleading.

---

#### code_vs_comment

**Description:** execute_get has similar missing validation for record_num as execute_put

**Affected files:**
- `src/interpreter.py`

**Details:**
Based on the pattern, execute_get (not shown in this excerpt but referenced by execute_put's structure) likely has the same issue with record number validation. Both GET and PUT should validate record_num >= 1.

---

#### Documentation inconsistency

**Description:** Module docstring mentions CursesIOHandler but the actual class name in curses_io.py is CursesIOHandler (correct), however the import statement uses 'from .curses_io import CursesIOHandler' which is correct. No actual inconsistency, but worth noting the module is named curses_io.py not cursesio.py.

**Affected files:**
- `src/iohandler/__init__.py`

**Details:**
The __init__.py correctly imports:
from .curses_io import CursesIOHandler

This is consistent with the actual file name 'curses_io.py' and class name 'CursesIOHandler'.

---

#### Code vs Comment conflict

**Description:** The input_char() method's fallback for Windows without msvcrt has a comment describing severe limitations, but the implementation doesn't fully match the warning

**Affected files:**
- `src/iohandler/console.py`

**Details:**
Comment says:
                    # Fallback for Windows without msvcrt: use input() with severe limitations
                    # WARNING: This fallback calls input() which:
                    # - Waits for Enter key (defeats the purpose of single-char input)
                    # - Returns the entire line, not just one character
                    # This is a known limitation when msvcrt is unavailable.
                    # For proper single-character input on Windows, msvcrt is required.
                    line = input()
                    return line[:1] if line else ""

The comment says it 'Returns the entire line, not just one character' but the code actually does 'return line[:1]' which returns only the first character. The comment is misleading about what the code does, though the limitation about waiting for Enter is accurate.

---

#### Documentation inconsistency

**Description:** The input_line() documentation in base.py describes a 'KNOWN LIMITATION' about not preserving leading/trailing spaces, and this is repeated in console.py, curses_io.py, and web_io.py. However, the specific platform limitations differ slightly between implementations but all reference the same base.py documentation.

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/console.py`
- `src/iohandler/curses_io.py`
- `src/iohandler/web_io.py`

**Details:**
base.py states:
        KNOWN LIMITATION (not a bug - platform limitation):
        Current implementations (console, curses, web) CANNOT fully preserve
        leading/trailing spaces due to underlying platform API constraints:
        - console: Python input() strips trailing newline/spaces
        - curses: getstr() strips trailing spaces
        - web: HTML input fields strip spaces

Each implementation file repeats:
        Note: Current implementation does NOT preserve leading/trailing spaces
        as documented in base class. [specific reason]. This is a known limitation - see input_line() documentation in base.py.

This is consistent documentation, not an inconsistency. Marking as low severity for completeness.

---

#### Code vs Documentation inconsistency

**Description:** KeywordCaseManager docstring mentions it is used by parser.py and position_serializer.py, but these files are not provided to verify this claim

**Affected files:**
- `src/keyword_case_manager.py`

**Details:**
Module docstring states:
Note: This class provides advanced case policies (first_wins, preserve, error) via
CaseKeeperTable and is used by parser.py and position_serializer.py.

The files parser.py and position_serializer.py are not included in the provided source code, so this usage cannot be verified.

---

#### Code vs Documentation inconsistency

**Description:** Module docstring mentions that the package avoids conflicts with Python's built-in 'io' module and references its usage in src/filesystem/sandboxed_fs.py and test files, but these files are not provided to verify

**Affected files:**
- `src/iohandler/__init__.py`

**Details:**
__init__.py docstring states:
Module naming: This package is named 'iohandler' rather than 'io' to avoid
conflicts with Python's built-in 'io' module, which is used elsewhere in the
codebase (e.g., in src/filesystem/sandboxed_fs.py and test files) for standard
I/O operations like io.StringIO and io.BytesIO.

The referenced files are not provided to verify this usage.

---

#### Code vs Documentation inconsistency

**Description:** WebIOHandler.input_char() docstring says 'Character input not supported in web UI (always returns empty string)' but the method signature has a 'blocking' parameter that is ignored

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Method signature:
    def input_char(self, blocking=True):
        """Get single character input (for INKEY$, INPUT$).

        Args:
            blocking: If True, wait for keypress. If False, return "" if no key ready.

        Returns:
            Single character string, or "" if not available

        Note: Character input not supported in web UI (always returns empty string).
        """
        return ""

The 'blocking' parameter is documented but completely ignored in the implementation. The docstring should clarify that the parameter is accepted for interface compatibility but has no effect.

---

#### code_vs_comment

**Description:** Comment in read_identifier() says 'Identifiers can contain letters, digits, and end with type suffix $ % ! #' but the code also allows periods in identifiers

**Affected files:**
- `src/lexer.py`

**Details:**
Comment says:
"Identifiers can contain letters, digits, and end with type suffix $ % ! #"

But code implementation allows periods:
while self.current_char() is not None:
    char = self.current_char()
    if char.isalnum() or char == '.':
        ident += self.advance()

The comment should mention that periods are also allowed (for Extended BASIC).

---

#### documentation_inconsistency

**Description:** Module docstring mentions 'MBASIC 5.21 (CP/M era MBASIC-80)' and 'Extended BASIC features' but doesn't clarify if Extended BASIC is the same as MBASIC 5.21 or a separate feature set

**Affected files:**
- `src/lexer.py`

**Details:**
Module docstring:
"Lexer for MBASIC 5.21 (CP/M era MBASIC-80)
Based on BASIC-80 Reference Manual Version 5.21

Note: MBASIC 5.21 includes Extended BASIC features (e.g., periods in identifiers)."

It's unclear if 'Extended BASIC' is a formal name for features in MBASIC 5.21 or if it refers to optional extensions.

---

#### code_vs_comment

**Description:** Comment in read_identifier() says 'Type suffix - only allowed at end of identifier' but the code breaks immediately after consuming the suffix, which is correct behavior but the comment could be clearer

**Affected files:**
- `src/lexer.py`

**Details:**
Comment says:
"# Type suffix - only allowed at end of identifier"

The code correctly breaks after consuming one suffix character:
elif char in ['$', '%', '!', '#']:
    ident += self.advance()
    break

The comment is accurate but could be more explicit that the break enforces this rule.

---

#### code_vs_comment

**Description:** Comment in tokenize() says 'Skip control characters gracefully' but the code raises an error for unexpected characters after skipping control characters

**Affected files:**
- `src/lexer.py`

**Details:**
Comment says:
"# Skip control characters gracefully"

But the code structure is:
if ord(char) < 32 and char not in ['\t', '\n', '\r']:
    self.advance()
    continue
raise LexerError(f"Unexpected character: '{char}' (0x{ord(char):02x})", start_line, start_column)

The comment is accurate - control characters are skipped. The error is raised for non-control unexpected characters. The comment placement might be confusing.

---

#### code_vs_comment

**Description:** Comment about semicolon handling in parse_line() is misleading about statement separation

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines 1485-1489 states:
"Allow trailing semicolon at end of line only (treat as no-op).
Context matters: Semicolons WITHIN PRINT/LPRINT are item separators (parsed there),
but semicolons BETWEEN statements are NOT valid in MBASIC.
MBASIC uses COLON (:) to separate statements, not semicolon (;)."

However, the code then checks:
"if not self.at_end_of_line() and not self.match(TokenType.COLON):
    token = self.current()
    raise ParseError(f"Expected : or newline after ;, got {token.type.name}", token)"

This suggests semicolons ARE allowed as statement separators if followed by colon or newline, contradicting the comment that says they're NOT valid between statements.

---

#### code_vs_comment

**Description:** Comment about comma after file number in PRINT statement is inconsistent with LPRINT

**Affected files:**
- `src/parser.py`

**Details:**
In parse_print() at lines 1575-1581:
"# Optionally consume comma after file number
# Note: MBASIC 5.21 typically uses comma (PRINT #1, "text").
# Our parser makes the comma optional for flexibility.
# If semicolon appears instead of comma, it will be treated as an item
# separator in the expression list below (not as a file number separator).
if self.match(TokenType.COMMA):
    self.advance()"

But in parse_lprint() at lines 1659-1662:
"# Expect comma after file number
if self.match(TokenType.COMMA):
    self.advance()"

The comment in LPRINT says "Expect comma" but the code only optionally consumes it (same as PRINT). Either both should be optional or both should be required for consistency.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for 'line ending' concepts

**Affected files:**
- `src/parser.py`

**Details:**
The code uses multiple overlapping concepts:
- at_end_of_line() checks for NEWLINE or EOF
- at_end_of_statement() checks for NEWLINE, EOF, COLON, or comments
- at_end() checks for EOF or position >= len(tokens)
- at_end_of_tokens() checks if current() is None

The docstrings describe these differently but there's overlap and potential confusion about when to use which method. For example, at_end() and at_end_of_tokens() seem to check similar conditions but are implemented differently.

---

#### code_vs_comment

**Description:** Comment about separators in PRINT statement is confusing about newline addition

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines 1609-1611 states:
"# Add newline if there's no trailing separator
# For N expressions: N-1 separators (between items) = no trailing separator
#                    N separators (between items + at end) = has trailing separator"

Then code at lines 1612-1613:
"if len(separators) < len(expressions):
    separators.append('\n')"

This logic adds a newline when separators < expressions, which means when there are N expressions and N-1 separators. But the comment says this is when there's "no trailing separator", which is correct. However, the comment doesn't explain what happens when separators == expressions (trailing separator exists) - in that case, no newline is added. This should be clarified.

---

#### code_vs_comment

**Description:** Inconsistent comment style for documenting AST node fields

**Affected files:**
- `src/parser.py`

**Details:**
Most parse methods (parse_print, parse_input, parse_goto, etc.) do not include inline comments documenting field names when creating AST nodes.

However, parse_showsettings() includes: "# Field name: 'pattern' (optional filter string)"
And parse_setsetting() includes: "# Field name: 'setting_name' (string identifying setting)"

This creates an inconsistent documentation pattern across the parser methods.

---

#### code_vs_comment

**Description:** Comment about DEF FN function name normalization may be incorrect

**Affected files:**
- `src/parser.py`

**Details:**
In parse_deffn() method:
Comment says: "# 'DEF FNR' without space - identifier is 'fnr' (lexer already normalized to lowercase)"

But earlier code shows: function_name = 'fn' + raw_name  # Use lowercase 'fn' to match function calls

This suggests the parser is constructing the lowercase 'fn' prefix, not that the lexer already normalized it. The comment may be outdated or misleading about where the normalization happens.

---

#### code_vs_comment

**Description:** Inconsistent handling of type suffixes in DEF FN parsing

**Affected files:**
- `src/parser.py`

**Details:**
In parse_deffn() method:
First branch: "# Strip type suffix from the name (e.g., 'test$' -> 'test')"
Then: function_name = 'fn' + raw_name

Second branch: "# 'DEF FNR' without space - identifier is 'fnr'"
Then: raw_name = fn_name_token.value

The first branch explicitly strips type suffixes, but the second branch doesn't show this stripping. The code after the if/elif is cut off, so it's unclear if both branches handle type suffixes consistently.

---

#### code_vs_comment

**Description:** CALL statement docstring claims MBASIC 5.21 primarily uses simple numeric address form, but implementation fully supports extended syntax without any version-specific handling

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states:
"MBASIC 5.21 syntax:
    CALL address           - Call machine code at numeric address

Extended syntax (for compatibility with other BASIC dialects):
    CALL ROUTINE(X,Y)      - Call with arguments

Note: MBASIC 5.21 primarily uses the simple numeric address form, but this parser fully supports both forms for broader compatibility."

However, the implementation treats both forms equally without any version checks or warnings. The comment suggests a distinction that doesn't exist in the code.

---

#### code_vs_comment

**Description:** WIDTH statement docstring describes device parameter but doesn't clarify what expressions are valid

**Affected files:**
- `src/parser.py`

**Details:**
Docstring says:
"Syntax: WIDTH width [, device]

Parses a WIDTH statement that specifies output width for a device.
Both the width and optional device parameters are parsed as expressions.

The parsed statement contains:
- width: Column width expression (typically 40 or 80)
- device: Optional device expression (typically screen or printer)"

The comment mentions 'typically screen or printer' but doesn't specify if these are string literals, identifiers, or numeric codes. The implementation just calls parse_expression() without validation.

---

#### code_vs_comment

**Description:** DEF FN comment about lexer normalization may be outdated or incorrect

**Affected files:**
- `src/parser.py`

**Details:**
In parse_def_fn() method, comment states:
"# raw_name already starts with lowercase 'fn' from lexer normalization"

However, earlier in the same method, there's code that checks:
if not raw_name.lower().startswith('fn'):
    raise ParseError(...)

If the lexer already normalizes to lowercase 'fn', why does the code need to call .lower() to check? This suggests either:
1. The comment is wrong and lexer doesn't normalize
2. The .lower() call is redundant
3. The normalization is inconsistent

---

#### documentation_inconsistency

**Description:** Inconsistent documentation style for statement syntax across different parse methods

**Affected files:**
- `src/parser.py`

**Details:**
Some methods use formal syntax notation:
- parse_open(): "OPEN 'R', #1, 'FILENAME'"
- parse_field(): "FIELD #n, width AS variable$ [, width AS variable$ ...]"

Others use informal description:
- parse_width(): "WIDTH width [, device]" with separate explanation
- parse_call(): Extended prose explanation with examples

The documentation style is inconsistent across similar statement parsing methods.

---

#### code_vs_comment

**Description:** Comment in serialize_let_statement mentions 'AssignmentStatementNode' as historical name but this creates confusion

**Affected files:**
- `src/position_serializer.py`

**Details:**
Comment states: 'In _adjust_statement_positions(), \'AssignmentStatementNode\' was used historically but has been replaced by \'LetStatementNode\' for consistency.'

However, _adjust_statement_positions() code only checks for 'LetStatementNode', not 'AssignmentStatementNode'. The comment references historical usage that may confuse readers looking at current code.

---

#### code_vs_comment

**Description:** Comment about operator positions says 'not tracked' but code uses None which could mean tracked-as-None vs not-tracked

**Affected files:**
- `src/position_serializer.py`

**Details:**
In serialize_let_statement: '# Equals sign (operator position not tracked - using None for column)'

The comment says 'not tracked' but the code explicitly passes None. This is ambiguous - does None mean 'no position info available' or 'position was never stored'? The emit_token function treats None as 'use pretty printing' which suggests it means 'no position info', but the comment phrasing is unclear.

---

#### documentation_inconsistency

**Description:** renumber_with_spacing_preservation docstring has redundant instruction about serialization

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring says: 'Text can then be regenerated from updated AST using serialize_line() (caller should call serialize_line() on each returned LineNode to regenerate text)'

And in Returns section: 'Dict of new_line_number -> LineNode (with updated positions)
Caller should serialize these LineNodes using serialize_line() to get text'

The same instruction is given twice in slightly different wording, which is redundant.

---

#### code_vs_comment

**Description:** Comment in serialize_expression says 'Only add type suffix if explicit' but doesn't explain what makes it explicit

**Affected files:**
- `src/position_serializer.py`

**Details:**
Code: '# Only add type suffix if explicit
if expr.type_suffix and getattr(expr, \'explicit_type_suffix\', False):'

The comment mentions 'explicit' but doesn't define what makes a type suffix explicit vs implicit. The code checks for an 'explicit_type_suffix' attribute but there's no documentation about when this is set or what it means.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology: 'MBASIC 5.21 compatibility' mentioned for max_string_length but no other MBASIC version references or compatibility notes elsewhere

**Affected files:**
- `src/resource_limits.py`

**Details:**
Lines with 'MBASIC 5.21 compatibility':
- Line ~35: max_string_length: int = 255,            # 255 bytes (MBASIC 5.21 compatibility)
- Line ~67: max_string_length: Maximum length for a string variable (bytes)
- Line ~330: max_string_length=255,              # 255 bytes (MBASIC 5.21 compatibility)
- Line ~349: max_string_length=255,              # 255 bytes (MBASIC 5.21 compatibility)
- Line ~368: max_string_length=1024*1024,        # 1MB strings (for testing/development - not MBASIC compatible)

The module documentation doesn't mention MBASIC compatibility as a design goal, and only string length has this specific version reference. This creates ambiguity about whether other limits are also meant to match MBASIC 5.21.

---

#### code_vs_comment

**Description:** Comment says 'DIM A(N) creates N+1 elements (0 to N) in MBASIC 5.21' but this is implementation detail that should be in interpreter.py, not resource_limits.py

**Affected files:**
- `src/resource_limits.py`

**Details:**
Comment at line ~177-178:
'# Note: DIM A(N) creates N+1 elements (0 to N) in MBASIC 5.21
# This calculation matches the array creation logic in src/interpreter.py execute_dim()'

This comment describes interpreter behavior, not resource limit behavior. The resource_limits module should not need to know or document how DIM works - it should only calculate memory based on what the interpreter tells it. This suggests tight coupling or that the calculation logic might belong in interpreter.py instead.

---

#### code_vs_comment

**Description:** Docstring for estimate_size() says it handles 'array' as a value type, but the implementation only handles scalar types

**Affected files:**
- `src/resource_limits.py`

**Details:**
Docstring at line ~149:
'Args:
    value: The actual value (number, string, array)
    var_type: TypeInfo (INTEGER, SINGLE, DOUBLE, STRING) or VarType enum'

But the implementation (lines ~156-169) only handles:
- TypeInfo.INTEGER
- TypeInfo.SINGLE
- TypeInfo.DOUBLE
- TypeInfo.STRING
- default case

There is no special handling for arrays. Arrays are handled separately by check_array_allocation() and allocate_array(). The docstring should not mention 'array' as a value parameter.

---

#### code_vs_comment

**Description:** Comment says 'Import here to avoid circular dependency' but doesn't explain what the circular dependency is or why it exists

**Affected files:**
- `src/resource_limits.py`

**Details:**
Line ~153: '# Import here to avoid circular dependency'
from src.ast_nodes import TypeInfo

This suggests a design issue where resource_limits.py and ast_nodes.py depend on each other, but the comment doesn't explain the nature of the circular dependency. This makes it difficult to understand if the local import is a workaround for a deeper architectural problem or a legitimate design choice.

---

#### code_vs_comment

**Description:** Comment in dimension_array() says DIM is tracked as both read and write, but explanation is misleading

**Affected files:**
- `src/runtime.py`

**Details:**
In dimension_array():
"# Note: DIM is tracked as both read and write for debugger display purposes.
# Technically DIM is an allocation/initialization (write-only), but tracking it
# as both allows debuggers to show 'last accessed' info for unaccessed arrays."

The code sets both last_read and last_write to the same tracking_info, but the comment suggests this is for showing 'last accessed' info. However, if an array is never accessed after DIM, showing DIM as the 'last read' is misleading since DIM doesn't read the array.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for 'canonical case' vs 'original case'

**Affected files:**
- `src/runtime.py`

**Details:**
In _check_case_conflict() method:
- Returns value is documented as 'The canonical case to use for this variable'
- Variable is named 'canonical_case'

But in get_variable() and set_variable():
- Parameter is named 'original_case'
- Stored in _variables dict as 'original_case'

The docstring for get_all_variables() uses 'original_case' to mean 'Canonical case for display'.

This mixing of 'canonical' and 'original' terminology is confusing since they mean different things (canonical = chosen variant, original = as written in source).

---

#### code_vs_comment

**Description:** Comment about error_handler tracking conflicts with actual usage

**Affected files:**
- `src/runtime.py`

**Details:**
In __init__:
"# Error handling registration (ON ERROR GOTO/GOSUB)
self.error_handler = None     # Line number for registered error handler
self.error_handler_is_gosub = False  # True if ON ERROR GOSUB, False if ON ERROR GOTO
# Note: Actual error state (occurred/active) is tracked in state.error_info, not here
# Runtime only stores the registered handler location, not whether an error occurred
# Error PC and details are stored in ErrorInfo (interpreter.py state)
# ERL%, ERS%, and ERR% system variables are set from ErrorInfo"

But then in __init__, ERR% and ERL% are initialized:
"# Initialize system variables ERR% and ERL% to 0
# These are integer type variables set by error handling code
self.set_variable_raw('err%', 0)
self.set_variable_raw('erl%', 0)"

The comment says error state is tracked in ErrorInfo and system variables are set from ErrorInfo, but the code initializes them in Runtime. This suggests Runtime does track some error state (the system variables), contradicting the comment.

---

#### documentation_inconsistency

**Description:** Incomplete docstring for get_all_variables() - example is truncated

**Affected files:**
- `src/runtime.py`

**Details:**
The docstring for get_all_variables() has an example that is cut off:

"Example:
    [
        {'name': 'counter', 'type_suffix': '%', 'is_array': False, 'value': 42,
         'original_case': 'Counter',
         'last_read': {'line': 20, 'position': 5, 'timestamp': 1234.567},
         'last_write': {'line': 10, 'position': 4, 'timestamp': 1234.500}},
        {'name': 'msg', 'type_suffix': '$', 'is_array': False, 'value': 'hello',
         'original_case': 'msg',"

The example ends abruptly without closing the dict or list, making it invalid Python.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for statement offset indexing in different docstrings

**Affected files:**
- `src/runtime.py`

**Details:**
In set_breakpoint() docstring:
"stmt_offset: Optional statement offset (0-based index). If None, breaks on entire line.
                        Ignored if line_or_pc is a PC object.
                        Note: offset 0 = 1st statement, offset 1 = 2nd statement, offset 2 = 3rd statement, etc."

In get_gosub_stack() docstring:
"Note: stmt_offset is a 0-based index where 0 = 1st statement, 1 = 2nd statement, etc."

Both describe the same concept (0-based indexing) but use slightly different phrasing. The first is more explicit with examples, while the second uses 'etc.' The terminology should be consistent across all methods dealing with statement offsets.

---

#### code_vs_comment

**Description:** Comment in parse_name() helper function describes behavior that may not match all cases

**Affected files:**
- `src/runtime.py`

**Details:**
The comment states:
"# No explicit suffix - default to single precision (!)
# Note: In _variables, all names should already have resolved type suffixes
# from _resolve_variable_name() which applies DEF type rules. This fallback
# handles edge cases where a variable was stored without a type suffix."

However, the function is used to parse names from both self._variables and self._arrays. The comment only discusses _variables behavior and doesn't mention whether arrays follow the same rules or if this fallback is actually needed for arrays. This could lead to confusion about whether arrays can be stored without type suffixes.

---

#### documentation_inconsistency

**Description:** get_loop_stack() marked as deprecated but no deprecation timeline or removal plan mentioned

**Affected files:**
- `src/runtime.py`

**Details:**
The method get_loop_stack() has a docstring:
"""Deprecated: Use get_execution_stack() instead."""

However, there's no information about:
- When it was deprecated
- When it might be removed
- Whether it's still safe to use
- What version introduced get_execution_stack() as replacement

This makes it unclear for users whether they need to urgently migrate or if this is a soft deprecation.

---

#### code_vs_comment_conflict

**Description:** Comment about load() behavior contradicts typical expectations but is intentional

**Affected files:**
- `src/settings.py`

**Details:**
In load() method, comment states: 'Implementation note: Settings are stored in flattened format on disk (e.g., {'editor.auto_number': True}) and save() uses _flatten_settings() to write them. However, load() intentionally does NOT call _unflatten_settings() - it keeps settings in flattened format after loading.'

This is unusual because there are both _flatten_settings() and _unflatten_settings() methods defined, but _unflatten_settings() is never called. The comment explains this is intentional because _get_from_dict() handles both formats, but having an unused method is confusing.

---

#### code_inconsistency

**Description:** Unused method _unflatten_settings() defined but never called

**Affected files:**
- `src/settings.py`

**Details:**
The method _unflatten_settings() is defined in SettingsManager class but is never called anywhere in the codebase. The load() method explicitly avoids calling it according to comments. This suggests either:
1. The method should be removed as dead code
2. The method is intended for future use
3. The load() implementation should use it

The comment in load() explains why it's not used, but having unused code is a maintenance burden.

---

#### documentation_inconsistency

**Description:** Comments about settings that don't exist are inconsistent with module purpose

**Affected files:**
- `src/settings_definitions.py`

**Details:**
At the end of SETTING_DEFINITIONS, there are comments:
'# Note: Tab key is used for window switching in curses UI, not indentation
# editor.tab_size setting not included - not relevant for BASIC

# Note: Line numbers are always shown - they're fundamental to BASIC!
# editor.show_line_numbers setting not included - makes no sense for BASIC'

These comments explain why certain settings DON'T exist. While informative, they're unusual in a definitions file - typically you document what IS there, not what ISN'T. This could confuse developers looking for these settings.

---

#### documentation_inconsistency

**Description:** Token dataclass note about field exclusivity is not enforced

**Affected files:**
- `src/tokens.py`

**Details:**
Token dataclass docstring says: 'Note: These fields serve different purposes and should be mutually exclusive (identifiers use original_case, keywords use original_case_keyword): - original_case: For identifiers (user variables) - preserves what user typed - original_case_keyword: For keywords - stores policy-determined display case. The dataclass doesn't enforce this exclusivity, but code should maintain it.'

This is a soft constraint documented but not enforced. If it's important enough to document, it might be worth enforcing with validation or a factory method. The current approach relies on developer discipline.

---

#### code_vs_documentation_inconsistency

**Description:** UIBackend subclasses listed in __init__.py don't match base.py documentation

**Affected files:**
- `src/ui/__init__.py`
- `src/ui/base.py`

**Details:**
src/ui/__init__.py lists: 'UIBackend', 'CLIBackend', 'VisualBackend', 'CursesBackend', 'TkBackend'

src/ui/base.py docstring lists: 'CLIBackend: Terminal-based REPL (interactive command mode), CursesBackend: Full-screen terminal UI with visual editor, TkBackend: Desktop GUI using Tkinter' and mentions 'Future/potential backend types (not yet implemented): WebBackend, HeadlessBackend'

The __init__.py includes 'VisualBackend' which is not mentioned in base.py's documentation. This could be an oversight or VisualBackend might be an alias/base class for visual UIs.

---

#### code_inconsistency

**Description:** CLIBackend replaces interactive's program manager but doesn't document why

**Affected files:**
- `src/ui/cli.py`

**Details:**
In CLIBackend.__init__():
'# Replace interactive's program manager with ours (for external control)
# This allows programmatic loading before start()
self.interactive.program = program_manager'

This replacement happens after InteractiveMode is created with io_handler. The comment says 'for external control' and 'allows programmatic loading before start()', but it's unclear why InteractiveMode can't just be initialized with the correct program_manager in the first place. This suggests either:
1. InteractiveMode constructor doesn't accept program_manager (API limitation)
2. There's a specific initialization order requirement
3. This is a workaround for a design issue

---

#### documentation_inconsistency

**Description:** Global settings path documentation has platform-specific inconsistency

**Affected files:**
- `src/settings.py`

**Details:**
Module docstring says: 'Global: ~/.mbasic/settings.json (Linux/Mac) or %APPDATA%/mbasic/settings.json (Windows)'

But _get_global_settings_path() implementation shows:
'if os.name == 'nt':  # Windows
    appdata = os.getenv('APPDATA', os.path.expanduser('~'))
    base_dir = Path(appdata) / 'mbasic'
else:  # Linux/Mac
    base_dir = Path.home() / '.mbasic''

On Windows, if APPDATA is not set, it falls back to home directory, which would be ~/mbasic (not %APPDATA%/mbasic). The documentation doesn't mention this fallback behavior.

---

#### code_vs_comment_conflict

**Description:** Defensive programming comment suggests invalid policy values are possible

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
In SimpleKeywordCase.__init__():
'if policy not in ["force_lower", "force_upper", "force_capitalize"]:
    # Fallback for invalid/unknown policy values (defensive programming)
    policy = "force_lower"'

The comment says 'defensive programming' but there's no documentation about where invalid values could come from. If this is reading from user settings (settings.py), the settings system should validate values before they reach here. This suggests either:
1. There's a validation gap in the settings system
2. This is overly defensive
3. SimpleKeywordCase can be instantiated from untrusted sources

---

#### code_vs_documentation_inconsistency

**Description:** AutoSaveManager cleanup_old_autosaves default differs from typical autosave retention

**Affected files:**
- `src/ui/auto_save.py`

**Details:**
AutoSaveManager.cleanup_old_autosaves() has default max_age_days=7, but there's no documentation about when this is called or if it's called automatically. The class docstring doesn't mention automatic cleanup, suggesting users must call it manually. This could lead to autosave directory bloat if users don't know to call cleanup.

Typically, autosave systems either:
1. Clean up automatically on startup
2. Clean up after successful save
3. Document that manual cleanup is needed

The current implementation has the method but no guidance on when to use it.

---

#### Code vs Documentation inconsistency

**Description:** The settings widget keypress handler comment states 'Ctrl+P is used for Cancel in the settings widget context (overrides editor's Parse Program binding)' but the curses_keybindings.json shows Ctrl+P is for 'Parse program' in the editor context. The comment correctly notes the override behavior, but there's no documentation of this modal override pattern elsewhere.

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
curses_settings_widget.py comment:
"# Note: Ctrl+P is used for Cancel in the settings widget context (overrides
# editor's Parse Program binding). When the settings widget is open, Ctrl+P
# closes the settings dialog. This is intentional - modal dialogs can override
# editor keybindings while they have focus."

curses_keybindings.json:
"parse": { "keys": ["Ctrl+P"], "primary": "Ctrl+P", "description": "Parse program" }

The keybindings JSON doesn't document context-specific overrides or modal behavior.

---

#### Code vs Comment conflict

**Description:** The _create_setting_widget() method has a comment about stripping 'force_' prefix for cleaner display, but the implementation uses removeprefix() with a fallback for older Python versions. The comment says 'Use removeprefix to only strip from the beginning, not anywhere in the string' but this is explaining Python string method behavior rather than documenting why the code needs this logic.

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
Code and comment:
"# Create display label (strip force_ prefix for cleaner display)
# Use removeprefix to only strip from the beginning, not anywhere in the string
display_label = choice.removeprefix('force_') if hasattr(str, 'removeprefix') else (choice[6:] if choice.startswith('force_') else choice)"

The comment explains the removeprefix behavior but doesn't explain why enum choices have 'force_' prefixes or why they need to be stripped for display. This makes the comment less useful than it could be.

---

#### Documentation inconsistency

**Description:** The cmd_break() docstring states 'Breakpoints are only activated when the RUN command is executed' and 'After setting breakpoints, use RUN to start/restart the program for them to take effect', but doesn't clarify whether breakpoints persist across multiple RUN commands or if they need to be reset.

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
Docstring:
"BREAK command - set/clear/list breakpoints.

Breakpoints are only activated when the RUN command is executed.
After setting breakpoints, use RUN to start/restart the program
for them to take effect."

The implementation stores breakpoints in self.breakpoints (a set) which persists across RUN commands, but this persistence behavior is not documented.

---

#### Code vs Documentation inconsistency

**Description:** The _create_body() docstring says it creates 'widgets for all settings (in order defined above)' but the comment refers to an order that isn't clearly defined. The categories dictionary defines the order, but 'above' is ambiguous.

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
Comment in code:
"# Create widgets for all settings (in order defined above)"

The categories are defined just above this comment:
"categories = {
    'editor': [],
    'keywords': [],
    'variables': [],
}"

But the comment 'in order defined above' is unclear - it could mean the order in the categories dict, or some other ordering. The actual iteration is 'for category in categories.keys()' which in Python 3.7+ preserves insertion order.

---

#### Code vs Comment conflict

**Description:** The _create_body() method creates a footer with text 'Enter=OK  ESC/^P=Cancel  ^A=Apply  ^R=Reset' but the comment says 'Create footer with keyboard shortcuts (instead of button widgets)'. The parenthetical comment suggests buttons were previously used, but this historical context isn't relevant to understanding the current code.

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
Code:
"# Create footer with keyboard shortcuts (instead of button widgets)
footer_text = urwid.Text('Enter=OK  ESC/^P=Cancel  ^A=Apply  ^R=Reset', align='center')"

The comment's '(instead of button widgets)' suggests a previous implementation that no longer exists, making it potentially confusing.

---

#### code_vs_comment

**Description:** Comment at line 147 mentions 'fixed 5-character width' but this contradicts variable-width design

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment states: "The keypress method uses _parse_line_number to find code boundaries
dynamically. The layout is a formatted string with three fields, not three columns."

But then at line 991 and 1024, _parse_line_numbers uses fixed width:
line_num_formatted = f"{num_str:>5}"

This suggests the design intent (variable width) doesn't match implementation (fixed width for pasted content).

---

#### code_vs_comment

**Description:** Comment at line 1088 describes target_column as approximation but doesn't explain variable-width implications

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Docstring states: "target_column: Column to position cursor at (default: 7). This value is an
approximation for typical line numbers. Since line numbers have
variable width, the actual code area start position varies.
The cursor will be positioned at this column or adjusted based
on actual line content."

However, if _parse_line_numbers uses fixed 5-char width (lines 991, 1024), then the code area should consistently start at column 7 (status + 5 chars + space), making this 'approximation' comment misleading.

---

#### code_vs_comment

**Description:** Comment about toolbar being removed conflicts with method still existing

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment in _create_ui() at line ~280 says: 'Toolbar removed from UI layout - use Ctrl+U menu instead for keyboard navigation (_create_toolbar method still exists but is not called)'

But the _create_toolbar() method at line ~240 has its own docstring saying: 'Note: This method is no longer used (toolbar removed from UI in favor of Ctrl+U menu for better keyboard navigation). The method is retained for reference and potential future re-enablement, but can be safely removed if the toolbar is not planned to return.'

Both comments say the same thing, which is consistent, but having the method present with a deprecation note while also having comments elsewhere about it being removed creates mild confusion.

---

#### code_vs_comment

**Description:** Comment says editor.lines is different object from editor_lines but both are dicts with same purpose

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~110 says: 'Note: self.editor_lines is the CursesBackend's storage dict self.editor.lines is the ProgramEditorWidget's storage dict (different object)'

Both are described as storage dicts for line_num -> text, suggesting they serve the same purpose but are separate objects. This creates confusion about why two separate storage mechanisms exist and which is authoritative. The comment doesn't explain the relationship or synchronization between them.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for step debugging commands

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
The code uses multiple terms for the same stepping operations:
- Method names: _debug_step() and _debug_step_line()
- Menu handlers: _menu_step() and _menu_step_line()
- Comments: 'Step Statement' vs 'Step Line'
- Status messages: 'Stepping...' vs 'Stepping line...'
- Key bindings: STEP_KEY and LIST_KEY (where LIST_KEY is described as 'Ctrl+L = Step Line')

The terminology mixing 'step', 'step statement', 'step line' could be more consistent.

---

#### code_vs_comment

**Description:** Comment describes layout positions that may not match actual implementation

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _toggle_variables_window() at line ~880, comment says:
"# Layout: menu (0), editor (1), variables (2), output (3), status (4)"

In _toggle_stack_window() at line ~1030, comment says:
"# Layout: menu (0), editor (1), [variables (2)], [stack (2 or 3)], output, status"

These comments describe the pile layout but don't account for dynamic insertion/removal. The second comment is more accurate with brackets indicating optional elements, but the first comment is misleading as it suggests a fixed layout when variables window is visible.

---

#### code_vs_comment

**Description:** Comment about statement-level precision for GOSUB but default value handling is unclear

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_stack_window() at line ~1010:
"# Show statement-level precision for GOSUB return address
# Note: default of 0 if return_stmt is missing means first statement on line
return_stmt = entry.get('return_stmt', 0)
line = f"{indent}GOSUB from line {entry['from_line']}.{return_stmt}"

The comment says 'default of 0 if return_stmt is missing means first statement on line', but this could be misleading. If return_stmt is genuinely missing (not just 0), using 0 as default might not accurately represent 'first statement' vs 'unknown statement'. The comment should clarify whether 0 is a valid value or just a fallback.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation of main_widget storage strategy

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _show_settings() at line ~773:
"Main widget storage: Uses self.main_widget (stored in __init__) rather than
self.loop.widget (which might be a menu or other overlay)."

And later at line ~790:
"# Main widget storage: Use self.main_widget (stored at UI creation)
# not self.loop.widget (current widget which might be a menu or overlay)"

These comments repeat the same information twice in the same method, suggesting either redundancy or that this pattern was problematic enough to warrant multiple warnings. This repetition indicates a potential design smell or past bugs related to widget storage.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate says 'No state checking - just ask the interpreter' but this is misleading since has_work() likely checks internal state

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment says:
"# Check if interpreter has work to do (after RUN statement)
# No state checking - just ask the interpreter
has_work = self.interpreter.has_work() if self.interpreter else False"

The comment 'No state checking' is misleading because calling has_work() IS checking state - it's just delegating the state check to the interpreter object rather than checking runtime.halted or similar flags directly.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate says command is logged to output pane 'not separate immediate history' but there's no context about what 'separate immediate history' refers to

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment says:
"# Log the command to output pane (not separate immediate history)
self.output_walker.append(make_output_line(f"> {command}"))"

The parenthetical note '(not separate immediate history)' suggests there was or could be a separate immediate history mechanism, but no such mechanism is visible in this code. This comment may be outdated from a previous design.

---

#### documentation_inconsistency

**Description:** Comment about version macro references non-existent src/version.py file

**Affected files:**
- `src/ui/help_macros.py`

**Details:**
In help_macros.py line 73, the comment states:
"# Hardcoded MBASIC version for documentation
# Note: Project has internal implementation version (src/version.py) separate from this"

This references 'src/version.py' but no such file is provided in the source code files. This could be outdated documentation if the file was removed, or the comment may be incorrect about where version information is stored.

---

#### code_vs_comment_conflict

**Description:** Comment about tier labels in search results doesn't match actual tier detection logic

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment in help_widget.py lines 127-129 states:
"# Map tier to labels for search result display
# Note: UI tier (e.g., 'ui/curses', 'ui/tk') is detected via startswith('ui/')
# check below and gets '📘 UI' label. Other unrecognized tiers get '📙 Other'."

However, the actual tier_labels dict (lines 130-133) only defines 'language' and 'mbasic' tiers. The comment mentions UI tier detection happens 'below', but the code at lines 148-151 shows:
"if tier_name.startswith('ui/'):
    tier_label = '📘 UI'
else:
    tier_label = tier_labels.get(tier_name, '📙 Other')"

The comment is accurate but could be clearer that the tier_labels dict is incomplete by design, with UI tiers handled separately via startswith() check.

---

#### code_vs_comment_conflict

**Description:** Comment about search index structure mentions 'pre-built merged search index' but doesn't explain what 'merged' means

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
In help_widget.py line 75:
"def _load_search_indexes(self) -> Dict:
    """Load pre-built merged search index for this UI."""
    merged_index_path = self.help_root / 'ui/curses/merged_index.json'"

The term 'merged' is used but not explained. It's unclear what is being merged - is it merging multiple tier indexes (language, mbasic, ui)? The three-tier help system is mentioned in the class docstring but the connection to 'merged' index isn't explicit.

---

#### code_inconsistency

**Description:** KeybindingLoader._to_tk_binding() has incomplete special character mapping

**Affected files:**
- `src/ui/keybinding_loader.py`

**Details:**
The _to_tk_binding() method (lines 127-189) has a special_map dict that only includes '?' and '/' characters:
"special_map = {
    'ESC': '<Escape>',
    'Enter': '<Return>',
    'Return': '<Return>',
    'Tab': '<Tab>',
    'Space': '<space>',
    '?': '<question>',
    '/': '<slash>',
}"

Many other special characters that might appear in keybindings are not mapped (e.g., ',', '.', ';', '[', ']', etc.). While this may be sufficient for current keybindings, it's inconsistent with the goal of being a general-purpose converter. The function should either document which characters are supported or provide more complete mapping.

---

#### documentation_inconsistency

**Description:** Inconsistent key notation formats in documentation

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
STATUS_BAR_SHORTCUTS uses ^X notation: "MBASIC - ^F help  ^U menu  ^W vars  ^K step line  Tab cycle  ^Q quit"

But KEYBINDINGS_BY_CATEGORY uses Ctrl+ notation in QUIT_DISPLAY, MENU_DISPLAY, etc.

The keymap_widget.py has a _format_key_display() function to convert Ctrl+ to ^, but this conversion happens at display time, creating inconsistency in the source data.

---

#### documentation_inconsistency

**Description:** KEYBINDINGS_BY_CATEGORY includes keys not defined as constants in the module

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
KEYBINDINGS_BY_CATEGORY includes:
- 'Shift+Ctrl+V' for 'Save As'
- 'Shift+Ctrl+O' for 'Recent files'
- 's' and 'd' for Variables Window

But these keys are not defined as module-level constants like other keys (e.g., no SAVE_AS_KEY, RECENT_FILES_KEY, etc.). This creates inconsistency in how keys are documented vs. how they're defined in code.

---

#### code_vs_comment

**Description:** Comment about Ctrl+L being context-sensitive lacks corresponding code

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Comment at end of debugger section: "Note: Ctrl+L is context-sensitive in curses UI:
- When debugging: Step Line (execute all statements on current line)
- When editing: List program (same as LIST_KEY)"

However, there is no CTRL_L_KEY constant defined, and the comment references LIST_KEY which is actually bound to Ctrl+K (from 'step_line' action), not Ctrl+L. This appears to be outdated or incorrect documentation.

---

#### code_vs_comment

**Description:** HELP_KEY comment says 'mnemonic: F for Find help' but F typically means File or Forward

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Comment: "# Help system - use Ctrl+F (mnemonic: F for Find help)"

Ctrl+F is more commonly associated with 'Find' or 'Search' functionality in most applications. Using it for Help with the mnemonic 'Find help' is unusual. This could confuse users expecting Ctrl+F to open a search dialog.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for step operations in documentation

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
In KEYBINDINGS_BY_CATEGORY debugger section:
- (LIST_DISPLAY, 'Step Line - execute all statements on current line')
- (STEP_DISPLAY, 'Step Statement - execute one statement at a time')

But LIST_KEY is loaded from 'step_line' action and STEP_KEY from 'step' action. The documentation uses 'Step Line' and 'Step Statement' but the JSON actions are 'step_line' and 'step'. The terminology should be consistent.

---

#### code_vs_comment

**Description:** Comment about Ctrl+S being unavailable contradicts its potential use

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Comment: "# Save program (Ctrl+S unavailable - terminal flow control)
# Use Ctrl+V instead (V for saVe)"

While Ctrl+S is traditionally used for XOFF in terminal flow control, many modern terminal emulators disable this by default or allow it to be disabled (stty -ixon). The comment presents this as an absolute limitation when it's actually configurable. This could mislead developers or users.

---

#### documentation_inconsistency

**Description:** MAXIMIZE_OUTPUT_KEY comment mentions change from Ctrl+O but doesn't explain why Ctrl+Shift+M was chosen

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Comment: "# Maximize output (for games/full-screen programs)
# Note: Changed from Ctrl+O to Ctrl+Shift+M to avoid conflict with Open (Ctrl+O)"

The comment explains why Ctrl+O was avoided but doesn't explain the mnemonic for Ctrl+Shift+M (presumably M for Maximize). This inconsistency in documentation style (some keys have mnemonics explained, others don't) makes the code less maintainable.

---

#### documentation_inconsistency

**Description:** Module docstring says 'Not thread-safe (no locking mechanism)' but doesn't explain implications

**Affected files:**
- `src/ui/recent_files.py`

**Details:**
Docstring: "Note: Not thread-safe (no locking mechanism)"

This warning is mentioned but there's no explanation of:
1. Whether MBASIC uses multiple threads that might access this
2. What could go wrong if concurrent access occurs
3. Whether this is a known limitation or future work

For a shared module used across multiple UIs, this is important information that should be documented more thoroughly.

---

#### Code vs Documentation inconsistency

**Description:** Return key binding for in-page search navigation not documented

**Affected files:**
- `src/ui/tk_help_browser.py`
- `src/ui/tk_keybindings.json`

**Details:**
In tk_help_browser.py line 126:
self.inpage_search_entry.bind('<Return>', lambda e: self._inpage_find_next())

The tk_keybindings.json documents Return key for 'Execute search (when in search box)' but does not document that Return also advances to the next match when in the in-page search box. This is a different behavior from the main search box.

---

#### Code duplication inconsistency

**Description:** Table formatting code is duplicated across files

**Affected files:**
- `src/ui/tk_help_browser.py`
- `src/ui/markdown_renderer.py`

**Details:**
In tk_help_browser.py line 673-675:
def _format_table_row(self, line: str) -> str:
    """Format a markdown table row for display.

    Note: This implementation is duplicated in src/ui/markdown_renderer.py.
    Consider extracting to a shared utility module if additional changes are needed.
    """

The comment explicitly acknowledges code duplication with markdown_renderer.py. This creates a maintenance burden where changes to table formatting logic must be synchronized across multiple files.

---

#### Code vs Comment conflict

**Description:** Comment about modal behavior is misleading

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
In tk_settings_dialog.py line 48-49:
# Make modal (prevents interaction with parent, but doesn't block code execution - no wait_window())
self.transient(parent)
self.grab_set()

The comment states 'prevents interaction with parent, but doesn't block code execution - no wait_window()'. However, this is describing expected behavior rather than clarifying a potential confusion. The comment could be clearer about what 'modal' means in this context - it prevents UI interaction with parent but doesn't block the calling code's execution flow.

---

#### Code vs Comment conflict

**Description:** Comment about tooltip is inaccurate

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
In tk_settings_dialog.py line 149-151:
else:
    # Show short help as inline label (not a hover tooltip, just a gray label)
    if defn.help_text:

The comment says 'not a hover tooltip, just a gray label' but this seems to be clarifying what the code does rather than describing a discrepancy. However, the phrasing 'not a hover tooltip' suggests there might have been an earlier implementation or design that used tooltips, making this comment potentially outdated.

---

#### Documentation inconsistency

**Description:** Inconsistent documentation of readonly behavior

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
In tk_help_browser.py line 107:
# Make text read-only but allow copy (Ctrl+C) and find (Ctrl+F)

And in line 108-115:
def readonly_key_handler(event):
    # Allow Ctrl+C (copy), Ctrl+A (select all), Ctrl+F (find)
    if event.state & 0x4:  # Control key
        if event.keysym in ('c', 'C', 'a', 'A'):  # Ctrl+C, Ctrl+A
            return  # Allow these
        elif event.keysym in ('f', 'F'):  # Ctrl+F
            self._inpage_search_show()
            return "break"
    return "break"  # Block all other keys

The outer comment mentions 'allow copy (Ctrl+C) and find (Ctrl+F)' but the inner comment adds 'Ctrl+A (select all)' which is not mentioned in the outer comment. This is a minor documentation inconsistency.

---

#### Code vs Comment conflict

**Description:** Comment about dismissing menu references undefined helper

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
In tk_help_browser.py line 638-640:
# Define dismiss_menu helper for ESC/FocusOut bindings (below)
def dismiss_menu():
    try:

The comment says 'for ESC/FocusOut bindings (below)' but the dismiss_menu function is defined before the bindings are created (lines 651-652). The comment's use of '(below)' is spatially inaccurate since the bindings come after in the code, not before. This is a minor directional inconsistency.

---

#### code_vs_comment

**Description:** Comment says immediate_history and immediate_status are set to None but explains they are 'not currently used'

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at lines ~280-283:
"# Set immediate_history and immediate_status to None
# These attributes are not currently used but are set to None for defensive programming
# in case future code tries to access them (will get None instead of AttributeError)"

This suggests these attributes were planned or previously used but removed. The comment is defensive but could indicate incomplete refactoring or planned features.

---

#### code_vs_comment

**Description:** Comment about Ctrl+I binding location conflicts with actual implementation approach

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~467 says:
"# Note: Ctrl+I is bound directly to editor text widget in start() (not root window)
# to prevent tab key interference - see editor_text.text.bind('<Control-i>', ...)"

But the actual binding at line ~213 is:
self.editor_text.text.bind('<Control-i>', self._on_ctrl_i)

The comment is accurate about WHERE it's bound (text widget not root), but the phrasing 'see editor_text.text.bind' suggests looking elsewhere when the code is right there at line 213. Minor clarity issue.

---

#### documentation_inconsistency

**Description:** Docstring usage example references ConsoleIOHandler but TkIOHandler is actually used

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring at lines ~54-63 shows:
"Usage:
    from src.iohandler.console import ConsoleIOHandler
    ...
    io = ConsoleIOHandler()"

But at line ~295, the actual code creates:
tk_io = TkIOHandler(self._add_output, self.root, backend=self)

The usage example should probably show TkIOHandler instead of ConsoleIOHandler for a TkBackend example.

---

#### code_vs_comment

**Description:** Comment about toolbar simplification references features that may still be accessible but location is unclear

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at lines ~494-498:
"# Note: Toolbar has been simplified to show only essential execution controls.
# Additional features are accessible via menus:
# - List Program → Run > List Program
# - New Program (clear) → File > New
# - Clear Output → Run > Clear Output"

This suggests a refactoring where toolbar buttons were removed. The comment is helpful but could indicate that the toolbar was previously more complex. Without seeing the full history, it's unclear if this is just informative or indicates incomplete refactoring.

---

#### code_implementation

**Description:** Methods _edit_array_element and _edit_simple_variable are called but not defined in provided code fragment

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
At line ~809, code calls:
self._edit_array_element(variable_display, type_suffix_display, value_display)

At line ~812, code calls:
self._edit_simple_variable(variable_display, type_suffix, current_value)

But _edit_simple_variable is only partially shown starting at line ~815, and _edit_array_element is not shown at all. The code fragment is incomplete, which makes it impossible to verify full consistency.

---

#### code_vs_comment

**Description:** Comment about formatting contradicts actual behavior in code

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
At line ~1050, comment states:
"# Insert line exactly as stored from program manager - no formatting applied here
# Note: Some formatting may occur elsewhere (e.g., variable display, stack display)
# This preserves compatibility with real MBASIC for program text"

However, throughout the file there are multiple places where formatting IS applied:
- Line ~450: Integer formatting without decimals for array subscripts
- Line ~520: Natural number formatting for FOR loop values
- Line ~850: Value formatting for variables display

The comment suggests no formatting occurs in the editor, but the note acknowledges formatting happens elsewhere. This is slightly contradictory - the comment should be clearer about what "no formatting applied here" means.

---

#### code_vs_comment

**Description:** Comment about type suffix extraction doesn't match all code paths

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
At line ~240, comment states:
"# Parse variable name (remove type suffix for runtime call)"

Then code does:
"if variable_name[-1] in '$%!#':
    base_name = variable_name[:-1]
    suffix = variable_name[-1]
else:
    base_name = variable_name
    suffix = None"

However, at line ~360 in _edit_array_element(), similar logic is used:
"base_name = variable_name[:-1] if variable_name[-1] in '$%!#' else variable_name
suffix = variable_name[-1] if variable_name[-1] in '$%!#' else None"

The logic is the same but written differently (ternary vs if/else). This inconsistency in style within the same file could indicate copy-paste without refactoring. Consider extracting to a helper method.

---

#### code_vs_comment

**Description:** Comment describes two cases for multi-line paste logic but the actual branching logic differs from description

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1230 says:
# Multi-line paste or single-line paste into blank line - use auto-numbering logic
# This handles two cases:
# 1. Multi-line paste (sanitized_text contains \n) - auto-number if needed
# 2. Single-line paste into blank line (current_line_text is empty) - auto-number if needed

However, the code flow doesn't explicitly check for case 2 (single-line paste into blank line). The code falls through to the multi-line logic after the inline paste check, but doesn't verify current_line_text is empty as the comment suggests. The comment implies a specific check for blank lines that isn't present.

---

#### code_vs_comment

**Description:** Comment says 'Lines are displayed exactly as stored' but this may not account for syntax highlighting or other display transformations

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1620 in _highlight_current_statement says:
# Lines are displayed exactly as stored, so char_start/char_end
# are relative to the line as displayed

This assumes no transformation between storage and display, but the editor_text widget may apply syntax highlighting, tags, or other formatting that could affect character positions. The comment makes an absolute claim that may not hold if display transformations are added.

---

#### code_vs_comment

**Description:** Docstring says _setup_immediate_context_menu is 'currently unused' but doesn't explain if it's ever called

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring states: "NOTE: This method is currently unused - immediate_history is always None in the Tk UI (see __init__). This is dead code retained for potential future use if immediate mode gets its own output widget."

However, the code doesn't show whether this method is called during initialization or not. If it's truly dead code, it should either be removed or the comment should clarify that it's never invoked.

---

#### documentation_inconsistency

**Description:** TkIOHandler docstring describes input strategy but implementation details don't fully match description

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Class docstring states: "Input strategy:
- INPUT statement: Prefers inline input field (when backend available), falls back to modal dialog
- LINE INPUT statement: Always uses modal dialog for consistent UX"

However, input_line() docstring says: "Unlike input() which prefers inline input field, this ALWAYS uses a modal dialog regardless of backend availability."

The second docstring adds 'regardless of backend availability' which is implied but not explicitly stated in the class docstring. While not contradictory, the class docstring could be clearer about the 'always' nature of LINE INPUT's modal dialog usage.

---

#### code_vs_comment

**Description:** Docstring for _on_status_click() says it shows 'breakpoint confirmation' but implementation shows 'breakpoint info' message

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Docstring: "Handle click on status column (show error details for ?, breakpoint confirmation for ●)."

Implementation shows: messagebox.showinfo(f"Breakpoint on Line {line_num}", f"Line {line_num} has a breakpoint set.\n\nUse the debugger menu or commands to manage breakpoints.")

This is informational, not a confirmation dialog. The term 'confirmation' typically implies a yes/no dialog, but showinfo() only displays information.

---

#### documentation_inconsistency

**Description:** Module docstring says 'line-numbered text editors' (plural) but only one widget class is defined

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Module docstring: "This module provides specialized widgets used by the Tk backend, including line-numbered text editors with status indicators."

Only one class is defined: LineNumberedText

The plural 'editors' suggests multiple editor classes, but only one is present. Should be 'editor' (singular) or the docstring should clarify it provides components for editors.

---

#### code_vs_comment

**Description:** Comment in _on_status_click() says 'Calculate which line was clicked based on Y coordinate' but then uses line height division which may not account for variable line heights or wrapped lines

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment: "# Calculate which line was clicked based on Y coordinate"

Code: clicked_line_offset = int(event.y / self.line_height)

This calculation assumes uniform line height, but the Text widget can have variable line heights with wrapped text or different font sizes. The code uses self.line_height from font metrics, but doesn't account for actual displayed line heights which could differ. The dlineinfo() method used in _redraw() would be more accurate for click detection.

---

#### code_vs_comment

**Description:** Docstring for serialize_variable() shows example output 'x$' (lowercase) but doesn't explain case preservation logic

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring example:
>>> serialize_variable(var_node)
'x$'

But the code uses: text = getattr(var, 'original_case', var.name) or var.name

The example shows lowercase output, but the actual behavior depends on whether original_case is preserved. The docstring should clarify this behavior.

---

#### documentation_inconsistency

**Description:** Module docstring states 'No UI-framework dependencies' are allowed, but doesn't clarify whether runtime/parser modules count as 'core interpreter modules' or external dependencies

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring states:
"No UI-framework dependencies (Tk, curses, web)
are allowed. Standard library modules (os, glob, re) and core interpreter
modules (runtime, parser, AST nodes) are permitted."

The distinction between 'standard library' and 'core interpreter modules' is unclear. Are runtime/parser considered part of the project's core or external dependencies?

---

#### code_vs_comment

**Description:** serialize_expression() docstring mentions ERR and ERL special handling but doesn't explain why they're special or reference any specification

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring note:
"ERR and ERL are special system variables that are serialized without
parentheses (e.g., 'ERR' not 'ERR()') when they appear as FunctionCallNode
with no arguments, matching MBASIC 5.21 syntax."

This explains the behavior but doesn't explain why ERR/ERL are parsed as FunctionCallNode if they're variables. This suggests a parser inconsistency that should be documented or fixed.

---

#### documentation_inconsistency

**Description:** renum_program() docstring states callback is 'responsible for identifying and updating statements with line number references' but doesn't specify which statement types have line references

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring states:
"renum_callback: Function that takes (stmt, line_map) to update statement references.
                Called for ALL statements; callback is responsible for identifying and
                updating statements with line number references (GOTO, GOSUB, ON GOTO,
                ON GOSUB, IF THEN/ELSE line numbers)"

The list in parentheses appears to be examples, but it's unclear if this is exhaustive. The function should either document all statement types with line references or provide a way to query which types need updating.

---

#### code_vs_comment

**Description:** serialize_statement() for RemarkStatementNode has comment about REMARK conversion that contradicts the code logic

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment states:
"# Preserve comments using original syntax (REM or ')
# Note: REMARK is converted to REM during parsing, not here"

But the code checks stmt.comment_type for 'APOSTROPHE' vs 'REM, REMARK, or default'. If REMARK is converted during parsing, why does the else clause mention it? This suggests either the comment is outdated or the code handles a case that shouldn't exist.

---

#### documentation_inconsistency

**Description:** cycle_sort_mode() docstring mentions 'Tk UI implementation' but this is supposed to be UI-agnostic common logic

**Affected files:**
- `src/ui/variable_sorting.py`

**Details:**
Docstring states:
"The cycle order is: accessed -> written -> read -> name -> (back to accessed)
This matches the Tk UI implementation."

Since this module provides common logic for all UIs, the reference to 'Tk UI implementation' suggests this was copied from Tk-specific code. The docstring should describe this as the standard cycle order, not reference a specific UI.

---

#### code_vs_comment

**Description:** get_sort_key_function() has a comment about unknown modes falling back to name sorting, but doesn't log or warn about this fallback

**Affected files:**
- `src/ui/variable_sorting.py`

**Details:**
Code comment:
"else:
    # Default to name sorting (unknown modes fall back to this)
    return lambda v: v['name'].lower()"

Silent fallback for unknown sort modes could hide bugs. The function should either validate the sort_mode parameter or log a warning when falling back to default behavior.

---


## Summary

- Total issues found: 477
- Code/Comment conflicts: 226
- Other inconsistencies: 251
