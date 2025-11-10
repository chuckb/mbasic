# Enhanced Consistency Report (Code + Documentation)

Generated: 2025-11-10 12:56:34
Analyzed: Source code (.py, .json) and Documentation (.md)

## 🔧 Code vs Comment Conflicts


## 📋 General Inconsistencies

### 🔴 High Severity

#### documentation_inconsistency

**Description:** Contradictory documentation about FileIO usage for LOAD/SAVE commands

**Affected files:**
- `src/codegen_backend.py`
- `src/editing/manager.py`

**Details:**
codegen_backend.py docstring states:
"Platform requirement: Assumes z88dk is installed via snap on Linux at /snap/bin/z88dk.zcc.
This path is hardcoded and will not work on other platforms or installation methods."

manager.py docstring states:
"FILE I/O ARCHITECTURE:
This manager provides direct Python file I/O methods (load_from_file, save_to_file)
for loading/saving .BAS program files. Used by both UI menus and BASIC commands.

Current implementation:
- LOAD/SAVE/MERGE commands (interactive.py) call ProgramManager methods directly
- UI menu operations (File > Open/Save) also call ProgramManager methods directly
- Local UIs (CLI, Curses, Tk) use direct filesystem access via ProgramManager
- Web UI currently does not support LOAD/SAVE commands (would need async refactor)

Related filesystem abstractions:
1. FileIO (src/file_io.py) - Planned abstraction for LOAD/SAVE/MERGE/KILL commands
   - NOT currently used by LOAD/SAVE commands (they call ProgramManager directly)"

The codegen_backend.py hardcodes a snap path which contradicts the manager.py claim that FileIO abstraction exists for cross-platform support. Both indicate platform-specific limitations but describe different architectural approaches.

---

#### Code vs Documentation inconsistency

**Description:** SandboxedFileIO.list_files() implementation doesn't match its documented purpose

**Affected files:**
- `src/file_io.py`

**Details:**
Documentation in module docstring states FileIO is for "PROGRAM file operations" and "Load .BAS programs into memory, save from memory to storage".

SandboxedFileIO.list_files() implementation:
```
if hasattr(self.backend, 'sandboxed_fs'):
    pattern = filespec.strip().strip('"').strip("'") if filespec else None
    files = self.backend.sandboxed_fs.list_files(pattern)
```

This queries backend.sandboxed_fs which is a SandboxedFileSystemProvider (runtime file I/O system). But FileIO is supposed to list .BAS program files, not runtime data files created by OPEN/PRINT# statements. The implementation lists the wrong filesystem.

---

#### code_vs_documentation_inconsistency

**Description:** Numbered line editing validation contradicts documented requirements

**Affected files:**
- `src/immediate_executor.py`

**Details:**
The execute() method docstring states:
"Numbered Line Editing:
    When a numbered line is entered (e.g., '100 PRINT X'), this method
    adds or updates that line in the program via UI integration:
    - Requires interpreter.interactive_mode to reference the UI object
    - UI must have add_line() and delete_line() methods
    - Empty line content (e.g., '100') deletes that line
    - Returns error tuple if UI integration is missing or incomplete"

However, the code validates ui.program.add_line and ui.program.delete_line (methods on ui.program), not ui.add_line and ui.delete_line (methods on ui). The validation code checks:
"if not hasattr(ui.program, 'add_line'):"
"if not hasattr(ui.program, 'delete_line'):"

The docstring should say "UI.program must have add_line() and delete_line() methods" not "UI must have add_line() and delete_line() methods".

---

#### code_vs_comment

**Description:** Comment claims clear_execution_state does NOT clear PC, but CONT documentation suggests PC validation happens

**Affected files:**
- `src/interactive.py`

**Details:**
In clear_execution_state method (~180), comment says:
'Note: We do NOT clear/reset the PC here. The PC is preserved so that CONT can detect if the program was edited using pc.is_valid(). If the PC position still exists after editing, CONT will allow resuming; if not, it shows "?Can't continue" matching MBASIC 5.21 behavior.'

However, in cmd_cont method (~380), the docstring says:
'BUG FIX: Now properly detects if the program has been edited (lines added, deleted, or renumbered) by using pc.is_valid() to check if the PC position still exists in the program.'

This creates confusion: if clear_execution_state is called when lines are edited (as stated in its docstring), and it preserves the PC, then how does CONT detect edits? The answer is pc.is_valid() checks the statement_table, but the relationship between clear_execution_state (which clears stacks but not PC) and CONT's validation is not clearly explained. The comment in clear_execution_state should explicitly mention that PC preservation enables CONT's pc.is_valid() check.

---

#### code_vs_comment_conflict

**Description:** Extensive comment about GOTO/GOSUB behavior in immediate mode describes complex transient jump behavior that may not match actual implementation

**Affected files:**
- `src/interactive.py`

**Details:**
Around line 345, there's a long comment:
# Save old PC to preserve stopped program position for CONT.
# Note: GOTO/GOSUB in immediate mode work but PC restoration affects CONT behavior:
# They execute and jump during execute_statement(), but we restore the
# original PC afterward to preserve CONT functionality. This means:
# - The jump happens and target code runs during execute_statement()
# - The final PC change is then reverted, preserving the stopped position
# - CONT will resume at the original stopped location, not the GOTO target
# This implementation allows GOTO/GOSUB to function while preserving CONT state.
# However, the transient jump behavior may be unexpected, hence marked 'not recommended'
# in help text.

This comment describes very specific behavior about 'transient jumps' and PC restoration, but:
1. The code only saves/restores old_pc, it doesn't show the complex jump-and-revert behavior described
2. The comment references 'not recommended in help text' but cmd_help() doesn't mention GOTO/GOSUB restrictions
3. The described behavior (jump happens, then PC reverted) seems contradictory - if the jump executes and runs target code, how does reverting PC make sense?
4. This needs clarification on what actually happens vs what the comment claims

---

#### code_vs_comment

**Description:** CLEAR statement comment says 'Only OS-level file errors are silently ignored' but code catches both OSError and IOError

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1437: "Note: Only OS-level file errors (OSError, IOError) are silently ignored to match MBASIC behavior. This differs from RESET which allows errors to propagate. We intentionally do NOT catch all exceptions (e.g., AttributeError) to avoid hiding programming errors."
Code at line ~1444: except (OSError, IOError):
In Python 3, IOError is an alias for OSError, so catching both is redundant. The comment should either: (1) acknowledge this is for Python 2 compatibility, (2) remove IOError from the comment, or (3) explain why both are listed.

---

#### code_vs_comment

**Description:** RENUM statement has TODO comment saying 'not yet implemented' but execute_renum method exists and delegates to interactive_mode

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1963: "TODO: Implement RENUM to modify AST directly. This is complex because it needs to: 1. Renumber lines in line_asts 2. Update statement_table PC keys 3. Update GOTO/GOSUB/ON GOTO target line numbers in AST nodes 4. Update RESTORE line number references"
Code at line ~1972: if hasattr(self, 'interactive_mode') and self.interactive_mode: self.interactive_mode.cmd_renum(args)
The TODO suggests RENUM is not implemented, but the code shows it IS implemented via delegation to interactive_mode. The TODO should either: (1) be removed if delegation is the intended implementation, or (2) clarified to say 'TODO: Implement RENUM directly in interpreter instead of delegating'.

---

#### code_vs_comment

**Description:** execute_cont() docstring describes different PC handling for STOP vs Break, but execute_stop() implementation contradicts the claim

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring (lines 3063-3074): "PC handling difference:
- STOP: execute_stop() explicitly moves PC to NPC (line 2825: pc = npc), ensuring CONT resumes from the statement AFTER the STOP.
- Break (Ctrl+C): BreakException handler (line 376-381) does NOT update PC, leaving PC pointing to the statement that was interrupted."

Actual execute_stop() code (lines 3044-3049):
if self.runtime.npc:
    self.runtime.pc = self.runtime.npc.stop("STOP")
else:
    self.runtime.pc = self.runtime.pc.stop("STOP")

The code conditionally moves PC to NPC only if NPC exists, otherwise it calls stop() on PC itself. The docstring's line reference (line 2825) is incorrect and the behavior description is incomplete.

---

#### code_vs_comment

**Description:** Critical inconsistency in 'original_case' field documentation vs actual behavior

**Affected files:**
- `src/runtime.py`

**Details:**
The _variables dict documentation states:
"# Note: The 'original_case' field stores the canonical case for display (determined by case_conflict policy).
#       Despite its misleading name, this field contains the policy-resolved canonical case variant,
#       not the original case as first typed. See _check_case_conflict() for resolution logic."

However, multiple code locations contradict this:

1. In get_variable():
   self._variables[full_name]['original_case'] = canonical_case  # Canonical case for display (field name is historical, see module header)

2. In set_variable():
   self._variables[full_name]['original_case'] = canonical_case  # Canonical case for display (field name is historical, see module header)

3. In update_variables():
   'original_case': var_info.get('original_case', var_info['name'])  # Preserve canonical case

The comments say 'field name is historical' and 'Preserve canonical case', but the module header comment says it stores 'canonical case for display (determined by case_conflict policy)' and 'Despite its misleading name'. This creates confusion about whether the field name is intentionally misleading or if the behavior changed.

---

#### code_vs_comment

**Description:** create_settings_backend() docstring claims fallback to FileSettingsBackend when session_id is None happens 'without logging/warning', but code prints warnings for Redis connection failures

**Affected files:**
- `src/settings_backend.py`

**Details:**
src/settings_backend.py lines 227-234:
Docstring states: "Note: If NICEGUI_REDIS_URL is set but session_id is None, falls back to FileSettingsBackend (this is expected behavior - Redis requires both URL and session_id, so incomplete config defaults to file mode without logging/warning)."

However, lines 260-265 show:
  except ImportError:
      print("Warning: redis package not installed, falling back to file backend")
      return FileSettingsBackend(project_dir)
  except Exception as e:
      print(f"Warning: Could not connect to Redis: {e}, falling back to file backend")

The code DOES print warnings for Redis failures, contradicting the docstring claim of 'without logging/warning'. The docstring is only accurate for the session_id=None case, not all fallback cases.

---

#### Documentation inconsistency

**Description:** Settings widget references SETTING_DEFINITIONS but the actual definitions are not visible in provided code

**Affected files:**
- `src/ui/curses_settings_widget.py`
- `src/settings_definitions.py`

**Details:**
curses_settings_widget.py imports:
```python
from src.settings_definitions import SETTING_DEFINITIONS, SettingType, SettingScope
from src.settings import get, set as set_setting
```

The widget creates UI for settings grouped by category:
```python
categories = {
    'editor': [],
    'keywords': [],
    'variables': [],
}
```

However, the actual SETTING_DEFINITIONS content is not provided in the source files. This makes it impossible to verify:
1. Whether auto-save settings exist
2. What the actual setting keys and types are
3. Whether the categories match the actual settings
4. Whether the enum handling (force_ prefix stripping) is correct

---

#### code_vs_comment

**Description:** Fast path comment claims to bypass syntax checking but syntax checking happens on special keys, not printable chars

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Lines ~1010-1015 in keypress():
'# FAST PATH: For normal printable characters, bypass editor-specific processing
# (syntax checking, column protection, etc.) for responsive typing
if len(key) == 1 and key >= ' ' and key <= '~':
    return super().keypress(size, key)'

Lines ~1020-1025:
'# For special keys (non-printable), we DO process them below to handle
# cursor navigation, protection of status column, etc.'

Lines ~1040-1050:
'# Check syntax when pressing control keys, navigation keys, or switching focus
# (Not during normal typing - avoids annoying errors for incomplete lines)'

The comment on the fast path claims it bypasses syntax checking for responsive typing, but the code below shows syntax checking only happens on control/navigation keys anyway (lines ~1040-1050). The fast path doesn't actually bypass syntax checking - it bypasses column protection and cursor handling. The comment is misleading about what optimization is being performed.

---

#### code_vs_comment

**Description:** Comment says immediate mode status remains disabled during step execution, but code calls _update_immediate_status() which would re-enable it

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple comments claim immediate mode stays disabled during step execution:

Line ~913: # (Immediate mode status remains disabled - execution will show output in output window)
Line ~945: # (Immediate mode status remains disabled during execution - output shows in output window)
Line ~1012: # (Immediate mode status remains disabled during execution - output shows in output window)

However, the code in these same functions calls _update_immediate_status() after execution:

Line ~976: self._update_immediate_status()
Line ~982: self._update_immediate_status()
Line ~987: self._update_immediate_status()
Line ~1043: self._update_immediate_status()
Line ~1049: self._update_immediate_status()
Line ~1054: self._update_immediate_status()

The _update_immediate_status() method would update the status (potentially re-enabling immediate mode), contradicting the comments that say it remains disabled.

---

#### code_vs_comment

**Description:** Comment in _sync_program_to_runtime contradicts the actual PC preservation logic

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1135: 'PC handling:
- If running and not paused at breakpoint: Preserves PC and execution state
- If paused at breakpoint: Resets PC to halted (prevents accidental resumption)
- If not running: Resets PC to halted for safety'

But the actual code at line ~1160:
if self.running and not self.paused_at_breakpoint:
    # Execution is running - preserve execution state
    self.runtime.pc = old_pc
else:
    # No execution in progress or paused at breakpoint - ensure halted
    self.runtime.pc = PC.halted_pc()

The comment says 'prevents accidental resumption' when paused at breakpoint, but this conflicts with another comment in the same function that says 'When the user continues from a breakpoint (via _debug_continue), the interpreter's state already has the correct PC.' This suggests the PC reset might cause issues.

---

#### code_vs_comment_conflict

**Description:** Comment claims help navigation keys are hardcoded and not loaded from keybindings JSON, but code actually does load keybindings via HelpMacros

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at line ~73 states:
"Note: Help navigation keys are HARDCODED (not loaded from keybindings JSON) to avoid circular dependency issues. The help widget uses fixed keys (U for back, / for search, ESC/Q to exit) that work regardless of user keybinding customization.

Note: HelpMacros (instantiated below) DOES load keybindings from JSON, but only for macro expansion in help content ({{kbd:action}} substitution). The help widget's own navigation doesn't consult those loaded keybindings - it uses hardcoded keys."

However, the code at line ~48 shows:
self.macros = HelpMacros('curses', help_root)

And help_macros.py _load_keybindings() method (line ~28) loads keybindings JSON:
keybindings_path = Path(__file__).parent / f"{self.ui_name}_keybindings.json"

The comment is technically correct that help_widget.py's keypress() method uses hardcoded keys, but the phrasing "not loaded from keybindings JSON" is misleading since HelpMacros does load the JSON (just for different purpose).

---

#### documentation_inconsistency

**Description:** Multiple keybinding systems exist with unclear relationships: keybindings.py (constants), keybinding_loader.py (JSON), and hardcoded keys in help_widget.py

**Affected files:**
- `src/ui/help_macros.py`
- `src/ui/help_widget.py`
- `src/ui/interactive_menu.py`
- `src/ui/keybinding_loader.py`

**Details:**
Three different keybinding approaches are used:

1. keybinding_loader.py (lines ~1-200+): Loads from JSON files like 'curses_keybindings.json', provides get_primary(), get_all_keys() methods

2. interactive_menu.py (line ~4): Imports 'from . import keybindings as kb' and uses constants like kb.NEW_KEY, kb.OPEN_KEY

3. help_widget.py (line ~73): Uses hardcoded keys in keypress() method, with comment explaining they're intentionally not loaded from JSON

4. help_macros.py (line ~28): Loads JSON keybindings but only for macro expansion

The relationship between these systems is unclear:
- Is keybindings.py (with constants) deprecated in favor of keybinding_loader.py (JSON)?
- Why does interactive_menu.py use the old system while keybinding_loader.py exists?
- Are there two separate keybinding files: keybindings.py and curses_keybindings.json?

This needs architectural clarification.

---

#### code_vs_comment

**Description:** _ImmediateModeToken docstring states it's 'instantiated when editing variables via the variable inspector (see _on_variable_edit() around line 1194)' but the referenced function name and line number don't exist in the provided code

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines ~18-26:
class _ImmediateModeToken:
    '''Token for variable edits from immediate mode or variable editor.

    This class is instantiated when editing variables via the variable inspector
    (see _on_variable_edit() around line 1194). Used to mark variable changes that
    originate from the variable inspector or immediate mode, not from program
    execution. The line=-1 signals to runtime.set_variable() that this is a
    debugger/immediate mode edit.
    '''

The code ends at line ~1094 with _on_variable_double_click() method, and there is no _on_variable_edit() method visible in the provided code. The line reference 'around line 1194' is beyond the provided code.

---

#### code_vs_comment

**Description:** Comment claims blank lines are removed but the actual removal happens in a different method

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_enter_key method around line 1010:
Comment says: '# At this point, the editor contains only the numbered lines (no blank lines)\n# because _refresh_editor loads from the program, which filters out blank lines'

But _refresh_editor doesn't filter blank lines - it loads from program.get_lines() which returns stored lines. The actual blank line removal happens in _remove_blank_lines() which is scheduled via _on_key_press. This comment misattributes the filtering mechanism.

---

#### code_vs_comment

**Description:** Comment describes character positions as 'directly usable' but doesn't explain coordinate system assumptions

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _highlight_current_statement method around line 1590:
Comment says: 'Lines in the editor match the program manager's formatted output (see _refresh_editor).\nThe char_start/char_end positions from runtime correspond to the displayed line text,\nso they are directly usable as Tk text indices.'

This assumes that char_start/char_end are 0-based column positions that match Tk's text widget column indexing. However, there's no validation or explanation of what happens if the runtime uses a different coordinate system (e.g., 1-based, or byte offsets). This could cause highlighting bugs if the assumption is violated.

---

#### code_vs_comment

**Description:** Comment warns about maintenance risk but duplicates logic anyway, creating fragile code

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_immediate method:
"# NOTE: Don't call interpreter.start() because it calls runtime.setup()
# which resets PC to the first statement. The RUN command has already
# set PC to the correct line (e.g., RUN 120 sets PC to line 120).
# Instead, we manually perform minimal initialization here.
#
# MAINTENANCE RISK: This duplicates part of start()'s logic (see interpreter.start()
# in src/interpreter.py). If start() changes, this code may need to be updated to
# match. We only replicate the minimal setup needed (marking first line) while
# avoiding the full initialization that start() does:
#   - runtime.setup() (rebuilds tables, resets PC) <- THIS is what we avoid
#   - Creates new InterpreterState
#   - Sets up Ctrl+C handler"

The code then does:
self.interpreter.state.is_first_line = True

This is a known fragile pattern that will break if interpreter.start() changes its initialization sequence. The comment acknowledges the risk but doesn't suggest a better solution.

---

#### code_vs_comment

**Description:** Comment in _delete_line() docstring describes parameter as 'Tkinter text widget line number (1-based sequential index), not BASIC line number', but the method is called with self.current_line which comes from cursor position tracking and is used directly as a text widget line number. However, the comment also mentions 'dual numbering' and 'BASIC line numbers for line_metadata lookups', which is correct for other methods but confusing here since _delete_line only uses editor line numbers.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Docstring says: 'line_num: Tkinter text widget line number (1-based sequential index), not BASIC line number (e.g., 10, 20, 30). Note: This class uses dual numbering - editor line numbers for text widget operations, BASIC line numbers for line_metadata lookups.'

Code usage in _on_cursor_move():
self.text.after_idle(self._delete_line, self.current_line)

where self.current_line = int(cursor_pos.split('.')[0])

The docstring is technically correct but the 'dual numbering' note is misleading in this context since _delete_line never interacts with line_metadata or BASIC line numbers.

---

#### code_vs_comment

**Description:** Comment claims Step commands clear output for debugging clarity, but code does not implement this

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment in _menu_run (line ~1845) states:
"# Note: Step commands (Ctrl+T/Ctrl+K) DO clear output for clarity when debugging"

However, examining _menu_step_line and _menu_step_stmt implementations:
- Both contain comment: "# Note: Output is NOT cleared - continuous scrolling like ASR33 teletype"
- Neither method contains any code that clears self.output.value or calls _clear_output()
- The behavior described in the RUN comment contradicts both the step method comments and the actual code implementation

---

#### code_vs_comment

**Description:** Comment claims _get_input returns empty string to signal interpreter state transition, but this behavior is not clearly documented in the interpreter contract

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_get_input() method:

Comment: "# Return empty string - signals interpreter to transition to 'waiting_for_input'
# state (state transition happens in interpreter when it receives empty string
# from input()). Execution pauses until _handle_output_enter() calls provide_input().
return ''"

This describes a specific protocol (empty string triggers state transition) but there's no visible documentation of this contract. If the interpreter changes its behavior for empty input, this code will break silently.

---

#### documentation_inconsistency

**Description:** Contradictory information about D vs E notation for exponents

**Affected files:**
- `docs/help/common/language/data-types.md`

**Details:**
data-types.md states under DOUBLE Precision: 'D notation (e.g., 1.5D+10) forces double-precision, required for exponents beyond single-precision range' and 'E notation (e.g., 1.5E+10) uses single-precision by default, converts to double if assigned to # variable'. However, it then says 'For values within single-precision range, D and E are interchangeable when assigned to # variables.' This is contradictory - if D 'forces' double-precision and E 'uses single-precision by default', they cannot be truly interchangeable even when assigned to # variables, as the intermediate calculation precision would differ.

---

#### documentation_inconsistency

**Description:** FOR-NEXT loop termination test description has internal contradiction

**Affected files:**
- `docs/help/common/language/statements/for-next.md`

**Details:**
for-next.md states:
"### Loop Termination:
The termination test happens AFTER each increment/decrement at the NEXT statement:
- **Positive STEP** (or no STEP): Loop continues while variable <= ending value
- **Negative STEP**: Loop continues while variable >= ending value

For example:
- `FOR I = 1 TO 10` executes with I=1,2,3,...,10 (10 iterations). After I=10 executes, NEXT increments to 11, test fails (11 > 10), loop exits.
- `FOR I = 10 TO 1 STEP -1` executes with I=10,9,8,...,1 (10 iterations). After I=1 executes, NEXT decrements to 0, test fails (0 < 1), loop exits."

The second example says 'test fails (0 < 1)' but according to the rule for negative STEP, the loop should continue while 'variable >= ending value'. So 0 >= 1 is false, which means the test passes (loop should exit). The wording 'test fails' is confusing - it should say 'test is false' or 'condition is false'.

---

#### documentation_inconsistency

**Description:** Contradictory implementation status for line printer features

**Affected files:**
- `docs/help/common/language/statements/llist.md`
- `docs/help/common/language/statements/lprint-lprint-using.md`

**Details:**
LLIST states: '⚠️ **Not Implemented**: This feature requires line printer hardware and is not implemented'

LPRINT states: '⚠️ **Not Implemented**: This feature requires line printer hardware and is not implemented'

Both claim to be 'not implemented' but LLIST says 'Statement is parsed but no listing is sent to a printer' while LPRINT says 'Statement is parsed but no output is sent to a printer'. However, both are marked as 'Versions: Extended, Disk' suggesting they should be available in those versions. This creates confusion about actual implementation status.

---

#### documentation_inconsistency

**Description:** Inconsistent implementation note formatting and detail level between WAIT and WIDTH.

**Affected files:**
- `docs/help/common/language/statements/width.md`
- `docs/help/common/language/statements/wait.md`

**Details:**
wait.md has detailed implementation note with sections:
- ⚠️ **Not Implemented**
- **Behavior**
- **Why**
- **Limitations**
- **Alternative**
- **Historical Reference**

width.md has similar note but less structured:
- ⚠️ **Not Implemented**
- **Behavior**
- **Why**
- **Limitations**
- **Alternative**
- **Historical Reference**

Both should use identical formatting structure for consistency.

---

#### documentation_inconsistency

**Description:** Conflicting information about Web UI file persistence

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/extensions.md`

**Details:**
compatibility.md states: 'Files stored in server-side memory (sandboxed filesystem per session)' and 'Files persist during browser session but are lost on page refresh' and 'Note: Settings (not files) persist in browser localStorage by default, or via Redis if configured'.

extensions.md states: 'Auto-save behavior varies by UI: **Web UI:** Files stored in server-side session memory only (not persistent across page refreshes)'.

The compatibility.md mentions localStorage and Redis for settings persistence, but this detail is missing from extensions.md. Also, the phrasing 'persist during browser session but are lost on page refresh' is contradictory - a page refresh typically ends the session.

---

#### documentation_inconsistency

**Description:** Self-contradictory statement about Web UI file persistence

**Affected files:**
- `docs/help/mbasic/extensions.md`

**Details:**
extensions.md states: 'Files persist during browser session only (lost on page refresh)'.

This is contradictory because a 'browser session' typically refers to the time the browser tab/window is open. A page refresh does NOT end the browser session in standard web terminology - closing the tab/window does.

The documentation should clarify whether files persist across page refreshes within the same browser session, or if they are truly lost on refresh.

---

#### documentation_inconsistency

**Description:** Contradictory information about LINE statement

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
features.md under Input/Output lists 'LINE INPUT - Full line input (Note: Graphics LINE statement is not implemented)'. However, not-implemented.md states 'LINE - Draw line (GW-BASIC graphics version - not the LINE INPUT statement which IS implemented)'. Both documents agree LINE INPUT is implemented and graphics LINE is not, but the phrasing and emphasis differ in ways that could confuse readers about what 'LINE' refers to.

---

#### documentation_inconsistency

**Description:** Contradictory information about variable editing capability

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
In variables.md: "⚠️ **Not Implemented**: You cannot edit variable values directly in the variables window."

In feature-reference.md: "### Edit Variable Value (Not implemented)
⚠️ Variable editing is not available in Curses UI. You cannot directly edit values in the variables window."

Both correctly state it's not implemented, but variables.md has a full section titled 'Limitations' with 'Variable Editing Not Available' while feature-reference.md lists it as a feature with '(Not implemented)' tag. This is consistent but could be clearer about whether it's a planned feature or permanent limitation.

---

#### documentation_inconsistency

**Description:** Execution Stack keyboard shortcut inconsistency

**Affected files:**
- `docs/help/ui/curses/quick-reference.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
In quick-reference.md: "| **Menu only** | Toggle execution stack window |"

In feature-reference.md: "**How to access:**
1. Press Ctrl+U to open the menu bar
2. Navigate to the Debug menu
3. Select 'Execution Stack' option

Note: There is no dedicated keyboard shortcut to avoid conflicts with editor typing."

The quick-reference says 'Menu only' but doesn't explain how to access the menu. The feature-reference explains the menu access method (Ctrl+U) but this should be consistent across both documents.

---

#### documentation_inconsistency

**Description:** Contradictory information about Find/Replace keyboard shortcuts and functionality

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/features.md`

**Details:**
feature-reference.md states:
"Find/Replace ({{kbd:find:tk}} / {{kbd:replace:tk}})
Powerful search and replace functionality:
- Find: {{kbd:find:tk}} - Opens Find-only dialog
- Replace: {{kbd:replace:tk}} - Opens combined Find/Replace dialog (includes both find and replace)"

But features.md states:
"Find and Replace
**Find text ({{kbd:find:tk}}):**
- Opens Find dialog with search options
**Replace text ({{kbd:replace:tk}}):**
- Opens combined Find/Replace dialog
**Note:** {{kbd:find:tk}} opens the Find dialog. {{kbd:replace:tk}} opens the Find/Replace dialog which includes both Find and Replace functionality."

The inconsistency: feature-reference.md says Find opens a "Find-only dialog" while features.md says Find opens "Find dialog with search options" (not explicitly "find-only"). The note in features.md clarifies that Replace includes both, but the description of Find is ambiguous.

---

#### documentation_inconsistency

**Description:** Contradictory information about Web UI debugger capabilities

**Affected files:**
- `docs/help/ui/index.md`
- `docs/help/ui/web/debugging.md`

**Details:**
index.md comparison table states for Web UI Debugger:
"Limited | Web: breakpoints, step, basic stack/vars (no advanced panels)"

But debugging.md extensively describes the debugger as having:
- "Basic breakpoint management (via Run menu)" (currently implemented)
- "Basic variable inspection (via Debug menu)" (currently implemented)
- Many features marked as "Planned" including Variables Panel, Watch Expressions, Advanced Stack Panel, Logpoints, Data Breakpoints, Debug Console, Performance Profiling

The index.md suggests more is currently available than debugging.md indicates. The index should clarify what "basic stack/vars" means and that most advanced features are planned, not implemented.

---

#### documentation_inconsistency

**Description:** Settings dialog implementation status unclear across documents

**Affected files:**
- `docs/help/ui/tk/settings.md`
- `docs/help/ui/tk/workflows.md`
- `docs/help/ui/tk/tips.md`

**Details:**
settings.md clearly states at the top:
"**Implementation Status:** The Tk (Tkinter) desktop GUI is planned to provide a comprehensive settings dialog. **The settings dialog itself is not yet implemented - settings are currently managed programmatically.**"

However, workflows.md and tips.md reference features like Smart Insert, Variables Window, Execution Stack, and Renumber as if they are fully implemented, with notes like:
"**Note:** The Tk UI has most features described below implemented (Smart Insert, Variables Window, Execution Stack, Renumber). The Settings dialog for configuring these features is planned but not yet implemented"

This creates confusion: Are the features implemented but just not configurable via dialog? Or are the features themselves not implemented? The distinction between "feature exists but no settings UI" vs "feature doesn't exist" needs clarification across all documents.

---

#### documentation_inconsistency

**Description:** Contradictory information about Variables Window availability

**Affected files:**
- `docs/help/ui/index.md`
- `docs/help/ui/tk/feature-reference.md`

**Details:**
index.md comparison table states for Tk UI:
"Variables Window | ✓"

This suggests the Variables Window is fully available in Tk UI. However, feature-reference.md describes it as a feature but settings.md indicates the settings dialog to configure it is not implemented. Additionally, workflows.md includes a note:
"**Note:** The Tk UI has most features described below implemented (Smart Insert, Variables Window, Execution Stack, Renumber)."

This suggests Variables Window IS implemented, but the settings to configure it are not. The index.md should clarify whether "✓" means "fully implemented and configurable" or just "feature exists".

---

#### documentation_inconsistency

**Description:** Contradictory information about program storage and auto-save functionality

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/settings.md`

**Details:**
features.md states under 'Local Storage > Currently Implemented': 'Program content stored in Python server memory (session-only, lost on page refresh)' and 'Recent files list (filenames only) stored in browser localStorage (persists across sessions)'

However, settings.md states under 'Settings Storage > Local Storage (Default)': 'By default, settings are stored in your browser's localStorage' and mentions 'Your editor settings ARE already saved to localStorage'

But getting-started.md says under 'Saving a File': 'Note: The Web UI uses browser downloads for saving program files to your computer. Auto-save of program code to browser localStorage is planned for a future release. (Note: Your editor settings ARE already saved to localStorage - see Settings)'

The confusion is: Are programs stored in server memory OR localStorage? The docs say both 'server memory (session-only)' and 'Auto-save of program code to browser localStorage is planned' which suggests programs are NOT in localStorage yet, only settings are.

---

#### documentation_inconsistency

**Description:** Contradictory information about file I/O persistence

**Affected files:**
- `docs/help/ui/web/web-interface.md`
- `docs/help/ui/web/features.md`

**Details:**
web-interface.md under 'File I/O' states: 'Files are stored in browser memory only' and 'Files persist during your session (but are cleared when session ends)'

But features.md under 'Local Storage > Currently Implemented' says: 'Program content stored in Python server memory (session-only, lost on page refresh)'

The contradiction is: Are files stored in 'browser memory' or 'Python server memory'? These are different locations with different implications for multi-tab behavior and server restarts.

Also, web-interface.md says files persist 'during your session' but features.md says 'lost on page refresh' - a page refresh is typically within the same session.

---

#### documentation_inconsistency

**Description:** Missing CLI debugging documentation despite claims of full debugging capabilities

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`
- `docs/user/QUICK_REFERENCE.md`

**Details:**
CHOOSING_YOUR_UI.md explicitly states CLI has debugging:
'**CLI is perfect for:**
```bash
# Debugging
python3 mbasic --debug program.bas
```'

and

'**Unique advantages:**
- Command-line debugging (BREAK, STEP, STACK commands)'

and

'**Limitations:**
- Line-by-line editing only
- No visual debugging interface (debugging via text commands only)'

This clearly indicates CLI supports BREAK, STEP, and STACK commands for debugging. However, QUICK_REFERENCE.md only documents Curses UI debugging and there is no CLI debugging reference document. Users wanting to use CLI debugging have no documentation on how to use these commands.

---

### 🟡 Medium Severity

#### documentation_inconsistency

**Description:** Version number inconsistency between setup.py and ast_nodes.py module docstring

**Affected files:**
- `setup.py`
- `src/ast_nodes.py`

**Details:**
setup.py states 'Package version: 0.99.0 (reflects approximately 99% implementation status - core complete)' and 'Language version: MBASIC 5.21 (Microsoft BASIC-80 for CP/M)'. The ast_nodes.py module docstring only mentions '5.21 refers to the Microsoft BASIC-80 language version, not this package version' but doesn't mention the package version 0.99.0 anywhere. This creates potential confusion about versioning.

---

#### code_vs_comment_conflict

**Description:** LineNode docstring claims no source_text field but doesn't explain char_start/char_end in StatementNode

**Affected files:**
- `src/ast_nodes.py`

**Details:**
LineNode docstring states: 'Design note: This class intentionally does not have a source_text field to avoid maintaining duplicate copies that could get out of sync with the AST during editing. Text regeneration is handled by the src.position_serializer module...'

However, StatementNode has char_start and char_end fields with a note: 'Note: char_start/char_end are populated by the parser and used by: - UI highlighting... - Position serializer: Preserves exact character positions for text regeneration'

The relationship between 'no source_text in LineNode' and 'char_start/char_end in StatementNode for text regeneration' is not clearly explained. It's unclear how text is regenerated from char positions without storing the original text somewhere.

---

#### documentation_inconsistency

**Description:** InputStatementNode has complex semicolon behavior that may be confusing

**Affected files:**
- `src/ast_nodes.py`

**Details:**
InputStatementNode docstring explains: 'The suppress_question field controls "?" display:
- suppress_question=False (default): Adds "?" after prompt
  Examples: INPUT var → "? ", INPUT "Name", var → "Name? "
- suppress_question=True: No "?" added (for INPUT; syntax)
  Examples: INPUT; var → "" (no prompt), INPUT "prompt"; var → "prompt" (no "?")

Semicolon usage in MBASIC:
- INPUT; var → semicolon immediately after INPUT (sets suppress_question=True)
- INPUT "prompt"; var → semicolon after prompt is just separator (suppress_question=False)'

This is confusing because:
1. INPUT "prompt"; var has a semicolon but suppress_question=False
2. INPUT; var has a semicolon and suppress_question=True
3. The distinction between 'semicolon immediately after INPUT' vs 'semicolon after prompt' is subtle and may lead to parser bugs

---

#### documentation_inconsistency

**Description:** VariableNode type_suffix and explicit_type_suffix relationship is complex and may cause bugs

**Affected files:**
- `src/ast_nodes.py`

**Details:**
VariableNode docstring explains: 'Type suffix handling:
- type_suffix: The actual suffix character ($, %, !, #) when present
- explicit_type_suffix: Boolean indicating the origin of type_suffix:
    * True: suffix appeared in source code (e.g., "X%" in "X% = 5")
    * False: suffix inferred from DEFINT/DEFSNG/DEFDBL/DEFSTR (e.g., "X" with DEFINT A-Z)

Source code regeneration rules:
- When explicit_type_suffix=True: suffix IS included in regenerated source (e.g., "X%")
- When explicit_type_suffix=False: suffix is NOT included in regenerated source (e.g., "X")'

This creates potential for bugs because:
1. type_suffix can be non-None even when explicit_type_suffix=False
2. Code must check BOTH fields to correctly handle variables
3. It's unclear what happens if type_suffix=None and explicit_type_suffix=True (invalid state?)
4. The example 'In "DEFINT A-Z: X=5", variable X has type_suffix="%" and explicit_type_suffix=False' shows that type_suffix is populated even when not explicit, which may surprise developers

---

#### code_vs_comment

**Description:** Comment describes INPUT$ file number parameter as 'WITHOUT the # prefix' but implementation expects it already stripped

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Comment at line 1009: 'This method receives the file number WITHOUT the # prefix (parser strips it).'
Comment at line 1013: 'INPUT$(n, #filenum) - read n characters from file'
Comment at line 1016: 'INPUT(n, filenum) - read n characters from file (# prefix already stripped)'

The comment correctly states the parser strips the # prefix, but the phrasing 'WITHOUT the # prefix' could be clearer about whether this is a requirement or observation.

---

#### code_vs_comment

**Description:** Comment about negative zero handling in format_numeric_field is verbose and potentially confusing

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Lines 373-378 contain detailed comment:
'# Determine sign - preserve negative sign for values that round to zero.
# Use original_negative (captured above before rounding) to detect negative values that rounded to zero.
# This allows us to detect cases like -0.001 which round to 0 but should display as "-0" (not "0").
# This matches MBASIC 5.21 behavior: negative values that round to zero display as "-0",
# while positive values that round to zero display as "0".'

The comment is accurate but the phrase 'Determine sign BEFORE rounding (for negative zero handling)' at line 368 already captured before the rounding at line 371, making the later comment somewhat redundant.

---

#### code_vs_comment

**Description:** Comment about leading sign format padding behavior may be misleading

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line 434: '# For leading sign: padding comes first (spaces only), then sign immediately before number'
Line 435: '# Note: Leading sign format uses spaces for padding, never asterisks (even if ** specified)'

The code at lines 437-439 implements this, but the comment 'even if ** specified' is potentially confusing because if ** is specified with leading +, the ** would be parsed as part of the numeric field before the +, not as padding for the leading sign format. The comment might imply a conflict that doesn't actually exist in practice.

---

#### code_comment_conflict

**Description:** Comment says GOSUB stack stores 'Return IDs (0, 1, 2...)' but implementation may be inconsistent

**Affected files:**
- `src/codegen_backend.py`

**Details:**
Line 147-148 comment:
'int gosub_stack[100];  /* Return IDs (0, 1, 2...) - not line numbers */'

But the _generate_gosub method (lines 382-389) generates:
'gosub_stack[gosub_sp++] = {return_id};  /* Push return address */'

And _generate_return (lines 391-410) generates a switch statement on return IDs.

The comment explicitly says 'not line numbers' which matches the implementation, but the comment on line 388 says '/* Push return address */' which could be misleading since it's pushing an ID, not an address. This is a minor terminology inconsistency in comments.

---

#### documentation_inconsistency

**Description:** Documentation claims FileIO abstraction exists but doesn't reference the actual file location

**Affected files:**
- `src/editing/manager.py`

**Details:**
manager.py lines 13-28 state:
"Related filesystem abstractions:
1. FileIO (src/file_io.py) - Planned abstraction for LOAD/SAVE/MERGE/KILL commands
   - NOT currently used by LOAD/SAVE commands (they call ProgramManager directly)
   - Provides backend-agnostic interface for future web UI support
   - RealFileIO: direct filesystem access for local UIs
   - SandboxedFileIO: in-memory virtual filesystem for web UI (not yet integrated)

2. FileSystemProvider (src/filesystem/base.py) - For runtime BASIC file I/O
   - Used during program execution (OPEN, INPUT#, PRINT#, CLOSE, etc.)
   - Separate from program loading (LOAD/SAVE which load .BAS source files)"

The documentation references src/file_io.py and src/filesystem/base.py but these files are not provided in the source code files for analysis. This makes it impossible to verify if the described architecture actually exists or if the documentation is aspirational/outdated.

---

#### Documentation inconsistency

**Description:** Contradictory statements about whether FileSystemProvider supports runtime file listing/deletion

**Affected files:**
- `src/file_io.py`
- `src/filesystem/base.py`

**Details:**
src/file_io.py states: "though not all BASIC dialects support runtime file listing/deletion" suggesting it's optional/dialect-dependent.

src/filesystem/base.py states: "Also provides: list_files() and delete() for runtime use" as if these are standard features.

Both files acknowledge the overlap but give different impressions about whether these methods are expected to be used at runtime.

---

#### Documentation inconsistency

**Description:** SandboxedFileIO docstring has contradictory statements about implementation status

**Affected files:**
- `src/file_io.py`

**Details:**
The docstring states:

"Implementation status:
- list_files(): IMPLEMENTED - delegates to backend.sandboxed_fs..."

But then later says:

"Why only list_files() is implemented: The sandboxed_fs filesystem already exists for runtime file I/O (OPEN/CLOSE/PRINT#). The list_files() method simply queries what files exist in that already-functional in-memory filesystem."

This implies list_files() works by querying runtime files created by BASIC programs (OPEN/PRINT#), but the FILES command in BASIC is meant to list .BAS program files, not runtime data files. The documentation conflates two different file namespaces without clarifying whether they're the same or different.

---

#### Code vs Documentation inconsistency

**Description:** Security documentation claims about user_id validation are not enforced in code

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
Documentation states:
"SECURITY: Must be securely generated/validated (e.g., session IDs) to prevent cross-user access. Do NOT use user-provided values."

And:
"IMPORTANT: Caller must ensure user_id is securely generated/validated to prevent cross-user access (e.g., use session IDs, not user-provided values)"

However, the __init__ method accepts user_id as a plain string with no validation:
```
def __init__(self, user_id: str, max_files: int = 50, max_file_size: int = 1024 * 1024):
    self.user_id = user_id
```

The code places full responsibility on the caller but provides no enforcement, type checking, or validation. This is a security-critical parameter with no safeguards.

---

#### Code vs Documentation inconsistency

**Description:** SandboxedFileIO.list_files() error handling doesn't match documented behavior

**Affected files:**
- `src/file_io.py`

**Details:**
Docstring states: "Returns empty list if backend.sandboxed_fs doesn't exist. Catches exceptions and returns (filename, None, False) for files that can't be stat'd."

Code implementation:
```
if hasattr(self.backend, 'sandboxed_fs'):
    pattern = filespec.strip().strip('"').strip("'") if filespec else None
    files = self.backend.sandboxed_fs.list_files(pattern)
    result = []
    for filename in files:
        try:
            size = self.backend.sandboxed_fs.get_size(filename)
            result.append((filename, size, False))
        except:
            result.append((filename, None, False))
    return result
return []
```

The code does catch exceptions in the try/except block as documented. However, if backend.sandboxed_fs.list_files(pattern) itself raises an exception (not caught), the method would raise rather than return an empty list. The documentation implies all exceptions are caught.

---

#### code_vs_comment_conflict

**Description:** Comment claims INPUT statement will fail at parse time, but code shows it fails at runtime

**Affected files:**
- `src/immediate_executor.py`

**Details:**
In OutputCapturingIOHandler.input() method:

Comment says: "INPUT not supported in immediate mode (fails at parse time)"

But the implementation raises RuntimeError when input() is called, which is runtime, not parse time. The docstring correctly states "INPUT statement will fail at runtime in immediate mode" and explains "INPUT statements parse successfully but execution fails when the interpreter calls this input() method."

---

#### code_vs_comment_conflict

**Description:** Comment about PC save/restore contradicts actual implementation behavior

**Affected files:**
- `src/immediate_executor.py`

**Details:**
After executing statements, there's a comment:
"# Note: We do not save/restore the PC before/after execution by design.
# This allows statements like RUN to properly change execution position.
# Tradeoff: Control flow statements (GOTO, GOSUB) can also modify PC but are
# not recommended in immediate mode as they may produce unexpected results"

However, there is no code that actually saves or restores PC anywhere in the method. The comment describes a design decision about NOT doing something that was never implemented in the first place. This appears to be a comment from a refactoring where PC save/restore was removed, but the explanatory comment remained.

---

#### code_vs_documentation_inconsistency

**Description:** Module docstring describes two-step process but sanitize_input doesn't validate parity clearing happened

**Affected files:**
- `src/input_sanitizer.py`

**Details:**
Module docstring states:
"This module provides functions to sanitize user input through a two-step process:
1. First: Clear parity bits from incoming characters (bit 7)
2. Then: Filter out unwanted control characters"

And later:
"Note: This function is typically called after clear_parity_all() in the sanitize_and_clear_parity() pipeline, where parity bits have already been cleared. It validates that characters are in the valid range (32-126, plus tab/newline/CR)."

However, sanitize_input() doesn't actually validate that parity bits were cleared - it just filters characters. A character with bit 7 set (e.g., chr(193)) would be filtered out by is_valid_input_char() because it's > 127, but this is filtering, not validating that parity clearing happened. The documentation implies validation occurs but the code just filters.

---

#### code_vs_comment

**Description:** Comment claims digits 'silently do nothing' in EDIT mode, but code has no explicit handling for digits

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~1050 says: 'INTENTIONAL MBASIC-COMPATIBLE BEHAVIOR: When digits are entered, they silently do nothing (no output, no cursor movement, no error)... Implementation: digits fall through the command checks without matching any elif branch.'

However, in the actual EDIT command implementation (cmd_edit method starting ~1060), there is no explicit handling or documentation of digit behavior. The while loop at ~1090 handles various commands (Space, D, I, X, H, E, Q, L, A, C) but has no elif branch or comment explaining digit handling. If digits truly 'fall through', they would reach the end of the if/elif chain with no action, but this is not explicitly documented in the code itself.

---

#### code_vs_comment

**Description:** Comment about MERGE variable passing behavior contradicts itself

**Affected files:**
- `src/interactive.py`

**Details:**
In cmd_chain method (~730), comment says:
'Save variables based on CHAIN options:
- ALL: passes all variables to the chained program
- MERGE: merges program lines (overlays code) - NOTE: Currently also passes all vars
- Neither: passes only COMMON variables'

Then immediately says:
'MBASIC 5.21 behavior: MERGE and ALL are orthogonal options.
Current implementation: Both MERGE and ALL result in passing all variables.
TODO: Separate line merging (MERGE) from variable passing (ALL).'

The code at ~745 implements: 'if all_flag or merge: saved_variables = self.program_runtime.get_all_variables()'

This is confusing because the comment first says MERGE 'merges program lines' (implying it shouldn't pass vars), then says it 'Currently also passes all vars', then says MERGE and ALL are 'orthogonal' (should be independent), but the implementation treats them as equivalent (both pass all vars). The TODO suggests this is a known bug, but the comment structure is contradictory.

---

#### code_vs_comment

**Description:** RENUM docstring describes ERL handling as 'intentionally broader' but doesn't explain the trade-off clearly

**Affected files:**
- `src/interactive.py`

**Details:**
In cmd_renum method (~950), docstring says:
'ERL handling: ERL expressions with ANY binary operators (ERL+100, ERL*2, ERL=100) have all right-hand numbers renumbered, even for arithmetic operations. This is intentionally broader than the MBASIC manual (which only specifies comparison operators) to avoid missing line references. Known limitation: arithmetic expressions like "IF ERL+100 THEN..." will incorrectly renumber the 100 if it happens to be an old line number. This is rare in practice.'

Then in _renum_erl_comparison method (~1020), a longer comment repeats this but adds:
'INTENTIONAL DEVIATION FROM MANUAL... This is a deliberate design choice to avoid missing valid line number references... Known limitation: Arithmetic like "IF ERL+100 THEN..." will incorrectly renumber the 100 if it happens to be an old line number. This is rare in practice.'

The issue: both comments acknowledge this causes incorrect renumbering but dismiss it as 'rare in practice' without explaining WHY this trade-off was chosen. A better explanation would be: 'We cannot distinguish ERL=100 (comparison, should renumber) from ERL+100 (arithmetic, should not) without semantic analysis, so we conservatively renumber both to avoid missing valid line references.' The current wording makes it sound like a bug rather than a deliberate conservative choice.

---

#### code_vs_comment_conflict

**Description:** Comment claims 'second return value is bool indicating if parity bits were found; not needed here' but sanitize_and_clear_parity() is called with only one assignment target

**Affected files:**
- `src/interactive.py`

**Details:**
Line ~150: Comment says:
# (second return value is bool indicating if parity bits were found; not needed here)
line_text, _ = sanitize_and_clear_parity(line_text)

But in cmd_edit() around line 80, the same function is called without unpacking:
line_text = sanitize_and_clear_parity(line_text)

This suggests either:
1. The function returns a tuple in AUTO but not in EDIT (inconsistent)
2. The comment is wrong and function always returns just a string
3. The EDIT code is missing the unpacking

---

#### code_vs_comment_conflict

**Description:** Comment about line_text_map in immediate mode contradicts the actual parameter passed

**Affected files:**
- `src/interactive.py`

**Details:**
In execute_immediate() around line 330:
Comment says:
# Pass empty line_text_map since immediate mode uses temporary line 0.
# Design note: Could pass {0: statement} to improve error reporting, but immediate
# mode errors typically reference the statement the user just typed (visible on screen),
# so line_text_map provides minimal benefit.

But the code passes: self.runtime = Runtime(ast, {})

The comment suggests passing {0: statement} would be possible and potentially useful, but then dismisses it. However, the comment doesn't match the actual behavior - it should either pass {0: statement} or the comment should be updated to reflect why {} is definitively correct, not just 'minimal benefit'.

---

#### code_vs_comment_conflict

**Description:** Comment in cmd_auto() about sanitize_and_clear_parity return value doesn't match usage in cmd_edit()

**Affected files:**
- `src/interactive.py`

**Details:**
In cmd_auto() around line 150:
line_text, _ = sanitize_and_clear_parity(line_text)

But in cmd_edit() around line 80:
line_text = sanitize_and_clear_parity(line_text)

One unpacks a tuple, one doesn't. Either:
1. The function has inconsistent return types (bug)
2. One of these usages is wrong
3. The function was refactored and one call site wasn't updated

This is the same issue as the first entry but worth highlighting the specific inconsistency between the two call sites.

---

#### code_vs_comment

**Description:** Comment describes skip_next_breakpoint_check behavior incorrectly - says it's set AFTER halting, but code sets it DURING halting check

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line 56-59 says:
"Set to True AFTER halting at a breakpoint (set after returning state).
On next execution, if still True, allows stepping past the breakpoint once,
then is cleared to False. Prevents re-halting on same breakpoint."

But code at lines 382-387 shows:
if at_breakpoint:
    if not self.state.skip_next_breakpoint_check:
        self.runtime.pc = pc.stop("BREAK")
        self.state.skip_next_breakpoint_check = True  # Set DURING halt, not after
        return self.state
    else:
        self.state.skip_next_breakpoint_check = False

---

#### code_vs_comment

**Description:** Comment about error_info timing contradicts actual code flow

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line 1009 says:
"Note: error_info is set in the exception handler in tick_pc() just before
calling this method. We're now ready to invoke the error handler."

This is correct for the normal exception path (line 418), but the comment doesn't mention that error_info is ALSO set earlier at line 406 for both handler and no-handler cases. The comment implies error_info is only set just before _invoke_error_handler(), but it's actually set for all errors regardless of whether a handler exists.

---

#### code_vs_comment

**Description:** execute_next() docstring incorrectly describes parser behavior for colon-separated NEXT statements

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring at lines 1249-1260 says:
"Note: This method handles a single NEXT statement, which may contain comma-separated
variables (NEXT I, J, K). The parser treats colon-separated NEXT statements
(NEXT I: NEXT J: NEXT K) as distinct statements, each calling execute_next()
independently. This method does NOT handle the colon-separated case - that's
handled by the parser creating multiple statements."

This comment makes a claim about parser behavior ("The parser treats colon-separated NEXT statements as distinct statements") but we cannot verify this from the provided code. The parser code is not included in the source files. This could be correct, outdated, or incorrect - we need to see the parser to verify.

---

#### code_vs_comment

**Description:** Comment describes NEXT without variable using current line for token, but code uses PC line number which may be 0 if not running

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1157: "NEXT without variable - use current line for token"
Code creates TokenInfo with: self.runtime.pc.line_num if self.runtime.pc.is_running() else 0
This means if PC is not running (halted/stopped), line_num will be 0, not the "current line" as comment suggests. The comment should clarify this edge case or the code should handle it differently.

---

#### code_vs_comment

**Description:** RESUME statement comment says 'MBASIC allows both RESUME and RESUME 0 as equivalent' but implementation treats None and 0 identically without preserving distinction

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1295: "Note: MBASIC allows both 'RESUME' and 'RESUME 0' as equivalent syntactic forms. Parser preserves the distinction (None vs 0) for source text regeneration, but runtime execution treats both identically."
Code at line ~1302: if stmt.line_number is None or stmt.line_number == 0:
This correctly implements the behavior, but the comment claims parser preserves distinction for source text regeneration. However, if both None and 0 execute identically, there's no way to know which form was originally used after execution. This suggests either: (1) the parser doesn't actually preserve the distinction in a way that matters, or (2) the comment is misleading about what 'preserve' means.

---

#### code_vs_comment

**Description:** CLEAR comment mentions RESET allowing errors to propagate, but RESET is not shown in this code file

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1437: "This differs from RESET which allows errors to propagate."
No execute_reset method is visible in the provided code. Either: (1) RESET is in a different part of the file not shown, (2) RESET is not implemented, or (3) the comment is outdated. This creates confusion about the actual behavior difference.

---

#### code_vs_comment

**Description:** Comment about latin-1 encoding says 'Future enhancement: Add optional encoding conversion' but this is in implementation code, not a TODO

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1651: "Note: CP/M systems often used code pages like CP437 or CP850 for characters 128-255, which do NOT match latin-1. Latin-1 preserves the BYTE VALUES but not necessarily the CHARACTER MEANING for non-ASCII CP/M text. Future enhancement: Add optional encoding conversion setting for CP437/CP850 display."
This 'Future enhancement' note is embedded in a docstring explaining current behavior. It should either be: (1) a TODO comment, (2) a GitHub issue reference, or (3) removed if not planned. Docstrings should describe what the code does, not what it might do in the future.

---

#### code_vs_comment

**Description:** CLOSE statement comment says 'Silently ignores closing unopened files' but code only closes files that exist in runtime.files

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~2055: "Note: Silently ignores closing unopened files (MBASIC 5.21 compatibility). This allows defensive CLOSE patterns like: CLOSE #1: CLOSE #2: CLOSE #3 which ensure files are closed without needing to track which files are open."
Code at line ~2067: if file_num in self.runtime.files:
The code checks if file_num exists before closing, which means it silently ignores unopened files. However, the comment doesn't mention that evaluating the file number expression still happens (and could raise errors). The comment should clarify that only the close operation is skipped, not the expression evaluation.

---

#### code_vs_comment

**Description:** execute_reset() docstring claims errors propagate to caller, but code has no error handling difference from CLEAR

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring (line 2707-2714): "Note: Unlike CLEAR (which silently ignores file close errors), RESET allows errors during file close to propagate to the caller. This is intentional different behavior between the two statements."

Code (line 2716-2722): Both RESET and CLEAR (line 2698-2703) use identical file closing logic:
for file_num in list(self.runtime.files.keys()):
    self.runtime.files[file_num]['handle'].close()
    del self.runtime.files[file_num]

No try/except blocks differentiate error handling between the two statements.

---

#### code_vs_comment

**Description:** execute_list() docstring warns about sync issues but doesn't explain when/how they occur

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring (lines 2968-2975): "Implementation note: Outputs from line_text_map (original source text), not regenerated from AST. This preserves original formatting/spacing/case. The line_text_map is maintained by ProgramManager and should be kept in sync with the AST during program modifications (add_line, delete_line, RENUM, MERGE). If ProgramManager fails to maintain this sync, LIST output may show stale or incorrect line text."

This warning suggests a potential bug or design flaw but doesn't specify:
1. Under what conditions does sync fail?
2. Is this a known bug or theoretical concern?
3. Should users/developers be aware of specific scenarios?

---

#### code_vs_comment

**Description:** execute_step() marked as NOT IMPLEMENTED but has partial implementation details in comments

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring (lines 3082-3099): "STEP is intended to execute one or more statements, then pause.

CURRENT STATUS: This method outputs an informational message but does NOT actually perform stepping. It's a stub...

Note: The tick_pc() method has working step infrastructure (modes 'step_statement' and 'step_line') that is used by UI debuggers. This STEP command... would need to be connected to that infrastructure by setting a runtime flag and coordinating with the UI's tick loop, but this integration does not currently exist."

This extensive comment suggests the feature is partially implemented elsewhere but not connected. It's unclear if this is:
1. A TODO item
2. An intentional design decision
3. A deprecated feature

---

#### code_vs_comment

**Description:** evaluate_functioncall() comment about debugger_set=True tracking avoidance is inconsistent with actual usage

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment (lines 3226-3236): "Note: get_variable_for_debugger() and debugger_set=True are used to avoid triggering variable access tracking. This save/restore is internal function call machinery, not user-visible variable access. The tracking system (if enabled) should distinguish between:
- User code variable access (tracked for debugging/variables window)
- Internal implementation details (not tracked)
Maintainer warning: Ensure all internal variable operations use debugger_set=True"

Code (lines 3237-3242): Uses get_variable_for_debugger() for reading but set_variable() WITHOUT debugger_set=True for writing:
self.runtime.set_variable(param.name, param.type_suffix, args[i], token=call_token, limits=self.limits)

Only the restore operation uses debugger_set=True (line 3249). This inconsistency contradicts the comment's guidance.

---

#### Code vs Documentation inconsistency

**Description:** web_io.py implements get_screen_size() method which is not part of IOHandler interface and not documented in base.py

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/web_io.py`

**Details:**
base.py IOHandler interface does not define get_screen_size() method.

web_io.py implements:
    def get_screen_size(self):
        '''Get terminal size.
        Returns:
            Tuple of (rows, cols) - returns reasonable defaults for web
        Note: This is a web_io-specific method, not part of the IOHandler base interface.'''
        return (24, 80)

The method's own docstring acknowledges it's not part of the base interface, but base.py's class docstring mentions: "Note: Implementations may provide additional methods beyond this interface for backend-specific functionality (e.g., web_io.get_screen_size())." This is documented in base.py but as an example of backend-specific extensions.

---

#### Code vs Documentation inconsistency

**Description:** console.py input_char() Windows fallback behavior differs significantly from documented purpose but warnings are present

**Affected files:**
- `src/iohandler/console.py`

**Details:**
console.py input_char() for Windows without msvcrt:
                    # Fallback for Windows without msvcrt: use input() with severe limitations
                    # WARNING: This fallback calls input() which:
                    # - Waits for Enter key (defeats the purpose of single-char input)
                    # - Reads the entire line but returns only the first character
                    # This is a known limitation when msvcrt is unavailable.
                    import warnings
                    warnings.warn(
                        "msvcrt not available on Windows - input_char() falling back to input() "
                        "(waits for Enter, not single character)",
                        RuntimeWarning
                    )
                    line = input()
                    return line[:1] if line else ""

The fallback completely defeats the purpose of single-character input by requiring Enter key, but this is documented with warnings. The severity is medium because the limitation is acknowledged but the behavior is fundamentally broken for the use case.

---

#### code_vs_comment

**Description:** Comment claims SimpleKeywordCase validates policy strings and auto-corrects invalid values, but this behavior is not verified in the provided code

**Affected files:**
- `src/lexer.py`

**Details:**
In create_keyword_case_manager() docstring:
"Note: SimpleKeywordCase validates policy strings in its __init__ method. Invalid
policy values (not in: force_lower, force_upper, force_capitalize) are automatically
corrected to force_lower. See src/simple_keyword_case.py for implementation."

However, SimpleKeywordCase implementation is not provided to verify this claim. The comment makes specific assertions about validation and auto-correction behavior that cannot be confirmed.

---

#### code_vs_comment

**Description:** Comment claims RND and INKEY$ are the only functions that can be called without parentheses in MBASIC 5.21, but this contradicts general MBASIC behavior

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line 18-19 states:
"Exception: Only RND and INKEY$ can be called without parentheses in MBASIC 5.21
  (this is specific to these two functions, not a general MBASIC feature)"

However, the code implementation at lines 1247-1260 shows:
- RND without parentheses is allowed (lines 1247-1254)
- INKEY$ without parentheses is allowed (lines 1256-1263)

This appears consistent, but the comment's claim that this is "specific to these two functions" may be misleading. In actual MBASIC implementations, other parameterless functions like TIME$ and DATE$ could also be called without parentheses. The comment should clarify whether this is a deliberate limitation or if other functions should also support this syntax.

---

#### code_vs_comment

**Description:** Comment claims semicolon between statements is not valid in MBASIC, but code allows trailing semicolons

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines 426-429 states:
"Semicolons WITHIN PRINT/LPRINT are item separators (parsed there),
but semicolons BETWEEN statements are NOT valid in MBASIC.
MBASIC uses COLON (:) to separate statements, not semicolon (;)."

However, the code at lines 421-431 allows trailing semicolons:
"elif self.match(TokenType.SEMICOLON):
    # Allow trailing semicolon at end of line only (treat as no-op).
    ...
    self.advance()"

The code then checks if there's more content after the semicolon, but the comment's absolute statement that semicolons are "NOT valid" between statements conflicts with the code allowing them in specific cases (trailing at end of line).

---

#### code_vs_comment

**Description:** Comment describes LINE_INPUT token behavior inconsistently with actual implementation

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line ~1150 states: 'Note: The lexer tokenizes LINE keyword as LINE_INPUT token both when standalone (LINE INPUT statement) and when used as modifier (INPUT...LINE). The parser distinguishes these cases by context - LINE INPUT is a statement, INPUT...LINE uses LINE as a modifier within the INPUT statement.'

However, the code at line ~1147 checks: 'if self.match(TokenType.LINE_INPUT):' which suggests the lexer produces LINE_INPUT token in both contexts. The comment implies the lexer doesn't distinguish between 'LINE INPUT' (statement) and 'INPUT...LINE' (modifier), but the parser code treats them the same way by checking for LINE_INPUT token type in both cases.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation about separator behavior in LPRINT vs PRINT statements

**Affected files:**
- `src/parser.py`

**Details:**
LPRINT parse_lprint() docstring (line ~1050) states: 'Separator count vs expression count:
- If separators < expressions: no trailing separator, add newline
- If separators >= expressions: has trailing separator, no newline added'

However, the PRINT statement parser (parse_print, not shown in this excerpt) may have different separator handling logic. The LPRINT implementation explicitly adds '\n' when len(separators) < len(expressions), but this behavior should be consistent across PRINT and LPRINT or the difference should be documented.

---

#### code_vs_comment

**Description:** Comment about DIM dimension expressions contradicts typical BASIC behavior

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line ~1785 states: 'Dimension expressions: This implementation accepts any expression for array dimensions (e.g., DIM A(X*2, Y+1)), with dimensions evaluated at runtime. This behavior has been verified with MBASIC 5.21 (see tests/bas_tests/ for examples). Note: Some compiled BASICs (e.g., QuickBASIC) may require constants only.'

This comment claims the behavior 'has been verified with MBASIC 5.21' but doesn't provide specific test file references. The phrase 'see tests/bas_tests/ for examples' is vague. If this is a significant deviation from other BASIC implementations, the specific test files should be referenced to verify the claim.

---

#### code_vs_comment

**Description:** parse_width() docstring describes device parameter incorrectly

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states: "The parser accepts any expression; validation occurs at runtime."

However, the code only parses device when a COMMA is present:
```
device = None
if self.match(TokenType.COMMA):
    self.advance()
    device = self.parse_expression()
```

The docstring should clarify that device is optional and only parsed after a comma separator.

---

#### code_vs_comment

**Description:** parse_resume() docstring and implementation have inconsistent handling of RESUME 0

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states:
"Note: RESUME with no argument retries the statement that caused the error.
RESUME 0 also retries the error statement (same as RESUME with no argument)."

And in AST representation:
"- RESUME (no arg) → line_number=None
- RESUME 0 → line_number=0 (interpreter handles 0 same as None)"

This creates ambiguity: the docstring says they're the same, but the AST stores different values (None vs 0). The comment "interpreter handles 0 same as None" suggests they should be equivalent, but storing different values could lead to confusion or bugs if the interpreter doesn't handle this correctly.

---

#### code_vs_comment

**Description:** parse_deffn() has complex function name normalization logic that may not match the docstring description

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states: "Function name normalization: All function names are normalized to lowercase with 'fn' prefix (e.g., \"FNR\" becomes \"fnr\", \"FNA$\" becomes \"fna$\") for consistent lookup."

The implementation has two branches:
1. When FN is separate token: strips type suffix, adds 'fn' prefix
2. When FN is part of identifier: expects 'fn' prefix already present from lexer, strips type suffix

The docstring example "FNA$" becomes "fna$" suggests the $ suffix is kept, but the code explicitly strips type suffixes:
```
type_suffix = self.get_type_suffix(raw_name)
if type_suffix:
    raw_name = raw_name[:-1]
```

This is inconsistent - either the suffix should be kept (as docstring suggests) or removed (as code does).

---

#### code_vs_comment

**Description:** PC.statement field documentation says 'stmt index' but comment in examples says 'stmt_offset'

**Affected files:**
- `src/pc.py`

**Details:**
In PC class docstring:
    Fields:
        statement: Statement index on the line (0-based)

But in examples comment:
    The stmt index is 0-based: first statement has index 0, second has index 1, etc.

However, there's also a compatibility property:
    @property
    def stmt_offset(self):
        """Compatibility: old code used stmt_offset instead of statement"""
        return self.statement

This suggests 'statement' is the current name and 'stmt_offset' is legacy, but the docstring examples use inconsistent terminology.

---

#### code_vs_comment

**Description:** emit_keyword docstring says keyword must be lowercase but serialize_rem_statement passes uppercase

**Affected files:**
- `src/position_serializer.py`

**Details:**
emit_keyword docstring states:
        Args:
            keyword: The keyword to emit (must be normalized lowercase by caller, e.g., "print", "for")

And the note says:
        Note: This function requires lowercase input because it looks up the display case
        from the keyword case manager using the normalized form.

However, in serialize_rem_statement:
    def serialize_rem_statement(self, stmt: ast_nodes.RemarkStatementNode) -> str:
        """Serialize REM statement

        Note: stmt.comment_type is stored in uppercase by the parser ("APOSTROPHE", "REM", or "REMARK").
        We convert to lowercase before passing to emit_keyword() which requires lowercase input.
        """
        if stmt.comment_type == "APOSTROPHE":
            result = self.emit_token("'", stmt.column, "RemKeyword")
        else:
            # Apply keyword case to REM/REMARK (convert to lowercase for emit_keyword)
            result = self.emit_keyword(stmt.comment_type.lower(), stmt.column, "RemKeyword")

The code correctly converts to lowercase with .lower(), so the implementation is correct. But the docstring for emit_keyword says 'must be normalized lowercase by caller' which implies the caller should have already done this normalization before calling, yet serialize_rem_statement does the normalization inside the call. This is a minor documentation inconsistency about where the normalization responsibility lies.

---

#### code_vs_comment

**Description:** emit_keyword architecture note says parser stores keywords in uppercase but apply_keyword_case_policy expects lowercase

**Affected files:**
- `src/position_serializer.py`

**Details:**
In emit_keyword docstring:
        Architecture note: The parser stores keywords in uppercase (from TokenType enum names),
        so callers must convert to lowercase before calling this method. See serialize_rem_statement()
        for an example where stmt.comment_type.lower() is used for this conversion.

But in apply_keyword_case_policy docstring:
    Args:
        keyword: The keyword to transform (should be normalized lowercase for consistency,
                 but first_wins policy can handle mixed case by normalizing internally)

And in the first_wins policy implementation:
        elif policy == "first_wins":
            # Use the first occurrence seen for this keyword
            if keyword_tracker is not None:
                keyword_lower = keyword.lower()
                if keyword_lower in keyword_tracker:
                    return keyword_tracker[keyword_lower]

This shows that apply_keyword_case_policy does normalize to lowercase internally for first_wins, but the architecture note in emit_keyword says callers must convert to lowercase. This creates confusion about where the normalization responsibility lies.

---

#### Documentation inconsistency

**Description:** Inconsistent documentation about string length limits across different functions and presets

**Affected files:**
- `src/resource_limits.py`

**Details:**
The module docstring and create_web_limits()/create_local_limits() state that 255 bytes is for 'MBASIC 5.21 compatibility', but create_unlimited_limits() has a WARNING that says setting max_string_length to 1MB 'INTENTIONALLY BREAKS MBASIC 5.21 COMPATIBILITY' and that 'For MBASIC 5.21 spec compliance, use create_local_limits() or create_web_limits() which enforce the mandatory 255-byte string limit.'

However, the __init__ docstring for max_string_length parameter says: 'Maximum byte length for a string variable (UTF-8 encoded). MBASIC 5.21 limit is 255 bytes.' This suggests 255 is the MBASIC limit but doesn't explicitly state it's mandatory for compatibility.

The check_string_length() docstring says: 'String limits are measured in bytes (UTF-8 encoded), not character count. This matches MBASIC 5.21 behavior which limits string storage size.' This implies matching MBASIC behavior but doesn't say it's required.

The inconsistency is whether the 255-byte limit is:
1. A historical MBASIC limit that we optionally match for compatibility
2. A mandatory requirement for MBASIC 5.21 spec compliance

---

#### code_vs_comment

**Description:** Inconsistent documentation about line=-1 usage in last_write tracking

**Affected files:**
- `src/runtime.py`

**Details:**
The module header documents line=-1 usage:
"# Note: line -1 in last_write indicates non-program execution sources:
#       1. System/internal variables (ERR%, ERL%) via set_variable_raw() with FakeToken(line=-1)
#       2. Debugger/interactive prompt via set_variable() with debugger_set=True and token.line=-1
#       Both use line=-1, making them indistinguishable from each other in last_write alone."

However, set_variable_raw() docstring says:
"The line=-1 marker in last_write indicates system/internal variables.
However, debugger sets also use line=-1 (via debugger_set=True),
making them indistinguishable from system variables in last_write alone.
Both are distinguished from normal program execution (line >= 0)."

But the actual set_variable() code shows debugger_set path uses:
if debugger_set:
    self._variables[full_name]['last_write'] = {
        'line': -1,
        'position': None,
        'timestamp': time.perf_counter()
    }

This means debugger_set ALWAYS uses line=-1, but the comment 'debugger_set=True and token.line=-1' suggests token.line could be something else. The code doesn't use token.line when debugger_set=True.

---

#### code_vs_comment

**Description:** Misleading comment about DIM tracking as both read and write

**Affected files:**
- `src/runtime.py`

**Details:**
In dimension_array(), the comment states:
"# Note: DIM is tracked as both read and write to provide consistent debugger display.
# While DIM is technically allocation/initialization (write-only operation), setting
# last_read to the DIM location ensures that debuggers/inspectors can show 'Last accessed'
# information even for arrays that have never been explicitly read. Without this, an
# unaccessed array would show no last_read info, which could be confusing. The DIM location
# provides useful context about where the array was created."

However, the code shows:
self._arrays[full_name] = {
    'dims': dimensions,
    'data': [default_value] * total_size,
    'last_read_subscripts': None,
    'last_write_subscripts': None,
    'last_read': tracking_info,
    'last_write': tracking_info
}

The comment justifies setting last_read for 'consistent debugger display' and to avoid confusion, but this creates a semantic inconsistency: DIM never actually reads the array, so marking it as a read operation is misleading. The comment acknowledges this ('technically allocation/initialization (write-only operation)') but then justifies the inconsistency for UI convenience.

---

#### code_vs_comment

**Description:** Inconsistent documentation about _resolve_variable_name() usage context

**Affected files:**
- `src/runtime.py`

**Details:**
The _resolve_variable_name() docstring states:
"This is the standard method for determining the storage key for a variable,
applying BASIC type resolution rules (explicit suffix > DEF type > default).
For special cases like system variables (ERR%, ERL%), see set_variable_raw()."

This suggests set_variable_raw() is an alternative to _resolve_variable_name() for system variables. However, set_variable_raw() actually calls set_variable() internally, which would use _resolve_variable_name() through the normal path. The docstring implies set_variable_raw() bypasses _resolve_variable_name(), but it doesn't - it just provides a convenience wrapper that splits the full name and calls set_variable().

---

#### Code vs Comment conflict

**Description:** Comment claims default type suffix '!' should not occur in practice, but code implements it as a fallback

**Affected files:**
- `src/runtime.py`

**Details:**
In parse_name() helper function within get_variables():

Comment says: "Note: In normal operation, all names in _variables have resolved type suffixes from _resolve_variable_name() which applies DEF type rules. This fallback is defensive programming for robustness - it should not occur in practice, but protects against potential edge cases in legacy code or future changes."

Code implements: "return full_name, '!'" as the default fallback when no type suffix is present.

The comment suggests this is defensive programming that shouldn't execute, but the code actively implements it as a working fallback. If it truly shouldn't occur, the code should raise an error or log a warning instead of silently defaulting.

---

#### code_vs_comment

**Description:** SettingsManager._get_global_settings_path() and _get_project_settings_path() docstrings claim methods are not called internally, but this is misleading - they ARE called by FileSettingsBackend

**Affected files:**
- `src/settings.py`

**Details:**
src/settings.py lines 67-72 and 84-89:
Docstrings state: "Note: This method is not called internally by SettingsManager. Path resolution has been delegated to the backend (FileSettingsBackend or Redis backend)."

However, src/settings_backend.py lines 67-82 show FileSettingsBackend.__init__() calls:
  self.global_settings_path = self._get_global_settings_path()
  self.project_settings_path = self._get_project_settings_path()

These methods ARE called internally, just by the backend instead of SettingsManager directly. The comment is technically correct but misleading - it implies the methods are unused when they're actually critical to FileSettingsBackend.

---

#### code_vs_comment

**Description:** RedisSettingsBackend docstring claims 'No disk writes in this mode' but __init__ loads default_settings from disk via FileSettingsBackend

**Affected files:**
- `src/settings_backend.py`

**Details:**
src/settings_backend.py lines 127-138:
Docstring states: "- No disk writes in this mode (Redis is the only storage)"

However, src/settings_backend.py lines 253-256 in create_settings_backend() show:
  # Load default settings from disk
  file_backend = FileSettingsBackend(project_dir)
  default_settings = file_backend.load_global()

Redis mode DOES read from disk (to get defaults), it just doesn't write to disk. The docstring should say 'No disk writes' not 'No disk writes in this mode' which implies no disk I/O at all.

---

#### code_vs_comment

**Description:** Module docstring claims both systems SHOULD read from same settings but implementation shows only KeywordCaseManager reads settings directly

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
src/simple_keyword_case.py lines 23-28:
"Note: Both systems SHOULD read from the same settings.get('keywords.case_style') setting for consistency. SimpleKeywordCase receives policy via __init__ parameter (caller should pass settings value), while KeywordCaseManager reads settings directly. Callers are responsible for passing consistent policy values from settings to ensure matching behavior across phases."

This describes the intended design but doesn't match actual implementation responsibility. SimpleKeywordCase.__init__() (lines 33-42) accepts policy parameter but has no way to verify it matches settings. The comment places burden on callers but provides no enforcement mechanism. This is a design documentation issue - the comment describes what SHOULD happen but doesn't acknowledge the lack of enforcement.

---

#### code_vs_comment

**Description:** Token dataclass docstring describes convention for original_case vs original_case_keyword but implementation doesn't enforce this convention

**Affected files:**
- `src/tokens.py`

**Details:**
src/tokens.py lines 186-202:
Docstring states: "Note: By convention, these fields are used for different token types:
- original_case: For IDENTIFIER tokens (user variables) - preserves what user typed
- original_case_keyword: For keyword tokens - stores policy-determined display case

The dataclass does not enforce this convention (both fields can technically be set on the same token) to allow implementation flexibility. However, the lexer/parser follow this convention and only populate the appropriate field for each token type."

This describes a convention that relies on external code following rules, but the Token class itself provides no validation or enforcement. This is a documentation of implementation weakness rather than a true inconsistency, but it's worth noting that the comment acknowledges the lack of enforcement while claiming 'lexer/parser follow this convention' without verification mechanism.

---

#### code_vs_comment

**Description:** SettingsManager.get() docstring describes file-level precedence but then contradicts itself by saying file settings are 'not populated in normal usage'

**Affected files:**
- `src/settings.py`

**Details:**
src/settings.py lines 183-193:
Docstring states: "Precedence order: file > project > global > definition default > provided default

Note: File-level settings (first in precedence) are not populated in normal usage, but can be set programmatically via set(key, value, scope=SettingScope.FILE). The file_settings dict is checked first, but no persistence layer exists (not saved/loaded) and no UI/command manages per-file settings. In practice, typical precedence order is: project > global > definition default > provided default."

This is confusing documentation. It lists file settings as first in precedence, then immediately says they're 'not populated in normal usage' and gives a different 'typical precedence order'. Either document the actual precedence (including file) or document the typical precedence (excluding file). Mixing both creates confusion.

---

#### Documentation inconsistency

**Description:** auto_save.py module is documented but not referenced in any UI backend implementation

**Affected files:**
- `src/ui/auto_save.py`
- `src/ui/curses_settings_widget.py`

**Details:**
auto_save.py provides AutoSaveManager class with comprehensive auto-save functionality including:
- Emacs-style #filename# naming
- Centralized temp directory (~/.mbasic/autosave/)
- Recovery prompts via format_recovery_prompt()
- Auto-save cleanup

However, this module is not imported or used in any of the UI backend files (cli.py, base.py, curses_settings_widget.py). The settings widget shows editor settings but no auto-save related settings are defined in the visible code.

---

#### Code vs Documentation inconsistency

**Description:** STEP command documentation claims statement-level stepping but implementation may not support it

**Affected files:**
- `src/ui/cli_debug.py`
- `src/ui/cli_keybindings.json`

**Details:**
cli_keybindings.json states:
"description": "Execute next statement or n statements (STEP | STEP n) - attempts statement-level stepping"

cli_debug.py cmd_step() docstring states:
"Executes a single statement (not a full line). If a line contains multiple statements separated by colons, each statement is executed separately."

However, the _execute_single_step() method includes this note:
"Note: The actual statement-level granularity depends on the interpreter's implementation of tick()/execute_next(). These methods are expected to advance the program counter by one statement, handling colon-separated statements separately. If the interpreter executes full lines instead, this method will behave as line-level stepping rather than statement-level."

This suggests the feature may not actually work as documented if the interpreter doesn't support statement-level execution.

---

#### Code vs Documentation inconsistency

**Description:** BREAK command can set breakpoints on non-existent lines according to docstring but code prevents it

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
cmd_break() docstring states:
"Breakpoints can be set before or during execution, but only on existing program lines. If you try to set a breakpoint on a non-existent line, an error message will be displayed."

The implementation correctly enforces this:
```python
if line_num in self.interactive.program.lines:
    self.breakpoints.add(line_num)
    self.interactive.io_handler.output(f"Breakpoint set at line {line_num}")
else:
    self.interactive.io_handler.output(f"Line {line_num} does not exist")
```

This is actually consistent - the docstring correctly describes the behavior. However, the phrasing "can be set before or during execution" might mislead users into thinking they can set breakpoints on lines that don't exist yet.

---

#### Documentation inconsistency

**Description:** Inconsistent keybinding for Continue command between CLI and Curses

**Affected files:**
- `src/ui/cli_keybindings.json`
- `src/ui/curses_keybindings.json`

**Details:**
CLI uses CONT command:
```json
"continue": {
  "keys": ["CONT"],
  "primary": "CONT",
  "description": "Continue execution"
}
```

Curses uses Ctrl+C:
```json
"continue": {
  "keys": ["Ctrl+C"],
  "primary": "Ctrl+C",
  "description": "Continue execution"
}
```

Note that in CLI, Ctrl+C is used for Stop:
```json
"stop": {
  "keys": ["Ctrl+C"],
  "primary": "Ctrl+C",
  "description": "Stop program execution"
}
```

While in Curses, Ctrl+X is used for Stop:
```json
"stop": {
  "keys": ["Ctrl+X"],
  "primary": "Ctrl+X",
  "description": "Stop program execution"
}
```

This creates a confusing situation where Ctrl+C has opposite meanings in the two UIs.

---

#### code_vs_comment

**Description:** Comment claims auto-numbering stops at 99999 but code allows manual entry of higher numbers, yet _parse_line_number() has no such restriction documented

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line ~1050 comment: 'Note: Auto-numbering stops at 99999 for display consistency, but manual
entry of higher line numbers is not prevented by _parse_line_number().
This is intentional - auto-numbering uses conservative limits while
manual entry allows flexibility.'

However, _parse_line_number() method (lines ~240-310) has no documentation about any line number limits, and the implementation parses any sequence of digits without validation. The comment suggests intentional design but the method itself has no comments explaining this behavior or any limits.

---

#### code_vs_comment

**Description:** Comment about line 0 handling is unclear and inconsistent with validation elsewhere

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line ~1690 in _update_syntax_errors(): 'Note: line_number > 0 check silently skips line 0 if present (not a valid
BASIC line number). This avoids setting status for malformed lines.
Consistent with _check_line_syntax which treats all empty lines as valid'

However:
1. _check_line_syntax() (lines ~1540-1600) has no special handling for line 0 - it only checks syntax of code_text parameter which has no line number
2. The comment claims consistency with _check_line_syntax treating empty lines as valid, but that's unrelated to line 0 validation
3. No other code in the file validates or rejects line number 0
4. BASIC traditionally allows line 0 as a valid line number

---

#### code_vs_comment

**Description:** Comment claims editor_lines stores execution state and is synced from editor, but code shows editor_lines is never actually populated or synced from editor.lines

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~217 says:
# Note: self.editor_lines stores execution state (lines loaded from file for RUN)
# self.editor.lines (in ProgramEditorWidget) stores the actual editing state
# These serve different purposes and are synchronized as needed

However, searching the code:
1. editor_lines is initialized as empty dict: self.editor_lines = {}
2. It's only read in _debug_step_line (line ~1027): line_code = self.editor_lines.get(state.current_line, "")
3. It's never written to or synced from self.editor.lines
4. The _save_editor_to_program method syncs editor.lines to program manager, not to editor_lines
5. The _refresh_editor method syncs program manager to editor.lines, not to editor_lines

---

#### code_vs_comment

**Description:** Comment claims ImmediateExecutor is recreated in start() to ensure clean state, but Interpreter (which holds state) is NOT recreated

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~273 says:
# ImmediateExecutor Lifecycle:
# Created here with an OutputCapturingIOHandler, then recreated in start() with
# a fresh OutputCapturingIOHandler. Both instances are fully functional - the
# recreation in start() ensures a clean state for each UI session.
# Note: The interpreter (self.interpreter) is created once here and reused.
# Only the executor and its IO handler are recreated in start().

This is contradictory because:
1. The comment says recreation ensures "clean state for each UI session"
2. But the Interpreter (which holds the actual execution state) is NOT recreated
3. Only the ImmediateExecutor wrapper and IO handler are recreated
4. If the goal is clean state per session, recreating just the executor doesn't achieve that since the interpreter retains state

---

#### code_vs_comment

**Description:** Comment in _continue_smart_insert says it cannot continue insert operation after renumber, but this limitation is not explained in the user-facing prompt

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1249:
# Note: Cannot continue the insert operation here because the context was lost
# when the dialog callback was invoked (lines, line_index, insert_num variables
# are no longer available). User will need to retry the insert operation manually.

But the prompt shown to the user (line ~1223) says:
f"No room between lines {prev_line_num} and {current_line_num}. Renumber? (y/n): "

The prompt doesn't inform the user that they'll need to retry the insert operation after renumbering. This could confuse users who expect the insert to complete automatically after renumbering.

---

#### code_vs_comment

**Description:** Comment claims breakpoints are stored in editor as authoritative source and re-applied after reset, but code shows breakpoints are stored in both editor.breakpoints AND interpreter, with potential sync issues

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1089 states:
"Note: reset_for_run() clears variables and resets PC. Breakpoints are STORED in
the editor (self.editor.breakpoints) as the authoritative source, not in runtime.
This allows them to persist across runs. After reset_for_run(), we re-apply them
to the interpreter below via set_breakpoint() calls so execution can check them."

However, the code shows:
1. _toggle_breakpoint_current_line() modifies self.editor.breakpoints
2. _clear_all_breakpoints() clears self.editor.breakpoints AND calls self.interpreter.clear_breakpoints()
3. _setup_program() re-applies breakpoints from editor to interpreter

This suggests a dual-storage model where both editor and interpreter maintain breakpoint state, contradicting the comment's claim that editor is the sole authoritative source.

---

#### code_vs_comment

**Description:** Comment about main widget storage strategy is inconsistent across methods

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple comments describe widget storage strategies:

1. _show_help() comment (line ~826): "Main widget retrieval: Use self.base_widget (stored at UI creation time in __init__) rather than self.loop.widget (which reflects the current widget and might be a menu or other overlay). This approach works for _show_help, _show_keymap, and _show_settings because these methods close any existing overlays first (via on_close callbacks) before creating new ones, ensuring self.base_widget is the correct base for the new overlay."

2. _activate_menu() comment (line ~883): "Main widget storage: Unlike _show_help/_show_keymap/_show_settings which close existing overlays first (and thus can use self.base_widget directly), this method extracts base_widget from self.loop.widget to unwrap any existing overlay. This preserves existing overlays (like help or settings) while adding the menu dropdown on top of them, allowing menu navigation even when other overlays are present."

However, examining _show_keymap() and _show_settings() code shows they do NOT close existing overlays first - they check if their own overlay is open (toggle behavior) but don't close other overlays. The comment in _show_help() claiming they "close any existing overlays first" is incorrect.

---

#### internal_inconsistency

**Description:** Inconsistent error handling and status bar updates across similar error paths

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Error handling shows inconsistent patterns:

1. Parse errors (line ~1073): Display in output buffer with box, no status bar update, no immediate status update
2. Undefined line errors (line ~1084): Display in output buffer, no status bar update, no immediate status update
3. Runtime errors (line ~1165): Display in output buffer with box, update immediate status
4. Unexpected errors (line ~1203): Display in output buffer with box, set status bar to "Internal error - See output"

Some error paths update status bar, some don't. Some update immediate status, some don't. This inconsistency makes the UI behavior unpredictable.

---

#### code_vs_comment

**Description:** Comment in _get_input_for_interpreter says 'PC already contains the position with stop_reason for CONT' but the actual behavior when input is cancelled is to set self.running = False without any PC manipulation

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1045: 'Note: This stops the UI tick. PC already contains the position with stop_reason for CONT.'

Actual code at line ~1050:
if result is None:
    # Stop execution - PC already contains the position for CONT to resume from
    self.running = False
    self._append_to_output("Input cancelled - Program stopped")
    self._update_immediate_status()
    return

The comment suggests PC has stop_reason set, but the code only sets self.running = False. No PC manipulation occurs.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate says 'No state checking - just ask the interpreter' but there is state checking via has_work()

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1330: '# Check if interpreter has work to do (after RUN statement)
# No state checking - just ask the interpreter
has_work = self.interpreter.has_work() if self.interpreter else False'

The comment claims 'No state checking' but has_work() is itself a state check. The comment may be outdated from a refactoring.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate about not calling interpreter.start() contradicts the claim that 'immediate executor handles program start setup'

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1340: 'NOTE: Don't call interpreter.start() here. The immediate executor handles
program start setup (e.g., RUN command sets PC appropriately via
interpreter.start()). This function only ensures InterpreterState exists
for tick-based execution tracking. If we called interpreter.start() here,
it would reset PC to the beginning, overriding the PC set by RUN command.'

This comment says 'immediate executor handles program start setup' and 'RUN command sets PC appropriately via interpreter.start()', which seems contradictory - if the executor calls interpreter.start(), then calling it here would be redundant, not conflicting. The comment needs clarification about the actual flow.

---

#### code_vs_comment

**Description:** Comment in cmd_delete and cmd_renum says 'Updates self.program immediately (source of truth), then syncs to runtime' but the code passes runtime=None to helper functions

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment in cmd_delete at line ~1410: 'Note: Updates self.program immediately (source of truth), then syncs to runtime.'

Code at line ~1415:
deleted = delete_lines_from_program(self.program, args, runtime=None)
self._sync_program_to_runtime()  # Sync runtime after program changes

Similar pattern in cmd_renum at line ~1430. The comment suggests a two-step process, but passing runtime=None means the helper function doesn't update runtime at all - only the explicit _sync_program_to_runtime() call does. This is correct behavior but the comment could be clearer.

---

#### code_vs_comment

**Description:** Comment about 'base_widget' in _show_recent_files doesn't match the actual variable name used

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1265: '# Use base_widget as base (not current loop.widget which might be a menu)'

Code at line ~1266:
main_widget = self.base_widget

But then the code uses 'main_widget' throughout, not 'base_widget'. The comment and variable naming are inconsistent.

---

#### code_vs_comment_conflict

**Description:** Comment claims tier labels use 'language' and 'mbasic' from tier_labels dict, but code shows tier_labels only has these two entries and uses startswith('ui/') check separately

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at line ~143 states:
"Note: Tier labels are determined from tier_labels dict ('language', 'mbasic'), startswith('ui/') check for UI tiers ('ui/curses', 'ui/tk'), or '📙 Other' fallback."

Code at lines ~145-148 shows:
tier_labels = {
    'language': '📕 Language',
    'mbasic': '📗 MBASIC',
}

Then at lines ~162-167:
tier_name = file_info.get('tier', '')
if tier_name.startswith('ui/'):
    tier_label = '📘 UI'
else:
    tier_label = tier_labels.get(tier_name, '📙 Other')

The comment accurately describes the logic, but the phrasing could be clearer that tier_labels is a local dict defined in the method, not a class attribute or external configuration.

---

#### documentation_inconsistency

**Description:** Both files have nearly identical comments about loading keybindings but for different purposes, creating potential confusion about their relationship

**Affected files:**
- `src/ui/help_macros.py`
- `src/ui/keybinding_loader.py`

**Details:**
help_macros.py line ~28 comment:
"Note: This loads the same keybinding JSON files as keybinding_loader.py, but for a different purpose: macro expansion in help content (e.g., {{kbd:run}} -> "^R") rather than runtime event handling. This is separate from help_widget.py which uses hardcoded keys for navigation within the help system itself."

keybinding_loader.py line ~28 comment:
"Note: This loads keybindings for runtime event handling (binding keys to actions). help_macros.py loads the same JSON files but for macro expansion in help content (e.g., {{kbd:run}} -> "^R"). Both read the same data but use it differently: KeybindingLoader for runtime key event handling, HelpMacros for documentation display."

These comments reference each other but could lead to circular confusion. The relationship is clear but the cross-referencing style is unusual.

---

#### code_vs_comment_conflict

**Description:** Comment claims help_widget.py uses hardcoded keys but doesn't mention that HelpMacros loads keybindings for macro expansion, creating confusion about what 'hardcoded' means

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Multiple comments in help_widget.py emphasize that navigation keys are hardcoded:

Line ~73: "Note: Help navigation keys are HARDCODED (not loaded from keybindings JSON)"

Line ~76: "Note: HelpMacros (instantiated below) DOES load keybindings from JSON, but only for macro expansion in help content ({{kbd:action}} substitution). The help widget's own navigation doesn't consult those loaded keybindings - it uses hardcoded keys."

Line ~79: "MAINTENANCE: If help navigation keys change, update:
1. All footer text assignments (search for 'self.footer' in this file - multiple locations)"

However, this creates confusion because:
1. HelpMacros IS instantiated and DOES load keybindings
2. The term 'hardcoded' is used to mean 'not dynamically loaded for navigation' but the keybindings ARE loaded (just for different purpose)
3. The maintenance note suggests manual updates to footer text, but doesn't clarify the relationship with the loaded keybindings

The comments are technically accurate but the repeated emphasis on 'hardcoded' vs 'loaded' creates unnecessary confusion about the architecture.

---

#### code_vs_comment_conflict

**Description:** Comment references keybindings module functions but code uses hardcoded keybinding references

**Affected files:**
- `src/ui/interactive_menu.py`

**Details:**
Comment at line ~23 states:
"# Use keybindings module to get actual shortcuts"

Code at lines ~24-44 shows menu definitions like:
(f'New            {key_to_display(kb.NEW_KEY)}', '_new_program'),
(f'Open...        {key_to_display(kb.OPEN_KEY)}', '_load_program'),

This imports from keybindings module (line ~4: from . import keybindings as kb) and uses constants like kb.NEW_KEY, kb.OPEN_KEY, etc.

However, this is inconsistent with the keybinding_loader.py approach which loads from JSON. The interactive_menu.py uses the old keybindings.py module with hardcoded constants, not the JSON-based keybinding_loader.py system.

This suggests there are two keybinding systems in use: the old keybindings.py with constants, and the new keybinding_loader.py with JSON configs.

---

#### Code vs Comment conflict

**Description:** Comment says QUIT_KEY has no dedicated keybinding and suggests using menu or Ctrl+C, but QUIT_ALT_KEY is defined and loaded from JSON config

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Lines 127-133:
# Quit - No dedicated keybinding in QUIT_KEY (most Ctrl keys intercepted by terminal or already assigned)
# Primary method: Use menu (Ctrl+U -> File -> Quit)
# Alternative method: Ctrl+C (interrupt signal) - handled by QUIT_ALT_KEY below
QUIT_KEY = None  # No standard keybinding (use menu or Ctrl+C instead)

# Alternative quit via interrupt signal (Ctrl+C)
# Note: While not a "standard keybinding", Ctrl+C provides a keyboard shortcut to quit.
# It's handled as a signal rather than a regular key event, hence the separate constant.
_quit_alt_from_json = _get_key('editor', 'quit')
QUIT_ALT_KEY = _ctrl_key_to_urwid(_quit_alt_from_json) if _quit_alt_from_json else 'ctrl c'

The comment implies Ctrl+C is a signal handler, but the code loads it from JSON as a regular keybinding.

---

#### Documentation inconsistency

**Description:** KEYBINDINGS_BY_CATEGORY comment lists keys not included in help, but doesn't mention QUIT_KEY (which is None) or explain why QUIT_ALT_KEY is shown instead

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Lines 217-226:
# All keybindings organized by category for help display
# Note: This dictionary contains keybindings shown in the help system.
# Some defined constants are not included here:
# - CLEAR_BREAKPOINTS_KEY (Shift+Ctrl+B) - Available in menu under Edit > Clear All Breakpoints
# - STOP_KEY (Ctrl+X) - Shown in debugger context in the Debugger category
# - MAXIMIZE_OUTPUT_KEY (Shift+Ctrl+M) - Menu-only feature, not documented as keyboard shortcut
# - STACK_KEY (empty string) - No keyboard shortcut assigned, menu-only
# - Dialog-specific keys (DIALOG_YES_KEY, DIALOG_NO_KEY, SETTINGS_APPLY_KEY, SETTINGS_RESET_KEY) - Shown in dialog prompts
# - Context-specific keys (VARS_SORT_MODE_KEY, VARS_SORT_DIR_KEY, etc.) - Shown in Variables Window category

Comment doesn't explain that QUIT_KEY is None and QUIT_ALT_KEY is used instead. Also, STOP_KEY comment says it's shown in debugger context, but looking at line 245, STOP_KEY IS included in the Debugger category.

---

#### Code vs Documentation inconsistency

**Description:** In-page search keybindings documented in code comments but missing from tk_keybindings.json

**Affected files:**
- `src/ui/tk_help_browser.py`
- `src/ui/tk_keybindings.json`

**Details:**
tk_help_browser.py lines 113-116 document Return and Escape keys for in-page search:
# Return key in search box navigates to next match (local widget binding)
# Note: This binding is specific to the in-page search entry widget and is not
# documented in tk_keybindings.json, which only documents global application
# keybindings. Local widget bindings are documented in code comments only.

However, tk_keybindings.json only documents Ctrl+F for inpage_search, missing Return (next match) and Escape (close search bar) which are implemented in lines 113-115.

---

#### Code duplication warning

**Description:** Path normalization logic duplicated between _follow_link() and _open_link_in_new_window() with warning comments

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
_follow_link() lines 244-248:
Note: Path normalization logic is duplicated in _open_link_in_new_window().
Both methods use similar approach: resolve relative paths, normalize to help_root,
handle path separators. If modification needed, update both methods consistently.

_open_link_in_new_window() lines 625-628:
Note: Path normalization logic is duplicated from _follow_link().
Both methods resolve paths relative to help_root with similar logic.
If modification needed, update both methods consistently.

Both methods implement similar path resolution logic (lines 250-276 and 630-651) with explicit warnings about keeping them synchronized.

---

#### code_vs_comment

**Description:** Comment states immediate_history and immediate_status are 'always None' but code explicitly sets them to None with defensive programming justification

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~147 comment: 'Note: immediate_history and immediate_status are always None in Tk UI'
Line ~348-351 code:
# Set immediate_history and immediate_status to None
# These attributes are not currently used but are set to None for defensive programming
# in case future code tries to access them (will get None instead of AttributeError)
self.immediate_history = None
self.immediate_status = None

---

#### code_vs_comment

**Description:** Docstring states 3-pane layout weights are '3:2:1 = total 6 units' but actual implementation uses different weights

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring lines ~66-70:
'- 3-pane vertical layout (weights: 3:2:1 = total 6 units):
  * Editor with line numbers (top, ~50% = 3/6 - weight=3)
  * Output pane (middle, ~33% = 2/6 - weight=2)
  * Immediate mode input line (bottom, ~17% = 1/6 - weight=1)'

Actual code lines ~235-245:
paned.add(editor_frame, weight=3)
paned.add(output_frame, weight=2)
paned.add(immediate_frame, weight=1)

However, immediate_frame contains only a 40px fixed-height input row (line ~308: input_frame = ttk.Frame(immediate_frame, height=40)), not a proportional 1/6 weight pane.

---

#### documentation_inconsistency

**Description:** Docstring describes INPUT row as 'shown/hidden dynamically for INPUT statements' but implementation details show it uses pack()/pack_forget() which is not mentioned

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring line ~69:
'- Contains INPUT row (shown/hidden dynamically for INPUT statements)'

Code lines ~283-285:
# INPUT row (hidden by default, shown when INPUT statement needs input)
# Visibility controlled via pack() when showing, pack_forget() when hiding
self.input_row = ttk.Frame(output_frame, height=40)
# Don't pack yet - will be packed when needed

The docstring doesn't explain the pack/pack_forget mechanism used for showing/hiding.

---

#### code_vs_comment

**Description:** Comment describes ARROW_CLICK_WIDTH as 'typical arrow icon width for standard Tkinter theme' but this is platform-dependent and may not be accurate

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~1074: ARROW_CLICK_WIDTH = 20  # Width of clickable arrow area in pixels (typical arrow icon width for standard Tkinter theme)

The hardcoded 20 pixels may not match actual arrow width on all platforms (Windows, macOS, Linux with different themes). The comment implies this is a universal standard when it's actually an approximation.

---

#### code_vs_comment

**Description:** Comment claims formatting may occur elsewhere, but code explicitly avoids formatting to preserve MBASIC compatibility

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _refresh_editor method around line 1150:
Comment says: "(Note: 'formatting may occur elsewhere' refers to the Variables and Stack windows, which DO format data for display - not the editor/program text itself)"

This comment is confusing because:
1. It appears in parentheses as a clarification
2. The phrase 'formatting may occur elsewhere' doesn't appear in the preceding comment
3. It seems to be defending against a criticism that wasn't made
4. The actual comment above it already clearly states: 'No formatting is applied to preserve compatibility with real MBASIC'

The comment appears to be a leftover from a code review or refactoring discussion.

---

#### code_vs_comment

**Description:** Comment about clearing yellow highlight conflicts with actual behavior

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_mouse_click method around line 1290:
Comment says: "Clear yellow statement highlight when clicking (allows text selection to be visible). The highlight is restored when execution resumes or when stepping to the next statement."

However, the code only clears the highlight when paused_at_breakpoint is True:
if self.paused_at_breakpoint:
    self._clear_statement_highlight()

The comment implies the highlight is always cleared on click, but the code only clears it when paused at a breakpoint. The comment should clarify this conditional behavior.

---

#### code_vs_comment

**Description:** Docstring for _edit_array_element has incorrect parameter description

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _edit_array_element method around line 950:
Docstring says:
"Args:
    variable_name: Array name with type suffix (e.g., 'A%')
    type_suffix: Type character ($, %, !, #, or empty)
    value_display: Display string like 'Array(10x10) [5,3]=42'"

But the code extracts type_suffix from variable_name:
base_name = variable_name[:-1] if variable_name[-1] in '$%!#' else variable_name
suffix = variable_name[-1] if variable_name[-1] in '$%!#' else None

This means type_suffix parameter is redundant - it's already in variable_name. The docstring should clarify that type_suffix is passed separately for convenience but is also embedded in variable_name.

---

#### code_vs_comment

**Description:** Comment claims blank lines are removed but code only removes them if they're not the last line

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_paste method around line 1050:
Comment says: '# Blank line' followed by code:
if not stripped:
    # Blank line
    if line != lines[-1]:
        removed_blank = True
    continue

This means the last blank line is NOT removed, but the comment and status message don't clarify this exception.

---

#### code_vs_comment

**Description:** Comment claims cursor moves to end of line but code shows it returns 'break' without moving cursor

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_enter_key method around line 1000:
Comment says: '# Don't refresh - let user fix the error\n# Just move cursor to end of current line'
But the code is:
if not success:
    # Don't refresh - let user fix the error
    # Just move cursor to end of current line
    self.editor_text.text.mark_set(tk.INSERT, f'{current_line_index}.end')
    return 'break'

The cursor IS moved to end of line, so this is actually consistent. However, the flow is confusing because earlier in the function there's validation that might prevent reaching this point.

---

#### code_vs_comment

**Description:** Comment describes default behavior that is actually prevented by returning 'break'

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_paste method around line 1140:
Comment says: '# Check if there's a text selection - if yes, let default behavior handle it\n# (default behavior: delete selection, insert newline)'
But the code does:
if self.editor_text.text.tag_ranges(tk.SEL):
    # There's a selection - delete it and insert newline
    self.editor_text.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
    self.editor_text.text.insert(tk.INSERT, '\n')
    return 'break'

Returning 'break' prevents default behavior. The code manually implements what would be default behavior, then blocks the default. The comment is misleading about 'letting default behavior handle it'.

---

#### code_vs_comment

**Description:** Comment claims line won't be removed but doesn't explain why

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _smart_insert_line method around line 1550:
Comment says: 'Note: This line won't be removed by _remove_blank_lines() because it contains\nthe line number (not completely blank)'

But _remove_blank_lines() filters based on 'if not line.strip()' which would be False for a line containing just a number and space. The comment is correct but doesn't explain the actual mechanism - it's not removed because strip() returns a non-empty string.

---

#### code_vs_comment

**Description:** Comment claims error line is marked but the code has exception handling that might silently fail

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_tick method around line 1710:
Comment says: '# Mark the error line with red ? indicator'
Followed by:
try:
    error_line_int = int(error_line)
    self.editor_text.set_error(error_line_int, True, str(e))
except (ValueError, AttributeError, TypeError) as marker_error:
    pass

The broad exception handling with 'pass' means marking might silently fail. The comment doesn't acknowledge this possibility, making it seem like marking always succeeds.

---

#### code_vs_comment

**Description:** Comment claims variables are cleared but doesn't mention breakpoints are preserved

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In cmd_run method around line 1800:
Comment says: '# Reset runtime with current program - RUN clears variables and starts execution\n# Preserves breakpoints (unlike CLEAR which removes program entirely)'

The second line about breakpoints is good, but it's in a comment about reset_for_run. The actual breakpoint preservation happens later in the code ('if self.breakpoints: self.interpreter.state.breakpoints = self.breakpoints.copy()'). The comment placement suggests reset_for_run preserves breakpoints, but actually the method calling it does.

---

#### code_vs_comment

**Description:** Comment claims _add_immediate_output adds to immediate output pane, but code forwards to main output pane

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Method docstring says:
"Add text to main output pane.

Note: This method name is historical/misleading - it actually adds to the
main output pane, not a separate immediate output pane. It simply forwards
to _add_output(). In the Tk UI, immediate mode output goes to the main
output pane. self.immediate_history is always None (see __init__)."

The comment correctly identifies the misleading name and explains the actual behavior. However, the method name itself (_add_immediate_output) creates confusion for future maintainers.

---

#### code_vs_comment

**Description:** Comment about GUI design choice contradicts typical BASIC behavior without explaining why

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_immediate method:
"# Execute without echoing (GUI design choice that deviates from typical BASIC
# behavior: command is visible in entry field, and 'Ok' prompt is unnecessary
# in GUI context - only results are shown. Traditional BASIC echoes to output.)"

This comment explains a design deviation but the rationale seems weak - the command being visible in the entry field doesn't prevent echoing to output for history purposes. This may confuse users expecting traditional BASIC behavior.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation about when has_work() is called

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment in _execute_immediate states:
"# Use has_work() to check if the interpreter is ready to execute (e.g., after RUN command).
# This is the only location in tk_ui.py that calls has_work()."

This creates a strong coupling assumption that may not be verified. If has_work() needs to be called elsewhere in the future, this comment creates confusion about whether it's safe to do so.

---

#### code_vs_comment

**Description:** TkIOHandler docstring describes input strategy but implementation details don't fully match explanation

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring states:
"Input strategy rationale:
- INPUT statement: Uses inline input field when backend available (allowing the user to
  see program output context while typing input), otherwise uses modal dialog as fallback.
  This is availability-based, not a UI preference.
- LINE INPUT statement: Always uses modal dialog for consistent UX. This is intentional
  because LINE INPUT reads entire lines including whitespace, and the modal dialog provides
  a clearer visual indication that the full line (including spaces) will be captured.
  The inline field is optimized for short INPUT responses, while LINE INPUT often requires
  more careful multi-word input."

However, the input() method implementation shows the inline input field is used when backend is available, but there's no clear indication in the code that the inline field is 'optimized for short INPUT responses' - it could handle long inputs just as well. The rationale for LINE INPUT always using modal dialog seems more about design preference than technical limitation.

---

#### code_vs_comment

**Description:** The _parse_line_number() docstring comment states 'Match line number followed by whitespace OR end of string (both valid)' and provides examples, but then contradicts itself by saying 'MBASIC 5.21 requires whitespace OR end-of-line between line number and statement' while also saying 'A standalone line number like "10" is valid (represents a numbered line with no code)'. The regex pattern r'^(\d+)(?:\s|$)' correctly implements whitespace-or-end, but the comment conflates 'end of string' with 'end-of-line' and 'no statement' inconsistently.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment says: 'Match line number followed by whitespace OR end of string (both valid).'
Then: 'Note: MBASIC 5.21 requires whitespace OR end-of-line between line number and statement.'
Then: 'A standalone line number like "10" is valid (represents a numbered line with no code).'

The regex r'^(\d+)(?:\s|$)' matches digits followed by whitespace OR end-of-string.

The terminology mixing 'end of string', 'end-of-line', and 'no statement' is confusing. In the context of line_text.strip(), end-of-string IS the end of the line content.

---

#### code_vs_comment

**Description:** The _on_status_click() docstring states it 'does NOT toggle breakpoints - that's handled by the UI backend's breakpoint toggle command (e.g., TkBackend._toggle_breakpoint(), accessed via ^B in Tk UI or menu)', but this references implementation details (TkBackend class, ^B keybinding) that are not in this file and may not exist or may have different names.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Docstring says: 'Note: This displays information messages only. It does NOT toggle breakpoints - that's handled by the UI backend's breakpoint toggle command (e.g., TkBackend._toggle_breakpoint(), accessed via ^B in Tk UI or menu).'

This file (tk_widgets.py) does not contain TkBackend class or any keybinding definitions. The comment references external implementation details that cannot be verified from this file alone.

---

#### code_vs_comment

**Description:** The _redraw() docstring states 'Note: BASIC line numbers are part of the text content (not drawn separately in the canvas). See _parse_line_number() for the regex-based extraction logic that validates line number format (requires whitespace or end-of-string after the number).' However, _parse_line_number() is called from multiple places and the validation logic is not just for _redraw(). The note placement suggests it's specific to _redraw() when it's actually a general class behavior.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Docstring in _redraw(): 'Note: BASIC line numbers are part of the text content (not drawn separately in the canvas). See _parse_line_number() for the regex-based extraction logic that validates line number format (requires whitespace or end-of-string after the number).'

_parse_line_number() is called from:
- _redraw()
- get_current_line_number()
- _on_status_click()

This note would be better placed in the class docstring or _parse_line_number() docstring since it describes general class behavior, not _redraw()-specific behavior.

---

#### code_vs_comment

**Description:** Comment in serialize_statement() claims 'REMARK is converted to REM during parsing, not here' but the code actually handles REMARK as a comment_type value

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Line ~730: Comment says '# Preserve comments using original syntax (REM or \')\n# Note: REMARK is converted to REM during parsing, not here'

But the code at line ~732 checks stmt.comment_type which could be 'APOSTROPHE', 'REM', 'REMARK', or default, suggesting REMARK is NOT converted during parsing and IS handled here.

The else clause at line ~734 says '# REM, REMARK, or default' confirming REMARK is a valid comment_type value that reaches this serialization code.

---

#### code_vs_comment

**Description:** Comment in serialize_statement() about unhandled statement types describes prevention strategy but doesn't match typical error handling patterns

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Lines ~810-817: Comment says:
'# For unhandled statement types, raise an error to prevent silent data corruption\n# Prevention strategy: Explicitly fail (with ValueError) rather than silently omitting\n# statements during RENUM, which would corrupt the program.\n# Note: There is no compile-time verification that all AST statement types are handled.\n# If new statement types are added to the parser, they won\'t be caught until runtime\n# when RENUM is attempted on code containing them. This is acceptable because the error\n# is explicit and prevents corruption (better than silently dropping statements).'

While the code does raise ValueError, the extensive justification in the comment suggests this was a debated design decision. The comment reads more like documentation or a design rationale than a typical inline comment explaining what the code does.

---

#### Code vs Comment conflict

**Description:** Comment in cmd_run() claims 'Runtime accesses program.line_asts directly, no need for program_ast variable' but the code actually passes program.line_asts to Runtime constructor

**Affected files:**
- `src/ui/visual.py`

**Details:**
Comment says: '(Runtime accesses program.line_asts directly, no need for program_ast variable)'
Code shows: 'self.runtime = Runtime(self.program.line_asts, self.program.lines)'

The comment suggests Runtime accesses line_asts directly (implying it might have a reference to the program object), but the code explicitly passes line_asts as a constructor argument, which is a different pattern.

---

#### Code vs Documentation inconsistency

**Description:** get_cursor_position() docstring claims it returns placeholder values but doesn't document this limitation in the main class docstring features list

**Affected files:**
- `src/ui/web/codemirror5_editor.py`

**Details:**
Method docstring says:
        """Get current cursor position.

        Note: This is a placeholder implementation that always returns line 0, column 0.
        Full implementation would require async JavaScript communication support.

        Returns:
            Dict with 'line' and 'column' keys (placeholder: always {'line': 0, 'column': 0})
        """

But the class docstring lists features without mentioning this limitation:
    """CodeMirror 5 based code editor component.

    This component uses CodeMirror 5 (legacy version) which doesn't require
    ES6 module loading, making it compatible with NiceGUI's module system.

    Features:
    - Find highlighting (yellow background)
    - Breakpoint markers (red line background)
    - Current statement highlighting (green background)
    - Line numbers
    - Text editing
    """

The features list doesn't mention cursor position retrieval at all, and the method is non-functional.

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

**Description:** Comment in FindReplaceDialog.show() says CodeMirror maintains scroll position, but no CodeMirror-specific code visible

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~565:
# Note: CodeMirror maintains scroll position automatically when dialog closes

This comment appears in the on_close() function, but there's no visible CodeMirror-specific code handling scroll position. The editor is self.backend.editor which is created as CodeMirror5Editor, but the automatic scroll position maintenance is not evident in the shown code.

---

#### code_vs_comment

**Description:** Comment claims output is NOT cleared on RUN, but Step commands DO clear output. However, examining the step command implementations (_menu_step_line and _menu_step_stmt), there is no code that clears output.

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~1845 states:
"# Don't clear output - continuous scrolling like ASR33 teletype
# Design choice: Unlike some modern BASIC interpreters that clear output on RUN,
# we preserve historical ASR33 behavior (continuous scrolling, no auto-clear).
# Note: Step commands (Ctrl+T/Ctrl+K) DO clear output for clarity when debugging"

However, in _menu_step_line (line ~2050) and _menu_step_stmt (line ~2110), the code only contains:
"# Note: Output is NOT cleared - continuous scrolling like ASR33 teletype"

There is no code in either step method that clears output. Both comments say output is NOT cleared.

---

#### code_vs_comment

**Description:** Duplicate and contradictory comments about INPUT prompt handling in _execute_tick

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _execute_tick method, there are two identical comment blocks explaining why the prompt is not appended to output:

First occurrence (line ~1910):
"# Note: We don't append the prompt to output here because the interpreter
# has already printed it via io.output() before setting input_prompt state.
# Verified: INPUT statement calls io.output(prompt) before awaiting user input."

Second occurrence (line ~1935):
"# Note: We don't append the prompt to output here because the interpreter
# has already printed it via io.output() before setting input_prompt state.
# Verified: INPUT statement calls io.output(prompt) before awaiting user input."

The duplication suggests copy-paste without cleanup.

---

#### code_vs_comment

**Description:** Comment about statement table usage in _update_breakpoint_display may be outdated

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _update_breakpoint_display (line ~1560), comment states:
"# Use the same logic as current_statement_char_end for consistency"

This references a property that may not exist or may have been refactored. The code then implements complex logic to calculate char_end by checking for next statement, but it's unclear if this matches the referenced 'current_statement_char_end' logic.

---

#### code_vs_comment

**Description:** Comment about runtime object reuse contradicts earlier comment about runtime creation

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _menu_step_stmt (line ~2120), comment states:
"# Note: Interpreter/runtime objects are reused across runs (not recreated each time).
# The runtime.reset_for_run() call above clears variables but preserves breakpoints."

However, just above this comment (line ~2115), the code shows:
"if self.runtime is None:
    self.runtime = Runtime(self.program.line_asts, self.program.lines)
    self.runtime.setup()
else:
    self.runtime.reset_for_run(self.program.line_asts, self.program.lines)"

The comment implies runtime is always reused, but the code shows it's created if None. The comment should clarify 'reused when possible' or 'reused after first creation'.

---

#### code_vs_comment

**Description:** Comment claims PC preservation logic prevents accidental execution starts, but code actually handles state preservation during statement table rebuilds

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_sync_program_to_runtime() method:

Comment says: "# Conditionally restore PC based on whether execution timer is active
# This logic is about PRESERVING vs RESETTING state, not about preventing accidental starts"

But earlier comment says: "# Timer is not active - no execution in progress, so reset to halted state
# (ensures program doesn't start executing unexpectedly when LIST/edit commands run)"

The second comment contradicts the first by claiming it DOES prevent accidental starts.

---

#### code_vs_comment

**Description:** Comment claims _on_enter_key handles auto-numbering, but method body shows it's actually handled by _on_editor_change

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_on_enter_key() docstring:
"Handle Enter key press in editor - triggers auto-numbering.

Note: This method is called internally by _on_editor_change when a new line
is detected. The actual auto-numbering logic is in _add_next_line_number."

But method body:
"# Auto-numbering on Enter is handled by _on_editor_change detecting new lines
# and calling _add_next_line_number via timer
pass"

The docstring says the method 'triggers auto-numbering' but the code does nothing (pass). The docstring is misleading about what this method does.

---

#### code_vs_comment

**Description:** Comment describes TWO input mechanisms but doesn't explain when each is used or if they can conflict

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_handle_output_enter() method:

Comment: "# Provide input to interpreter via TWO mechanisms (we check both in case either is active):
# 1. interpreter.provide_input() - Used when interpreter is waiting synchronously
#    (checked via interpreter.state.input_prompt). Stores input for retrieval.
...
# 2. input_future.set_result() - Used when async code is waiting via asyncio.Future
#    (see _get_input_async method). Only one path will be active at a time, but we
#    check both to handle whichever path the interpreter is currently using."

The comment says 'Only one path will be active at a time' but the code calls BOTH unconditionally. This could cause issues if both mechanisms are active simultaneously, or waste cycles checking both every time.

---

#### code_vs_comment

**Description:** Comment claims method removes blank lines 'except the last line', but code preserves last line unconditionally even if it's the only line

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_remove_blank_lines() docstring:
"Remove blank lines from editor except the last line.

The last line is preserved even if blank to avoid removing it while the user
is actively typing on it. Only the final line is preserved; all other blank
lines are removed regardless of cursor position."

Code:
"for i, line in enumerate(lines):
    if line.strip() or i == len(lines) - 1:
        non_blank_lines.append(line)"

If there's only ONE line and it's blank, the code preserves it (i == len(lines) - 1 is true). The docstring doesn't clarify this edge case - it could be interpreted as 'remove all blank lines except when it's the last line of multiple lines'.

---

#### code_vs_comment

**Description:** Comment claims 'halted flag removed' and 'PC is now immutable', but code still calls PC.halted_pc() method

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~13: '# Note: halted flag removed - PC is now immutable and indicates running state'

But code at line ~48 uses: 'self.runtime.pc = PC(state['pc']['line'], state['pc']['stmt']) if state['pc'] else PC.halted_pc()'

This suggests either:
1. The comment is outdated and PC.halted_pc() is still a valid method
2. The code should be using a different approach to represent halted state

---

#### code_vs_comment

**Description:** Comment claims 'stopped flag removed' and 'PC.stop_reason now indicates stop state', but no code references stop_reason attribute

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~24: '# Note: stopped flag removed - PC.stop_reason now indicates stop state (display only)'

Comment at line ~60: '# Note: stopped flag removed - PC.stop_reason now indicates stop state (display only)'

However, nowhere in the visible code is 'stop_reason' attribute accessed or used. The serialization/deserialization code doesn't handle stop_reason at all, only mentions it in comments.

---

#### documentation_inconsistency

**Description:** Help URL inconsistency - documentation mentions legacy localhost:8000 but code uses /mbasic_docs path

**Affected files:**
- `docs/help/README.md`
- `src/ui/web_help_launcher.py`

**Details:**
README.md states: '(Legacy code may reference `http://localhost:8000`, which is deprecated in favor of the `/mbasic_docs` path.)'

But web_help_launcher.py HELP_BASE_URL = 'http://localhost/mbasic_docs' and the WebHelpLauncher_DEPRECATED class uses self.server_port = 8000 with localhost:8000 URLs.

The deprecated class comment says: 'NEW: In NiceGUI backend, use: ui.navigate.to('/mbasic_docs/statements/print/', new_tab=True)' but this path format is inconsistent with HELP_BASE_URL which includes the full http://localhost prefix.

---

#### documentation_inconsistency

**Description:** Documentation references shortcuts that don't exist in keybindings config

**Affected files:**
- `docs/help/common/debugging.md`
- `src/ui/web_keybindings.json`

**Details:**
debugging.md references:
- 'toggle_stack' shortcut (Tk UI section)
- 'step_line' shortcut (Curses UI section)
- 'quit' shortcut

But web_keybindings.json only defines:
- run, stop, save, new, open, help, toggle_breakpoint, step, continue, toggle_variables

Missing: toggle_stack, step_line, quit (though 'stop' may be equivalent to 'quit')

---

#### documentation_inconsistency

**Description:** Optimization doc claims '27 optimizations' but lists 27 items with some being analysis not optimization

**Affected files:**
- `docs/help/common/compiler/optimizations.md`

**Details:**
optimizations.md title: '27 compiler optimization techniques'

But several listed items are analysis techniques, not optimizations:
- 'Subroutine Side-Effect Analysis' - tracks effects, doesn't optimize
- 'Loop Analysis' - detects loops, doesn't optimize them
- 'OPTION BASE Analysis' - validates consistency
- 'Uninitialized Variable Detection' - warns, doesn't optimize
- 'Range Analysis' - tracks ranges for other optimizations
- 'Live Variable Analysis' - foundational analysis
- 'Built-in Function Purity Analysis' - classifies functions
- 'Alias Analysis' - determines safety of other optimizations
- 'Available Expression Analysis' - tracks expressions

These are important compiler features but calling them 'optimizations' is misleading. They enable optimizations but aren't optimizations themselves.

---

#### code_documentation_mismatch

**Description:** Settings dialog exists in code but not documented in help system

**Affected files:**
- `src/ui/web/web_settings_dialog.py`
- `docs/help/common/debugging.md`
- `docs/help/common/editor-commands.md`

**Details:**
web_settings_dialog.py implements a full settings dialog with:
- Editor settings (auto-numbering, line number increment)
- Resource limits (read-only)
- Save/Cancel functionality

But debugging.md and editor-commands.md don't mention any settings dialog or how to access it. Users won't know this feature exists or how to configure auto-numbering.

---

#### documentation_inconsistency

**Description:** Inconsistent cross-references between getting-started.md and language.md

**Affected files:**
- `docs/help/common/getting-started.md`
- `docs/help/common/language.md`

**Details:**
getting-started.md says 'For detailed reference documentation, see [BASIC Language Reference](language.md)' but language.md says 'For a beginner-friendly tutorial, see [Getting Started](getting-started.md)'. However, getting-started.md also links to [BASIC Language Reference](language/statements/index.md) in the 'Next Steps' section, creating confusion about whether language.md or language/statements/index.md is the main reference.

---

#### documentation_inconsistency

**Description:** Inconsistent precision information for ATN function

**Affected files:**
- `docs/help/common/language/data-types.md`
- `docs/help/common/language/functions/atn.md`

**Details:**
data-types.md states SINGLE precision has '~7 significant digits' and atn.md says 'the evaluation of ATN is always performed in single precision (~7 significant digits)'. However, atn.md also has a note: 'When computing PI with `ATN(1) * 4`, the result is limited to single precision (~7 digits). For higher precision, use `ATN(CDBL(1)) * 4` to get double precision.' This contradicts the statement that ATN is 'always performed in single precision' - if CDBL can force double precision, then ATN is not always single precision.

---

#### documentation_inconsistency

**Description:** Error code reference inconsistency

**Affected files:**
- `docs/help/common/language/appendices/error-codes.md`
- `docs/help/common/language/functions/cvi-cvs-cvd.md`

**Details:**
cvi-cvs-cvd.md states 'Raises "Illegal function call" (error code FC)' but error-codes.md lists this as 'Code: FC, Number: 5'. The function doc uses 'FC' as the error code, which matches error-codes.md, but it would be clearer to also mention 'error number 5' for consistency with how errors are typically referenced in BASIC.

---

#### documentation_inconsistency

**Description:** Incomplete cross-referencing between character set and ASCII codes

**Affected files:**
- `docs/help/common/language/character-set.md`
- `docs/help/common/language/appendices/ascii-codes.md`

**Details:**
character-set.md has a 'See Also' section linking to ascii-codes.md, but ascii-codes.md does not reciprocally link back to character-set.md in its 'See Also' section. This creates a one-way reference that makes navigation less intuitive.

---

#### documentation_inconsistency

**Description:** Missing error code reference in EOF documentation

**Affected files:**
- `docs/help/common/language/functions/eof.md`
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
eof.md mentions 'to avoid "Input past end" errors' but doesn't reference the specific error code. According to error-codes.md, this is error 62 'Input past end'. The EOF documentation should reference this error code for consistency with other function docs like cvi-cvs-cvd.md which explicitly mentions error codes.

---

#### documentation_inconsistency

**Description:** LOF function is documented in detail but missing from the index categorization

**Affected files:**
- `docs/help/common/language/functions/index.md`
- `docs/help/common/language/functions/lof.md`

**Details:**
The index.md file lists LOF under 'File I/O Functions' in the alphabetical quick reference, but LOF is not listed in the 'By Category' section under 'File I/O Functions'. The category section lists: EOF, INPUT$, LOC, LOF (missing), LPOS, but LOF has a complete documentation file at lof.md.

---

#### documentation_inconsistency

**Description:** Inconsistent Control-C behavior documentation

**Affected files:**
- `docs/help/common/language/functions/inkey_dollar.md`
- `docs/help/common/language/functions/input_dollar.md`

**Details:**
Both INKEY$ and INPUT$ document Control-C behavior with identical notes: 'Note: Control-C behavior varied in original implementations. In MBASIC 5.21 interpreter mode, Control-C would terminate the program. This implementation passes Control-C through (CHR$(3)) for program detection and handling, allowing programs to detect and handle it explicitly.' However, this note appears to be implementation-specific and may not belong in both places, or should be consistently applied to all input functions.

---

#### documentation_inconsistency

**Description:** LPOS 'See Also' section references functions not in its category

**Affected files:**
- `docs/help/common/language/functions/lpos.md`

**Details:**
LPOS is categorized as a 'file-io' function but its 'See Also' section references POS, LPRINT, LPRINT USING, WIDTH LPRINT, PRINT, and PRINT# - mixing console, printer, and file I/O functions. The original documentation had a different 'See Also' list that was replaced with implementation-specific alternatives.

---

#### documentation_inconsistency

**Description:** CLEAR documentation has conflicting information about parameter meanings between MBASIC 5.21 and earlier versions

**Affected files:**
- `docs/help/common/language/statements/clear.md`

**Details:**
The documentation states:

"In MBASIC 5.21 (BASIC-80 release 5.0 and later):
- expression1: If specified, sets the highest memory location available for BASIC to use
- expression2: Sets the stack space reserved for BASIC"

But then notes:

"Historical note: In earlier versions of BASIC-80 (before release 5.0), the parameters had different meanings:
- expression1 set the amount of string space
- expression2 set the end of memory"

This is confusing because the current documentation is for MBASIC 5.21, but includes historical information that contradicts the current behavior. The syntax section doesn't clarify which version's behavior is being documented.

---

#### documentation_inconsistency

**Description:** DEF FN documentation claims multi-character function names are an extension over MBASIC 5.21, but DEFINT/SNG/DBL/STR documentation doesn't mention this is also an extension

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`
- `docs/help/common/language/statements/defint-sng-dbl-str.md`

**Details:**
def-fn.md states:
"**Original MBASIC 5.21**: Function names were limited to a single character after FN:
- ✓ `FNA` - single character
- ✓ `FNB$` - single character with type suffix

**This implementation (extension)**: Function names can be multiple characters"

However, defint-sng-dbl-str.md doesn't clarify whether the DEF<type> statements themselves have any extensions or differences from original MBASIC 5.21. The documentation should be consistent about noting extensions.

---

#### documentation_inconsistency

**Description:** END documentation states files remain closed after CONT, but doesn't clarify if this is different from STOP behavior

**Affected files:**
- `docs/help/common/language/statements/end.md`
- `docs/help/common/language/statements/stop.md`

**Details:**
end.md states:
"Both END and STOP allow continuation with CONT. The key difference is that END closes all files before returning to command level, and these files remain closed even if execution is continued with CONT."

However, the stop.md file is not provided in the documentation set, so we cannot verify if STOP's behavior with files and CONT is properly documented for comparison. This creates potential confusion about file handling after CONT.

---

#### documentation_inconsistency

**Description:** FIELD and GET documentation have inconsistent detail about random file operations

**Affected files:**
- `docs/help/common/language/statements/field.md`
- `docs/help/common/language/statements/get.md`

**Details:**
field.md provides extensive detail:
"FIELD does NOT place any data in the random file buffer. (See LSET/RSET and GET.)

The total number of bytes allocated in a FIELD statement must not exceed the record length that was specified when the file was OPENed. Otherwise, a 'Field overflow' error occurs. (The default record length is 128.)

Any number of FIELD statements may be executed for the same file, and all FIELD statements that have been executed are in effect at the same time."

get.md is much briefer:
"<file number> is the number under which the file was OPENed. If <record number> is omitted, the next record (after the last GET) is read into the buffer. The largest possible record number is 32767."

The GET documentation doesn't mention the relationship with FIELD statements or how the buffer is structured, which could confuse users trying to understand the complete random file I/O workflow.

---

#### documentation_inconsistency

**Description:** INPUT and INPUT# have different levels of detail about data parsing rules

**Affected files:**
- `docs/help/common/language/statements/input.md`
- `docs/help/common/language/statements/input_hash.md`

**Details:**
input.md provides basic behavior:
"Key behaviors:
- Multiple values must be separated by commas
- String values may be entered with or without quotes (quotes are required if the string contains commas)
- If too few values are entered, the prompt is repeated with ?? for the remaining values
- If too many values are entered, a '?Redo from start' message is displayed and the user must re-enter all values"

input_hash.md provides much more detailed parsing rules:
"With INPUT#, no question mark is printed, as with INPUT. The data items in the file should appear just as they would if data were being typed in response to an INPUT statement. With numeric values, leading spaces, carriage returns and line feeds are ignored. The first character encountered that is not a space, carriage return or line feed is assumed to be the start of a number. The number terminates on a space, carriage return, line feed or comma. If BASIC-80 is scanning the sequential data file for a string item, leading spaces, carriage returns and line feeds are also ignored. The first character encountered that is not a space, carriage return, or line feed is assumed to be the start of a string item. If this first character is a quotation mark ("), the string item will consist of all characters read between the first quotation mark and the second. Thus, a quoted string may not contain a quotation mark as a character. If the first character of the string is not a quotation mark, the string is an unquoted string, and will terminate on a comma, carriage or line feed (or after 255 characters have been read)."

The INPUT documentation should include similar parsing detail since the behavior should be the same.

---

#### documentation_inconsistency

**Description:** ERR/ERL documentation states ERR is reset to 0 after RESUME, but ERROR documentation doesn't mention this

**Affected files:**
- `docs/help/common/language/statements/err-erl-variables.md`
- `docs/help/common/language/statements/error.md`

**Details:**
err-erl-variables.md states:
"- ERR is reset to 0 when:
  - RESUME statement is executed
  - A new RUN command is issued
  - An error handling routine ends normally (without error)"

error.md doesn't mention what happens to ERR after the error handler completes or after RESUME. This could lead to confusion about when ERR values persist.

---

#### documentation_inconsistency

**Description:** Inconsistent maximum line length specification between LINE INPUT# and LINE INPUT

**Affected files:**
- `docs/help/common/language/statements/inputi.md`
- `docs/help/common/language/statements/line-input.md`

**Details:**
LINE INPUT# documentation states: 'To read an entire line (up to 254 characters)'
LINE INPUT documentation states: 'To input an entire line (up to 254 characters)'
Both claim 254 character limit, but this should be verified as consistent across both file and console input operations.

---

#### documentation_inconsistency

**Description:** Contradictory information about file closing behavior

**Affected files:**
- `docs/help/common/language/statements/load.md`
- `docs/help/common/language/statements/merge.md`

**Details:**
LOAD documentation states:
'**LOAD** (without ,R): Closes all open files and deletes all variables and program lines currently in memory before loading'
'**LOAD** with **,R** option: Program is RUN after loading, and all open data files are **kept open** for program chaining'
'Compare with **MERGE**: Never closes files (see [MERGE](merge.md))'

MERGE documentation states:
'**File handling:** Unlike LOAD (without ,R), MERGE does **NOT close open files**. Files that are open before MERGE remain open after MERGE completes. (Compare with [LOAD](load.md) which closes files except when using the ,R option.)'

The LOAD doc says 'Compare with MERGE: Never closes files' but MERGE says 'Unlike LOAD (without ,R)' - this creates potential confusion about the default LOAD behavior.

---

#### documentation_inconsistency

**Description:** Inconsistent string modification behavior documentation

**Affected files:**
- `docs/help/common/language/statements/lset.md`
- `docs/help/common/language/statements/mid-assignment.md`

**Details:**
LSET documentation states: 'If the string is shorter than the field defined by the string variable, the string is padded on the right with spaces. If the string is longer than the field, the extra characters on the right are truncated.'

MID$ Assignment states: 'The string length never changes (no characters are added or removed)'

Both modify strings but LSET can pad with spaces while MID$ cannot change length. This difference should be more clearly highlighted as they serve different purposes (LSET for file fields, MID$ for in-place modification).

---

#### documentation_inconsistency

**Description:** Inconsistent error handling documentation for ON statements

**Affected files:**
- `docs/help/common/language/statements/on-error-goto.md`
- `docs/help/common/language/statements/on-gosub-on-goto.md`

**Details:**
ON...GOSUB/ON...GOTO states: 'If the value of <expression> is zero or greater than the number of items in the list (but less than or equal to 255), BASIC continues with the next executable statement. If the value of <expression> is negative or greater than 255, an "Illegal function call" error occurs.'

ON ERROR GOTO does not document what happens if the line number is out of range (>65529) or negative, only stating 'If <line number> does not exist, an "Undefined line" error results.' This creates inconsistent error condition documentation across ON statements.

---

#### documentation_inconsistency

**Description:** Missing information about interaction with existing arrays

**Affected files:**
- `docs/help/common/language/statements/option-base.md`

**Details:**
OPTION BASE documentation states: 'The OPTION BASE statement must appear before any DIM statements or array references in the program.'

But does not specify what happens if:
1. OPTION BASE appears after arrays are already dimensioned
2. Multiple OPTION BASE statements appear (it says 'Only one OPTION BASE statement is allowed per program' but doesn't specify the error)
3. Arrays are used before OPTION BASE with implicit dimensioning

This creates ambiguity about error conditions and enforcement.

---

#### documentation_inconsistency

**Description:** Contradictory information about PRINT# usage with random files

**Affected files:**
- `docs/help/common/language/statements/put.md`
- `docs/help/common/language/statements/printi-printi-using.md`

**Details:**
PUT documentation states: 'PRINT#, PRINT# USING, and WRITE# may be used to put characters in the random file buffer before a PUT statement.'

PRINT# documentation states: 'PRINT# writes data to a sequential file opened for output (mode "O") or append (mode "A")'

PUT suggests PRINT# can be used with random files, but PRINT# documentation only mentions sequential files. This creates confusion about whether PRINT# works with random files.

---

#### documentation_inconsistency

**Description:** Cross-reference inconsistency: RESET warns not to confuse with RSET, but RSET warns not to confuse with RESET. Both should reference each other consistently.

**Affected files:**
- `docs/help/common/language/statements/reset.md`
- `docs/help/common/language/statements/rset.md`

**Details:**
reset.md: "**Note:** Do not confuse RESET with [RSET](rset.md), which right-justifies strings in random file fields."

rset.md: "**Note:** Do not confuse RSET with [RESET](reset.md), which closes all open files."

Both documents have the warning, which is good, but the phrasing could be more consistent.

---

#### documentation_inconsistency

**Description:** RESUME and RESTORE have very similar names but completely different purposes. No cross-reference warning exists to prevent confusion.

**Affected files:**
- `docs/help/common/language/statements/resume.md`
- `docs/help/common/language/statements/restore.md`

**Details:**
RESUME continues after error handling (error-handling category)
RESTORE resets DATA pointer (data category)

These similar names could easily be confused by users. Consider adding cross-reference warnings like the RESET/RSET pattern.

---

#### documentation_inconsistency

**Description:** SAVE documentation mentions file extensions but RUN documentation doesn't clearly specify default extension behavior.

**Affected files:**
- `docs/help/common/language/statements/save.md`
- `docs/help/common/language/statements/run.md`

**Details:**
save.md: "(With CP/M, the default extension .BAS is supplied.)"

run.md: "File extension defaults to .BAS if not specified" (in Notes section)

The RUN documentation should be more explicit about this in the Remarks section, matching the clarity in SAVE.

---

#### documentation_inconsistency

**Description:** WIDTH documentation states unsupported syntax will cause parse error, but doesn't specify the exact error message or error code.

**Affected files:**
- `docs/help/common/language/statements/width.md`

**Details:**
width.md: "**⚠️ UNSUPPORTED SYNTAX** - Original MBASIC 5.21 also supported:
```basic
WIDTH LPRINT <integer expression>  ' ⚠️ NOT SUPPORTED - will cause parse error
```"

Should specify what error message users will see when attempting to use this syntax.

---

#### documentation_inconsistency

**Description:** Variables documentation mentions case_conflict setting but doesn't link to settings documentation, while settings documentation doesn't link back to variables.

**Affected files:**
- `docs/help/common/language/variables.md`
- `docs/help/common/settings.md`

**Details:**
variables.md: "**Case Sensitivity:** Variable names are not case-sensitive by default (Count = COUNT = count), but the behavior when using different cases can be configured via the `variables.case_conflict` setting..."

settings.md has detailed explanation of variables.case_conflict but no link back to variables.md.

These should cross-reference each other.

---

#### documentation_inconsistency

**Description:** Settings documentation shows SETSETTING syntax without quotes around setting name, but doesn't explicitly state this is required syntax.

**Affected files:**
- `docs/help/common/settings.md`
- `docs/help/common/language/statements/showsettings.md`
- `docs/help/common/language/statements/setsetting.md`

**Details:**
settings.md example: "SETSETTING editor.auto_number_step 100"
setsetting.md syntax: "SETSETTING setting.name value"

Should explicitly state in setsetting.md Remarks: "The setting name uses dotted notation without quotes" to match the clarity in settings.md.

---

#### documentation_inconsistency

**Description:** RESUME documentation has extensive examples and testing notes, but other error handling statements (ON ERROR GOTO) may not have equivalent detail.

**Affected files:**
- `docs/help/common/language/statements/resume.md`

**Details:**
resume.md has:
- 5 detailed examples with output
- Error codes reference table
- Testing verification section: "Verified behavior against real MBASIC 5.21"

This level of detail should be consistent across related error handling documentation.

---

#### documentation_inconsistency

**Description:** TRON-TROFF documentation doesn't specify if trace output goes to screen or can be redirected, and doesn't mention performance impact.

**Affected files:**
- `docs/help/common/language/statements/tron-troff.md`

**Details:**
tron-troff.md shows trace output in example but doesn't specify:
- Does trace output go to screen or can it be redirected to file?
- What's the performance impact of TRON?
- Does TRON affect timing-sensitive code?
- Can TRON output be captured by PRINT# redirection?

---

#### documentation_inconsistency

**Description:** Settings documentation shows storage paths for Linux/Mac/Windows but doesn't mention project-level settings file location clearly in the storage section.

**Affected files:**
- `docs/help/common/settings.md`

**Details:**
settings.md "Settings Storage" section:
- **Linux/Mac**: `~/.mbasic/settings.json`
- **Windows**: `%APPDATA%\mbasic\settings.json`
- **Project**: `.mbasic/settings.json` in project directory

But earlier in "Settings Scope" it mentions project scope. The storage section should be more explicit about when/how project settings are used.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation about EDIT command availability and purpose across UIs

**Affected files:**
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/curses/editing.md`

**Details:**
CLI docs state: 'The CLI includes a line editor accessed with the **EDIT** command' and lists it as a common command.

Curses docs state: 'The **EDIT** command is supported for compatibility with traditional BASIC, but the Curses UI provides full-screen editing capabilities that make it unnecessary.'

This creates confusion about whether EDIT is a primary feature (CLI) or a compatibility-only feature (Curses).

---

#### documentation_inconsistency

**Description:** Contradictory information about BREAK, STEP, STACK command availability

**Affected files:**
- `docs/help/mbasic/extensions.md`
- `docs/help/common/ui/cli/index.md`

**Details:**
extensions.md states these are 'CLI (command form)' available.

However, cli/index.md does NOT list BREAK, STEP, or STACK in the 'Common Commands' table, nor mentions them anywhere in the document.

If these are CLI commands, they should be documented in the CLI interface guide.

---

#### documentation_inconsistency

**Description:** Inconsistent description of PEEK behavior

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/compatibility.md`

**Details:**
architecture.md states: 'PEEK: Returns random integer 0-255 (for RNG seeding compatibility)'

compatibility.md states the same but adds: '**Why:** Programs often used `RANDOMIZE PEEK(0)` to seed random numbers. Since we cannot access real memory, PEEK returns random values to support this common pattern.'

The rationale in compatibility.md is helpful context that should also be in architecture.md for completeness.

---

#### documentation_inconsistency

**Description:** Inconsistent information about WIDTH statement support

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/extensions.md`

**Details:**
compatibility.md states: 'WIDTH is parsed for compatibility but performs no operation. Terminal width is controlled by the UI or OS. The "WIDTH LPRINT" syntax is not supported.'

extensions.md does not mention WIDTH at all in its feature comparison or enhancement sections.

Since WIDTH is mentioned as a compatibility feature with specific limitations, it should be documented in extensions.md as well.

---

#### documentation_inconsistency

**Description:** Missing reference to extensions.md in main help index

**Affected files:**
- `docs/help/mbasic/extensions.md`
- `docs/help/index.md`

**Details:**
index.md lists key documentation sections including 'Getting Started', 'Features', 'Compatibility', 'Architecture' under the MBASIC section.

However, it does NOT list 'Extensions' which is a major documentation file (extensions.md) that users would want to discover.

The extensions.md file should be linked from the main index.

---

#### documentation_inconsistency

**Description:** Contradictory statement about line ending handling

**Affected files:**
- `docs/help/mbasic/compatibility.md`

**Details:**
compatibility.md states: '**Line ending support:** More permissive than MBASIC 5.21' and 'CP/M MBASIC 5.21: Only recognizes CRLF (`\r\n`)' and 'This implementation: Recognizes CRLF, LF (`\n`), and CR (`\r`)'.

Later it states: '**More permissive than MBASIC 5.21:** Accepts LF, CR, or CRLF line endings (original only CRLF)'.

This is repeated information in two different sections, which could lead to maintenance issues if one is updated and the other isn't.

---

#### documentation_inconsistency

**Description:** Inconsistent information about Find/Replace availability across UIs

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/find-replace.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
features.md states 'Find/Replace is not available in Curses UI. Use the Tk UI' and 'Find/Replace is not available in CLI. Use the Tk UI' and 'Find/Replace is not available in Web UI. Use the Tk UI', but find-replace.md for CLI provides detailed workarounds and alternative methods. The features.md document should either acknowledge these workarounds exist or be more specific that there's no built-in command (as find-replace.md correctly states).

---

#### documentation_inconsistency

**Description:** Debugging features availability inconsistency

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/debugging.md`

**Details:**
features.md states under Debugging: 'Breakpoints - Set/clear breakpoints (available in all UIs; access method varies)' and similar for step execution, variable viewing, and stack viewer. However, cli/debugging.md documents BREAK, STEP, and STACK commands as CLI-specific features. The features.md should clarify that these are CLI commands, while other UIs have different mechanisms (keyboard shortcuts, menu items, etc.).

---

#### documentation_inconsistency

**Description:** LPRINT implementation status inconsistency

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
features.md states 'LPRINT - Line printer output (Note: Statement is parsed but produces no output - see [LPRINT](../common/language/statements/lprint-lprint-using.md) for details)'. This suggests LPRINT is partially implemented (parsed but non-functional). However, not-implemented.md does not list LPRINT in its comprehensive list of not-implemented features, which could lead readers to believe it's fully functional.

---

#### documentation_inconsistency

**Description:** Keyboard shortcut notation inconsistency

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
features.md uses template notation like '{{kbd:run:curses}}' and '{{kbd:help:curses}}' for keyboard shortcuts, while getting-started.md uses the same notation. However, the actual key combinations are never shown in these documents - they reference a template system that should be resolved. This makes the documentation less useful as standalone reference material.

---

#### documentation_inconsistency

**Description:** PEEK/POKE implementation status unclear

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
features.md lists under Functions: 'PEEK, POKE - Memory access (emulated)' and under Intentional Differences: 'PEEK/POKE - Emulated (no direct memory access)'. not-implemented.md states 'PEEK/POKE are emulated with virtual memory in this implementation' under Available in MBASIC 5.21. However, it also lists under Hardware Access 'Note: PEEK/POKE are emulated with virtual memory in this implementation' suggesting they're not fully functional. The exact capabilities and limitations need clarification.

---

#### documentation_inconsistency

**Description:** Web UI feature completeness inconsistency

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`
- `docs/help/ui/cli/find-replace.md`

**Details:**
features.md describes Web UI with 'Basic debugging - Simple breakpoint support via menu' and lists significant limitations (session-based storage, 50 file limit, 1MB per file, no paths). However, getting-started.md presents Web UI as a full alternative ('Best for: Remote access, collaborative development, modern web-based workflow') without mentioning these significant limitations upfront. Users might be misled about Web UI capabilities.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation for toggle variables

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/cli/variables.md`

**Details:**
In curses/variables.md: "Press `{{kbd:toggle_variables:curses}}` to open the variables window."

In cli/variables.md: "The CLI does not have a Variables Window feature. For visual variable inspection, use:
- **Curses UI** - Full-screen terminal with Variables Window ({{kbd:toggle_variables:curses}})"

The notation is consistent, but cli/variables.md should clarify that this shortcut only works in Curses UI, not CLI.

---

#### documentation_inconsistency

**Description:** Execution Stack access method inconsistency

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/variables.md`

**Details:**
In feature-reference.md: "### Execution Stack
View the call stack showing:

**Access methods:**
- Via menu: Ctrl+U → Debug → Execution Stack
- Via command: Type `STACK` in immediate mode (same as CLI)"

In variables.md, there is no mention of the Execution Stack feature at all, even though it's a debugging feature related to variable inspection. The variables.md document should cross-reference the Execution Stack feature.

---

#### documentation_inconsistency

**Description:** Cut/Copy/Paste explanation inconsistency

**Affected files:**
- `docs/help/ui/curses/editing.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
In editing.md: "**Note:** Cut/Copy/Paste operations are not available in the Curses UI due to keyboard shortcut conflicts:
- **{{kbd:stop:curses}}** (Ctrl+C) - Used for Stop/Interrupt, cannot be used for Copy
- **{{kbd:save:curses}}** (Ctrl+S) - Used for Save File, cannot be used for Paste (also reserved by terminal for flow control)
- Cut would require Ctrl+X which isn't used but omitted for consistency"

In feature-reference.md: "### Cut/Copy/Paste (Not implemented)
Standard clipboard operations are not available in the Curses UI due to keyboard shortcut conflicts:
- **{{kbd:stop:curses}}** - Used for Stop/Interrupt (cannot be used for Cut)
- **{{kbd:continue:curses}}** - Terminal signal to exit program (cannot be used for Copy)
- **{{kbd:save:curses}}** - Used for Save File (cannot be used for Paste; {{kbd:save:curses}} is reserved by terminal for flow control)"

The explanations differ: editing.md says Ctrl+C is for Stop (correct), but feature-reference.md says {{kbd:continue:curses}} is for Copy, which is inconsistent. Also, feature-reference.md mentions {{kbd:continue:curses}} as 'Terminal signal to exit program' which seems wrong - that's typically Ctrl+C, not the continue key.

---

#### documentation_inconsistency

**Description:** Running.md placeholder vs actual content

**Affected files:**
- `docs/help/ui/common/running.md`
- `docs/help/ui/curses/running.md`

**Details:**
In common/running.md: "**Status:** PLACEHOLDER - Documentation in progress

This page will cover:
- How to run BASIC programs
- RUN command
- Program execution
- Stopping programs
- Continuing after STOP"

In curses/running.md: Full documentation exists with sections on 'Running a Program', 'Output Window', 'Interactive Programs', 'Stopping a Program', 'Listing Programs', etc.

The common/running.md is marked as a placeholder but curses/running.md has complete content. Either the common version should be filled in or it should reference the UI-specific versions.

---

#### documentation_inconsistency

**Description:** Error handling documentation references non-existent pages

**Affected files:**
- `docs/help/ui/common/errors.md`
- `docs/help/ui/cli/variables.md`

**Details:**
In common/errors.md: "## See Also

- [ON ERROR GOTO](../../common/language/statements/on-error-goto.md) - Set up error handling
- [ERR and ERL](../../common/language/statements/err-erl-variables.md) - Error information
- [RESUME](../../common/language/statements/resume.md) - Continue after error
- [Error Codes](../../common/language/appendices/error-codes.md) - Complete error code reference"

These referenced files are not provided in the documentation set, so we cannot verify if they exist or if the paths are correct. This could be a broken link issue.

---

#### documentation_inconsistency

**Description:** Window control shortcuts may not be implemented

**Affected files:**
- `docs/help/ui/curses/variables.md`

**Details:**
In variables.md under 'Window Controls':
"### Resize and Position
- **Ctrl+Arrow**: Move window
- **Alt+Arrow**: Resize window
- **Ctrl+M**: Maximize/restore
- **{{kbd:stop:curses}}**: Close window"

These window manipulation shortcuts (Ctrl+Arrow, Alt+Arrow, Ctrl+M) are not mentioned anywhere else in the documentation and seem inconsistent with the terminal-based nature of the Curses UI. This section may describe planned features or may be copied from a different UI (like Tk). Needs verification.

---

#### documentation_inconsistency

**Description:** Mouse support features may not be implemented

**Affected files:**
- `docs/help/ui/curses/variables.md`

**Details:**
In variables.md:
"### Quick Navigation
- Double-click variable name (if mouse enabled)
- Jumps to first usage in code
- Shows all references"

And under 'Limitations':
"### Current Limitations
1. **No inline editing**: Cannot modify values in window
2. **No array expansion**: Cannot view array elements
3. **Limited mouse support**: Depends on terminal"

The document describes mouse features (double-click) but then lists 'Limited mouse support' as a limitation. This is contradictory. Either mouse support exists or it doesn't.

---

#### documentation_inconsistency

**Description:** Missing keyboard shortcut for Search Help in feature-reference.md

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/features.md`

**Details:**
feature-reference.md lists Search Help under Help System features but states:
"**Note:** Search function is available via the help browser's search box (no dedicated keyboard shortcut)."

However, features.md does not mention Search Help at all in its feature list, creating an inconsistency about whether this feature exists and how it's accessed.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut references for Step Statement

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/features.md`
- `docs/help/ui/tk/workflows.md`

**Details:**
feature-reference.md states:
"Step Statement
Execute one BASIC statement at a time.
- Menu: Run → Step Statement
- Toolbar: 'Stmt' button
- No keyboard shortcut"

But workflows.md states:
"Use Step Statement (Run menu) to step through code"

And features.md references:
"{{kbd:step_statement:tk}} - Execute next statement"

This is contradictory: feature-reference.md explicitly says "No keyboard shortcut" but features.md uses a kbd template suggesting there IS a shortcut. Either the shortcut exists or it doesn't.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut references for Continue

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/features.md`

**Details:**
feature-reference.md states:
"Continue
Resume execution after pausing at a breakpoint.
- Menu: Run → Continue
- Toolbar: 'Cont' button
- No keyboard shortcut"

But features.md references:
"{{kbd:continue_execution:tk}} - Continue to next breakpoint"

This is contradictory: feature-reference.md says "No keyboard shortcut" but features.md uses a kbd template suggesting there IS a shortcut.

---

#### documentation_inconsistency

**Description:** Inconsistent implementation status for keyboard shortcuts

**Affected files:**
- `docs/help/ui/web/debugging.md`

**Details:**
debugging.md states under Keyboard Shortcuts:
"**Currently Implemented:**
- `{{kbd:run:web}}` - Run program from beginning
- `{{kbd:continue:web}}` - Continue to next breakpoint
- `{{kbd:step:web}}` - Step to next line
- `{{kbd:stop:web}}` - Stop execution"

But then states:
"**Note:** {{kbd:toggle_breakpoint:web}} is implemented but currently available via menu only (not yet bound to keyboard)."

This is confusing: if toggle_breakpoint is "implemented" but "not yet bound to keyboard", should it be listed under "Currently Implemented" or "Planned"? The distinction between "feature implemented" and "keyboard shortcut bound" needs clarification.

---

#### documentation_inconsistency

**Description:** Inconsistent default UI information

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/getting-started.md`

**Details:**
getting-started.md states:
"```bash
mbasic --ui tk [filename.bas]
```

Or to use the default curses UI:
```bash
mbasic [filename.bas]
```"

This suggests curses is the default UI. However, index.md states:
"```bash
mbasic                # Default UI
mbasic --ui curses
```"

This confirms curses is default. But the phrasing in getting-started.md ("Or to use the default curses UI") is awkward because it's presented as an alternative to the Tk UI command, when actually it's just showing how to use the default. This could confuse users about which UI is default.

---

#### documentation_inconsistency

**Description:** Inconsistent information about browser DevTools keyboard shortcut

**Affected files:**
- `docs/help/ui/web/debugging.md`

**Details:**
debugging.md states under "Integration with Browser Tools":
"Press `F12` to open browser tools (standard browser shortcut):"

Then labels this as "(Standard Browser Features)" but earlier in the document under "Keyboard Shortcuts" section, it only lists MBASIC-specific shortcuts and doesn't mention F12. This creates inconsistency about whether F12 is considered part of the Web UI's keyboard shortcuts or just a browser feature. The document should clarify this distinction.

---

#### documentation_inconsistency

**Description:** Inconsistent information about file operations and toolbar buttons

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`

**Details:**
features.md under 'File Operations > Currently Implemented' states: 'Load .BAS files from local filesystem' and 'Save/download programs as .BAS files'

But getting-started.md under 'Toolbar' says: 'File operations (New, Open, Save, Save As) are available through the File menu.' - implying toolbar does NOT have file operation buttons.

However, getting-started.md later under 'Opening a File' says: 'Click Open button (or File → Open)' - implying there IS an Open button in the toolbar.

This is contradictory about whether file operation buttons exist in the toolbar or only in the menu.

---

#### documentation_inconsistency

**Description:** Inconsistent menu structure documentation

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
features.md under 'Debugging Tools > Variable Inspector > Currently Implemented' states: 'Basic variable viewing via Debug menu'

But web-interface.md under 'Menu Functions' lists: 'File Menu', 'Edit Menu', 'Run Menu', 'View Menu', 'Help Menu' - there is NO 'Debug menu' mentioned.

Later, web-interface.md under 'View Menu' says: 'Show Variables - Open the Variables Window to view and monitor program variables in real-time'

So the feature exists but is in the View menu, not a Debug menu. The features.md reference to 'Debug menu' is incorrect.

---

#### documentation_inconsistency

**Description:** Contradictory information about settings persistence and Redis storage

**Affected files:**
- `docs/help/ui/web/settings.md`
- `docs/help/ui/web/features.md`

**Details:**
settings.md describes two storage modes:
1. 'Local Storage (Default)' - 'settings are stored in your browser's localStorage'
2. 'Redis Session Storage (Multi-User Deployments)' - 'If the web server is configured with NICEGUI_REDIS_URL, settings are stored in Redis with per-session isolation'

But features.md under 'Local Storage > Currently Implemented' only mentions: 'Editor settings stored in browser localStorage (persists across sessions)' with no mention of Redis option.

Also, settings.md says Redis storage means 'Settings are session-based (cleared when session expires)' which contradicts the localStorage description that says settings 'persist across page reloads' and 'persist across sessions'.

This creates confusion about whether settings persist or are session-only, and whether Redis is actually implemented.

---

#### documentation_inconsistency

**Description:** Inconsistent information about breakpoint management interface

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
features.md under 'Breakpoints > Currently Implemented' states: 'Line breakpoints (toggle via Run menu)' and 'Management: Toggle via Run menu → Toggle Breakpoint'

getting-started.md under 'Breakpoints' says: 'Use Run → Toggle Breakpoint menu option' and 'Enter the line number'

But web-interface.md under 'Run Menu' says: 'Toggle Breakpoint - Set or remove a breakpoint at a specific line number' with no mention of how the line number is specified (dialog? current cursor position?).

The inconsistency is in the user interaction: Do you toggle at cursor position, or does a dialog ask for line number? The 'Enter the line number' phrase suggests a dialog, but this isn't clearly stated.

---

#### documentation_inconsistency

**Description:** Inconsistent toolbar button descriptions

**Affected files:**
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
getting-started.md under 'Toolbar' describes buttons as:
- 'Run - Parse and execute the program (▶️ green button, {{kbd:run:web}})'
- 'Step - Execute all statements on current line, then pause (⏭️ button, {{kbd:step_line:web}})'
- 'Stmt - Execute one statement, then pause (↻ button, {{kbd:step:web}})'

But web-interface.md under 'Toolbar' describes them as:
- 'Run (▶️ green) - Start program execution'
- 'Step (⏭️) - Execute all statements on current line'
- 'Stmt (↻) - Execute one statement'

The inconsistency is in the descriptions: getting-started.md says 'Parse and execute' and 'then pause', while web-interface.md just says 'Start program execution' and omits 'then pause'. The level of detail differs significantly.

---

#### documentation_inconsistency

**Description:** Calendar program appears in both Games and Utilities libraries with different descriptions and different actual programs

**Affected files:**
- `docs/library/games/index.md`
- `docs/library/utilities/index.md`

**Details:**
Games library describes calendar.bas as 'Full-year calendar display program - shows entire year's calendar at once (Creative Computing, 1979)' with a note pointing to Utilities.

Utilities library describes calendar.bas as 'Month/year calendar generator - prompts for specific month and year (1900-2099), prints formatted calendar (Dr Dobbs, 1982)' with a note pointing to Games.

These are clearly two different programs (1979 vs 1982, different sources, different functionality) but both are named 'calendar.bas'. The cross-references suggest they are alternatives, but they have the same filename which would cause a conflict.

---

#### documentation_inconsistency

**Description:** Most game entries are missing descriptions, authors, and tags

**Affected files:**
- `docs/library/games/index.md`

**Details:**
Out of approximately 130 games listed, only 3 have complete metadata (Calendar, Survival, and a few others). The vast majority show:

**Year:** 1980s
**Tags:** 

with empty descriptions and tags. This is inconsistent with other library categories (Electronics, Ham Radio, Utilities) where most entries have detailed descriptions.

---

#### documentation_inconsistency

**Description:** Timer555.bas appears to be duplicate of 555-ic.bas

**Affected files:**
- `docs/library/electronics/index.md`

**Details:**
Two entries with very similar descriptions:

555-Ic: '555 Timer calculator - calculates resistance and capacitance values for proper operation of the 555 timer-oscillator at desired frequency'

Timer555: '555 Timer circuit calculator - calculates component values for 555 timer circuits (similar to 555-ic.bas)'

The Timer555 description explicitly notes it's 'similar to 555-ic.bas', suggesting these may be duplicate or very similar programs. This should be clarified - are they different implementations, or is one redundant?

---

#### documentation_inconsistency

**Description:** CHOOSING_YOUR_UI.md claims CLI has 'full debugging capabilities through text commands' but QUICK_REFERENCE.md only documents Curses UI debugging features

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`
- `docs/user/QUICK_REFERENCE.md`

**Details:**
CHOOSING_YOUR_UI.md states:
'**Unique advantages:**
- Command-line debugging (BREAK, STEP, STACK commands)'

and

'> **Note:** CLI has full debugging capabilities through text commands (BREAK, STEP, STACK, etc.), but lacks visual debugging features (Variables Window, clickable breakpoints, graphical interface) found in Curses, Tk, and Web UIs.'

However, QUICK_REFERENCE.md is titled 'MBASIC Curses IDE - Quick Reference Card' and only documents Curses UI debugging with keyboard shortcuts like 'b' or 'F9' for breakpoints and 'c', 's', 'e' for continue/step/end. No CLI text commands are documented.

---

#### documentation_inconsistency

**Description:** Contradictory information about CLI dependencies

**Affected files:**
- `docs/user/INSTALL.md`
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
INSTALL.md states:
'| UI Mode | External Dependencies |
|---------|----------------------|
| **CLI** | None (Python standard library only) |'

and

'**If you only want CLI mode**, you can skip all pip dependency installation steps. Just run `python3 mbasic` and you\'re ready to go!'

CHOOSING_YOUR_UI.md confirms this:
'**Unique advantages:**
- Fastest startup time
- Lowest memory usage'

However, CHOOSING_YOUR_UI.md also lists CLI debugging commands (BREAK, STEP, STACK) which are not documented anywhere in the provided files, creating uncertainty about whether these are actually implemented or require additional setup.

---

#### documentation_inconsistency

**Description:** Settings file location inconsistency for Windows

**Affected files:**
- `docs/user/INSTALL.md`
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
INSTALL.md states:
'**On Debian/Ubuntu/Linux Mint systems**, you need to install these packages via `apt` with `sudo`'

But does not provide Windows-specific settings file location.

SETTINGS_AND_CONFIGURATION.md provides:
'**Location:**
- **Linux/Mac:** `~/.mbasic/settings.json`
- **Windows:** `%APPDATA%/mbasic/settings.json` (typically `C:\Users\YourName\AppData\Roaming\mbasic\settings.json`)'

INSTALL.md should reference where settings files are created on different platforms, especially since it mentions 'Settings files are automatically created' but doesn't specify where on Windows.

---

#### documentation_inconsistency

**Description:** README.md references keyboard-shortcuts.md as Curses-specific but doesn't clarify Tk shortcuts location

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`
- `docs/user/README.md`

**Details:**
README.md states:
'- **[keyboard-shortcuts.md](keyboard-shortcuts.md)** - Keyboard shortcuts reference (Curses UI specific; Tk shortcuts in TK_UI_QUICK_START.md)'

CHOOSING_YOUR_UI.md mentions keyboard shortcuts for multiple UIs:
'**Unique advantages:**
- Keyboard shortcuts' (for Curses)
'**Unique advantages:**
- Mouse support' (for Tk)

But doesn't clearly indicate where to find Tk keyboard shortcuts. Users might expect a unified keyboard shortcuts document or clearer signposting to TK_UI_QUICK_START.md from CHOOSING_YOUR_UI.md.

---

#### documentation_inconsistency

**Description:** File format documentation doesn't mention UI-specific file handling differences

**Affected files:**
- `docs/user/FILE_FORMAT_COMPATIBILITY.md`
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
FILE_FORMAT_COMPATIBILITY.md states:
'- **Loading files**: MBASIC automatically handles files with any line ending style'

and

'- **Saving files**: MBASIC always saves with LF line endings (`\n`)'

CHOOSING_YOUR_UI.md mentions:
'**Limitations:**
- Browser storage only
- No local file access' (for Web UI)

This suggests Web UI might handle files differently (browser storage vs filesystem), but FILE_FORMAT_COMPATIBILITY.md doesn't address whether line ending handling differs between UIs or how browser storage affects file format compatibility.

---

#### documentation_inconsistency

**Description:** Settings system status inconsistency

**Affected files:**
- `docs/user/INSTALL.md`
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
INSTALL.md states:
'- ✓ Settings system (SET, SHOW SETTINGS commands with global/project configuration files)'

Indicating the settings system is fully implemented.

SETTINGS_AND_CONFIGURATION.md has a status note:
'> **Status:** The settings system is implemented and available in all UIs. Core commands (SET, SHOW SETTINGS, HELP SET) work as documented. Settings files are automatically created in ~/.mbasic/settings.json (Linux/Mac) or %APPDATA%/mbasic/settings.json (Windows). Note: Some individual settings are still planned (see status notes for each setting).'

Then lists multiple settings as '**Status:** 🔧 PLANNED - Not yet implemented':
- interpreter.strict_mode
- interpreter.debug_mode
- ui.theme
- ui.font_size

This creates confusion about what 'implemented' means. INSTALL.md should clarify that the settings *system* is implemented but not all individual settings are available yet.

---

#### documentation_inconsistency

**Description:** TK_UI_QUICK_START.md references keyboard shortcuts for Tk UI but keyboard-shortcuts.md only documents Curses UI shortcuts

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md uses template notation like {{kbd:run_program}}, {{kbd:file_save}}, {{kbd:smart_insert}}, {{kbd:renumber}}, {{kbd:toggle_variables}}, {{kbd:toggle_stack}}, {{kbd:toggle_breakpoint}}, {{kbd:replace}}, {{kbd:file_open}}, {{kbd:file_new}}, {{kbd:help_topics}}, {{kbd:file_quit}} for Tk UI.

However, keyboard-shortcuts.md is titled 'MBASIC Curses UI Keyboard Shortcuts' and only documents Curses shortcuts like Ctrl+R (Run), Ctrl+V (Save), Ctrl+N (New), Ctrl+O (Open), Ctrl+H (Help), Ctrl+Q (Quit), Ctrl+B (Toggle breakpoint), Ctrl+W (Toggle variables), Ctrl+E (Renumber), Ctrl+T (Step statement), Ctrl+K (Step Line), Ctrl+C (Continue), Ctrl+X (Stop).

No separate keyboard-shortcuts.md file exists for Tk UI, despite TK_UI_QUICK_START.md referencing 'See [Tk Keyboard Shortcuts](keyboard-shortcuts.md)'.

---

#### documentation_inconsistency

**Description:** Conflicting information about Step/Continue/Stop keyboard shortcuts in Tk UI

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
TK_UI_QUICK_START.md states: 'Note: Step, Continue, and Stop are available via toolbar buttons or the Run menu (no keyboard shortcuts).'

However, UI_FEATURE_COMPARISON.md in the 'Debugging Shortcuts' table shows:
- Step: 'Menu/Toolbar' for Tk
- Continue: 'Menu/Toolbar' for Tk
- Stop: 'Esc' for Tk

This indicates Stop DOES have a keyboard shortcut (Esc) in Tk UI, contradicting the TK_UI_QUICK_START.md statement.

---

#### documentation_inconsistency

**Description:** Conflicting information about Curses UI resizable panels feature

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
UI_FEATURE_COMPARISON.md Feature Availability Matrix shows:
- Resizable panels for Curses: ❌ (Not available or not applicable)
- Notes: 'Curses: fixed 70/30 split (not user-resizable)'

This note indicates that Curses DOES have panels (with a fixed 70/30 split), but they are not user-resizable. The ❌ symbol suggests the feature is completely unavailable, but the note clarifies it exists in a limited form. This should perhaps be ⚠️ (Partially implemented) instead of ❌.

---

#### documentation_inconsistency

**Description:** Conflicting information about variable editing in Curses UI

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
UI_FEATURE_COMPARISON.md Feature Availability Matrix shows:
- Edit variables for Curses: ⚠️ (Partially implemented)
- Notes: 'CLI: immediate mode only'

However, in 'Detailed UI Descriptions' under Curses Limitations:
- 'Partial variable editing'

And in 'Feature Implementation Status' under 'Coming Soon':
- '⏳ Variable editing in Curses'

This is contradictory: the matrix shows it as partially implemented (⚠️), but 'Coming Soon' suggests it's not yet implemented (⏳). The status is unclear.

---

### 🟢 Low Severity

#### code_vs_comment_conflict

**Description:** PrintStatementNode.keyword_token field marked as legacy/unused but still present in dataclass

**Affected files:**
- `src/ast_nodes.py`

**Details:**
PrintStatementNode docstring states: 'Note: keyword_token fields are present in some statement nodes (PRINT, IF, FOR) but not others. These were intended for case-preserving keyword regeneration but are not currently used by position_serializer, which handles keyword case through apply_keyword_case_policy() and the KeywordCaseManager instead. The fields remain for potential future use and backward compatibility.'

However, the field is still defined as:
keyword_token: Optional[Token] = None  # Token for PRINT keyword (legacy, not currently used)

This creates maintenance burden and potential confusion. Similar issue exists in IfStatementNode (keyword_token, then_token, else_token) and ForStatementNode (keyword_token, to_token, step_token).

---

#### documentation_inconsistency

**Description:** CallStatementNode has unused 'arguments' field with incomplete explanation

**Affected files:**
- `src/ast_nodes.py`

**Details:**
CallStatementNode docstring states: 'Implementation Note: The 'arguments' field is currently unused (always empty list). It exists for potential future support of BASIC dialects that allow CALL with arguments (e.g., CALL ROUTINE(args)). Standard MBASIC 5.21 only accepts a single address expression in the 'target' field. Code traversing the AST can safely ignore the 'arguments' field for MBASIC 5.21 programs.'

This creates confusion because:
1. The field is defined but never used
2. It's unclear if the parser actually sets it to empty list or if it could be None
3. The comment says 'parser always sets to empty list' but the field type is List['ExpressionNode'] without a default value, suggesting it could be uninitialized

---

#### documentation_inconsistency

**Description:** RemarkStatementNode comment_type default value explanation is verbose and potentially confusing

**Affected files:**
- `src/ast_nodes.py`

**Details:**
RemarkStatementNode docstring states: 'Note: comment_type preserves the original comment syntax used in source code. The parser sets this to "REM", "REMARK", or "APOSTROPHE" based on input. Default value "REM" is used only when creating nodes programmatically (not from parsed source). When generating source text, this value determines which comment keyword appears.'

The explanation about when the default is used ('only when creating nodes programmatically') may be confusing because:
1. It's unclear why programmatic creation would default to "REM" instead of requiring explicit specification
2. The distinction between parser-created and programmatically-created nodes is not explained elsewhere in the file

---

#### documentation_inconsistency

**Description:** TypeInfo class has dual purpose that may be confusing

**Affected files:**
- `src/ast_nodes.py`

**Details:**
TypeInfo docstring states: 'This class serves two purposes:
1. Static helper methods for type conversions (from_suffix, from_token, etc.)
2. Compatibility layer: Class attributes (INTEGER, SINGLE, etc.) alias VarType enum values to support legacy code that used TypeInfo.INTEGER instead of VarType.INTEGER. This allows gradual migration without breaking existing code. Note: New code should use VarType enum directly.'

This creates confusion because:
1. It's unclear when the migration from TypeInfo to VarType should be complete
2. Having two ways to reference the same types (TypeInfo.INTEGER vs VarType.INTEGER) may lead to inconsistent code
3. The 'legacy code' comment suggests this is temporary, but there's no deprecation warning or timeline

---

#### documentation_inconsistency

**Description:** ChainStatementNode has complex optional parameters that may be confusing

**Affected files:**
- `src/ast_nodes.py`

**Details:**
ChainStatementNode has multiple optional fields (start_line, merge, all_flag, delete_range) with complex interactions:

Syntax examples:
'CHAIN "MENU"                    # Load and run MENU
CHAIN "PROG", 1000              # Start at line 1000
CHAIN "PROG", , ALL             # Pass all variables
CHAIN MERGE "OVERLAY"           # Merge as overlay
CHAIN MERGE "SUB", 1000, ALL, DELETE 100-200  # Full syntax'

The use of commas to skip parameters (e.g., 'CHAIN "PROG", , ALL') is not clearly explained in terms of how the parser handles this or how the AST represents it. It's unclear if start_line=None means 'not specified' or 'start at beginning'.

---

#### documentation_inconsistency

**Description:** RenumStatementNode parameter omission with commas is not clearly explained

**Affected files:**
- `src/ast_nodes.py`

**Details:**
RenumStatementNode docstring states: 'Parameters can be omitted using commas:
    RENUM 100,,20  - new_start=100, old_start=0 (default), increment=20
    RENUM ,50,20   - new_start=10 (default), old_start=50, increment=20'

However, the docstring doesn't explain:
1. What happens with RENUM ,,20 (all defaults except increment)?
2. How the parser distinguishes between 'omitted' (use default) and 'not provided' (None)?
3. The relationship between None values and the defaults mentioned (10, 0, 10)

---

#### code_vs_comment

**Description:** EOF function comment references execute_open() implementation details but doesn't verify consistency

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Comment at line 1000-1007 states:
'Implementation details:
- execute_open() in interpreter.py stores mode (\'I\', \'O\', \'A\', \'R\') in file_info[\'mode\']
- Mode \'I\' files are opened in binary mode (\'rb\'), allowing ^Z detection
- Text mode files (output \'O\', append \'A\') use standard Python EOF detection without ^Z
- See execute_open() in interpreter.py for file opening implementation (search for "execute_open")'

This references interpreter.py implementation but interpreter.py is not provided to verify the claims are accurate.

---

#### documentation_inconsistency

**Description:** Module docstring claims 'MBASIC 5.21 (CP/M era MBASIC-80)' but Version 5.21 note is ambiguous about what version number refers to

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line 2: 'Built-in functions for MBASIC 5.21 (CP/M era MBASIC-80).'
Lines 6-8: 'Note: Version 5.21 refers to BASIC-80 Reference Manual Version 5.21, which documents\nMicrosoft BASIC-80 as implemented for CP/M systems. This version was chosen as the\nreference implementation for maximum compatibility with classic BASIC programs.'

The note clarifies 5.21 is the manual version, not necessarily the BASIC version, but the module docstring says 'MBASIC 5.21' which could be misinterpreted as the BASIC version number.

---

#### code_vs_comment

**Description:** Comment about identifier case handling references runtime.py implementation details not provided

**Affected files:**
- `src/case_string_handler.py`

**Details:**
Lines 51-56: 'Identifiers (variable/function names) always preserve original case in display.\nUnlike keywords (which follow case_style policy), identifiers retain case as typed.\nThis matches MBASIC 5.21: identifiers are case-insensitive for matching but\npreserve display case. Case-insensitive matching happens at runtime (runtime.py\nuses lowercase keys via _resolve_variable_name() which calls name.lower()) and\nparsing (uses normalized forms), while this function only handles display formatting.'

References runtime.py and _resolve_variable_name() function but runtime.py is not provided to verify this claim.

---

#### code_vs_comment

**Description:** Sign behavior comment in parse_numeric_field uses inconsistent terminology

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Lines 234-237:
'Sign behavior:
- leading_sign: + at start, always adds + or - sign (reserves 1 char for sign)
- trailing_sign: + at end, always adds + or - sign (reserves 1 char for sign)
- trailing_minus_only: - at end, adds - for negative OR space for non-negative (reserves 1 char)'

The comment says 'always adds + or - sign' for leading_sign and trailing_sign, but later at line 421 the code checks 'is_negative' to determine which sign to add. The comment should say 'reserves space for + or - sign' to be more accurate.

---

#### code_vs_comment

**Description:** EOF function comment about ^Z detection references 'binary mode' but mode 'I' is described as 'input' not 'binary input'

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line 991: 'Note: For binary input files (OPEN statement mode \'I\'), respects ^Z (ASCII 26)'
Line 1002: '- Mode \'I\' files are opened in binary mode (\'rb\'), allowing ^Z detection'

The term 'binary input files' is used but mode 'I' typically means 'input' (sequential input) in BASIC, not 'binary'. The comment conflates 'binary mode' (Python file opening mode 'rb') with 'binary input files' (BASIC file type). This could be confusing.

---

#### documentation_inconsistency

**Description:** Duplicate two-letter error codes documented but potential ambiguity not addressed in implementation

**Affected files:**
- `src/error_codes.py`

**Details:**
error_codes.py documents duplicate two-letter codes:
"Specific duplicates (from MBASIC 5.21 specification):
- DD: code 10 ('Duplicate definition') and code 68 ('Device unavailable')
- DF: code 25 ('Device fault') and code 61 ('Disk full')
- CN: code 17 ('Can't continue') and code 69 ('Communication buffer overflow')

These duplicates exist in the original MBASIC 5.21 specification likely due to error codes
being added at different times during development (communication and device errors came later).
All error handling in this implementation uses numeric codes for lookups, so the duplicate
two-letter codes do not cause ambiguity in practice."

However, the get_error_message function (lines 88-94) returns both two_letter and message, and format_error (lines 97-108) uses the two_letter code in output. If any code tries to reverse-lookup by two-letter code, it would be ambiguous. The documentation claims no ambiguity but doesn't show how reverse lookups are prevented.

---

#### code_comment_conflict

**Description:** Comment about negative step handling says 'TODO' but code doesn't implement it

**Affected files:**
- `src/codegen_backend.py`

**Details:**
Line 283 in _generate_for method:
'# If step is negative, use >= instead of <=
# For now, assume positive step (TODO: handle negative steps)'

The code then unconditionally sets comp = '<=' regardless of step value. This is a known limitation documented in the comment, but it's unclear if this is intentional for the current version or a bug that needs fixing.

---

#### code_comment_conflict

**Description:** Docstring says 'Future: String support' but no indication if this is planned or aspirational

**Affected files:**
- `src/codegen_backend.py`

**Details:**
Lines 76-82 in Z88dkCBackend docstring:
"Supports:
- Integer variables (BASIC ! suffix maps to C int)
- FOR/NEXT loops
- PRINT statements for integers

Future:
- String support (requires runtime library)
- Arrays
- More complex expressions"

The 'Future' section lists features but doesn't indicate priority, timeline, or whether these are definite plans or just possibilities. This could mislead users about what to expect.

---

#### code_comment_conflict

**Description:** Comment says 'For now, assume positive step' but doesn't explain what happens with negative steps

**Affected files:**
- `src/codegen_backend.py`

**Details:**
Line 283-285:
'# Determine comparison operator based on step
if stmt.step_expr:
    # If step is negative, use >= instead of <=
    # For now, assume positive step (TODO: handle negative steps)
    comp = '<='
else:
    comp = '<='

The comment acknowledges negative steps need different handling (>= instead of <=) but then unconditionally uses <=. It's unclear if negative steps will cause incorrect behavior, infinite loops, or if they're validated elsewhere.

---

#### documentation_inconsistency

**Description:** Module docstring references 'IDEs or other development tools' but implementation is stderr-only

**Affected files:**
- `src/debug_logger.py`

**Details:**
Lines 3-8:
"Provides centralized debug output controlled by MBASIC_DEBUG environment variable.
When enabled, errors and debug info are output to stderr and returned as formatted
strings for UI display when debugging with IDEs or other development tools."

The implementation only writes to stderr (lines 77, 106). There's no special IDE integration or structured output format that would make it particularly useful for 'other development tools'. The documentation oversells the capability.

---

#### Code vs Comment conflict

**Description:** InMemoryFileHandle.flush() docstring describes behavior that differs from actual implementation

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
Docstring says: "Flush write buffers (no-op for in-memory files). Note: This calls StringIO/BytesIO flush() which are no-ops. Content is only saved to the virtual filesystem on close()."

Code implementation:
```
if hasattr(self.file_obj, 'flush'):
    self.file_obj.flush()
```

The docstring correctly states that StringIO/BytesIO flush() are no-ops and content is saved on close(). However, it also says "This calls StringIO/BytesIO flush()" but the code has a hasattr check suggesting uncertainty about whether flush() exists. StringIO and BytesIO always have flush() methods, so the hasattr check is unnecessary defensive programming that contradicts the confident statement in the docstring.

---

#### Documentation inconsistency

**Description:** Inconsistent terminology for storage location in SandboxedFileIO

**Affected files:**
- `src/file_io.py`

**Details:**
The docstring uses multiple terms for the same concept:
- "Python server memory"
- "server memory virtual filesystem"
- "in-memory virtual filesystem"
- "server memory"

While these all refer to the same thing, the inconsistent terminology could cause confusion. The phrase "Python server memory" appears in the class docstring but method docstrings use "server memory virtual filesystem".

---

#### Documentation inconsistency

**Description:** Redundant explanation of why list_files() is the only implemented method

**Affected files:**
- `src/file_io.py`

**Details:**
The SandboxedFileIO docstring explains twice why only list_files() is implemented:

1. In the "Implementation status" section for each method
2. In a separate paragraph starting with "Why only list_files() is implemented:"

The second explanation is more detailed but largely repeats information already stated, making the documentation unnecessarily verbose.

---

#### Code vs Comment conflict

**Description:** RealFileHandle.is_eof() comment says 'Try to read one byte' but reads one character in text mode

**Affected files:**
- `src/filesystem/real_fs.py`

**Details:**
Comment in is_eof() method:
```
# Try to read one byte
byte = self.file_obj.read(1)
```

In text mode (binary=False), read(1) reads one character, not one byte. A multi-byte UTF-8 character would be read as one unit. The variable is also named 'byte' which is misleading in text mode. The logic works correctly but the comment and variable name are inaccurate for text mode files.

---

#### Documentation inconsistency

**Description:** Inconsistent capitalization in docstring descriptions

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
Some method docstrings end with periods, others don't:
- "Check if file exists." (has period)
- "Delete a file (only user's files, not examples)." (has period)
- "Close all open files." (has period)
- "Get file size in bytes." (has period)

But the class docstring feature list uses no periods:
- "All files stored in memory (no disk access)"
- "Per-user isolation (user_id-based)"

Minor style inconsistency but affects documentation readability.

---

#### code_vs_documentation_inconsistency

**Description:** Help text says multi-statement lines are not supported, but code doesn't prevent them

**Affected files:**
- `src/immediate_executor.py`

**Details:**
In _show_help() method, LIMITATIONS section states:
"• Multi-statement lines (: separator) not supported"

However, the execute() method processes all statements in line_node.statements with a loop:
"for stmt in line_node.statements:
    interpreter.execute_statement(stmt)"

This would execute all statements on a line, including those separated by colons. There's no code that prevents or filters multi-statement lines. The help text was later updated to say "Multi-statement lines (: separator) are fully supported" which matches the implementation.

---

#### documentation_inconsistency

**Description:** Class docstring mentions state names that don't exist in implementation

**Affected files:**
- `src/immediate_executor.py`

**Details:**
The class docstring lists state names like 'idle', 'paused', 'at_breakpoint', 'done', 'error', 'waiting_for_input', 'running' and then says:

"State names used in documentation (not actual enum values):"

Then later says:
"Note: The actual implementation checks PC.is_running(), error_info, and input_prompt, not string state values."

This is confusing documentation - it introduces state names for explanation purposes but then clarifies they're not real. While technically not an inconsistency (it does clarify), it could be clearer by just describing the actual boolean checks without inventing state names.

---

#### code_vs_comment_conflict

**Description:** Comment about numbered line editing describes wrong method signature

**Affected files:**
- `src/immediate_executor.py`

**Details:**
In the numbered line editing section, comment states:
"# Add/update line - add_line expects complete line text with line number"

But the code calls:
"success, error = ui.program.add_line(line_num, complete_line)"

This shows add_line() takes TWO parameters (line_num and complete_line), but the comment only mentions it expects "complete line text with line number" (singular), which could be interpreted as a single parameter. The comment should clarify it takes both the line number as an integer AND the complete line text as separate parameters.

---

#### code_vs_comment

**Description:** Docstring claims EDIT subcommands are 'implemented subset' but doesn't specify which are missing

**Affected files:**
- `src/interactive.py`

**Details:**
Docstring at ~1040 says: 'Edit mode subcommands (implemented subset of MBASIC EDIT):' and lists commands like Space, D, C, I, X, H, L, E, Q, A, <CR>.

Then says: 'Note: Count prefixes ([n]D, [n]C) and search commands ([n]S, [n]K) are not yet implemented.'

However, the actual implementation in cmd_edit (~1090-1170) implements: Space, D, I, X, H, E, Q, L, A, C, and CR. The docstring should clarify that ALL listed commands ARE implemented, and only count prefixes and search commands are missing.

---

#### documentation_inconsistency

**Description:** Module docstring lists commands in different order than implementation

**Affected files:**
- `src/interactive.py`

**Details:**
Module docstring at top (~1-20) says:
'- Immediate mode statements: Most commands (RUN, LIST, SAVE, LOAD, NEW, MERGE, FILES, SYSTEM, DELETE, RENUM, CONT, CHAIN, etc.)'

But the execute_command method (~280) handles commands in order: AUTO, EDIT, HELP, then everything else goes to execute_immediate.

The docstring should clarify that AUTO, EDIT, HELP are 'Direct commands' (special-cased before parser), while RUN, LIST, SAVE, etc. are 'Immediate mode statements' (parsed as BASIC statements). The current wording mixes these categories.

---

#### code_vs_comment

**Description:** Comment about readline Ctrl+A binding is unclear about when the character is inserted

**Affected files:**
- `src/interactive.py`

**Details:**
In _setup_readline method (~120), comment says:
'Bind Ctrl+A to insert the character (ASCII 0x01) into the input line, overriding the default Ctrl+A (beginning-of-line) behavior. When the user presses Ctrl+A, readline's 'self-insert' action inserts the 0x01 character into the input string and returns it to the application. The start() method then detects this character and enters edit mode.'

This is technically correct but could be clearer. The comment should explain that readline's 'self-insert' inserts the literal Ctrl+A character (0x01) into the input buffer, which is then returned as part of the input string when the user presses Enter. The current wording 'returns it to the application' is ambiguous - it sounds like Ctrl+A immediately returns, but actually the user must press Enter first.

---

#### code_vs_comment_conflict

**Description:** Comment about bare except being 'acceptable' contradicts the detailed explanation of why it's needed

**Affected files:**
- `src/interactive.py`

**Details:**
In _read_char() around line 40:
# Fallback for non-TTY/piped input or any terminal errors.
# Bare except is acceptable here because we're degrading gracefully to basic read()
# on any error (AttributeError, termios.error, ImportError on Windows, etc.)

The comment lists specific exceptions (AttributeError, termios.error, ImportError) which suggests the developer knows what to catch, but uses bare except anyway. This is a code smell - if you know the exceptions, catch them specifically. The comment tries to justify the bare except but actually undermines it by showing specific exceptions could be caught.

---

#### documentation_inconsistency

**Description:** cmd_files() docstring mentions future enhancement for drive letter mapping but doesn't indicate priority or tracking

**Affected files:**
- `src/interactive.py`

**Details:**
In cmd_files() docstring around line 240:
'Future enhancement: Could add drive letter mapping.'

This is mentioned as a limitation but there's no indication if this is planned, tracked in an issue, or just a note. Documentation should clarify the status of 'future enhancements'.

---

#### code_vs_comment

**Description:** InterpreterState docstring lists execution order but doesn't match actual tick_pc() implementation order

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring at lines 44-51 lists:
"Internal execution order in tick_pc() (for developers understanding control flow):
1. pause_requested check - pauses if pause() was called
2. is_running() check - stops if PC is not running
3. break_requested check - handles Ctrl+C breaks
4. breakpoints check - pauses at breakpoints
5. trace output - displays [line] or [line.stmt] if TRON is active
6. statement execution - where input_prompt may be set
7. error handling - where error_info is set via exception handlers"

But tick_pc() implementation (lines 330-450) shows error handling happens in try/except blocks around statement execution, not as a separate step 7. The error_info is set in the exception handler at line 418 BEFORE invoking error handler, not after all other steps.

---

#### documentation_inconsistency

**Description:** Comment about version removal is imprecise about what was removed

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at lines 697-702 says:
"OLD EXECUTION METHODS REMOVED (version 1.0.299)
Note: The project has an internal implementation version (tracked in src/version.py)
which is separate from the MBASIC 5.21 language version being implemented.
Old methods: run_from_current(), _run_loop(), step_once() (removed in v1.0.299)
These used old current_line/next_line fields (also removed in v1.0.299)
Replaced by tick_pc() and PC-based execution"

The comment says "old current_line/next_line fields (also removed in v1.0.299)" but doesn't specify where these fields were located. Were they in InterpreterState? In Interpreter? The comment is vague about what data structure contained these removed fields.

---

#### code_vs_comment

**Description:** Comment about RETURN validation is slightly misleading about sentinel value

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at lines 1176-1186 explains:
"return_stmt is 0-indexed offset into statements array.
Valid range: 0 to len(statements) (inclusive).
- 0 to len(statements)-1: Normal statement positions
- len(statements): Special sentinel - GOSUB was last statement on line, so RETURN
  continues at next line. This value is valid because PC can point one past the
  last statement to indicate 'move to next line' (handled by statement_table.next_pc).
Values > len(statements) indicate the statement was deleted (validation error)."

The comment says "len(statements): Special sentinel" but doesn't clarify that this sentinel value is created by statement_table.next_pc() when advancing past the last statement, not explicitly set by GOSUB. The comment could be clearer that this is an automatic behavior of PC advancement, not a special GOSUB feature.

---

#### code_vs_comment

**Description:** current_statement_char_end docstring has redundant explanation

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring at lines 90-103 explains three cases for current_statement_char_end, but case 1 explanation is verbose:
"1. Next statement exists: Returns max(char_end, next_char_start - 1)
   - Handles string tokens where char_end may be too short
   - The colon separator is at next_char_start - 1
   - Most tokens have correct char_end >= next_char_start - 1"

The third bullet point ("Most tokens have correct char_end >= next_char_start - 1") is redundant with the first bullet ("Handles string tokens where char_end may be too short"). If most tokens are correct, then only string tokens need special handling, which is already stated.

---

#### code_vs_comment

**Description:** Comment about WEND timing says 'Pop the loop from the stack (after setting npc above, before WHILE re-executes)' but the pop happens after the comment explaining why

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1267: "Pop the loop from the stack (after setting npc above, before WHILE re-executes)."
Followed by multi-line comment explaining timing rationale.
Then actual pop at line ~1273: self.limits.pop_while_loop() and self.runtime.pop_while_loop()
The first comment makes it sound like the pop is immediate, but there's explanatory text between the comment and the actual pop. Minor clarity issue.

---

#### code_vs_comment

**Description:** INPUT statement comment says 'Currently always None since file input bypasses this path' but the code sets input_file_number

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1577: "Note: input_file_number is set to None for keyboard input and file# for file input. This allows the UI to distinguish between keyboard prompts (show in UI) and file input (internal, no prompt needed). Currently always None since file input bypasses this path."
Code at line ~1606: self.state.input_file_number = None  # None indicates keyboard input (not file)
The comment says 'Currently always None' which suggests the file input path (setting it to a file number) is never used. This makes the earlier explanation about distinguishing keyboard vs file input seem pointless. Either the feature is incomplete or the comment is misleading.

---

#### code_vs_comment

**Description:** DELETE statement comment says 'keeps variables, unlike NEW which clears both' but the note is redundant with the detailed explanation below

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1906: "DELETE           - Delete all lines (keeps variables, unlike NEW which clears both)"
Followed by detailed note at line ~1911: "Note: This implementation preserves variables and ALL runtime state when deleting lines. NEW clears both lines and variables (execute_new calls clear_variables/clear_arrays), while DELETE only removes lines from the program AST, leaving variables, open files, error handlers, and loop stacks intact."
The first comment already mentions the NEW vs DELETE distinction, making the detailed note somewhat redundant. Could be consolidated for clarity.

---

#### code_vs_comment

**Description:** execute_lset() and execute_rset() comments claim fallback is 'deliberate extension' but behavior is inconsistent with MBASIC 5.21

**Affected files:**
- `src/interpreter.py`

**Details:**
Comments (lines 2906-2913, 2943-2948): "Compatibility note: In strict MBASIC 5.21, LSET/RSET are only for field variables... This fallback is a deliberate extension that performs simple assignment without left-justification... This extension behavior allows LSET/RSET to work as simple assignment operators when not used with FIELD, which is intentional flexibility in this implementation, not a bug or incomplete feature."

This contradicts the stated goal of MBASIC 5.21 compatibility. The comment acknowledges deviation from MBASIC 5.21 behavior but frames it as intentional rather than a compatibility issue.

---

#### code_vs_comment

**Description:** evaluate_binaryop() string concatenation limit comment has overly detailed encoding discussion

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment (lines 3137-3147): "Enforce 255 character string limit for concatenation (MBASIC 5.21 compatibility)
Note: This check only applies to concatenation via PLUS operator.
Other string operations (MID$, INPUT) do not enforce this 255-char limit.
LSET/RSET have different limits: they enforce field width limits (defined by FIELD statement) rather than the 255-char concatenation limit.
Also note: len() counts characters. For ASCII and latin-1 (both single-byte encodings), character count equals byte count. Field buffers (LSET/RSET) use latin-1 encoding. This implementation assumes strings are ASCII/latin-1; Unicode strings with multi-byte characters may have len() < 255 but exceed 255 bytes. MBASIC 5.21 used single-byte encodings only."

The encoding discussion is excessive for a simple length check. The comment conflates character vs byte counting concerns that may not be relevant to the actual implementation.

---

#### documentation_inconsistency

**Description:** execute_midassignment() has redundant validation comment that duplicates code logic

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment (line 2976): "# Validate start position (must be within string: 0 <= start_idx < len)
# Note: start_idx == len(current_value) is considered out of bounds (can't start replacement past end)"

Code (lines 2977-2980):
if start_idx < 0 or start_idx >= len(current_value):
    # Start position is out of bounds - no replacement (MBASIC 5.21 behavior)
    return

The comment restates what the code clearly expresses. The 'Note' adds clarification but the main comment is redundant.

---

#### Documentation inconsistency

**Description:** Module docstring states GUIIOHandler is not exported due to dependencies, but gui.py shows it's a stub with no actual dependencies

**Affected files:**
- `src/iohandler/__init__.py`
- `src/iohandler/gui.py`

**Details:**
__init__.py says: "GUIIOHandler and WebIOHandler are not exported here because they have dependencies on their respective UI frameworks (tkinter, nicegui)."

But gui.py shows GUIIOHandler is actually a stub implementation with no external dependencies:
"class GUIIOHandler(IOHandler):
    '''GUI-based I/O handler stub.
    This is a minimal stub implementation showing how to create a custom I/O handler for GUI applications.'''

The stub only uses internal buffers and has no tkinter dependency.

---

#### Code vs Comment conflict

**Description:** Backward compatibility comment for print() method says it was renamed to avoid conflicts with Python's built-in, but both methods coexist

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Comment states:
    # Backward compatibility alias
    # This method was renamed from print() to output() to avoid conflicts with Python's
    # built-in print function. The print() alias is maintained for backward compatibility
    # with older code that may still call io_handler.print().
    def print(self, text="", end="\n"):

However, having a method named print() doesn't actually conflict with the built-in print() function in Python - they exist in different namespaces (instance method vs built-in function). The comment's reasoning is technically incorrect.

---

#### Code vs Comment conflict

**Description:** get_char() backward compatibility comment claims it preserves non-blocking behavior, but original implementation details are not visible

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Comment states:
    # Backward compatibility alias
    # This method was renamed from get_char() to input_char() for consistency with
    # the IOHandler base class interface. The get_char() alias is maintained for
    # backward compatibility with older code.
    def get_char(self):
        '''Deprecated: Use input_char() instead.
        This is a backward compatibility alias. New code should use input_char().
        Note: Always calls input_char(blocking=False) for non-blocking behavior.
        The original get_char() implementation was non-blocking, so this preserves
        that behavior for backward compatibility.'''
        return self.input_char(blocking=False)

The comment claims the original get_char() was non-blocking, but we cannot verify this from the provided code. Also, input_char() in web_io always returns "" immediately regardless of blocking parameter, so the distinction is meaningless.

---

#### Documentation inconsistency

**Description:** Inconsistent documentation about input() behavior regarding whitespace preservation

**Affected files:**
- `src/iohandler/console.py`

**Details:**
console.py input_line() docstring says:
        '''Input a complete line from console.
        For console, this delegates to self.input() (same behavior).
        Note: Python's input() strips only the trailing newline. Leading/trailing
        spaces are generally preserved, but terminal input behavior may vary across
        platforms. See input_line() documentation in base.py for details.'''

This states "Leading/trailing spaces are generally preserved" but then adds "terminal input behavior may vary across platforms" which creates uncertainty. The base.py documentation is more definitive about the limitation being a "platform limitation" rather than uncertain behavior.

---

#### Documentation inconsistency

**Description:** Module docstring references SimpleKeywordCase but doesn't provide import path or explain relationship clearly

**Affected files:**
- `src/keyword_case_manager.py`

**Details:**
Module docstring states:
"Note: This class provides advanced case policies (first_wins, preserve, error) via
CaseKeeperTable and is used by parser.py and position_serializer.py. For simpler
force-based policies in the lexer, see SimpleKeywordCase (src/simple_keyword_case.py)
which only supports force_lower, force_upper, and force_capitalize."

The note mentions SimpleKeywordCase but doesn't explain:
1. Why there are two separate keyword case systems
2. When to use which one
3. Whether they should be kept in sync
4. The architectural reason for the split

---

#### Code vs Documentation inconsistency

**Description:** input_char() docstring says blocking parameter is 'ignored' but implementation actually accepts it

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
web_io.py input_char() signature and docstring:
    def input_char(self, blocking=True):
        '''Get single character input (for INKEY$, INPUT$).
        Args:
            blocking: Accepted for interface compatibility but ignored in web UI.
        Returns:
            Empty string (character input not supported in web UI)
        Note: Character input is not supported in web UI. This method always returns
        an empty string immediately, regardless of the blocking parameter value.'''
        return ""

The parameter is accepted but has no effect on behavior. This is correct for interface compatibility but the wording 'ignored' could be clearer - it's accepted for signature compatibility but doesn't affect the return value.

---

#### code_vs_comment

**Description:** Comment about identifier case handling mentions two different fields but explanation could be clearer

**Affected files:**
- `src/lexer.py`

**Details:**
In read_identifier() method around line 280:
"# Preserve original case for display. Identifiers use the original_case field
# to store the exact case as typed. Keywords use original_case_keyword to store
# the case determined by the keyword case policy (see Token class in tokens.py)."

This comment is placed in the identifier section but discusses both identifiers and keywords. The Token class definition is not provided to verify these field names exist and are used as described.

---

#### code_vs_comment

**Description:** Comment about old BASIC preprocessing contradicts the actual implementation which does handle PRINT# special case

**Affected files:**
- `src/lexer.py`

**Details:**
Comment at line ~270 states:
"# NOTE: We do NOT handle old BASIC where keywords run together (NEXTI, FORI).
# This is properly-formed MBASIC 5.21 which requires spaces.
# Exception: PRINT# and similar file I/O keywords (handled above) support # without space.
# Other old BASIC syntax should be preprocessed with conversion scripts."

However, the code immediately above (lines ~250-265) DOES handle the special case of splitting PRINT# and similar constructs, which is a form of handling keywords that run together. The comment says 'Exception' but frames it as if no handling occurs, when in fact special handling code exists.

---

#### documentation_inconsistency

**Description:** Module docstring claims to be based on MBASIC-80 Reference Manual Version 5.21 but doesn't specify if all features from that manual are implemented

**Affected files:**
- `src/lexer.py`

**Details:**
Module docstring:
"Lexer for MBASIC 5.21 (CP/M era MBASIC-80)
Based on BASIC-80 Reference Manual Version 5.21

MBASIC 5.21 Extended BASIC features: This implementation enables Extended BASIC
features (e.g., periods in identifiers like "RECORD.FIELD") as they are part of MBASIC 5.21."

The phrase 'Based on' is ambiguous - it's unclear if this is a complete implementation of all lexer features from the manual or a partial implementation. The only specific feature mentioned is periods in identifiers.

---

#### code_vs_comment

**Description:** Comment about type suffix behavior may not match implementation for all cases

**Affected files:**
- `src/lexer.py`

**Details:**
In read_identifier() at line ~220:
"# Type suffix - terminates identifier (e.g., A$ reads as A$, not A$B)
ident += self.advance()
break"

The comment says type suffix terminates the identifier, and the code breaks. However, for the special case of # following file I/O keywords (lines ~240-265), the # is put back and re-tokenized separately. This creates an inconsistency: # sometimes terminates and is included (normal identifiers), and sometimes is excluded and re-tokenized (file I/O keywords). The comment doesn't acknowledge this dual behavior.

---

#### code_vs_comment

**Description:** at_end_of_line() docstring warns against using it for statement parsing, but parse_def_type_declaration() uses it

**Affected files:**
- `src/parser.py`

**Details:**
The at_end_of_line() docstring at lines 163-177 states:
"Note: Most statement parsing should use at_end_of_statement(), not this method.
Using at_end_of_line() in statement parsing can cause bugs where comments are
parsed as part of the statement instead of ending it."

However, parse_def_type_declaration() at line 267 uses at_end_of_line():
"while not self.at_end_of_line():"

This may be intentional since DEF statements are collected in a first pass and have special parsing rules, but the inconsistency between the warning and usage should be clarified or the method should use at_end_of_statement() instead.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for 'end of statement' checking

**Affected files:**
- `src/parser.py`

**Details:**
The parser uses multiple methods with overlapping purposes:
- at_end_of_line() (line 154): Checks for NEWLINE or EOF
- at_end_of_statement() (line 179): Checks for NEWLINE, EOF, COLON, or comment tokens
- at_end() (line 145): Checks for EOF or position >= len(tokens)
- at_end_of_tokens() (line 153): Checks if current() is None

The docstrings explain the differences, but the naming could be clearer. For example, at_end_of_line() doesn't actually check for 'end of line' in the logical sense (which would include colons), it checks for physical line breaks. This could confuse developers about which method to use.

---

#### code_vs_comment

**Description:** Comment about MID$ statement detection mentions error handling but implementation may not handle all cases

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines 717-720 states:
"# Catch lookahead failures during MID$ statement detection
# IndexError: if we run past end of tokens
# ParseError: if malformed syntax encountered during lookahead
# Position is restored below, so proper error will be reported later if needed"

The try-except block catches IndexError and ParseError, but the lookahead code uses methods like at_end_of_line() and match() which may not raise these exceptions in all failure cases. For example, if tokens are malformed in unexpected ways, the lookahead might succeed incorrectly rather than raising an exception. The comment implies comprehensive error handling that may not be fully implemented.

---

#### code_vs_comment

**Description:** parse_print() docstring shows optional comma after file number, but comment says MBASIC 5.21 typically requires it

**Affected files:**
- `src/parser.py`

**Details:**
Docstring at lines 1398-1403 shows syntax:
"PRINT #filenum, expr1       - Print to file"

But comment at lines 1411-1417 states:
"# Note: MBASIC 5.21 typically requires comma (PRINT #1, 'text').
# Our parser makes the comma optional for compatibility with BASIC variants
# that allow PRINT #1; 'text' or PRINT #1 'text'."

This is internally consistent (docstring shows comma, comment explains it's required in MBASIC but optional in parser), but could be clearer about whether this is a deliberate deviation from MBASIC 5.21 spec or an attempt to be more permissive.

---

#### code_vs_comment

**Description:** Comment about MID$ tokenization uses inconsistent terminology

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line ~1893 states: 'Note: The lexer tokenizes 'MID$' in source as TokenType.MID (the $ is part of the keyword, not a separate token). The token type name is 'MID', not 'MID$'.'

This comment is technically correct but potentially confusing because it emphasizes that the token type is 'MID' not 'MID$', yet the actual source keyword is 'MID$'. The comment could be clearer about whether the dollar sign is stripped during lexing or if TokenType.MID represents the full 'MID$' keyword.

---

#### code_vs_comment

**Description:** Comment about INPUT semicolon behavior is verbose and potentially confusing

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines ~1115-1122 explains: 'Note: In MBASIC 5.21, the separator after prompt affects "?" display:
- INPUT "Name"; X  displays "Name? " (semicolon AFTER prompt shows '?')
- INPUT "Name", X  displays "Name " (comma AFTER prompt suppresses '?')
Different behavior: INPUT; (semicolon IMMEDIATELY after INPUT keyword, no prompt) suppresses the default '?' prompt entirely (tracked by suppress_question flag above).'

This comment describes two different semicolon behaviors (after prompt vs after INPUT keyword) which could be confusing. The distinction between 'semicolon after prompt' and 'semicolon after INPUT keyword' is important but the comment structure makes it easy to conflate the two cases.

---

#### code_vs_comment

**Description:** Comment about DEFTYPE behavior describes implementation detail that may not be obvious

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line ~1928 states: 'Note: This method always updates def_type_map during parsing. The type map is shared across all statements (both in interactive mode where statements are parsed one at a time, and in batch mode where the entire program is parsed). The type map affects variable type inference throughout the program. The AST node is created for program serialization/documentation.'

This comment describes the implementation but doesn't explain why the type map is updated during parsing rather than during execution. This could be confusing because most BASIC statements have their effects during execution, not parsing. The comment should clarify whether this is a design decision or a limitation.

---

#### code_inconsistency

**Description:** Inconsistent handling of type suffixes in FOR and NEXT statements

**Affected files:**
- `src/parser.py`

**Details:**
In parse_for() (line ~1645), when no explicit type suffix is found, the code checks def_type_map and assigns a suffix:
'if not type_suffix:
    first_letter = var_name[0].lower()
    if first_letter in self.def_type_map:
        var_type = self.def_type_map[first_letter]
        # Determine suffix based on DEF type'

The same logic appears in parse_next() (line ~1697). However, in parse_dim() (line ~1774), the code modifies the name itself by appending the suffix:
'if name and name[-1] not in "$%!#":
    # No explicit suffix - check DEF type map
    first_letter = name[0].lower()
    if first_letter in self.def_type_map:
        var_type = self.def_type_map[first_letter]
        # Append appropriate suffix based on DEF type
        if var_type == TypeInfo.STRING:
            name = name + "$"'

This inconsistency (modifying type_suffix variable vs modifying name variable) could lead to bugs or confusion.

---

#### code_vs_comment

**Description:** parse_call() docstring claims full support for extended syntax but implementation may not handle all cases

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states: "Note: MBASIC 5.21 primarily uses the simple numeric address form, but this parser fully supports both forms for broader compatibility."

The implementation attempts to handle both forms by checking if target is VariableNode with subscripts or FunctionCallNode, but the comment claims "full support" which may be overstated. The parser converts these to CallStatementNode but doesn't validate that the extended syntax is semantically correct for MBASIC 5.21.

---

#### code_vs_comment

**Description:** parse_data() docstring mentions line numbers but implementation treats them as unquoted strings

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states: "Line numbers (e.g., DATA 100 200) are treated as part of unquoted strings."

Implementation has:
```
elif tok.type == TokenType.LINE_NUMBER:
    string_parts.append(str(tok.value))
    self.advance()
```

This is consistent, but the docstring could be clearer that LINE_NUMBER tokens are converted to strings and included in the unquoted string value, not treated as numeric data items.

---

#### code_vs_comment

**Description:** parse_common() docstring says 'just a marker' but doesn't explain what happens to array indicator

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states: "The empty parentheses () indicate an array variable (all elements shared). This is just a marker - no subscripts are specified or stored."

The implementation consumes the parentheses but stores only the variable name as a string:
```
if self.match(TokenType.LPAREN):
    self.advance()
    if not self.match(TokenType.RPAREN):
        raise ParseError(...)
    self.advance()
variables.append(var_name)
```

The docstring could be clearer that the array indicator is completely discarded and not represented in the AST - there's no way to distinguish between 'COMMON A' and 'COMMON A()' in the resulting CommonStatementNode.

---

#### code_vs_comment

**Description:** apply_keyword_case_policy docstring says keyword should be normalized lowercase but also says it can handle mixed case

**Affected files:**
- `src/position_serializer.py`

**Details:**
Function docstring states:
    Args:
        keyword: The keyword to transform (should be normalized lowercase for consistency,
                 but first_wins policy can handle mixed case by normalizing internally)

This is contradictory - it says 'should be normalized lowercase' but then says 'can handle mixed case'. The note at the end clarifies:
    Note: While this function can handle mixed-case input (first_wins policy normalizes
    to lowercase internally for lookup), callers should normalize to lowercase before
    calling to ensure consistent behavior with emit_keyword() and avoid case-sensitivity
    issues in non-first_wins policies.

But the initial Args description is still confusing.

---

#### documentation_inconsistency

**Description:** serialize_let_statement docstring says 'always outputs without LET keyword' but doesn't mention this is intentional data loss

**Affected files:**
- `src/position_serializer.py`

**Details:**
The docstring states:
        Design decision: LetStatementNode represents both explicit LET statements and implicit
        assignments in the AST. This serializer intentionally ALWAYS outputs the implicit
        assignment form (A=5) without the LET keyword, regardless of the original source.

        Note: This means round-trip serialization will convert "LET A=5" to "A=5".

This is clearly documented as intentional, but the module-level docstring says:
        Key principle: AST is the single source of truth for CONTENT (what tokens exist
        and their values). Original token positions are HINTS for formatting (where to
        place tokens). When positions conflict with content, content wins and a
        PositionConflict is recorded.

The LET keyword case is different - it's not a position conflict, it's intentional content loss. This should be mentioned in the module-level docstring as an exception to the 'AST is source of truth for content' principle.

---

#### code_vs_comment

**Description:** PC.__repr__ shows 'HALTED' state but PC.halted() factory creates PC with stop_reason='END'

**Affected files:**
- `src/pc.py`

**Details:**
In PC.__repr__:
        if self.line is None:
            if self.stop_reason:
                return f"PC(STOPPED:{self.stop_reason})"
            return "PC(HALTED)"

But in PC.halted() factory:
    @classmethod
    def halted(cls):
        """Create a halted PC (not in program, fell off end)."""
        return cls(line=None, statement=0, stop_reason="END", error=None)

So halted() creates a PC with stop_reason="END", which means __repr__ would show "PC(STOPPED:END)" not "PC(HALTED)". The "PC(HALTED)" case in __repr__ would only occur if line=None and stop_reason=None, which is not created by any factory method.

---

#### Code vs Comment conflict

**Description:** Comment about array indexing convention may be misleading about what it's documenting

**Affected files:**
- `src/resource_limits.py`

**Details:**
In check_array_allocation(), there's a comment:
'# Note: DIM A(N) creates N+1 elements (0 to N) in MBASIC 5.21
# We replicate this convention here for accurate size calculation (limit checking must match
# the actual allocation size). The execute_dim() method in interpreter.py uses the same
# convention when creating arrays, ensuring consistency between limit checks and allocation.'

The comment says 'We replicate this convention here' but the code that follows is just calculating size for limit checking, not actually creating the array. The comment might be clearer if it said 'We account for this convention here' or 'We use this convention in our size calculation'. The phrase 'replicate this convention' suggests the code is implementing the indexing behavior, when it's actually just calculating the memory impact of that behavior.

---

#### Documentation inconsistency

**Description:** Module docstrings have reciprocal references but use slightly different wording

**Affected files:**
- `src/resource_limits.py`
- `src/resource_locator.py`

**Details:**
resource_limits.py says: 'Note: This is distinct from resource_locator.py which finds package data files.'

resource_locator.py says: 'Note: This is distinct from resource_limits.py which enforces runtime execution limits.'

The first uses 'finds package data files' while the second uses 'enforces runtime execution limits'. For consistency, they should use parallel phrasing, such as:
- resource_limits.py: 'enforces runtime execution limits'
- resource_locator.py: 'locates package data files'

Or both could use 'provides' or 'handles'. The current wording is not wrong but lacks parallelism.

---

#### Code vs Documentation inconsistency

**Description:** Docstring says 'Different UIs can create appropriate limit configurations' but only shows three preset functions

**Affected files:**
- `src/resource_limits.py`

**Details:**
The module docstring states: 'Different UIs can create appropriate limit configurations (web UI uses tight limits, local UIs use generous limits).'

The usage examples show:
- create_web_limits() for Web UI
- create_local_limits() for Local UI
- create_unlimited_limits() for Testing/Development

However, the module only provides these three preset functions. If 'different UIs' need to create 'appropriate limit configurations', the documentation should either:
1. Clarify that UIs should use one of these three presets
2. Show how UIs can create custom ResourceLimits instances with custom parameters
3. Explain when/why a UI would need something other than these three presets

The current wording suggests more flexibility than is demonstrated.

---

#### documentation_inconsistency

**Description:** Inconsistent parameter documentation for token in get_variable()

**Affected files:**
- `src/runtime.py`

**Details:**
The get_variable() docstring describes token parameter with detailed fallback behavior:
"token: REQUIRED - A token object must be provided (ValueError raised if None).
       The token enables source location tracking for this variable access.

       Token attributes have fallback behavior:
       - token.line: Used for tracking if present, otherwise falls back to self.pc.line_num
       - token.position: Used for tracking if present, otherwise falls back to None

       Why token object is required: Even with attribute fallbacks, the token object
       itself is mandatory to distinguish intentional program execution (which must
       provide a token) from debugging/inspection (which should use get_variable_for_debugger())."

However, the actual tracking code uses:
'line': getattr(token, 'line', self.pc.line_num if self.pc and not self.pc.halted() else None),
'position': getattr(token, 'position', None),

The fallback for token.line is complex (self.pc.line_num if self.pc and not self.pc.halted() else None), but the documentation simplifies it to 'falls back to self.pc.line_num'. The documentation doesn't mention the halted() check or the None fallback.

---

#### code_vs_comment

**Description:** Incomplete docstring for get_all_variables() - truncated mid-sentence

**Affected files:**
- `src/runtime.py`

**Details:**
The get_all_variables() method docstring is incomplete:
"Export all variables with structured type information.

Returns detailed information about each variable including:
- Base name (without type suffix)
- Type suffix character
- For scalars: current value
- For arrays: dimensions and base
- Access tracking: last_read and last_write info

Returns:
    list: List of dictionaries with variable information
          Each dict contains:
          - 'name': Base name (e.g., 'x', 'counter', 'msg')

The docstring ends abruptly after listing only the 'name' field, but the description promises information about type suffix, value, dimensions, and access tracking. The complete list of dict fields is missing.

---

#### Documentation inconsistency

**Description:** Redundant field documentation acknowledges redundancy but doesn't explain why it exists

**Affected files:**
- `src/runtime.py`

**Details:**
In get_execution_stack() docstring for GOSUB:

"Note: 'from_line' is redundant with 'return_line' - both contain the same value (the line number to return to after RETURN). The 'from_line' field exists for backward compatibility with code that expects it. Use 'return_line' for new code as it more clearly indicates the field's purpose."

However, in the actual code implementation:
"'from_line': entry.get('return_line', 0),  # Line to return to"

The comment says 'Line to return to' which is the same as return_line's purpose. The documentation could be clearer about what 'from_line' originally meant (perhaps 'line where GOSUB was called from') vs what it actually contains now (return address).

---

#### Code vs Documentation inconsistency

**Description:** Inconsistent statement offset terminology in examples

**Affected files:**
- `src/runtime.py`

**Details:**
In set_breakpoint() docstring:
"set_breakpoint(100, 2)        # Statement-level (line 100, statement offset 2 = 3rd statement)"

In get_gosub_stack() docstring:
"Note: stmt_offset uses 0-based indexing (offset 0 = 1st statement, offset 1 = 2nd statement, etc.)"

Both correctly describe 0-based indexing, but the set_breakpoint example says 'offset 2 = 3rd statement' while get_gosub_stack says 'offset 1 = 2nd statement'. Both are mathematically correct (offset N = (N+1)th statement), but the inconsistent phrasing could confuse readers. One uses 'offset 2 = 3rd' and the other uses 'offset 1 = 2nd' as examples.

---

#### Documentation inconsistency

**Description:** Deprecation notice has inconsistent date format

**Affected files:**
- `src/runtime.py`

**Details:**
In get_loop_stack() docstring:
"Deprecated since: 2025-10-25 (commit cda25c84)
Will be removed: No earlier than 2026-01-01"

The date '2025-10-25' uses format YYYY-MM-DD (October 25, 2025), but this appears to be a future date which is logically inconsistent with marking something as already deprecated. This is likely a typo and should be '2024-10-25' or the deprecation notice is premature.

---

#### code_vs_comment

**Description:** SettingsManager.load() docstring describes flexible format handling but implementation doesn't actually handle format detection

**Affected files:**
- `src/settings.py`

**Details:**
src/settings.py lines 98-106:
Docstring states: "The backend determines the format (flat vs nested) based on what was saved. Internal representation is flexible: _get_from_dict() handles both flat keys like 'editor.auto_number' and nested dicts like {'editor': {'auto_number': True}}."

However, the load() implementation (lines 107-109) just assigns backend results directly:
  self.global_settings = self.backend.load_global()
  self.project_settings = self.backend.load_project()

No format detection or conversion happens in load(). The backend returns flat dicts (from JSON), and _get_from_dict() handles both formats during retrieval, but load() itself doesn't do format handling. The comment overstates what load() does.

---

#### code_vs_comment

**Description:** SimpleKeywordCase.register_keyword() docstring says line_num and column are 'unused' but also 'required for KeywordCaseManager compatibility'

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
src/simple_keyword_case.py lines 62-65:
"Maintains signature compatibility with KeywordCaseManager.register_keyword() which uses line_num and column for advanced policies (first_wins, preserve, error). SimpleKeywordCase only supports force-based policies, so these parameters are unused."

Then lines 68-70:
"line_num: Line number (unused - required for KeywordCaseManager compatibility)
column: Column (unused - required for KeywordCaseManager compatibility)"

This is self-contradictory phrasing. Parameters can't be both 'unused' and 'required'. Should say 'unused by SimpleKeywordCase but required for API compatibility' or 'accepted but ignored'.

---

#### documentation_inconsistency

**Description:** Comment claims 'editor.tab_size setting not included' but doesn't explain why tab_size would be irrelevant when BASIC programs can contain whitespace

**Affected files:**
- `src/settings_definitions.py`

**Details:**
src/settings_definitions.py lines 119-121:
"# Note: editor.tab_size setting not included - BASIC uses line numbers for program structure, not indentation, so tab size is not a meaningful setting for BASIC source code"

This reasoning is questionable. While BASIC doesn't use indentation for structure, tab size still affects how code is displayed/edited. The comment justifies exclusion based on structural irrelevance, but tab size affects visual presentation regardless of whether indentation has semantic meaning. This may be intentional design decision but the justification is weak.

---

#### code_vs_comment

**Description:** SettingsManager class docstring describes file-level settings as 'PARTIALLY IMPLEMENTED' and 'RESERVED FOR FUTURE USE' but implementation is actually complete for in-memory usage

**Affected files:**
- `src/settings.py`

**Details:**
src/settings.py lines 28-34:
"Note: File-level settings (per-file settings) are PARTIALLY IMPLEMENTED. The file_settings dict exists and can be set programmatically via set(key, value, scope=SettingScope.FILE), but there is NO persistence layer (load() doesn't populate it, save() doesn't persist it) and NO UI/command interface to manage them. These are temporary in-memory settings only, reserved for future use when a persistence layer is added."

The implementation is actually FULLY functional for in-memory use - get() checks file_settings first (line 195), set() can write to it (line 249), reset_to_defaults() can clear it (line 327). The only missing piece is persistence. Calling it 'PARTIALLY IMPLEMENTED' is misleading - it's 'FULLY IMPLEMENTED except for persistence'. The comment conflates 'implementation' with 'persistence'.

---

#### Documentation inconsistency

**Description:** Curses UI has separate Step Line and Step Statement commands, CLI only has STEP

**Affected files:**
- `src/ui/cli_debug.py`
- `src/ui/curses_keybindings.json`

**Details:**
curses_keybindings.json defines two separate stepping commands:
- "step_line" (Ctrl+K): "Step Line (execute all statements on current line)"
- "step" (Ctrl+T): "Step statement (execute one statement)"

cli_debug.py cmd_step() docstring acknowledges this:
"This implements statement-level stepping similar to the curses UI 'Step Statement' command (Ctrl+T). The curses UI also has a separate 'Step Line' command (Ctrl+K) which is not available in the CLI."

This is documented but represents a feature disparity between UIs that users should be aware of.

---

#### Code vs Comment conflict

**Description:** get_additional_keybindings() comment says Ctrl+A is overridden but doesn't explain the override behavior

**Affected files:**
- `src/ui/cli.py`

**Details:**
Comment in get_additional_keybindings() states:
"# Note: Ctrl+A is overridden by MBASIC to trigger edit mode"

However, cli_keybindings.json shows:
"edit": {
  "keys": ["Ctrl+A"],
  "primary": "Ctrl+A",
  "description": "Edit line (last line or Ctrl+A followed by line number)"
}

The comment suggests Ctrl+A is completely overridden, but the keybinding description shows it has MBASIC-specific behavior (edit mode) rather than readline's default (move to start of line). The comment could be clearer about what 'overridden' means in this context.

---

#### Documentation inconsistency

**Description:** Readline keybindings documentation split between code comment and JSON file

**Affected files:**
- `src/ui/cli.py`
- `src/ui/cli_keybindings.json`

**Details:**
get_additional_keybindings() function in cli.py documents readline keybindings (Ctrl+E, Ctrl+K, etc.) with explanation:
"NOTE: These keybindings are intentionally NOT in cli_keybindings.json because:
1. They're provided by readline, not the MBASIC keybinding system
2. They're only available when readline is installed (platform-dependent)
3. Users can't customize them through MBASIC settings
4. They follow standard readline/Emacs conventions"

However, this creates a documentation split where some keybindings are in JSON and others are in Python code. Users looking at cli_keybindings.json won't see the complete picture. The function returns an empty dict if readline is unavailable, but the documentation in the function body is always present in the source.

---

#### Code vs Comment conflict

**Description:** Comment about stripping 'force_' prefix uses hasattr check for removeprefix method

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
In _create_setting_widget() method:
```python
# Strip 'force_' prefix from beginning for cleaner display
display_label = choice.removeprefix('force_') if hasattr(str, 'removeprefix') else (choice[6:] if choice.startswith('force_') else choice)
```

The comment says it strips the prefix for cleaner display, and the code has a fallback for Python versions without removeprefix (added in 3.9). However, this creates a subtle inconsistency: the code stores the actual value with prefix in rb._actual_value but displays without prefix. Later code in _on_reset() has a comment explaining this:
"# Note: Compares actual value (stored in _actual_value) not display label
# since display labels have 'force_' prefix stripped"

The initial comment doesn't explain why this stripping is necessary or that the actual value is preserved separately.

---

#### Code vs Documentation inconsistency

**Description:** UIBackend docstring mentions WebBackend as future/potential but doesn't mention CursesBackend

**Affected files:**
- `src/ui/base.py`

**Details:**
base.py UIBackend docstring states:
"Different UIs can implement this interface:
- CLIBackend: Terminal-based REPL (interactive command mode)
- CursesBackend: Full-screen terminal UI with visual editor
- TkBackend: Desktop GUI using Tkinter

Future/potential backend types (not yet implemented):
- WebBackend: Browser-based interface"

However, curses_keybindings.json and curses_settings_widget.py clearly show that CursesBackend is implemented, not just planned. The docstring should list CursesBackend as implemented, not as a future type. Additionally, TkBackend is listed as if it exists, but no TkBackend code is provided in the files.

---

#### code_vs_comment

**Description:** Comment about default target_column=7 is outdated due to variable-width line numbers

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line ~1005 in keypress() docstring: 'Note: Methods like _sort_and_position_line use a default target_column of 7,
which assumes typical line numbers (status=1 char + number=5 digits + space=1 char).
This is an approximation since line numbers have variable width.'

Line ~1850 _sort_and_position_line signature: 'def _sort_and_position_line(self, lines, current_line_index, target_column=7):'

The comment explains target_column=7 assumes 5-digit line numbers, but the class docstring (lines ~570-580) and multiple other comments emphasize that line numbers are variable-width with no padding. The default of 7 is arbitrary and the comment's justification is misleading since the system explicitly doesn't use fixed-width formatting.

---

#### code_vs_comment

**Description:** Comment about BASIC statements starting with digits contradicts paste handling logic

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line ~1780 in _parse_line_numbers(): 'In this context, we assume lines starting with digits are numbered program lines (e.g., "10 PRINT").
Note: While BASIC statements can start with digits (numeric expressions), when pasting
program code, lines starting with digits are conventionally numbered program lines.'

The code at line ~1785 unconditionally treats any line starting with a digit as a numbered program line and reformats it. However, the comment acknowledges that BASIC statements can start with digits (like numeric expressions or variable assignments). This means pasting code like 'X=5' on a line would work, but pasting '5+X' would be incorrectly reformatted as line number 5 with code '+X'. The comment tries to justify this but the logic is still inconsistent with valid BASIC syntax.

---

#### documentation_inconsistency

**Description:** Module docstring describes features not visible in provided code

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Lines 1-7 module docstring: 'Curses UI backend using urwid.

This module provides a full-screen terminal UI for MBASIC using the urwid library.
It provides an editor, output window, and menu system.'

The provided code only shows ProgramEditorWidget and helper classes (TopLeftBox, InputDialog, YesNoDialog, SelectableText). The main CursesBackend class, output window implementation, and menu system are not included in the provided code excerpt. This makes it impossible to verify if the module docstring accurately describes the complete implementation.

---

#### code_vs_comment

**Description:** Comment says immediate_io is recreated in start() but the code shows it's created in both __init__ and start()

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~245 says:
# 2. immediate_io (OutputCapturingIOHandler) - Used for immediate mode commands
#    Created here temporarily, then RECREATED in start() with fresh instance each time

But the code shows:
1. In __init__ (line ~256): immediate_io = OutputCapturingIOHandler()
2. In start() (line ~336): immediate_io = OutputCapturingIOHandler()

The comment implies the first creation is temporary/throwaway, but doesn't explain why it's needed at all in __init__ if it will be recreated. The Interpreter is initialized with this temporary immediate_io, then the IO handler is replaced during execution.

---

#### code_vs_comment

**Description:** Comment about toolbar being removed contradicts the existence of menu_bar widget

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~421 says:
# Toolbar removed from UI layout - use Ctrl+U interactive menu bar instead for keyboard navigation

But the code immediately before (line ~420) creates:
self.menu_bar = InteractiveMenuBar(self)

And the menu_bar is added to the UI layout in the Pile widget (line ~467).

The comment seems to refer to a different toolbar that was removed, but the menu_bar is still present and functional.

---

#### documentation_inconsistency

**Description:** Docstring for _save_editor_to_program says it returns True/False but doesn't document what the return value means

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Docstring at line ~295:
"""Save editor content back to program.

Parses lines from editor and saves them to program manager.
Returns True if successful, False if errors occurred.
"""

The docstring says it returns True/False but doesn't explain:
1. What happens to the errors when False is returned
2. Whether the program is partially saved or not saved at all on errors
3. The errors are stored in self.editor.errors but this isn't mentioned

---

#### code_vs_comment

**Description:** Comment describes statement-level precision for GOSUB but uses ambiguous terminology

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_stack_window() at line ~1007:
Comment: "# Show statement-level precision for GOSUB return address
# return_stmt is statement offset (0-based index): 0 = first statement, 1 = second, etc."

Code displays: f"GOSUB from line {entry['from_line']}.{return_stmt}"

The comment correctly describes return_stmt as a 0-based statement offset, but the display format 'line.stmt' might be confusing to users who expect 1-based indexing for statements (similar to how line numbers work). This is a minor documentation clarity issue rather than a bug.

---

#### code_vs_comment

**Description:** Comment about immediate mode status updates is inconsistent with actual behavior

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple locations have comments about when immediate mode status is updated:

1. Line ~1073: "# Don't update immediate status here - error is displayed in output"
2. Line ~1084: "# Don't update immediate status here - error is in output"
3. Line ~1127: "# Immediate mode status remains disabled during execution - program output shows in output window"
4. Line ~1165: "self._update_immediate_status()" (called after error)
5. Line ~1177: "self._update_immediate_status()" (called after pause)
6. Line ~1182: "self._update_immediate_status()" (called after halt)

The comments suggest immediate status should NOT be updated during errors, but the code consistently calls _update_immediate_status() after errors, pauses, and halts. This indicates the comments are outdated or the pattern has changed.

---

#### code_vs_comment

**Description:** Comment about PC setting timing contradicts itself

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _setup_program() at line ~1095:
"# If start_line is specified (e.g., RUN 100), set PC to that line
# This must happen AFTER interpreter.start() because start() calls setup()
# which resets PC to the first line in the program. By setting PC here,
# we override that default and begin execution at the requested line."

The comment correctly describes the timing requirement, but the phrase 'This must happen AFTER' followed by 'By setting PC here' is slightly confusing because 'here' refers to the location in code (which is indeed after start()), not a temporal sequence. Minor clarity issue.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate says 'Immediate mode status remains disabled during execution' but the code doesn't explicitly disable it

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1350: '# Immediate mode status remains disabled during execution - program output shows in output window'

The code sets self.running = True but doesn't explicitly call any method to disable immediate mode status. The status update happens elsewhere via _update_immediate_status() which checks can_execute_immediate().

---

#### code_vs_comment

**Description:** Comment in _sync_program_to_editor says 'This is used when a program is loaded externally (e.g., from command line) before the UI starts' but the function is also called after loading files in the UI

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1200: 'Sync program from ProgramManager to editor display.

This is used when a program is loaded externally (e.g., from command line)
before the UI starts, and we need to populate the editor.'

But the function is called in _load_program_file at line ~1220, which is used during UI operation, not just at startup. The comment is incomplete.

---

#### code_vs_comment_conflict

**Description:** Comment describes _expand_kbd parameter format but doesn't mention the actual implementation handles both formats in the same parameter

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at lines ~107-115 states:
"Args:
    key_name: Name of key action, optionally with UI specifier.
             Formats:
             - 'action' - searches current UI (e.g., 'help', 'save', 'run')
             - 'action:ui' - searches specific UI (e.g., 'save:curses', 'run:tk')"

But the docstring example at lines ~117-119 shows:
"Example:
    _expand_kbd('help') searches current UI for action 'help'
    _expand_kbd('save:curses') searches Curses UI for action 'save'"

The format description uses 'action:ui' but the example shows 'save:curses' which reverses the order. The code at line ~126 shows:
if ':' in key_name:
    action, ui = key_name.split(':', 1)

So the format is actually 'action:ui' as stated, but the example 'save:curses' makes it look like 'action:ui_name' where 'save' is the action and 'curses' is the UI, which is correct. This is actually consistent, just potentially confusing.

---

#### documentation_inconsistency

**Description:** Docstring example format inconsistency in macro syntax

**Affected files:**
- `src/ui/help_macros.py`

**Details:**
Module docstring at lines ~7-11 shows:
"Examples:
  {{kbd:help}} → looks up 'help' action in current UI's keybindings and returns
                  the primary keybinding for that action
  {{kbd:save:curses}} → looks up 'save' action in Curses UI specifically
  {{version}} → MBASIC version string"

The example {{kbd:save:curses}} suggests a three-part format (macro:action:ui), but the actual implementation and _expand_kbd docstring show the format is {{kbd:action}} or {{kbd:action:ui}} where the macro name is 'kbd' and the argument is 'action' or 'action:ui'.

The example should be {{kbd:save:curses}} which is parsed as macro='kbd', arg='save:curses', then arg is split into action='save', ui='curses'. The example is correct but could be clearer about the parsing.

---

#### code_vs_comment_conflict

**Description:** Comment describes link format matching but implementation uses different regex pattern than described

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at lines ~234-240 states:
"Links are marked with [text] or [text](url) in the rendered output. This method finds ALL such patterns for display/navigation using regex r'\\[([^\\]]+)\\](?:\\([^)]+\\))?', which matches both formats. The renderer's links list is used for target mapping when following links."

The regex pattern in the comment is escaped for docstring (\\[ becomes \[), but the actual pattern at line ~253 is:
link_pattern = r'\[([^\]]+)\](?:\([^)]+\))?'

The comment's regex representation is correct for a docstring but could be confusing. The actual pattern is correct and matches the description.

---

#### Code vs Comment conflict

**Description:** Comment says CONTINUE_KEY is for 'Go to line' in editor and 'Continue execution (Go)' in debugger, but JSON key is 'goto_line' which doesn't clearly indicate dual purpose

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

The comment explains dual purpose but this may not be documented in the JSON schema or help text.

---

#### Code vs Comment conflict

**Description:** Comment says STOP_KEY is 'Shown in debugger context in the Debugger category' implying it's NOT in KEYBINDINGS_BY_CATEGORY, but it IS present in the 'Debugger (when program running)' category

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Line 221 comment:
# - STOP_KEY (Ctrl+X) - Shown in debugger context in the Debugger category

But line 245 in KEYBINDINGS_BY_CATEGORY:
'Debugger (when program running)': [
    ...
    (key_to_display(STOP_KEY), 'Stop execution (eXit)'),
    ...
]

The comment is misleading - STOP_KEY IS included in KEYBINDINGS_BY_CATEGORY.

---

#### Code inconsistency

**Description:** Inconsistent handling of JSON fallbacks - some keys have fallback values, others don't

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Most keys have fallback values:
RUN_KEY = _ctrl_key_to_urwid(_run_from_json) if _run_from_json else 'ctrl r'

But some don't:
QUIT_ALT_KEY = _ctrl_key_to_urwid(_quit_alt_from_json) if _quit_alt_from_json else 'ctrl c'

This is inconsistent - either all should have fallbacks or none should. The pattern suggests all keys should have sensible defaults if JSON is missing.

---

#### Code vs Documentation inconsistency

**Description:** keymap_widget.py converts 'Ctrl+' to '^' notation but keybindings.py key_to_display() already does this conversion, creating redundant logic

**Affected files:**
- `src/ui/keybindings.py`
- `src/ui/keymap_widget.py`

**Details:**
In keybindings.py lines 107-123, key_to_display() converts:
'ctrl a' -> '^A'
'shift ctrl b' -> '^Shift+B'

In keymap_widget.py lines 10-23, _format_key_display() converts:
'Ctrl+F' -> '^F'
'Shift+Ctrl+V' -> 'Shift+^V'

These functions handle different input formats (urwid keys vs Ctrl+ notation) but the keymap_widget function seems unnecessary since key_to_display() is already called in KEYBINDINGS_BY_CATEGORY construction.

---

#### Documentation inconsistency

**Description:** Module docstring says keybindings are loaded from curses_keybindings.json but doesn't mention validation rules or fallback behavior

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Lines 1-11:
"""
Keyboard binding definitions for MBASIC Curses UI.

This module loads keybindings from curses_keybindings.json and provides them
in the format expected by the Curses UI (urwid key names, character codes, display names).

This ensures consistency between the JSON config, the UI behavior, and the documentation.

File location: curses_keybindings.json is located in the src/ui/ directory (same directory as this module).
If you need to modify keybindings, edit that JSON file rather than changing constants here.
"""

Docstring doesn't mention:
1. Validation rules (Ctrl+A through Ctrl+Z only)
2. Duplicate key detection
3. Fallback values when JSON keys are missing
4. That validation happens at module load time

---

#### Code inconsistency

**Description:** Hardcoded keys (MENU_KEY, CLEAR_BREAKPOINTS_KEY, DELETE_LINE_KEY, etc.) are not loaded from JSON despite module claiming all keybindings come from JSON

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Line 124:
MENU_KEY = 'ctrl u'

Line 169:
CLEAR_BREAKPOINTS_KEY = 'ctrl shift b'

Line 172:
DELETE_LINE_KEY = 'ctrl d'

Line 175:
RENUMBER_KEY = 'ctrl e'

Line 178:
INSERT_LINE_KEY = 'ctrl y'

Line 193:
STOP_KEY = 'ctrl x'

Line 196:
SETTINGS_KEY = 'ctrl p'

Line 199:
MAXIMIZE_OUTPUT_KEY = 'ctrl shift m'

These are hardcoded but module docstring says 'If you need to modify keybindings, edit that JSON file rather than changing constants here.'

---

#### Code vs Comment conflict

**Description:** Comment claims context menu dismissal is automatic, but code explicitly releases grab

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Lines 598-602 comment states:
# Note: tk_popup() handles menu dismissal automatically (ESC key,
# clicks outside menu, selecting items). Explicit bindings for
# FocusOut/Escape are not needed and may not fire reliably since
# Menu widgets have their own event handling for dismissal.

But lines 603-607 explicitly release grab:
try:
    menu.tk_popup(event.x_root, event.y_root)
finally:
    # Release grab after menu is shown. Note: tk_popup handles menu interaction,
    # but we explicitly release the grab to ensure clean state.
    menu.grab_release()

The comment says explicit handling is not needed, but code does explicit grab_release() with justification.

---

#### Code duplication warning

**Description:** Table formatting may be duplicated in markdown_renderer.py

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
_format_table_row() method at line 655 has comment:
Note: This implementation may be duplicated in src/ui/markdown_renderer.py.
If both implementations exist and changes are needed to table formatting logic,
consider extracting to a shared utility module to maintain consistency.

Warns about potential duplication with another file not included in the analysis.

---

#### Code vs Comment conflict

**Description:** Comment about link tag prefixes may be incomplete

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Lines 575-579 comment states:
Note: Both "link_" (from _render_line_with_links) and "result_link_"
(from _execute_search) prefixes are checked. Both types are stored
identically in self.link_urls, but the prefixes distinguish their origin.

However, _render_line_with_links() at line 227 creates tags with prefix "link_" (not "link_" and "result_link_"), while _execute_search() at line 437 creates "result_link_" prefix. The comment correctly describes the two prefixes, but the code at line 580-582 checks for both:
for tag in tags:
    if tag.startswith("link_") or tag.startswith("result_link_"):
        link_tag = tag

This is consistent, not a conflict.

---

#### Code vs Comment conflict

**Description:** Comment describes widget storage incorrectly

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Lines 189-192 comment in _get_current_widget_values():
# All entries in self.widgets dict are tk.Variable instances (BooleanVar, StringVar, IntVar),
# not the actual widget objects (Checkbutton, Spinbox, Entry, Combobox).
# The variables are associated with widgets via textvariable/variable parameters.

This is accurate based on _create_setting_widget() lines 139-161 which stores variables (var) not widgets in self.widgets[key]. Not a conflict, comment is correct.

---

#### Documentation inconsistency

**Description:** Docstring describes modal behavior incompletely

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Line 36 comment states:
# Make modal (prevents interaction with parent, but doesn't block code execution - no wait_window())

This clarifies that grab_set() is used without wait_window(), making it modal for interaction but not blocking. However, the class docstring at line 15 just says 'Dialog for modifying MBASIC settings' without mentioning modal behavior. Minor documentation gap.

---

#### Code vs Documentation inconsistency

**Description:** Help display mechanism described as tooltip in comment but implemented as label

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Line 172 comment states:
# Show short help as inline label (not a hover tooltip, just a gray label)

This clarifies the implementation is a static label, not a tooltip. The comment is accurate and matches the code at lines 173-175 which creates a ttk.Label. Not an inconsistency, just explicit clarification.

---

#### code_vs_comment

**Description:** Comment describes immediate_entry as 'the actual Entry widget created in start()' but immediate_entry is also set to None in __init__

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~147: 'immediate_entry is the actual Entry widget created in start()'
Line ~149 in __init__: self.immediate_entry = None

---

#### code_vs_comment

**Description:** Comment states variables_sort_column default is 'accessed' for 'last-accessed timestamp' but heading text shows 'Last Accessed' not timestamp

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~138: self.variables_sort_column = 'accessed'  # Current sort column (default: 'accessed' for last-accessed timestamp)
Line ~139: self.variables_sort_reverse = True  # Sort direction: False=ascending, True=descending (default descending for timestamps)

But line ~1009: tree.heading('#0', text='↓ Variable (Last Accessed)')

The comment implies timestamps are displayed, but the heading just says 'Last Accessed' without clarifying it's a timestamp.

---

#### code_vs_comment

**Description:** Comment states 'Note: Toolbar has been simplified' but doesn't specify what was removed or when

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines ~577-582:
# Note: Toolbar has been simplified to show only essential execution controls.
# Additional features are accessible via menus:
# - List Program → Run > List Program
# - New Program (clear) → File > New
# - Clear Output → Run > Clear Output

This comment references a simplification but provides no context about the previous state or when this change occurred.

---

#### code_vs_comment

**Description:** Comment about validation timing is incomplete regarding when validation actually occurs

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _validate_editor_syntax method around line 1200:
Comment says: "Note: This method is called:
- With 100ms delay after cursor movement/clicks (to avoid excessive validation during rapid editing)
- Immediately when focus leaves editor (to ensure validation before switching windows)"

However, looking at the actual event bindings:
- _on_cursor_move calls validation with 100ms delay (correct)
- _on_mouse_click calls validation with 100ms delay (correct)
- _on_focus_out calls validation immediately (correct)
- _on_focus_in does NOT call validation

The comment is accurate but incomplete - it doesn't mention that validation is NOT called on focus-in, which might be relevant context.

---

#### code_vs_comment

**Description:** Comment about when _remove_blank_lines is called may be outdated

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _remove_blank_lines method around line 1330:
Comment says: "Currently called only from _on_enter_key (after each Enter key press), not after pasting or other modifications."

This comment describes the current usage but:
1. The method _on_enter_key is not shown in the provided code
2. Cannot verify if this is the only caller
3. The comment uses 'Currently' which suggests it may change, making it potentially outdated

This is a low-severity documentation issue - the comment may be accurate but cannot be verified from the provided code.

---

#### code_vs_comment

**Description:** Comment about error display logic doesn't match the actual condition

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _validate_editor_syntax method around line 1220:
Comment says: "Only show full error list in output if there are multiple errors. For single errors, the red ? icon in the editor is sufficient feedback. This avoids cluttering the output pane with repetitive messages during editing."

The code then does:
should_show_list = len(errors_found) > 1
if should_show_list:
    # Show errors

This means errors are shown when there are 2 or more errors (> 1), not just when there are multiple. The comment is technically correct but could be clearer that 'multiple' means 'more than one' (i.e., >= 2).

---

#### code_vs_comment

**Description:** Comment about OPTION BASE validation is defensive but accurate

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _edit_array_element method around line 975:
Comment says: "OPTION BASE only allows 0 or 1 (validated by OPTION statement parser). The else clause is defensive programming for unexpected values."

The code then has:
if array_base == 0:
    # use all zeros
elif array_base == 1:
    # use all ones
else:
    # Defensive fallback for invalid array_base (should not occur)
    default_subscripts = ','.join(['0'] * len(dimensions))

This is good defensive programming, but the comment could be clearer that the else clause should never execute in normal operation. The comment is accurate but could emphasize this is truly defensive (unreachable in correct operation).

---

#### code_vs_comment

**Description:** Comment describes behavior that doesn't match the actual condition check

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_enter_key method around line 880:
Comment says: '# Check if line is just a line number with no content (e.g., "20 ")'
But the regex pattern is: r'^\s*(\d+)\s*$'

This pattern matches a line number with ANY amount of trailing whitespace, not specifically 'no content'. The comment should clarify that trailing spaces/whitespace count as 'no content'.

---

#### code_vs_comment

**Description:** Comment claims inline paste but logic also handles blank line case

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_paste method around line 1230:
Comment says: '# Multi-line paste or single-line paste into blank line - use auto-numbering logic\nNote: Single-line paste into existing line uses different logic (inline paste above).'

This is accurate but the comment structure is confusing. The 'Note:' appears to be explaining what happens in a DIFFERENT code path (above), not the current path. This makes it hard to understand what the current code block does.

---

#### code_vs_comment

**Description:** Inconsistent comment style for explaining control flow

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Throughout the file, some comments explain what code does ('# Clear output') while others explain why ('# Prevent default paste behavior'). In _on_enter_key around line 1000, the comment '# Don't refresh - let user fix the error' mixes both styles in a way that's confusing about whether this is describing the action or the reason.

---

#### code_vs_comment

**Description:** Dead code comment for _setup_immediate_context_menu but method is defined and could be called

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment states:
"DEAD CODE: This method is never called because immediate_history is always
None in the Tk UI (see __init__). Retained for potential future use if
immediate mode gets its own output widget. Related dead code:
_copy_immediate_selection() and _select_all_immediate()."

While the comment is accurate that immediate_history is None and the method isn't currently called, the method is fully implemented and could be called if immediate_history were initialized. This is more 'unused code' than 'dead code'.

---

#### code_vs_comment

**Description:** Comment about 'not self.running' preventing race conditions may be inaccurate

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _update_immediate_status method:
"# Check if safe to execute - use both can_execute_immediate() AND self.running flag
# The 'not self.running' check prevents immediate mode execution when a program is running,
# even if the tick hasn't completed yet. This prevents race conditions where immediate
# mode could execute while the program is still running but between tick cycles."

The comment suggests this prevents race conditions, but self.running is a simple boolean flag that doesn't provide actual synchronization. If there's a real race condition concern, a proper lock mechanism would be needed. The comment may be overstating the protection provided.

---

#### code_vs_comment

**Description:** Comment about CLS being ignored contradicts clear_screen implementation

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In TkIOHandler.clear_screen():
"Design decision: GUI output is persistent for review. Users can manually
clear output via Run > Clear Output menu if desired. CLS command is ignored
to preserve output history during program execution."

The comment says 'CLS command is ignored' but the method is a no-op, which means it's not actively ignored - it's just not implemented. The distinction matters because 'ignored' implies active detection and suppression, while no-op means the command is processed but has no effect.

---

#### documentation_inconsistency

**Description:** The class docstring describes status priority as 'error > breakpoint > blank' and states 'Both set_error() and set_breakpoint() apply the same priority logic', but the implementation in both methods is identical (error takes priority if has_error is True, then breakpoint, then blank). The phrase 'no special handling for clearing vs setting' is unclear - both methods handle clearing (when enabled=False or has_error=False) by updating the status based on the remaining flags.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Class docstring: 'Status priority (when both error and breakpoint): - ? takes priority (error shown) - After fixing error, ● becomes visible - Both set_error() and set_breakpoint() apply the same priority logic: error > breakpoint > blank (no special handling for clearing vs setting)'

Both set_error() and set_breakpoint() use identical logic:
if metadata['has_error']:
    metadata['status'] = '?'
elif metadata['has_breakpoint']:
    metadata['status'] = '●'
else:
    metadata['status'] = ' '

The 'no special handling for clearing vs setting' phrase is confusing since the methods do handle clearing by setting the flag to False and recalculating status.

---

#### code_vs_comment

**Description:** The _on_cursor_move() method has a detailed comment explaining why after_idle is used: 'Schedule deletion after current event processing to avoid interfering with ongoing key/mouse event handling (prevents cursor position issues, undo stack corruption, and widget state conflicts during event processing)'. However, this is an inline comment that could be in the docstring for better visibility.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Inline comment: '# Schedule deletion after current event processing to avoid interfering\n# with ongoing key/mouse event handling (prevents cursor position issues,\n# undo stack corruption, and widget state conflicts during event processing)'

This important implementation detail is buried in an inline comment rather than being in the method's docstring where it would be more visible to developers.

---

#### code_vs_comment

**Description:** Comment in serialize_line() about fallback behavior is overly detailed and potentially confusing

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Lines ~680-687: The comment explains:
'# Note: If source_text doesn\'t match pattern (or is unavailable), falls back to relative_indent=1.\n# When does this occur?\n# 1. Programmatically inserted lines (no source_text attribute)\n# 2. Lines where source_text doesn\'t start with line_number + spaces (edge case)\n# Result: These lines get single-space indentation instead of preserving original spacing.\n# This is expected behavior - programmatically inserted lines use standard formatting.'

This is accurate but the level of detail about edge cases and expected behavior seems excessive for inline comments. The code logic is straightforward (default to 1 space if no match), and the comment could be simplified.

---

#### code_vs_comment

**Description:** Comment in serialize_variable() about explicit_type_suffix attribute handling is defensive but may indicate incomplete implementation

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Lines ~838-841: Comment says:
'# Only add type suffix if it was explicit in the original source\n# Don\'t add suffixes that were inferred from DEF statements\n# Note: explicit_type_suffix is not always set (depends on parser implementation),\n# so getattr defaults to False if missing, preventing incorrect suffix output'

The comment acknowledges that explicit_type_suffix 'is not always set (depends on parser implementation)' which suggests inconsistent behavior across the codebase. The defensive getattr with False default may be masking an incomplete implementation where the parser should always set this attribute.

---

#### documentation_inconsistency

**Description:** Module docstring claims 'No UI-framework dependencies' but doesn't mention the glob and os imports which are filesystem dependencies

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Module docstring at top says:
'This module contains UI-agnostic helper functions that can be used by\nany UI (CLI, Tk, Web, Curses). No UI-framework dependencies (Tk, curses, web)\nare allowed. Standard library modules (os, glob, re) and core interpreter\nmodules (runtime, parser, AST nodes) are permitted.'

The docstring does mention 'Standard library modules (os, glob, re)' are permitted, so this is actually consistent. However, the phrasing 'No UI-framework dependencies' followed by listing allowed dependencies could be clearer - it might read as 'no dependencies' at first glance.

---

#### code_vs_documentation

**Description:** Function cycle_sort_mode() comment says it 'matches the Tk UI implementation' but this is supposed to be UI-agnostic shared code

**Affected files:**
- `src/ui/variable_sorting.py`

**Details:**
Line ~24 comment: 'This matches the Tk UI implementation.'

Since this is in a shared UI module (variable_sorting.py) that provides 'consistent variable sorting behavior across all UI backends', referencing a specific UI implementation (Tk) in the comment suggests this was extracted from Tk-specific code. The comment should describe the behavior generically rather than referencing a specific UI.

---

#### code_vs_comment

**Description:** update_line_references() docstring describes 'Two-pattern approach (applied sequentially in a single pass)' but the implementation uses two separate regex substitutions, not a single pass

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Lines ~163-165: Comment says:
'# Two-pattern approach (applied sequentially in a single pass):\n# Pattern 1: Match keyword + first line number (GOTO/GOSUB/THEN/ELSE/ON...GOTO/ON...GOSUB)\n# Pattern 2: Match comma-separated line numbers (for ON...GOTO/GOSUB lists)'

But the code at lines ~183 and ~192 does:
code = pattern.sub(replace_line_ref, code)  # First substitution
...
code = comma_pattern.sub(replace_comma_line, code)  # Second substitution

This is two passes over the string, not 'a single pass'. The comment is misleading about the implementation approach.

---

#### Documentation inconsistency

**Description:** Docstring example in cmd_list() shows implementation pattern but the actual implementation is already complete, not a stub

**Affected files:**
- `src/ui/visual.py`

**Details:**
Docstring says:
        """Execute LIST command - list program lines.

        Example:
            lines = self.program.get_lines()
            for line_num, line_text in lines:
                self.io.output(line_text)
        """

But the method body already contains this exact implementation:
        lines = self.program.get_lines()
        for line_num, line_text in lines:
            self.io.output(line_text)

The docstring presents it as an 'Example' to implement, but it's already implemented.

---

#### Code vs Comment conflict

**Description:** Comment in _internal_change_handler says 'CodeMirror sends new value in e.args attribute' but this is implementation detail that may not be accurate

**Affected files:**
- `src/ui/web/codemirror5_editor.py`

**Details:**
Comment in __init__ method:
        def _internal_change_handler(e):
            self._value = e.args  # CodeMirror sends new value in e.args attribute
            if on_change:
                on_change(e)

The comment claims CodeMirror sends the value in e.args, but this is actually a NiceGUI event handling detail, not a CodeMirror behavior. The comment could be misleading about where this behavior originates.

---

#### Code vs Documentation inconsistency

**Description:** value property getter has defensive code for dict/None cases but this behavior is not documented in the property docstring

**Affected files:**
- `src/ui/web/codemirror5_editor.py`

**Details:**
Property implementation:
    @property
    def value(self) -> str:
        """Get current editor content.

        Always returns a string, even if internal value is dict or None.
        """
        if isinstance(self._value, dict):
            # Sometimes event args are dict - return empty string
            return ''
        return self._value or ''

The docstring mentions this behavior, but it's unclear why _value would ever be a dict. The comment 'Sometimes event args are dict' suggests this is a workaround for an event handling issue, but this is not explained in the class documentation or __init__ docstring.

---

#### code_vs_comment

**Description:** Comment references _enable_inline_input() method that is not visible in the provided code

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~70 references:
# by _enable_inline_input() in the NiceGUIBackend class.

This method is not shown in the provided code snippet (part 1 of nicegui_backend.py). Either the method exists in part 2 (not shown), or the comment is outdated.

---

#### code_vs_comment

**Description:** Comment says prompt display is handled by _get_input via _enable_inline_input, but implementation details not visible

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~60-62:
# Don't print prompt here - the input_callback (backend._get_input) handles
# prompt display via _enable_inline_input() method in the NiceGUIBackend class

The _get_input method is not shown in the provided code, so cannot verify if this is accurate or outdated.

---

#### documentation_inconsistency

**Description:** Multiple references to MBASIC version '5.21' as language version, but inconsistent labeling

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~598: # Note: '5.21' is the MBASIC language version (intentionally hardcoded)
Line ~599: ui.label('MBASIC 5.21 Web IDE').classes('text-lg')
Line ~1062: ui.page_title('MBASIC 5.21 - Web IDE')
Line ~1117: self.output_text = f'MBASIC 5.21 Web IDE - {VERSION}\n'

The comment clarifies 5.21 is the language version, but the UI labels mix 'MBASIC 5.21 Web IDE' with implementation VERSION. This could be clearer about which version is which.

---

#### code_vs_comment

**Description:** Comment references line numbers that may be incorrect due to code changes

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Multiple comments reference specific line numbers:
- Line 1932 referenced in comment at line ~1680: "# is focused for user input (see _execute_tick() at line 1932)."
- Line ~1845 referenced in comment at line ~1845: "# Note: This implementation does NOT clear output (see comment at line ~1845 below)."

These hardcoded line numbers will become incorrect as code is modified.

---

#### code_vs_comment

**Description:** Comment about RUN behavior mentions line ~1845 but the actual line number is different

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _menu_run method around line 1845, comment states:
"# Don't clear output - continuous scrolling like ASR33 teletype
# Design choice: Unlike some modern BASIC interpreters that clear output on RUN,
# we preserve historical ASR33 behavior (continuous scrolling, no auto-clear).
# Note: Step commands (Ctrl+T/Ctrl+K) DO clear output for clarity when debugging"

But earlier in the same method, another comment references this:
"# Note: This implementation does NOT clear output (see comment at line ~1845 below)."

The self-referential line number is approximate and will drift.

---

#### code_vs_comment

**Description:** Comment about method location uses search instruction instead of line reference

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~1650 states:
"# (Note: Method defined later in this class - search for 'def _on_editor_change')"

This is actually good practice (search-based reference instead of line number), but inconsistent with other comments that use line numbers. Not really an inconsistency, just noting the mixed approach.

---

#### code_vs_comment

**Description:** Comment describes double line number detection threshold as arbitrary, but provides specific rationale

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _on_editor_change():

Comment: "# The 5-char threshold is arbitrary - balances detecting small pastes while avoiding
# false positives from rapid typing (e.g., typing 'PRINT' quickly = 5 chars but not a paste)."

The comment calls it 'arbitrary' but then provides specific reasoning, which contradicts the meaning of arbitrary. Should either remove 'arbitrary' or acknowledge it's a heuristic with trade-offs.

---

#### code_vs_comment

**Description:** Comment about architecture decision contradicts actual behavior in immediate executor

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_execute_immediate() method:

Comment: "# Architecture: We do NOT auto-sync editor from AST after immediate commands.
# This preserves one-way data flow (editor → AST → execution) and prevents
# losing user's formatting/comments. Commands that modify code (like RENUM)
# update the editor text directly."

But the code calls _save_editor_to_program() which syncs FROM editor TO program, not the other way. The comment describes the opposite direction. The comment is correct about the architecture decision but describes it backwards.

---

#### code_vs_comment

**Description:** Comment about CP/M EOF marker handling is inconsistent with actual file loading behavior

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_save_editor_to_program() method:

Comment: "# \x1a (Ctrl+Z, CP/M EOF marker - included for consistency with file loading)
text = text.replace('\r\n', '\n').replace('\r', '\n').replace('\x1a', '')"

The comment says this is 'for consistency with file loading', but there's no visible file loading code in this file that shows the same handling. This suggests either:
1. File loading is in another file and should be referenced
2. The comment is outdated and file loading doesn't actually do this
3. The handling is inconsistent between editor and file loading

---

#### code_vs_comment

**Description:** Comment mentions backwards compatibility for 'halted' and 'stopped' keys but no code actually handles them

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~51: '# Ignore 'halted' key if present (backwards compatibility with old saved states)'

Comment at line ~61: '# Ignore 'stopped' key if present (backwards compatibility with old saved states)'

The comments claim to ignore these keys for backwards compatibility, but there's no actual code that checks for or ignores these keys. If old saved states contain these keys, they would simply be unused (which may be intentional), but the comment implies active handling.

---

#### documentation_inconsistency

**Description:** Docstring for start() method says 'NOT IMPLEMENTED' but implementation actually raises NotImplementedError with different message

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Docstring: 'NOT IMPLEMENTED - raises NotImplementedError.'

Actual error message: 'Web backend uses start_web_ui() function, not backend.start()'

While both convey the method shouldn't be called, the docstring could be more specific about the alternative approach.

---

#### code_comment_conflict

**Description:** Comment says 'new code should use direct web URL' but provides function-based API

**Affected files:**
- `src/ui/web_help_launcher.py`

**Details:**
Comment in web_help_launcher.py:
'# Legacy class kept for compatibility - new code should use direct web URL instead'
'# The help site is already built and served at http://localhost/mbasic_docs'

But the module provides open_help_in_browser() function as the new API, not 'direct web URL'. The migration guide shows function calls, not direct URL usage.

---

#### documentation_inconsistency

**Description:** Keyboard shortcut placeholders not replaced with actual keys

**Affected files:**
- `docs/help/common/debugging.md`

**Details:**
debugging.md contains placeholder syntax like:
'Shortcuts: Tk/Curses/Web: **{{kbd:step:curses}}** or Step button'
'Press **{{kbd:continue:curses}}** or click **Continue**'
'Press **{{kbd:quit:curses}}** or click **Stop**'
'**Tk UI:** Debug → Execution Stack or **{{kbd:toggle_stack:tk}}**'
'**Curses UI:** **{{kbd:step_line:curses}}** during execution'

These {{kbd:...}} placeholders should be replaced with actual keyboard shortcuts from web_keybindings.json (F10 for step, F5 for continue, Esc for stop, F9 for breakpoint, Ctrl+Alt+V for toggle_variables).

---

#### code_documentation_mismatch

**Description:** SessionState tracks auto_save settings but debugging docs don't mention auto-save feature

**Affected files:**
- `src/ui/web/session_state.py`
- `docs/help/common/debugging.md`

**Details:**
session_state.py SessionState class has:
- auto_save_enabled: bool = True
- auto_save_interval: int = 30
- last_save_content: str = ''

But debugging.md and other help docs don't document any auto-save feature or how it works. Users may not know this feature exists.

---

#### documentation_inconsistency

**Description:** Inconsistent UI naming - 'Curses UI' vs 'curses backend'

**Affected files:**
- `docs/help/common/debugging.md`

**Details:**
debugging.md uses both:
- 'Curses UI' (capitalized, with space)
- 'curses backend' (lowercase)

README.md consistently uses 'Curses' (capitalized) in section headers. Should standardize on one format.

---

#### documentation_inconsistency

**Description:** Loop examples use inconsistent indentation style

**Affected files:**
- `docs/help/common/examples/loops.md`

**Details:**
loops.md shows some examples with indented loop bodies:
'10 FOR I = 1 TO 10
20   PRINT I
30 NEXT I'

But other examples have no indentation:
'10 FOR ROW = 1 TO 10
20   FOR COL = 1 TO 10
30     PRINT ROW * COL;
40   NEXT COL
50   PRINT
60 NEXT ROW'

While BASIC doesn't require indentation, examples should be consistent for readability.

---

#### code_comment_conflict

**Description:** Function docstring says 'Returns bool' but doesn't document what True/False means

**Affected files:**
- `src/ui/web_help_launcher.py`

**Details:**
open_help_in_browser() docstring:
'Returns:
    bool: True if browser opened successfully, False otherwise'

But the function implementation shows:
'result = webbrowser.open(url)'
'return result'

webbrowser.open() returns True if a browser was found, but doesn't guarantee the URL loaded successfully. The docstring should clarify this distinction.

---

#### documentation_inconsistency

**Description:** Documentation uses 'Execution Stack' but may be inconsistent with actual UI labels

**Affected files:**
- `docs/help/common/debugging.md`

**Details:**
debugging.md consistently refers to 'Execution Stack Window' and 'Execution Stack'.

Without seeing the actual UI code, cannot verify if the UI uses 'Execution Stack', 'Call Stack', 'Stack', or another label. Should verify UI labels match documentation.

---

#### code_documentation_mismatch

**Description:** SessionState tracks find/replace state but no documentation for find/replace feature

**Affected files:**
- `src/ui/web/session_state.py`

**Details:**
session_state.py has:
- last_find_text: str = ''
- last_find_position: int = 0
- last_case_sensitive: bool = False

This suggests a find/replace feature exists, but no help documentation describes how to use it or what keyboard shortcuts activate it.

---

#### documentation_inconsistency

**Description:** Priority indicators section mentions parse errors but doesn't explain how to fix them

**Affected files:**
- `docs/help/common/debugging.md`

**Details:**
debugging.md 'Priority Indicators' section:
'1. **? (Question mark)** - Parse error (highest priority)'

But the 'Error Markers' section later says 'Read error message - Check the output window for details' without explaining where the output window is or how to access it in each UI.

---

#### documentation_inconsistency

**Description:** Inconsistent statement about IF-THEN-ELSE file reference

**Affected files:**
- `docs/help/common/getting-started.md`
- `docs/help/common/language.md`

**Details:**
getting-started.md links to 'See: [IF-THEN-ELSE](language/statements/if-then-else-if-goto.md)' but language.md doesn't provide a similar link in its IF...THEN section, only describing the syntax without a reference link.

---

#### documentation_inconsistency

**Description:** Missing INT function documentation but referenced in FIX

**Affected files:**
- `docs/help/common/language/functions/fix.md`
- `docs/help/common/language/functions/int.md`

**Details:**
fix.md states 'FIX(X) is equivalent to SGN(X)*INT(ABS(X))' and 'The major difference between FIX and INT is that FIX does not return the next lower number for negative X.' It also has 'See Also' link to INT. However, the int.md file is not provided in the documentation set, making it impossible to verify the comparison or understand INT's behavior fully.

---

#### documentation_inconsistency

**Description:** Inconsistent constant value precision

**Affected files:**
- `docs/help/common/language/appendices/math-functions.md`

**Details:**
math-functions.md provides PI# = 3.141592653589793 (16 digits) and E# = 2.718281828459045 (15 digits). The documentation states double precision has '~16 significant digits' but E# only shows 15 digits while PI# shows 16. This inconsistency in precision representation may confuse users about the actual precision available.

---

#### documentation_inconsistency

**Description:** Inconsistent range notation format

**Affected files:**
- `docs/help/common/language/data-types.md`

**Details:**
data-types.md uses different formats for ranges: 'Approximately 2.938736×10^-39 to 1.701412×10^38' for SINGLE but 'Approximately 2.938736×10^-308 to 1.797693×10^308 (much larger range than single-precision, with greater precision)' for DOUBLE. The SINGLE range omits the ± symbol while DOUBLE section mentions it in the table but not in the description. Inconsistent formatting makes comparison harder.

---

#### documentation_inconsistency

**Description:** Incomplete error handling information in EXP

**Affected files:**
- `docs/help/common/language/functions/exp.md`
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
exp.md states 'If EXP overflows, the "Overflow" error message is displayed, machine infinity with the appropriate sign is supplied as the result, and execution continues.' However, error-codes.md for error 6 (OV - Overflow) states 'The result of a calculation is too large to be represented in BASIC-80's number format' without mentioning that execution continues with infinity. This creates uncertainty about whether overflow always continues or halts execution.

---

#### documentation_inconsistency

**Description:** Cross-reference inconsistency between LOC and LOF

**Affected files:**
- `docs/help/common/language/functions/loc.md`
- `docs/help/common/language/functions/lof.md`

**Details:**
LOC.md 'See Also' section does not reference LOF, but LOF.md 'See Also' section references LOC with description 'Returns current file position/record number (LOF returns total size in bytes)'. This creates an asymmetric cross-reference relationship.

---

#### documentation_inconsistency

**Description:** Inconsistent 'See Also' sections across system functions

**Affected files:**
- `docs/help/common/language/functions/fre.md`
- `docs/help/common/language/functions/hex_dollar.md`
- `docs/help/common/language/functions/inkey_dollar.md`
- `docs/help/common/language/functions/inp.md`

**Details:**
FRE, INKEY$, INP, and PEEK all have nearly identical 'See Also' sections listing the same functions, but HEX$ (a string function) has a completely different set of 'See Also' references. The system functions appear to share a template 'See Also' list that may not be contextually relevant for each function.

---

#### documentation_inconsistency

**Description:** Inconsistent 'See Also' ordering in mathematical functions

**Affected files:**
- `docs/help/common/language/functions/int.md`
- `docs/help/common/language/functions/sgn.md`
- `docs/help/common/language/functions/sin.md`
- `docs/help/common/language/functions/sqr.md`

**Details:**
Mathematical functions have 'See Also' sections with the same functions but in different orders. For example, INT lists them as: ABS, ATN, CDBL, CINT, COS, CSNG, EXP, FIX, LOG, RND, SGN, SIN, SQR, TAN. SGN lists them as: ABS, ATN, COS, EXP, FIX, INT, LOG, RND, SIN, SQR, TAN (missing CDBL, CINT, CSNG). This inconsistency makes navigation less predictable.

---

#### documentation_inconsistency

**Description:** PEEK documentation states POKE is complementary but implementation note contradicts this

**Affected files:**
- `docs/help/common/language/functions/peek.md`

**Details:**
The Description section states: 'PEEK is traditionally the complementary function to the POKE statement. However, in this implementation, PEEK returns random values and POKE is a no-op, so they are not functionally related.' This creates confusion as the traditional relationship is mentioned but then immediately contradicted. The documentation should be clearer about the non-functional relationship upfront.

---

#### documentation_inconsistency

**Description:** SPACE$ and SPC have overlapping functionality but inconsistent cross-references

**Affected files:**
- `docs/help/common/language/functions/space_dollar.md`
- `docs/help/common/language/functions/spc.md`

**Details:**
SPACE$ documentation says 'For variable spacing in PRINT statements, see SPC() and TAB()' and lists SPC in 'See Also'. However, SPC documentation does not mention SPACE$ in its 'See Also' section, only listing TAB, PRINT, LPRINT, POS. This creates an asymmetric relationship.

---

#### documentation_inconsistency

**Description:** MKI$/MKS$/MKD$ 'See Also' section includes unrelated functions

**Affected files:**
- `docs/help/common/language/functions/mki_dollar-mks_dollar-mkd_dollar.md`

**Details:**
The 'See Also' section includes CLOAD and CSAVE with notes 'THIS COMMAND IS NOT INCLUDED IN THE DEC VT180 VERSION', which are cassette tape commands unrelated to the core functionality of converting numbers to strings for random file operations. Also includes LPRINT which is not directly related to file buffer operations.

---

#### documentation_inconsistency

**Description:** Index categorization may be incomplete or inconsistent

**Affected files:**
- `docs/help/common/language/functions/index.md`

**Details:**
The index shows 'System Functions' category includes: FRE, INKEY$, INP, PEEK, USR, VARPTR. However, LPOS is categorized as 'file-io' in its frontmatter but could arguably be a system function since it deals with hardware (line printer). The categorization scheme may need review for consistency.

---

#### documentation_inconsistency

**Description:** Inconsistent 'related' field in frontmatter - str_dollar.md lists 'left_dollar' and 'right_dollar' but string_dollar.md does not include these in its See Also section

**Affected files:**
- `docs/help/common/language/functions/str_dollar.md`
- `docs/help/common/language/functions/string_dollar.md`

**Details:**
str_dollar.md frontmatter:
related: ['val', 'print-using', 'left_dollar', 'right_dollar']

string_dollar.md See Also section does not include left_dollar or right_dollar references, though both documents have similar See Also lists for other string functions.

---

#### documentation_inconsistency

**Description:** TAB function documentation includes READ and DATA in See Also section, but these are not directly related to TAB functionality

**Affected files:**
- `docs/help/common/language/functions/tab.md`

**Details:**
TAB See Also includes:
- [READ](../statements/read.md) - Read data from DATA statements (used in example above)
- [DATA](../statements/data.md) - Store data for READ statements (used in example above)

These are only tangentially related because they appear in the example code, not because they're functionally related to TAB. Other function docs don't include every statement used in their examples.

---

#### documentation_inconsistency

**Description:** AUTO documentation example shows usage but doesn't demonstrate the asterisk warning behavior described in Remarks

**Affected files:**
- `docs/help/common/language/statements/auto.md`

**Details:**
Remarks section states:
"If AUTO generates a line number that is already being used, an asterisk is printed after the number to warn the user that any input will replace the existing line."

But the Example section doesn't show this behavior:
```basic
AUTO 100,50
REM Generates line numbers 100, 150, 200, etc.

AUTO
REM Generates line numbers 10, 20, 30, 40, etc.
```

A more complete example would demonstrate the asterisk warning.

---

#### documentation_inconsistency

**Description:** CHAIN documentation states 'Open files remain open across the chain operation' but doesn't clarify if this applies to all file types or has limitations

**Affected files:**
- `docs/help/common/language/statements/chain.md`

**Details:**
Under 'Memory:' section:
"The current program is removed from memory unless MERGE is specified. Open files remain open across the chain operation."

This is stated without qualification, but it's unclear if this applies to all file types (sequential, random, etc.) or if there are any limitations. Other file I/O documentation doesn't cross-reference this behavior.

---

#### documentation_inconsistency

**Description:** CLOSE documentation states END closes all files, but doesn't mention CHAIN behavior with open files

**Affected files:**
- `docs/help/common/language/statements/close.md`
- `docs/help/common/language/statements/chain.md`

**Details:**
CLOSE.md states:
"The END statement and the NEW command always CLOSE all disk files automatically. (STOP does not close disk files.)"

But CHAIN.md states:
"Open files remain open across the chain operation."

These two statements should be cross-referenced, as CHAIN is a program control statement that affects file state.

---

#### documentation_inconsistency

**Description:** CLS documentation states it's implemented in all UI backends but doesn't specify which backends exist

**Affected files:**
- `docs/help/common/language/statements/cls.md`

**Details:**
CLS.md states:
"Note: CLS is implemented in MBASIC and works in all UI backends."

But there's no reference to what UI backends are available or where to find that information. The index.md doesn't mention UI backends either.

---

#### documentation_inconsistency

**Description:** CONT documentation references a non-existent example in Section 2.61

**Affected files:**
- `docs/help/common/language/statements/cont.md`

**Details:**
Example section states:
```basic
See example Section 2.61, STOP.
```

But the documentation uses markdown file structure, not numbered sections. The reference should be to the STOP.md file instead.

---

#### documentation_inconsistency

**Description:** DATA documentation doesn't mention RESTORE in the main Remarks section, only in See Also

**Affected files:**
- `docs/help/common/language/statements/data.md`

**Details:**
The Remarks section states:
"DATA statements may be reread from the beginning by use of the RESTORE statement."

This is the only mention of RESTORE in the main documentation. Given that RESTORE is critical to DATA usage, it could be explained more thoroughly in the Remarks section rather than just mentioned at the end.

---

#### documentation_inconsistency

**Description:** Inconsistent formatting of 'See Also' sections between related DEF statements

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`
- `docs/help/common/language/statements/def-usr.md`

**Details:**
def-fn.md 'See Also' section:
- [DEF USR](def-usr.md) - Define assembly subroutine address
- [USR](../functions/usr.md) - Call assembly language subroutine
- [GOSUB-RETURN](gosub-return.md) - Branch to and return from a subroutine

def-usr.md 'See Also' section:
- [USR](../functions/usr.md) - Call assembly language subroutine
- [DEF FN](def-fn.md) - Define user-defined function
- [POKE](poke.md) - Write byte to memory location
- [PEEK](../functions/peek.md) - Read byte from memory location

The descriptions are inconsistent (e.g., 'Define assembly subroutine address' vs 'Define user-defined function' - one has 'assembly' detail, other doesn't).

---

#### documentation_inconsistency

**Description:** DELETE and EDIT have different levels of detail about error conditions

**Affected files:**
- `docs/help/common/language/statements/delete.md`
- `docs/help/common/language/statements/edit.md`

**Details:**
delete.md states:
"If <line number> does not exist, an 'Illegal function call' error occurs."

edit.md states:
"If the line doesn't exist, an error is generated."

The EDIT documentation doesn't specify which error is generated, while DELETE is specific. This inconsistency in documentation detail could confuse users.

---

#### documentation_inconsistency

**Description:** GOSUB and GOTO have inconsistent example formatting

**Affected files:**
- `docs/help/common/language/statements/gosub-return.md`
- `docs/help/common/language/statements/goto.md`

**Details:**
gosub-return.md example:
```basic
10 GOSUB 40
20 PRINT "BACK FROM SUBROUTINE"
30 END
40 PRINT "SUBROUTINE ";
50 PRINT " IN";
60 PRINT " PROGRESS"
70 RETURN
```

goto.md example:
LIST
              10 READ R
              20 PRINT "R =" :R,
              30 A = 3.l4*R .... 2
              40 PRINT "AREA =" :A
              50 GOTO 10
              60 DATA 5,7,12
              Ok
              RUN
              R = 5                AREA = 78.5

The GOTO example includes the LIST and RUN commands with output, while GOSUB just shows the code. This inconsistency in example presentation style could confuse users.

---

#### documentation_inconsistency

**Description:** Index page lists STOP but the STOP.md file is not provided in the documentation set

**Affected files:**
- `docs/help/common/language/statements/index.md`

**Details:**
index.md includes:
"- [STOP](stop.md) - Stop program execution"

And in the categorized section:
"### Program Control
- [STOP](stop.md) - Stop execution"

However, stop.md is not included in the provided documentation files. This creates broken links and incomplete documentation.

---

#### documentation_inconsistency

**Description:** DEF FN Example 4 uses hexadecimal notation but the cross-reference link is generic

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`

**Details:**
Example 4 in def-fn.md states:
"- `&H5F` is hexadecimal notation (hex 5F = decimal 95 = binary 01011111)
- For more on hexadecimal constants, see [Constants](../data-types.md)"

The link goes to a generic 'data-types.md' file which is not provided in the documentation set. It's unclear if this file exists or if hexadecimal notation is properly documented elsewhere.

---

#### documentation_inconsistency

**Description:** HELPSETTING is listed in index but marked as MBASIC Extension without version clarification

**Affected files:**
- `docs/help/common/language/statements/helpsetting.md`
- `docs/help/common/language/statements/index.md`

**Details:**
helpsetting.md states:
"**Versions:** MBASIC Extension"

index.md lists it under:
"### Modern Extensions (MBASIC only)
- [HELPSETTING](helpsetting.md) - Display help for settings"

The terminology is inconsistent: 'MBASIC Extension' vs 'Modern Extensions (MBASIC only)'. It's unclear if these mean the same thing or if there's a distinction.

---

#### documentation_inconsistency

**Description:** Incomplete cross-reference in LINE INPUT# See Also section

**Affected files:**
- `docs/help/common/language/statements/inputi.md`

**Details:**
LINE INPUT# See Also section references:
- [LINE INPUT](line-input.md) - Read entire line from keyboard

But LINE INPUT's See Also section does NOT reference LINE INPUT# back, creating an asymmetric cross-reference.

---

#### documentation_inconsistency

**Description:** Inconsistent error code documentation for file operations

**Affected files:**
- `docs/help/common/language/statements/kill.md`
- `docs/help/common/language/statements/name.md`

**Details:**
KILL states: 'If a KILL statement is given for a file that is currently OPEN, a "File already open" error occurs (error code 55).'

NAME does not specify error codes for its error conditions ('<old filename> must exist and <new filename> must not exist; otherwise an error will result'), creating inconsistent error documentation.

---

#### documentation_inconsistency

**Description:** Inconsistent format numbering between LIST and LLIST

**Affected files:**
- `docs/help/common/language/statements/list.md`
- `docs/help/common/language/statements/llist.md`

**Details:**
LIST documentation uses 'Format 1' and 'Format 2' to distinguish 8K version from Extended/Disk versions.

LLIST documentation references 'Format 2' in remarks ('The options for LLIST are the same as for LIST, Format 2') but does not define Format 1 or Format 2 in its own syntax section, creating potential confusion.

---

#### documentation_inconsistency

**Description:** Missing cross-reference to related memory/resource commands

**Affected files:**
- `docs/help/common/language/statements/limits.md`

**Details:**
LIMITS See Also section includes:
- [FRE](../functions/fre.md)
- [SHOWSETTINGS](showsettings.md)
- [CLEAR](clear.md)
- [DIM](dim.md)

But does not reference NULL statement which also affects resource usage (null character output), creating an incomplete resource management reference list.

---

#### documentation_inconsistency

**Description:** Missing mode documentation in OPEN for append mode

**Affected files:**
- `docs/help/common/language/statements/open.md`
- `docs/help/common/language/statements/printi-printi-using.md`

**Details:**
OPEN documentation lists modes:
- "O" - specifies sequential output mode
- "I" - specifies sequential input mode
- "R" - specifies random input/output mode

PRINT# documentation mentions: 'PRINT# writes data to a sequential file opened for output (mode "O") or append (mode "A")'

OPEN does not document the "A" append mode, creating incomplete mode documentation.

---

#### documentation_inconsistency

**Description:** Inconsistent implementation note formatting

**Affected files:**
- `docs/help/common/language/statements/out.md`
- `docs/help/common/language/statements/poke.md`

**Details:**
OUT states: '⚠️ **Emulated as No-Op**: This feature requires direct hardware I/O port access'

POKE states: '⚠️ **Emulated as No-Op**: This feature requires direct memory access'

Both use same warning format but OUT says 'Cannot access hardware I/O ports from a Python interpreter' while POKE says 'Cannot write to arbitrary memory addresses from a Python interpreter'. The phrasing should be consistent for similar no-op implementations.

---

#### documentation_inconsistency

**Description:** Incomplete print zone documentation

**Affected files:**
- `docs/help/common/language/statements/print.md`

**Details:**
PRINT documentation states zones are 'every 14 columns' and lists:
- Columns 1-14 (first zone)
- Columns 15-28 (second zone)
- Columns 29-42 (third zone)
- Columns 43-56 (fourth zone)
- Columns 57-70 (fifth zone)

But does not specify:
1. What happens after column 70 (sixth zone and beyond)
2. How WIDTH statement affects zone width
3. Whether zones wrap or continue

This creates incomplete zone behavior documentation.

---

#### documentation_inconsistency

**Description:** Missing information about seed value range and behavior

**Affected files:**
- `docs/help/common/language/statements/randomize.md`

**Details:**
RANDOMIZE documentation shows prompt: 'Random Number Seed (-32768 to 32767)?'

But does not specify:
1. What happens if a value outside this range is entered
2. Whether floating point values are accepted and truncated
3. What the default seed is if RANDOMIZE is never called
4. Whether seed 0 has special meaning

This creates incomplete seed behavior documentation.

---

#### documentation_inconsistency

**Description:** Missing information about DATA pointer behavior

**Affected files:**
- `docs/help/common/language/statements/read.md`

**Details:**
READ documentation states: 'A READ statement must always be used with a DATA statement' and 'If the number of variables in the list exceeds the number of elements in the DATA statement(s), an "Out of DATA" error occurs.'

But does not specify:
1. Whether the DATA pointer advances past the last element on error
2. What happens if READ is called after all DATA is consumed
3. How multiple READ statements share the DATA pointer
4. Whether RESTORE is required to re-read DATA

This creates incomplete DATA pointer behavior documentation.

---

#### documentation_inconsistency

**Description:** Incomplete error condition documentation

**Affected files:**
- `docs/help/common/language/statements/renum.md`

**Details:**
RENUM documentation states: 'Cannot create line numbers > 65529' and 'Cannot reorder lines'

But does not specify:
1. What error message appears for line number > 65529
2. What error message appears for reordering attempt
3. Whether RENUM is atomic (all-or-nothing) or partial
4. What happens to the program if RENUM fails midway
5. Whether undefined line references prevent RENUM from executing

The 'Undefined line xxxxx in yyyyy' message suggests RENUM completes even with bad references, but this should be explicit.

---

#### documentation_inconsistency

**Description:** Similar command names (RESTORE vs RESET) could cause confusion, but no cross-reference warning exists between them like exists for RESET/RSET.

**Affected files:**
- `docs/help/common/language/statements/restore.md`
- `docs/help/common/language/statements/reset.md`

**Details:**
RESTORE resets DATA pointer, RESET closes all files. These are completely different operations with similar names. Consider adding a note in RESTORE.md similar to the RESET/RSET warnings to prevent confusion.

---

#### documentation_inconsistency

**Description:** Inconsistent cross-referencing between program termination commands. RUN references STOP and SYSTEM, but STOP doesn't reference SYSTEM, and cross-references are incomplete.

**Affected files:**
- `docs/help/common/language/statements/run.md`
- `docs/help/common/language/statements/stop.md`
- `docs/help/common/language/statements/system.md`

**Details:**
run.md See Also includes: STOP, SYSTEM, END, CHAIN, etc.
stop.md See Also includes: CONT, END, CHAIN, CLEAR, RUN, SYSTEM
system.md See Also includes: CHAIN, CLEAR, COMMON, CONT, END, NEW, RUN, STOP

All three should have consistent cross-references to each other since they're related program control commands.

---

#### documentation_inconsistency

**Description:** WRITE and WRITE# have different title formats in metadata.

**Affected files:**
- `docs/help/common/language/statements/write.md`
- `docs/help/common/language/statements/writei.md`

**Details:**
write.md: title: "WRITE (Screen)"
writei.md: title: "WRITE# (File)"

Both use parenthetical clarification but one uses # and one doesn't. Should be consistent, e.g., both use "WRITE (Screen)" and "WRITE# (File)" or both use "WRITE" and "WRITE #".

---

#### documentation_inconsistency

**Description:** Variables documentation states 'only first 2 characters significant' in original MBASIC but doesn't clarify if this applies to array names or just scalar variables.

**Affected files:**
- `docs/help/common/language/variables.md`

**Details:**
variables.md: "**Note on Variable Name Significance:** In the original MBASIC 5.21, only the first 2 characters of variable names were significant (AB, ABC, and ABCDEF would be the same variable)."

Should clarify whether this limitation applied to array names as well (e.g., would ARRAY1 and ARRAY2 be the same array?).

---

#### documentation_inconsistency

**Description:** Shortcuts documentation uses {{kbd:...}} template syntax but doesn't explain what this syntax means or how it's rendered.

**Affected files:**
- `docs/help/common/shortcuts.md`

**Details:**
shortcuts.md uses syntax like: "{{kbd:run:cli}}" and "{{kbd:run_program:tk}}"

No explanation of what these template tags mean or how they're processed. Should include a note explaining this is template syntax that gets replaced with actual key combinations.

---

#### documentation_inconsistency

**Description:** SWAP documentation doesn't specify what happens with array elements or whether you can swap array elements with scalar variables.

**Affected files:**
- `docs/help/common/language/statements/swap.md`

**Details:**
swap.md: "Any type variable may be SWAPped (integer, single precision, double precision, string), but the two variables must be of the same type"

Doesn't clarify:
- Can you SWAP A(1), A(2)?
- Can you SWAP A, B(1)?
- Can you SWAP A$(1), B$?

---

#### documentation_inconsistency

**Description:** WHILE-WEND documentation doesn't specify maximum nesting depth or what error occurs if nesting is too deep.

**Affected files:**
- `docs/help/common/language/statements/while-wend.md`

**Details:**
while-wend.md: "WHILE/WEND loops may be nested to any level."

Should specify:
- Is there a practical nesting limit?
- What error occurs if limit is exceeded?
- Does nesting depth affect performance?

---

#### documentation_inconsistency

**Description:** Settings documentation mentions 'File scope (future feature)' but doesn't explain what this would mean or when it might be available.

**Affected files:**
- `docs/help/common/settings.md`

**Details:**
settings.md: "1. **File scope** (highest priority) - Per-file settings (future feature)"

Should either:
- Remove this if not planned
- Add note about what file-scope settings would enable
- Indicate timeline or version when this might be available

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut documentation format

**Affected files:**
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/tk/index.md`

**Details:**
CLI docs use: '**{{kbd:stop:cli}}**' for keyboard shortcuts.

Tk docs use: '**{{kbd:file_new:tk}}**', '**{{kbd:run_program:tk}}**', etc.

The shortcut naming convention differs (stop vs file_new, run_program) which may indicate different template variable systems or inconsistent naming.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation of Find/Replace feature availability

**Affected files:**
- `docs/help/common/ui/curses/editing.md`
- `docs/help/common/ui/tk/index.md`

**Details:**
curses/editing.md does not mention Find or Replace functionality.

tk/index.md states: 'Find and replace' as an editor feature and lists '**{{kbd:find:tk}}** - Find' in keyboard shortcuts.

extensions.md clarifies: '**Find** ❌ (Curses) ✅ (Tk)' and '**Replace** ❌ (Curses) ✅ (Tk)'.

The Curses editing guide should explicitly state that Find/Replace is not available, rather than omitting it.

---

#### documentation_inconsistency

**Description:** Inconsistent cross-referencing to AUTO and RENUM commands

**Affected files:**
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/curses/editing.md`
- `docs/help/common/ui/tk/index.md`

**Details:**
All three UI docs reference AUTO and RENUM commands with 'See: [AUTO Command](../../language/statements/auto.md)' and similar.

However, the actual path structure is not verified. The docs use relative paths like '../../language/statements/' but we don't have those files in the provided documentation to verify the links are correct.

This is a potential broken link issue.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for 'this implementation' vs 'MBASIC-2025'

**Affected files:**
- `docs/help/mbasic/architecture.md`

**Details:**
architecture.md uses 'MBASIC' and 'this implementation' throughout.

Other docs (compatibility.md, extensions.md) use 'MBASIC-2025' as the official name.

The architecture doc should consistently use 'MBASIC-2025' or define the naming convention at the start.

---

#### documentation_inconsistency

**Description:** Inconsistent UI count - three vs four interfaces

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
getting-started.md section 'Choosing a User Interface' states 'MBASIC supports four interfaces' and lists CLI, Curses, Tkinter, and Web UI. However, features.md in multiple places refers to 'three UIs' or lists only CLI, Curses, and Tk without mentioning Web UI in the main features list. The Web UI section appears later but isn't consistently included in counts.

---

#### documentation_inconsistency

**Description:** STEP command implementation status unclear

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/debugging.md`

**Details:**
cli/debugging.md shows 'Planned (not yet implemented): STEP INTO - Step into subroutines (planned), STEP OVER - Step over subroutine calls (planned)' but features.md lists 'Step execution - Execute one line at a time (available in all UIs)' without mentioning these limitations or planned features.

---

#### documentation_inconsistency

**Description:** Documentation structure description mismatch

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/index.md`

**Details:**
index.md states 'This documentation is organized in three tiers: 1. MBASIC Implementation, 2. BASIC-80 Language Reference, 3. UI-Specific Guides'. However, features.md and other docs don't consistently follow or reference this three-tier structure. Some cross-references use different organizational language.

---

#### documentation_inconsistency

**Description:** Settings commands not listed in features

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/settings.md`

**Details:**
cli/settings.md documents SHOWSETTINGS and SETSETTING commands in detail, but features.md does not list these under 'Program Control' or 'Direct Commands' sections. These are significant CLI features that should be mentioned in the main features list.

---

#### documentation_inconsistency

**Description:** CLS implementation details inconsistency

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
not-implemented.md states 'Basic CLS (clear screen) IS implemented in MBASIC' with a note that 'The GW-BASIC extended CLS with optional parameters is not implemented'. features.md lists 'CLS - Clear screen' without mentioning this limitation. Users might expect GW-BASIC style CLS parameters to work.

---

#### documentation_inconsistency

**Description:** Function count discrepancy

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/index.md`

**Details:**
features.md section heading states 'Functions (45+)' but cli/index.md states 'Functions - All 40 functions'. This is a 5+ function discrepancy that should be reconciled.

---

#### documentation_inconsistency

**Description:** Statement count discrepancy

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/index.md`

**Details:**
cli/index.md states 'Statements - All 63 statements' but features.md doesn't provide a specific count. If there are 63 statements, this should be mentioned in features.md for consistency.

---

#### documentation_inconsistency

**Description:** Error code count discrepancy

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/index.md`

**Details:**
cli/index.md states 'Error Codes - All 68 error codes' but features.md doesn't mention the number of error codes. This specific count should be included in features.md for completeness.

---

#### documentation_inconsistency

**Description:** Variable sorting default order inconsistency

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
In variables.md: "Press `s` to cycle through sort orders:
- **Accessed**: Most recently accessed (read or written) - shown first (default)"

In feature-reference.md: "### Variable Sorting (s key in variables window)
Cycle through different sort orders:
- **Accessed**: Most recently accessed (read or written) - newest first"

Both mention 'Accessed' as default but use slightly different wording ('shown first' vs 'newest first'). This is minor but could be standardized.

---

#### documentation_inconsistency

**Description:** Variable filtering options inconsistency

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
In variables.md: "Press `f` to cycle through filters:
- **All**: Show all variables
- **Scalars**: Hide arrays
- **Arrays**: Show only arrays
- **Modified**: Show recently changed"

In feature-reference.md: "### Variable Filtering (f key in variables window)
Filter the variables list to show only variables matching a search term."

The feature-reference.md describes filtering as a search function, while variables.md describes it as cycling through predefined filter types. These are different features. The feature-reference.md should be updated to match the actual filtering behavior described in variables.md.

---

#### documentation_inconsistency

**Description:** Keyboard reference table incomplete

**Affected files:**
- `docs/help/ui/curses/variables.md`

**Details:**
In variables.md, the 'Keyboard Reference' section lists:
| Key | Action |
|-----|--------|
| `{{kbd:toggle_variables:curses}}` | Open/focus variables window |
| `Esc` | Close window |
| `Tab` | Switch between windows |
| `↑↓` | Navigate variables |
| `/` | Search |
| `f` | Filter |
| `s` | Sort |
| `r` | Refresh |
| `u` | Toggle auto-update |
| `e` | Export to file |
| `h` | Help |

However, earlier in the document it mentions:
- `n` for next search match
- `N` for previous search match
- `d` for toggle sort direction
- `v` for toggle value truncation
- `t` for toggle type display
- `w` for word wrap
- `p` for pin window
- `q` for close (alternative to Esc)

These keys are not in the reference table. The table should be complete or note that it's a subset.

---

#### documentation_inconsistency

**Description:** Save keyboard shortcut explanation inconsistency

**Affected files:**
- `docs/help/ui/curses/files.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
In files.md: "1. Press **{{kbd:save:curses}}** to save (Ctrl+S unavailable - terminal flow control)"

In quick-reference.md: "| **{{kbd:save:curses}}** | Save program (Ctrl+S unavailable - terminal flow control) |"

Both mention Ctrl+S is unavailable due to terminal flow control, but neither explains what {{kbd:save:curses}} actually is. The documentation should clarify what key combination {{kbd:save:curses}} represents (likely Ctrl+W based on context).

---

#### documentation_inconsistency

**Description:** Display options shortcuts may not be implemented

**Affected files:**
- `docs/help/ui/curses/variables.md`

**Details:**
In variables.md under 'Window Controls':
"### Display Options
- **v**: Toggle value truncation
- **t**: Toggle type display
- **d**: Show decimal/hex toggle
- **w**: Word wrap long strings"

These display option shortcuts are mentioned but not included in the 'Keyboard Reference' table later in the same document. Also, 'd' is mentioned earlier as 'toggle sort direction' but here as 'decimal/hex toggle'. This is a conflict.

---

#### documentation_inconsistency

**Description:** Export to file feature may not be implemented

**Affected files:**
- `docs/help/ui/curses/variables.md`

**Details:**
In variables.md, the keyboard reference table lists:
"| `e` | Export to file |"

And in tips: "4. **Export list**: Press `e` to save variable list to file"

However, this feature is not described anywhere else in the documentation. No explanation of what format the export uses, where it saves, or how to use the exported file. This may be a planned feature that's not yet implemented.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut references for Renumber

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/tips.md`

**Details:**
feature-reference.md states:
"Renumber ({{kbd:renumber:tk}})
Renumber program lines with specified start and increment.
- Menu: Edit → Renumber
- Shortcut: {{kbd:renumber:tk}}"

But tips.md states:
"Renumber (**{{kbd:renumber:tk}}**) before sharing code."

While both reference the same shortcut, tips.md uses bold formatting (**) around the kbd template, which is inconsistent with the rest of the documentation style. This is a minor formatting inconsistency.

---

#### documentation_inconsistency

**Description:** Inconsistent shortcut notation for Run Program

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
feature-reference.md states:
"Run Program ({{kbd:run_program:tk}} or F5)
Execute the current program from the beginning.
- Menu: Run → Run Program
- Shortcuts: {{kbd:run_program:tk}} or F5"

This suggests there are TWO shortcuts: one referenced by the kbd template and also F5. But it's unclear if these are the same shortcut or different shortcuts. If {{kbd:run_program:tk}} resolves to F5, then saying "or F5" is redundant. If they're different, it should be clarified.

---

#### documentation_inconsistency

**Description:** Inconsistent feature count in section headers

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
feature-reference.md has section headers like:
"## File Operations (8 features)"
"## Execution & Control (6 features)"
"## Debugging (6 features)"
"## Variable Inspection (6 features)"
"## Editor Features (7 features)"
"## Help System (4 features)"

But when counting the actual features listed under each section, the counts may not match. For example, under "Help System (4 features)" it lists: Help Command, Integrated Docs, Search Help, Context Help - which is indeed 4. However, this should be verified for all sections to ensure accuracy.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`

**Details:**
features.md uses template notation like: '{{kbd:find:web}}', '{{kbd:replace:web}}', '{{kbd:run:web}}', '{{kbd:step:web}}', etc.

But getting-started.md uses the same notation: '{{kbd:run:web}}', '{{kbd:stop:web}}', '{{kbd:step_line:web}}', '{{kbd:step:web}}', '{{kbd:continue:web}}'

However, web-interface.md uses different notation: '{{kbd:paste:web}}', '{{kbd:select_all:web}}', '{{kbd:copy:web}}'

The inconsistency is minor but the shortcut key names differ: 'step_line' vs 'step', and it's unclear if these template tags are meant to be rendered or are placeholders.

---

#### documentation_inconsistency

**Description:** Inconsistent description of Command area behavior

**Affected files:**
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
getting-started.md under 'Command Area' says: 'Type: PRINT 2+2\nClick Execute → Output shows: 4' - implying you must click Execute button.

But web-interface.md under 'Command (Bottom)' says: 'Type: PRINT 2+2\nPress Enter → Output shows: 4' - implying pressing Enter is sufficient.

Later, getting-started.md says: 'Type: PRINT 2+2\nPress Enter → Output shows: 4' - now agreeing with web-interface.md.

The inconsistency is whether you need to click Execute or just press Enter in the Command area.

---

#### documentation_inconsistency

**Description:** Missing 'Open Example' feature in menu documentation

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
web-interface.md under 'File Menu' states: 'Note: An "Open Example" feature to choose from sample BASIC programs is planned for a future release.'

But features.md under 'File Operations > Open Files (Planned)' lists: 'Recent files list' as planned, with no mention of 'Open Example' feature.

Also, the library index files (games/index.md, business/index.md, etc.) exist and document many example programs, suggesting the feature might be partially implemented or the documentation is outdated.

---

#### documentation_inconsistency

**Description:** Category name mismatch in header and footer

**Affected files:**
- `docs/library/electronics/index.md`

**Details:**
Header says '# MBASIC Electronics Programs' but the footer section says '## About These Electronics' (missing 'Programs'). Other library docs consistently use the full category name in the footer (e.g., 'About These Games', 'About These Ham Radio', 'About These Telecommunications').

---

#### documentation_inconsistency

**Description:** Inconsistent footer section naming pattern

**Affected files:**
- `docs/library/ham_radio/index.md`
- `docs/library/telecommunications/index.md`

**Details:**
Ham Radio footer says '## About These Ham Radio' and Telecommunications says '## About These Telecommunications', but these should probably be '## About These Ham Radio Programs' and '## About These Telecommunications Programs' to match the pattern in other libraries (Games, Utilities, etc.).

---

#### documentation_inconsistency

**Description:** Library statistics may be outdated

**Affected files:**
- `docs/library/index.md`

**Details:**
The index.md states '**Library Statistics:**
- 177 programs from the 1970s-1980s'

Counting the programs listed in the provided documentation:
- Games: ~130 programs
- Utilities: 19 programs
- Electronics: 13 programs
- Ham Radio: 7 programs
- Telecommunications: 5 programs

This totals approximately 174 programs visible in the provided docs, which is close to 177 but may not include Education, Business, Data Management, and Demos categories that are mentioned but not provided. The count should be verified against actual program files.

---

#### documentation_inconsistency

**Description:** Million.bas categorization inconsistency

**Affected files:**
- `docs/library/utilities/index.md`

**Details:**
Million.bas is described as 'Millionaire life simulation game - make financial decisions to accumulate wealth' with tags 'simulation, financial, game', but it's placed in the Utilities library rather than the Games library where it would seem to belong based on its description.

---

#### documentation_inconsistency

**Description:** Rotate.bas categorization inconsistency

**Affected files:**
- `docs/library/utilities/index.md`

**Details:**
Rotate.bas is described as 'Letter rotation puzzle game - order letters A-P by rotating groups clockwise' with tags 'puzzle, game, logic', but it's placed in the Utilities library rather than the Games library where games typically belong.

---

#### documentation_inconsistency

**Description:** Bearing.bas categorization inconsistency

**Affected files:**
- `docs/library/electronics/index.md`

**Details:**
Bearing.bas is described as 'Compute bearings between geographic coordinates - calculates distance and bearing between two latitude/longitude positions' with tags 'geography, navigation, coordinates, bearing'. This appears to be a navigation/geography utility rather than an electronics program. It might be better suited for a different category or the Utilities library.

---

#### documentation_inconsistency

**Description:** Reference to non-existent bug report link

**Affected files:**
- `docs/user/CASE_HANDLING_GUIDE.md`

**Details:**
The CASE_HANDLING_GUIDE.md is in docs/user/ but references features that aren't mentioned in the library documentation. More importantly, the library index.md states '⚠️ **Important:** These programs have had minimal testing by humans. If you encounter issues, please submit a bug report (link coming soon).' - the bug report link is marked as 'coming soon' but no actual link or instructions are provided.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation between documents

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`
- `docs/user/QUICK_REFERENCE.md`

**Details:**
CHOOSING_YOUR_UI.md uses plain text for shortcuts:
'**Unique advantages:**
- Keyboard shortcuts'

QUICK_REFERENCE.md uses template notation:
'| `{{kbd:new}}` | New | Clear program, start fresh |'
'| `{{kbd:open}}` | Load | Load program from file |'

The {{kbd:command}} notation is explained in QUICK_REFERENCE.md but not in CHOOSING_YOUR_UI.md, which could confuse users reading both documents.

---

#### documentation_inconsistency

**Description:** Performance measurements lack context and disclaimers

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
CHOOSING_YOUR_UI.md provides specific performance numbers:
'### Startup Time
1. **CLI**: ~0.1s (fastest)
2. **Curses**: ~0.3s
3. **Tk**: ~0.8s
4. **Web**: ~2s (includes browser launch time)'

and

'### Memory Usage (approximate)
1. **CLI**: 20MB (lowest)
2. **Curses**: 25MB
3. **Tk**: 40MB
4. **Web**: 50MB+ (Python process only; browser adds 100MB+)'

The document includes a note at the top of the Performance Comparison section, but these specific numbers could vary significantly based on system configuration, Python version, and installed dependencies. The note should be more prominent or repeated near the actual numbers.

---

#### documentation_inconsistency

**Description:** Inconsistent feature availability claims for Find/Replace

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
CHOOSING_YOUR_UI.md Decision Matrix shows:
'| **Find/Replace** | ❌ | ❌ | ✅ | ❌ |'

Indicating only Tk has Find/Replace. However, in the Curses limitations section:
'**Limitations:**
- Limited mouse support
- Partial variable editing
- No clipboard integration
- Terminal color limits
- No Find/Replace'

This is consistent. But in the Tk section:
'**Unique advantages:**
- Find/Replace dialogs'

The term 'dialogs' (plural) suggests multiple Find/Replace features, but the matrix only shows a single checkmark. This could be clarified to indicate whether Tk has separate Find and Replace dialogs or a combined Find/Replace dialog.

---

#### documentation_inconsistency

**Description:** Inconsistent boolean value notation in examples

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
SETTINGS_AND_CONFIGURATION.md shows:
'**Using SET command (in BASIC):**
```basic
SET "variables.case_conflict" "error"
SET "editor.auto_number" true
```'

and later:

'**Type Conversion:**
- Strings: `"value"` (with quotes)
- Numbers: `5` (without quotes)
- Booleans: `true` or `false` (lowercase, no quotes in both commands and JSON files)'

The examples are consistent with the type conversion rules, but the phrase 'no quotes in both commands and JSON files' could be clearer. In JSON, booleans are indeed unquoted, but the phrasing might confuse users about whether quotes are needed in SET commands (they are not, as shown in examples).

---

#### documentation_inconsistency

**Description:** Ambiguous keyboard shortcut documentation

**Affected files:**
- `docs/user/QUICK_REFERENCE.md`

**Details:**
QUICK_REFERENCE.md states:
'> **Note:** This reference uses `{{kbd:command}}` notation for keyboard shortcuts (e.g., `{{kbd:run}}` is typically `^R` for Ctrl+R). Actual key mappings are configurable. To see your current key bindings, press the Help key or check `~/.mbasic/curses_keybindings.json` for the full list of default and customized keys.'

The phrase 'typically `^R`' suggests this is the default but might not be accurate for all users. The document should either:
1. State definitively what the default is, or
2. Remove 'typically' and just say 'configurable (default: ^R)' or
3. Not provide specific examples if they vary

This is minor but could confuse users who have different defaults.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut template notation between documents

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
TK_UI_QUICK_START.md uses notation like {{kbd:run_program}}, {{kbd:file_save}}, {{kbd:smart_insert}} without UI suffix.

UI_FEATURE_COMPARISON.md uses notation with UI suffix like {{kbd:run:cli}}, {{kbd:run:curses}}, {{kbd:run_program:tk}}, {{kbd:run:web}}, {{kbd:save:cli}}, {{kbd:save:curses}}, {{kbd:file_save:tk}}, {{kbd:save:web}}.

The comparison guide explicitly states: 'This guide uses {{kbd:action:ui}} notation for keyboard shortcuts' but TK_UI_QUICK_START.md does not follow this convention consistently (no :tk suffix).

---

#### documentation_inconsistency

**Description:** Inconsistent feature status for Find/Replace in Web UI

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
UI_FEATURE_COMPARISON.md Feature Availability Matrix shows:
- Find/Replace for Web: 📋 (Planned for future implementation)
- Notes: 'Tk: implemented, Web: planned'

UI_FEATURE_COMPARISON.md 'Feature Implementation Status' section under 'Coming Soon' lists:
- '⏳ Find/Replace in Web UI'

However, TK_UI_QUICK_START.md does not mention this limitation when discussing Find/Replace, only noting it as 'Tk UI only' in the keyboard shortcuts table.

---

#### documentation_inconsistency

**Description:** Inconsistent symbol usage in Feature Availability Matrix

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
The Legend defines:
- ⚠️ Partially implemented (see Notes column for details)
- 📋 Planned for future implementation (not yet available)

However, in 'Feature Implementation Status' section, different symbols are used:
- ✅ for 'Recently Added'
- ⏳ for 'Coming Soon' (not 📋 as defined in legend)

The ⏳ symbol is not defined in the legend but is used to indicate planned features, creating confusion with the 📋 symbol.

---

#### documentation_inconsistency

**Description:** Inconsistent information about CLI save functionality

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
UI_FEATURE_COMPARISON.md Feature Availability Matrix shows:
- Save (interactive) for CLI: ❌
- Save (command) for CLI: ✅
- Notes: 'Keyboard shortcut prompts for filename'

However, in 'Detailed UI Descriptions' under CLI Limitations, it states:
- 'No interactive save prompt (must use SAVE "filename" command)'

And in 'Known Gaps' section:
- 'CLI: No interactive save prompt (use SAVE "filename" command instead)'

The note 'Keyboard shortcut prompts for filename' in the matrix seems to apply to other UIs, not CLI, but its placement in the Notes column is ambiguous about which UIs it refers to.

---

#### documentation_inconsistency

**Description:** Keyboard shortcuts document title does not match referenced location

**Affected files:**
- `docs/user/keyboard-shortcuts.md`

**Details:**
The file docs/user/keyboard-shortcuts.md is titled 'MBASIC Curses UI Keyboard Shortcuts' indicating it documents Curses UI shortcuts.

However, TK_UI_QUICK_START.md references it as 'See [Tk Keyboard Shortcuts](keyboard-shortcuts.md)' suggesting it should contain Tk shortcuts.

This creates confusion about which UI's shortcuts are documented in this file.

---

#### documentation_inconsistency

**Description:** Missing reference to actual keyboard shortcuts documentation

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
TK_UI_QUICK_START.md states at the top: 'Actual key mappings shown in the Help menu (Help → Keyboard Shortcuts) or in the Tk UI documentation.'

And in 'Next Steps' section: 'Keyboard Shortcuts: See [Tk Keyboard Shortcuts](keyboard-shortcuts.md)'

However, keyboard-shortcuts.md only contains Curses UI shortcuts, not Tk UI shortcuts. There is no separate Tk UI keyboard shortcuts documentation file referenced or available.

---


## Summary

- Total issues found: 707
- Code/Comment conflicts: 238
- Other inconsistencies: 469
