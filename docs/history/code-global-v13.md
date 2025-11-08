# Global Code Changes Requiring Review (v13)

Generated from code-v13.md
Contains: Changes to interpreter/runtime/interactive and other global code
These changes affect ALL UIs and require careful review before implementation

Total global issues: 23

### 🔴 High Severity

#### Code vs Documentation inconsistency

**Description:** Security warning about user_id validation is in docstring but not enforced in code

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
src/filesystem/sandboxed_fs.py SandboxedFileSystemProvider.__init__() docstring states:
"Args:
    user_id: Unique identifier for this user/session
            SECURITY: Must be securely generated/validated (e.g., session IDs)
            to prevent cross-user access. Do NOT use user-provided values."

And in the class docstring:
"Security:
- No access to real filesystem
- No path traversal (../ etc.)
- Resource limits enforced
- Per-user isolation via user_id keys in class-level storage
  IMPORTANT: Caller must ensure user_id is securely generated/validated
  to prevent cross-user access (e.g., use session IDs, not user-provided values)"

However, the __init__() method accepts user_id without any validation:
def __init__(self, user_id: str, max_files: int = 50, max_file_size: int = 1024 * 1024):
    self.user_id = user_id
    ...

The code relies entirely on the caller to provide a secure user_id, but there's no enforcement or validation. This is a security-critical documentation vs implementation gap - the documentation warns about security but the code doesn't enforce it.

---
---
#### code_vs_comment

**Description:** Extensive comment block about numbered line editing describes validation checks that don't match the actual code flow

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Comment at lines ~95-103 states:
'This feature requires the following UI integration:
- interpreter.interactive_mode must reference the UI object (checked with hasattr)
- UI.program must have add_line() and delete_line() methods (validated, errors if missing)
- UI._refresh_editor() method to update the display (optional, checked with hasattr)
- UI._highlight_current_statement() for restoring execution highlighting (optional, checked with hasattr)
If interactive_mode doesn't exist or is falsy, returns error: "Cannot edit program lines in this mode".
If interactive_mode exists but required program methods are missing, returns error message.'

However, the actual code (lines ~109-145) performs validation checks in a different order and with different error messages:
1. First checks 'if not hasattr(ui, "program") or not ui.program' -> returns 'UI program manager not available'
2. Then checks for add_line/delete_line methods conditionally based on whether line_content exists
3. The validation happens AFTER checking interactive_mode, not as part of the initial check

The comment describes a validation flow that doesn't match the implementation.

---
---
#### code_vs_comment

**Description:** Comment in _renum_erl_comparison says implementation renumbers 'ANY binary operator' but then describes this as broader than manual specifies, creating confusion about whether this is correct behavior

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 636-651:
MBASIC manual specifies: if ERL appears on left side of comparison operator
(=, <>, <, >, <=, >=), the right-hand number is a line number reference.

IMPORTANT: Current implementation renumbers for ANY binary operator with ERL on left,
including arithmetic (ERL + 100, ERL * 2). This is broader than the manual specifies.

Rationale: Without semantic analysis, we cannot distinguish ERL=100 (comparison)
from ERL+100 (arithmetic) at parse time. We conservatively renumber all cases
to avoid missing valid line number references in comparisons.

Known limitation: Arithmetic like "IF ERL+100 THEN..." will incorrectly renumber
the 100 if it happens to be an old line number. This is rare in practice.

This is a documented bug/limitation being treated as acceptable behavior. The comment admits the implementation is incorrect ('incorrectly renumber') but justifies it as 'rare in practice'. This should be flagged as a known bug, not described as intentional behavior.

---
---
### 🟡 Medium Severity

#### code_vs_documentation

**Description:** Docstring claims INPUT 'will fail at runtime' but implementation shows it fails when input() is called, not during parsing/execution setup

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Class docstring and help text state: 'INPUT statement will fail at runtime in immediate mode (use direct assignment instead)'

OutputCapturingIOHandler.input() method comment states: 'Note: INPUT statements are parsed and executed normally, but fail at runtime when the interpreter calls this input() method.'

The second description is more accurate - INPUT statements are fully parsed and execution begins, but fail when the interpreter attempts to call the IOHandler's input() method. The first description could be misinterpreted as INPUT being blocked earlier in the process.

---
---
#### code_vs_comment

**Description:** Comment claims EDIT command 'cannot be parsed as BASIC statements' but code attempts to parse it through execute_immediate() before checking for EDIT

**Affected files:**
- `src/interactive.py`

**Details:**
Line 177-180 comment:
# Special commands that require direct handling
# AUTO and EDIT cannot be parsed as BASIC statements (no corresponding AST nodes),
# so they're handled directly here before attempting to parse.

But line 183-184 shows EDIT is checked AFTER the comment claims it should be handled:
elif command == "EDIT":
    self.cmd_edit(args)

The code structure matches the comment (EDIT is handled before execute_immediate), so this is not a bug, but the comment's explanation is misleading since it implies EDIT would fail if parsed, when actually it's just more efficient to handle it directly.

---
---
#### internal_inconsistency

**Description:** Inconsistent error handling between CLEAR and RESET for file closing

**Affected files:**
- `src/interpreter.py`

**Details:**
execute_clear (line ~1275) uses try/except to silently ignore file close errors:
try:
    file_obj = self.runtime.files[file_num]
    if hasattr(file_obj, 'close'):
        file_obj.close()
except:
    pass

execute_reset (line ~1735) allows errors to propagate:
for file_num in list(self.runtime.files.keys()):
    self.runtime.files[file_num]['handle'].close()
    del self.runtime.files[file_num]

The comment at line ~1730 claims this is intentional: "Unlike CLEAR (which silently ignores file close errors), RESET allows errors during file close to propagate to the caller."

However, this design decision is not documented anywhere else and seems arbitrary. Why should CLEAR ignore errors but RESET propagate them?

---
---
#### documentation_inconsistency

**Description:** execute_step() docstring claims it's a placeholder and not functional, but also describes working step infrastructure in tick_pc() that UIs should use directly

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring states: 'IMPORTANT: This method is a placeholder and does NOT actually perform stepping. The tick_pc() method DOES have working step infrastructure (modes 'step_statement' and 'step_line'), which is used by UI debuggers.'

This creates confusion about whether stepping functionality exists and where it should be used. The relationship between this STEP command and the tick_pc() stepping modes is unclear.

---
---
#### Code vs Documentation inconsistency

**Description:** web_io.py implements get_screen_size() method which is not part of the IOHandler base interface

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/web_io.py`

**Details:**
base.py IOHandler defines the interface with methods: output, input, input_line, input_char, clear_screen, error, debug, locate, get_cursor_position

web_io.py adds: get_screen_size() with comment "Note: This is a web_io-specific method, not part of the IOHandler base interface."

This breaks the abstraction - code using IOHandler interface cannot portably call get_screen_size().

---
---
#### code_vs_comment

**Description:** Comment about DIM tracking as both read and write is inconsistent with typical semantics

**Affected files:**
- `src/runtime.py`

**Details:**
Line 619-627 in dimension_array(): "# Note: DIM is tracked as both read and write to provide consistent debugger display.
# While DIM is technically allocation/initialization (write-only operation), setting
# last_read to the DIM location ensures that debuggers/inspectors can show 'Last accessed'
# information even for arrays that have never been explicitly read. Without this, an
# unaccessed array would show no last_read info, which could be confusing. The DIM location
# provides useful context about where the array was created."

This is a design decision that treats DIM as a read operation for debugger convenience, but it's semantically incorrect. DIM is purely a write/allocation operation. The comment acknowledges this inconsistency but justifies it for debugger display purposes. This could confuse users who expect 'last_read' to mean actual read access.

---
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
---
#### code_vs_comment

**Description:** Comment claims RUN clears output, but code explicitly does NOT clear output

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~1845 comment: 'Note: This implementation does NOT clear output (see comment at line ~1845 below).' but the actual comment at that location says: 'Don't clear output - continuous scrolling like ASR33 teletype
# Design choice: Unlike some modern BASIC interpreters that clear output on RUN,
# we preserve historical ASR33 behavior (continuous scrolling, no auto-clear).
# Note: Step commands (Ctrl+T/Ctrl+K) DO clear output for clarity when debugging'

However, the code for step commands (_menu_step_line and _menu_step_stmt) also has comment 'Note: Output is NOT cleared - continuous scrolling like ASR33 teletype' which contradicts the claim that step commands DO clear output.

---
---
#### documentation_inconsistency

**Description:** Version string 'MBASIC 5.21' in UI title doesn't match VERSION constant usage pattern

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
At line ~453:
ui.run(
    title='MBASIC 5.21 - Web IDE',
    ...
)

But earlier at line ~437:
sys.stderr.write(f"MBASIC Web UI Starting - Version {VERSION}\n")

The hardcoded '5.21' in the title should use the VERSION constant for consistency: title=f'MBASIC {VERSION} - Web IDE'

---
---
#### code_internal_inconsistency

**Description:** Inconsistent error handling between periodic save and disconnect save - both catch exceptions but one is described as 'won't crash' while other is just 'save on disconnect'

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
save_state_periodic() at ~459:
try:
    app.storage.client['session_state'] = backend.serialize_state()
except Exception as e:
    sys.stderr.write(f"Warning: Failed to save session state: {e}\n")

save_on_disconnect() at ~473:
try:
    app.storage.client['session_state'] = backend.serialize_state()
except Exception as e:
    sys.stderr.write(f"Warning: Failed to save final session state: {e}\n")

Both have identical error handling but different commentary about their reliability. The 'won't crash the UI' comment for periodic saves suggests higher confidence than warranted.

---
---
### 🟢 Low Severity

#### documentation_inconsistency

**Description:** ChainStatementNode delete_range type annotation inconsistency

**Affected files:**
- `src/ast_nodes.py`

**Details:**
ChainStatementNode definition line 545:
'delete_range: Optional[Tuple[int, int]] = None  # (start_line_number, end_line_number) for DELETE option - tuple of int line numbers'

The comment redundantly specifies 'tuple of int line numbers' when the type annotation 'Tuple[int, int]' already makes this clear. More importantly, the comment format '(start_line_number, end_line_number)' uses underscores while other similar comments use spaces (e.g., 'line_number' vs 'line number'), creating minor inconsistency in documentation style.

---
---
#### documentation_inconsistency

**Description:** Help text mentions 'Ctrl+H (UI help)' but this is UI-specific and may not be available in all contexts

**Affected files:**
- `src/immediate_executor.py`

**Details:**
In _show_help() method, the help text ends with:
'Press Ctrl+H (UI help) for keyboard shortcuts and UI features.'

This assumes a specific UI implementation with Ctrl+H bound to help, but ImmediateExecutor is designed to be UI-agnostic. The help text should either be generic or note that this is specific to certain UIs.

---
---
#### code_vs_comment

**Description:** Docstring for cmd_edit says 'Count prefixes ([n]D, [n]C) and search commands ([n]S, [n]K) are not yet implemented' but then describes digit behavior as 'INTENTIONAL BEHAVIOR' that 'preserves MBASIC compatibility'

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 682-688:
Note: Count prefixes ([n]D, [n]C) and search commands ([n]S, [n]K) are not yet implemented.
INTENTIONAL BEHAVIOR: When digits are entered, they are silently ignored (no output, no
cursor movement, no error). This preserves MBASIC compatibility where digits are reserved
for count prefixes in the full EDIT implementation. Future enhancement will parse and
use digit prefixes to repeat commands.

The 'not yet implemented' suggests it's a missing feature, but 'INTENTIONAL BEHAVIOR' and 'preserves MBASIC compatibility' suggests it's working as designed. These statements are contradictory - either it's unimplemented (a gap) or it's intentionally compatible (working correctly).

---
---
#### code_vs_comment_conflict

**Description:** Comment in execute_list() warns about ProgramManager sync issues, but doesn't specify what operations might fail to maintain sync

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: 'If ProgramManager fails to maintain this sync, LIST output may show stale or incorrect line text.'

The comment mentions 'add_line, delete_line, RENUM, MERGE' as operations that should maintain sync, but doesn't clarify if there are known cases where sync fails or if this is just a general warning.

---
---
#### code_vs_comment_conflict

**Description:** Comment in evaluate_functioncall() explains debugger_set=True usage but the actual code uses get_variable_for_debugger() for reading, not set_variable with debugger_set

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment states: 'Note: get_variable_for_debugger() and debugger_set=True are used to avoid triggering variable access tracking.'

However, the save code uses: 'saved_vars[param_name] = self.runtime.get_variable_for_debugger(param.name, param.type_suffix)'

And the restore code uses: 'self.runtime.set_variable(base_name, type_suffix, saved_value, debugger_set=True)'

The comment groups these together but they're different mechanisms - one for reading, one for writing.

---
---
#### Code vs Documentation inconsistency

**Description:** input_line() limitation about not preserving spaces is documented as platform limitation, but implementations don't attempt any workarounds

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/console.py`
- `src/iohandler/curses_io.py`
- `src/iohandler/web_io.py`

**Details:**
base.py says: "KNOWN LIMITATION (not a bug - platform limitation):
Current implementations (console, curses, web) CANNOT fully preserve
leading/trailing spaces due to underlying platform API constraints"

But the implementations simply delegate to input() or getstr() without any attempt to work around the limitation (e.g., by prompting user to type a delimiter, or using raw input modes). The limitation is accepted without exploration of alternatives.

---
---
#### code_vs_comment

**Description:** Comment about line=-1 usage is inconsistent between different locations

**Affected files:**
- `src/runtime.py`

**Details:**
Line 47-52 in __init__ comment: "Note: line -1 in last_write indicates non-program execution sources:
1. System/internal variables (ERR%, ERL%) via set_variable_raw() with FakeToken(line=-1)
2. Debugger/interactive prompt via set_variable() with debugger_set=True and token.line=-1
Both use line=-1, making them indistinguishable from each other in last_write alone.
However, line=-1 distinguishes these special sources from normal program execution (line >= 0)."

Line 425-432 in set_variable_raw() comment: "The line=-1 marker in last_write indicates system/internal variables.
However, debugger sets also use line=-1 (via debugger_set=True),
making them indistinguishable from system variables in last_write alone.
Both are distinguished from normal program execution (line >= 0)."

These comments are consistent with each other, but the distinction between system/internal variables and debugger sets is mentioned as important yet they're stored identically. This may indicate a design issue where these should be distinguishable.

---
---
#### code_vs_comment

**Description:** Comment about token requirements is verbose and could be clearer

**Affected files:**
- `src/runtime.py`

**Details:**
Line 289-299 in get_variable(): "Token object is required but its attributes are optional:
- token.line: Preferred for tracking, falls back to self.pc.line_num if missing
- token.position: Preferred for tracking, falls back to None if missing

This allows robust handling of tokens from various sources (lexer, parser,
fake tokens) while enforcing that some token object must be provided.
For debugging without token requirements, use get_variable_for_debugger()."

This comment is accurate but the fallback behavior (using self.pc.line_num when token.line is missing) is not consistently documented elsewhere. The set_variable() method has similar token handling but less detailed comments.

---
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
---
