# Documentation & Comment Inconsistencies - v19

Generated: 2025-11-10
Source: docs_inconsistencies_report-v19.md  
Category: Documentation issues, code comments where code works correctly

#### Code vs Documentation inconsistency

**Description:** SandboxedFileIO methods documented as STUB but some are partially implemented

**Affected files:**
- `src/file_io.py`

**Details:**
Documentation states all methods except list_files() are STUB implementations that raise IOError. However, list_files() is fully implemented and delegates to backend.sandboxed_fs. The documentation says "Implementation status: - list_files(): IMPLEMENTED" but then the docstrings for load_file, save_file, delete_file, and file_exists all say "STUB: Raises error (requires async refactor)" which is accurate. The inconsistency is that the class docstring claims these are stubs but doesn't explain why list_files() works while others don't.

---



#### Documentation inconsistency

**Description:** Contradictory information about storage location for SandboxedFileIO

**Affected files:**
- `src/file_io.py`

**Details:**
Class docstring for SandboxedFileIO states:
"Storage location: Python server memory (NOT browser localStorage or disk files).
Why server memory? Web UI runs Python interpreter on server, not in browser."

But earlier in the module docstring it says:
"* SandboxedFileIO: In-memory virtual filesystem on Python server (Web UI - NOT browser storage)"

These are consistent, but then the class docstring also says:
"Lifetime: Files exist only during the server session (cleared on restart)."

This contradicts typical web application behavior where you'd want persistence. The documentation should clarify if this is intentional (ephemeral storage) or a limitation.

---



#### code_vs_comment

**Description:** emit_keyword docstring requires lowercase input but serialize_rem_statement passes uppercase comment_type from parser, then converts to lowercase before calling emit_keyword. This suggests the parser stores uppercase but serializer expects lowercase.

**Affected files:**
- `src/position_serializer.py`

**Details:**
emit_keyword docstring: 'Args:
    keyword: The keyword to emit (must be normalized lowercase by caller, e.g., "print", "for")'

But serialize_rem_statement comment says: 'Note: stmt.comment_type is stored in uppercase by the parser ("APOSTROPHE", "REM", or "REMARK").
We convert to lowercase before passing to emit_keyword() which requires lowercase input.'

Code:
    else:
        # Apply keyword case to REM/REMARK (convert to lowercase for emit_keyword)
        result = self.emit_keyword(stmt.comment_type.lower(), stmt.column, "RemKeyword")

This reveals an inconsistency: the parser stores keywords in uppercase, but emit_keyword requires lowercase. This conversion burden is placed on each call site.

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

**Description:** Dead code comment contradicts actual implementation state

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Method _setup_immediate_context_menu() has comment:
"DEAD CODE: This method is never called because immediate_history is always None in the Tk UI (see __init__). Retained for potential future use if immediate mode gets its own output widget."

However, the method references self.immediate_history which doesn't exist in the visible code, and related methods _copy_immediate_selection() and _select_all_immediate() also reference this non-existent widget. If truly dead code, these methods should be removed or the comment should explain why they're kept.

---



#### code_vs_comment

**Description:** Comment describes maintenance risk with duplicated logic that may cause bugs

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_immediate() method, comment states:
"NOTE: Don't call interpreter.start() because it calls runtime.setup() which resets PC to the first statement. The RUN command has already set PC to the correct line (e.g., RUN 120 sets PC to line 120). Instead, we manually perform minimal initialization here.

MAINTENANCE RISK: This duplicates part of start()'s logic. If start() changes, this code may need to be updated to match."

This indicates fragile code that manually replicates initialization logic instead of using proper abstraction. If interpreter.start() changes, this code will silently break.

---



#### documentation_inconsistency

**Description:** Contradictory information about EDIT command availability

**Affected files:**
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/curses/editing.md`

**Details:**
CLI docs state 'The CLI includes a line editor accessed with the EDIT command' and references 'See: [EDIT Command](../../language/statements/edit.md)', but Curses docs make no mention of an EDIT command despite being a full-screen editor. The CLI description suggests EDIT is a command-mode feature, but it's unclear if this exists in CLI or if it's confused with the Curses full-screen editor.

---



#### documentation_inconsistency

**Description:** Contradictory information about STEP INTO/OVER implementation

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/debugging.md`

**Details:**
features.md under 'Debugging' states:
'- **Step execution** - Execute one line at a time (available in all UIs; access method varies)'

However, cli/debugging.md under 'STEP - Single-Step Execution' shows:
'**Syntax:**
STEP [n]               - Execute n statements (default: 1)
STEP INTO             - Step into subroutines
STEP OVER             - Step over subroutine calls'

But then in the 'Limitations' section states:
'- STEP INTO/OVER not yet implemented (use STEP)'

This is contradictory - the syntax section suggests STEP INTO/OVER are available, but limitations say they're not implemented.

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
- Find: {{kbd:find:tk}}
- Replace: {{kbd:replace:tk}}"

But features.md states:
"Find text ({{kbd:find:tk}}):
- Opens Find dialog with search options

Replace text ({{kbd:replace:tk}}):
- Opens combined Find/Replace dialog

**Note:** {{kbd:find:tk}} opens the Find dialog. {{kbd:replace:tk}} opens the Find/Replace dialog which includes both Find and Replace functionality."

These descriptions conflict - feature-reference.md implies separate Find and Replace dialogs, while features.md explicitly states that {{kbd:replace:tk}} opens a combined dialog that includes both functions.

---



#### documentation_inconsistency

**Description:** Auto-Save feature documented but settings indicate it's not implemented

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/settings.md`

**Details:**
feature-reference.md lists under File Operations:
"### Auto-Save
Tk UI supports auto-save functionality. Programs are periodically saved to prevent data loss.
- Configurable interval
- Creates backup files"

However, settings.md states at the top:
"**Implementation Status:** The Tk (Tkinter) desktop GUI is planned to provide the most comprehensive settings dialog. **The features described in this document represent planned/intended implementation and are not yet available.**"

And later: "**Current Status:** Most features described below are not yet implemented."

If the settings dialog isn't implemented, it's unclear how Auto-Save's "configurable interval" would be configured. This suggests Auto-Save may also not be implemented, but feature-reference.md presents it as a current feature without any implementation status warning.

---



#### documentation_inconsistency

**Description:** Renumber feature implementation status unclear

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/workflows.md`
- `docs/help/ui/tk/tips.md`

**Details:**
feature-reference.md lists Renumber as a current feature:
"### Renumber ({{kbd:renumber:tk}})
Renumber program lines with specified start and increment.
- Menu: Edit → Renumber
- Shortcut: {{kbd:renumber:tk}}
- Opens dialog for configuration"

workflows.md describes using it:
"## 5. Renumber Before Sharing
1. Press **{{kbd:renumber:tk}}** (Renumber)
2. Set Start=10, Increment=10
3. Click 'Renumber'
4. All GOTO/GOSUB references automatically updated!"

tips.md also references it:
"## Renumber Before Sharing
Keep development line numbers messy, but Renumber (**{{kbd:renumber:tk}}**) before sharing code."

However, workflows.md has a note: "**Note:** Some features described below (Smart Insert, Variables Window, Execution Stack, Renumber dialog) are documented here based on the Tk UI design specifications. Check [Settings](settings.md) for current implementation status..."

This creates confusion - is Renumber implemented or not? feature-reference.md presents it as current, but workflows.md suggests it may be planned.

---



#### documentation_inconsistency

**Description:** Web UI debugging documentation describes many unimplemented features without clear status markers

**Affected files:**
- `docs/help/ui/web/debugging.md`

**Details:**
The document has inconsistent implementation status markers. Some sections clearly state "(Planned)" or "**Note:** The following features are planned..." but many sections describe features in present tense without clarification:

- "Variables Panel" section describes detailed UI that is then marked as "(Planned)"
- "Call Stack" section describes features, then has a note saying it's "not yet implemented"
- "Execution Flow" section describes features in present tense, then has a note saying they're "planned for future releases"
- "Advanced Debugging" section is entirely marked as planned
- "Debug Settings" section is marked as planned

But the "Overview" section states current capabilities without marking what's actually implemented vs planned:
"The Web UI debugger currently offers:
- Basic breakpoint management (via Run menu)
- Step-by-step execution
- Basic variable inspection (via Debug menu)
- Visual indicators in editor"

This creates confusion about what actually works now vs what's planned.

---



#### documentation_inconsistency

**Description:** Contradictory information about file persistence and auto-save functionality

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
features.md states:
- 'Programs stored in Python server memory (session-only, lost on page refresh)'
- 'Recent files list stored in browser localStorage'
- Under 'Automatic Saving (Planned)': 'Saves programs to browser localStorage for persistence'

But getting-started.md states:
- 'Note: The Web UI uses browser downloads for saving program files to your computer. Auto-save of program code to browser localStorage is planned for a future release. (Note: Your editor settings ARE already saved to localStorage - see [Settings](settings.md))'

And web-interface.md states:
- 'Important: Programs and data created via BASIC file I/O commands (OPEN, PRINT #, etc.) exist only in memory during your browser session. To save your BASIC program source code permanently, use File → Save to download it to your computer.'

The features.md document contradicts itself by listing localStorage storage as 'Currently Implemented' for recent files but 'Planned' for automatic program saving.

---



#### documentation_inconsistency

**Description:** Contradictory information about Step/Continue/Stop keyboard shortcuts

**Affected files:**
- `docs/user/QUICK_REFERENCE.md`
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
QUICK_REFERENCE.md (for Curses UI) shows keyboard shortcuts for debugging: 'c' or 'C' for Continue, 's' or 'S' for Step, 'e' or 'E' for End. TK_UI_QUICK_START.md explicitly states: 'Note: Step, Continue, and Stop are available via toolbar buttons or the Run menu (no keyboard shortcuts).' This is a direct contradiction - either Tk UI has different shortcuts than Curses, or one document is incorrect.

---

### 🟡 Medium Severity



#### Documentation inconsistency

**Description:** Version number inconsistency between setup.py and ast_nodes.py module docstring

**Affected files:**
- `setup.py`
- `src/ast_nodes.py`

**Details:**
setup.py states 'Package version: 0.99.0 (reflects approximately 99% implementation status - core complete)' and 'Language version: MBASIC 5.21 (Microsoft BASIC-80 for CP/M)'. The ast_nodes.py module docstring only mentions '5.21 refers to the Microsoft BASIC-80 language version, not this package version' but doesn't mention the package version 0.99.0 anywhere. This creates potential confusion about versioning.

---



#### Code vs Comment conflict

**Description:** VariableNode type_suffix and explicit_type_suffix documentation may be confusing

**Affected files:**
- `src/ast_nodes.py`

**Details:**
VariableNode has complex documentation for type_suffix handling: 'type_suffix: The actual suffix character ($, %, !, #) when present' and 'explicit_type_suffix: Boolean indicating the origin of type_suffix: True: suffix appeared in source code (e.g., "X%" in "X% = 5"), False: suffix inferred from DEFINT/DEFSNG/DEFDBL/DEFSTR'. The example states 'In "DEFINT A-Z: X=5", variable X has type_suffix=\'%\' and explicit_type_suffix=False.' However, this creates ambiguity: if type_suffix is present when explicit_type_suffix=False, how do you distinguish between no suffix and inferred suffix? The comment 'Both fields must always be examined together' suggests complexity that may indicate a design issue.

---



#### code_vs_comment

**Description:** Comment describes EOF() behavior for mode 'I' files but implementation details reference is incomplete

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Comment at line 717-726 states:
"Note: For binary input files (OPEN statement mode 'I'), respects ^Z (ASCII 26)
as EOF marker (CP/M style).

Implementation details:
- execute_open() in interpreter.py stores mode ('I', 'O', 'A', 'R') in file_info['mode']
- Mode 'I' files are opened with binary=True, allowing ^Z detection
- Text mode files (output 'O', append 'A') use standard Python EOF detection without ^Z
- See execute_open() in interpreter.py lines 2313-2369 for file opening implementation"

However, the actual implementation at lines 735-756 shows:
- Line 735: "if file_info['mode'] == 'I':"
- Line 741-742: "# Binary mode files ('rb'): read(1) returns bytes object
# next_byte[0] accesses the first byte value as integer (0-255)"
- Line 747: "elif next_byte[0] == 26:  # ^Z (ASCII 26)"

The comment references 'binary=True' parameter but code comment says files are opened with 'rb' mode. These are related but not identical concepts.

---



#### code_vs_comment

**Description:** Comment about negative zero handling describes behavior but implementation logic is complex

**Affected files:**
- `src/basic_builtins.py`

**Details:**
At lines 277-283, comment states:
"# Determine sign - preserve negative sign for values that round to zero.
# Use original_negative (captured above before rounding) to detect negative values that rounded to zero.
# This allows us to detect cases like -0.001 which round to 0 but should display as "-0" (not "0").
# This matches MBASIC 5.21 behavior: negative values that round to zero display as "-0",
# while positive values that round to zero display as "0"."

Then at lines 284-288:
"if rounded == 0 and original_negative:
    is_negative = True
else:
    is_negative = rounded < 0"

The comment is accurate but the logic could be clearer. The 'else' branch sets is_negative based on rounded value, but for non-zero values, original_negative and (rounded < 0) should always match. The comment doesn't explain why we need the else branch.

---



#### code_vs_comment

**Description:** INPUT function docstring describes BASIC syntax with # but implementation note says # is stripped

**Affected files:**
- `src/basic_builtins.py`

**Details:**
At lines 862-873:
"INPUT$ - Read num characters from keyboard or file.
(Method name is INPUT since Python doesn't allow $ in names)

BASIC syntax:
    INPUT$(n) - read n characters from keyboard
    INPUT$(n, #filenum) - read n characters from file

Python call syntax (from interpreter):
    INPUT(n) - read n characters from keyboard
    INPUT(n, filenum) - read n characters from file

Note: The # prefix in BASIC syntax is stripped by the parser before calling this method."

The note at the end clarifies that # is stripped, but the docstring shows both BASIC syntax (with #) and Python call syntax (without #). This could be clearer by stating upfront that the function receives the file number without the # prefix.

---



#### Documentation inconsistency

**Description:** Conflicting documentation about FileIO vs ProgramManager file operations

**Affected files:**
- `src/file_io.py`
- `src/editing/manager.py`

**Details:**
src/file_io.py states: "FileIO.load_file() returns raw file content (string), caller passes to ProgramManager" but src/editing/manager.py's load_from_file() method uses direct Python file I/O (open(filename, 'r')) instead of using FileIO abstraction. The documentation claims ProgramManager.load_from_file() is separate from FileIO, but this creates confusion about when to use which interface.

---



#### Code vs Documentation inconsistency

**Description:** ProgramManager file operations documentation contradicts actual implementation

**Affected files:**
- `src/editing/manager.py`

**Details:**
Module docstring states:
"FILE I/O ARCHITECTURE:
This manager provides direct Python file I/O methods (load_from_file, save_to_file)
for local UIs (CLI, Curses, Tk) to load/save .BAS program files via UI menus/dialogs.
This is separate from the two filesystem abstractions"

But then it says:
"Why ProgramManager has its own file I/O methods:
- Provides simpler API for local UI menu operations (File > Open/Save dialogs)
- Only used by local UIs (CLI, Curses, Tk) where filesystem access is safe
- Separate from BASIC command flow: UI menus call ProgramManager directly,
  BASIC commands (LOAD/SAVE) go through FileIO abstraction first"

This creates confusion: if LOAD/SAVE commands go through FileIO, but ProgramManager also has load_from_file/save_to_file, when should each be used? The architecture is unclear.

---



#### Code vs Documentation inconsistency

**Description:** get_compiler_command documentation doesn't match implementation details

**Affected files:**
- `src/codegen_backend.py`

**Details:**
Method docstring says:
"Return z88dk.zcc command for CP/M compilation"

But implementation returns:
return ['/snap/bin/z88dk.zcc', '+cpm', source_file, '-create-app', '-lm', '-o', output_file]

The hardcoded path '/snap/bin/z88dk.zcc' assumes snap installation on Linux. This won't work on other platforms or if z88dk is installed differently. Documentation should mention this platform-specific assumption.

---



#### code_vs_comment

**Description:** Comment claims 'We do not save/restore the PC before/after execution by design' to allow RUN to change execution position, but this design choice could have unintended consequences for other control flow statements that are explicitly discouraged in the help text

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Code comment in execute() method:
"# Note: We do not save/restore the PC before/after execution by design.
# This allows statements like RUN to properly change execution position.
# Control flow statements (GOTO, GOSUB) can also modify PC but are not recommended
# in immediate mode as they may produce unexpected results (see help text)."

Help text says:
"• GOTO, GOSUB, and control flow statements are not recommended
  (they will execute but may produce unexpected results)"

The design intentionally allows PC modification for RUN but acknowledges this creates problems for GOTO/GOSUB. This seems like a design tradeoff rather than an inconsistency, but the comment could be clearer about why this tradeoff was chosen.

---



#### code_vs_comment

**Description:** OutputCapturingIOHandler.input() docstring says 'INPUT statements are parsed and executed normally, but fail at runtime when the interpreter calls this input() method', but this contradicts the help text which says 'INPUT statement will fail at runtime in immediate mode'

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Docstring in OutputCapturingIOHandler.input():
"Input not supported in immediate mode.

Note: INPUT statements are parsed and executed normally, but fail
at runtime when the interpreter calls this input() method."

Help text in _show_help():
"LIMITATIONS:
───────────────────────────────────────────────────────────────────

  • INPUT statement will fail at runtime in immediate mode (use direct assignment instead)"

Both say INPUT fails at runtime, so this is actually consistent. However, the phrasing could be clearer - the docstring emphasizes that parsing succeeds (which is implementation detail), while help text focuses on user-facing behavior.

---



#### code_vs_comment

**Description:** Comment claims EDIT command is 'handled before parsing' but code shows it goes through execute_command() which is called AFTER line number processing

**Affected files:**
- `src/interactive.py`

**Details:**
Module docstring (line 8-9) says:
"- Direct commands: AUTO, EDIT, HELP (handled before parsing)"

But in process_line() (line 186-203), numbered lines are processed first, then execute_command() is called for non-numbered lines. execute_command() (line 205-228) then handles EDIT as a special case.

The comment suggests EDIT is handled before any parsing, but it's actually handled after line number detection and as part of command execution flow.

---



#### code_vs_comment

**Description:** Comment about digit handling in EDIT says 'no output, no cursor movement, no error' but doesn't explain this is intentional MBASIC compatibility behavior

**Affected files:**
- `src/interactive.py`

**Details:**
cmd_edit() docstring (line 803-820) says:
"Note: Count prefixes ([n]D, [n]C) and search commands ([n]S, [n]K) are not yet implemented.
INTENTIONAL BEHAVIOR: When digits are entered, they fall through the command checks and are not processed (no output, no cursor movement, no error). This happens because there's no explicit digit handling - they simply don't match any elif branch. This preserves MBASIC compatibility where digits are reserved for count prefixes in the full EDIT implementation."

The comment explains the behavior but the code (lines 850-920) has no digit handling at all - digits silently do nothing. The comment says this is intentional for MBASIC compatibility, but a reader might expect an error message or some indication that digits are reserved.

---



#### code_vs_comment

**Description:** _renum_erl_comparison() docstring claims to handle 'ERL binary operations' but implementation only checks for ERL on left side, not general binary operations with ERL

**Affected files:**
- `src/interactive.py`

**Details:**
Function docstring (line 732-758) says:
"Handle ERL binary operations in expressions"

But the implementation (lines 760-776) only checks:
"if type(left).__name__ == 'VariableNode' and left.name == 'ERL':"

This only handles ERL on the LEFT side of binary operations. If ERL appears on the right side (e.g., '100 = ERL'), it won't be detected. The docstring should say 'Handle ERL on left side of binary operations' to match implementation.

---



#### code_vs_comment_conflict

**Description:** Comment claims immediate mode GOTO/GOSUB behavior is 'not recommended' but code fully supports it with documented semantics

**Affected files:**
- `src/interactive.py`

**Details:**
In execute_immediate() method around line 1050:

Comment says: "This is the intended behavior but may be unexpected, hence 'not recommended'."

However, the code implements a complete and well-defined behavior:
1. Saves old PC
2. Executes statement (allowing GOTO/GOSUB to work)
3. Restores old PC to preserve CONT functionality

The comment suggests this is problematic ('not recommended'), but the implementation is intentional and functional. The comment appears to be expressing uncertainty about design rather than documenting actual issues.

---



#### code_vs_comment_conflict

**Description:** Comment describes GOTO/GOSUB semantics as 'special' but doesn't explain they differ from standard MBASIC behavior

**Affected files:**
- `src/interactive.py`

**Details:**
In execute_immediate() around line 1045:

Comment: "Note: GOTO/GOSUB in immediate mode work but have special semantics:\nThey execute and jump during execute_statement(), but we restore the\noriginal PC afterward to preserve CONT functionality."

This describes implementation details but doesn't clarify whether this matches original MBASIC behavior or is a deviation. In classic MBASIC, immediate mode GOTO would typically transfer control permanently, not restore PC. The comment should clarify if this is intentional compatibility or a design choice.

---



#### code_vs_comment

**Description:** Comment states WEND pops loop 'after setting npc above, before WHILE re-executes' but timing explanation could be clearer

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1070 states:
# Pop the loop from the stack (after setting npc above, before WHILE re-executes).
# Timing: We pop NOW so the stack is clean before WHILE condition re-evaluation.
# The WHILE will re-push if its condition is still true, or skip the loop body
# if false. This ensures clean stack state and proper error handling if the
# WHILE condition evaluation fails (loop already popped, won't corrupt stack).

The comment explains the timing well, but the phrase 'after setting npc above, before WHILE re-executes' is slightly ambiguous - it could mean 'after the npc assignment statement above' or 'after setting npc but before WHILE executes'. The detailed explanation clarifies this, but the first sentence could be more precise.

---



#### code_vs_comment

**Description:** Comment about CLEAR state preservation mentions user_functions but doesn't mention other preserved state

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1250 states:
# State preservation for CHAIN compatibility:
#
# PRESERVED by CLEAR (not cleared):
#   - runtime.common_vars (list of COMMON variable names - the list itself, not values)
#   - runtime.user_functions (DEF FN functions)
#
# NOT PRESERVED (cleared above):
#   - All variables and arrays
#   - All open files (closed and cleared)
#   - Field buffers

This comment doesn't mention whether other runtime state like error handlers, FOR/WHILE loop stacks, GOSUB stack, DATA pointer, etc. are preserved or cleared. The comment should be more comprehensive about what state is affected.

---



#### code_vs_comment

**Description:** Comment about INPUT state machine mentions input_file_number but says 'Currently always None'

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1350 states:
Note: input_file_number is set to None for keyboard input and file# for file input.
This allows the UI to distinguish between keyboard prompts (show in UI) and file input
(internal, no prompt needed). Currently always None since file input bypasses this path.

The phrase 'Currently always None' suggests this is a temporary state or incomplete implementation, but the comment also explains that file input bypasses the state machine. This is confusing - if file input always bypasses the state machine, then input_file_number will always be None for the state machine path, which is by design, not a temporary limitation.

---



#### code_vs_comment

**Description:** Comment claims LSET/RSET fallback is 'documented behavior, not a bug', but there is no actual documentation of this extension behavior

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_lset() and execute_rset(), the comment states:
'Compatibility note: In strict MBASIC 5.21, LSET/RSET are only for field variables (used with FIELD statement for random file access). This fallback is a deliberate extension that performs simple assignment without left-justification. The formatting only applies when used with FIELD variables. This is documented behavior, not a bug.'

However, no documentation file is provided that describes this extension. The comment claims it's 'documented behavior' but there's no evidence of such documentation in the provided files.

---



#### internal_inconsistency

**Description:** Inconsistent handling of out-of-bounds conditions in MID$ assignment

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_midassignment(), the comment states:
'Validate start position (must be within string: 0 <= start_idx < len)
Note: start_idx == len(current_value) is considered out of bounds (can't start replacement past end)'

However, the code checks:
if start_idx < 0 or start_idx >= len(current_value):
    return

This means if start_idx equals len(current_value), it returns (no replacement). But the subsequent code calculates:
chars_to_replace = min(length, len(new_value), len(current_value) - start_idx)

If start_idx == len(current_value), then (len(current_value) - start_idx) = 0, which would naturally result in no replacement anyway. The early return is redundant but the comment suggests it's a special case.

---



#### Code vs Documentation inconsistency

**Description:** console.py input_line() documentation claims Python's input() preserves leading/trailing spaces, but this contradicts the base.py KNOWN LIMITATION that says console may vary by platform

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/console.py`

**Details:**
console.py says: "Note: Python's input() strips only the trailing newline, preserving leading/trailing spaces. However, terminal input behavior may vary across platforms."

base.py says: "console: Python input() strips the trailing newline. Leading/trailing spaces are generally preserved, but terminal behavior may vary by platform."

The console.py comment is more definitive ("preserving") while base.py is more cautious ("generally preserved"). This creates ambiguity about the actual behavior.

---



#### Code vs Documentation inconsistency

**Description:** web_io.py has get_screen_size() method not defined in IOHandler base interface, but no documentation explains this is web-specific

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
web_io.py implements:
def get_screen_size(self):
    """Get terminal size.
    Returns: Tuple of (rows, cols) - returns reasonable defaults for web
    Note: This is a web_io-specific method, not part of the IOHandler base interface."""
    return (24, 80)

The docstring acknowledges it's not part of the base interface, but __init__.py and base.py don't document that implementations may have additional methods beyond the interface.

---



#### code_vs_comment

**Description:** Comment claims at_end_of_line() does NOT check for COLON or comment tokens, but the method description contradicts this and suggests using at_end_of_statement() instead

**Affected files:**
- `src/parser.py`

**Details:**
at_end_of_line() docstring says:
"Important: This does NOT check for COLON or comment tokens. For statement parsing,
use at_end_of_statement() instead to properly stop at colons and comments."

But at_end_of_statement() docstring says:
"A statement ends at:
- End of line (NEWLINE or EOF)
- Statement separator (COLON) - allows multiple statements per line
- Comment (REM, REMARK, or APOSTROPHE) - everything after is ignored"

The comment in at_end_of_line() warns about NOT checking COLON/comments, but then says to use at_end_of_statement() which DOES check them. This creates confusion about when to use which method.

---



#### code_vs_comment

**Description:** Comment in parse_statement() for MID$ detection mentions catching ParseError during lookahead, but the error handling strategy is unclear

**Affected files:**
- `src/parser.py`

**Details:**
In parse_statement() MID$ detection:
"except (IndexError, ParseError):
    # Catch lookahead failures during MID$ statement detection
    # IndexError: if we run past end of tokens
    # ParseError: if malformed syntax encountered during lookahead
    # Position is restored below, so proper error will be reported later if needed
    pass"

The comment says 'proper error will be reported later if needed', but the code then raises:
"raise ParseError(f'MID$ must be used as function (in expression) or assignment statement', token)"

This suggests the error IS reported immediately, not 'later'. The comment may be outdated from a refactoring.

---



#### code_vs_comment

**Description:** Comment describes LINE_INPUT token behavior inconsistently with actual implementation

**Affected files:**
- `src/parser.py`

**Details:**
In parse_input() method around line 1050:

Comment states: "Note: The lexer tokenizes LINE keyword as LINE_INPUT token both when standalone (LINE INPUT statement) and when used as modifier (INPUT...LINE). The parser distinguishes these cases by context - LINE INPUT is a statement, INPUT...LINE uses LINE as a modifier within the INPUT statement."

However, the code checks for TokenType.LINE_INPUT in both contexts:
- line_mode = False
- if self.match(TokenType.LINE_INPUT):
    line_mode = True
    self.advance()

This suggests the lexer produces the same token type for both cases, which the comment confirms. The comment is accurate but could be clearer about why this design choice was made.

---



#### code_vs_comment

**Description:** Comment about separator behavior in LPRINT may be incomplete

**Affected files:**
- `src/parser.py`

**Details:**
In parse_lprint() method around line 1000:

Comment explains: "Separator count vs expression count:\n- If separators < expressions: no trailing separator, add newline\n- If separators >= expressions: has trailing separator, no newline added\nExamples: \"LPRINT A;B;C\" has 2 separators for 3 items (no trailing sep, adds \\n)\n           \"LPRINT A;B;C;\" has 3 separators for 3 items (trailing sep, no \\n)\n           \"LPRINT ;\" has 1 separator for 0 items (trailing sep, no \\n)"

The code implements:
if len(separators) < len(expressions):
    separators.append('\\n')

However, the comment doesn't explain what happens with mixed separators (comma vs semicolon) or how they affect output formatting differently. The code treats them the same for newline logic, but commas and semicolons have different spacing behavior in BASIC PRINT statements.

---



#### code_vs_comment

**Description:** parse_data() docstring says 'Line numbers (e.g., DATA 100 200) are treated as part of unquoted strings' but the code has a TokenType.LINE_NUMBER case that converts to string, suggesting line numbers might be tokenized separately rather than as identifiers

**Affected files:**
- `src/parser.py`

**Details:**
Docstring: "Unquoted strings extend until comma, colon, end of line, or unrecognized token.
Line numbers (e.g., DATA 100 200) are treated as part of unquoted strings."

Code has:
```python
elif tok.type == TokenType.LINE_NUMBER:
    string_parts.append(str(tok.value))
    self.advance()
```

This suggests LINE_NUMBER tokens exist and are handled specially. If line numbers in DATA statements are truly 'part of unquoted strings', they should be tokenized as identifiers or numbers, not as LINE_NUMBER tokens. The comment may be describing intended behavior that differs from implementation.

---



#### code_vs_comment

**Description:** apply_keyword_case_policy function docstring states 'keyword: The keyword to transform (must be normalized lowercase)' but the function itself handles uppercase input for 'first_wins' policy by converting to lowercase internally.

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring says: 'Args:
    keyword: The keyword to transform (must be normalized lowercase)'

But in code:
    elif policy == "first_wins":
        # Use the first occurrence seen for this keyword
        if keyword_tracker is not None:
            keyword_lower = keyword.lower()
            if keyword_lower in keyword_tracker:
                return keyword_tracker[keyword_lower]

The function converts to lowercase internally for first_wins, suggesting it can handle non-lowercase input. The 'must be normalized lowercase' requirement may not be strictly enforced.

---



#### code_vs_comment

**Description:** serialize_expression for VariableNode has comment 'Only add type suffix if explicit' but the code checks 'explicit_type_suffix' attribute which may not always exist (uses getattr with default False).

**Affected files:**
- `src/position_serializer.py`

**Details:**
Code:
    # Only add type suffix if explicit
    if expr.type_suffix and getattr(expr, 'explicit_type_suffix', False):
        text += expr.type_suffix

The use of getattr with default False suggests explicit_type_suffix may not always be present on VariableNode. The comment doesn't mention this optional nature. If the attribute is missing, the suffix won't be added even if type_suffix exists.

---



#### Documentation inconsistency

**Description:** Inconsistent documentation about string length limits across different preset configurations

**Affected files:**
- `src/resource_limits.py`

**Details:**
create_web_limits() and create_local_limits() both document 'Maintains MBASIC 5.21 compatibility with 255-byte string length limit' but create_unlimited_limits() explicitly states 'This configuration intentionally breaks MBASIC 5.21 compatibility by setting max_string_length to 1MB (instead of 255 bytes)'. However, the warning in create_unlimited_limits() suggests this is a testing-only exception and warns that 'tests to pass with unlimited limits that would fail with MBASIC-compatible limits'. This creates confusion about whether the 255-byte limit is a hard requirement for MBASIC 5.21 compatibility or just a recommended default.

---



#### code_vs_comment

**Description:** SettingsManager docstring claims file_settings dict is 'partially implemented' but it is fully implemented for runtime manipulation

**Affected files:**
- `src/settings.py`

**Details:**
Class docstring says: 'File-level settings infrastructure is partially implemented (file_settings dict, FILE scope support in get/set/reset methods for runtime manipulation), but persistence is not implemented'

However, the code fully implements:
- file_settings dict initialization in __init__
- FILE scope handling in get() method (checks file_settings first)
- FILE scope handling in set() method (sets in file_settings)
- FILE scope handling in reset_to_defaults() method (clears file_settings)

The only missing piece is persistence (load/save), which is explicitly documented as 'not implemented'. The runtime manipulation is complete, not partial.

---



#### code_vs_comment

**Description:** load() method docstring describes format handling but doesn't match actual implementation behavior

**Affected files:**
- `src/settings.py`

**Details:**
Docstring says: 'Format handling: Settings are stored on disk in flattened format (e.g., {\'editor.auto_number\': True}) but this method loads them as-is without unflattening. Internal representation is flexible: _get_from_dict() handles both flat keys like \'editor.auto_number\' and nested dicts like {\'editor\': {\'auto_number\': True}}. Loaded settings remain flat; settings modified via set() become nested; both work.'

However, the code simply calls:
self.global_settings = self.backend.load_global()
self.project_settings = self.backend.load_project()

The backend (FileSettingsBackend) loads from JSON with structure {'version': '1.0', 'settings': {...}} and returns the 'settings' dict. The format (flat vs nested) depends entirely on what was saved. The docstring implies load() does something special with format handling, but it just delegates to backend.

---



#### code_vs_comment

**Description:** get() method docstring claims file_settings is 'not populated in normal usage' but provides no mechanism to populate it

**Affected files:**
- `src/settings.py`

**Details:**
Docstring says: 'Note: File-level settings (first in precedence) are not populated in normal usage. The file_settings dict can be set programmatically and is checked first, but no persistence layer exists (not saved/loaded) and no UI/command manages per-file settings.'

This is accurate but incomplete. The comment should clarify HOW to set file_settings programmatically (via set() with scope=SettingScope.FILE), since there's no other documented way to populate it.

---



#### code_vs_comment

**Description:** create_settings_backend() docstring describes fallback behavior that contradicts implementation

**Affected files:**
- `src/settings_backend.py`

**Details:**
Docstring says: 'session_id: Session ID for Redis mode (required for Redis backend, but falls back to file backend if not provided even when NICEGUI_REDIS_URL is set)'

Implementation:
if redis_url and session_id:
    # Redis mode
else:
    # File mode
    return FileSettingsBackend(project_dir)

This is consistent. However, the docstring also says: 'Note: If NICEGUI_REDIS_URL is set but session_id is None, silently falls back to FileSettingsBackend.'

The word 'silently' is misleading - there's no warning or logging when this fallback occurs, but the docstring makes it sound intentional. Should clarify if this is expected behavior or if a warning should be logged.

---



#### code_vs_comment

**Description:** Module docstring describes architecture but doesn't explain why both systems read from same setting

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
Docstring says: 'Note: Both systems read from the same settings.get("keywords.case_style") setting, so they should normally be configured with the same policy.'

This implies both SimpleKeywordCase and KeywordCaseManager read from settings, but SimpleKeywordCase.__init__() takes a policy parameter directly:
def __init__(self, policy: str = "force_lower")

There's no code in SimpleKeywordCase that reads from settings. The docstring is misleading - it should say 'Both systems SHOULD read from the same setting' or 'Callers should pass the same policy from settings to both systems'.

---



#### Documentation inconsistency

**Description:** STEP command description inconsistency between keybindings and implementation

**Affected files:**
- `src/ui/cli_keybindings.json`
- `src/ui/cli_debug.py`

**Details:**
cli_keybindings.json describes STEP as 'Execute next statement or n statements - statement-level only, not line-level (STEP | STEP n)'

However, cli_debug.py cmd_step() docstring says: 'This implements statement-level stepping similar to the curses UI Step Statement command (Ctrl+T). The curses UI also has a separate Step Line command (Ctrl+K) which is not available in the CLI.'

But the actual implementation in _execute_single_step() has a NOTE: 'The actual statement-level granularity depends on the interpreter's implementation of tick()/execute_next(). These methods are expected to advance the program counter by one statement, handling colon-separated statements separately. If the interpreter executes full lines instead, this method will behave as line-level stepping rather than statement-level.'

This creates uncertainty about whether STEP actually does statement-level stepping or might do line-level stepping depending on interpreter implementation.

---



#### Code vs Comment conflict

**Description:** Module docstring claims UI layer is responsible for prompting, but format_recovery_prompt() method suggests otherwise

**Affected files:**
- `src/ui/auto_save.py`

**Details:**
Module docstring states: 'This module provides building blocks for auto-save functionality. The UI layer is responsible for:
- Prompting user before overwriting files with autosave content
- Offering recovery on startup if autosave is newer
- Deciding when to trigger auto-save operations'

However, the AutoSaveManager class includes a format_recovery_prompt() method that generates formatted recovery prompt messages, which suggests the module does provide UI-level functionality beyond just 'building blocks'. This contradicts the claim that prompting is the UI layer's responsibility.

---



#### code_vs_comment

**Description:** Comment claims auto-numbering stops at 99999 but code allows manual entry of higher numbers, yet _parse_line_number() has no such restriction documented

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~680: "# Note: Auto-numbering stops at 99999 for display consistency, but manual
# entry of higher line numbers is not prevented by _parse_line_number()."

However, _parse_line_number() docstring and implementation show no validation or mention of line number limits. The method parses any sequence of digits without upper bounds checking.

---



#### code_vs_comment

**Description:** Docstring for _sort_and_position_line says default target_column is 7, but this assumes 5-digit line numbers which contradicts variable-width design

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line ~1133 docstring: "target_column: Column to position cursor at (default: 7). Since line numbers have
                          variable width, this is approximate."

The value 7 assumes: 1 char status + 5 digit line number + 1 space = 7 total.

However, throughout the code, line numbers are explicitly variable width (can be 1-5+ digits). A line number like '10' would only need column 4 (status + 2 digits + space), while '10000' needs column 8. The default of 7 is arbitrary and doesn't align with the variable-width philosophy.

---



#### documentation_inconsistency

**Description:** Module docstring describes 'urwid' but class docstrings use inconsistent terminology for line format

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Module docstring (line 1): "Curses UI backend using urwid."

ProgramEditorWidget docstring (line ~180): "Display format: 'S<linenum> CODE' where:
- Field 1 (1 char): Status
- Field 2 (variable width): Line number (1-5 digits, no padding)"

But _format_line docstring (line ~420): "Format a single program line with status, line number, and code.
...Returns: Formatted string or urwid markup: 'S<num> CODE'"

The inconsistency is '<linenum>' vs '<num>' and '1-5 digits' vs no digit limit mentioned. The code actually supports any number of digits.

---



#### code_vs_comment

**Description:** Comment claims line 0 is an 'edge case' but code doesn't explain why line 0 would exist or how it's handled elsewhere

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line ~876: "# Note: line_number > 0 check handles edge case of line 0 (if present)
# Consistent with _check_line_syntax which treats all empty lines as valid"

BASIC programs typically start at line 10 or higher. Line 0 would be unusual. The comment doesn't explain if line 0 is actually supported, forbidden, or just theoretically possible. The code silently skips it without error.

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
2. It's only READ in _debug_step_line() and _debug_step(): line_code = self.editor_lines.get(state.current_line, "")
3. It's never WRITTEN to or synced from editor.lines anywhere in this file
4. The _refresh_editor() method syncs FROM program manager TO editor.lines, but never touches editor_lines
5. The _save_editor_to_program() method syncs FROM editor.lines TO program manager, but never touches editor_lines

---



#### code_vs_comment

**Description:** Comment claims ImmediateExecutor is recreated in start() to ensure attribute exists, but the code shows it's fully functional in __init__ and then replaced in start()

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~273 says:
# ImmediateExecutor Lifecycle:
# Created here with temporary IO handler (to ensure attribute exists),
# then recreated in start() with a fresh OutputCapturingIOHandler.

This suggests the __init__ version is just a placeholder, but the code shows:
1. In __init__: self.immediate_executor = ImmediateExecutor(self.runtime, self.interpreter, immediate_io)
2. In start(): self.immediate_executor = ImmediateExecutor(self.runtime, self.interpreter, immediate_io)

Both are fully functional instances, not a placeholder followed by a real one. The comment's justification 'to ensure attribute exists' is misleading - it could just be set to None if that were the goal.

---



#### code_vs_comment

**Description:** Comment in _debug_step() and _debug_step_line() says 'Immediate mode status remains disabled during execution' but there's no code that disables it

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple comments say:
# (Immediate mode status remains disabled during execution - output shows in output window)

Appears at:
- Line ~730 in _debug_step()
- Line ~750 in _debug_step()
- Line ~820 in _debug_step_line()
- Line ~840 in _debug_step_line()

However, there's no code in these methods that actually disables immediate mode status. The only calls to _update_immediate_status() are AFTER execution completes or errors, which would re-enable it, not disable it during execution.

---



#### code_vs_comment

**Description:** Comment claims breakpoints are stored in editor as authoritative source and re-applied after reset, but code shows breakpoints are cleared during reset_for_run and then re-applied from editor.breakpoints

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1089 states:
"Note: reset_for_run() clears variables and resets PC. Breakpoints are STORED in
the editor (self.editor.breakpoints) as the authoritative source, not in runtime.
This allows them to persist across runs. After reset_for_run(), we re-apply them
to the interpreter below via set_breakpoint() calls so execution can check them."

This is accurate - the comment correctly describes the implementation where breakpoints persist in editor.breakpoints and are re-applied after reset. However, the phrasing could be clearer that reset_for_run() clears breakpoints from the interpreter/runtime, not from the editor.

---



#### code_vs_comment

**Description:** Comment about statement-level precision for GOSUB contradicts the actual display format

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
At line ~1011, comment states:
"Show statement-level precision for GOSUB return address
return_stmt is statement offset (0-based index): 0 = first statement, 1 = second, etc."

But the code formats it as:
line = f"{indent}GOSUB from line {entry['from_line']}.{return_stmt}"

This displays as "line 100.0" which could be confusing since .0 suggests the first statement but users might interpret it as a decimal. The comment is accurate about the implementation, but the display format may not be intuitive.

---



#### code_vs_comment

**Description:** Comment in _execute_immediate says 'Immediate mode status remains disabled during execution' but there's no code that actually disables it

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1638:
# Immediate mode status remains disabled during execution - program output shows in output window
self.running = True

The comment claims immediate mode status 'remains disabled' but there's no code here that disables it. The _update_immediate_status() method checks can_execute_immediate() to determine status, but nothing in this block explicitly disables the immediate mode status.

---



#### code_vs_comment

**Description:** Comment in _sync_program_to_runtime says it 'conditionally preserving PC' but the logic is more complex than just conditional preservation

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Docstring at line ~1165:
"""Sync program to runtime, conditionally preserving PC.

Updates runtime's statement_table and line_text_map from self.program.

PC handling:
- If running and not paused at breakpoint: Preserves PC and execution state
- If paused at breakpoint: Resets PC to halted (prevents accidental resumption)
- If not running: Resets PC to halted for safety

This allows LIST and other commands to see the current program without
accidentally triggering execution. When paused at a breakpoint, the PC is
intentionally reset; when the user continues via _debug_continue(), the
interpreter's state already has the correct PC.
"""

The docstring describes three different behaviors based on state, which is more nuanced than 'conditionally preserving'. The phrase 'conditionally preserving PC' in the summary doesn't capture that it also 'resets PC to halted' in two of the three cases.

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
Comment at line ~115 says:
# Quit - No dedicated keybinding in QUIT_KEY (most Ctrl keys intercepted by terminal or already assigned)
# Primary method: Use menu (Ctrl+U -> File -> Quit)
# Alternative method: Ctrl+C (interrupt signal) - handled by QUIT_ALT_KEY below
QUIT_KEY = None  # No standard keybinding (use menu or Ctrl+C instead)

But then code loads from JSON:
_quit_alt_from_json = _get_key('editor', 'quit')
QUIT_ALT_KEY = _ctrl_key_to_urwid(_quit_alt_from_json) if _quit_alt_from_json else 'ctrl c'

This suggests there IS a quit keybinding in the JSON config, contradicting the comment that says there's no dedicated keybinding.

---



#### Documentation inconsistency

**Description:** KEYBINDINGS_BY_CATEGORY comment lists keys not included in help, but QUIT_KEY is mentioned as not included when it's actually None and QUIT_ALT_KEY is shown instead

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Comment at line ~215 says:
# Note: This dictionary contains keybindings shown in the help system.
# Some defined constants are not included here:
# - CLEAR_BREAKPOINTS_KEY (Shift+Ctrl+B) - Available in menu under Edit > Clear All Breakpoints
# - STOP_KEY (Ctrl+X) - Shown in debugger context in the Debugger category
# - MAXIMIZE_OUTPUT_KEY (Shift+Ctrl+M) - Menu-only feature, not documented as keyboard shortcut
# - STACK_KEY (empty string) - No keyboard shortcut assigned, menu-only

But STOP_KEY (Ctrl+X) IS actually included in the 'Debugger (when program running)' category in KEYBINDINGS_BY_CATEGORY, contradicting the comment that says it's not included.

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
# ESC key closes search bar (local widget binding, not in tk_keybindings.json)

However, tk_keybindings.json only documents Ctrl+F for inpage_search, missing Return (next match) and Escape (close search bar) bindings. The comment explicitly states these are not in tk_keybindings.json, but this creates incomplete documentation of available keybindings.

---



#### Code duplication with inconsistency risk

**Description:** Path normalization logic duplicated between _follow_link() and _open_link_in_new_window() methods

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
In _follow_link() (line 244):
# Note: Path normalization logic is duplicated in _open_link_in_new_window().
# Both methods use similar approach: resolve relative paths, normalize to help_root,
# handle path separators. If modification needed, update both methods consistently.

In _open_link_in_new_window() (line 638):
# Note: Path normalization logic is duplicated from _follow_link().
# Both methods resolve paths relative to help_root with similar logic.
# If modification needed, update both methods consistently.

Both methods implement similar path resolution logic (lines 247-272 and 645-665). This duplication creates maintenance risk where changes to one method may not be reflected in the other, leading to inconsistent behavior.

---



#### code_vs_comment

**Description:** Comment states immediate_history and immediate_status are 'always None' but code explicitly sets them to None with defensive programming justification

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~265 comment: 'Note: immediate_history and immediate_status are always None in Tk UI'
Line ~267 comment: '(Tk uses immediate_entry Entry widget directly instead of separate history/status widgets)'
Line ~273-276 code:
# Set immediate_history and immediate_status to None
# These attributes are not currently used but are set to None for defensive programming
# in case future code tries to access them (will get None instead of AttributeError)
self.immediate_history = None
self.immediate_status = None

---



#### code_vs_comment

**Description:** _ImmediateModeToken docstring references line 1194 for _on_variable_edit() but this is a forward reference that may be incorrect

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~18-23 docstring:
'''Token for variable edits from immediate mode or variable editor.

This class is instantiated when editing variables via the variable inspector
(see _on_variable_edit() around line 1194). Used to mark variable changes that
originate from the variable inspector or immediate mode, not from program
execution. The line=-1 signals to runtime.set_variable() that this is a
debugger/immediate mode edit.'''

The file is truncated at line ~1194 with _edit_simple_variable method, but _on_variable_edit() is not visible in the provided code. The line number reference may be outdated or incorrect.

---



#### code_vs_comment

**Description:** Variables window heading text shows 'Last Accessed' but comment says it matches 'accessed' column with descending sort

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~1088-1089 code:
# Set initial heading text with down arrow (matches self.variables_sort_column='accessed', descending)
tree.heading('#0', text='↓ Variable (Last Accessed)')

Line ~107 initialization:
self.variables_sort_column = 'accessed'  # Current sort column (default: 'accessed' for last-accessed timestamp)

The heading text 'Last Accessed' suggests the column shows when variables were last accessed, but the actual column name is 'Variable' (showing variable names). The comment may be describing the sort order rather than the column content.

---



#### code_vs_comment

**Description:** Comment in _on_variable_double_click describes format examples that don't match the actual parsing logic shown

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~1152 comment:
# Format examples: 'A%', 'NAME$', 'X', 'A%(10x10) [5,3]=42'

The code checks if 'Array' is in value_display (line ~1155), but the example shows array format as 'A%(10x10) [5,3]=42' which suggests the word 'Array' might not appear in that format. The actual format used by the display logic is not shown in the truncated code.

---



#### code_vs_comment

**Description:** Comment claims formatting may occur elsewhere, but code explicitly avoids formatting to preserve MBASIC compatibility

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _refresh_editor method around line 1150:
Comment says: '# (Note: "formatting may occur elsewhere" refers to the Variables and Stack windows,\n# which DO format data for display - not the editor/program text itself)'

This comment is confusing because it suggests formatting happens elsewhere, but the actual intent is to clarify that NO formatting happens to program text (only to Variables/Stack display data). The parenthetical note tries to clarify this but creates ambiguity about whether 'elsewhere' means 'in other parts of the code' or 'in other windows'.

---



#### internal_inconsistency

**Description:** Inconsistent handling of syntax validation output messages

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _validate_editor_syntax method around line 1250:
The code has logic: 'should_show_list = len(errors_found) > 1'
with comment: '# Only show full error list in output if there are multiple errors.\n# For single errors, the red ? icon in the editor is sufficient feedback.'

However, the status bar is ALWAYS updated with error count (lines 1260-1265):
if errors_found:
    ...
    error_count = len(errors_found)
    plural = "s" if error_count > 1 else ""
    self._set_status(f"Syntax error{plural} in program - cannot run")

This means single errors get status bar message but not output window message, while multiple errors get both. The inconsistency in feedback channels (status bar vs output window) based on error count may confuse users about where to look for error information.

---



#### code_vs_comment

**Description:** Comment claims _on_key_press clears highlight on ANY key, but code only clears on printable characters

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1050 states: "Clears on ANY key (even arrows/function keys)"

But code at line ~1060 returns None for non-printable keys BEFORE clearing highlight:

```
if len(event.char) != 1:
    return None
```

The highlight clearing happens at the top of the function, so it DOES clear on any key. However, the comment's justification about "editing shifts character positions" only applies to actual text modifications, not arrow keys.

---



#### code_vs_comment

**Description:** Comment about paste handling describes three cases but implementation has different logic flow

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1140 states: "The auto-numbering path handles:
1. Multi-line paste: sanitized_text contains \n → multiple lines to process
2. Single-line paste into blank line: current_line_text empty → one line to process"

However, the code checks for '\n' in sanitized_text first (line ~1125), then checks if current line has content. The logic is:
- If no newlines AND current line has content → inline paste
- Otherwise → auto-numbering path

This means single-line paste into non-blank line uses inline paste, not auto-numbering. The comment's case 2 is correct but incomplete.

---



#### code_vs_comment

**Description:** Comment about _smart_insert_line saving behavior contradicts when line is actually saved

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1330 states: "DON'T save to program yet - the line only has a line number with no statement, so _save_editor_to_program() will skip it (only saves lines with statements)."

This implies _save_editor_to_program() filters out lines with only line numbers. However, the comment then says: "Note: This line won't be removed by _remove_blank_lines() because it contains the line number (not completely blank)"

This creates ambiguity: if the line has a line number, will _save_editor_to_program() save it or skip it? The comment suggests it will skip it, but doesn't explain the exact filtering logic.

---



#### documentation_inconsistency

**Description:** Inconsistent documentation of RENUM command behavior

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
The cmd_renum docstring at line ~1730 states: "Uses AST-based approach:
1. Build line number mapping (old -> new)
2. Walk AST and update all line number references
3. Serialize AST back to source
4. Refresh editor display

This ensures AST is the single source of truth."

However, the implementation calls renum_program from ui_helpers, which may have different behavior. The docstring describes implementation details that may not match the actual consolidated implementation in ui_helpers.

---



#### code_vs_comment

**Description:** Incomplete docstring for cmd_cont command

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
The cmd_cont docstring at line ~1820 is cut off mid-sentence: "The interpreter moves NPC to PC when STOP is executed (see execute_stop() in interpreter.py). CONT simply clears the stopped/halted flags and resumes"

The docstring ends abruptly without completing the explanation of what CONT does after clearing flags.

---



#### code_vs_comment

**Description:** Method name contradicts its documented behavior

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Method _add_immediate_output() has docstring:
"Add text to main output pane.

Note: This method name is historical/misleading - it actually adds to the main output pane, not a separate immediate output pane. It simply forwards to _add_output(). In the Tk UI, immediate mode output goes to the main output pane. self.immediate_history is always None (see __init__)."

The method name suggests it adds to immediate output, but documentation says it adds to main output. This is a naming inconsistency that could confuse maintainers.

---



#### documentation_inconsistency

**Description:** Inconsistent documentation about INPUT handling strategy

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
TkIOHandler docstring states:
"Input strategy rationale:
- INPUT statement: Uses inline input field when backend available (allowing the user to see program output context while typing input), otherwise uses modal dialog as fallback. This is availability-based, not a UI preference.
- LINE INPUT statement: Always uses modal dialog for consistent UX."

However, the input() method implementation shows it's not just availability-based - it's a design choice. The comment says 'This is availability-based, not a UI preference' but then LINE INPUT 'Always uses modal dialog for consistent UX' which IS a UI preference. These statements contradict each other.

---



#### code_vs_comment

**Description:** Comment describes complex state management that may indicate design issue

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _update_immediate_status() method:
"Check if safe to execute - use both can_execute_immediate() AND self.running flag. The 'not self.running' check prevents immediate mode execution when a program is running, even if the tick hasn't completed yet. This prevents race conditions where immediate mode could execute while the program is still running but between tick cycles."

This suggests the code is working around race conditions rather than properly synchronizing state. The need for multiple redundant checks indicates potential architectural issues.

---



#### code_vs_comment_conflict

**Description:** The _delete_line() docstring describes line_num as 'Tkinter text widget line number (1-based sequential index), not BASIC line number' and mentions 'dual numbering', but the class docstring says 'BASIC line numbers are part of the text content (not drawn separately in the canvas)' without clearly explaining this dual numbering system upfront.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
_delete_line() docstring: 'Args:
    line_num: Tkinter text widget line number (1-based sequential index),
             not BASIC line number (e.g., 10, 20, 30).
             Note: This class uses dual numbering - editor line numbers for
             text widget operations, BASIC line numbers for line_metadata lookups.'

Class docstring mentions: 'Note: BASIC line numbers are part of the text content (not drawn separately in the canvas).'

The class docstring should explain the dual numbering system more clearly upfront since it's a critical concept for understanding the widget's operation.

---



#### documentation_inconsistency

**Description:** The _redraw() docstring says 'Note: BASIC line numbers are part of the text content (not drawn separately in the canvas)' and references _parse_line_number() for 'regex-based extraction logic that validates line number format (requires whitespace or end-of-string after the number)', but this same information is repeated in multiple places with slightly different wording, creating potential for inconsistency.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
_redraw() docstring: 'Note: BASIC line numbers are part of the text content (not drawn separately in the canvas). See _parse_line_number() for the regex-based extraction logic that validates line number format (requires whitespace or end-of-string after the number).'

_parse_line_number() has its own detailed comment: 'Match line number followed by whitespace OR end of string (both valid).'

Class docstring: 'Note: BASIC line numbers are part of the text content (not drawn separately in the canvas).'

The regex pattern requirement is documented in _parse_line_number() but also mentioned in _redraw()'s docstring. If the regex changes, both need updating.

---



#### code_vs_comment_conflict

**Description:** The class docstring states 'After fixing error, ● becomes visible (automatically handled by set_error() method which checks has_breakpoint flag when clearing errors)', but examining set_error() shows it updates status based on has_breakpoint without any special 'checking' logic - it's just a simple if/elif/else priority check.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Class docstring: 'After fixing error, ● becomes visible (automatically handled by set_error() method which checks has_breakpoint flag when clearing errors)'

set_error() implementation:
'# Update status symbol (error takes priority)
if metadata['has_error']:
    metadata['status'] = '?'
elif metadata['has_breakpoint']:
    metadata['status'] = '●'
else:
    metadata['status'] = ' '

The docstring makes it sound like there's special logic for 'checking has_breakpoint flag when clearing errors', but it's just the standard priority logic that runs every time set_error() is called. The phrasing is misleading.

---



#### Code vs Documentation inconsistency

**Description:** cmd_delete() and cmd_renum() docstrings reference 'curses_ui.py or tk_ui.py' for examples but these files are not present in the provided source code

**Affected files:**
- `src/ui/visual.py`

**Details:**
cmd_delete() docstring:
        """Execute DELETE command - delete line range.

        Status: Stub implementation. Override in subclass to implement.
        See curses_ui.py or tk_ui.py for example implementations.
        ...
        """

cmd_renum() docstring:
        """Execute RENUM command - renumber lines.

        Status: Stub implementation. Override in subclass to implement.
        See ui_helpers.renum_program() for the shared implementation logic.
        ...
        """

These references to external files (curses_ui.py, tk_ui.py) and modules (ui_helpers) cannot be verified from the provided code.

---



#### code_vs_comment

**Description:** Docstring claims columns are not sortable, but code shows sortable: False explicitly set

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~213:
# Create table - columns not sortable (we handle sorting via buttons above)

Then at line ~216-219:
columns = [
    {'name': 'name', 'label': name_header, 'field': 'name', 'align': 'left', 'sortable': False},
    {'name': 'type', 'label': 'Type', 'field': 'type', 'align': 'left', 'sortable': False},
    {'name': 'value', 'label': 'Value', 'field': 'value', 'align': 'left', 'sortable': False},
]

This is actually consistent - the comment explains WHY sortable is False. Not an inconsistency.

---



#### code_vs_comment

**Description:** Comment claims PC preservation logic prevents accidental execution starts, but code actually handles state preservation during statement table rebuilds

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _sync_program_to_runtime() method:

Comment says: "This logic is about PRESERVING vs RESETTING state, not about preventing accidental starts"

But earlier comment says: "(ensures program doesn't start executing unexpectedly when LIST/edit commands run)"

The second comment contradicts the first by claiming the logic DOES prevent accidental starts. The code shows it's about preserving PC during active execution vs resetting when idle, not about preventing starts.

---



#### code_vs_comment

**Description:** Comment claims _on_enter_key handles auto-numbering but method body shows it does nothing

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Method _on_enter_key() has docstring:
"Handle Enter key press in editor - triggers auto-numbering.

Note: This method is called internally by _on_editor_change when a new line
is detected. The actual auto-numbering logic is in _add_next_line_number."

But the method body only contains:
# Auto-numbering on Enter is handled by _on_editor_change detecting new lines
# and calling _add_next_line_number via timer
pass

The docstring suggests this method has a purpose, but it's completely empty. Either the method should be removed or the docstring should clarify it's a placeholder/hook.

---



#### code_vs_comment

**Description:** Comment about interpreter.has_work() query contradicts earlier pattern of checking runtime flags

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _execute_immediate() method:

Comment says: "Check if interpreter has work to do (after RUN statement)
Query interpreter directly via has_work() instead of checking runtime flags"

This suggests a deliberate architectural choice to query interpreter instead of runtime, but doesn't explain why. Earlier in the codebase, runtime flags (like self.running, self.paused) are used extensively. The comment should explain why this specific check uses a different pattern.

---



#### code_vs_comment

**Description:** Docstring for _get_input describes state transition mechanism but implementation just returns empty string

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Method _get_input() has docstring:
"Get input from user (non-blocking version for web UI).

Instead of blocking, this shows the input UI and returns empty string.
The interpreter will transition to 'waiting_for_input' state, and
when the user submits input via _handle_output_enter(), it will call
interpreter.provide_input() to continue execution."

The docstring describes a complex state machine, but the code just calls _enable_inline_input() and returns "". The docstring should clarify that the state transition happens in the interpreter (not in this method), or the comment about state transition should be moved to where it actually happens.

---



#### documentation_inconsistency

**Description:** Help URL inconsistency - documentation mentions both localhost:8000 and /mbasic_docs paths

**Affected files:**
- `docs/help/README.md`
- `src/ui/web_help_launcher.py`

**Details:**
README.md states: 'Help content is built using MkDocs and served locally at `http://localhost/mbasic_docs` for the Tk and Web UIs... (Legacy code may reference `http://localhost:8000`, which is deprecated in favor of the `/mbasic_docs` path.)'

However, web_help_launcher.py uses:
HELP_BASE_URL = "http://localhost/mbasic_docs"

But the deprecated WebHelpLauncher_DEPRECATED class uses:
self.server_port = 8000
base_url = f"http://localhost:{self.server_port}"

The documentation correctly notes the legacy issue, but the deprecated class is still present in the codebase serving on port 8000.

---



#### documentation_inconsistency

**Description:** Inconsistent precision information for SINGLE type

**Affected files:**
- `docs/help/common/language/data-types.md`
- `docs/help/common/language/functions/atn.md`

**Details:**
data-types.md states SINGLE has 'approximately 7 digits' of precision, while atn.md states 'the evaluation of ATN is always performed in single precision (~7 significant digits)'. The atn.md note about PI calculation says 'the result is limited to single precision (~7 digits)' but then says 'For higher precision, use ATN(CDBL(1)) * 4 to get double precision' - this is misleading because ATN itself is always single precision according to the same document.

---



#### documentation_inconsistency

**Description:** Missing cross-reference to overflow error documentation

**Affected files:**
- `docs/help/common/language/data-types.md`
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
data-types.md mentions 'ERROR: Overflow' in examples but doesn't link to the error codes documentation. The error-codes.md file exists and documents overflow as error code 6 (OV), but there's no cross-reference from the data types page.

---



#### documentation_inconsistency

**Description:** Incomplete cross-reference in appendices index

**Affected files:**
- `docs/help/common/language/appendices/index.md`
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
appendices/index.md says error-codes.md includes 'Error handling references (see [Error Handling](../statements/index.md#error-handling) for detailed examples)' but error-codes.md itself has a 'See Also' section that references individual statements like 'ON ERROR GOTO', 'ERR and ERL', 'ERROR', and 'RESUME' without mentioning the general error handling section.

---



#### documentation_inconsistency

**Description:** Error code reference format inconsistency

**Affected files:**
- `docs/help/common/language/functions/cvi-cvs-cvd.md`
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
cvi-cvs-cvd.md states 'Raises "Illegal function call" (error code FC)' using the two-letter code 'FC', while error-codes.md shows this as 'Code: FC, Number: 5'. The documentation should be consistent about whether to use the letter code, number, or both when referencing errors.

---



#### documentation_inconsistency

**Description:** Inconsistent navigation between main index and getting started

**Affected files:**
- `docs/help/common/index.md`
- `docs/help/common/getting-started.md`

**Details:**
index.md shows a table with keyboard shortcuts for different UIs and links to UI-specific guides, but getting-started.md has a 'How to Enter Programs' section that also links to UI-specific help. The index.md says 'For complete shortcuts, see your UI-specific guide' while getting-started.md says 'See your UI-specific help for how to type programs'. These should be coordinated to avoid redundancy.

---



#### documentation_inconsistency

**Description:** LOF function missing from index categorization

**Affected files:**
- `docs/help/common/language/functions/index.md`
- `docs/help/common/language/functions/lof.md`

**Details:**
The index.md file lists LOF in the alphabetical quick reference at the bottom, but it is NOT listed in the 'File I/O Functions' category section at the top. Other file I/O functions like EOF, INPUT$, LOC, and LPOS are listed in the category, but LOF is missing despite being a file I/O function.

---



#### documentation_inconsistency

**Description:** Inconsistent Control-C behavior documentation

**Affected files:**
- `docs/help/common/language/functions/input_dollar.md`
- `docs/help/common/language/functions/inkey_dollar.md`

**Details:**
Both INPUT$ and INKEY$ have identical notes about Control-C behavior:

'Note: Control-C behavior varied in original implementations. In MBASIC 5.21 interpreter mode, Control-C would terminate the program. This implementation passes Control-C through (CHR$(3)) for program detection and handling, allowing programs to detect and handle it explicitly.'

However, INPUT$ is documented as a Disk version function while INKEY$ has no version restriction. If Control-C handling is implementation-specific, it should be documented consistently across all input functions, or the note should clarify which versions this applies to.

---



#### documentation_inconsistency

**Description:** Inconsistent implementation note formatting and detail level

**Affected files:**
- `docs/help/common/language/functions/lpos.md`
- `docs/help/common/language/functions/inp.md`
- `docs/help/common/language/functions/peek.md`

**Details:**
All three functions have 'Implementation Note' sections for unimplemented/emulated features, but with different formatting and detail levels:

LPOS: Simple note, states 'Function always returns 0', brief explanation

INP: More detailed, uses warning emoji, states 'Always returns 0', includes 'Why', 'Alternative', and 'Historical Reference' sections

PEEK: Most detailed, uses info emoji, explains random value behavior, includes 'Behavior', 'Why', 'Important Limitations' (bullet list), and 'Recommendation' sections

These should follow a consistent template for clarity and professionalism.

---



#### documentation_inconsistency

**Description:** DEF FN documentation claims multi-character function names are an extension over MBASIC 5.21, but DEFINT/SNG/DBL/STR documentation doesn't mention this is original MBASIC behavior

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`
- `docs/help/common/language/statements/defint-sng-dbl-str.md`

**Details:**
def-fn.md states:
"**Original MBASIC 5.21**: Function names were limited to a single character after FN:
- ✓ `FNA` - single character
- ✓ `FNB$` - single character with type suffix

**This implementation (extension)**: Function names can be multiple characters"

However, defint-sng-dbl-str.md shows no version restrictions and appears to be documenting original MBASIC 5.21 behavior without noting any extensions. The inconsistency is whether multi-character names after DEF keywords are extensions or original features.

---



#### documentation_inconsistency

**Description:** END documentation references STOP but STOP documentation file is not provided in the documentation set

**Affected files:**
- `docs/help/common/language/statements/end.md`
- `docs/help/common/language/statements/stop.md`

**Details:**
end.md states:
"### Difference from STOP

**END:**
- Closes all open files
- Returns to command level
- No 'Break' message printed
- Can be continued with CONT (execution resumes at next statement after END)
- Note: Files remain closed if CONT is used after END

**STOP:**
- Does NOT close files
- Returns to command level
- Prints 'Break in line nnnnn' message
- Can be continued with CONT (execution resumes at statement after STOP)"

However, stop.md is not included in the provided documentation files, so we cannot verify if STOP's documentation matches this description or if there are contradictions.

---



#### documentation_inconsistency

**Description:** FOR-NEXT loop termination test description is detailed but potentially confusing about when the test occurs

**Affected files:**
- `docs/help/common/language/statements/for-next.md`

**Details:**
for-next.md states:
"### Loop Termination:
The termination test happens AFTER each increment/decrement at the NEXT statement:
- **Positive STEP** (or no STEP): Loop continues while variable <= ending value
- **Negative STEP**: Loop continues while variable >= ending value

For example:
- `FOR I = 1 TO 10` executes with I=1,2,3,...,10 (10 iterations). After I=10 executes, NEXT increments to 11, test fails (11 > 10), loop exits."

This is technically correct but the phrasing 'test happens AFTER each increment' followed by 'Loop continues while' could be clearer. The test determines whether to continue or exit, and it happens after incrementing but before the next iteration.

---



#### documentation_inconsistency

**Description:** GOSUB documentation mentions STOP, END, or GOTO to prevent inadvertent subroutine entry, but doesn't show example; GOTO example shows infinite loop without this protection

**Affected files:**
- `docs/help/common/language/statements/gosub-return.md`
- `docs/help/common/language/statements/goto.md`

**Details:**
gosub-return.md states:
"Subroutines may appear anywhere in the program, but it is recommended that the subroutine be readily distinguishable from the main program. To prevent inadvertent entry into the subroutine, it may be preceded by a STOP, END, or GOTO statement that directs program control around the subroutine."

The GOSUB example shows:
"10 GOSUB 40
20 PRINT 'BACK FROM SUBROUTINE'
30 END
40 PRINT 'SUBROUTINE ';
50 PRINT ' IN';
60 PRINT ' PROGRESS'
70 RETURN"

This example correctly uses END at line 30 to prevent fall-through. However, the GOTO example shows an infinite loop without proper termination, which could confuse readers about best practices.

---



#### documentation_inconsistency

**Description:** INPUT documentation describes behavior with semicolons but the explanation is somewhat ambiguous

**Affected files:**
- `docs/help/common/language/statements/input.md`

**Details:**
input.md states:
"- A semicolon immediately after INPUT suppresses the carriage return/line feed after the user presses Enter
- A semicolon after the prompt string causes the prompt to be displayed without a question mark"

These two uses of semicolon are different:
1. INPUT; (semicolon after INPUT keyword)
2. INPUT 'prompt'; (semicolon after prompt string)

The syntax line shows: INPUT[;] ['prompt string'[;|,]]variable[,variable...]

This indicates both positions are valid, but the explanation could be clearer about which semicolon does what. The syntax shows [;|,] after prompt, meaning semicolon OR comma, but doesn't explain the difference between them.

---



#### documentation_inconsistency

**Description:** DEF FN Example 4 uses bitwise AND operation (&H5F) but doesn't explain hexadecimal notation or bitwise operations

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`

**Details:**
def-fn.md Example 4 shows:
"10 DEF FNUCASE$(Z$,N)=CHR$(ASC(MID$(Z$,N,1)) AND &H5F)"

With explanation:
"- AND &H5F clears bit 5, converting lowercase to uppercase"

This example uses hexadecimal notation (&H5F) and bitwise AND operation without explaining these concepts or linking to documentation about them. Other examples in the same file don't use such advanced features without explanation.

---



#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation for stopping AUTO mode

**Affected files:**
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/curses/editing.md`

**Details:**
CLI docs say 'Press {{kbd:stop:cli}} to stop AUTO mode' while Curses docs say 'Exit AUTO mode with {{kbd:continue:curses}} or by typing a line number manually'. These appear to be different key bindings for the same action (stopping AUTO mode), but use different placeholder names (stop vs continue).

---



#### documentation_inconsistency

**Description:** Broken or inconsistent internal link structure

**Affected files:**
- `docs/help/index.md`
- `docs/help/common/ui/cli/index.md`

**Details:**
Main help index references 'UI-Specific Help' with links like '[CLI (Command Line)](ui/cli/index.md)' but the actual file path shown in the provided docs is 'docs/help/common/ui/cli/index.md'. The link path 'ui/cli/index.md' is relative and may not resolve correctly depending on where the help index is located. This suggests either the file structure doesn't match the documentation or the links need to be updated.

---



#### documentation_inconsistency

**Description:** Inconsistent description of WIDTH statement behavior

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/extensions.md`

**Details:**
Compatibility doc states 'WIDTH 80 ... Accepted (no-op)' and 'Note: WIDTH is parsed for compatibility but performs no operation. Terminal width is controlled by the UI or OS. The "WIDTH LPRINT" syntax is not supported.' Extensions doc doesn't mention WIDTH at all. Since WIDTH is a compatibility feature (accepted but no-op), it should be documented in the extensions guide as well, or at least cross-referenced.

---



#### documentation_inconsistency

**Description:** Inconsistent information about Find/Replace availability across UIs

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/find-replace.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
features.md states:
- Curses UI: 'Note: Find/Replace is not available in Curses UI. Use the Tk UI for search/replace functionality.'
- CLI Mode: 'Note: Find/Replace is not available in CLI. Use the Tk UI for search/replace functionality.'
- Tkinter GUI: 'Find and Replace - Search and replace text ({{kbd:find:tk}}/{{kbd:replace:tk}})'
- Web UI: 'Note: Find/Replace is not available in Web UI. Use the Tk UI for search/replace functionality.'

However, find-replace.md for CLI provides detailed alternatives and workarounds, suggesting this is a known limitation rather than a missing feature. The documentation should be consistent about whether this is a limitation or missing feature, and all UI sections should have similar guidance.

---



#### documentation_inconsistency

**Description:** Contradictory information about CLS implementation

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
not-implemented.md states:
'**Note:** Basic CLS (clear screen) IS implemented in MBASIC - see [CLS](../common/language/statements/cls.md). The GW-BASIC extended CLS with optional parameters is not implemented.'

However, features.md does not list CLS in the 'Input/Output' section under 'Console I/O' or anywhere else in the features list. If CLS is implemented, it should be documented in the features list.

---



#### documentation_inconsistency

**Description:** Incomplete function count in features list

**Affected files:**
- `docs/help/mbasic/features.md`

**Details:**
features.md states:
'### Functions (50+)'

But then only lists about 20-25 functions across Mathematical, String, Type Conversion, System, and User-Defined categories. If there are truly 50+ functions, the list should be more complete, or it should reference a complete function index. The documentation mentions 'All 40 functions' in other places, creating further confusion about the actual count.

---



#### documentation_inconsistency

**Description:** Inconsistent Web UI session storage description

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
features.md states about Web UI:
'- **Session-based storage** - Files persist during browser session only (lost on page refresh)'

This is contradictory - if files persist during the browser session, they should NOT be lost on page refresh (which is part of the same session). The documentation should clarify whether:
1. Files persist across page refreshes within a session
2. Files are lost on any page refresh
3. Session storage means something else in this context

---



#### documentation_inconsistency

**Description:** Contradictory information about LPRINT implementation

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
features.md states:
'- **LPRINT** - Line printer output (Note: Statement is parsed but produces no output - see [LPRINT](../common/language/statements/lprint-lprint-using.md) for details)'

This suggests LPRINT is partially implemented (parsed but non-functional). However, not-implemented.md does not list LPRINT in its list of unimplemented features. The documentation should clarify:
1. Is LPRINT considered 'implemented' (even if non-functional)?
2. Should it be listed in not-implemented.md?
3. What is the expected behavior?

---



#### documentation_inconsistency

**Description:** Inconsistent information about GET/PUT implementation

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
features.md under 'File I/O' states:
'- **Random files:** FIELD, GET, PUT, LSET, RSET'

And under 'File Format Support' states:
'✓ MBASIC file I/O conventions'

However, not-implemented.md states:
'- **GET/PUT** - Graphics block operations (not the file I/O GET/PUT which ARE implemented)'

This clarification in not-implemented.md is helpful but creates potential confusion. The features.md should explicitly note that GET/PUT for graphics are NOT implemented, while file I/O GET/PUT ARE implemented, to avoid confusion.

---



#### documentation_inconsistency

**Description:** Inconsistent information about Variables Window keyboard shortcut

**Affected files:**
- `docs/help/ui/curses/quick-reference.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
docs/help/ui/curses/quick-reference.md under 'Global Commands' states: '**Menu only** | Toggle variables window'

But docs/help/ui/curses/feature-reference.md under 'Variable Inspection' states: '### Variables Window (Menu only)' and 'Open/close the variables inspection window showing all program variables and their current values. **Note:** Access via menu only - no keyboard shortcut assigned.'

However, docs/help/ui/curses/variables.md shows: 'Press `{{kbd:toggle_variables:curses}}` to open the variables window.'

This is contradictory - either there is a keyboard shortcut or there isn't.

---



#### documentation_inconsistency

**Description:** Inconsistent information about Execution Stack access method

**Affected files:**
- `docs/help/ui/curses/quick-reference.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
docs/help/ui/curses/quick-reference.md under 'Global Commands' states: '**Menu only** | Toggle execution stack window'

But docs/help/ui/curses/feature-reference.md under 'Variable Inspection' provides detailed access methods:
'**Access methods:**
- Via menu: Ctrl+U → Debug → Execution Stack
- Via command: Type `STACK` in immediate mode (same as CLI)'

This suggests the Execution Stack can be accessed via command (STACK), not just menu-only as the quick reference states.

---



#### documentation_inconsistency

**Description:** Inconsistent information about variable sorting default order

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
docs/help/ui/curses/variables.md states under 'Sorting Options':
'Press `s` to cycle through sort orders:
- **Accessed**: Most recently accessed (read or written) - shown first
- **Written**: Most recently written to - shown first
- **Read**: Most recently read from - shown first
- **Name**: Alphabetical by variable name'

But docs/help/ui/curses/feature-reference.md states:
'### Variable Sorting (s key in variables window)
Cycle through different sort orders:
- **Accessed**: Most recently accessed (read or written) - newest first
- **Written**: Most recently written to - newest first
- **Read**: Most recently read from - newest first
- **Name**: Alphabetically by variable name'

The variables.md doc doesn't specify which is the DEFAULT sort order, while feature-reference.md doesn't either. Also, variables.md later says 'Accessed: Most recently accessed (read or written) - default, newest first' in the Sort Modes section, but this conflicts with the earlier section that doesn't mention it's the default.

---



#### documentation_inconsistency

**Description:** Inconsistent information about variable editing capability

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/index.md`

**Details:**
docs/help/ui/curses/variables.md states: '### Direct Editing Not Available
⚠️ **Not Implemented**: You cannot edit variable values directly in the variables window.'

But docs/help/ui/index.md comparison table shows:
| Feature | Curses | CLI | Tkinter | Web |
|---------|--------|-----|---------|-----|
| Edit values | ❌ | ❌ | ✅ | ✅ |

This is consistent, but docs/help/ui/curses/feature-reference.md states:
'### Edit Variable Value (Not implemented)
⚠️ Variable editing is not available in Curses UI. You cannot directly edit values in the variables window. Use immediate mode commands to modify variable values instead.'

All three documents agree, so this is actually consistent. However, the comparison table in variables.md at the bottom shows:
| Feature | Curses | CLI | Tk | Web |
|---------|--------|-----|-----|-----|
| Edit values | ❌ | ❌ | ✅ | ✅ |

Which is also consistent. No actual inconsistency found here upon closer inspection.

---



#### documentation_inconsistency

**Description:** Inconsistent information about Renumber command access

**Affected files:**
- `docs/help/ui/curses/quick-reference.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
docs/help/ui/curses/quick-reference.md under 'Editing' states: '**Menu only** | Renumber all lines (RENUM)'

But docs/help/ui/curses/feature-reference.md states:
'### Renumber ({{kbd:renumber:curses}})
Renumber all program lines with consistent increments. Opens a dialog to specify start line and increment.'

This is contradictory - either Renumber has a keyboard shortcut {{kbd:renumber:curses}} or it's menu-only.

---



#### documentation_inconsistency

**Description:** Inconsistent feature count claims

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/features.md`

**Details:**
feature-reference.md title claims "Complete Feature Reference" and organizes features into categories:
- File Operations (8 features)
- Execution & Control (6 features)
- Debugging (6 features)
- Variable Inspection (6 features)
- Editor Features (7 features)
- Help System (4 features)
Total: 37 features

However, features.md is titled "Essential TK GUI Features" and only documents a subset: Smart Insert, Syntax Checking, Breakpoints, Variables Window, Execution Stack, Find and Replace, Context Help, and mentions "More Features" with links.

The relationship between these documents is unclear - is features.md meant to be a subset, or are they describing different feature sets?

---



#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation for Smart Insert

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/features.md`

**Details:**
feature-reference.md uses:
"### Smart Insert ({{kbd:smart_insert:tk}})"

But features.md uses:
"## Smart Insert ({{kbd:smart_insert}})"

The :tk suffix is missing in features.md. This inconsistency appears throughout features.md for multiple shortcuts (toggle_breakpoint, toggle_variables, toggle_stack, find:tk, replace:tk).

---



#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut information for Stop/Interrupt

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
In the Execution & Control section:
"### Stop/Interrupt
Stop a running program immediately.
- Menu: Run → Stop
- No keyboard shortcut (menu only)"

But in the Quick Reference table at the bottom:
"| (menu only) | Stop Program |"

The table entry is consistent, but this feature is the only one in the entire document that explicitly states "No keyboard shortcut (menu only)" while others that also lack shortcuts (like Continue, Step Statement, Clear All Breakpoints) don't include this clarification. This inconsistency in documentation style could confuse users about whether other features without listed shortcuts truly have none or if the documentation is incomplete.

---



#### documentation_inconsistency

**Description:** Contradictory information about breakpoint setting methods

**Affected files:**
- `docs/help/ui/web/debugging.md`

**Details:**
Under "Setting Breakpoints" → "Currently Implemented":
"1. Use **Run → Toggle Breakpoint** menu option
2. Enter the line number when prompted"

But under "Keyboard Shortcuts" → "Planned for Future Releases":
"**Note:** {{kbd:toggle_breakpoint:web}} is implemented but currently available via menu only (not yet bound to keyboard)."

This is contradictory - if toggle_breakpoint is implemented and available via menu, why does the user need to "enter the line number when prompted"? The first description suggests a dialog-based approach, while the second suggests a toggle command that works on the current line or selection.

---



#### documentation_inconsistency

**Description:** Inconsistent command line examples for starting the UI

**Affected files:**
- `docs/help/ui/tk/getting-started.md`
- `docs/help/ui/tk/index.md`

**Details:**
getting-started.md shows:
"```bash
mbasic --ui tk [filename.bas]
```

Or to use the default curses UI:
```bash
mbasic [filename.bas]
```"

But index.md shows:
"**Start the GUI:**
```bash
mbasic --ui tk [filename.bas]
```"

The getting-started.md implies curses is the default UI, but doesn't explain what happens if you use --ui tk vs no flag. The index.md only shows the tk flag without mentioning defaults or alternatives. This could confuse users about which UI they'll get by default.

---



#### documentation_inconsistency

**Description:** Inconsistent implementation status warnings across workflow documents

**Affected files:**
- `docs/help/ui/tk/workflows.md`
- `docs/help/ui/tk/tips.md`
- `docs/help/ui/tk/getting-started.md`

**Details:**
workflows.md has a note at the top:
"**Note:** Some features described below (Smart Insert, Variables Window, Execution Stack, Renumber dialog) are documented here based on the Tk UI design specifications. Check [Settings](settings.md) for current implementation status..."

tips.md has a similar note:
"**Note:** Some features described below (Smart Insert, Variables Window, Execution Stack) are documented here based on the Tk UI design specifications. Check [Settings](settings.md) for current implementation status..."

But getting-started.md has no such warning and presents all features as currently available:
"## Essential Shortcuts
| Shortcut | Action |
|----------|--------|
| {{kbd:run_program}} | Run program |
| {{kbd:save_file}} | Save file |
| {{kbd:smart_insert}} | Insert line between existing lines |
| {{kbd:toggle_breakpoint}} | Toggle breakpoint |
| {{kbd:toggle_variables}} | Show/hide variables window |"

This inconsistency makes it unclear which features are actually implemented.

---



#### documentation_inconsistency

**Description:** Inconsistent information about Step execution commands

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`

**Details:**
features.md lists under 'Execution Control' → 'Currently Implemented':
- 'Step statement ({{kbd:step:web}})'
- 'Step line ({{kbd:step_line:web}})'

But getting-started.md describes them differently:
- 'Step - Execute all statements on current line, then pause (⏭️ button, {{kbd:step_line:web}})'
- 'Stmt - Execute one statement, then pause (↻ button, {{kbd:step:web}})'

The toolbar button labeled 'Step' corresponds to step_line functionality, while 'Stmt' corresponds to step functionality. This naming mismatch could confuse users.

---



#### documentation_inconsistency

**Description:** Contradictory information about settings storage mechanisms

**Affected files:**
- `docs/help/ui/web/settings.md`
- `docs/help/ui/web/features.md`

**Details:**
settings.md describes two storage mechanisms:
1. 'Local Storage (Default)' - settings stored in browser localStorage
2. 'Redis Session Storage (Multi-User Deployments)' - settings stored in Redis

However, features.md under 'Local Storage' → 'Currently Implemented' states:
- 'Programs stored in Python server memory (session-only, lost on page refresh)'
- 'Recent files list stored in browser localStorage'

This creates confusion about what is stored where. The settings.md document discusses settings storage but doesn't clarify the relationship with program storage mentioned in features.md.

---



#### documentation_inconsistency

**Description:** Contradictory information about breakpoint management interface

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`

**Details:**
features.md under 'Breakpoints' → 'Currently Implemented' states:
- 'Line breakpoints (toggle via Run menu)'
- 'Management: Toggle via Run menu → Toggle Breakpoint'

But getting-started.md under 'Debugging Features' → 'Breakpoints' states:
- 'Set breakpoints to pause execution at specific lines:
1. Use Run → Toggle Breakpoint menu option
2. Enter the line number'

This suggests a dialog for entering line numbers, but features.md doesn't mention this dialog interface. The exact mechanism for specifying which line to set a breakpoint on is unclear.

---



#### documentation_inconsistency

**Description:** Inconsistent information about session recovery feature status

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/settings.md`

**Details:**
features.md under 'Local Storage' → 'Session Recovery (Planned)' states:
- 'Restores last program from browser storage'
- 'Recovers after crash or page refresh'
- 'Maintains breakpoints'
- 'Preserves variables'

But settings.md under 'Settings Storage' → 'Local Storage (Default)' → 'Limitations' states:
- 'Settings are per-browser, per-domain'
- 'Clearing browser data clears settings'

And under 'Troubleshooting' → 'Settings reset after reload':
- 'Browser may be clearing localStorage'

This suggests that while settings persist, program recovery is still planned. However, the exact current state of what persists (settings vs programs vs variables) is unclear across these documents.

---



#### documentation_inconsistency

**Description:** Calendar program appears in both Games and Utilities libraries with cross-references, but the descriptions and metadata differ

**Affected files:**
- `docs/library/games/index.md`
- `docs/library/utilities/index.md`

**Details:**
Games library shows:
### Calendar
Year-long calendar display program from Creative Computing
**Source:** Creative Computing, Morristown, NJ
**Year:** 1979
**Tags:** calendar, display
**Note:** A simpler calendar utility is also available in the [Utilities Library](../utilities/index.md#calendar)

Utilities library shows:
### Calendar
Simple calendar generator - prints a formatted calendar for any month/year (1900-2099)
**Source:** Dr Dobbs Nov 1981
**Year:** 1982
**Tags:** date, calendar, utility
**Note:** A different calendar program is also available in the [Games Library](../games/index.md#calendar)

The sources differ (Creative Computing vs Dr Dobbs), years differ (1979 vs 1982), and descriptions conflict (year-long vs month/year, simpler vs different)

---



#### documentation_inconsistency

**Description:** CLI debugging capabilities description is contradictory

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
The document states:
**Limitations:**
- Line-by-line editing only
- No visual debugging (text commands only)
- No mouse support
- No Save without filename

But then includes a note:
> **Note:** CLI has full debugging capabilities through commands (BREAK, STEP, STACK), but lacks the visual debugging interface (Variables Window, clickable breakpoints, etc.) found in Curses, Tk, and Web UIs.

The limitation says 'No visual debugging (text commands only)' which could be misinterpreted as 'no debugging at all' rather than 'no visual debugging interface'. The note clarifies this but the limitation bullet could be clearer.

---



#### documentation_inconsistency

**Description:** Example code shows inconsistent variable naming that contradicts the point being made

**Affected files:**
- `docs/user/CASE_HANDLING_GUIDE.md`

**Details:**
In the 'Problem 1: Accidental Typos' section:
```basic
10 TotalCount = 0
20 FOR I = 1 TO 10
30   TotalCont = TotalCount + I   ← Typo! Missing 'u' in assignment target
40 NEXT I
50 PRINT TotalCount
```

The comment says 'Missing u in assignment target' but the actual typo is missing 'u' in 'TotalCont' (should be 'TotalCount'). The comment should say 'Typo in variable name' or 'Missing u in TotalCount' to be clearer. The phrase 'assignment target' is technically correct but may confuse beginners.

---



#### documentation_inconsistency

**Description:** Performance comparison lacks units and methodology

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
The Performance Comparison section shows:
### Startup Time
1. **CLI**: ~0.1s (fastest)
2. **Curses**: ~0.3s
3. **Tk**: ~0.8s
4. **Web**: ~2s (browser launch)

### Memory Usage (approximate)
1. **CLI**: 20MB (lowest)
2. **Curses**: 25MB
3. **Tk**: 40MB
4. **Web**: 50MB+ (plus browser)

No information is provided about:
- What hardware these measurements were taken on
- What Python version
- Whether these are cold or warm starts
- What 'plus browser' means for Web UI memory
- Whether memory includes the Python interpreter itself

Without this context, users cannot determine if these numbers apply to their system.

---



#### documentation_inconsistency

**Description:** Inconsistent status indicators for planned features

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
SETTINGS_AND_CONFIGURATION.md uses emoji status indicators inconsistently. Some planned features show '🔧 PLANNED - Not yet implemented' (e.g., interpreter.strict_mode, interpreter.debug_mode, ui.theme, ui.font_size) while others have no status indicator but include '(future)' in their descriptions. The top of the document has a status note but doesn't use the same emoji system.

---



#### documentation_inconsistency

**Description:** Keyboard shortcuts table references undefined kbd template values

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
TK_UI_QUICK_START.md 'Essential Keyboard Shortcuts' table uses template notation like {{kbd:run_program}}, {{kbd:file_save}}, {{kbd:smart_insert}}, etc., but these are never defined or mapped to actual key combinations in the document. Users cannot determine what keys to actually press.

---



#### documentation_inconsistency

**Description:** Contradictory information about Recent files in Web UI

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
In 'File Operations' table, Recent files for Web shows '⚠️' with note 'Tk: menu, Web: localStorage'. The ⚠️ symbol means 'Partially implemented' according to legend, but the note suggests it IS implemented via localStorage. Should be either ✅ if fully working or the note should explain what's partial/missing.

---



#### documentation_inconsistency

**Description:** Inconsistent feature status for Resizable panels

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
In 'User Interface' table, 'Resizable panels' shows:
- Curses: '⚠️' (partially implemented)
- Tk: '✅' (fully implemented)
- Web: '✅' (fully implemented)
No note explains what's partial about Curses implementation, making it unclear what works vs doesn't work.

---

### 🟢 Low Severity



#### Code vs Comment conflict

**Description:** keyword_token fields documented as 'legacy, not currently used' but still present in code

**Affected files:**
- `src/ast_nodes.py`

**Details:**
Multiple statement nodes (PrintStatementNode, IfStatementNode, ForStatementNode) have keyword_token fields with comments stating they are 'legacy, not currently used'. For example: 'keyword_token: Optional[Token] = None  # Token for PRINT keyword (legacy, not currently used)'. The docstrings explain these were 'intended for case-preserving keyword regeneration but are not currently used by position_serializer'. This suggests technical debt where fields exist but serve no purpose.

---



#### Documentation inconsistency

**Description:** LineNode docstring mentions position_serializer module but doesn't explain relationship fully

**Affected files:**
- `src/ast_nodes.py`

**Details:**
LineNode docstring states: 'Text regeneration is handled by the position_serializer module which reconstructs source text from statement nodes and their token information.' However, there's no reference to where position_serializer is located or how it integrates with the AST. The comment also mentions 'Each StatementNode has char_start/char_end offsets' but doesn't explain how position_serializer uses these.

---



#### Documentation inconsistency

**Description:** RemarkStatementNode comment_type default value explanation inconsistency

**Affected files:**
- `src/ast_nodes.py`

**Details:**
RemarkStatementNode docstring states: 'Note: comment_type preserves the original comment syntax used in source code. The parser sets this to "REM", "REMARK", or "APOSTROPHE" based on input. Default value "REM" is used only when creating nodes programmatically.' However, the field definition shows 'comment_type: str = "REM"' which means any programmatic creation without specifying comment_type will default to "REM", potentially misrepresenting the original syntax if the node is created from parsed apostrophe comments.

---



#### Documentation inconsistency

**Description:** TypeInfo class documentation describes dual purpose but implementation is unclear

**Affected files:**
- `src/ast_nodes.py`

**Details:**
TypeInfo docstring states: 'This class serves two purposes: 1. Static helper methods for type conversions 2. Compatibility layer: Class attributes (INTEGER, SINGLE, etc.) alias VarType enum values to support legacy code using TypeInfo.INTEGER instead of VarType.INTEGER'. However, the implementation shows 'INTEGER = VarType.INTEGER' etc., which are simple aliases. The term 'compatibility layer' suggests this is for backward compatibility with older code, but there's no indication of deprecation or migration path.

---



#### Documentation inconsistency

**Description:** Missing documentation for char_start and char_end usage in StatementNode

**Affected files:**
- `src/ast_nodes.py`

**Details:**
StatementNode defines 'char_start: int = 0  # Character offset from start of line for highlighting' and 'char_end: int = 0    # Character offset end position for highlighting'. The comments mention 'highlighting' but don't explain what highlighting system uses these, how they're populated, or their relationship to the position_serializer mentioned in LineNode documentation.

---



#### Code vs Comment conflict

**Description:** PrintStatementNode keyword_token field presence contradicts usage documentation

**Affected files:**
- `src/ast_nodes.py`

**Details:**
PrintStatementNode has 'keyword_token: Optional[Token] = None  # Token for PRINT keyword (legacy, not currently used)' but the class docstring states 'Note: keyword_token fields are present in some statement nodes (PRINT, IF, FOR) but not others. These were intended for case-preserving keyword regeneration but are not currently used by position_serializer, which handles keyword case through case_keepy_string() instead.' This mentions a function 'case_keepy_string()' that is not defined or imported in this file, creating a dangling reference.

---



#### code_vs_comment

**Description:** UsingFormatter.format_numeric_field has confusing comment about sign behavior

**Affected files:**
- `src/basic_builtins.py`

**Details:**
At lines 234-239, the docstring states:
"Sign behavior:
- leading_sign: + at start, always adds + or - sign (reserves 1 char for sign)
- trailing_sign: + at end, always adds + or - sign (reserves 1 char for sign)
- trailing_minus_only: - at end, adds - for negative OR space for non-negative (reserves 1 char)"

But at line 318, the comment says:
"# Add sign to content width (trailing_minus_only ALWAYS adds a char, - or space)"

The docstring says 'adds - for negative OR space for non-negative' while the inline comment emphasizes 'ALWAYS adds a char'. These say the same thing but with different emphasis, which could be confusing.

---



#### code_vs_comment

**Description:** Long comment about identifier case handling could be more concise

**Affected files:**
- `src/case_string_handler.py`

**Details:**
At lines 48-60, there's a detailed comment:
"# Identifiers always preserve their original case in display.
# Unlike keywords, which can be forced to a specific case policy,
# identifiers (variable/function names) retain their case as typed.
# This matches MBASIC 5.21 behavior where identifiers are case-insensitive
# for matching but preserve display case.
#
# Note: This function ONLY handles display formatting (what the user sees).
# Case-insensitive matching occurs elsewhere:
# - At runtime: Variable lookups use canonicalized (lowercase) names as keys
#   in Runtime.variables and Runtime.arrays dictionaries (see runtime.py)
# - During parsing: Identifier comparison uses lowercase normalized forms
# This separation allows "MyVar", "myvar", and "MYVAR" to reference the same
# variable while each preserves its own display case when printed."

Followed by simple code at line 61:
"return original_text"

The comment is accurate but very long for a single return statement. This is more of a style issue than an inconsistency.

---



#### documentation

**Description:** Module docstring references 'MBASIC 5.21 (CP/M era MBASIC-80)' but doesn't explain version significance

**Affected files:**
- `src/basic_builtins.py`

**Details:**
At lines 1-7:
"Built-in functions for MBASIC 5.21 (CP/M era MBASIC-80).

BASIC built-in functions (SIN, CHR$, INT, etc.) and formatting utilities (TAB, SPC, USING).

Note: Version 5.21 refers to BASIC-80 Reference Manual Version 5.21."

The note clarifies that 5.21 refers to the manual version, but doesn't explain why this specific version was chosen or what features are specific to it. This is minor documentation incompleteness.

---



#### code_vs_comment

**Description:** Comment about leading sign padding behavior could be more precise

**Affected files:**
- `src/basic_builtins.py`

**Details:**
At line 323, comment states:
"# For leading sign: padding comes first, then sign immediately before number"

Then at lines 324-329:
"if spec['leading_sign']:
    # Add padding first (but only spaces, not asterisks for leading sign)
    result_parts.append(' ' * max(0, padding_needed))
    # Then the sign
    result_parts.append('-' if is_negative else '+')"

The inline comment at line 325 adds important detail '(but only spaces, not asterisks for leading sign)' that isn't in the comment at line 323. The line 323 comment should mention this restriction.

---



#### Documentation inconsistency

**Description:** Duplicate error code documentation mentions specific codes but not all duplicates

**Affected files:**
- `src/error_codes.py`

**Details:**
Module docstring states:
"Specific duplicates (from MBASIC 5.21 specification):
- DD: code 10 ("Duplicate definition") and code 68 ("Device unavailable")
- DF: code 25 ("Device fault") and code 61 ("Disk full")
- CN: code 17 ("Can't continue") and code 69 ("Communication buffer overflow")"

This is accurate based on ERROR_CODES dict, but the documentation doesn't explain WHY these duplicates exist or if this is intentional in the MBASIC 5.21 spec. It just states they exist.

---



#### Code vs Comment conflict

**Description:** Comment about variable name mangling doesn't mention all transformations

**Affected files:**
- `src/codegen_backend.py`

**Details:**
Method _mangle_variable_name() docstring says:
"Convert BASIC variable name to valid C identifier.

BASIC allows names like "I!", "COUNT%", "VALUE#"
C needs alphanumeric + underscore, no type suffixes."

But the code also:
1. Converts to lowercase: name = name.lower()
2. Adds 'v_' prefix for C keywords

The docstring doesn't mention the lowercase conversion or the keyword prefix, which are important transformations.

---



#### Documentation inconsistency

**Description:** Module docstring has redundant/conflicting information about FileIO usage

**Affected files:**
- `src/editing/manager.py`

**Details:**
The module docstring has two sections explaining the same thing:

1. "FILE I/O ARCHITECTURE:" section explains ProgramManager has its own file I/O
2. "Why ProgramManager has its own file I/O methods:" section repeats similar information

Then it says:
"Note: ProgramManager.load_from_file() returns (success, errors) tuple where errors
is a list of (line_number, error_message) tuples for direct UI error reporting,
while FileIO.load_file() returns raw file text."

This note contradicts the earlier claim that "BASIC commands (LOAD/SAVE) go through FileIO abstraction first" - if FileIO.load_file() returns raw text, how does it integrate with ProgramManager's error reporting?

---



#### documentation_inconsistency

**Description:** Module docstring describes two filesystem abstractions (FileIO and FileSystemProvider) with intentional overlap, but FileIO is referenced as 'src/file_io.py' which is not included in the provided source files, making it impossible to verify the claimed relationship

**Affected files:**
- `src/filesystem/base.py`

**Details:**
From base.py docstring:
"TWO FILESYSTEM ABSTRACTIONS (with some intentional overlap):
1. FileIO (src/file_io.py) - Program management operations
   - Used by: Interactive mode, UI file browsers
   - Operations: FILES (list), LOAD/SAVE/MERGE (program files), KILL (delete)
   - Purpose: Load .BAS programs into memory, save from memory to disk

2. FileSystemProvider (this file) - Runtime file I/O"

The referenced src/file_io.py is not provided, so the relationship and overlap cannot be verified.

---



#### code_vs_documentation

**Description:** Module docstring mentions 'Implementation note: Uses standard Python type hints (e.g., tuple[str, bool]) which require Python 3.9+' but doesn't specify what the minimum Python version requirement is for the entire project

**Affected files:**
- `src/input_sanitizer.py`

**Details:**
Module docstring:
"Implementation note: Uses standard Python type hints (e.g., tuple[str, bool])
which require Python 3.9+. For earlier Python versions, use Tuple[str, bool] from typing."

This suggests the code requires Python 3.9+, but no project-wide Python version requirement is documented in the provided files. If the project supports Python 3.8 or earlier, this module would be incompatible.

---



#### code_vs_comment

**Description:** SandboxedFileSystemProvider docstring emphasizes 'IMPORTANT: Caller must ensure user_id is securely generated/validated' but the class itself has no validation or security checks on user_id, relying entirely on caller responsibility

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
Class docstring:
"Security:
- No access to real filesystem
- No path traversal (../ etc.)
- Resource limits enforced
- Per-user isolation via user_id keys in class-level storage
  IMPORTANT: Caller must ensure user_id is securely generated/validated
  to prevent cross-user access (e.g., use session IDs, not user-provided values)"

__init__ docstring:
"Args:
    user_id: Unique identifier for this user/session
            SECURITY: Must be securely generated/validated (e.g., session IDs)
            to prevent cross-user access. Do NOT use user-provided values."

The class accepts any string as user_id without validation. This is a design choice (security is caller's responsibility), but the repeated warnings suggest this might be a security concern that should be enforced at the class level.

---



#### code_vs_comment

**Description:** Comment says 'Immediate mode statements: All other commands (RUN, LIST, SAVE, LOAD, NEW, MERGE, FILES, SYSTEM, DELETE, RENUM, etc.) are handled directly by execute_immediate() methods' but code shows many are handled as special cases before execute_immediate()

**Affected files:**
- `src/interactive.py`

**Details:**
Module docstring (line 9-10) says:
"- Immediate mode statements: All other commands (RUN, LIST, SAVE, LOAD, NEW, MERGE, FILES, SYSTEM, DELETE, RENUM, etc.) are handled directly by execute_immediate() methods"

But in execute_command() (line 205-228), the code shows:
- AUTO, EDIT, HELP are handled as special cases (lines 217-223)
- Everything else goes to execute_immediate() (line 226)

The comment incorrectly lists commands that are NOT handled by execute_immediate() (AUTO, EDIT, HELP are special cases).

---



#### documentation_inconsistency

**Description:** Module docstring lists commands in different order than they appear in code

**Affected files:**
- `src/interactive.py`

**Details:**
Module docstring (line 9) lists:
"RUN, LIST, SAVE, LOAD, NEW, MERGE, FILES, SYSTEM, DELETE, RENUM, etc."

But the actual command methods in the class are defined in order:
cmd_run, cmd_cont, cmd_list, cmd_new, cmd_save, cmd_load, cmd_merge, cmd_chain, cmd_delete, cmd_renum, cmd_edit

The docstring omits CHAIN and CONT which are significant commands, and lists them in a different order than implementation.

---



#### code_vs_comment

**Description:** Comment says readline provides 'Emacs keybindings (Ctrl+K, Ctrl+U, etc.)' but Ctrl+A is explicitly rebound to self-insert, breaking Emacs beginning-of-line

**Affected files:**
- `src/interactive.py`

**Details:**
Comment in start() (line 24-30) says:
"# Try to import readline for better line editing
# This enhances input() with:
# - Backspace/Delete working properly
# - Arrow keys for navigation
# - Command history (up/down arrows)
# - Ctrl+A (start of line), Ctrl+E (end of line)
# - Emacs keybindings (Ctrl+K, Ctrl+U, etc.)"

But _setup_readline() (line 113) explicitly rebinds Ctrl+A:
"readline.parse_and_bind('Control-a: self-insert')"

With comment explaining:
"# Bind Ctrl+A to insert the character (ASCII 0x01) into the input line,
# overriding the default Ctrl+A (beginning-of-line) behavior."

The initial comment is misleading - Ctrl+A does NOT work as beginning-of-line because it's rebound for EDIT mode.

---



#### code_vs_comment_conflict

**Description:** Comment about line_text_map being empty for immediate mode contradicts its stated purpose

**Affected files:**
- `src/interactive.py`

**Details:**
In execute_immediate() around line 1035:

Comment: "Pass empty line_text_map since immediate mode uses temporary line 0\n(no source line text available for error reporting, but this is fine\nfor immediate mode where the user just typed the statement)"

However, the source line text IS available - it's the 'statement' parameter passed to execute_immediate(). The comment claims source text isn't available, but it could easily be passed as {0: statement} to improve error reporting in immediate mode.

---



#### documentation_inconsistency

**Description:** cmd_files docstring mentions unsupported drive letter syntax but doesn't explain why or what alternatives exist

**Affected files:**
- `src/interactive.py`

**Details:**
In cmd_files() docstring:

"Note: Drive letter syntax (e.g., 'A:*.*') is not supported in this implementation."

This note mentions a limitation but provides no context about:
- Why it's not supported (design decision vs. future feature)
- What the alternative is for users expecting MBASIC compatibility
- Whether this is a permanent limitation or planned feature

---



#### code_vs_comment_conflict

**Description:** Comment about sanitize_and_clear_parity return value ignores second return value without explanation

**Affected files:**
- `src/interactive.py`

**Details:**
In cmd_auto() around line 970:

Code: "line_text, _ = sanitize_and_clear_parity(line_text)"

Comment: "Sanitize input: clear parity bits and filter control characters"

The comment describes what sanitize_and_clear_parity does but doesn't explain what the ignored second return value (captured as _) represents or why it's not needed. This makes the code harder to understand for maintainers.

---



#### code_vs_comment

**Description:** Comment about return_stmt validation mentions 'strictly greater than' but doesn't explain the sentinel value clearly in validation logic

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1010 states:
# return_stmt is 0-indexed offset into statements array.
# Valid range:
#   - 0 to len(statements)-1: Normal statement positions (existing statements)
#   - len(statements): Special sentinel value - FOR was last statement on line,
#                      continue execution at next line (no more statements to execute on current line)
#   - > len(statements): Invalid - indicates the statement was deleted
#
# Validation: Check for strictly greater than (== len is OK as sentinel)
if return_stmt > len(line_statements):

The comment is clear, but the validation logic comment 'Check for strictly greater than (== len is OK as sentinel)' could be misread as checking '> len' when it should say 'strictly greater than len' or '> len(statements)' to be unambiguous.

---



#### code_vs_comment

**Description:** Comment about OPTION BASE says 'strictly enforced' but doesn't mention what happens if base is not 0 or 1

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1290 states:
MBASIC 5.21 restrictions (strictly enforced):
- OPTION BASE can only be executed once per program run
- Must be executed BEFORE any arrays are dimensioned (implicit or explicit)
- Violating either condition raises 'Duplicate Definition' error

Syntax: OPTION BASE 0 | 1

The comment doesn't mention what happens if stmt.base is not 0 or 1. The code doesn't validate this, so presumably the parser handles it, but the comment should clarify this or the code should validate.

---



#### code_vs_comment

**Description:** Comment about _read_line_from_file encoding mentions CP437/CP850 but doesn't explain when conversion is needed

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1430 states:
Encoding:
Uses latin-1 (ISO-8859-1) to preserve byte values 128-255 unchanged.
CP/M and MBASIC used 8-bit characters; latin-1 maps bytes 0-255 to
Unicode U+0000-U+00FF, allowing round-trip byte preservation.
Note: CP/M systems often used code pages like CP437 or CP850 for characters
128-255, which do NOT match latin-1. Latin-1 preserves the BYTE VALUES but
not necessarily the CHARACTER MEANING for non-ASCII CP/M text. Conversion
may be needed for accurate display of non-English CP/M files.

The comment says 'Conversion may be needed' but doesn't explain where or how this conversion should happen. Is this a TODO? Should the caller handle it? Should there be a setting? This is unclear.

---



#### code_vs_comment

**Description:** Comment about DELETE says it preserves variables but doesn't mention other state

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1800 states:
Note: This implementation preserves variables when deleting lines. NEW clears both
lines and variables (execute_new calls clear_variables/clear_arrays), while DELETE
only removes lines from the program AST, leaving variables intact.

The comment only mentions variables/arrays but doesn't clarify whether other state like open files, error handlers, loop stacks, etc. are preserved. This should be clarified.

---



#### code_vs_comment

**Description:** Comment about CLOSE says 'Silently ignores closing unopened files' but doesn't explain why

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~2050 states:
Note: Silently ignores closing unopened files (MBASIC 5.21 compatibility)

Code at line ~2060:
if file_num in self.runtime.files:
    self.runtime.files[file_num]['handle'].close()
    del self.runtime.files[file_num]
# Silently ignore closing unopened files (like MBASIC)

The comment explains this is for MBASIC compatibility, but doesn't explain WHY MBASIC does this. Is it because CLOSE is often used defensively (CLOSE #1: CLOSE #2: CLOSE #3) to ensure files are closed? This context would be helpful.

---



#### code_vs_comment

**Description:** Comment about string length limit mentions both character and byte count but doesn't clarify potential Unicode issues

**Affected files:**
- `src/interpreter.py`

**Details:**
In evaluate_binaryop(), the comment states:
'Also note: len() counts characters. For ASCII and latin-1 (both single-byte encodings), character count equals byte count. Field buffers (LSET/RSET) use latin-1 encoding.'

While the code uses len(result) > 255 for string concatenation limit, the comment only addresses ASCII/latin-1. If the interpreter accepts Unicode strings elsewhere, this could be inconsistent. The comment assumes single-byte encodings but doesn't verify the string is actually in that encoding.

---



#### code_vs_comment

**Description:** Comment about debugger_set parameter usage is verbose but the actual tracking distinction may not be clear to maintainers

**Affected files:**
- `src/interpreter.py`

**Details:**
In evaluate_functioncall(), the comment explains:
'Note: get_variable_for_debugger() and debugger_set=True are used to avoid triggering variable access tracking. This save/restore is internal function call machinery, not user-visible variable access. The tracking system (if enabled) distinguishes between: - User code variable access (tracked for debugging/variables window) - Internal implementation details (not tracked)'

While informative, this comment suggests a complex tracking system that may have edge cases. The distinction between 'user code' and 'internal' access could be fragile if not consistently applied throughout the codebase.

---



#### Documentation inconsistency

**Description:** input_line() documentation in base.py describes it as 'LINE INPUT statement' but the actual BASIC statement name is inconsistently referenced

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/console.py`
- `src/iohandler/curses_io.py`
- `src/iohandler/web_io.py`

**Details:**
base.py docstring: "Input a complete line from user (LINE INPUT statement)."
console.py docstring: "Input a complete line from console."
curses_io.py docstring: "Input a full line (LINE INPUT statement)."
web_io.py docstring: "Get a complete line from user via dialog (LINE INPUT statement)."

The terminology varies between 'complete line', 'full line', and references to 'LINE INPUT statement' are inconsistent.

---



#### Documentation inconsistency

**Description:** Module docstring mentions 'embedded' as a use case but no EmbeddedIOHandler is provided or mentioned elsewhere

**Affected files:**
- `src/iohandler/__init__.py`
- `src/iohandler/base.py`

**Details:**
__init__.py: "allowing the interpreter to work with different I/O backends (console, GUI, curses, embedded, etc.)."

base.py: "This allows the MBASIC interpreter to work with any I/O system without modifying the core interpreter logic."

No EmbeddedIOHandler exists in the codebase, and 'embedded' is only mentioned in __init__.py but not in base.py's list of examples.

---



#### Documentation inconsistency

**Description:** Module docstring references SimpleKeywordCase in src/simple_keyword_case.py but this file is not provided in the source code files

**Affected files:**
- `src/keyword_case_manager.py`

**Details:**
keyword_case_manager.py docstring: "For simpler force-based policies in the lexer, see SimpleKeywordCase (src/simple_keyword_case.py) which only supports force_lower, force_upper, and force_capitalize."

The file src/simple_keyword_case.py is not included in the provided source code files, making this reference unverifiable.

---



#### Code vs Comment conflict

**Description:** input_char() docstring says 'blocking parameter value' is 'ignored' but also says method 'always returns empty string immediately, regardless of the blocking parameter'

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Docstring says:
"Args:
    blocking: Accepted for interface compatibility but ignored in web UI.

Returns:
    Empty string (character input not supported in web UI)

Note: Character input is not supported in web UI. This method always returns an empty string immediately, regardless of the blocking parameter value."

The Args section says 'ignored' while the Note section says 'regardless of', which is redundant. The implementation also doesn't use the blocking parameter at all:
def input_char(self, blocking=True):
    return ""

This is consistent but the documentation is verbose and repetitive.

---



#### code_vs_comment

**Description:** Comment in parse_print() says comma after file number is optional, but MBASIC 5.21 typically requires it

**Affected files:**
- `src/parser.py`

**Details:**
Comment in parse_print() says:
"# Optionally consume comma after file number
# Note: MBASIC 5.21 typically uses comma (PRINT #1, 'text').
# Our parser makes the comma optional for flexibility."

This suggests the parser is more lenient than MBASIC 5.21 spec, which could lead to accepting invalid MBASIC programs. The comment acknowledges this but doesn't explain why this deviation is acceptable.

---



#### code_vs_comment

**Description:** Comment about semicolon handling in parse_line() is confusing about when semicolons are valid

**Affected files:**
- `src/parser.py`

**Details:**
In parse_line():
"elif self.match(TokenType.SEMICOLON):
    # Allow trailing semicolon at end of line only (treat as no-op).
    # Context matters: Semicolons WITHIN PRINT/LPRINT are item separators (parsed there),
    # but semicolons BETWEEN statements are NOT valid in MBASIC.
    # MBASIC uses COLON (:) to separate statements, not semicolon (;).
    self.advance()
    # If there's more after the semicolon (except another colon or newline), it's an error
    if not self.at_end_of_line() and not self.match(TokenType.COLON):
        token = self.current()
        raise ParseError(f'Expected : or newline after ;, got {token.type.name}', token)"

The comment says 'Allow trailing semicolon at end of line only', but then checks for COLON after it, which would mean it's not at end of line. This is confusing about what 'trailing' means.

---



#### code_vs_comment

**Description:** Comment in parse_print() about separator count logic has confusing examples

**Affected files:**
- `src/parser.py`

**Details:**
In parse_print():
"# Add newline if there's no trailing separator
# Separator count vs expression count:
# - If separators < expressions: no trailing separator, add newline
# - If separators >= expressions: has trailing separator, no newline added
# Examples: 'PRINT A;B;C' has 2 separators for 3 items (no trailing sep, adds \n)
#           'PRINT A;B;C;' has 3 separators for 3 items (trailing sep, no \n)"

The logic is correct, but the phrasing 'separators < expressions' vs 'separators >= expressions' could be clearer. The examples help, but the mathematical comparison is slightly confusing since separators are parsed between and after expressions.

---



#### code_vs_comment

**Description:** Comment about MID$ tokenization may be misleading

**Affected files:**
- `src/parser.py`

**Details:**
In parse_mid_assignment() method around line 1850:

Comment states: "Note: The lexer tokenizes 'MID$' in source as a single MID token (the $ is part of the keyword, not a separate token)."

Then code shows:
token = self.current()  # MID token (represents 'MID$' from source)

This is consistent, but the comment could be clearer about whether the token type is actually called 'MID' or 'MID$' in the TokenType enum. The comment suggests the $ is stripped during lexing, but doesn't explicitly state what the token type name is.

---



#### code_vs_comment

**Description:** Comment about dimension expressions in DIM statement may not match all BASIC dialects

**Affected files:**
- `src/parser.py`

**Details:**
In parse_dim() method around line 1750:

Comment states: "Dimension expressions: This implementation accepts any expression for array dimensions (e.g., DIM A(X*2, Y+1)), with dimensions evaluated at runtime. This matches MBASIC 5.21 behavior. Note: Some compiled BASICs (e.g., QuickBASIC) may require constants only."

The code implementation does accept any expression:
dim_expr = self.parse_expression()
dimensions.append(dim_expr)

This is consistent, but the comment makes a claim about "MBASIC 5.21 behavior" without providing a reference or verification. This could be misleading if MBASIC 5.21 actually has different behavior.

---



#### documentation_inconsistency

**Description:** Inconsistent documentation style for statement syntax descriptions

**Affected files:**
- `src/parser.py`

**Details:**
Throughout the parser methods, syntax documentation uses inconsistent formatting:

Some use indented examples:
  parse_lprint(): "Syntax:\n    LPRINT expr1, expr2         - Print to printer\n    LPRINT #filenum, expr1      - Print to file"

Others use simple lists:
  parse_input(): "Syntax:\n    INPUT var1, var2           - Read from keyboard\n    INPUT \"prompt\"; var1       - Read with prompt"

Others use bullet points:
  parse_on(): "Syntax:\n        - ON expression GOTO line1, line2, ...\n        - ON expression GOSUB line1, line2, ..."

This inconsistency makes the documentation harder to read and maintain.

---



#### code_vs_comment

**Description:** parse_resume() docstring states 'RESUME 0 also retries the error statement (interpreter treats 0 and None equivalently)' but the code stores the actual value 0, not None

**Affected files:**
- `src/parser.py`

**Details:**
Comment says: "Note: RESUME 0 means 'retry error statement' (interpreter treats 0 and None equivalently)
We store the actual value (0 or other line number) for the AST"

The comment claims 0 and None are treated equivalently by the interpreter, but the code explicitly stores 0 when parsed, not None. This creates ambiguity about whether line_number=0 and line_number=None should be treated identically downstream.

---



#### code_vs_comment

**Description:** serialize_let_statement docstring claims 'The AST doesn\'t track whether LET was originally present' but this is an intentional design decision, not a limitation. The comment could be clearer about this being by design.

**Affected files:**
- `src/position_serializer.py`

**Details:**
Comment says: 'The AST doesn\'t track whether LET was originally present (intentional simplification)'

This phrasing suggests it could track it but chooses not to. More accurate would be: 'The AST intentionally does not distinguish between explicit LET and implicit assignment forms, as they are semantically equivalent.'

---



#### documentation_inconsistency

**Description:** PC class examples show notation like 'PC(10.0)' and 'PC(10.2)' but the __repr__ method outputs 'PC(10.0)' format. The examples use dot notation but don't clarify if this is just documentation shorthand or actual syntax.

**Affected files:**
- `src/pc.py`

**Details:**
Examples in docstring:
    PC(10.0)  - First statement on line 10 (stmt_offset=0)
    PC(10.2)  - Third statement on line 10 (stmt_offset=2)

__repr__ implementation:
    return f"PC({self.line_num}.{self.stmt_offset})"

The examples match the repr output, so this is consistent. However, the constructor signature is PC(line_num, stmt_offset), not PC(10.0) as a single float. The examples could clarify this is the string representation, not constructor syntax.

---



#### code_vs_comment

**Description:** PositionSerializer.__init__ docstring says 'If None (default), keywords are forced to lowercase (fallback mode)' but emit_keyword implementation shows fallback uses keyword.lower(), which matches. However, apply_keyword_case_policy with no manager would use capitalize() for unknown policies.

**Affected files:**
- `src/position_serializer.py`

**Details:**
__init__ docstring: 'keyword_case_manager: KeywordCaseManager instance (from parser) with keyword case table.
                          If None (default), keywords are forced to lowercase (fallback mode).'

emit_keyword code:
    if self.keyword_case_manager:
        keyword_with_case = self.keyword_case_manager.get_display_case(keyword)
    else:
        # Fallback if no manager provided (default to lowercase)
        keyword_with_case = keyword.lower()

This is consistent. However, apply_keyword_case_policy has different fallback behavior (capitalize for unknown policy), which could cause confusion if used independently.

---



#### Code vs Comment conflict

**Description:** Comment describes array indexing convention but implementation responsibility is unclear

**Affected files:**
- `src/resource_limits.py`

**Details:**
In check_array_allocation(), the comment states:
'# Note: DIM A(N) creates N+1 elements (0 to N) in MBASIC 5.21
# We use this convention here to calculate the correct size for limit checking only.
# The actual array creation/initialization is handled by execute_dim() in interpreter.py.'

The code then uses: total_elements *= (dim_size + 1)  # +1 for 0-based indexing (0 to N)

This creates ambiguity: if execute_dim() handles actual array creation, why does check_array_allocation() need to know about the +1 convention? The comment suggests this is just for size calculation, but it's unclear if execute_dim() uses the same convention or if there could be a mismatch.

---



#### Documentation inconsistency

**Description:** Inconsistent terminology for string length measurement

**Affected files:**
- `src/resource_limits.py`

**Details:**
The __init__ docstring says 'max_string_length: Maximum byte length for a string variable (UTF-8 encoded). MBASIC 5.21 limit is 255 bytes.' but the check_string_length() docstring says 'String limits are measured in bytes (UTF-8 encoded), not character count. This matches MBASIC 5.21 behavior which limits string storage size.' The first uses 'byte length' while the second uses 'bytes' and 'storage size'. While these mean the same thing, consistent terminology would be clearer.

---



#### Code vs Comment conflict

**Description:** Comment about MBASIC 5.21 compatibility may be outdated or incomplete

**Affected files:**
- `src/resource_limits.py`

**Details:**
Multiple comments state '255 bytes (MBASIC 5.21 compatibility)' but there's no documentation explaining what other aspects of MBASIC 5.21 are or aren't compatible. The comment in create_unlimited_limits() warns about breaking compatibility, but it's unclear if other limits (memory, array sizes, etc.) also need specific values for MBASIC 5.21 compatibility or if only string length matters.

---



#### Documentation inconsistency

**Description:** Module docstrings reference each other but with slightly different descriptions

**Affected files:**
- `src/resource_limits.py`
- `src/resource_locator.py`

**Details:**
resource_limits.py says: 'Note: This is distinct from resource_locator.py which finds package data files.'
resource_locator.py says: 'Note: This is distinct from resource_limits.py which enforces runtime execution limits.'

The first describes resource_locator as finding 'package data files' while resource_locator's own docstring describes itself as finding 'package resources (data files, docs, examples)'. The term 'package data files' vs 'package resources' is inconsistent.

---



#### code_vs_comment

**Description:** Comment about set_variable() token requirement doesn't mention FakeToken usage pattern

**Affected files:**
- `src/runtime.py`

**Details:**
Lines 295-310 docstring says token is REQUIRED unless debugger_set=True, but doesn't mention the FakeToken pattern used by set_variable_raw().

Line 437-451 set_variable_raw() docstring explains:
"Internally calls set_variable() with a FakeToken(line=-1) to mark this as
a system/internal set (not from program execution)."

This FakeToken pattern is a third way to call set_variable() (beyond normal token and debugger_set=True), but it's not documented in set_variable()'s docstring. Users reading set_variable() won't know about this pattern.

---



#### code_vs_comment

**Description:** Comment in _get_global_settings_path() and _get_project_settings_path() says methods are 'not currently used' but they may be used for manual path queries

**Affected files:**
- `src/settings.py`

**Details:**
Methods have comment: 'Note: This method is not currently used. Path resolution has been delegated to the backend...Kept for potential future use or manual path queries.'

The comment is accurate that these methods aren't called by SettingsManager itself (backend handles paths), but saying 'not currently used' is ambiguous - they could be called externally. Better wording: 'not called internally' or 'not used by SettingsManager'.

---



#### documentation_inconsistency

**Description:** Module docstrings describe different storage locations for global settings

**Affected files:**
- `src/settings.py`
- `src/settings_backend.py`

**Details:**
src/settings.py docstring: 'Global: ~/.mbasic/settings.json (Linux/Mac) or %APPDATA%/mbasic/settings.json (Windows)'

src/settings_backend.py FileSettingsBackend docstring: 'Global: ~/.mbasic/settings.json (Linux/Mac) or %APPDATA%/mbasic/settings.json (Windows)'

Both are consistent, but the actual implementation in _get_global_settings_path() uses:
Windows: os.getenv('APPDATA', os.path.expanduser('~')) / 'mbasic'

The fallback to os.path.expanduser('~') when APPDATA is not set is not documented. This means on Windows without APPDATA env var, it would use ~/mbasic instead of %APPDATA%/mbasic.

---



#### code_vs_comment

**Description:** RedisSettingsBackend.load_project() docstring says 'returns empty dict' but implementation could return None in error cases

**Affected files:**
- `src/settings_backend.py`

**Details:**
Docstring: 'Load project settings (returns empty dict in Redis mode). In Redis mode, all settings are session-scoped, not project-scoped. This method returns an empty dict rather than None for consistency.'

Implementation:
def load_project(self) -> Dict[str, Any]:
    return {}

This is consistent. However, the parent class SettingsBackend has abstract method signature that returns Dict[str, Any], which doesn't allow None. The comment 'rather than None' suggests there was consideration of returning None, but the type hints prevent it. Comment is slightly misleading.

---



#### documentation_inconsistency

**Description:** Comment says 'editor.tab_size setting not included' but doesn't explain why it's mentioned

**Affected files:**
- `src/settings_definitions.py`

**Details:**
After editor.auto_number_step definition, there's a comment:
'# Note: editor.tab_size setting not included - BASIC uses line numbers for program structure, not indentation, so tab size is not a meaningful setting for BASIC source code'

This comment references a setting that was never defined or discussed elsewhere in the code. It's unclear why this specific non-existent setting is called out. Either:
1. It was planned and removed (should document why)
2. It's a comparison to other editors (should clarify)
3. It's defensive documentation (should explain context)

---



#### code_vs_comment

**Description:** register_keyword() docstring says parameters are 'unused' but they're used for signature compatibility

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
Docstring: 'line_num: Line number (unused - required for KeywordCaseManager compatibility)'

The parameters ARE used - for maintaining API compatibility. Saying 'unused' is technically correct (not used in computation) but misleading. Better wording: 'not used by force-based policies' or 'reserved for compatibility with KeywordCaseManager'.

---



#### documentation_inconsistency

**Description:** KEYWORDS dict comment says 'lexer normalizes to lowercase' but doesn't specify when

**Affected files:**
- `src/tokens.py`

**Details:**
Comment: '# Keywords mapping (case-insensitive, use lowercase since lexer normalizes to lowercase)'

This implies the lexer normalizes keywords before lookup, but doesn't specify:
1. Whether normalization happens before or after keyword detection
2. Whether original case is preserved anywhere
3. How this interacts with keyword case policies

The comment is accurate but incomplete for understanding the full keyword processing flow.

---



#### code_vs_comment

**Description:** Module docstring says 'different UI types' but only lists backend types, not actual UI types

**Affected files:**
- `src/ui/__init__.py`

**Details:**
Docstring: 'This module provides abstract interfaces and implementations for different UI types (CLI, GUI, web, mobile, etc.).'

The code imports: UIBackend, CLIBackend, VisualBackend, TkBackend, CursesBackend

These are all desktop UI types (CLI, terminal, GUI). There's no web or mobile backend. The docstring overpromises what's available. Should say 'different UI backends (CLI, terminal, GUI)' or remove 'web, mobile' from the list.

---



#### Code vs Documentation inconsistency

**Description:** Inconsistent terminology for stepping commands between CLI and curses

**Affected files:**
- `src/ui/curses_keybindings.json`
- `src/ui/cli_keybindings.json`

**Details:**
curses_keybindings.json uses:
- 'step_line': 'Step Line (execute all statements on current line)' for Ctrl+K
- 'step': 'Step statement (execute one statement)' for Ctrl+T

cli_keybindings.json uses:
- 'step': 'Execute next statement or n statements - statement-level only, not line-level'

The curses UI distinguishes between 'Step Line' and 'Step statement' while CLI only has 'step' (statement-level). The documentation should clarify this difference more explicitly.

---



#### Documentation inconsistency

**Description:** get_additional_keybindings() function has extensive documentation but returns empty dict when readline unavailable

**Affected files:**
- `src/ui/cli.py`

**Details:**
The get_additional_keybindings() function has a detailed docstring explaining why readline keybindings are NOT in cli_keybindings.json and documenting all the readline keybindings. However, when readline is not available (which could be common on some platforms), it returns an empty dict {}. The docstring doesn't mention this behavior or explain what happens when readline is unavailable, which could confuse users expecting those keybindings to be documented.

---



#### Code vs Documentation inconsistency

**Description:** Comment claims all shortcuts use constants but hardcoded arrow symbols used

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
Comment in _create_body() states: 'Note: All shortcuts use constants from keybindings module to ensure footer display matches actual key handling in keypress() method'

However, the footer text uses hardcoded arrow symbols: '↑↓ {key_to_display(ENTER_KEY)}=OK'

The up/down arrows are not using constants from the keybindings module, contradicting the comment's claim that 'all shortcuts use constants'.

---



#### Code vs Comment conflict

**Description:** Comment about stripping 'force_' prefix uses deprecated hasattr check

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
In _create_setting_widget(), the code has:
display_label = choice.removeprefix('force_') if hasattr(str, 'removeprefix') else (choice[6:] if choice.startswith('force_') else choice)

With comment: '# Strip force_ prefix from beginning for cleaner display'

The hasattr(str, 'removeprefix') check suggests compatibility code for older Python versions, but this is inconsistent with modern Python practices. The comment doesn't explain why this compatibility check exists or what Python version is being targeted.

---



#### Documentation inconsistency

**Description:** UIBackend docstring lists future backend types but contradicts itself about batch execution

**Affected files:**
- `src/ui/base.py`

**Details:**
The docstring states: 'Future/potential backend types (not yet implemented):
- WebBackend: Browser-based interface'

Then immediately says: 'Note: Non-interactive/batch execution (running programs from command line without UI) is intentionally not included as a UIBackend type, as it would contradict the purpose of the UIBackend abstraction. Batch execution is better handled outside this framework.'

This note seems oddly placed since WebBackend was just mentioned as a future type, not batch execution. The note appears to be preemptively addressing a question nobody asked in this context.

---



#### Code vs Documentation inconsistency

**Description:** CapturingIOHandler has minimal documentation despite being used by various UI backends

**Affected files:**
- `src/ui/capturing_io_handler.py`

**Details:**
The module docstring is very brief: 'Capturing IO Handler for output buffering.

This module provides a simple IO handler that captures output to a buffer, used by various UI backends for executing commands and capturing their output.'

However, there's no documentation about:
- Which UI backends use it
- How it differs from other IO handlers
- When to use it vs other IO handlers
- The class itself has no docstring
- Methods have no docstrings

Given that it's described as being used by 'various UI backends', more comprehensive documentation would be helpful.

---



#### code_vs_comment

**Description:** Comment says 'Never edit code to match comments without getting explicit permission' but this is meta-guidance, not code documentation

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line ~1046: "# Never edit code to match comments without getting explicit
#        permission.  Code updates often do not update the comments"

This appears to be instructions for code reviewers/maintainers rather than documentation of the code's behavior. It's misplaced as an inline comment.

---



#### code_vs_comment

**Description:** Comment about 'use None instead of not' is overly defensive for a simple check

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line ~906: "# Check if output walker is available (use 'is None' instead of 'not' to avoid false positive on empty walker)"

The comment suggests 'not self._output_walker' could give false positives on empty walkers, but urwid walkers don't have a __bool__ that returns False when empty. The 'is None' check is correct but the justification is misleading.

---



#### code_vs_comment

**Description:** Bug fix comment describes incrementing next_auto_line_num prematurely but doesn't explain the fix mechanism

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line ~467: "# DON'T increment counter here - that happens only on Enter
# Bug fix: Incrementing here caused next_auto_line_num to advance prematurely,
# displaying the wrong line number before the user typed anything"

The comment describes the bug but doesn't explain that the fix is to only increment in the Enter key handler (line ~640). A reader might wonder where the increment actually happens.

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
1. In __init__ (line ~260): immediate_io = OutputCapturingIOHandler()
2. In start() (line ~310): immediate_io = OutputCapturingIOHandler()

The comment implies it's only temporary in __init__, but both instances are actually used - one for Interpreter initialization, one for ImmediateExecutor initialization.

---



#### code_vs_comment

**Description:** Comment says 'Toolbar removed from UI layout' but there's no evidence a toolbar ever existed in this code

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~383:
# Toolbar removed from UI layout - use Ctrl+U interactive menu bar instead for keyboard navigation

This comment suggests a toolbar was removed, but:
1. No toolbar widget is defined anywhere in the visible code
2. No commented-out toolbar code is present
3. The comment may be outdated from a previous refactoring

---



#### code_vs_comment

**Description:** Comment about _setup_program() in _debug_step() and _debug_step_line() but this method is not shown in the provided code

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Both _debug_step() (line ~710) and _debug_step_line() (line ~790) call:
if not self._setup_program():
    return  # Setup failed (error already displayed)

The method _setup_program() is referenced but not defined in the provided code excerpt. This could be defined elsewhere in the file (part 1) or could be missing.

---



#### code_vs_comment

**Description:** Comment about main widget storage strategy differs between methods but implementation is consistent

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _show_help (line ~449), _show_keymap (line ~476), and _show_settings (line ~629), comments state:
"Main widget retrieval: Use self.base_widget (stored at UI creation time in __init__)
rather than self.loop.widget (which reflects the current widget and might be a menu
or other overlay)."

But in _activate_menu (line ~540), comment states:
"Extract base widget from current loop.widget to unwrap any existing overlay.
This differs from _show_help/_show_keymap/_show_settings which use self.base_widget
directly, since menu needs to work even when other overlays are already present."

The comments accurately describe different strategies for different use cases, but the verbosity and repetition across multiple methods suggests these could be consolidated or referenced to a single explanation.

---



#### code_vs_comment

**Description:** Comment about immediate mode status updates is inconsistent across error handling paths

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple locations have comments like:
- Line ~1074: "Don't update immediate status here - error is displayed in output"
- Line ~1168: "Don't update immediate status on exception - error is in output"
- Line ~1207: "Don't update immediate status here - error is displayed in output"
- Line ~1224: "Don't update immediate status here - error is displayed in output"

But then at line ~1226 and ~1243, the code DOES call self._update_immediate_status() after errors. This suggests either:
1. The comments are outdated and immediate status should be updated after errors
2. The code is wrong and shouldn't update immediate status
3. There's a distinction between error types that isn't clearly documented

---



#### code_vs_comment

**Description:** Comment about PC setting timing may be misleading

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
At line ~1119, comment states:
"If start_line is specified (e.g., RUN 100), set PC to that line
This must happen AFTER interpreter.start() because start() calls setup()
which resets PC to the first line in the program. By setting PC here,
we override that default and begin execution at the requested line."

While technically accurate, this comment doesn't explain WHY this design exists or if it's intentional that start() resets PC only to have it immediately overridden. This could indicate a design issue where start() shouldn't reset PC if a start_line is provided.

---



#### code_vs_comment

**Description:** Comment in _execute_immediate says 'Don't call interpreter.start() here' but then explains why, suggesting there may have been a bug where it was called

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1625:
# NOTE: Don't call interpreter.start() here. The immediate executor handles
# program start setup (e.g., RUN command sets PC appropriately via
# interpreter.start()). This function only ensures InterpreterState exists
# for tick-based execution tracking. If we called interpreter.start() here,
# it would reset PC to the beginning, overriding the PC set by RUN command.

This defensive comment suggests there may have been confusion or a bug. The detailed explanation of what would go wrong if interpreter.start() were called indicates this might have been an actual issue that was fixed.

---



#### code_vs_comment

**Description:** Comment says 'Sync program to runtime (updates statement table and line text map)' but doesn't mention it also handles PC state

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1577:
# Sync program to runtime (updates statement table and line text map).
# If execution is running, _sync_program_to_runtime preserves current PC.
# If not running, it sets PC to halted. Either way, this doesn't start execution,
# but allows commands like LIST to see the current program.
self._sync_program_to_runtime()

The comment describes PC handling inline but the method's docstring (at line ~1165) describes much more complex PC handling including breakpoint logic. The inline comment is incomplete/simplified.

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

**Description:** Comment describes CONTINUE_KEY as dual-purpose (Go to line / Continue execution) but the JSON key name 'goto_line' only reflects one purpose

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Comment at line ~165 says:
# Go to line (also used for Continue execution in debugger context)
# Note: This key serves dual purpose - "Go to line" in editor mode and
# "Continue execution (Go)" in debugger mode. The JSON key is 'goto_line'
# to reflect its primary function, but CONTINUE_KEY name reflects debugger usage.

This is internally consistent but creates potential confusion between the constant name (CONTINUE_KEY), the JSON key name (goto_line), and the actual dual functionality.

---



#### Code vs Documentation inconsistency

**Description:** keymap_widget.py converts key display format but keybindings.py already has key_to_display() function that does similar conversion

**Affected files:**
- `src/ui/keymap_widget.py`
- `src/ui/keybindings.py`

**Details:**
In keymap_widget.py:
def _format_key_display(key_str):
    """Convert Ctrl+ notation to ^ notation for consistency."""
    if key_str.startswith('Ctrl+'):
        return '^' + key_str[5:]
    elif key_str.startswith('Shift+Ctrl+'):
        return 'Shift+^' + key_str[11:]
    return key_str

But keybindings.py already has:
def key_to_display(urwid_key):
    """Convert urwid key name to user-friendly display string."""
    # Returns strings like '^A', '^R', '^Shift+B'

The keymap_widget is re-converting keys that were already converted by key_to_display(), and the conversion logic differs slightly (Shift+^V vs ^Shift+V).

---



#### Documentation inconsistency

**Description:** Module docstring says 'Not thread-safe (no locking mechanism)' but doesn't explain implications or suggest alternatives

**Affected files:**
- `src/ui/recent_files.py`

**Details:**
Docstring says:
Features:
- Stores last 10 recently opened files
- Records full path and last access timestamp
- Automatically creates config directory if needed
- Cross-platform (uses pathlib)
- Note: Not thread-safe (no locking mechanism)

This warning is mentioned but there's no guidance on whether this is a problem for the application, whether concurrent access is expected, or what users should do about it.

---



#### Code duplication with inconsistency risk

**Description:** Table formatting logic may be duplicated in markdown_renderer.py

**Affected files:**
- `src/ui/tk_help_browser.py`
- `src/ui/markdown_renderer.py`

**Details:**
In _format_table_row() method (line 677):
# Note: This implementation may be duplicated in src/ui/markdown_renderer.py.
# If both implementations exist and changes are needed to table formatting logic,
# consider extracting to a shared utility module to maintain consistency.

The comment suggests potential duplication with src/ui/markdown_renderer.py, but markdown_renderer.py is not provided in the source files. If duplication exists, changes to table formatting in one location may not be reflected in the other.

---



#### Code vs Comment conflict

**Description:** Comment about link tag prefixes may be incomplete or misleading

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
In _create_context_menu() method (line 598):
# Note: Both "link_" (from _render_line_with_links) and "result_link_"
# (from _execute_search) prefixes are checked. Both types are stored
# identically in self.link_urls, but the prefixes distinguish their origin.

However, in _render_line_with_links() (line 211), links are tagged with "link_{counter}" format, and in _execute_search() (line 437), search result links are tagged with "result_link_{counter}" format. The comment correctly identifies both prefixes, but the actual code in _render_line_with_links() creates tags like "link_1", "link_2", etc., while _execute_search() creates "result_link_1", "result_link_2", etc. The comment is accurate but could be clearer about the counter suffix pattern.

---



#### Code vs Comment conflict

**Description:** Comment about widget storage contradicts actual implementation

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
In _get_current_widget_values() method (line 192):
# All entries in self.widgets dict are tk.Variable instances (BooleanVar, StringVar, IntVar),
# not the actual widget objects (Checkbutton, Spinbox, Entry, Combobox).
# The variables are associated with widgets via textvariable/variable parameters.

This comment is accurate and matches the implementation in _create_setting_widget() (lines 145-169) where tk.Variable instances are stored in self.widgets, not the widget objects themselves. However, the comment could be misleading because the method name suggests it gets values from widgets, when it actually gets values from variables. This is not a conflict but could cause confusion.

---



#### Code vs Comment conflict

**Description:** Comment about inline help label describes it as 'not a hover tooltip' but implementation is just a label

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
In _create_setting_widget() method (line 176):
# Show short help as inline label (not a hover tooltip, just a gray label)

The comment clarifies that the help text is displayed as a static label, not a tooltip. However, the parenthetical clarification '(not a hover tooltip, just a gray label)' seems defensive, suggesting there might have been confusion or a previous implementation using tooltips. The code matches the comment, but the comment's phrasing suggests potential past inconsistency.

---



#### Code vs Comment conflict

**Description:** Comment about modal dialog behavior may be misleading about blocking

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
In __init__() method (line 44):
# Make modal (prevents interaction with parent, but doesn't block code execution - no wait_window())

The comment clarifies that grab_set() makes the dialog modal (preventing interaction with parent) but doesn't block code execution because wait_window() is not called. This is accurate, but the phrasing 'doesn't block code execution' could be misunderstood - it means the calling code continues executing, not that the dialog itself is non-blocking. The comment is technically correct but could be clearer.

---



#### Code vs Comment conflict

**Description:** Comment about menu dismissal handling may be incomplete

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
In _create_context_menu() method (line 617):
# Note: tk_popup() handles menu dismissal automatically (ESC key,
# clicks outside menu, selecting items). Explicit bindings for
# FocusOut/Escape are not needed and may not fire reliably since
# Menu widgets have their own event handling for dismissal.

Followed by (line 623):
# Release grab after menu is shown. Note: tk_popup handles menu interaction,
# but we explicitly release the grab to ensure clean state.

The first comment states that explicit dismissal handling is not needed, but the second comment shows grab_release() is called explicitly. While grab_release() is not the same as dismissal event binding, the two comments together could be confusing about what is automatic vs. manual.

---



#### code_vs_comment

**Description:** Docstring describes 3-pane layout with specific weights (3:2:1) but implementation uses ttk.PanedWindow which doesn't use those exact weight values

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring lines ~48-52:
'- 3-pane vertical layout (weights: 3:2:1 = total 6 units):
  * Editor with line numbers (top, ~50% = 3/6 - weight=3)
  * Output pane (middle, ~33% = 2/6 - weight=2)
    - Contains INPUT row (shown/hidden dynamically for INPUT statements)
  * Immediate mode input line (bottom, ~17% = 1/6 - weight=1)'

Implementation lines ~177-195:
paned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
paned.add(editor_frame, weight=3)
paned.add(output_frame, weight=2)
paned.add(immediate_frame, weight=1)

The weights are correct, but the description is overly specific about percentages which may not match actual rendering.

---



#### code_vs_comment

**Description:** Comment states Ctrl+I is bound to editor text widget to prevent tab interference, but the actual binding location is not shown in truncated code

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~207 comment: 'Bind Ctrl+I for smart insert line (must be on text widget to prevent tab)'
Line ~208 code: 'self.editor_text.text.bind('<Control-i>', self._on_ctrl_i)'

But later in _create_menu() line ~449:
'# Note: Ctrl+I is bound directly to editor text widget in start() (not root window)'
'# to prevent tab key interference - see editor_text.text.bind('<Control-i>', ...)'

The comment is consistent but the explanation about 'prevent tab key interference' is unclear - Ctrl+I and Tab are different keys.

---



#### documentation_inconsistency

**Description:** Docstring example shows TkIOHandler created without backend reference, but actual initialization pattern may differ

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines ~56-63 docstring:
'Usage:
    from src.ui.tk_ui import TkBackend, TkIOHandler
    from src.editing.manager import ProgramManager

    io = TkIOHandler()  # TkIOHandler created without backend reference initially
    def_type_map = {}  # Type suffix defaults for variables (DEFINT, DEFSNG, etc.)
    program = ProgramManager(def_type_map)
    backend = TkBackend(io, program)'

The comment says 'TkIOHandler created without backend reference initially' but the actual TkIOHandler class definition is not shown in the provided code to verify if this is the correct initialization pattern.

---



#### code_vs_comment

**Description:** Comment describes ARROW_CLICK_WIDTH as 'typical arrow icon width for standard Tkinter theme' but 20 pixels may not match all themes

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~1127-1128:
ARROW_CLICK_WIDTH = 20  # Width of clickable arrow area in pixels (typical arrow icon width for standard Tkinter theme)

This hardcoded value may not work correctly across different Tkinter themes or DPI settings. The comment acknowledges it's for 'standard' theme but doesn't mention potential issues with other themes.

---



#### code_vs_comment

**Description:** Comment about validation timing is incomplete regarding when validation occurs

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _validate_editor_syntax method around line 1230:
Comment says: '# Note: This method is called:\n# - With 100ms delay after cursor movement/clicks (to avoid excessive validation during rapid editing)\n# - Immediately when focus leaves editor (to ensure validation before switching windows)'

However, looking at the code, validation is also called:
- In _on_enter_key after Enter is pressed (line ~1380: 'self.root.after(100, self._validate_editor_syntax)')
- After mouse clicks (line ~1360: 'self.root.after(100, self._validate_editor_syntax)')

The comment should mention all trigger points or be more general.

---



#### code_vs_comment

**Description:** Comment about when _remove_blank_lines is called is incomplete

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _remove_blank_lines method around line 1310:
Comment says: 'Currently called only from _on_enter_key (after each Enter key press), not\nafter pasting or other modifications.'

This comment describes current behavior but doesn't explain WHY it's only called from _on_enter_key. Is this intentional design (blank lines should only be removed on Enter) or a limitation (should be called after paste but isn't yet)? The comment leaves this ambiguous.

---



#### code_vs_comment

**Description:** Comment about clearing yellow highlight doesn't explain restoration timing

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_mouse_click method around line 1355:
Comment says: '# Clear yellow statement highlight when clicking (allows text selection to be visible).\n# The highlight is restored when execution resumes or when stepping to the next statement.'

The comment mentions restoration happens 'when execution resumes or when stepping', but doesn't clarify what happens if the user clicks while paused and then continues without stepping. Does the highlight get restored? The restoration logic isn't visible in this method, making the comment incomplete.

---



#### code_vs_comment

**Description:** Comment describes backspace/delete as control characters but code treats them specially

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1068 states: "Note: These are control characters (ASCII 8 and 127) but we need them for text editing. Other control characters are blocked by validation later."

This is accurate but potentially confusing because the code explicitly allows these before the control character validation, making them exceptions rather than control characters that pass validation.

---



#### code_vs_comment

**Description:** Comment about cursor movement triggering sort has outdated explanation

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1260 states: "Don't trigger sort when:
- old_line_num is None: First time tracking this line (cursor just moved here, no editing yet)
- This prevents unnecessary re-sorting when user clicks around without making changes"

The code correctly implements this, but the comment could be clearer that old_line_num being None means we haven't tracked any previous line yet (first call to _check_line_change), not just "first time tracking this line".

---



#### code_vs_comment

**Description:** Comment about ERL comparison handling is incomplete

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~1790 states: "According to MBASIC manual: if ERL appears on the left side of =, the number on the right side is treated as a line number reference.

Also handles: ERL <> line, ERL < line, ERL > line, etc."

The implementation only checks for BinaryOpNode and doesn't verify the operator type. This means it will renumber the right side for ANY binary operation with ERL on the left (including +, -, *, /, etc.), not just comparisons. This may be intentional but the comment suggests only comparison operators are handled.

---



#### code_vs_comment

**Description:** Comment about CLS behavior may not match user expectations

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In TkIOHandler.clear_screen() method:
"Design decision: GUI output is persistent for review. Users can manually clear output via Run > Clear Output menu if desired. CLS command is ignored to preserve output history during program execution."

This is a no-op implementation that ignores CLS commands. While documented as intentional, this deviates from standard BASIC behavior where CLS clears the screen. Users expecting standard BASIC behavior will be confused.

---



#### code_vs_comment

**Description:** Comment about has_work() usage location may be outdated

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_immediate() method:
"Use has_work() to check if the interpreter is ready to execute (e.g., after RUN command). This is the only location in tk_ui.py that calls has_work()."

This comment claims it's the ONLY location calling has_work(), but without seeing the full file, this assertion cannot be verified and may become outdated as code evolves.

---



#### code_vs_comment_conflict

**Description:** The _parse_line_number() docstring and inline comments provide extensive explanation of valid/invalid line number formats, but the class docstring's 'Automatic blank line removal' section doesn't mention that blank lines with valid BASIC line numbers (e.g., '10' alone) are NOT removed, only completely blank lines.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
_parse_line_number() comment: 'Valid examples:
  "10 PRINT" - line number 10 followed by whitespace, then statement
  "10" - standalone line number (no statement, just the line number)'

_on_cursor_move() code: 'if line_text.strip() == '': # Delete the blank line'

A line containing only '10' would have line_text.strip() == '10', not '', so it would NOT be deleted. However, the class docstring says 'When cursor moves away from a blank line, that line is automatically deleted' without clarifying that lines with only a BASIC line number are preserved.

---



#### code_vs_comment_conflict

**Description:** The _on_cursor_move() method has a comment explaining why after_idle() is used: 'Schedule deletion after current event processing to avoid interfering with ongoing key/mouse event handling (prevents cursor position issues, undo stack corruption, and widget state conflicts during event processing)', but this detailed explanation is not mentioned in the method's docstring or the class docstring's 'Automatic blank line removal' section.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Inline comment: '# Schedule deletion after current event processing to avoid interfering with ongoing key/mouse event handling (prevents cursor position issues, undo stack corruption, and widget state conflicts during event processing)'

Class docstring only says: 'When cursor moves away from a blank line, that line is automatically deleted'

The technical reason for using after_idle() is important for maintainers but not documented in the docstring.

---



#### code_vs_comment_conflict

**Description:** The _parse_line_number() inline comment references 'MBASIC 5.21' as requiring whitespace or end-of-line between line number and statement, but no other part of the file mentions this version number or specification, making it unclear if this is the actual target version for the entire project.

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
_parse_line_number() comment: 'Note: MBASIC 5.21 requires whitespace OR end-of-line between line number and statement.'

This is the only reference to 'MBASIC 5.21' in the entire file. The module docstring says 'Custom Tkinter widgets for MBASIC Tk UI' but doesn't specify which version of MBASIC is being targeted.

---



#### documentation_inconsistency

**Description:** Multiple references to MBASIC version '5.21' as language version vs implementation version

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
The code has multiple comments clarifying version numbers:
- Line ~438: # Note: '5.21' is the MBASIC language version (intentionally hardcoded)
- Line ~896: # Use CodeMirror 5 (legacy) - simple script tags, no ES6 modules
- Line ~920: ui.page_title('MBASIC 5.21 - Web IDE')
- Line ~1000: self.output_text = f'MBASIC 5.21 Web IDE - {VERSION}\n'

This is actually consistent, but the repeated clarifications suggest past confusion. The pattern is correct: '5.21' is the BASIC language version, VERSION is the implementation version.

---



#### code_vs_comment

**Description:** Comment about sort state matching Tk UI defaults references external file

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~159-160:
# Sort state (matches Tk UI defaults: see sort_mode and sort_reverse in src/ui/tk_ui.py)
self.sort_mode = 'accessed'  # Current sort mode
self.sort_reverse = True  # Sort direction

This references src/ui/tk_ui.py which is not provided. Cannot verify if the defaults actually match.

---



#### code_vs_comment

**Description:** Comment describes double mechanism for input handling but doesn't explain why both are needed or when each is used

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _handle_output_enter() method:

Comment says: "Provide input to interpreter via TWO mechanisms (we check both in case either is active):
1. interpreter.provide_input() - Used when interpreter is waiting synchronously
2. input_future.set_result() - Used when async code is waiting via asyncio.Future

Only one path will be active at a time, but we check both to handle whichever path the interpreter is currently using."

This is confusing - if only one path is active at a time, why check both? The comment should explain the architectural reason for having two mechanisms rather than just stating they exist.

---



#### code_vs_comment

**Description:** Comment about sys.stderr.write in _sync_program_from_editor is redundant

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _sync_program_from_editor() method:

Comment says: "Using sys.stderr.write directly to ensure output even if logging fails."

But the code already shows sys.stderr.write() is being used, and the reason is obvious from context (error handling during serialization). The comment adds no value and could be removed.

---



#### documentation_inconsistency

**Description:** Placeholder keyboard shortcut syntax in debugging documentation

**Affected files:**
- `docs/help/common/debugging.md`

**Details:**
The debugging.md file uses placeholder syntax like {{kbd:step:curses}} and {{kbd:continue:curses}} throughout, which suggests these are template variables that should be replaced with actual keyboard shortcuts. Examples:

'Shortcuts: Tk/Curses/Web: **{{kbd:step:curses}}** or Step button'
'Press **{{kbd:continue:curses}}** or click **Continue**'
'Press **{{kbd:quit:curses}}** or click **Stop**'
'**Tk UI:** Debug → Execution Stack or **{{kbd:toggle_stack:tk}}**'

These placeholders appear to be unresolved template variables rather than actual documentation.

---



#### code_documentation_mismatch

**Description:** Keybindings JSON exists but debugging docs use placeholder syntax instead of referencing actual bindings

**Affected files:**
- `src/ui/web_keybindings.json`
- `docs/help/common/debugging.md`

**Details:**
web_keybindings.json defines actual keybindings:
{
  "editor": {
    "run": {"keys": ["Ctrl+R", "F5"], "primary": "Ctrl+R/F5"},
    "stop": {"keys": ["Esc"], "primary": "Esc"},
    "step": {"keys": ["F10"], "primary": "F10"},
    "continue": {"keys": ["F5"], "primary": "F5"},
    "toggle_breakpoint": {"keys": ["F9"], "primary": "F9"}
  }
}

But debugging.md uses {{kbd:step:curses}} placeholders instead of documenting the actual F10, F5, F9 keys from the JSON config.

---



#### code_comment_conflict

**Description:** Comment describes class as deprecated but it's still fully implemented with detailed functionality

**Affected files:**
- `src/ui/web_help_launcher.py`

**Details:**
Comment says:
'# Legacy class kept for compatibility - new code should use direct web URL instead'
'# The help site is already built and served at http://localhost/mbasic_docs'
'# Migration guide for code using this class:'

But the WebHelpLauncher_DEPRECATED class has 150+ lines of implementation including:
- Server process management
- MkDocs building
- Port checking
- Fallback viewer logic

If truly deprecated for removal, it should be a simple wrapper. If still needed for functionality, the comment is misleading.

---



#### documentation_inconsistency

**Description:** Compiler documentation exists but implementation status unclear

**Affected files:**
- `docs/help/common/compiler/index.md`
- `docs/help/common/compiler/optimizations.md`

**Details:**
index.md states: 'Documentation for the code generation phase will be added as the compiler backend is developed.'

optimizations.md states: '**27 optimizations analyzed** in the semantic analysis phase... The actual code transformations will be applied during code generation (currently in development).'

And later: '**Status:** In Progress

Additional optimizations will be added during code generation'

This suggests the compiler is partially implemented (semantic analysis done, code generation in progress), but there's no corresponding code files in the provided source to verify this status.

---



#### documentation_inconsistency

**Description:** Documentation mentions BASIC version limitation but doesn't specify which version MBASIC implements

**Affected files:**
- `docs/help/common/examples/loops.md`

**Details:**
loops.md states: '**Note:** MBASIC 5.21 does not have EXIT FOR or EXIT WHILE statements (those were added in later BASIC versions). GOTO is the standard way to exit loops early in BASIC-80.'

This correctly identifies MBASIC 5.21 as the target version. However, src/version.py shows:
MBASIC_VERSION = "5.21"  # The MBASIC version we implement
COMPATIBILITY = "100% MBASIC 5.21 compatible with optional extensions"

The documentation is consistent with the code, but the phrase 'optional extensions' in version.py could create confusion about whether EXIT FOR/EXIT WHILE might be available as extensions.

---



#### code_documentation_mismatch

**Description:** SessionState has auto_save fields but WebSettingsDialog doesn't expose them in UI

**Affected files:**
- `src/ui/web/session_state.py`
- `src/ui/web/web_settings_dialog.py`

**Details:**
session_state.py defines:
auto_save_enabled: bool = True
auto_save_interval: int = 30

But web_settings_dialog.py only creates UI for:
- editor.auto_number (checkbox)
- editor.auto_number_step (number input)
- limits.* (read-only display)

The auto_save settings in SessionState are never exposed in the settings dialog UI, suggesting either:
1. They should be added to the settings dialog
2. They're legacy fields that should be removed from SessionState
3. They're managed elsewhere and the naming is coincidental

---



#### documentation_inconsistency

**Description:** README mentions four UI backends but help structure may not match all of them

**Affected files:**
- `docs/help/README.md`

**Details:**
README.md states: 'MBASIC supports four UI backends: CLI (command-line interface), Curses (terminal full-screen), Tk (desktop GUI), and Web (browser-based).'

Help directories exist for:
- /ui/cli
- /ui/curses
- /ui/tk
- /ui/web

This appears consistent, but the README also states 'the CLI and Curses UIs use built-in markdown rendering' while 'Tk and Web UIs' use the MkDocs server. However, web_help_launcher.py's open_help_in_browser() function has a ui_type parameter that defaults to 'tk', suggesting all UIs might use the web-based help system.

---



#### documentation_inconsistency

**Description:** Inconsistent statement about line number range

**Affected files:**
- `docs/help/common/getting-started.md`
- `docs/help/common/language.md`

**Details:**
getting-started.md states 'Numbers can be 1-65535' but language.md does not specify the valid range for line numbers. This should be consistent across both documents.

---



#### documentation_inconsistency

**Description:** Circular reference in FIX documentation

**Affected files:**
- `docs/help/common/language/functions/fix.md`
- `docs/help/common/language/functions/int.md`

**Details:**
fix.md states 'FIX(X) is equivalent to SGN(X)*INT(ABS(X))' and says 'The major difference between FIX and INT is that FIX does not return the next lower number for negative X.' However, int.md is referenced in the 'See Also' section but the actual int.md file content is not provided in the documentation set, making it impossible to verify the consistency of this explanation.

---



#### documentation_inconsistency

**Description:** Inconsistent ASCII code references

**Affected files:**
- `docs/help/common/language/character-set.md`
- `docs/help/common/language/appendices/ascii-codes.md`

**Details:**
character-set.md has a table of control characters with codes (7=BEL, 8=BS, 9=TAB, 10=LF, 13=CR, 27=ESC) and says 'See [ASCII Codes](appendices/ascii-codes.md) for a complete reference.' The ascii-codes.md file exists and provides the complete table, but character-set.md could be clearer that it's showing a subset.

---



#### documentation_inconsistency

**Description:** Missing error code reference in EOF documentation

**Affected files:**
- `docs/help/common/language/functions/eof.md`
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
eof.md mentions 'to avoid "Input past end" errors' but doesn't reference the error code. According to error-codes.md, this is error 62 'Input past end'. The documentation should include the error code reference for consistency.

---



#### documentation_inconsistency

**Description:** Inconsistent overflow error behavior description

**Affected files:**
- `docs/help/common/language/functions/exp.md`
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
exp.md states 'If EXP overflows, the "Overflow" error message is displayed, machine infinity with the appropriate sign is supplied as the result, and execution continues.' However, error-codes.md for error 6 (OV) states 'The result of a calculation is too large to be represented in BASIC-80's number format' without mentioning that execution continues with infinity. This behavior difference should be clarified.

---



#### documentation_inconsistency

**Description:** Inconsistent 'See Also' sections for system functions

**Affected files:**
- `docs/help/common/language/functions/fre.md`
- `docs/help/common/language/functions/inkey_dollar.md`
- `docs/help/common/language/functions/inp.md`
- `docs/help/common/language/functions/peek.md`

**Details:**
All four system function docs (FRE, INKEY$, INP, PEEK) have identical 'See Also' sections listing the same 12 items. However, this creates circular references where each function references the others in the same category. For example, FRE's 'See Also' includes INKEY$, INP, and PEEK, and vice versa. This is redundant and doesn't provide useful cross-referencing to related but different functionality.

---



#### documentation_inconsistency

**Description:** Inconsistent 'See Also' sections between HEX$ and OCT$

**Affected files:**
- `docs/help/common/language/functions/hex_dollar.md`
- `docs/help/common/language/functions/oct_dollar.md`

**Details:**
HEX$ and OCT$ are parallel functions (convert decimal to hex/octal strings), but their 'See Also' sections are identical and include each other. However, neither references STR$ which is the decimal equivalent, while both reference less related functions like INSTR, LEFT$, RIGHT$, etc. The cross-references should be more focused on related conversion functions.

---



#### documentation_inconsistency

**Description:** Inconsistent handling of boundary conditions in string extraction functions

**Affected files:**
- `docs/help/common/language/functions/left_dollar.md`
- `docs/help/common/language/functions/right_dollar.md`
- `docs/help/common/language/functions/mid_dollar.md`

**Details:**
LEFT$ doc: 'If I is greater than LEN(X$), the entire string (X$) will be returned. If I=0, the null string (length zero) is returned.'

RIGHT$ doc: 'If I=LEN(X$), returns X$. If I=0, the null string (length zero) is returned.'

MID$ doc: 'If J is omitted or if there are fewer than J characters to the right of the Ith character, all rightmost characters beginning with the Ith character are returned. If I>LEN(X$), MID$ returns a null string.'

LEFT$ and RIGHT$ document I=0 behavior, but MID$ does not. MID$ documents I>LEN(X$) behavior, but LEFT$ and RIGHT$ don't explicitly state what happens when I>LEN(X$) (though LEFT$ implies it returns the whole string). The boundary condition documentation should be consistent across all three functions.

---



#### documentation_inconsistency

**Description:** SIN documentation includes note about COS relationship but COS doesn't reciprocate

**Affected files:**
- `docs/help/common/language/functions/sin.md`
- `docs/help/common/language/functions/index.md`

**Details:**
sin.md includes: 'Note: COS(X) = SIN(X + 3.14159/2)'

However, cos.md does not include a reciprocal note about SIN. If mathematical relationships are documented, they should be bidirectional for completeness.

---



#### documentation_inconsistency

**Description:** DEF FN shows detailed examples and modern implementation notes, while DEF USR only shows 'Not Implemented' without similar detail level

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`
- `docs/help/common/language/statements/def-usr.md`

**Details:**
def-fn.md has 8 detailed examples with explanations, syntax notes about spacing, and compatibility information.

def-usr.md only has:
"⚠️ **Not Implemented**: This feature defines the starting address of assembly language subroutines and is not implemented in this Python-based interpreter."

The documentation style and depth are inconsistent between related DEF statements.

---



#### documentation_inconsistency

**Description:** EDIT documentation mentions 'Tk, Curses, or Web UI' but these UI types are not explained or documented elsewhere in the provided files

**Affected files:**
- `docs/help/common/language/statements/edit.md`

**Details:**
edit.md states:
"**Modern MBASIC Implementation:** This implementation provides full-screen editing capabilities through the integrated editor (Tk, Curses, or Web UI)."

No other documentation file in the set explains what these UI options are, how to select them, or their differences. This creates an incomplete reference.

---



#### documentation_inconsistency

**Description:** FILES documentation mentions CP/M behavior but doesn't clarify if this applies to the current implementation

**Affected files:**
- `docs/help/common/language/statements/files.md`

**Details:**
files.md states:
"**Note**: CP/M automatically adds .BAS extension if none is specified for BASIC program files."

The documentation doesn't clarify whether this CP/M-specific behavior is emulated in the modern Python implementation or if it's just historical reference. Other statements like DEF USR clearly mark unimplemented features.

---



#### documentation_inconsistency

**Description:** HELPSETTING is listed in index.md under 'Modern Extensions' but SETSETTING is referenced as 'SET' in the See Also section

**Affected files:**
- `docs/help/common/language/statements/helpsetting.md`
- `docs/help/common/language/statements/index.md`

**Details:**
helpsetting.md See Also section references:
"- [SETSETTING](setsetting.md) - Configure interpreter settings"

But index.md lists it as:
"- [SET](setsetting.md) - Configure interpreter settings"

The actual command name should be consistent. Based on the filename 'setsetting.md', the command is likely SETSETTING, not SET.

---



#### documentation_inconsistency

**Description:** INPUT# documentation title has inconsistent formatting with parenthetical '(File)' not used in other file I/O statements

**Affected files:**
- `docs/help/common/language/statements/input_hash.md`

**Details:**
input_hash.md has title: 'INPUT# (File)'

Other file I/O statements don't use this pattern:
- get.md: 'GET'
- field.md: 'FIELD'
- open.md: 'OPEN'

The '(File)' suffix appears to distinguish from INPUT statement, but this naming convention is not consistently applied to other statements that have both file and non-file versions (like PRINT vs PRINT#).

---



#### documentation_inconsistency

**Description:** DEFINT/SNG/DBL/STR example shows DATA# with # suffix but doesn't explain that type suffix overrides DEF declaration

**Affected files:**
- `docs/help/common/language/statements/defint-sng-dbl-str.md`

**Details:**
defint-sng-dbl-str.md example shows:
"40 DATA# = 12.5     ' Double precision (starts with D, has # suffix)"

The comment says 'has # suffix' but the explanation section states:
"**Type Declaration Precedence:**
- **Type suffix always wins:** `NAME1$` is string even though N→Z are declared integer"

The example comment for DATA# should clarify that the # suffix is what makes it double precision, not the DEFDBL D-E declaration. The current comment 'starts with D, has # suffix' could be misread as both contributing to the type.

---



#### documentation_inconsistency

**Description:** Confusing note about PRINT# with random files

**Affected files:**
- `docs/help/common/language/statements/put.md`

**Details:**
Note states: 'PRINT#, PRINT# USING, and WRITE# may be used to put characters in the random file buffer before a PUT statement.'
This is an advanced technique that seems inconsistent with the FIELD/LSET/RSET approach documented elsewhere. The relationship between these approaches needs clarification.

---



#### documentation_inconsistency

**Description:** Maximum line number inconsistency

**Affected files:**
- `docs/help/common/language/statements/renum.md`

**Details:**
Documentation states: 'Cannot create line numbers > 65529'
This specific limit (65529 vs 65535) should be verified as consistent across all line number operations (AUTO, GOTO, etc.) and documented why this specific limit exists.

---



#### documentation_inconsistency

**Description:** WRITE and WRITE# have inconsistent title formatting

**Affected files:**
- `docs/help/common/language/statements/write.md`
- `docs/help/common/language/statements/writei.md`

**Details:**
write.md has title: 'WRITE (Screen)'
writei.md has title: 'WRITE# (File)'

The hash symbol placement is inconsistent - one uses space before parenthetical, the other includes # in the command name. Should be consistent, likely 'WRITE (Screen)' and 'WRITE# (File)' or 'WRITE' and 'WRITE #'.

---



#### documentation_inconsistency

**Description:** Inconsistent 'Versions' field presence across documentation files

**Affected files:**
- `docs/help/common/language/statements/swap.md`
- `docs/help/common/language/statements/tron-troff.md`
- `docs/help/common/language/statements/wait.md`
- `docs/help/common/language/statements/while-wend.md`
- `docs/help/common/language/statements/width.md`
- `docs/help/common/language/statements/write.md`

**Details:**
Some files have 'Versions: Disk' or 'Versions: Extended, Disk' or 'Versions: MBASIC Extension' in the frontmatter, while others (SWAP, TRON-TROFF, WAIT, WHILE-WEND, WRITE) have it in the body under 'Syntax' or 'Purpose' sections.

For consistency, all files should have version information in the same location, preferably in the YAML frontmatter.

---



#### documentation_inconsistency

**Description:** Incomplete feature availability matrix

**Affected files:**
- `docs/help/common/ui/tk/index.md`
- `docs/help/mbasic/extensions.md`

**Details:**
Tk docs mention 'Some Tk configurations include an immediate mode panel' but Extensions guide doesn't mention this variability. Extensions guide states 'Find and Replace (Tk only)' but Tk docs only mention 'Find' in the menu ({{kbd:find:tk}}), not Replace. This suggests either the feature matrix is incomplete or the Tk docs are missing Replace documentation.

---



#### documentation_inconsistency

**Description:** Inconsistent DELETE command syntax

**Affected files:**
- `docs/help/common/ui/curses/editing.md`

**Details:**
Curses editing doc shows 'DELETE 20' and 'DELETE 10-30' as examples but doesn't specify if DELETE is a direct mode command or a program statement. The doc context suggests it's a direct command (like in the CLI), but this should be clarified since the Curses UI is primarily a full-screen editor, not a command-line interface.

---



#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation format

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
features.md uses template notation like '{{kbd:run:curses}}' for keyboard shortcuts:
- 'Press **{{kbd:run:curses}}** to run.'
- '**{{kbd:save:curses}}** - Save program'

But getting-started.md also uses the same notation:
- 'Press **{{kbd:run:curses}}** to run.'

This suggests these are template placeholders that should be replaced with actual key combinations (like 'F5' or 'Ctrl+R'). The documentation should either:
1. Replace all {{kbd:...}} with actual keys
2. Explain the template system
3. Provide a key reference table

---



#### documentation_inconsistency

**Description:** Inconsistent UI count - three vs four interfaces

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/index.md`

**Details:**
features.md section 'Choosing a User Interface' states:
'MBASIC supports four interfaces:'
And lists: Curses UI, CLI Mode, Tkinter GUI, Web UI

However, index.md states:
'- Choice of user interfaces (CLI, Curses, Tkinter)'
Only listing three interfaces, omitting Web UI.

The documentation should consistently list all four UIs or explain why Web UI is sometimes excluded.

---



#### documentation_inconsistency

**Description:** Inconsistent statement count

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/index.md`

**Details:**
cli/index.md states:
'- [Statements](../../common/language/statements/index.md) - All 63 statements'

However, features.md does not provide a specific count of statements. If there are exactly 63 statements, this should be consistently documented across all references to the statement list.

---



#### documentation_inconsistency

**Description:** Inconsistent optimization count

**Affected files:**
- `docs/help/mbasic/features.md`

**Details:**
features.md states:
'The interpreter includes an advanced semantic analyzer with 18 optimizations:'

Then lists exactly 18 numbered optimizations (1-18). However, it's unclear if this list is exhaustive or if there are additional unlisted optimizations. The phrasing 'includes' suggests there might be more, but the numbered list suggests completeness.

---



#### documentation_inconsistency

**Description:** Incomplete settings list in Quick Reference table

**Affected files:**
- `docs/help/ui/cli/settings.md`

**Details:**
settings.md provides a 'Quick Reference' table listing settings by category:
- editor: auto_number, auto_number_step, tab_size, show_line_numbers
- keywords: case_style
- variables: case_conflict, show_types_in_window
- interpreter: strict_mode, max_execution_time, debug_mode
- ui: theme, font_size

However, earlier in the same document, SHOWSETTINGS example output shows these exact settings, suggesting the list is complete. But the document also states 'For a complete list of available settings, see [Settings System Overview](../../common/settings.md)' - implying there might be more settings not shown in the quick reference.

---



#### documentation_inconsistency

**Description:** Inconsistent information about Cut/Copy/Paste availability

**Affected files:**
- `docs/help/ui/curses/editing.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
docs/help/ui/curses/editing.md states: '**Note:** Cut/Copy/Paste operations are not available in the Curses UI due to keyboard shortcut conflicts. Use your terminal's native clipboard functions instead (typically Shift+Ctrl+C/V or mouse selection).'

But docs/help/ui/curses/feature-reference.md provides more detailed explanation:
'### Cut/Copy/Paste (Not implemented)
Standard clipboard operations are not available in the Curses UI due to keyboard shortcut conflicts:
- **{{kbd:stop:curses}}** - Used for Stop/Interrupt (cannot be used for Cut)
- **{{kbd:continue:curses}}** - Terminal signal to exit program (cannot be used for Copy)
- **{{kbd:save:curses}}** - Used for Save File (cannot be used for Paste; {{kbd:save:curses}} is reserved by terminal for flow control)'

The feature-reference provides more context about WHY these shortcuts conflict, which should be consistent across both documents.

---



#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut for Settings

**Affected files:**
- `docs/help/ui/curses/quick-reference.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
docs/help/ui/curses/quick-reference.md under 'Global Commands' states: '**Menu only** | Settings'

But docs/help/ui/curses/settings.md states: '**Keyboard shortcut:** `Ctrl+,`'

This is contradictory - either Settings has a keyboard shortcut (Ctrl+,) or it's menu-only.

---



#### documentation_inconsistency

**Description:** Placeholder documentation with incomplete information

**Affected files:**
- `docs/help/ui/common/running.md`

**Details:**
docs/help/ui/common/running.md is marked as 'PLACEHOLDER - Documentation in progress' and only provides minimal information:
'For now, see:
- Type `RUN` to execute the current program
- Use the Run button in GUI interfaces
- Press Ctrl+C or use STOP button to interrupt
- Type `CONT` to continue after STOP'

This is incomplete and may not match the actual implementation details described in UI-specific docs like docs/help/ui/curses/running.md which provides much more detail.

---



#### documentation_inconsistency

**Description:** Inconsistent information about Find/Replace availability

**Affected files:**
- `docs/help/ui/curses/find-replace.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
docs/help/ui/curses/find-replace.md states: 'The Curses UI currently **does not have** Find/Replace functionality for the editor. This feature is planned for future implementation.'

But docs/help/ui/curses/feature-reference.md states:
'### Find/Replace (Not yet implemented)
Find and Replace functionality is not yet available in Curses UI via keyboard shortcuts.'

Both agree it's not implemented, but find-replace.md says it's 'planned for future implementation' while feature-reference.md says 'not yet available...via keyboard shortcuts' which could imply it might be available via other means. The wording should be consistent.

---



#### documentation_inconsistency

**Description:** Inconsistent sort mode descriptions within same document

**Affected files:**
- `docs/help/ui/curses/variables.md`

**Details:**
In docs/help/ui/curses/variables.md, under 'Sorting Options' section:
'Press `s` to cycle through sort orders:
- **Accessed**: Most recently accessed (read or written) - shown first
- **Written**: Most recently written to - shown first
- **Read**: Most recently read from - shown first
- **Name**: Alphabetical by variable name'

But later in the same document under 'Variables Window (when visible)' section:
'**Sort Modes:**
- **Accessed**: Most recently accessed (read or written) - default, newest first
- **Written**: Most recently written to - newest first
- **Read**: Most recently read from - newest first
- **Name**: Alphabetically by variable name - A to Z'

The second description adds 'default' for Accessed mode and 'A to Z' for Name mode, which should be consistent throughout the document.

---



#### documentation_inconsistency

**Description:** Search Help feature description inconsistency

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
The Search Help feature states:
"### Search Help
Search across all help documentation:
- Full-text search
- Keyword search
- Results with context
- Jump to relevant section

**Note:** Search function is available via the help browser's search box (no dedicated keyboard shortcut)."

This is the only Help System feature with a note about keyboard shortcuts. The note seems defensive, as if responding to an expectation that wasn't set. Other features without keyboard shortcuts don't include such notes, making this inconsistent with the documentation style.

---



#### documentation_inconsistency

**Description:** Inconsistent capitalization of 'Tk' vs 'TK' in title

**Affected files:**
- `docs/help/ui/tk/features.md`

**Details:**
The file is titled "Essential TK GUI Features" (all caps TK) but throughout the documentation and in other files, it's consistently referred to as "Tk" (capital T, lowercase k) or "Tkinter". The title should likely be "Essential Tk GUI Features" for consistency.

---



#### documentation_inconsistency

**Description:** Inconsistent menu structure documentation

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
features.md under 'Debugging Tools' → 'Variable Inspector' → 'Currently Implemented' states:
- 'Basic variable viewing via Debug menu'

But web-interface.md under 'Menu Functions' lists:
- 'View Menu' with 'Show Variables - Open the Variables Window to view and monitor program variables in real-time'

There is no 'Debug menu' mentioned in web-interface.md, only a 'View menu'. This inconsistency in menu naming could confuse users trying to find features.

---



#### documentation_inconsistency

**Description:** Inconsistent menu bar description

**Affected files:**
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
getting-started.md states:
- 'Menu Bar: At the very top, three menus: File, Run, Help'

But web-interface.md states:
- 'Menu Bar: Located at the top with File, Edit, Run, View, and Help menus'

The getting-started.md is missing Edit and View menus from its description.

---



#### documentation_inconsistency

**Description:** Missing 'Open Example' feature mentioned in one doc but not others

**Affected files:**
- `docs/help/ui/web/web-interface.md`
- `docs/help/ui/web/getting-started.md`

**Details:**
web-interface.md under 'File Menu' states:
- 'Note: An "Open Example" feature to choose from sample BASIC programs is planned for a future release.'

However, getting-started.md under 'Tips and Tricks' mentions:
- 'Check errors: Red error messages in output show what went wrong'

But doesn't mention anything about example programs. The index.md also doesn't reference this planned feature. This creates inconsistency about whether example programs are available or planned.

---



#### documentation_inconsistency

**Description:** Library documentation references games but other categories lack metadata

**Affected files:**
- `docs/help/ui/web/index.md`
- `docs/library/business/index.md`
- `docs/library/data_management/index.md`
- `docs/library/demos/index.md`
- `docs/library/education/index.md`
- `docs/library/electronics/index.md`

**Details:**
index.md prominently features:
- '🎮 Games Library'
- 'Browse and download classic BASIC games:'
- '[Games Library](../../../library/games/index.md) - 113 classic CP/M era games to download and load!'

However, the other library category index files (business, data_management, demos, education, electronics) all show programs with empty metadata:
- 'Year: 1980s'
- 'Tags: ' (empty except for some test tags)

This suggests incomplete documentation for non-game library programs, or that the games library has special treatment not documented in the web UI help.

---



#### documentation_inconsistency

**Description:** Library statistics claim 202 programs but actual count may differ

**Affected files:**
- `docs/library/index.md`

**Details:**
The index states:
**Library Statistics:**
- 202 programs from the 1970s-1980s

However, this is a static number that may not reflect the actual count of programs listed across all category pages. No verification mechanism is mentioned.

---



#### documentation_inconsistency

**Description:** Curses UI limitations list includes 'No Find/Replace' but this may be outdated

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
Under Curses UI limitations:
**Limitations:**
- Limited mouse support
- Partial variable editing
- No clipboard integration
- Terminal color limits
- No Find/Replace

However, the Decision Matrix at the bottom shows:
| **Find/Replace** | ❌ | ❌ | ✅ | ❌ |

This confirms Curses lacks Find/Replace, but without seeing the actual code implementation, we cannot verify if this is current or if the feature was added later.

---



#### documentation_inconsistency

**Description:** Inconsistent terminology for line ending types

**Affected files:**
- `docs/user/FILE_FORMAT_COMPATIBILITY.md`

**Details:**
The document uses multiple terms for the same concepts:
- 'Unix-style line endings' and 'LF' and '\n'
- 'Windows' and 'CRLF' and '\r\n'
- 'Classic Mac' and 'CR' and '\r'

While technically correct, the document could be more consistent in using one primary term with alternatives in parentheses throughout.

---



#### documentation_inconsistency

**Description:** Inconsistent program descriptions - some have detailed descriptions, others are minimal or cryptic

**Affected files:**
- `docs/library/utilities/index.md`

**Details:**
Compare these entries:

### Bigcal2
Extended precision calculator with up to 100-digit precision for arithmetic operations
**Author:** Judson D. McClendon, modified by R.J. Sandel
**Year:** 1980s
**Tags:** calculator, math, precision

vs.

### Un-Prot
Fixup for ** UN.COM **
**Year:** 1980s
**Tags:** 

vs.

### Xextract
0 -->END PAGE / 1-20 -->EXTRACT ITEM / 21 -->RESTART
**Year:** 1980s
**Tags:** 

The quality and clarity of descriptions varies dramatically. Some programs have no tags, some have cryptic descriptions that appear to be copied from the program itself.

---



#### documentation_inconsistency

**Description:** Many game entries have empty metadata fields

**Affected files:**
- `docs/library/games/index.md`

**Details:**
Most game entries show:
**Year:** 1980s
**Tags:** 

With no author, source, or specific tags. Only a few entries (like Calendar, Survival) have complete metadata. This inconsistency makes it unclear whether the information is missing or was never available.

---



#### documentation_inconsistency

**Description:** QUICK_REFERENCE.md is labeled as Curses UI specific but uses generic kbd template notation

**Affected files:**
- `docs/user/QUICK_REFERENCE.md`
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
QUICK_REFERENCE.md header states 'MBASIC Curses IDE - Quick Reference Card' and mentions it's 'Curses UI specific', but uses {{kbd:...}} template notation which appears to be a placeholder system. TK_UI_QUICK_START.md uses the same notation for different UI. This suggests either the template system is cross-UI or the documentation is mislabeled.

---



#### documentation_inconsistency

**Description:** Ambiguous kbd template notation without explanation

**Affected files:**
- `docs/user/QUICK_REFERENCE.md`

**Details:**
QUICK_REFERENCE.md extensively uses {{kbd:...}} notation (e.g., {{kbd:new}}, {{kbd:open}}, {{kbd:save}}) but never explains what these placeholders represent or how they map to actual keys. Users reading this document won't know what keys to press. This appears to be a template system that should be processed before user consumption.

---



#### documentation_inconsistency

**Description:** Inconsistent command prompt examples between operating systems

**Affected files:**
- `docs/user/INSTALL.md`

**Details:**
INSTALL.md shows different command styles: Linux/Mac uses 'python3 mbasic' while Windows examples show both 'python mbasic' and 'python3 mbasic' inconsistently. The troubleshooting section mentions 'python3: command not found' and suggests using 'python' instead, but this guidance could be clearer upfront.

---



#### documentation_inconsistency

**Description:** README lists keyboard-shortcuts.md as Curses UI specific but doesn't clarify if Tk UI has different shortcuts

**Affected files:**
- `docs/user/README.md`

**Details:**
docs/user/README.md lists 'keyboard-shortcuts.md - Keyboard shortcuts reference (Curses UI specific)' but doesn't indicate whether there's a separate keyboard shortcuts document for Tk UI, or if Tk UI shortcuts are only documented in TK_UI_QUICK_START.md. This creates ambiguity about where to find complete Tk UI keyboard reference.

---



#### documentation_inconsistency

**Description:** Inconsistent status symbols for Auto-save feature

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
In 'File Operations' table, Auto-save shows:
- Tk: '⚠️' with note 'Tk: planned/optional'
- Web: '✅'
The legend defines ⚠️ as 'Partially implemented' but the note says 'planned', which should be 📋 according to the legend. This creates ambiguity about whether Tk auto-save is partially working or not implemented at all.

---



#### documentation_inconsistency

**Description:** Keyboard shortcuts table uses template variables without explanation

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
The 'Keyboard Shortcuts Comparison' tables use template variables like {{kbd:run:cli}}, {{kbd:save:curses}}, etc. without explaining what these resolve to or providing a reference to where actual key combinations are documented. Users cannot determine actual shortcuts from this table alone.

---


## Summary

- Total issues found: 564
- Code/Comment conflicts: 235
- Other inconsistencies: 329
- Ignored (already reviewed): 126


## Summary

- Total documentation issues: 298
