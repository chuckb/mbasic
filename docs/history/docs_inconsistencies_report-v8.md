# Enhanced Consistency Report (Code + Documentation)

Generated: 2025-11-05 09:56:49
Analyzed: Source code (.py, .json) and Documentation (.md)

## 🔧 Code vs Comment Conflicts


## 📋 General Inconsistencies

### 🔴 High Severity

#### documentation_inconsistency

**Description:** Contradictory documentation about which abstraction handles LOAD/SAVE/MERGE commands

**Affected files:**
- `src/editing/manager.py`
- `src/file_io.py`

**Details:**
src/editing/manager.py docstring states:
"FILE I/O ARCHITECTURE:
This manager uses direct Python file I/O (open/read/write) for loading and saving
.BAS program files. This is intentional and separate from the two filesystem abstractions:

1. FileIO (src/file_io.py) - For interactive commands (FILES, LOAD, SAVE)"

But src/file_io.py docstring states:
"This module handles PROGRAM file operations (FILES, LOAD, SAVE, MERGE, KILL commands)."

The manager.py claims FileIO handles LOAD/SAVE commands, but then implements load_from_file() and save_to_file() methods itself using direct file I/O. This creates confusion about which component is responsible for these operations.

---

#### code_vs_documentation

**Description:** ProgramManager claims to be UI-agnostic but uses direct file I/O that only works for local UIs

**Affected files:**
- `src/editing/manager.py`

**Details:**
manager.py docstring states:
"Manages program lines, ASTs, parsing, and file operations.
Extracted from InteractiveMode to enable reuse across different UIs."

And:
"ProgramManager uses direct file I/O because:
- It's only used by local UIs (CLI, Curses, Tk) where filesystem access is safe
- Web UI uses FileIO abstraction in interactive.py instead"

This contradicts the stated goal of 'reuse across different UIs'. The manager is not actually reusable for Web UI, making it UI-specific rather than UI-agnostic. The documentation should clarify it's specifically for local UIs.

---

#### code_vs_comment

**Description:** cmd_cont docstring says it 'Clears stopped/halted flags' but code only clears stopped and halted, not stop_pc

**Affected files:**
- `src/interactive.py`

**Details:**
Docstring at line ~430 says:
"State management:
- Clears stopped/halted flags in runtime
- Restores PC from stop_pc (saved execution position)"

Code at lines ~440-445 shows:
self.program_runtime.stopped = False
self.program_runtime.halted = False

# Restore execution position from PC
self.program_runtime.pc = self.program_runtime.stop_pc

The docstring says it 'restores PC from stop_pc', which is correct. However, it doesn't mention that stop_pc itself is NOT cleared, which could be important for understanding state management.

---

#### code_vs_comment

**Description:** cmd_chain comment about variable preservation contradicts itself about MERGE behavior

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~715 says:
"# Save variables based on CHAIN options:
# - MERGE: always preserves all variables (it's an overlay)
# - ALL: passes all variables to new program
# - Neither: only pass COMMON variables"

But earlier comment at line ~695 says MERGE is a parameter that controls whether to merge or replace the program. The first comment implies MERGE always preserves variables, but the code shows that MERGE is about program loading, not variable preservation. The variable preservation logic at line ~720 shows:
if all_flag or merge:
    # Save all variables

This means MERGE does preserve all variables, but the comment structure makes it seem like MERGE is a separate concept from the merge parameter, which is confusing.

---

#### code_vs_comment

**Description:** Comment about return_stmt validation in execute_next contradicts execute_return validation

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_return (lines 1088-1093), comment says:
"return_stmt is 0-indexed offset into statements array.
Valid range: 0 to len(statements) where len(statements) is a special sentinel value
meaning 'continue at next line'...
Values > len(statements) indicate the statement was deleted (validation error)."

Validation: `if return_stmt > len(line_statements):`

But in _execute_next_single (lines 1254-1260), comment says:
"return_stmt is 0-indexed offset into statements array. Valid indices are 0 to len(statements)-1.
return_stmt == len(statements) is a special sentinel: FOR was last statement, continue at next line.
return_stmt > len(statements) is invalid (statement was deleted)."

Validation: `if return_stmt > len(line_statements):`

Both use the same validation logic (> len), but the comments describe different semantics. The first says "0 to len(statements)" is valid (inclusive), the second says "0 to len(statements)-1" is valid (exclusive of len). They can't both be correct.

---

#### code_vs_comment

**Description:** OPTION BASE documentation claims 'Duplicate Definition' for any arrays, but condition check may not catch all cases

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~500 says:
"MBASIC 5.21 gives 'Duplicate Definition' if:
1. OPTION BASE has already been executed, OR
2. Any arrays have been created (both explicitly via DIM and implicitly via first use like A(5)=10)
   This applies regardless of the current array base (0 or 1)."

Code checks:
if len(self.runtime._arrays) > 0:
    raise RuntimeError("Duplicate Definition")

However, the comment mentions 'implicitly via first use like A(5)=10' but doesn't clarify if self.runtime._arrays tracks implicit array creation. If implicit arrays are created elsewhere without updating _arrays, this check would miss them.

---

#### code_vs_comment

**Description:** OPEN mode validation comment claims 'Invalid OPEN mode' error but doesn't document valid modes in error message

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~950 says:
"Valid modes: I (input), O (output), A (append), R (random access)
Any other mode raises 'Invalid OPEN mode: {mode}' error (with actual mode shown)"

Code at line ~970 raises:
raise RuntimeError(f"Invalid OPEN mode: {mode}")

The error message shows the invalid mode but doesn't tell the user what valid modes are. This is a usability issue - the error should list valid options.

---

#### code_vs_comment

**Description:** MID$ assignment validation logic contradicts comment about bounds checking

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment says:
"# Validate start position
if start_idx < 0 or start_idx >= len(current_value):
    # Start position is out of bounds - no replacement
    return"

The condition 'start_idx >= len(current_value)' means if start equals the string length, no replacement occurs. However, the comment earlier states:
"- If start is beyond the string length, no replacement occurs"

The word 'beyond' typically means '>' not '>='. In BASIC, MID$(A$, LEN(A$)+1, 1) = "X" should do nothing, but MID$(A$, LEN(A$), 1) = "X" might be expected to work (replacing the last character). The current code treats both as out of bounds. This needs verification against MBASIC 5.21 behavior.

---

#### implementation_inconsistency

**Description:** input_line() implementations don't preserve leading/trailing spaces as documented in base class

**Affected files:**
- `src/iohandler/console.py`
- `src/iohandler/curses_io.py`
- `src/iohandler/web_io.py`

**Details:**
base.py documents input_line as:
"Similar to input() but preserves leading/trailing spaces and
doesn't interpret commas as field separators."

But all implementations just delegate to input() or use the same underlying mechanism:
- console.py: return self.input(prompt)
- curses_io.py: return self.input(prompt)
- web_io.py: return self.input(prompt)

None of these implementations actually preserve spaces or handle commas differently than input().

---

#### code_vs_comment

**Description:** Comment in parse_print_using says format string can be any expression, but error message hardcodes expectation of semicolon which contradicts flexible expression parsing

**Affected files:**
- `src/parser.py`

**Details:**
Comment in parse_print_using() says:
"The format string is parsed as an expression, allowing:
- String literals: PRINT USING '###.##'; X
- String variables: PRINT USING F$; X
- Any expression that evaluates to a string"

But the error message uses:
"raise ValueError(f'Expected \';\' after PRINT USING format string at line {self.current.line}')"

This uses ValueError instead of ParseError (inconsistent with rest of parser), and references self.current.line directly instead of self.current().line (would cause AttributeError if current() returns None).

---

#### code_internal_inconsistency

**Description:** parse_print_using uses ValueError instead of ParseError, inconsistent with all other parsing methods

**Affected files:**
- `src/parser.py`

**Details:**
In parse_print_using() around line 1050:
"raise ValueError(f'Expected \';\' after PRINT USING format string at line {self.current.line}')"

Every other parsing method in the file uses ParseError, not ValueError. This is inconsistent error handling.

---

#### code_internal_inconsistency

**Description:** parse_print_using accesses self.current.line directly instead of self.current().line, will cause AttributeError

**Affected files:**
- `src/parser.py`

**Details:**
In parse_print_using() around line 1050:
"raise ValueError(f'Expected \';\' after PRINT USING format string at line {self.current.line}')"

Should be self.current().line (method call) not self.current.line (property access). All other code in the file uses self.current() as a method.

---

#### code_vs_comment

**Description:** get_all_variables() docstring example shows 'case_variants' field but implementation doesn't include it

**Affected files:**
- `src/runtime.py`

**Details:**
Docstring example shows:
"Example:
    [
        {'name': 'counter', 'type_suffix': '%', 'is_array': False, 'value': 42,
         'last_read': {'line': 20, 'position': 5, 'timestamp': 1234.567},
         'last_write': {'line': 10, 'position': 4, 'timestamp': 1234.500}},
        ...
    ]"

But the actual implementation at the end:
```python
var_info = {
    'name': base_name,
    'type_suffix': type_suffix,
    'is_array': False,
    'value': var_entry['value'],
    'last_read': var_entry['last_read'],
    'last_write': var_entry['last_write'],
    'original_case': var_entry.get('original_case', base_name)
}
```

The docstring mentions 'original_case' in the description but doesn't show it in the example. Also, the docstring earlier mentions 'case_variants' in variable storage but it's not included in the returned dict.

---

#### documentation_inconsistency

**Description:** Settings file paths documented inconsistently between Windows and Unix

**Affected files:**
- `src/settings.py`

**Details:**
In _get_global_settings_path():
if os.name == 'nt':  # Windows
    appdata = os.getenv('APPDATA', os.path.expanduser('~'))
    base_dir = Path(appdata) / 'mbasic'
else:  # Linux/Mac
    base_dir = Path.home() / '.mbasic'

Windows uses 'mbasic' (no dot) while Unix uses '.mbasic' (with dot). The module docstring says:
"Supports global settings (~/.mbasic/settings.json) and project settings (.mbasic/settings.json)."

This only documents the Unix path convention, not the Windows path (APPDATA/mbasic/settings.json). Users on Windows won't know where to find their settings.

---

#### internal_inconsistency

**Description:** Code uses both fixed-width (5-char) and variable-width line number formatting in different places

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Variable width in _format_line():
line_num_str = f"{line_num}"

Fixed width in _parse_line_numbers():
line_num_formatted = f"{num_str:>5}"

This inconsistency means pasted lines get 5-char formatting but programmatically added lines get variable width, leading to inconsistent display.

---

#### code_internal_inconsistency

**Description:** Multiple IO handlers created with unclear lifecycle and usage

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Three different IO handler instances are created:
1. self.io_handler = CapturingIOHandler() (line ~65) - used for program execution
2. immediate_io = OutputCapturingIOHandler() (line ~66) - used for interpreter
3. immediate_io = OutputCapturingIOHandler() (line ~85 in start()) - recreated for ImmediateExecutor

The code creates self.io_handler (CapturingIOHandler) but then creates a different type (OutputCapturingIOHandler) for the interpreter. It's unclear which IO handler is actually used during program execution vs immediate mode, and why two different types are needed.

---

#### code_vs_comment

**Description:** Comment states 'don't reset PC' and 'RUN 120 already set PC to line 120', but the code doesn't actually check or preserve PC from a RUN command with line number

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment says: '# NOTE: Don't call interpreter.start() because it resets PC!
# RUN 120 already set PC to line 120, so we preserve it.'

However, the code flow shows:
1. _execute_immediate() calls immediate_executor.execute(command)
2. If command is 'RUN 120', the immediate executor would handle it
3. The code then checks 'if self.interpreter.has_work()' and starts execution
4. But there's no evidence that RUN 120 actually sets PC before this point
5. The comment assumes PC is already set, but the code doesn't verify this

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of program synchronization - _execute_immediate syncs program to runtime but cmd_delete and cmd_renum don't

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
_execute_immediate() does:
# Parse editor content into program (in case user typed lines directly)
self._parse_editor_content()
# Load program lines into program manager
self.program.clear()
for line_num in sorted(self.editor_lines.keys()):
    line_text = f"{line_num} {self.editor_lines[line_num]}"
    self.program.add_line(line_num, line_text)
# Sync program to runtime
self._sync_program_to_runtime()

But cmd_delete() and cmd_renum() only call:
self._refresh_editor()

They don't sync to runtime, which could cause inconsistencies if program is modified during execution.

---

#### code_vs_documentation

**Description:** Help widget hardcodes 'curses' UI name but keybindings.py shows HELP_KEY is Ctrl+F, not matching the comment in help_widget.py

**Affected files:**
- `src/ui/help_widget.py`
- `src/ui/keybindings.py`

**Details:**
help_widget.py line 42: "# HelpWidget is curses-specific (uses urwid), so hardcode 'curses' UI name"
help_widget.py line 43: "self.macros = HelpMacros('curses', help_root)"

keybindings.py lines 103-106:
"# Help system - use Ctrl+F (F for help/Find help)
HELP_KEY = 'ctrl f'
HELP_CHAR = '\x06'
HELP_DISPLAY = '^F'"

The comment says Ctrl+F is for help, but the actual keybinding loaded from JSON might be different. The help_widget should use the keybindings module to get the actual help key.

---

#### code_vs_comment

**Description:** Comment says 'Step Line (Ctrl+K) - execute all statements on current line' but the variable is named LIST_KEY, which is confusing

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py lines 169-172:
"# Step Line (Ctrl+K) - execute all statements on current line
_list_key = _get_key('editor', 'step_line') or 'Ctrl+K'
LIST_KEY = _ctrl_key_to_urwid(_list_key)
LIST_CHAR = _ctrl_key_to_char(_list_key)
LIST_DISPLAY = _list_key"

The variable is named LIST_KEY but the comment and JSON key say 'step_line'. This is very confusing. Either the variable should be renamed to STEP_LINE_KEY, or the comment should explain why it's called LIST_KEY (perhaps historical reasons from BASIC's LIST command?).

---

#### code_vs_comment

**Description:** Critical incomplete method that would cause runtime errors

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
The _edit_simple_variable method is incomplete:

'class ImmediateModeToken:
    def __init__(self):'

This class definition has no body and the method doesn't complete. If this method is called (via double-click on variable), it would raise SyntaxError or IndentationError. This is a critical bug that would crash the application.

---

#### code_vs_comment

**Description:** cmd_cont() docstring claims functionality is incomplete and attributes don't exist, but code attempts to use them anyway

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring says: 'TODO: This implementation is incomplete. The runtime.stop_line and runtime.stop_stmt_index attributes are not set anywhere when a program stops, so this will fail. Need to implement proper state saving on STOP.'

But code still tries to use these attributes:
if hasattr(self.runtime, 'stop_line') and hasattr(self.runtime, 'stop_stmt_index'):
    self.runtime.current_line = self.runtime.stop_line
    self.runtime.current_stmt_index = self.runtime.stop_stmt_index

---

#### code_vs_comment

**Description:** Comment says 'Don't check self.running' but then checks self.interpreter which depends on running state

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~1181 in _execute_tick(): '# Don't check self.running - it seems to not persist correctly in NiceGUI callbacks'
But immediately after:
'if not self.interpreter:
    return'
And throughout the method, self.running is set to False on errors. The comment suggests self.running is unreliable, but the code still uses it extensively.

---

#### code_vs_comment

**Description:** Comment in _on_editor_change claims to detect paste by content difference, but the logic checks for double line numbers

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment says: '# If content changed significantly (>5 chars), likely a paste'

But the actual paste detection logic checks:
```
if lines and re.match(r'^\d+\s+\d+\s+', lines[0]):
    # First line has format "10 100 ..." - double line number from paste
```

This is checking for a specific pattern (double line numbers) not just content size. The comment about '>5 chars' describes the trigger condition, but the actual paste handling is pattern-based. These are two different detection strategies that may not align.

---

#### code_vs_documentation

**Description:** Help system URL mismatch between code and documentation structure

**Affected files:**
- `src/ui/web_help_launcher.py`
- `docs/help/README.md`

**Details:**
web_help_launcher.py uses HELP_BASE_URL = 'http://localhost/mbasic_docs' and constructs URLs like 'http://localhost/mbasic_docs/ui/tk/', but the documentation structure in docs/help/ suggests paths like 'docs/help/ui/tk/index.md'. The code assumes a web server at localhost serving mbasic_docs, but the actual documentation is in a different directory structure.

---

#### documentation_inconsistency

**Description:** Error codes table has gaps and inconsistent numbering

**Affected files:**
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
The error codes documentation states:
'Error codes 24-25, 27-28, and 31-49 are not defined in MBASIC 5.21 and are reserved for future use'
'Error codes 56, 59-60, and 65 are not defined in MBASIC 5.21 and are reserved for future use'

However, the tables show error codes 1-23, then jump to 26, 29-30, then 50-58, 61-64, 66-67. This creates confusion about which codes are actually defined vs reserved. The documentation should clearly list all defined codes in sequence or provide a complete table showing reserved codes explicitly.

---

#### documentation_inconsistency

**Description:** Contradictory information about PEEK/POKE implementation

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/compatibility.md`

**Details:**
architecture.md states: "PEEK/POKE - Emulated for compatibility" and "POKE: Parsed and executes successfully, but performs no operation (no-op)" and "PEEK: Returns random integer 0-255"

compatibility.md states: "PEEK/POKE - Emulated for compatibility" with same description but adds: "PEEK does NOT return values written by POKE"

Both documents describe the same feature but architecture.md is more detailed. The key point about PEEK not returning POKE values should be consistent across both documents.

---

#### documentation_inconsistency

**Description:** Self-contradictory information about Web UI file persistence

**Affected files:**
- `docs/help/mbasic/compatibility.md`

**Details:**
Within the same document (compatibility.md), the Web UI section states:
1. "Files stored in browser memory (not browser localStorage)"
2. "Files persist only during browser session"

But then in the same section it also states:
"File names:
- Must be simple names (no slashes, no paths)
- Automatically uppercased (CP/M style)"

The uppercasing behavior suggests some level of persistence or state management that contradicts the "memory only" claim. This needs clarification about what exactly is stored where.

---

#### documentation_inconsistency

**Description:** Execution Stack access method unclear

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
feature-reference.md lists 'Execution Stack (Menu only)' under Variable Inspection features and states 'Access through the menu bar' twice. However, it's unclear if this is actually implemented in Curses UI or if this is aspirational documentation. The '(Menu only)' designation is used for multiple features but no menu bar navigation is documented elsewhere in the Curses UI docs.

---

#### documentation_inconsistency

**Description:** Contradictory keyboard shortcuts for Save operation

**Affected files:**
- `docs/help/ui/curses/files.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
files.md states: 'Press **Ctrl+V** (Note: Ctrl+S unavailable due to terminal flow control)' for saving programs.

However, quick-reference.md shows: '**^V** (Ctrl+V) | Save program (Ctrl+S unavailable - terminal flow control)'

But the quick-reference table also lists 'Ctrl+S' as unavailable, yet files.md explicitly says to use Ctrl+V. This creates confusion about which key actually saves files.

---

#### documentation_inconsistency

**Description:** Contradictory sort mode cycling information

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
variables.md states: 'Press `s` to cycle through sort orders: - **Name (A-Z)**: Alphabetical by variable name - **Type**: Group by variable type - **Value**: Sort by value (numerics first) - **Last Modified**: Recently changed first'

quick-reference.md states: '**s** | Cycle sort mode (Name → Accessed → Written → Read → Type → Value)'

These are completely different sort mode lists. The quick-reference includes 'Accessed', 'Written', 'Read' which are not in variables.md, and variables.md includes 'Last Modified' which is not in quick-reference.md.

---

#### documentation_inconsistency

**Description:** Find/Replace feature availability contradiction

**Affected files:**
- `docs/help/ui/curses/find-replace.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
find-replace.md clearly states: '## Current Status

The Curses UI currently **does not have** Find/Replace functionality. This feature is planned for future implementation.'

However, quick-reference.md does not mention this limitation and the help-navigation.md shows search functionality with '**{{kbd:search}}** | Open search prompt'.

This creates confusion about whether search/find exists in Curses UI or not.

---

#### documentation_inconsistency

**Description:** Tk settings documentation describes comprehensive multi-tab settings dialog with Editor, Keywords, Variables, Interpreter, and UI tabs, but Web settings documentation only shows Editor and Limits tabs. The Tk documentation explicitly states it's 'planned' and 'intended implementation' but then describes features as if they exist.

**Affected files:**
- `docs/help/ui/tk/settings.md`
- `docs/help/ui/web/settings.md`

**Details:**
Tk settings.md states: 'The Tk (Tkinter) desktop GUI is planned to provide the most comprehensive settings dialog. The features described below represent the intended implementation.' but then proceeds to document features like Keywords tab with 'Case Style' dropdown, Variables tab with 'Case Conflict' and 'Show Types In Window', Interpreter tab with 'Strict Mode', 'Max Execution Time', 'Debug Mode', and UI tab with 'Theme' and 'Font Size' as if they are implemented.

Web settings.md clearly states: 'Unlike the Tk desktop interface which has extensive configuration options, the Web UI focuses on the most commonly used settings' and only documents Editor tab (auto-numbering settings) and Limits tab (view-only).

This creates confusion about what is actually implemented vs planned.

---

#### documentation_inconsistency

**Description:** Contradictory information about implemented debugging features

**Affected files:**
- `docs/help/ui/web/debugging.md`
- `docs/help/ui/web/features.md`

**Details:**
debugging.md states under 'Setting Breakpoints > Currently Implemented':
'1. Use **Run → Toggle Breakpoint** menu option
2. Enter the line number when prompted
3. A visual indicator appears in the editor
4. Use **Run → Clear All Breakpoints** to remove all'

But then under 'Variable Inspector' it says:
'**Note:** The detailed variable inspector features described below are partially implemented. Basic variable viewing via Debug menu is available, but the advanced panels and watch expressions are planned for future releases.'

And under 'Call Stack' it says:
'**Note:** The call stack panel described below is a planned feature and not yet implemented in the Web UI.'

features.md under 'Debugging Tools > Breakpoints' says:
'**Currently Implemented:**
- Line breakpoints (toggle via Run menu)
- Clear all breakpoints
- Visual indicators in editor'

But then under 'Variable Inspector' it describes extensive features without clearly marking them as planned vs implemented.

---

#### documentation_inconsistency

**Description:** Features document extensively describes unimplemented features without consistent marking

**Affected files:**
- `docs/help/ui/web/features.md`

**Details:**
features.md has a note at the top: 'This document describes both currently implemented features and planned enhancements. Some advanced features (code intelligence, automatic saving, session recovery, collaborative editing) are planned for future releases.'

However, many sections describe features in present tense without indicating they are planned:

- 'Code Intelligence' section describes auto-completion, syntax checking, code folding as if implemented
- 'Search and Replace' section describes Find (Ctrl+F) and Replace (Ctrl+H) as if implemented
- 'Session Management' has a note saying collaboration features aren't implemented, but other session features are described without clarification
- 'Templates' section describes program templates and code snippets as if implemented
- 'Documentation > Inline Help' describes hover documentation and parameter hints as if implemented
- 'Testing' section describes test support and benchmarking as if implemented

Only some sections have '(Planned)' or '(Future)' markers. This inconsistency makes it very difficult to know what is actually available.

---

#### documentation_inconsistency

**Description:** Settings system documented but implementation status unclear

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`
- `docs/user/INSTALL.md`

**Details:**
SETTINGS_AND_CONFIGURATION.md provides extensive documentation for a settings system with commands like:
- SET "setting.name" value
- SHOW SETTINGS
- HELP SET "setting.name"

It describes settings files at ~/.mbasic/settings.json and .mbasic/settings.json with JSON configuration.

However, INSTALL.md's 'Feature Status' section lists what works and what doesn't, but makes no mention of a settings system, configuration files, or the SET/SHOW SETTINGS commands. This is a significant omission if the settings system is implemented, or misleading documentation if it's not.

---

#### documentation_inconsistency

**Description:** Contradictory information about CLI Save functionality

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
UI_FEATURE_COMPARISON.md states multiple times that CLI cannot save without filename:
| **Save (with prompt)** | ❌ | ✅ | ✅ | ✅ |
'Limitations: No Save without filename prompt'
'Known Gaps: CLI: No Save without prompt'

However, the same document shows CLI has Save As:
| **Save As** | ✅ | ✅ | ✅ | ✅ | SAVE "filename" / Ctrl+Shift+S |

This is contradictory - if CLI supports 'SAVE "filename"' (Save As), then it does support saving, just requires a filename. The distinction between 'Save with prompt' vs 'Save As' is unclear.

---

### 🟡 Medium Severity

#### documentation_inconsistency

**Description:** Version mismatch between setup.py and documentation comments

**Affected files:**
- `setup.py`
- `src/ast_nodes.py`

**Details:**
setup.py declares version="0.99.0" with comment "Reflects ~99% implementation status (core complete)", but the docstrings throughout ast_nodes.py consistently reference "MBASIC 5.21" as the target version. The setup.py version number (0.99.0) suggests implementation completeness while the code comments suggest targeting a specific MBASIC version (5.21).

---

#### code_comment_conflict

**Description:** PrintStatementNode has keyword_token field but other similar nodes don't consistently have it

**Affected files:**
- `src/ast_nodes.py`

**Details:**
PrintStatementNode has:
    keyword_token: Optional[Token] = None  # Token for PRINT keyword (for case handling)

IfStatementNode has:
    keyword_token: Optional[Token] = None  # Token for IF keyword
    then_token: Optional[Token] = None     # Token for THEN keyword
    else_token: Optional[Token] = None     # Token for ELSE keyword (if present)

ForStatementNode has:
    keyword_token: Optional[Token] = None  # Token for FOR keyword
    to_token: Optional[Token] = None       # Token for TO keyword
    step_token: Optional[Token] = None     # Token for STEP keyword (if present)

However, many other statement nodes (LprintStatementNode, InputStatementNode, etc.) do not have keyword_token fields. This inconsistency suggests incomplete implementation of case-preserving functionality across all statement types.

---

#### code_vs_comment

**Description:** Comment in INPUT method claims it reads from file_handle, but code actually reads from file_info['handle']

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line ~1050: Comment says 'file_handle = self.runtime.files[file_num]' but code does:
            file_num = int(file_num)
            if file_num not in self.runtime.files:
                raise ValueError(f"File #{file_num} not open")

            file_handle = self.runtime.files[file_num]
            return file_handle.read(num)

However, based on EOF() method pattern, self.runtime.files[file_num] returns a dict with 'handle' key, not a file handle directly. The variable name 'file_handle' is misleading - it should be 'file_info' and then access file_info['handle'].read(num)

---

#### code_vs_comment

**Description:** EOF() method comment describes ^Z handling but implementation may not work correctly for all file modes

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Lines ~920-925: Comment says 'Note: For input files, respects ^Z (ASCII 26) as EOF marker (CP/M style)'

However, the code only checks for ^Z when mode == 'I'. The read(1) operation returns bytes, but the code checks 'next_byte[0] == 26' which assumes bytes indexing. This works, but the comment doesn't clarify that this only applies to binary/input mode files, not text mode files where ^Z might be handled differently by Python's file system.

---

#### code_internal_inconsistency

**Description:** Inconsistent file info access pattern between EOF() and INPUT() methods

**Affected files:**
- `src/basic_builtins.py`

**Details:**
EOF() method (line ~930) correctly accesses file info:
file_info = self.runtime.files[file_num]
file_handle = file_info['handle']

But INPUT() method (line ~1050) incorrectly treats the dict as a file handle:
file_handle = self.runtime.files[file_num]
return file_handle.read(num)

This should be:
file_info = self.runtime.files[file_num]
return file_info['handle'].read(num)

---

#### code_vs_documentation

**Description:** SandboxedFileIO documentation claims it uses browser localStorage, but implementation uses backend.sandboxed_fs (server memory)

**Affected files:**
- `src/file_io.py`

**Details:**
src/file_io.py SandboxedFileIO docstring:
"Sandboxed file operations for web UI.

Acts as an adapter to backend.sandboxed_fs (SandboxedFileSystemProvider from
src/filesystem/sandboxed_fs.py), which provides an in-memory virtual filesystem.
Files are stored in Python server memory (not browser localStorage)."

But earlier in the same file:
"- SandboxedFileIO: Browser localStorage (Web UI)"

And in the method docstrings:
"Load file from browser localStorage."
"Save file to browser localStorage."
"Delete file from browser localStorage."
"Check if file exists in browser localStorage."

The class docstring correctly states files are in server memory, but the method docstrings and summary incorrectly claim localStorage.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for the two filesystem abstractions

**Affected files:**
- `src/file_io.py`
- `src/filesystem/base.py`

**Details:**
src/file_io.py uses:
"TWO SEPARATE FILESYSTEM ABSTRACTIONS:
1. FileIO (this file) - Program management operations
2. FileSystemProvider (src/filesystem/base.py) - Runtime file I/O"

src/filesystem/base.py uses:
"TWO SEPARATE FILESYSTEM ABSTRACTIONS:
1. FileIO (src/file_io.py) - Program management operations
2. FileSystemProvider (this file) - Runtime file I/O"

Both describe the same architecture but with slightly different wording. The descriptions should be identical for consistency, or reference a single canonical source.

---

#### code_vs_documentation

**Description:** SandboxedFileIO methods are documented as STUBS but list_files() is fully implemented

**Affected files:**
- `src/file_io.py`

**Details:**
The class docstring states:
"NOTE: Partially implemented. list_files() delegates to backend.sandboxed_fs,
but load_file(), save_file(), delete_file(), and file_exists() are STUBS that
raise IOError or return empty results."

However, list_files() is fully implemented and functional, not a stub. The documentation should clarify that list_files() is the ONE implemented method, while the others are stubs. Current wording suggests all methods including list_files() might be problematic.

---

#### code_vs_documentation

**Description:** SandboxedFileSystemProvider claims per-user isolation but uses class-level storage that could leak between instances

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
The docstring states:
"Features:
- All files stored in memory (no disk access)
- Per-user isolation (user_id-based)"

And:
"Security:
- No access to real filesystem
- No path traversal (../ etc.)
- Resource limits enforced"

The implementation uses:
"# Class-level storage for all users
# Structure: {user_id: {filename: content}}
_user_filesystems: Dict[str, Dict[str, Union[str, bytes]]] = {}"

While this does provide per-user isolation via user_id keys, the class-level storage means all users' data is in the same dictionary. This is secure if user_id is properly validated, but the security documentation doesn't mention the requirement for secure user_id generation/validation.

---

#### code_vs_comment

**Description:** Docstring claims immediate mode is allowed during 'waiting_for_input' state, but implementation may not properly handle this case

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Docstring states:
"CAN execute when waiting for input:
- 'waiting_for_input' - Program is waiting for INPUT. Immediate mode is allowed
  to inspect/modify variables while paused for input."

However, can_execute_immediate() checks:
"return (self.runtime.halted or
        state.error_info is not None or
        state.input_prompt is not None)"

The check 'state.input_prompt is not None' assumes that when waiting for input, input_prompt is set. But there's no verification that this state attribute exists or is properly maintained. The docstring promises this works, but the implementation doesn't validate the state model matches the documentation.

---

#### code_vs_comment

**Description:** Numbered line handling has complex UI interaction logic that may not work if 'interactive_mode' is not properly set

**Affected files:**
- `src/immediate_executor.py`

**Details:**
The execute() method has special handling for numbered lines:
"if hasattr(self.interpreter, 'interactive_mode') and self.interpreter.interactive_mode:"

This assumes:
1. The interpreter has an 'interactive_mode' attribute
2. That attribute points to a UI object with 'program' attribute
3. The program has 'add_line' and 'delete_line' methods
4. The UI has '_refresh_editor' and '_highlight_current_statement' methods

None of these assumptions are documented in the class docstring or validated. If any of these conditions fail, the code falls through to:
"return (False, 'Cannot edit program lines in this mode\n')"

But the error message doesn't explain why it failed or what mode is required.

---

#### code_vs_comment

**Description:** Docstring claims to check 'microprocessor model' but implementation checks generic state attributes

**Affected files:**
- `src/immediate_executor.py`

**Details:**
The can_execute_immediate() method has a comment:
"# Check interpreter state using microprocessor model"

But the actual implementation just checks:
"if hasattr(self.interpreter, 'state') and self.interpreter.state:"

There's no reference to any 'microprocessor model' in the code. This appears to be either:
1. A reference to an architectural concept not explained in this file
2. An outdated comment from a previous implementation
3. A planned feature that wasn't implemented

The term 'microprocessor model' is not defined or documented anywhere in the provided code.

---

#### code_vs_comment

**Description:** Comment claims _renum_erl_comparison only handles comparison operators, but code renumbers for ANY binary operator with ERL on left

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~1050 says:
"MBASIC manual specifies: if ERL appears on left side of comparison operator
(=, <>, <, >, <=, >=), the right-hand number is a line number reference.

Current implementation: Renumbers for ANY binary operator with ERL on left,
including arithmetic (ERL + 100, ERL * 2)."

The code at line ~1065 checks:
if type(expr).__name__ != 'BinaryOpNode':
    return

This means it processes ALL binary operators (arithmetic, comparison, logical), not just comparisons as the manual specifies.

---

#### code_vs_comment

**Description:** EDIT command docstring claims count prefixes and search commands are not implemented, but doesn't explain what happens when entered

**Affected files:**
- `src/interactive.py`

**Details:**
Docstring at line ~1145 says:
"Note: Count prefixes ([n]D, [n]C) and search commands ([n]S, [n]K) are not yet implemented.
If entered, they will be treated as unknown commands and silently ignored."

However, the code at lines ~1190-1240 shows that entering digits or letters like 'S' or 'K' would be processed as individual commands. For example:
- Entering '5' would be treated as an unknown command (no handler for '5')
- Entering 'D' after '5' would delete one character

The commands are NOT silently ignored - they're processed character by character. The docstring is misleading.

---

#### code_vs_comment

**Description:** Comment about COMMON variables in cmd_chain says 'common_vars stores base names' but doesn't explain type suffix resolution logic clearly

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~730 says:
"# Note: common_vars stores base names (e.g., 'i'), but actual variables
# may have type suffixes (e.g., 'i%', 'i$') based on DEF statements"

The code then tries all possible suffixes ('%', '$', '!', '#', '') to find the variable. However, the comment doesn't explain WHY this is necessary or what happens if multiple variables with different suffixes exist (e.g., both 'i%' and 'i$'). The code would only save the first one found, which might not be the intended behavior.

---

#### code_vs_comment

**Description:** cmd_merge docstring says it 'adds or replaces lines' but doesn't mention it updates runtime statement_table

**Affected files:**
- `src/interactive.py`

**Details:**
Docstring at line ~640 says:
"MERGE 'filename' - Merge program from file into current program

MERGE adds or replaces lines from a file without clearing existing lines.
- Lines with matching line numbers are replaced
- New line numbers are added
- Existing lines not in the file are kept"

But code at lines ~675-680 shows:
if self.program_runtime:
    for line_num in self.program.line_asts:
        line_ast = self.program.line_asts[line_num]
        self.program_runtime.statement_table.replace_line(line_num, line_ast)

The docstring doesn't mention that MERGE also updates the runtime's statement_table if a program is currently loaded, which is important for understanding side effects.

---

#### code_vs_comment

**Description:** execute_immediate docstring says it uses program_runtime for 'stopped OR finished programs' but doesn't explain the difference

**Affected files:**
- `src/interactive.py`

**Details:**
Docstring at line ~1310 says:
"Runtime selection:
- If program_runtime exists (from RUN), use it so immediate mode can
  examine/modify program variables (works for stopped OR finished programs)
- Otherwise use persistent immediate mode runtime for variable isolation"

The comment mentions 'stopped OR finished programs' but doesn't explain:
1. What's the difference between stopped and finished?
2. How does the code distinguish between them?
3. Why does it matter for immediate mode execution?

The code doesn't check whether the program is stopped or finished - it just checks if program_runtime exists.

---

#### code_vs_comment_conflict

**Description:** Comment claims GOTO/GOSUB in immediate mode won't have intended effect due to PC save/restore, but code actually allows them to execute and only restores PC afterward

**Affected files:**
- `src/interactive.py`

**Details:**
Comment states: "Immediate mode should NOT use GOTO/GOSUB (see help text) because PC changes would break CONT functionality for stopped programs. We save/restore PC to prevent this, but the statements themselves can technically execute GOTO/GOSUB - they just won't have the intended effect."

However, the code allows GOTO/GOSUB to execute normally:
```
for stmt in line_node.statements:
    interpreter.execute_statement(stmt)
```
Then restores PC after execution. This means GOTO/GOSUB WILL execute and change PC during execution, potentially jumping to program lines and executing code there. Only after all statements complete is PC restored. The comment suggests they won't work, but they actually will work during execution - just the final PC change is reverted.

---

#### code_vs_comment

**Description:** Comment describes skip_next_breakpoint_check behavior incorrectly

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line 48-50 says:
"Set when halting at a breakpoint.
On next execution, allows stepping past the breakpoint once,
then clears itself. Prevents re-halting on same breakpoint."

But code at lines 331-336 shows:
```
if at_breakpoint:
    if not self.state.skip_next_breakpoint_check:
        self.runtime.halted = True
        self.state.skip_next_breakpoint_check = True
        return self.state
    else:
        self.state.skip_next_breakpoint_check = False
```

The flag is SET when halting (not before), and CLEARED when allowing execution past the breakpoint. The comment suggests it's set before halting, but the code sets it during the halt.

---

#### code_vs_comment

**Description:** Comment about return_stmt validation contradicts actual validation logic

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at lines 1088-1092 says:
"return_stmt is 0-indexed offset into statements array.
Valid range: 0 to len(statements) where len(statements) is a special sentinel value
meaning 'continue at next line' (GOSUB's last statement completed, resume after the line).
Values > len(statements) indicate the statement was deleted (validation error)."

But validation code at line 1093 checks:
```
if return_stmt > len(line_statements):  # Check for strictly greater than (== len is OK)
```

This means return_stmt == len(statements) is valid (as comment states), but the comment's description of "valid range: 0 to len(statements)" is ambiguous - it could mean inclusive or exclusive of len(statements). The code clarifies it's inclusive, but the comment could be clearer.

---

#### code_vs_comment

**Description:** current_statement_char_end docstring describes complex logic that may not match all edge cases

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring at lines 77-85 says:
"Uses max(char_end, next_char_start - 1) to handle string tokens correctly.
For the last statement on a line, uses line_text_map to get actual line length.
This works because:
- If there's a next statement, the colon is at next_char_start - 1
- If char_end is correct (most tokens), it will be >= next_char_start - 1
- If char_end is too short (string tokens), next_char_start - 1 is larger"

However, the code at lines 95-97 has a fallback:
```
else:
    return stmt_char_end
```

This fallback returns stmt_char_end when there's no line_text_map entry, but the docstring doesn't mention this case. The docstring implies line_text_map is always available for last statements, but the code handles its absence.

---

#### code_vs_comment

**Description:** Comment claims WEND pops loop before jumping, but code pops after setting NPC

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~285 says:
"Pop the loop from the stack BEFORE jumping back to WHILE.
The WHILE will re-push if the condition is still true, or skip the
loop body if the condition is now false. This ensures clean stack state."

But code does:
self.runtime.npc = PC(loop_info['while_line'], loop_info['while_stmt'])
self.limits.pop_while_loop()
self.runtime.pop_while_loop()

The NPC is set BEFORE popping, meaning the pop happens after the jump target is set, not before.

---

#### code_vs_comment

**Description:** CLEAR documentation claims to preserve COMMON variables but code clears them

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~450 says:
"Note: Preserved state for CHAIN compatibility:
  - runtime.common_vars (COMMON variables)
  - runtime.files (open file handles)
  - runtime.field_buffers (random access file buffers)
  - runtime.user_functions (DEF FN functions)"

But the execute_clear code at line ~440 calls:
self.runtime.clear_variables()
self.runtime.clear_arrays()

And then closes all files:
for file_num in list(self.runtime.files.keys()):
    try:
        file_obj = self.runtime.files[file_num]
        if hasattr(file_obj, 'close'):
            file_obj.close()
    except:
        pass
self.runtime.files.clear()
self.runtime.field_buffers.clear()

The code explicitly clears files and field_buffers, contradicting the comment that says they are preserved.

---

#### code_vs_comment

**Description:** File reading comment claims 'bare except: pass' for error handling but no such code exists in CLEAR

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~445 says:
"Note: Errors during file close are silently ignored (bare except: pass below)"

But the code uses:
try:
    file_obj = self.runtime.files[file_num]
    if hasattr(file_obj, 'close'):
        file_obj.close()
except:
    pass

This is indeed a bare except with pass, so the comment is accurate. However, the same comment appears at line ~1050 in execute_reset with identical code, suggesting copy-paste documentation.

---

#### documentation_inconsistency

**Description:** Multiple comments reference 'tick-based execution mode' and 'state machine' for INPUT but implementation details are scattered

**Affected files:**
- `src/interpreter.py`

**Details:**
Comments at lines ~540 and ~650 mention:
"In tick-based execution mode, this may transition to 'waiting_for_input' state
instead of blocking."

However, the actual state machine logic (checking self.state.input_buffer, setting self.state.input_prompt, etc.) is implemented inline without clear documentation of the state transitions or how provide_input() interacts with this. The state machine behavior is implied but not explicitly documented.

---

#### code_vs_comment

**Description:** Comment claims MID$ assignment length parameter is required, but code handles missing length gracefully

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment in execute_midassignment says:
"(length is required in our implementation; parser should enforce this)"

But the code evaluates stmt.length without checking if it exists:
length = int(self.evaluate_expression(stmt.length))

If length were truly required and enforced by parser, this comment is misleading. If it's optional, the comment is wrong and code should handle None case.

---

#### code_vs_comment

**Description:** Comment about CONT and Break behavior is confusing and potentially incorrect

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_cont:
"Note: This function only checks the stopped flag. Ctrl+C (Break) interrupts execution
without setting stopped=True, so CONT cannot resume after Break. This is handled elsewhere
in the execution flow (Break sets halted but not stopped)."

The comment says Break sets halted but not stopped, and that CONT cannot resume after Break. However, the code only checks:
if not self.runtime.stopped:
    raise RuntimeError("Can't continue - no program stopped")

This suggests the distinction between stopped (STOP statement) and halted (Break) is important, but the comment placement in execute_cont makes it unclear if this is the intended behavior or a limitation.

---

#### documentation_inconsistency

**Description:** LIST command documentation claims to preserve formatting but relies on line_text_map staying in sync

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_list docstring:
"Note: Outputs from line_text_map (original source text), not regenerated from AST.
This preserves formatting but requires line_text_map to stay in sync with AST."

This is a significant implementation constraint that could lead to bugs if line_text_map gets out of sync with the AST (e.g., after program modifications). The documentation doesn't explain when/how this sync is maintained or what happens if they diverge. This is a potential source of bugs that should be documented more thoroughly.

---

#### code_vs_comment

**Description:** String length limit enforcement comment doesn't match error handling pattern

**Affected files:**
- `src/interpreter.py`

**Details:**
In evaluate_binaryop for PLUS operator:
"# Enforce 255 byte string limit (MBASIC 5.21 compatibility)
if isinstance(result, str) and len(result) > 255:
    raise RuntimeError("String too long")"

This is the only place in the visible code that enforces the 255-byte string limit. The comment claims MBASIC 5.21 compatibility, but:
1. It only checks string concatenation, not other string operations
2. It uses len(result) which counts characters, not bytes (latin-1 encoding could differ)
3. No other string operations (MID$, LSET, RSET, etc.) show this check

This suggests either incomplete implementation of the limit or the comment is misleading about the scope of enforcement.

---

#### documentation_inconsistency

**Description:** Module docstring claims 'originally named io' but provides no evidence this naming conflict was actually a problem in the codebase

**Affected files:**
- `src/iohandler/__init__.py`
- `src/iohandler/base.py`

**Details:**
src/iohandler/__init__.py states:
"Note: This module was originally named 'io' but was renamed to 'iohandler'
to avoid conflicts with Python's built-in 'io' module."

However, there's no indication in the code that Python's built-in 'io' module is actually used anywhere in the project, making this historical note potentially misleading or unnecessary.

---

#### code_vs_comment_conflict

**Description:** Deprecated alias methods suggest backward compatibility concern but no version history or migration guide exists

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
web_io.py contains:
"# Alias for backward compatibility
def print(self, text='', end='\n'):
    '''Deprecated: Use output() instead.'''
    self.output(text, end)"

and:
"# Alias for backward compatibility
def get_char(self):
    '''Deprecated: Use input_char() instead.'''
    return self.input_char(blocking=False)"

These suggest an API change occurred, but there's no documentation of when this happened, what the migration path is, or when these will be removed.

---

#### code_vs_comment_conflict

**Description:** Comment about KeywordCaseManager contradicts actual implementation using SimpleKeywordCase

**Affected files:**
- `src/lexer.py`

**Details:**
In lexer.py create_keyword_case_manager() docstring:
"Uses SimpleKeywordCase for straightforward case policy handling.
(Historical note: Earlier versions considered a more complex KeywordCaseManager
for advanced policies, but SimpleKeywordCase proved sufficient.)"

But src/keyword_case_manager.py shows KeywordCaseManager DOES exist and supports advanced policies like 'first_wins', 'preserve', and 'error' - not just simple force-based policies. The comment suggests KeywordCaseManager was abandoned, but it's a fully implemented class in the codebase.

---

#### implementation_inconsistency

**Description:** Lexer uses SimpleKeywordCase but KeywordCaseManager exists with more features

**Affected files:**
- `src/lexer.py`
- `src/keyword_case_manager.py`

**Details:**
lexer.py line ~30:
"# Keyword case handler - uses SimpleKeywordCase (simple force-based policies only)
# Note: KeywordCaseManager class exists for more complex policies (first_wins, preserve)
self.keyword_case_manager = keyword_case_manager or SimpleKeywordCase(policy='force_lower')"

But keyword_case_manager.py shows KeywordCaseManager supports:
- force_lower, force_upper, force_capitalize
- first_wins (use first occurrence)
- error (raise error on conflicts)
- preserve (preserve original case)

The lexer comment suggests these advanced policies exist but aren't used. This creates confusion about which class should be used and why SimpleKeywordCase exists separately.

---

#### implementation_inconsistency

**Description:** Platform-specific input_char() implementation has incomplete Windows fallback

**Affected files:**
- `src/iohandler/console.py`

**Details:**
console.py input_char() has this fallback for Windows:
"except ImportError:
    # Fallback: use input()
    return input()[:1] if input() else ''"

This fallback calls input() which blocks and waits for Enter key, completely defeating the purpose of single-character input. The function should either raise NotImplementedError or document this severe limitation.

---

#### code_vs_comment

**Description:** Comment claims APOSTROPHE starts a comment that consumes rest of line and no further statements can follow, but code allows statements after APOSTROPHE via COLON separator

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line ~120 says:
"Note: APOSTROPHE (') starts a comment that consumes the rest of the line.
The comment content is preserved in the AST as a statement, but no further
statements can follow on the same line after a comment."

But in parse_line() around line 280, the code explicitly handles APOSTROPHE as a statement that can be followed by more statements:
"elif self.match(TokenType.REM, TokenType.REMARK, TokenType.APOSTROPHE):
    # Allow REM/REMARK/' without colon after statement (standard MBASIC)
    # These consume rest of line as a comment
    stmt = self.parse_remark()
    if stmt:
        statements.append(stmt)
    break  # Comment ends the line"

The 'break' statement confirms comments end the line, but the earlier comment in at_end_of_line() contradicts the behavior described in parse_line().

---

#### code_vs_comment

**Description:** Comment says semicolons BETWEEN statements are treated as trailing no-ops, but code raises error if statement follows semicolon

**Affected files:**
- `src/parser.py`

**Details:**
Comment in parse_line() around line 270 says:
"# Allow trailing semicolon at end of line (treat as no-op).
# Context matters: Semicolons WITHIN PRINT/LPRINT are item separators (parsed there),
# but semicolons BETWEEN statements are treated as trailing no-ops (handled here)."

But the code immediately after:
"self.advance()
# If there's more after the semicolon, treat it as error
# But allow end of line or colon after semicolon
if not self.at_end_of_line() and not self.match(TokenType.COLON):
    token = self.current()
    raise ParseError(f'Expected : or newline after ;, got {token.type.name}', token)"

This means semicolons are NOT treated as statement separators (no-ops between statements), they can only appear at end of line. The comment is misleading.

---

#### code_vs_comment

**Description:** Comment says 'Some dialects allow semicolon, but MBASIC uses comma' after file number in PRINT, but no validation enforces this

**Affected files:**
- `src/parser.py`

**Details:**
In parse_print() around line 990:
"# Expect comma after file number
if self.match(TokenType.COMMA):
    self.advance()
# Note: Some dialects allow semicolon, but MBASIC uses comma"

The comment claims MBASIC requires comma, but the code doesn't enforce it - it just optionally consumes a comma if present. If semicolon appears instead, it would be treated as a separator in the expression list, not as an error. This is inconsistent with the stated MBASIC behavior.

---

#### code_vs_comment

**Description:** Comment claims both comma and semicolon after INPUT prompt show '?' but code doesn't track separator type

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line ~35 states:
"# Note: In MBASIC, both comma and semicolon after prompt show "?" prompt.
# The separator type doesn't affect behavior (both display "?"), so we just
# consume it without tracking."

However, this contradicts the suppress_question flag logic which specifically handles INPUT; (semicolon immediately after INPUT keyword) to suppress the '?' prompt. The comment suggests separator after prompt doesn't matter, but the code has special handling for semicolon position.

---

#### code_vs_documentation

**Description:** SHOWSETTINGS field name mismatch between implementation and node definition

**Affected files:**
- `src/parser.py`

**Details:**
In parse_showsettings() at line ~420, the code creates ShowSettingsStatementNode with:
  pattern=filter_expr,  # Use 'pattern' field name to match node definition

The comment explicitly states it's using 'pattern' to match the node definition, but the docstring describes the parameter as 'filter'. This suggests either the node definition uses 'pattern' while documentation uses 'filter', or vice versa.

---

#### code_vs_documentation

**Description:** SETSETTING field name mismatch between implementation and node definition

**Affected files:**
- `src/parser.py`

**Details:**
In parse_setsetting() at line ~440, the code creates SetSettingStatementNode with:
  setting_name=key_expr,  # Use 'setting_name' field name to match node definition

The comment explicitly states it's using 'setting_name' to match the node definition, but the docstring describes the parameter as 'key'. This suggests inconsistency between the node definition field names and the documentation.

---

#### code_vs_comment

**Description:** FOR statement comment mentions handling degenerate loops but implementation creates dummy variable

**Affected files:**
- `src/parser.py`

**Details:**
The docstring at line ~1140 states:
"Note: Some files may have degenerate FOR loops like 'FOR 1 TO 100'
which we'll try to handle gracefully"

The implementation creates a dummy variable 'I' for such cases. However, this may not be 'graceful' handling - it silently changes the semantics by creating a variable that wasn't in the original code. This could cause unexpected behavior if the code later references variable I.

---

#### code_vs_comment

**Description:** parse_width docstring claims statement is 'no-op in execution' but this is parser code, not execution code

**Affected files:**
- `src/parser.py`

**Details:**
Docstring says: 'Both parameters are parsed but the statement is a no-op in execution (see execute_width). Modern terminals handle line width automatically.'

This comment belongs in the executor, not the parser. The parser's job is to parse the syntax, not to describe execution behavior. The reference to 'execute_width' suggests this docstring was copied from or intended for the executor module.

---

#### code_vs_comment

**Description:** PC class docstring describes stmt_offset as '0-based index' but example shows confusion between offset and index terminology

**Affected files:**
- `src/pc.py`

**Details:**
Docstring says:
"The stmt_offset is a 0-based index into the statements list for a line."
Then example says:
"PC(10, 2)  - Third statement on line 10 (offset 2 = index 2)"

The parenthetical '(offset 2 = index 2)' is redundant if offset IS the index. This suggests either:
1. The terminology was changed during refactoring and comment wasn't updated
2. There's confusion about whether offset means 'distance from start' vs 'index position'

---

#### code_vs_documentation

**Description:** Inconsistent AST node type names between serialize_statement and _adjust_statement_positions

**Affected files:**
- `src/position_serializer.py`

**Details:**
In serialize_statement, the code checks:
if stmt_type == 'LetStatementNode':
    return self.serialize_let_statement(stmt)

But in _adjust_statement_positions, it checks:
if stmt_type == 'AssignmentStatementNode':
    _adjust_expression_positions(stmt.variable, offset)
    _adjust_expression_positions(stmt.expression, offset)

These appear to be the same statement type but with different names. This will cause _adjust_statement_positions to fail to adjust positions for LET statements.

---

#### code_vs_comment

**Description:** apply_keyword_case_policy docstring says 'keyword: The keyword to transform (normalized lowercase)' but doesn't enforce this

**Affected files:**
- `src/position_serializer.py`

**Details:**
Function docstring:
"Args:
    keyword: The keyword to transform (normalized lowercase)"

But the function doesn't validate or normalize the input. It just applies the policy to whatever is passed. For 'first_wins' policy, it does:
keyword_lower = keyword.lower()

This suggests the input might NOT be normalized lowercase. The docstring should either:
1. Remove '(normalized lowercase)' if caller is responsible for normalization
2. Add normalization at start of function if this function should handle it

---

#### code_vs_comment

**Description:** StatementTable.next_pc docstring says 'sequential execution' but doesn't clarify behavior for multi-statement lines

**Affected files:**
- `src/pc.py`

**Details:**
Method docstring:
"Get next PC after given PC (sequential execution)."

But doesn't explain that 'sequential' means:
1. Next statement on same line (increment stmt_offset)
2. OR first statement of next line (if at end of current line)

The implementation handles this correctly by using the keys_cache (which is insertion-ordered), but the docstring could be clearer about what 'sequential' means in the context of multi-statement lines.

---

#### code_vs_comment

**Description:** Docstring for get_variable() states token is REQUIRED but implementation allows token=None in some cases

**Affected files:**
- `src/runtime.py`

**Details:**
Docstring says:
"This method MUST be called with a token for normal program execution."
"Args:
    token: REQUIRED - Token object with line and position info for tracking."

But implementation has:
```python
if token is None:
    raise ValueError("get_variable() requires token parameter. Use get_variable_for_debugger() instead.")
```

However, later in the code:
```python
tracking_info = {
    'line': getattr(token, 'line', self.pc.line_num if self.pc and not self.pc.halted() else None),
    'position': getattr(token, 'position', None),
    'timestamp': time.perf_counter()
}
```

The getattr with fallback suggests token could be None or missing attributes, contradicting the REQUIRED claim and the ValueError check.

---

#### code_vs_comment

**Description:** Comment in _variables storage says 'line -1 indicates debugger/prompt/internal set' but set_variable() uses line=-1 for debugger_set=True

**Affected files:**
- `src/runtime.py`

**Details:**
Comment at line ~50:
"# Each variable is stored as: name_with_suffix -> {'value': val, 'last_read': {...}, 'last_write': {...}, 'original_case': str, 'case_variants': [...]}
# Note: line -1 in last_write indicates debugger/prompt/internal set (not from program execution)"

But in set_variable_raw() implementation:
```python
class FakeToken:
    def __init__(self):
        self.line = -1
        self.position = None

fake_token = FakeToken()

# Call set_variable for uniform handling
self.set_variable(name, type_suffix, value, token=fake_token)
```

This creates a token with line=-1 for internal/system variables (like ERR%, ERL%), which is different from debugger_set=True. The comment suggests line=-1 is only for debugger sets, but it's also used for system variable initialization.

---

#### code_vs_comment

**Description:** set_variable() docstring says 'MUST be called with a token' but allows token=None when debugger_set=True

**Affected files:**
- `src/runtime.py`

**Details:**
Docstring says:
"This method MUST be called with a token for normal program execution.
For debugger writes, pass debugger_set=True (token can be None).

Args:
    token: REQUIRED (unless debugger_set=True) - Token with line and position"

But implementation check:
```python
if token is None and not debugger_set:
    raise ValueError("set_variable() requires token parameter. Use debugger_set=True for debugger writes.")
```

This is consistent, but later code has:
```python
if not debugger_set and token is not None:
    if original_case is None:
        original_case = name
    canonical_case = self._check_case_conflict(name, original_case, token, settings_manager)
```

The 'token is not None' check is redundant given the earlier ValueError - if we reach this point and debugger_set=False, token cannot be None.

---

#### code_vs_comment

**Description:** dimension_array() docstring says 'token: Optional token for tracking DIM statement location' but implementation always uses it if provided

**Affected files:**
- `src/runtime.py`

**Details:**
Docstring says:
"Args:
    token: Optional token for tracking DIM statement location"

But implementation:
```python
tracking_info = None
if token is not None:
    tracking_info = {
        'line': getattr(token, 'line', self.pc.line_num if self.pc and not self.pc.halted() else None),
        'position': getattr(token, 'position', None),
        'timestamp': time.perf_counter()
    }

# Create array with access tracking
self._arrays[full_name] = {
    'dims': dimensions,
    'data': [default_value] * total_size,
    'last_read_subscripts': None,
    'last_write_subscripts': None,
    'last_read': tracking_info,  # DIM counts as both read and write
    'last_write': tracking_info
}
```

The comment 'DIM counts as both read and write' is misleading - DIM is an allocation/initialization operation, not a read. This should probably only set last_write.

---

#### code_vs_comment

**Description:** Inconsistency in get_execution_stack() docstring regarding 'from_line' field for GOSUB entries

**Affected files:**
- `src/runtime.py`

**Details:**
The docstring states:
"For GOSUB calls:
{
    'type': 'GOSUB',
    'from_line': 60,      # Line to return to (despite misleading name)
    'return_line': 60,    # Line to return to
    'return_stmt': 0      # Statement offset to return to
}"

But the actual code implementation is:
result.append({
    'type': 'GOSUB',
    'from_line': entry.get('return_line', 0),  # Line to return to
    'return_line': entry.get('return_line', 0),
    'return_stmt': entry.get('return_stmt', 0)  # Statement offset
})

The docstring acknowledges 'from_line' is misleading but still includes it in the documented return format. The field name suggests 'line where GOSUB was called from' but the comment and implementation show it's actually 'line to return to', making it redundant with 'return_line'.

---

#### documentation_inconsistency

**Description:** Comment claims 'Note: ui.theme not implemented yet' but there is no ui.theme setting defined in SETTING_DEFINITIONS

**Affected files:**
- `src/settings_definitions.py`

**Details:**
Comment at end of SETTING_DEFINITIONS dict says:
# Note: ui.theme not implemented yet
But no ui.theme setting exists in the definitions, making this comment confusing - it's unclear if it was removed or never added.

---

#### documentation_inconsistency

**Description:** Settings docstring mentions 'file > project > global > default' precedence but file-level settings are not fully implemented

**Affected files:**
- `src/settings.py`
- `src/settings_definitions.py`

**Details:**
In settings.py docstring:
"""Handles loading, saving, and accessing user settings with scope precedence.
Supports global settings (~/.mbasic/settings.json) and project settings (.mbasic/settings.json)."""

And in SettingsManager class:
"""Manages user settings with scope precedence (file > project > global > default)"""

But in __init__:
self.file_settings: Dict[str, Any] = {}  # Future: per-file settings

The 'file' scope is mentioned in precedence but marked as 'Future', creating confusion about whether it's supported.

---

#### code_vs_comment_conflict

**Description:** Token class has both original_case and original_case_keyword fields with overlapping purposes

**Affected files:**
- `src/tokens.py`

**Details:**
Token dataclass defines:
original_case: Any = None  # Original case for identifiers (before lowercasing)
original_case_keyword: str = None  # Original case for keywords (e.g., 'PRINT', 'Print', 'print')

The docstring says original_case is for 'identifiers before normalization' but also says original_case_keyword is 'Used by keyword case formatter to preserve or enforce case style'. This creates confusion - why have two fields? The __repr__ method shows both can be set simultaneously, suggesting they serve different purposes, but the distinction isn't clear from the comments.

---

#### code_vs_comment_conflict

**Description:** CLIBackend docstring mentions 'Future refactoring could move command logic' but this is implementation detail in user-facing docs

**Affected files:**
- `src/ui/cli.py`

**Details:**
CLIBackend docstring states:
"Implementation: Wraps the existing InteractiveMode class to reuse
its command parsing and execution logic. Future refactoring could
move command logic directly into this UIBackend subclass."

This is an implementation detail and future plan that shouldn't be in user-facing documentation. It creates uncertainty about the stability of the API.

---

#### code_vs_documentation_inconsistency

**Description:** load() method doesn't use _unflatten_settings but save() uses _flatten_settings

**Affected files:**
- `src/settings.py`

**Details:**
In load() method:
with open(self.global_settings_path, 'r') as f:
    data = json.load(f)
    self.global_settings = data.get('settings', {})

This directly assigns the loaded dict without unflattening.

But in _save_global():
data = {
    'version': '1.0',
    'settings': self._flatten_settings(self.global_settings)
}

This flattens before saving. If settings are stored flat but loaded as-is, there's a mismatch. Either:
1. Settings are stored flat and should be unflattened on load (bug in load)
2. Settings are stored nested and _flatten_settings shouldn't be called (bug in save)
3. The internal representation is flat and _flatten_settings is a no-op (confusing code)

---

#### Documentation inconsistency

**Description:** CLI STEP command documentation claims it matches curses UI 'Step Statement' (Ctrl+T), but the curses keybindings show both 'Step Statement' (Ctrl+T) and 'Step Line' (Ctrl+K) as separate commands. The CLI only implements statement-level stepping.

**Affected files:**
- `src/ui/cli_debug.py`
- `src/ui/curses_keybindings.json`

**Details:**
cli_debug.py docstring says:
"This matches the curses UI 'Step Statement' command (Ctrl+T).
Note: The curses UI also has 'Step Line' (Ctrl+K) which executes all
statements on the current line. The CLI STEP command is statement-only."

But curses_keybindings.json shows:
"step_line": {
  "keys": ["Ctrl+K"],
  "description": "Step Line (execute all statements on current line)"
}
"step": {
  "keys": ["Ctrl+T"],
  "description": "Step statement (execute one statement)"
}

This suggests the CLI is missing the 'Step Line' functionality that curses has.

---

#### Code vs Comment conflict

**Description:** The cmd_step docstring claims it 'Executes a single statement (not a full line)' and that 'each statement is executed separately', but the implementation calls tick() or execute_next() without any clear statement-level granularity control.

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
Docstring says:
"Executes a single statement (not a full line). If a line contains multiple
statements separated by colons, each statement is executed separately."

Implementation:
def _execute_single_step(self):
    """Execute a single statement (not a full line).

    Uses the interpreter's tick() or execute_next() method to execute
    one statement at the current program counter position.
    """
    if self.interactive.program_interpreter:
        # Use interpreter's tick() method if available
        if hasattr(self.interactive.program_interpreter, 'tick'):
            self.interactive.program_interpreter.tick()
        else:
            # Fallback to execute_next
            self.interactive.program_interpreter.execute_next()

The code doesn't show any logic to handle colon-separated statements differently. It's unclear if tick()/execute_next() actually provide statement-level granularity or if they execute entire lines.

---

#### Code vs Documentation inconsistency

**Description:** The enhance_run_command method modifies the RUN command to support breakpoints, but the cmd_break docstring doesn't mention that RUN must be called for breakpoints to take effect.

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
cmd_break docstring shows usage:
"Usage:
    BREAK           - List all breakpoints
    BREAK 100       - Set breakpoint at line 100
    BREAK 100-      - Clear breakpoint at line 100
    BREAK CLEAR     - Clear all breakpoints"

But the enhance_run_command implementation shows:
def enhanced_run(start_line=None):
    """Enhanced RUN with breakpoint support

    Args:
        start_line: Optional line number to start execution at
    """
    # Call original to set up runtime/interpreter
    original_run(start_line=start_line)

    # If we have breakpoints, modify interpreter behavior
    if self.breakpoints and self.interactive.program_interpreter:
        self._install_breakpoint_handler()

Breakpoints are only installed when RUN is called. Users might set breakpoints and expect them to work immediately, but they won't take effect until the next RUN command.

---

#### Code vs Comment conflict

**Description:** The cmd_step method shows current position after each step with output like '[{line_num}]', but the docstring doesn't mention this output behavior.

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
Docstring:
"""STEP command - execute one statement and pause.

Executes a single statement (not a full line). If a line contains multiple
statements separated by colons, each statement is executed separately.

This matches the curses UI 'Step Statement' command (Ctrl+T).
Note: The curses UI also has 'Step Line' (Ctrl+K) which executes all
statements on the current line. The CLI STEP command is statement-only.

Usage:
    STEP        - Execute next statement and pause
    STEP n      - Execute n statements
"""

Implementation:
# Show current position
if self.interactive.program_runtime.current_line:
    line_num = self.interactive.program_runtime.current_line.line_number
    self.interactive.io_handler.output(f"[{line_num}]")

The docstring should document that the current line number is displayed after each step.

---

#### code_vs_comment

**Description:** Comment claims line numbers are formatted with fixed 5-char width, but code uses variable width

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Class docstring says:
"Note: Line numbers are formatted with fixed 5-char width for alignment,
but parsing accepts variable width for flexibility."

But _format_line() method uses:
line_num_str = f"{line_num}"
prefix = f"{status}{line_num_str} "

This is variable width, not fixed 5-char width. The comment appears outdated from a refactoring.

---

#### code_vs_comment

**Description:** Comment describes column structure with fixed positions but implementation uses variable width

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In keypress() method, comment says:
"Format: 'S<linenum> CODE' (where <linenum> is variable width)
- Column 0: Status (●, ?, space) - read-only
- Columns 1+: Line number (variable width) - editable"

But later in the same method, there's a check:
"if 1 <= col_in_line <= 6:"

This hardcoded column 6 boundary contradicts the variable width claim. If line numbers are truly variable width, the boundary should be calculated dynamically, not hardcoded to column 6.

---

#### code_vs_comment

**Description:** Comment describes 3-column structure but implementation doesn't enforce column boundaries

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Class docstring says:
"3-column program editor widget for BASIC programs.

Columns:
1. Status (1 char): ● for breakpoint, ? for error, space otherwise
2. Line number (variable width): auto-numbered line numbers
3. Program text (rest): BASIC code"

But the implementation doesn't enforce these as true columns. The line number width varies, and there's no column separator. It's more accurately a formatted string with fields, not a columnar layout.

---

#### code_vs_comment

**Description:** Comment claims interpreter is created once and reused, but code creates it twice in __init__

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~40: '# Create one interpreter for the session - don\'t create multiple!'
But code creates interpreter twice:
1. Line ~67: self.interpreter = Interpreter(self.runtime, immediate_io, limits=create_unlimited_limits())
2. Line ~71: self.immediate_executor = ImmediateExecutor(self.runtime, self.interpreter, immediate_io)
Then in start() method (~line 85), creates ANOTHER ImmediateExecutor with a new OutputCapturingIOHandler, potentially creating confusion about which interpreter/IO handler is active.

---

#### code_vs_comment

**Description:** Comment says 'Create a proper ImmediateExecutor' but then recreates it in start()

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~70: '# Create a proper ImmediateExecutor (will be re-initialized in start() and _run_program())'
This suggests the ImmediateExecutor created in __init__ is temporary/improper, but it's still created. If it's going to be recreated anyway, the __init__ creation seems unnecessary and wasteful.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of main_widget storage and retrieval

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _show_help() (line ~680):
- Stores: main_widget = self.loop.widget
- But never uses it or restores it

In _show_keymap() (line ~695):
- Uses: main_widget = self.main_widget (stored instance variable)
- Stores in: self._keymap_main_widget

In _show_settings() (line ~750):
- Uses: main_widget = self.main_widget (stored instance variable)
- Stores in: self._settings_main_widget

In _activate_menu() (line ~730):
- Uses: main_widget = self.loop.widget.base_widget if hasattr(...)

Inconsistent approach to getting the 'main widget' - sometimes from self.main_widget, sometimes from self.loop.widget, sometimes with base_widget unwrapping.

---

#### code_internal_inconsistency

**Description:** Inconsistent pattern for closing overlays

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
_show_keymap() and _show_settings() both:
1. Check if already open and close if so (toggle behavior)
2. Store overlay in instance variable (_keymap_overlay, _settings_overlay)
3. Store main widget in instance variable

But _show_help():
1. Does NOT check if already open
2. Does NOT store overlay in instance variable
3. Stores main_widget locally but never uses it

This inconsistency means help cannot be toggled like keymap/settings can.

---

#### code_vs_comment

**Description:** Comment says 'RUN = CLEAR + GOTO first line (or start_line if specified)' but code behavior differs

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _setup_program() method around line 1050:
Comment: '# Reset runtime with current program - RUN = CLEAR + GOTO first line (or start_line if specified)'
Comment: '# This preserves breakpoints but clears variables'

However, the code calls runtime.reset_for_run() which clears variables, then later the comment says 'preserves breakpoints' but there's no explicit code to preserve breakpoints. The breakpoints are set AFTER reset via 'for line_num in self.editor.breakpoints: self.interpreter.set_breakpoint(line_num)' which suggests they are NOT preserved by reset_for_run, but rather re-applied.

---

#### code_vs_comment

**Description:** Comment about statement-level precision contradicts actual implementation

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_stack_window() around line 970:
Comment: '# Show statement-level precision for GOSUB return address'
Code: 'return_stmt = entry.get('return_stmt', 0)'
Code: 'line = f"{indent}GOSUB from line {entry['from_line']}.{return_stmt}"'

The comment claims statement-level precision, but the code uses a default of 0 if 'return_stmt' is missing, which may not be accurate. This suggests the precision is not guaranteed.

---

#### code_vs_comment

**Description:** Comment about preserving PC contradicts actual halting behavior

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _sync_program_to_runtime() around line 1290:
Comment: '# Restore PC only if execution is running AND not paused at breakpoint'
Comment: '# (paused programs need PC reset to current breakpoint location)'
Comment: '# Otherwise ensure halted (don't accidentally start execution)'

The comment says 'paused programs need PC reset' but the code doesn't actually reset PC for paused programs - it just ensures halted. The logic is:
if self.running and not self.paused_at_breakpoint:
    # preserve PC
else:
    # set to halted

This doesn't match the comment's claim about resetting PC for paused programs.

---

#### code_vs_comment

**Description:** Comment about 'last accessed cell' contradicts conditional check

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_variables_window() around line 750:
Comment: '# Array: show dimensions and last accessed cell if available'
Code: 'if var.get('last_accessed_subscripts') and var.get('last_accessed_value') is not None:'

The comment says 'if available' but the code checks for both subscripts AND value being not None. However, the value check uses 'is not None' which means a value of 0 or empty string would pass, but the subscripts check uses truthiness which means an empty list would fail. This asymmetry could cause bugs where last_accessed_value exists but last_accessed_subscripts is an empty list.

---

#### code_vs_comment

**Description:** Comment claims immediate mode commands are logged to output pane 'not separate immediate history', but there is no evidence of a separate immediate history feature anywhere in the code

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line comment: '# Log the command to output pane (not separate immediate history)'
This comment implies there was or could be a separate immediate history feature, but no such feature exists in the codebase. The comment is misleading.

---

#### code_vs_comment

**Description:** Comment suggests CapturingIOHandler is duplicated and should be extracted to shared location, but no action is taken

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment: '# (duplicates definition in _run_program - consider extracting to shared location)'

The CapturingIOHandler class is defined inline in _execute_immediate() method, and the comment acknowledges it's a duplicate of code in _run_program. This is a code smell that should be addressed, not just commented.

---

#### code_vs_comment

**Description:** Comment claims InterpreterState is only created if it doesn't exist (first run), but doesn't explain what happens on subsequent runs

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment: '# We only create InterpreterState if it doesn't exist (first run of session),
# which initializes tracking state but doesn't modify PC/runtime state.'

Code:
if not hasattr(self.interpreter, 'state') or self.interpreter.state is None:
    self.interpreter.state = InterpreterState(_interpreter=self.interpreter)

The comment explains first-run behavior but doesn't clarify what happens when state already exists. Does it preserve the old state? Should it be reset? This is unclear.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate says 'This updates self.program but doesn't affect runtime yet', but then immediately syncs to runtime

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment: '# Parse editor content into program (in case user typed lines directly)
# This updates self.program but doesn't affect runtime yet'

But a few lines later:
# Sync program to runtime (but don't reset PC - keep current execution state)
self._sync_program_to_runtime()

The comment says it doesn't affect runtime yet, but then it immediately does affect runtime. The comment is misleading.

---

#### code_vs_comment

**Description:** Comment says 'Execution stack window (menu only - no dedicated key)' but then says 'Note: Ctrl+K is used by step_line, not stack window' which is confusing

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py lines 143-147:
"# Execution stack window (menu only - no dedicated key)
# Note: Ctrl+K is used by step_line, not stack window
STACK_KEY = ''  # No keyboard shortcut
STACK_CHAR = ''
STACK_DISPLAY = 'Menu only'"

The note about Ctrl+K seems to be addressing a potential confusion, but it's unclear why this note is here specifically. It suggests there may have been a previous version where Ctrl+K was considered for stack window.

---

#### code_vs_documentation

**Description:** Help widget footer shows hardcoded keybindings that may not match actual keybindings from JSON config

**Affected files:**
- `src/ui/help_widget.py`
- `src/ui/keybindings.py`

**Details:**
help_widget.py line 59:
"self.footer = urwid.Text(" ↑/↓=Scroll Tab=Next Link Enter=Follow /=Search U=Back ESC/Q=Exit ")"

This hardcodes the keybindings in the footer, but the actual keybindings are loaded from JSON via keybindings.py. If the JSON config changes, this footer will be incorrect. The footer should dynamically use the keybindings from the keybindings module or HelpMacros.

---

#### code_vs_documentation

**Description:** Interactive menu uses keybindings module constants but formats them with fmt_key() function, which may not match the actual display format from JSON

**Affected files:**
- `src/ui/interactive_menu.py`
- `src/ui/keybindings.py`

**Details:**
interactive_menu.py lines 28-31:
"def fmt_key(display):
    '''Convert keybinding display to compact ^X format.'''
    if display.startswith('Ctrl+'):
        return '^' + display[5:]
    return display"

interactive_menu.py lines 33-50 use this to format menu items like:
"(f'New            {fmt_key(kb.NEW_DISPLAY)}', '_new_program')"

However, keybindings.py already provides DISPLAY constants (e.g., NEW_DISPLAY = 'Ctrl+N'). The fmt_key function converts these to '^N' format, but this conversion is hardcoded and assumes the format is always 'Ctrl+X'. If the JSON config uses different formats (e.g., 'Alt+N', 'F5'), this will break.

---

#### code_vs_documentation

**Description:** CONTINUE_KEY is loaded from 'goto_line' action in JSON, but the comment says 'Continue execution (Go)'

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py lines 237-240:
"# Continue execution (Go)
_continue_key = _get_key('editor', 'goto_line') or 'Ctrl+G'
CONTINUE_KEY = _ctrl_key_to_urwid(_continue_key)
CONTINUE_CHAR = _ctrl_key_to_char(_continue_key)
CONTINUE_DISPLAY = _continue_key"

The comment says this is for 'Continue execution (Go)' but it's loading from 'goto_line' action. This suggests either:
1. The JSON config has the wrong action name (should be 'continue' not 'goto_line')
2. The comment is wrong (this is actually for goto_line, not continue)
3. The same key is used for both goto_line and continue in different contexts

---

#### code_vs_comment

**Description:** Comment in _search_indexes says 'Map tier to labels (UI tier handled separately inline, Other is fallback)' but the code shows UI tier is handled in the loop, not separately

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
help_widget.py lines 96-99:
"# Map tier to labels (UI tier handled separately inline, Other is fallback)
tier_labels = {
    'language': '📕 Language',
    'mbasic': '📗 MBASIC',
}"

help_widget.py lines 115-120:
"# Determine tier label from tier field or path
tier_name = file_info.get('tier', '')
if tier_name.startswith('ui/'):
    tier_label = '📘 UI'
else:
    tier_label = tier_labels.get(tier_name, '📙 Other')"

The comment says 'UI tier handled separately inline' which is correct, but it's misleading because it suggests the UI tier is not in the tier_labels dict for a special reason, when actually it's just handled with an if statement. The comment could be clearer.

---

#### code_vs_documentation

**Description:** STATUS_BAR_SHORTCUTS shows '^K step' but LIST_KEY comment says 'Step Line (Ctrl+K)' - inconsistent terminology

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py line 318:
"STATUS_BAR_SHORTCUTS = "MBASIC - ^F help  ^U menu  ^W vars  ^K step  Tab cycle  ^Q quit""

keybindings.py line 169:
"# Step Line (Ctrl+K) - execute all statements on current line"

The status bar says '^K step' but the comment says 'Step Line'. The terminology should be consistent - either both say 'step' or both say 'step line'.

---

#### code_vs_documentation

**Description:** Help browser implements Ctrl+F for in-page search but this keybinding is not documented in tk_keybindings.json

**Affected files:**
- `src/ui/tk_help_browser.py`
- `src/ui/tk_keybindings.json`

**Details:**
tk_help_browser.py line 119-120:
# Make text read-only but allow copy (Ctrl+C) and find (Ctrl+F)
def readonly_key_handler(event):
    # Allow Ctrl+C (copy), Ctrl+A (select all), Ctrl+F (find)
    if event.state & 0x4:  # Control key
        if event.keysym in ('c', 'C', 'a', 'A'):  # Ctrl+C, Ctrl+A
            return  # Allow these
        elif event.keysym in ('f', 'F'):  # Ctrl+F
            self._inpage_search_show()
            return "break"

Line 127:
self.bind("<Control-f>", lambda e: self._inpage_search_show())

tk_keybindings.json has no entry for Ctrl+F in help_browser section

---

#### code_vs_documentation

**Description:** Duplicate entries for same functionality with different keys - 'new_program' and 'file_new' both map to Ctrl+N, 'save_file' and 'file_save' both map to Ctrl+S

**Affected files:**
- `src/ui/tk_keybindings.json`

**Details:**
tk_keybindings.json:
"file_new": {
  "keys": ["Ctrl+N"],
  "primary": "Ctrl+N",
  "description": "New file"
},
"new_program": {
  "keys": ["Ctrl+N"],
  "primary": "Ctrl+N",
  "description": "New file"
}

"file_save": {
  "keys": ["Ctrl+S"],
  "primary": "Ctrl+S",
  "description": "Save file"
},
"save_file": {
  "keys": ["Ctrl+S"],
  "primary": "Ctrl+S",
  "description": "Save file"
}

These appear to be duplicate entries for the same actions with inconsistent naming

---

#### code_internal_inconsistency

**Description:** Inconsistent error handling between _on_apply and _on_cancel methods

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
_on_apply method (lines 193-201):
    try:
        set_setting(key, value, SettingScope.GLOBAL)
    except Exception as e:
        messagebox.showerror(...)
        return False

_on_cancel method (lines 212-218):
    try:
        set_setting(key, value, SettingScope.GLOBAL)
    except Exception:
        pass  # Ignore errors on cancel

The _on_apply method shows error dialogs and stops on first error, while _on_cancel silently ignores all errors. This inconsistency means if settings fail to restore on cancel, the user gets no feedback, potentially leaving settings in an inconsistent state.

---

#### code_vs_comment

**Description:** Comment describes 3-pane layout but implementation shows different structure

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring says: '3-pane vertical layout: editor (top), output (middle), immediate mode (bottom)'

But code shows:
- editor_frame with weight=3
- output_frame with weight=2
- immediate_frame with weight=1

The immediate_frame contains only an input line, not a full pane. The comment '# Bottom pane: Immediate Mode - just the input line (weight=1, ~17% of space)' contradicts the docstring which implies immediate mode is a full pane like editor and output.

---

#### code_vs_comment

**Description:** Incomplete implementation in _edit_simple_variable method

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
The method _edit_simple_variable ends with:

'# Create a token with line=-1 to indicate immediate mode / variable editor
# This token is used by set_variable to track the edit source
class ImmediateModeToken:
    def __init__(self):'

The class definition is incomplete (no body, no usage). The method appears to be cut off mid-implementation. The comment describes what should happen but the code doesn't implement it.

---

#### code_vs_comment

**Description:** Inconsistent handling of statement highlighting after execution

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _menu_step_line and _menu_step methods, there's complex logic to determine whether to highlight a statement after halting:

'# Get statement at PC to check if it's END or steppable
stmt = self.runtime.statement_table.get(pc)
if stmt and stmt.__class__.__name__ == 'EndStatementNode':
    # Stopped at END statement - don't highlight
    ...
else:
    # Paused at steppable statement - highlight it'

But the logic checks for 'EndStatementNode' by string name comparison, which is fragile. If the class is renamed or moved, this breaks silently. Should use isinstance() or a more robust check.

---

#### code_vs_comment

**Description:** Comment about region check contradicts actual check

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_variable_double_click:

Comment: '# Check if we clicked on a row (accept 'tree' for first column or 'cell' for other columns)'

Code: 'if region not in ('cell', 'tree'):'

The comment says 'accept tree for first column or cell for other columns' but the code accepts both for any column. The logic doesn't distinguish between columns as the comment implies.

---

#### code_vs_comment

**Description:** Comment claims default subscripts use array_base, but code has fallback to 0 for invalid array_base

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~95 says:
# If no default subscripts, use first element based on array_base

But code at lines ~97-105 has:
if array_base == 0:
    # OPTION BASE 0: use all zeros
    default_subscripts = ','.join(['0'] * len(dimensions))
elif array_base == 1:
    # OPTION BASE 1: use all ones
    default_subscripts = ','.join(['1'] * len(dimensions))
else:
    # Invalid array_base - default to 0
    default_subscripts = ','.join(['0'] * len(dimensions))

The comment doesn't mention the fallback behavior for invalid array_base values (not 0 or 1).

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of ImmediateModeToken class definition - defined inline twice

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
ImmediateModeToken is defined as an inline class in two different methods:

1. In _edit_simple_variable (around line ~50):
class ImmediateModeToken:
    def __init__(self):
        self.line = -1
        self.position = None

2. In _edit_array_element (around line ~240):
class ImmediateModeToken:
    def __init__(self):
        self.line = -1
        self.position = None

This duplication suggests the class should be defined once at module or class level, not redefined in each method.

---

#### code_vs_comment

**Description:** Comment claims blank lines are removed 'after any modification' but implementation only calls it from _on_enter_key

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment in _remove_blank_lines at line ~1175:
"""Remove all blank lines from the editor (except final line).

Removes blank lines to keep program clean, but preserves the final
line which is always blank in Tk Text widget (internal Tk behavior).
Called after any modification (typing, pasting, etc.)
"""

However, searching the code shows _remove_blank_lines is only called from _on_enter_key (around line ~1220), not after 'any modification'. The comment overstates when this function is invoked.

---

#### code_vs_comment

**Description:** Comment in cmd_cont() mentions fixed bugs but uses incorrect attribute names in the fix description

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment says: '# Fixed: was self.is_running' and '# Fixed: was self._tick()'

But the actual code uses self.running and self._execute_tick(), suggesting either:
1. The comment is describing a previous bug that was already fixed
2. The comment is incorrect about what the bug was

The comment implies these were recent fixes but provides no context about when or why.

---

#### code_vs_comment

**Description:** Comment in _update_immediate_status() describes checking 'both can_execute_immediate() AND self.running flag' but implementation may have race condition

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment says: '# Check if safe to execute - use both can_execute_immediate() AND self.running flag
# The running flag is set False immediately when program stops, even before tick completes'

This suggests the running flag is used to avoid a race condition, but the comment doesn't explain why can_execute_immediate() alone is insufficient, or what specific race condition is being prevented.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate() describes querying interpreter 'directly via has_work()' but this contradicts earlier pattern of checking runtime flags

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment: '# Check if interpreter has work to do (after RUN statement)
# Query interpreter directly via has_work() instead of checking runtime flags'

This suggests a design change from checking runtime flags to using has_work(), but:
1. Earlier in the same method, code checks self.runtime.npc
2. Other methods still check self.running and self.runtime.halted
3. No explanation of why has_work() is preferred or what changed

---

#### code_vs_comment

**Description:** Comment in _smart_insert_line() says 'DON'T save to program yet' but doesn't explain the full lifecycle

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment: '# DON'T save to program yet - the line is blank and would be filtered out
# Just position the cursor on the new line so user can start typing
# The line will be saved when they finish typing and move off it'

This describes a multi-step process but doesn't explain:
1. What triggers the eventual save (which method?)
2. What happens if user never types anything
3. Whether blank numbered lines are always filtered or only in certain contexts

---

#### code_vs_comment

**Description:** Comment in _on_paste() describes 'auto-numbering logic' but the implementation has two different paste behaviors with unclear boundaries

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment: '# Multi-line paste or paste into blank line - use auto-numbering logic'

But earlier code has:
if '\n' not in sanitized_text:
    # Single line paste - check if we're in the middle of an existing line
    ...
    if current_line_text:
        # If current line has content (not blank), do simple inline paste

This creates three cases:
1. Single line paste into line with content (simple paste)
2. Single line paste into blank line (auto-numbering)
3. Multi-line paste (auto-numbering)

The comment only describes case 3, making the full logic unclear.

---

#### code_vs_comment

**Description:** Comment in _add_immediate_output method is misleading about its purpose

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Method docstring says: "Add text to main output pane (immediate mode has no history widget)."
However, the method name is _add_immediate_output which suggests it should add to immediate output, not main output. The comment in parentheses suggests immediate mode doesn't have a history widget, but the code shows immediate_history widget exists elsewhere in the file (used in _setup_immediate_context_menu, _copy_immediate_selection, _select_all_immediate).

---

#### documentation_inconsistency

**Description:** Inconsistent documentation about input methods between input() and input_line()

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
TkIOHandler.input() docstring: "Input from user via inline input field."
TkIOHandler.input_line() docstring: "Unlike input(), always uses modal dialog (not inline input field)."
However, input() has fallback code that uses simpledialog.askstring (modal dialog) when backend is not available. The documentation doesn't mention this fallback behavior, making the distinction between input() and input_line() unclear in all cases.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of immediate_history widget existence

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
The _add_immediate_output method docstring claims "immediate mode has no history widget", but multiple methods reference self.immediate_history:
- _setup_immediate_context_menu() binds to self.immediate_history
- _copy_immediate_selection() uses self.immediate_history.get()
- _select_all_immediate() uses self.immediate_history.tag_add()
This suggests immediate_history widget does exist, contradicting the comment in _add_immediate_output.

---

#### code_vs_comment

**Description:** Docstring states line numbers should be part of text content (not drawn separately) and requires Phase 2 refactoring, but code actually parses line numbers from text content already

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Class docstring says:
"Note: Line numbers should be part of the text content (not drawn separately).
This requires Phase 2 refactoring to integrate line numbers into text."

But _redraw() method comment says:
"Note: Line numbers are no longer drawn in canvas - they should be
part of the text content itself (Phase 2 of editor refactoring)."

However, the code already implements this - _parse_line_number() extracts BASIC line numbers from text content, and _redraw() uses this parsed number. The implementation already treats line numbers as part of text content, not drawn separately.

---

#### code_vs_comment

**Description:** Status click handler docstring says it handles breakpoint toggling, but implementation only shows info messages without toggling

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Method docstring:
"Handle click on status column (show error for ?, breakpoint info for ●)."

And the info message says:
"Click the ● again to toggle it off."

But the _on_status_click() method only displays messagebox.showinfo() or messagebox.showerror() - it does not actually toggle breakpoints. There is no code to call set_breakpoint() or modify line_metadata to toggle the breakpoint state.

---

#### code_vs_comment

**Description:** _parse_line_number regex comment says 'Whitespace or end of string' but regex allows both simultaneously

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment in _parse_line_number():
match = re.match(r'^(\d+)(?:\s|$)', line_text)  # Whitespace or end of string

The regex pattern '(?:\s|$)' means 'whitespace OR end of string', which is correct. However, the comment could be misread as requiring one or the other exclusively. The regex will match '10 PRINT' (whitespace after number) and '10' (end of string after number), which is the intended behavior. The comment is technically accurate but could be clearer about the 'or' relationship.

---

#### code_vs_documentation

**Description:** Function update_line_references() documentation claims it handles ON...GOTO/GOSUB but the regex pattern is incomplete and may not correctly parse complex ON expressions

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring says: "Update GOTO/GOSUB/THEN/ELSE line number references in code."

Regex pattern: r'\b(GOTO|GOSUB|THEN|ELSE|ON\s+[^G]+\s+GOTO|ON\s+[^G]+\s+GOSUB)\s+(\d+)'

The pattern 'ON\s+[^G]+\s+GOTO' uses [^G]+ which matches any character except 'G'. This will fail if the expression contains the letter 'G', such as:
- ON G GOTO 10,20
- ON FLAG GOTO 10,20
- ON SGN(X) GOTO 10,20

The pattern should use a more robust expression matcher.

---

#### code_vs_documentation

**Description:** Function serialize_variable() has logic for 'explicit_type_suffix' attribute but this attribute is not documented and may not be set by parser

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Code at line ~1050:
if var.type_suffix and getattr(var, 'explicit_type_suffix', False):
    text += var.type_suffix

Comment says: "Only add type suffix if it was explicit in the original source. Don't add suffixes that were inferred from DEF statements"

However, there's no documentation about when/how 'explicit_type_suffix' is set on VariableNode objects. If the parser doesn't set this attribute, the getattr() will always return False and type suffixes will never be serialized, which could cause data loss during RENUM.

---

#### code_vs_documentation

**Description:** Function renum_program() documentation says it updates GOTO/GOSUB references via callback, but the callback responsibility is unclear about which statement types need handling

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring says:
"renum_callback: Function that takes (stmt, line_map) to update statement references. Called for ALL statements; callback is responsible for identifying and updating statements with line number references (GOTO, GOSUB, ON GOTO, ON GOSUB, IF THEN/ELSE line numbers)"

This lists specific statement types but doesn't mention:
- RESTORE (if implemented)
- RESUME (if implemented)
- Other potential line-number-referencing statements

The documentation should either be exhaustive or say 'including but not limited to' to avoid confusion.

---

#### code_vs_documentation

**Description:** Docstring claims Runtime accesses program.line_asts directly, but code shows Runtime is initialized with program.line_asts and program.lines as separate parameters

**Affected files:**
- `src/ui/visual.py`

**Details:**
Comment in cmd_run() says:
"# (Runtime accesses program.line_asts directly, no need for program_ast variable)"

But the actual code is:
"self.runtime = Runtime(self.program.line_asts, self.program.lines)"

This suggests Runtime receives line_asts and lines as constructor parameters, not accessing them directly from program object.

---

#### code_vs_comment

**Description:** Missing assignment of program_manager to self.program in __init__ method

**Affected files:**
- `src/ui/visual.py`

**Details:**
The __init__ docstring and class docstring reference 'self.program' throughout:
"Args:
    program_manager: ProgramManager instance"

And usage examples show:
"self.program.add_line(line_num, text)"
"self.program.get_lines()"
"self.program.clear()"

But the __init__ method only shows:
"super().__init__(io_handler, program_manager)"
"self.runtime = None"
"self.interpreter = None"

There's no visible 'self.program = program_manager' assignment, suggesting it might be done in the parent UIBackend class, but this is not documented.

---

#### code_vs_comment

**Description:** Comment says 'Don't print prompt here' but doesn't explain why or where prompt IS printed

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In SimpleWebIOHandler.input() method (line 61):
Comment: '# Don't print prompt here - _enable_inline_input will add it'
This references a method _enable_inline_input that is not shown in the provided code. The comment assumes knowledge of implementation details not visible in this file, making it unclear where the prompt actually gets displayed.

---

#### code_internal_inconsistency

**Description:** VariablesDialog references 'src.ui.variable_sorting' module but doesn't import it at module level

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In VariablesDialog.show() method (line 149) and _cycle_mode() method (line 141):
```
from src.ui.variable_sorting import sort_variables, get_sort_mode_label, cycle_sort_mode
```
And in _cycle_mode():
```
from src.ui.variable_sorting import cycle_sort_mode, get_default_reverse_for_mode
```
These imports are done inside methods rather than at the module level. While this works, it's inconsistent with the module-level imports at the top of the file (lines 6-15) and could cause performance issues if these methods are called frequently.

---

#### code_vs_comment

**Description:** Comment says 'Make output textarea editable when input needed' but code makes it readonly

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~142: Comment says '# INPUT handling: Make output textarea editable when input needed'
But in _menu_stop() around line ~1088, code explicitly makes it readonly:
self.output.run_method('''() => {
    const el = this.$el.querySelector('textarea');
    if (el) {
        el.setAttribute('readonly', 'readonly');
    }
}''')
The output textarea is created with 'readonly' prop at line ~139.

---

#### code_vs_comment

**Description:** Docstring says RUN clears output but code explicitly doesn't clear output

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~1103 in _menu_run() docstring: 'RUN is always valid - it's just CLEAR + GOTO first line.'
But line ~1131 has comment: '# Don't clear output - continuous scrolling like ASR33 teletype'
The code does NOT call self._clear_output() before running, contradicting the 'CLEAR' part of the docstring.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of empty program between RUN and STEP commands

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_menu_run() line ~1148: 'if not self.program.lines:
    self._set_status('Ready')
    self.running = False
    return'

_menu_step_line() line ~1276: 'if not self.program.lines:
    self._set_status('Ready')
    return'

_menu_step_stmt() line ~1330: 'if not self.program.lines:
    self._set_status('Ready')
    return'

RUN sets self.running = False, but STEP commands don't. This could leave running state inconsistent.

---

#### code_internal_inconsistency

**Description:** Inconsistent breakpoint storage types: PC objects vs plain integers

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_toggle_breakpoint() line ~569: 'pc = PC(line_num, stmt_offset)'
Line ~577: 'if pc in self.runtime.breakpoints:'

_update_breakpoint_display() line ~603: 'for item in self.runtime.breakpoints:
    if isinstance(item, PC):
        ...
    else:
        # Plain integer - highlight whole line'

The code handles both PC objects and plain integers in breakpoints set, but _toggle_breakpoint only creates PC objects. This suggests mixed types are possible but unclear when integers are added.

---

#### code_internal_inconsistency

**Description:** Inconsistent timer cancellation patterns

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_menu_run() line ~1107: 'if self.exec_timer:
    self.exec_timer.cancel()
    self.exec_timer = None'

_menu_stop() line ~1082: 'if self.exec_timer:
    self.exec_timer.cancel()
    self.exec_timer = None'

_execute_tick() line ~1247: 'if self.exec_timer:
    self.exec_timer.cancel()
    self.exec_timer = None'

But in _menu_continue() line ~1449, timer is started without checking if one already exists:
'if not self.exec_timer:
    self.exec_timer = ui.timer(0.01, self._execute_tick, once=False)'

This could lead to multiple timers running if continue is called multiple times.

---

#### code_vs_comment

**Description:** Comment about Ctrl+C handling describes behavior not implemented in this method

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~1177-1185 in _execute_tick() has extensive comment about Ctrl+C handling:
'Note on Ctrl+C handling:
This method is called every 10ms by ui.timer()...
The KeyboardInterrupt handling is done at the top level in mbasic...'

But _execute_tick() has no Ctrl+C or KeyboardInterrupt handling code. The comment describes external behavior, making it unclear why it's in this method's docstring.

---

#### code_vs_comment

**Description:** Comment claims _sync_program_to_runtime preserves PC conditionally, but code always checks exec_timer state

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Docstring says: 'Preserves current PC/execution state only if exec_timer is active; otherwise resets PC to halted.'

But the code logic:
1. Always saves old_pc and old_halted
2. Rebuilds statement table
3. Only restores if exec_timer is active
4. Otherwise sets PC to halted

This matches the docstring, but the comment 'Preserve current PC if it's valid (execution in progress)' is misleading - it's not about validity, it's about whether exec_timer is active.

---

#### code_vs_comment

**Description:** Inconsistent handling of input futures - both interpreter.provide_input() and input_future.set_result() are called

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _handle_output_enter():
```
# Provide input to interpreter
if self.interpreter and self.interpreter.state.input_prompt:
    self.interpreter.provide_input(user_input)

# Also handle async input futures for compatibility
if self.input_future and not self.input_future.done():
    self.input_future.set_result(user_input)
```

Comment says 'for compatibility' but it's unclear which path is primary. The _get_input() method returns empty string and relies on interpreter state transitions, while _get_input_async() uses futures. This dual approach may cause confusion.

---

#### code_vs_comment

**Description:** Docstring for _check_auto_number says 'Only auto-numbers a line once' but implementation checks multiple conditions

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Docstring: 'Only auto-numbers a line once - tracks the last snapshot to avoid re-numbering lines while user is still typing on them.'

But the code has complex logic:
```
if stripped and (i < len(old_lines) or len(lines) > len(old_lines)):
    old_line = old_lines[i] if i < len(old_lines) else ''
    if not re.match(r'^\s*\d+', old_line):
        # Line wasn't numbered before, number it now
```

The 'once' behavior depends on: line existed in old snapshot OR more lines now, AND old line wasn't numbered. This is more nuanced than 'once'.

---

#### internal_inconsistency

**Description:** Multiple methods handle editor changes with overlapping responsibilities

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_on_editor_change() is described as 'This replaces the old keyup and paste handlers' but _on_key_released(), _on_paste(), _on_editor_click(), and _on_editor_blur() still exist and are presumably still connected. This creates potential for duplicate processing or race conditions. The comment suggests a refactoring that may not be complete.

---

#### code_vs_comment

**Description:** Inconsistent approach to preventing execution start - comment says 'don't accidentally start execution' but code checks exec_timer.active

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _sync_program_to_runtime():
```
if self.exec_timer and self.exec_timer.active:
    # Timer is running - preserve execution state
    self.runtime.pc = old_pc
    self.runtime.halted = old_halted
else:
    # No execution in progress - ensure halted
    self.runtime.pc = PC.halted_pc()
    self.runtime.halted = True
```

Comment says 'don't accidentally start execution' but the code is checking if execution is ALREADY running (exec_timer.active). The logic is about preserving vs resetting state, not preventing accidental starts. The comment is misleading about what the code does.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut documentation for toggling breakpoints

**Affected files:**
- `docs/help/common/debugging.md`
- `docs/help/common/editor-commands.md`

**Details:**
debugging.md states 'position cursor on the line and press **Ctrl+B**' for Tk UI, but editor-commands.md does not list Ctrl+B in the Editing Commands or Program Commands sections. The debugging.md file also mentions 'b' for Curses UI but editor-commands.md doesn't document this either.

---

#### documentation_inconsistency

**Description:** Missing debugging commands in editor-commands.md

**Affected files:**
- `docs/help/common/debugging.md`
- `docs/help/common/editor-commands.md`

**Details:**
editor-commands.md has a 'Debugging Commands' section that says 'For debugging-specific commands like breakpoints and stepping, see [Debugging Features](debugging.md)' but doesn't list any of the key debugging shortcuts like Ctrl+R (Run), Ctrl+T (Step), Ctrl+G (Continue), Ctrl+Q (Stop), Ctrl+V (Variables), Ctrl+K (Stack) that are documented in debugging.md.

---

#### code_vs_documentation

**Description:** Settings dialog implementation doesn't match debugging documentation claims

**Affected files:**
- `src/ui/web/web_settings_dialog.py`
- `docs/help/common/debugging.md`

**Details:**
web_settings_dialog.py only implements editor settings (auto-numbering) and read-only limits settings. However, debugging.md extensively documents debugging features like breakpoints, stepping, variables window, and execution stack window, but there's no settings UI for configuring these debugging features (e.g., breakpoint colors, step behavior, etc.).

---

#### documentation_inconsistency

**Description:** Run program shortcut inconsistency

**Affected files:**
- `docs/help/common/debugging.md`
- `docs/help/common/editor-commands.md`

**Details:**
debugging.md states 'Shortcuts: Tk/Curses/Web: **Ctrl+T** or Step button' for stepping, but editor-commands.md shows '**F2** | **Ctrl+R** | Run program' and doesn't mention Ctrl+T at all. Additionally, debugging.md uses Ctrl+R for Run but editor-commands.md shows F2 as primary.

---

#### documentation_inconsistency

**Description:** ASCII codes documentation references non-existent 'Appendix M' in error-codes.md

**Affected files:**
- `docs/help/common/language/appendices/ascii-codes.md`
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
In error-codes.md, the ASC function description states: 'Returns a numerical value that is the ASCII code of the first character of the string X$. (See Appendix M for ASCII codes.)'

However, the ASCII codes are documented in 'docs/help/common/language/appendices/ascii-codes.md', not 'Appendix M'. This reference appears to be from an older manual format.

---

#### documentation_inconsistency

**Description:** Mathematical constants have inconsistent precision values

**Affected files:**
- `docs/help/common/language/appendices/math-functions.md`

**Details:**
In math-functions.md, the constants section shows:
'PI = 3.141592653589793   ' Use ATN(1) * 4 for pi
E = 2.718281828459045    ' Use EXP(1) for e'

However, the precision shown (16-17 digits) suggests double precision, but the comment for PI says 'Use ATN(1) * 4' which would be calculated in single precision (7 digits) according to the ATN function documentation that states 'the evaluation of ATN is always performed in single precision'.

---

#### documentation_inconsistency

**Description:** ASC function documentation references 'Appendix M' instead of actual ASCII codes location

**Affected files:**
- `docs/help/common/language/functions/asc.md`
- `docs/help/common/language/appendices/ascii-codes.md`

**Details:**
In asc.md: 'Returns a numerical value that is the ASCII code of the first character of the string X$. (See Appendix M for ASCII codes.)'

The actual ASCII codes are in 'docs/help/common/language/appendices/ascii-codes.md', not 'Appendix M'. This appears to be a legacy reference from printed manual format.

---

#### documentation_inconsistency

**Description:** Inconsistent precision ranges for floating-point types

**Affected files:**
- `docs/help/common/language/data-types.md`
- `docs/help/common/language/functions/cdbl.md`
- `docs/help/common/language/functions/csng.md`

**Details:**
In data-types.md:
'SINGLE: ±10^-38 to ±10^38, ~7 digits'
'DOUBLE: ±10^-308 to ±10^308, ~16 digits'

In cdbl.md:
'Double-precision numbers have approximately 16 digits of precision and range from 2.938735877055719 x 10^-39 to 1.701411834604692 x 10^38.'

In csng.md:
'Single-precision numbers have approximately 7 digits of precision and range from 2.938736 x 10^-39 to 1.701412 x 10^38.'

The ranges in cdbl.md and csng.md are much more restrictive than stated in data-types.md (10^38 vs 10^308 for double, and the minimum values differ).

---

#### documentation_inconsistency

**Description:** Index describes error handling features not fully documented in error-codes.md

**Affected files:**
- `docs/help/common/language/appendices/index.md`
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
In index.md, the error codes section claims to include:
'- Error handling examples'

However, error-codes.md only has one basic example at the end. The index promises more comprehensive error handling examples that aren't present.

---

#### documentation_inconsistency

**Description:** LPOS implementation note says it returns 0, but doesn't clarify if this is for all calls or just when no printer exists

**Affected files:**
- `docs/help/common/language/functions/lpos.md`

**Details:**
Implementation note states: 'Function always returns 0'

But the original description says it 'Returns the current position of the line printer print head within the line printer buffer.'

Should clarify that 0 is returned because the feature is not implemented, not because position is 0.

---

#### documentation_inconsistency

**Description:** PEEK implementation note says it returns random values but doesn't clarify relationship with POKE

**Affected files:**
- `docs/help/common/language/functions/peek.md`

**Details:**
Implementation note states: 'PEEK does NOT return values written by POKE (POKE is a no-op)'

But the original description says: 'PEEK is traditionally the complementary function to the POKE statement.'

This contradiction should be more prominently highlighted at the top of the doc.

---

#### documentation_inconsistency

**Description:** Function count mismatch in language reference index

**Affected files:**
- `docs/help/common/language/index.md`
- `docs/help/common/language/functions/index.md`

**Details:**
The language index states:
"[Functions](functions/index.md) - 40 intrinsic functions"

This specific count (40) should be verified against the actual number of documented functions. If the count is incorrect or changes, it creates an inconsistency.

---

#### documentation_inconsistency

**Description:** Statement count mismatch in language reference index

**Affected files:**
- `docs/help/common/language/index.md`
- `docs/help/common/language/statements/index.md`

**Details:**
The language index states:
"[Statements](statements/index.md) - 63 commands and statements"

This specific count (63) should be verified against the actual number of documented statements. If the count is incorrect or changes, it creates an inconsistency.

---

#### documentation_inconsistency

**Description:** Contradictory information about CLEAR parameter meanings across BASIC-80 versions

**Affected files:**
- `docs/help/common/language/statements/clear.md`

**Details:**
The CLEAR documentation states:
"**Note about string space:** In BASIC-80 release 5.0 and later (including MBASIC 5.21), string space is allocated dynamically...

**Historical note:** In earlier versions of BASIC-80, expression1 set the amount of string space and expression2 set the end of memory. This behavior changed in release 5.0."

But the Parameters section states:
"- **expression1**: If specified, sets the highest memory location available for BASIC to use
- **expression2**: Sets the stack space reserved for BASIC"

This creates confusion about what expression1 actually does in version 5.21 - does it set memory end or is it ignored due to dynamic string allocation?

---

#### documentation_inconsistency

**Description:** END statement documentation contradicts CONT behavior with END vs ERROR statement

**Affected files:**
- `docs/help/common/language/statements/end.md`
- `docs/help/common/language/statements/error.md`

**Details:**
end.md states: 'CONT - To continue program execution after a Control-C has been typed, or a STOP or END statement has been executed'

This suggests CONT can resume after END, but END.md also states: 'Unlike the STOP statement, END closes all open files and does not cause a BREAK message to be printed' and 'BASIC-80 always returns to command level after an END is executed'

The contradiction is whether END allows CONT to resume execution or not. STOP allows CONT, but END's behavior is unclear.

---

#### documentation_inconsistency

**Description:** Inconsistent information about when ERR is reset to 0

**Affected files:**
- `docs/help/common/language/statements/err-erl-variables.md`
- `docs/help/common/language/statements/error.md`

**Details:**
err-erl-variables.md states:
'ERR is reset to 0 when:
  - RESUME statement is executed
  - A new RUN command is issued
  - An error handling routine ends normally'

However, error.md states:
'ERR variable will contain the error code'

But doesn't clarify if ERROR statement resets previous ERR value or if it persists. The interaction between ERROR statement and ERR variable lifecycle needs clarification.

---

#### documentation_inconsistency

**Description:** Inconsistent file extension handling documentation

**Affected files:**
- `docs/help/common/language/statements/files.md`
- `docs/help/common/language/statements/kill.md`
- `docs/help/common/language/statements/load.md`

**Details:**
load.md states:
'(With CP/M, the default extension .BAS is supplied.)'

merge.md states:
'(With CP/M, the default extension .BAS is supplied.)'

But files.md doesn't mention default extensions at all when discussing filespec. The documentation should consistently explain when .BAS is automatically added.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation of semicolon behavior after INPUT

**Affected files:**
- `docs/help/common/language/statements/input.md`
- `docs/help/common/language/statements/line-input.md`

**Details:**
input.md states:
'The semicolon after INPUT suppresses the carriage return after the user presses Enter'

line-input.md states:
'If LINE INPUT is immediately followed by a semicolon, then the carriage return typed by the user to end the input line does not echo a carriage return/line feed sequence at the terminal.'

Both describe semicolon suppressing CR/LF but use different terminology. Should be consistent.

---

#### documentation_inconsistency

**Description:** KILL error message inconsistency

**Affected files:**
- `docs/help/common/language/statements/kill.md`
- `docs/help/common/language/statements/open.md`

**Details:**
kill.md states:
'If a KILL statement is given for a file that is currently OPEN, a RFile already open R error occurs.'

The error message format 'RFile already open R' appears to have formatting issues (R at beginning and end). Should clarify the actual error message text.

---

#### documentation_inconsistency

**Description:** MERGE and LOAD have different behaviors regarding open files but documentation is unclear

**Affected files:**
- `docs/help/common/language/statements/merge.md`
- `docs/help/common/language/statements/load.md`

**Details:**
load.md states:
'LOAD closes all open files and deletes all variables and program lines currently residing in memory before it loads the designated program. However, if the nRn option is used with LOAD, the program is RUN after it is LOADed, and all open data files are kept open.'

merge.md doesn't mention what happens to open files during MERGE. Should clarify if MERGE closes files or keeps them open.

---

#### documentation_inconsistency

**Description:** ON ERROR GOTO documentation has incomplete See Also section

**Affected files:**
- `docs/help/common/language/statements/on-error-goto.md`

**Details:**
The See Also section references 'ERR/ERL' as 'err-erl-variables.md' but the actual file path should be '../functions/err-erl.md' or similar based on the pattern in other files. The link format is inconsistent.

---

#### documentation_inconsistency

**Description:** RENUM documentation has version inconsistency

**Affected files:**
- `docs/help/common/language/statements/renum.md`

**Details:**
The RENUM documentation does not specify which versions support it (no 'Versions:' line in syntax section), but it's described as a modern editing feature. Other statements clearly indicate '8K, Extended, Disk' or 'Disk' versions. This should be clarified.

---

#### documentation_inconsistency

**Description:** SETSETTING marked as MBASIC Extension but not in original

**Affected files:**
- `docs/help/common/language/statements/setsetting.md`

**Details:**
The documentation states 'Versions: MBASIC Extension' and 'This is a modern extension not present in original MBASIC 5.21'. This is inconsistent with the documentation set which appears to be for MBASIC 5.21. Modern extensions should be clearly separated or marked differently throughout.

---

#### documentation_inconsistency

**Description:** SHOWSETTINGS documentation mentions HELPSETTING statement that doesn't exist in settings.md

**Affected files:**
- `docs/help/common/language/statements/showsettings.md`
- `docs/help/common/settings.md`

**Details:**
showsettings.md lists 'HELPSETTING' in 'See Also' section and describes it as 'Display help for a specific setting', but this statement is not documented in settings.md or anywhere else in the documentation. The settings.md file only mentions SHOWSETTINGS and SETSETTING commands.

---

#### documentation_inconsistency

**Description:** Variable name significance behavior documented differently

**Affected files:**
- `docs/help/common/language/variables.md`
- `docs/help/common/settings.md`

**Details:**
variables.md states: 'In the original MBASIC 5.21, only the first 2 characters of variable names were significant (AB, ABC, and ABCDEF would be the same variable). This Python implementation uses the full variable name for identification, allowing distinct variables like COUNT and COUNTER. The case handling is configurable via the `variables.case_conflict` setting.'

However, settings.md describes variables.case_conflict as handling 'case conflicts' not 'name significance'. The setting choices (first_wins, error, prefer_upper, prefer_lower, prefer_mixed) all relate to case handling, not to whether full names or first-2-chars are significant.

---

#### documentation_inconsistency

**Description:** Settings commands documented in settings.md but not in CLI index

**Affected files:**
- `docs/help/common/settings.md`
- `docs/help/common/ui/cli/index.md`

**Details:**
settings.md shows CLI commands:
```basic
SHOWSETTINGS                    ' Show all settings
SHOWSETTINGS editor             ' Show editor settings only
SETSETTING editor.auto_number_step 100   ' Change a setting
```

However, ui/cli/index.md does not mention SHOWSETTINGS or SETSETTING in its 'Common Commands' table, which lists RUN, LIST, NEW, SAVE, LOAD, RENUM, AUTO, SYSTEM. The CLI documentation should reference these settings commands.

---

#### documentation_inconsistency

**Description:** Broken link in main index to getting-started.md

**Affected files:**
- `docs/help/index.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
index.md has a link '[Getting Started](mbasic/getting-started.md)' in the 'About MBASIC 5.21' section.

However, in the 'Most Commonly Searched' section at the bottom, there's also a reference to getting started but the path structure suggests it should be under common: 'For more details, see [About MBASIC](mbasic/index.md).' but earlier references show '[Getting Started](../../getting-started.md)' in other files like ui/tk/index.md, suggesting the file might be at common/getting-started.md not mbasic/getting-started.md.

---

#### documentation_inconsistency

**Description:** Settings documentation references UI-specific pages that may not exist

**Affected files:**
- `docs/help/common/settings.md`

**Details:**
settings.md has a section 'Accessing Settings by UI' that references:
- [CLI Settings Commands](../ui/cli/settings.md)
- [Curses Settings Widget](../ui/curses/settings.md)
- [Tk Settings Dialog](../ui/tk/settings.md)
- [Web Settings Dialog](../ui/web/settings.md)

However, none of these specific settings documentation files are provided in the documentation set. Only index files exist for these UIs (ui/cli/index.md, ui/tk/index.md, ui/curses/editing.md).

---

#### documentation_inconsistency

**Description:** Inconsistent naming of the project

**Affected files:**
- `docs/help/mbasic/extensions.md`
- `docs/help/mbasic/features.md`

**Details:**
extensions.md states: "This is **MBASIC-2025**, a modern implementation of Microsoft BASIC-80 5.21" and lists multiple project names under consideration:
- MBASIC-2025 (emphasizes the modern update)
- Visual MBASIC 5.21 (emphasizes the multiple UIs)
- MBASIC++ (emphasizes extensions)
- MBASIC-X (extended MBASIC)

However, features.md and other documents consistently refer to it as "MBASIC interpreter" or "this MBASIC interpreter" without the -2025 suffix. The project name should be consistent across all documentation.

---

#### documentation_inconsistency

**Description:** Contradictory information about Web UI filesystem capabilities

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/extensions.md`

**Details:**
compatibility.md states about Web UI: "Files stored in browser memory (not browser localStorage)" and "Files persist only during browser session"

However, extensions.md states about Web UI: "Auto-save - Automatic saving to browser storage"

These statements contradict each other - if files are only in memory and not in localStorage, then auto-save to browser storage is not possible. Need clarification on whether Web UI uses localStorage or only memory.

---

#### documentation_inconsistency

**Description:** Inconsistent information about WIDTH statement support

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/features.md`

**Details:**
compatibility.md states: "WIDTH is parsed for compatibility but performs no operation. Terminal width is controlled by the UI or OS. The 'WIDTH LPRINT' syntax is not supported."

features.md does not mention WIDTH statement at all in its comprehensive feature list, despite it being parsed and accepted.

If WIDTH is accepted (even as a no-op), it should be documented in the features list for completeness.

---

#### documentation_inconsistency

**Description:** Inconsistent information about debugging command availability

**Affected files:**
- `docs/help/mbasic/extensions.md`
- `docs/help/mbasic/features.md`

**Details:**
extensions.md states for BREAK, STEP, STACK commands: "Availability: CLI (command form), Curses (Ctrl+B), Tk (UI controls)"

features.md under Debugging section lists: "Breakpoints - Set/clear breakpoints (UI-dependent)" and "Step execution - Execute one line at a time (UI-dependent)" and "Stack viewer - View call stack (UI-dependent)"

The features.md description is vague about which UIs support which features, while extensions.md is specific. These should be consistent - either both should be specific or both should note UI-dependency generally.

---

#### documentation_inconsistency

**Description:** Inconsistent command for running MBASIC

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
features.md implies the command is: "mbasic" (lowercase, no extension)

However, getting-started.md shows: "mbasic" in examples but the actual Python invocation would typically be "python3 mbasic" or "./mbasic" depending on setup.

The installation section in getting-started.md shows "# Run MBASIC" followed by "mbasic" but doesn't explain if this requires adding to PATH, creating a symlink, or using a shell script. This could confuse users.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut documentation for Delete Lines

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/editing.md`

**Details:**
feature-reference.md states 'Delete Lines (Ctrl+D)' under File Operations, but editing.md does not mention Ctrl+D for deleting lines. Instead, editing.md describes manual deletion by removing text and pressing Enter, or typing just the line number. The Ctrl+D shortcut is not documented in the editing guide.

---

#### documentation_inconsistency

**Description:** Variables Window availability inconsistency

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/cli/variables.md`

**Details:**
curses/feature-reference.md documents 'Variables Window (Ctrl+W)' as a feature of Curses UI. However, cli/variables.md states 'The CLI does not have a Variables Window feature' and lists Curses UI as having this feature. This is consistent, but the CLI docs also say 'For visual variable inspection, use: Curses UI - Full-screen terminal with Variables Window (Ctrl+W)' which confirms Curses has it. No inconsistency here actually - both agree Curses has it and CLI doesn't.

---

#### documentation_inconsistency

**Description:** Cut/Copy/Paste keyboard shortcut conflict

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
feature-reference.md states 'Cut/Copy/Paste (Not implemented)' and explains 'Note: Ctrl+X is used for Stop/Interrupt, Ctrl+C exits the program, and Ctrl+V is used for Save.' However, earlier in the same document under File Operations, it states 'Save File (Ctrl+V)' with the note 'Uses Ctrl+V because Ctrl+S is reserved for terminal flow control.' This is consistent within the doc, but the explanation about why standard clipboard shortcuts aren't available could be clearer about the conflict.

---

#### documentation_inconsistency

**Description:** STEP INTO/OVER implementation status unclear

**Affected files:**
- `docs/help/mbasic/not-implemented.md`
- `docs/help/ui/cli/debugging.md`

**Details:**
cli/debugging.md documents 'STEP INTO' and 'STEP OVER' as part of the STEP command syntax ('STEP INTO - Step into subroutines' and 'STEP OVER - Step over subroutine calls'), but then in the Limitations section states 'STEP INTO/OVER not yet implemented (use STEP)'. This is contradictory - the syntax is documented as if it works, but then marked as not implemented.

---

#### documentation_inconsistency

**Description:** Placeholder documentation marked as in progress

**Affected files:**
- `docs/help/ui/common/running.md`

**Details:**
running.md is marked as 'PLACEHOLDER - Documentation in progress' and only provides minimal information. However, this is referenced from multiple other documentation files as if it were complete. Users following links will find incomplete documentation.

---

#### documentation_inconsistency

**Description:** Variable editing capability inconsistency

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
feature-reference.md lists 'Edit Variable Value (Limited - Not fully implemented)' and states 'Variable editing is currently limited in Curses UI. You cannot directly edit values in the variables window.' This suggests some editing capability exists but is limited, but then says you cannot edit at all and must use immediate mode commands instead. The 'Limited' designation is misleading if no editing is possible.

---

#### documentation_inconsistency

**Description:** Inconsistent help keyboard shortcut documentation

**Affected files:**
- `docs/help/ui/curses/quick-reference.md`
- `docs/help/ui/curses/getting-started.md`

**Details:**
quick-reference.md states: '**Ctrl+Q** | Quit' and '**Ctrl+U** | Show menu' and '**^F** (Ctrl+F) | Help (with search)'

getting-started.md states: '- **^F** (Ctrl+F) - Help (you're here now!)' and '- **Ctrl+P** to open help'

There's a conflict: is help opened with Ctrl+F or Ctrl+P? Both are mentioned in different documents.

---

#### documentation_inconsistency

**Description:** Inconsistent search keyboard shortcut

**Affected files:**
- `docs/help/ui/curses/help-navigation.md`
- `docs/help/ui/curses/index.md`

**Details:**
help-navigation.md shows search key as: '**{{kbd:search}}** | Open search prompt'

index.md states: 'Press **/** to search across all help content'

The kbd:search placeholder is not resolved to an actual key, and index.md uses '/' which may be different.

---

#### documentation_inconsistency

**Description:** Inconsistent back/quit navigation keys

**Affected files:**
- `docs/help/ui/curses/help-navigation.md`
- `docs/help/ui/curses/index.md`

**Details:**
help-navigation.md shows: '**{{kbd:back}}** | Go back to previous topic' and '**{{kbd:quit}}** | Exit help, return to editor'

index.md shows: '**U** | Go back to previous page' and '**ESC** or **Q** | Close help and return to editor'

The kbd placeholders don't match the actual keys documented in index.md (U for back, ESC/Q for quit).

---

#### documentation_inconsistency

**Description:** Inconsistent filter options documentation

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
variables.md states: 'Press `f` to cycle through filters: - **All**: Show all variables - **Scalars**: Hide arrays - **Arrays**: Show only arrays - **Modified**: Show recently changed'

quick-reference.md states: '**f** | Filter variables (All/Scalars/Arrays/Modified)'

While these match, the quick-reference format suggests these are the only options, but doesn't clarify if it cycles or if there's a different interaction model.

---

#### documentation_inconsistency

**Description:** Inconsistent Find keyboard shortcut documentation

**Affected files:**
- `docs/help/ui/tk/features.md`
- `docs/help/ui/tk/feature-reference.md`

**Details:**
features.md states: '**Find text (Ctrl+F):** - Opens Find dialog with search options'

feature-reference.md states: '### Find/Replace (Ctrl+F / Ctrl+H)' and later 'Find: Ctrl+F'

While both agree on Ctrl+F for Find, the feature-reference.md combines Find and Replace in one section header which could cause confusion about whether Ctrl+F opens both or just Find.

---

#### documentation_inconsistency

**Description:** Settings keyboard shortcut not documented in quick reference

**Affected files:**
- `docs/help/ui/curses/settings.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
settings.md states: '**Keyboard shortcut:** `Ctrl+,`' for opening settings.

quick-reference.md does not list Ctrl+, anywhere in its keyboard shortcuts table, despite being a global command.

---

#### documentation_inconsistency

**Description:** Inconsistent Quit keyboard shortcut

**Affected files:**
- `docs/help/ui/curses/quick-reference.md`
- `docs/help/ui/curses/getting-started.md`

**Details:**
quick-reference.md shows: '**Ctrl+Q** | Quit'

getting-started.md shows: '- **Q** - Quit'

One uses Ctrl+Q, the other just Q. These are different keys.

---

#### documentation_inconsistency

**Description:** Context Help keyboard shortcut inconsistency

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/features.md`

**Details:**
feature-reference.md states: '### Context Help (Shift+F1)
Get help for the BASIC keyword at the cursor: - Place cursor on keyword - Press Shift+F1'

features.md does not mention Context Help at all, despite being in the 'Essential Features' guide.

This is a significant feature omission from the essential features document.

---

#### documentation_inconsistency

**Description:** Settings storage location inconsistency between Tk and Web UI documentation

**Affected files:**
- `docs/help/ui/tk/settings.md`
- `docs/help/ui/web/settings.md`

**Details:**
Tk settings.md states settings are saved to:
- Linux/Mac: `~/.mbasic/settings.json`
- Windows: `%APPDATA%\mbasic\settings.json`

Web settings.md states: 'Web UI settings are stored in your browser's localStorage' and mentions 'Import in other browser or save to `~/.mbasic/settings.json`' as a future feature.

This is technically correct (different UIs, different storage), but the Tk documentation doesn't clarify whether these settings are actually implemented or just planned.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcuts documentation for debugging

**Affected files:**
- `docs/help/ui/web/debugging.md`
- `docs/help/ui/web/getting-started.md`

**Details:**
debugging.md under 'Debug Controls' lists:
'**Currently implemented:**
- **Run (Ctrl+R)** - Start program from beginning
- **Continue (Ctrl+G)** - Run to next breakpoint
- **Step Statement (Ctrl+T)** - Execute one statement
- **Step Line (Ctrl+K)** - Execute one line (all statements on line)
- **Stop (Ctrl+Q)** - End execution'

But getting-started.md doesn't mention these keyboard shortcuts at all when describing the toolbar buttons. It only mentions clicking buttons, not keyboard shortcuts.

Also, debugging.md says 'Function key shortcuts (F5, F10, F11, etc.) are not implemented in the Web UI' but then later under 'Execution Control' lists:
'**Step Controls:**
- Step over (F10)
- Step into (F11)
- Step out (Shift+F11)
- Run to cursor'

This is contradictory.

---

#### documentation_inconsistency

**Description:** Contradictory information about file saving and localStorage

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`

**Details:**
features.md under 'File Management > Local Storage' states:
'**Automatic Saving:**
- Saves to browser storage
- Every 30 seconds
- On significant changes
- Before running

**Session Recovery:**
- Restores last program
- Recovers after crash
- Maintains breakpoints
- Preserves variables'

But getting-started.md under 'Saving a File' says:
'**Note:** The Web UI uses browser localStorage for auto-save functionality and downloads for explicit saves to your computer.'

And later: 'The Web UI auto-saves to browser localStorage every 30 seconds. Your program should be restored automatically on refresh.'

However, features.md also has a note at the top: '**Note:** This document describes both currently implemented features and planned enhancements. Some advanced features (code intelligence, automatic saving, session recovery, collaborative editing) are planned for future releases.'

This creates confusion about whether auto-save is implemented or planned.

---

#### documentation_inconsistency

**Description:** Settings dialog documentation mixes planned and implemented features without clear distinction throughout

**Affected files:**
- `docs/help/ui/tk/settings.md`

**Details:**
The Tk settings.md document starts with a clear note: 'The features described below represent the intended implementation. Check the actual UI for currently available settings.'

However, the rest of the document is written as if all features are implemented, using present tense:
- 'The settings dialog is a multi-tabbed window'
- 'Controls editor behavior'
- 'Controls keyword display'
- 'Settings are saved to disk automatically'

This makes it very difficult for users to know what actually exists vs what is planned. The document should either:
1. Clearly mark each section as 'Implemented' or 'Planned'
2. Use future tense for planned features
3. Be split into separate 'Current Features' and 'Planned Features' sections

---

#### documentation_inconsistency

**Description:** Contradictory information about F-key shortcuts in same document

**Affected files:**
- `docs/help/ui/web/debugging.md`

**Details:**
debugging.md under 'Debug Controls' states:
'**Note:** Function key shortcuts (F5, F10, F11, etc.) are not implemented in the Web UI.'

But then under 'Execution Control' it lists:
'**Step Controls:**
- Step over (F10)
- Step into (F11)
- Step out (Shift+F11)
- Run to cursor

**Flow Control:**
- Continue (F5)
- Pause
- Stop (Shift+F5)
- Restart'

And under 'Keyboard Shortcuts' it says:
'**Planned for Future Releases:**
- `F5` - Start/Continue debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into'

This is internally contradictory within the same document.

---

#### documentation_inconsistency

**Description:** Web interface documentation describes 'Load Example' menu option, but library documentation only mentions 'Download' and 'Open' for loading files

**Affected files:**
- `docs/help/ui/web/web-interface.md`
- `docs/library/*/index.md`

**Details:**
web-interface.md states:
'Load Example - Choose from sample BASIC programs'

But all library index.md files say:
'Web/Tkinter UI: Click File → Open, select the downloaded file'

No mention of 'Load Example' feature in library docs. Users may be confused about how to access example programs.

---

#### documentation_inconsistency

**Description:** Web UI documentation mentions CLI commands that don't apply to web interface

**Affected files:**
- `docs/help/ui/web/web-interface.md`
- `docs/library/*/index.md`

**Details:**
web-interface.md File I/O section and library docs both show:
'CLI: Type `LOAD "filename.bas"`'

But web-interface.md earlier states:
'Cannot directly access local filesystem (but can load files via browser file picker)'

The LOAD command syntax shown would not work in web UI's sandboxed environment. This could confuse web users.

---

#### documentation_inconsistency

**Description:** Contradictory information about debugger support

**Affected files:**
- `docs/help/ui/web/web-interface.md`

**Details:**
web-interface.md Limitations section states:
'Limited debugger support (basic breakpoints only via Run menu)'

But the Run Menu section only lists:
'Run Program - Parse and execute the current program
Stop - Stop a running program'

No mention of breakpoints or debugger features in the Run menu description. Either the limitation is wrong or the menu description is incomplete.

---

#### documentation_inconsistency

**Description:** Web UI documentation doesn't mention case handling settings available in MBASIC

**Affected files:**
- `docs/help/ui/web/web-interface.md`
- `docs/user/CASE_HANDLING_GUIDE.md`

**Details:**
CASE_HANDLING_GUIDE.md extensively documents:
'SET "variables.case_conflict" "error"'
'SET "keywords.case_style" "force_capitalize"'
'SHOW SETTINGS'

But web-interface.md makes no mention of these settings or the SET/SHOW commands. Web users may not know these features exist.

---

#### documentation_inconsistency

**Description:** File persistence information contradicts session-based claim

**Affected files:**
- `docs/help/ui/web/web-interface.md`

**Details:**
Security & Privacy section states:
'Session-based - Data cleared when session ends'

But File I/O section states:
'Files persist during your session'

And Limitations section states:
'Files don't persist after session ends (stored in browser memory only)'

These are consistent with each other but could be clearer. The phrasing 'persist during your session' might confuse users into thinking files are saved permanently.

---

#### documentation_inconsistency

**Description:** Two separate installation guides exist with overlapping content and different levels of detail

**Affected files:**
- `docs/user/INSTALL.md`
- `docs/user/INSTALLATION.md`

**Details:**
INSTALL.md provides comprehensive installation instructions with virtual environment setup, troubleshooting, and feature status. INSTALLATION.md is marked as a PLACEHOLDER that redirects to INSTALL.md. This creates confusion about which file is authoritative and may lead to maintenance issues where one gets updated but not the other.

---

#### documentation_inconsistency

**Description:** Different UI documentation focuses - CHOOSING_YOUR_UI.md covers all UIs, QUICK_REFERENCE.md only covers Curses

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`
- `docs/user/QUICK_REFERENCE.md`

**Details:**
CHOOSING_YOUR_UI.md provides comprehensive comparison of CLI, Curses, Tk, and Web UIs with decision trees and use cases.

QUICK_REFERENCE.md is titled 'MBASIC Curses IDE - Quick Reference Card' and only documents Curses UI commands and workflows.

The README.md in docs/user/ lists QUICK_REFERENCE.md without clarifying it's Curses-specific, which could mislead users expecting a general quick reference.

---

#### documentation_inconsistency

**Description:** Settings documentation describes unimplemented features without clear status indicators

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
The document describes many settings in detail (variables.case_conflict, editor.auto_number, interpreter.strict_mode, ui.theme, etc.) as if they are fully implemented, using present tense and providing examples.

At the very end, there's a 'Future Settings (Planned)' section listing keywords.case_style, spacing.operator_style, etc.

However, there's no indication in the main sections which settings are actually implemented vs. designed but not yet functional. The document should clearly mark each setting's implementation status.

---

#### documentation_inconsistency

**Description:** Contradictory information about CLI debugging features

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
In 'Detailed UI Profiles' for CLI, under 'Unique advantages':
- 'New debugging commands (BREAK, STEP, WATCH)'

In 'Decision Matrix' table:
- CLI Debugging: ✅
- Curses Debugging: ✅
- Tk Debugging: ✅
- Web Debugging: ✅

However, in 'Limitations' for CLI:
- 'No visual debugging'

This creates confusion: CLI has debugging commands (BREAK, STEP, WATCH) and gets a ✅ for debugging, but also 'no visual debugging'. The distinction between command-line debugging and visual debugging should be clearer in the comparison table.

---

#### documentation_inconsistency

**Description:** Breakpoint commands documentation references non-existent files

**Affected files:**
- `docs/user/QUICK_REFERENCE.md`

**Details:**
At the end of QUICK_REFERENCE.md under 'Examples', it lists:
- test_continue.bas
- demo_continue.bas
- test_continue_manual.sh

And under 'More Information':
- DEBUGGER_COMMANDS.md
- CONTINUE_FEATURE.md
- BREAKPOINT_SUMMARY.md
- HELP_SYSTEM_SUMMARY.md

These files are not provided in the documentation set. If they don't exist, these references should be removed or marked as TODO. If they do exist, they should be included in reviews.

---

#### documentation_inconsistency

**Description:** Keyboard shortcut documentation mismatch between Tk UI and Curses UI guides

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md documents Ctrl+H as 'Find and replace' for Tk UI:
| **Ctrl+H** | Find and replace |

But keyboard-shortcuts.md (Curses UI) documents ^F (Ctrl+F) as help:
| `^F` | This help |

And Ctrl+H as help in Curses:
| Ctrl+H/F1 | Help |

This creates confusion about whether Ctrl+H is Find/Replace (Tk) or Help (Curses). The UI_FEATURE_COMPARISON.md confirms Find/Replace is Tk-only, but the shortcut conflict isn't clearly documented.

---

#### documentation_inconsistency

**Description:** Conflicting information about Find/Replace availability in Web UI

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
TK_UI_QUICK_START.md states Find/Replace is Tk-only:
'### 5. Advanced Editing - Find and Replace'

UI_FEATURE_COMPARISON.md Feature Matrix shows:
| **Find/Replace** | ❌ | ❌ | ✅ | ❌ | Tk only (new feature) |

But later in UI_FEATURE_COMPARISON.md under 'Coming Soon':
'⏳ Find/Replace in Web UI'

This suggests Find/Replace might be coming to Web UI, but the feature matrix marks it as unavailable with no indication it's planned.

---

#### documentation_inconsistency

**Description:** Execution Stack window shortcut only available via menu in Curses UI

**Affected files:**
- `docs/user/keyboard-shortcuts.md`

**Details:**
keyboard-shortcuts.md states:
| `Menu only` | Toggle execution stack window |

This appears twice in the document (under Global Commands and Debugger sections). However, TK_UI_QUICK_START.md documents Ctrl+K for Execution Stack in Tk UI:
| **Ctrl+K** | Show/hide Execution Stack window |

It's unclear why Curses UI doesn't have a keyboard shortcut for this feature when Tk UI does.

---

#### documentation_inconsistency

**Description:** Inconsistent feature status for auto-save

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
UI_FEATURE_COMPARISON.md shows:
| **Auto-save** | ❌ | ❌ | ⚠️ | ✅ | Tk: optional, Web: automatic |

The ⚠️ symbol for Tk suggests partial support ('optional'), but it's not clear what 'optional' means - is it a setting users can enable, or is it not fully implemented? The distinction between ❌ (not available) and ⚠️ (partial) needs clarification.

---

### 🟢 Low Severity

#### code_comment_conflict

**Description:** LineNode docstring contradicts its own structure

**Affected files:**
- `src/ast_nodes.py`

**Details:**
LineNode class docstring states: "The AST is the single source of truth. Text is always regenerated from the AST using token positions. Never store source_text - it creates a duplicate copy that gets out of sync."

However, the LineNode class definition does not have a source_text field, so this warning appears to be addressing a non-existent field. This suggests either:
1. The field was removed during refactoring but the warning comment remained
2. The comment is preemptively warning against adding such a field

---

#### code_comment_conflict

**Description:** InputStatementNode docstring describes behavior inconsistently

**Affected files:**
- `src/ast_nodes.py`

**Details:**
InputStatementNode docstring states:
"Note: Both comma and semicolon after prompt show '?' in real MBASIC.
Only INPUT; (semicolon immediately after INPUT) suppresses the '?'."

This describes two different uses of semicolon:
1. After prompt: shows '?'
2. Immediately after INPUT keyword: suppresses '?'

The field 'suppress_question' is documented as "True if INPUT; (semicolon immediately after INPUT)" but the syntax examples show both "INPUT 'prompt'; var1" (semicolon after prompt) and "INPUT; var1" (semicolon after INPUT). The distinction between these two cases and how they map to the suppress_question field could be clearer.

---

#### documentation_inconsistency

**Description:** Duplicate node definitions mentioned in comment but not visible

**Affected files:**
- `src/ast_nodes.py`

**Details:**
Comment at line ~700 states:
"# NOTE: SetSettingStatementNode and ShowSettingsStatementNode are defined later in the file
# in the 'Settings Commands' section (around line 1005-1038) with the correct field names.
# These earlier definitions were removed to eliminate duplicates."

This comment references earlier duplicate definitions that were removed, but the comment itself remains. This is a documentation artifact from refactoring that should be cleaned up since there are no longer any duplicates to warn about.

---

#### code_comment_conflict

**Description:** CallStatementNode docstring describes non-standard syntax as accepted

**Affected files:**
- `src/ast_nodes.py`

**Details:**
CallStatementNode docstring states:
"Standard MBASIC 5.21 Syntax:
    CALL address           - Call machine code at numeric address
...
Note: Parser also accepts extended syntax for compatibility with
other BASIC dialects (e.g., CALL ROUTINE(args)), but this is not
standard MBASIC 5.21."

The node has an 'arguments' field described as "Arguments (non-standard, for compatibility)" but the docstring claims the parser accepts this syntax. Without seeing the parser code, we cannot verify if this extended syntax is actually implemented or if this is aspirational documentation.

---

#### documentation_inconsistency

**Description:** TypeInfo class marked as potentially redundant

**Affected files:**
- `src/ast_nodes.py`

**Details:**
TypeInfo class docstring states:
"Note: This class provides convenience methods for working with VarType enum.
Kept for backwards compatibility but could be refactored away."

This suggests the class is deprecated or redundant, but it's still fully implemented with static methods. This creates uncertainty about whether new code should use TypeInfo or VarType directly.

---

#### documentation_inconsistency

**Description:** VariableNode has redundant type information fields

**Affected files:**
- `src/ast_nodes.py`

**Details:**
VariableNode has both 'type_suffix' and 'explicit_type_suffix' fields:
- type_suffix: Optional[str] = None  # $, %, !, #
- explicit_type_suffix: bool = False  # True if type_suffix was in original source, False if inferred from DEF

The comment suggests that type_suffix can be either explicit (from source) or inferred (from DEF statements). However, having both fields creates potential for inconsistency where type_suffix is set but explicit_type_suffix doesn't accurately reflect its origin.

---

#### documentation_inconsistency

**Description:** DimStatementNode has unexplained 'token' field

**Affected files:**
- `src/ast_nodes.py`

**Details:**
DimStatementNode has a field:
    token: Optional[Any] = None  # Token for tracking access time

The comment "Token for tracking access time" is unclear. Other statement nodes use keyword_token for preserving case, but this field is named just 'token' and mentions 'access time' which is not explained elsewhere. This appears to be either:
1. A different purpose than other token fields
2. An incomplete or outdated implementation
3. Poorly documented functionality

---

#### code_vs_comment

**Description:** Comment claims identifiers bypass the identifier_table, but the table is still created and could be used

**Affected files:**
- `src/case_string_handler.py`

**Details:**
Lines ~45-51: Comment states:
# Note: We bypass the identifier_table here since identifiers always return
# original_text. The table could be used in future for conflict detection.

This suggests the identifier_table exists but is unused. However, the get_identifier_table() method is defined and creates the table. This is inconsistent - either the table should be removed entirely or the comment should clarify why it's created but not used.

---

#### documentation_inconsistency

**Description:** Docstring for MBASIC version is inconsistent across file

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line 2: Module docstring says 'Built-in functions for MBASIC 5.21'
Line 169: Class docstring says 'MBASIC 5.21 built-in functions'

Both reference version 5.21, but there's no version constant imported or defined. If version matters for compatibility, it should be imported from src.version module (referenced in debug_logger.py).

---

#### code_vs_comment

**Description:** UsingFormatter.format_numeric_field comment about negative zero handling may not match all BASIC implementations

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Lines ~360-363: Comment states:
# Determine sign - preserve negative sign for values that round to zero.
# This matches BASIC behavior where -0.001 formatted with no decimal places
# displays as "-0" (not "0"). Positive values that round to zero display as "0".

This is a specific interpretation of BASIC behavior. The comment claims this 'matches BASIC behavior' but doesn't specify which BASIC variant. MBASIC 5.21 behavior for negative zero may differ. Without testing against actual MBASIC 5.21, this claim is unverified.

---

#### code_vs_comment

**Description:** INKEY() docstring says 'MBASIC INKEY$ function' but method is named INKEY without $

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line ~1000: Docstring says 'This is the MBASIC INKEY$ function.'

The method is named INKEY() because Python doesn't allow $ in identifiers. This is fine, but the docstring should clarify this is the Python implementation of BASIC's INKEY$ to avoid confusion. Similar issue with INPUT() method which implements INPUT$.

---

#### documentation_inconsistency

**Description:** Module docstring mentions 'UI' but doesn't specify which UI implementation

**Affected files:**
- `src/debug_logger.py`

**Details:**
Lines 1-6: Docstring says 'errors and debug info are output to both the UI and stderr'

The module doesn't define what 'the UI' is. Based on the code, it only outputs to stderr and returns strings. The caller is responsible for displaying to UI. The docstring should clarify this is a utility that returns formatted strings for UI display, not that it directly outputs to UI.

---

#### code_vs_comment

**Description:** InMemoryFileHandle.flush() comment describes behavior that differs from typical file semantics

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
The flush() method comment states:
"Note: This calls StringIO/BytesIO flush() which are no-ops.
Content is only saved to the virtual filesystem on close().
This differs from file flush() semantics where flush() typically
persists buffered writes."

This is technically correct but potentially misleading. The comment explains the difference from real file semantics, but doesn't clarify whether this is intentional design or a limitation. For BASIC programs expecting flush() to persist data, this could cause bugs.

---

#### documentation_inconsistency

**Description:** Inconsistent capitalization of 'MERGE' in documentation

**Affected files:**
- `src/editing/manager.py`

**Details:**
In manager.py docstring:
"- File operations (SAVE, LOAD, MERGE)"

But in method docstring:
"manager.merge_from_file(\"overlay.bas\")  # Merges without clearing"

And in the actual method name: merge_from_file()

The command is capitalized in the list but lowercase in usage examples. Should be consistent (either all caps when referring to the BASIC command, or lowercase when referring to the Python method).

---

#### code_vs_documentation

**Description:** Error code documentation mentions ambiguous two-letter codes but doesn't explain resolution strategy

**Affected files:**
- `src/error_codes.py`

**Details:**
The module docstring states:
"Note: Some two-letter codes are duplicated (e.g., DD, CN, DF) across different
numeric error codes. This matches the original MBASIC 5.21 specification where
the two-letter codes alone are ambiguous - the numeric code is authoritative."

The code shows:
10: (\"DD\", \"Duplicate definition\")
61: (\"DF\", \"Disk full\")
68: (\"DD\", \"Device unavailable\")

Error 10 uses DD, error 68 also uses DD. Error 54 uses DF (not shown but implied). The documentation explains the ambiguity exists but doesn't explain how the interpreter resolves it when displaying errors or how users should interpret these codes.

---

#### code_vs_comment

**Description:** Comment says 'We do not save/restore the PC' but doesn't explain why this is safe for all statement types

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Comment in execute() method:
"# Note: We do not save/restore the PC before/after execution.
# This allows statements like RUN to change execution position.
# Normal statements (PRINT, LET, etc.) don't modify PC anyway."

This comment claims normal statements don't modify PC, but doesn't address what happens with GOTO, GOSUB, or other control flow statements that ARE mentioned in the help text as 'not recommended'. The help says:
"• GOTO, GOSUB, and control flow statements are not recommended
  (they will execute but may produce unexpected results)"

The comment should acknowledge these edge cases or the help text should be more specific about why they produce unexpected results.

---

#### documentation_inconsistency

**Description:** Help text mentions 'Ctrl+H (UI help)' but this is not documented in the immediate_executor module

**Affected files:**
- `src/immediate_executor.py`

**Details:**
The _show_help() method displays:
"Press Ctrl+H (UI help) for keyboard shortcuts and UI features."

This references UI functionality that is outside the scope of the immediate_executor module. There's no documentation about what UI this refers to or whether Ctrl+H is actually implemented. This creates a forward reference to undocumented functionality.

---

#### code_vs_comment

**Description:** Help text says 'Multi-statement lines work but are not recommended' but doesn't explain why or what issues may occur

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Help text states:
"• Multi-statement lines (: separator) work but are not recommended"

This is vague and doesn't explain:
1. What specific problems occur with multi-statement lines
2. Whether this is a limitation of immediate mode or the parser
3. Whether the output will be confusing or execution will fail

The implementation doesn't show any special handling or warnings for multi-statement lines, so it's unclear why they're 'not recommended'.

---

#### documentation_inconsistency

**Description:** Module docstring mentions 'MBASIC editor' but the functions are generic and don't reference any specific editor

**Affected files:**
- `src/input_sanitizer.py`

**Details:**
Module docstring:
"Input sanitization utilities for MBASIC editor."

But the functions (is_valid_input_char, sanitize_input, clear_parity, etc.) are completely generic and don't have any MBASIC-specific or editor-specific logic. They could be used for any text input sanitization. The docstring should either:
1. Explain why these are specific to MBASIC editor
2. Remove the 'for MBASIC editor' qualifier and make it generic

The functions themselves don't reference 'editor' or 'MBASIC' anywhere.

---

#### code_vs_comment

**Description:** Function clear_parity() docstring example shows chr(193) as 'A' with bit 7 set, but doesn't explain the serial communication context

**Affected files:**
- `src/input_sanitizer.py`

**Details:**
The clear_parity() docstring states:
"In serial communication, bit 7 is sometimes used for parity checking.
This can cause 'A' (65) to become 'A'+128 (193), which breaks character
comparison and display."

However, the immediate_executor.py file doesn't mention serial communication anywhere, and there's no documentation about when or why parity bits would be present in the input. This suggests either:
1. The input_sanitizer is designed for a specific use case (serial input) not documented in immediate_executor
2. This is legacy documentation from a different context
3. There's missing documentation about the input source

The connection between these two modules and the parity bit issue is not explained.

---

#### code_vs_comment

**Description:** Comment says 'bare except' for _read_char fallback, but except clause has no colon

**Affected files:**
- `src/interactive.py`

**Details:**
At line ~1235, comment says:
"# Fallback for non-TTY/piped input or any terminal errors (bare except)"

But the code shows:
except:
    # Fallback for non-TTY/piped input or any terminal errors (bare except)
    ch = sys.stdin.read(1)
    return ch if ch else None

This IS a bare except (catches all exceptions), so the comment is accurate. However, the comment's phrasing 'bare except' in parentheses suggests it might be explaining why this pattern is used, which is correct.

---

#### documentation_inconsistency

**Description:** Module docstring claims 'MBASIC 5.21' but startup message says 'MBASIC-2025'

**Affected files:**
- `src/interactive.py`

**Details:**
Module docstring at line 2:
"MBASIC 5.21 Interactive Command Mode"

But start() method at line 140 prints:
print("MBASIC-2025 - Modern MBASIC 5.21 Interpreter")

The version naming is inconsistent - is it 'MBASIC 5.21' or 'MBASIC-2025'?

---

#### code_vs_comment

**Description:** Comment about readline Ctrl+A binding says it 'triggers edit mode' but doesn't explain the full flow

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~125 says:
"# Bind Ctrl+A to insert the character instead of moving cursor to beginning-of-line
# This overrides default Ctrl+A (beginning-of-line) behavior.
# When user presses Ctrl+A, the terminal sends ASCII 0x01, and 'self-insert'
# tells readline to insert it as-is instead of interpreting it as a command.
# The \x01 character in the input string triggers edit mode (see start() method)"

The comment explains the readline binding but doesn't clearly explain that the \x01 character is then detected in the start() method's main loop (line ~155) to trigger EDIT mode. The connection between the readline binding and the edit mode detection is not explicit.

---

#### code_vs_comment_conflict

**Description:** Comment says 'Execute just the statement at line 0' but code executes all statements on line 0

**Affected files:**
- `src/interactive.py`

**Details:**
Comment: "# Execute just the statement at line 0"

Code:
```
for stmt in line_node.statements:
    interpreter.execute_statement(stmt)
```

The comment uses singular 'statement' but the code loops through multiple statements. Should say 'Execute all statements at line 0' or 'Execute the statements at line 0'.

---

#### code_vs_comment

**Description:** InterpreterState docstring describes checking order that doesn't match typical usage patterns

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring at lines 30-35 says:
"Primary execution states (check these to determine current status):
- error_info: Non-None if an error occurred (check FIRST - highest priority)
- input_prompt: Non-None if waiting for input (check SECOND)
- runtime.halted: True if stopped (paused/done/at breakpoint) (check LAST)"

However, in tick_pc() method (lines 280-400), the actual checking order is:
1. pause_requested (line 286)
2. pc.halted() or runtime.halted (line 293)
3. break_requested (line 301)
4. breakpoints (line 310)
5. input_prompt (line 372)
6. error_info (set during exception handling)

The docstring suggests error_info should be checked first, but the code checks halted state and pause requests before errors can even occur.

---

#### documentation_inconsistency

**Description:** Version comment mentions internal version but doesn't explain versioning scheme

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at lines 656-659 says:
"# OLD EXECUTION METHODS REMOVED (internal version v1.0.300 - this is the mbasic implementation
# version, not the MBASIC 5.21 language version)"

This mentions two version numbers (v1.0.300 and MBASIC 5.21) but:
1. The file header only mentions "MBASIC 5.21 Interpreter" (line 2)
2. No other documentation explains the internal versioning scheme
3. It's unclear what v1.0.300 represents or where it's tracked

---

#### code_vs_comment

**Description:** Comment about RESUME 0 vs RESUME None behavior is misleading

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~310 says:
"RESUME or RESUME 0 - retry the statement that caused the error
Parser treats these differently (None vs 0) as separate AST representations,
but they have identical runtime behavior (both retry the error statement)"

This suggests the parser creates different AST nodes for RESUME vs RESUME 0, but the comment doesn't clarify why this distinction exists if behavior is identical. The code treats both cases the same (line_number is None or 0), making the parser distinction seem unnecessary.

---

#### code_vs_comment

**Description:** INPUT statement comment mentions 'input_file_number' state variable but code sets it to None for keyboard input

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~540 says:
"Sets: input_prompt (prompt text), input_variables (var list),
input_file_number (file # or None)."

Code at line ~570 sets:
self.state.input_file_number = None

This is correct for keyboard input, but the comment could be clearer that input_file_number is only set to a number when reading from a file, not for keyboard input.

---

#### code_vs_comment

**Description:** LSET/RSET fallback behavior documented as 'compatibility extension' but may not match MBASIC 5.21

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1180 says:
"If not a field variable, fall back to normal assignment.
Note: In strict MBASIC 5.21, LSET/RSET are only for field variables.
This fallback is a compatibility extension."

This explicitly documents deviation from MBASIC 5.21 behavior. If strict compatibility is a goal, this extension may cause issues. The comment acknowledges this but doesn't indicate if this is intentional or a TODO.

---

#### code_vs_comment

**Description:** CP/M ^Z EOF handling documented extensively but encoding choice (latin-1) rationale could be clearer

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~590 provides extensive CP/M background:
"CP/M Background:
On CP/M 1.x and 2.x, files were stored in 128-byte sectors..."

And explains:
"Encoding:
Uses latin-1 (ISO-8859-1) to preserve byte values 128-255 unchanged.
CP/M and MBASIC used 8-bit characters; latin-1 maps bytes 0-255 to
Unicode U+0000-U+00FF, allowing round-trip byte preservation."

While technically correct, the comment doesn't mention that this choice may cause issues with actual CP/M files that used different code pages (e.g., CP/M with non-English character sets). This is a minor documentation gap.

---

#### code_vs_comment

**Description:** Comment about LSET/RSET fallback contradicts claim of strict MBASIC 5.21 compatibility

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_lset/execute_rset:
"# If not a field variable, fall back to normal assignment.
# Note: In strict MBASIC 5.21, LSET/RSET are only for field variables.
# This fallback is a compatibility extension."

The comment acknowledges this is NOT strict MBASIC 5.21 behavior, but the code implements it anyway. This is a documented deviation but creates ambiguity about compatibility claims elsewhere in the codebase.

---

#### code_vs_comment

**Description:** Comment about variable access tracking in function calls is overly detailed and may be outdated

**Affected files:**
- `src/interpreter.py`

**Details:**
In evaluate_functioncall, there are two detailed comments about using get_variable_for_debugger and debugger_set=True:

"# Note: Use get_variable_for_debugger to avoid triggering variable access tracking.
# We ARE using the value (to save/restore), but this is implementation detail,
# not program-level variable access."

and

"# Use debugger_set=True to avoid tracking this as program-level assignment.
# This is function call implementation (save/restore params), not user code."

These comments suggest a sophisticated variable tracking system for debugging, but it's unclear if this tracking system exists or if these comments are remnants from a different implementation. The level of detail suggests either important context or outdated implementation notes.

---

#### code_vs_comment

**Description:** STEP command implementation status is unclear

**Affected files:**
- `src/interpreter.py`

**Details:**
The execute_step docstring says:
"STEP is intended to execute one or more statements, then pause.
Current implementation: Placeholder that prints a message (not yet functional).
Full implementation would require debugger integration."

But the code outputs:
"STEP {count} - Debug stepping not fully implemented"

The message to users says 'not fully implemented' (implying partial implementation), while the docstring says it's a 'placeholder' and 'not yet functional' (implying no implementation). These are different claims about the implementation status.

---

#### code_vs_comment_conflict

**Description:** Comment says input_line delegates to self.input with 'same behavior', but this contradicts the base class documentation

**Affected files:**
- `src/iohandler/console.py`

**Details:**
In console.py line ~60:
"""Input a complete line from console.

For console, this delegates to self.input() (same behavior).
"""

But base.py documents input_line as:
"Similar to input() but preserves leading/trailing spaces and
doesn't interpret commas as field separators."

The comment claims 'same behavior' but the base class says they should differ in comma handling and space preservation.

---

#### documentation_inconsistency

**Description:** Example in docstring uses inconsistent prompt format

**Affected files:**
- `src/iohandler/base.py`

**Details:**
In base.py input() method examples:
"Examples:
    name = input('Enter name: ')
    value = input('? ')"

But in input_line() examples:
"Examples:
    line = input_line('Enter text: ')"

The first uses both descriptive and minimal prompts, the second only descriptive. This inconsistency in documentation examples could confuse users about prompt conventions.

---

#### code_vs_comment_conflict

**Description:** Comment says error() tries to use red color but implementation uses color_pair(4) without defining what that is

**Affected files:**
- `src/iohandler/curses_io.py`

**Details:**
curses_io.py error() method:
"# Try to use red color for errors
if self.output_win:
    try:
        if curses.has_colors():
            self.output_win.addstr(message, curses.color_pair(4))"

The comment says 'red color' but color_pair(4) is used without any initialization or documentation of what color pair 4 represents. There's no code showing color pairs being set up, so this may not actually be red.

---

#### documentation_inconsistency

**Description:** Docstring claims input_char always returns empty string but doesn't explain why

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
web_io.py input_char():
"Note: Character input not supported in web UI (always returns empty string)."

This limitation is stated but not explained. Users might wonder why it's not supported (technical limitation? design choice?) and whether there are workarounds. The base class documents this as a key feature for INKEY$ and INPUT$ functions.

---

#### code_vs_comment_conflict

**Description:** Comment about preprocessing old BASIC contradicts claim that lexer handles properly-formed MBASIC 5.21

**Affected files:**
- `src/lexer.py`

**Details:**
lexer.py read_identifier() contains:
"This lexer parses properly-formed MBASIC 5.21 which requires spaces
between keywords and identifiers. Old BASIC with NEXTI instead of NEXT I
should be preprocessed before parsing."

And later:
"# NOTE: We do NOT handle old BASIC where keywords run together (NEXTI, FORI).
# This is properly-formed MBASIC 5.21 which requires spaces.
# Old BASIC files should be preprocessed with conversion scripts."

But there's no documentation of these 'conversion scripts' anywhere in the codebase, and no guidance on how to preprocess old BASIC files. This creates a documentation gap.

---

#### code_vs_comment

**Description:** Docstring claims RND and INKEY$ can be called without parentheses for MBASIC 5.21 compatibility, but this is standard BASIC behavior not specific to version 5.21

**Affected files:**
- `src/parser.py`

**Details:**
Module docstring at top says:
"Expression parsing notes:
- Functions generally require parentheses: SIN(X), CHR$(65)
- Exception: RND and INKEY$ can be called without parentheses (MBASIC 5.21 compatibility)"

This implies it's a special compatibility feature for version 5.21, but RND and INKEY$ without parentheses is standard across most BASIC dialects, not a version-specific compatibility feature.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for 'end of input' vs 'end of tokens'

**Affected files:**
- `src/parser.py`

**Details:**
Multiple methods use different terminology:
- at_end() checks for 'end of tokens'
- has_more_tokens() checks if 'there are more tokens to parse'
- at_end_of_tokens() is described as 'alias for current() is None'
- expect() raises 'Unexpected end of input'
- advance() raises 'Unexpected end of input'

The terms 'end of input', 'end of tokens', and 'exhausted all tokens' are used interchangeably without clear distinction.

---

#### code_vs_comment

**Description:** Comment describes LINE modifier syntax that appears incomplete or incorrect

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line ~50 states:
"# Check for LINE modifier after semicolon: INPUT "prompt";LINE var$
# LINE allows input of entire line including commas"

The code checks for LINE_INPUT token type, but the comment suggests it comes after a semicolon following the prompt. However, the code doesn't verify this position requirement - it just checks if LINE_INPUT token exists at current position, which could be anywhere in the statement.

---

#### code_vs_comment

**Description:** IF statement comment describes syntax variations but implementation may not handle all cases correctly

**Affected files:**
- `src/parser.py`

**Details:**
The docstring for parse_if() lists syntax variations including:
"- IF condition THEN line_number :ELSE line_number"

However, the code has complex logic around line ~1050 that tries to handle :ELSE by peeking ahead and restoring position. The comment suggests this is a standard syntax, but the implementation treats it as a special case requiring lookahead, suggesting potential inconsistency in how this syntax is documented vs. implemented.

---

#### code_vs_comment

**Description:** DIM statement comment claims dimensions must be constant but code accepts any expression

**Affected files:**
- `src/parser.py`

**Details:**
The docstring for parse_dim() at line ~1330 states:
"Note: In compiled BASIC, dimensions must be constant expressions"

However, the implementation calls parse_expression() for dimensions without any validation that they are constant. The code accepts any expression, contradicting the comment's claim about compiled BASIC requirements.

---

#### code_vs_comment

**Description:** MID$ assignment comment shows syntax with $ but notes it's tokenized without $

**Affected files:**
- `src/parser.py`

**Details:**
The docstring for parse_mid_assignment() at line ~1410 shows:
"Syntax:
    MID$(string_var, start, length) = value"

But then states:
"Note: MID$ is tokenized as a single MID token"

The comment then says 'Skip MID (which includes the $)'. This is confusing - if it's tokenized as MID without $, why does the comment say it 'includes the $'? The syntax example and implementation note are inconsistent.

---

#### code_vs_comment

**Description:** DEFTYPE comment mentions batch vs interactive mode but implementation doesn't show mode-specific behavior

**Affected files:**
- `src/parser.py`

**Details:**
The docstring for parse_deftype() at line ~1450 states:
"Note: In batch mode, type collection already happened in first pass.
In interactive mode, this updates the def_type_map."

However, the implementation unconditionally updates def_type_map regardless of mode. There's no conditional logic checking batch vs interactive mode, suggesting the comment describes intended behavior that isn't actually implemented.

---

#### code_vs_comment

**Description:** DEFFN comment shows inconsistent function name normalization

**Affected files:**
- `src/parser.py`

**Details:**
In parse_deffn() around line ~1500, the code handles two cases:
1. 'DEF FN name' creates 'fn' + raw_name with comment 'Use lowercase fn to match function calls'
2. 'DEF FNR' expects identifier starting with 'fn' (already lowercase)

The comment suggests lowercase 'fn' is important for matching, but the second case doesn't normalize to lowercase - it just checks if it starts with 'fn'. This inconsistency in normalization could cause matching issues.

---

#### code_vs_comment

**Description:** parse_call docstring describes MBASIC 5.21 'standard syntax' vs 'extended syntax' but implementation treats both equally

**Affected files:**
- `src/parser.py`

**Details:**
Docstring says:
'MBASIC 5.21 standard syntax:
    CALL address           - Call machine code at numeric address

Extended syntax (other BASIC dialects):
    CALL ROUTINE(X,Y)      - Call with arguments (fully parsed/supported)'

However, the implementation parses both forms identically and creates CallStatementNode with arguments in both cases. There's no distinction in the code between 'standard' and 'extended' syntax - both are fully supported. The comment suggests a historical distinction that doesn't exist in the implementation.

---

#### code_vs_comment

**Description:** parse_resume comment says 'RESUME 0 is valid BASIC syntax' but doesn't explain what it means

**Affected files:**
- `src/parser.py`

**Details:**
Comment says: 'Note: RESUME 0 is valid BASIC syntax meaning "retry error statement" (same as RESUME)'

This is informative but incomplete. The code sets line_number to 0 (not None) when RESUME 0 is used, but the comment suggests it should behave the same as RESUME (which would be line_number=None). This creates ambiguity about whether line_number=0 and line_number=None are treated the same by the executor.

---

#### code_vs_comment

**Description:** parse_common docstring says 'we don't need to do anything special with arrays' but then checks for array indicator

**Affected files:**
- `src/parser.py`

**Details:**
Docstring says: 'The empty parentheses () indicate an array variable (all elements shared). This is just a marker - no subscripts are specified or stored.'

Then in comment: '# Check for array indicator ()
# (we don't need to do anything special with arrays in COMMON,
# just note the variable name)'

The code does check for and consume the parentheses, which is 'doing something' with arrays. The comment is slightly misleading - it should say 'we don't need to store array information separately' rather than 'don't need to do anything special'.

---

#### documentation_inconsistency

**Description:** parse_line_input docstring mentions 'Lexer produces LINE_INPUT token' but this is implementation detail not syntax documentation

**Affected files:**
- `src/parser.py`

**Details:**
Docstring says: 'Note: Lexer produces LINE_INPUT token, but INPUT keyword may follow'

This is an implementation note about tokenization, not syntax documentation. It's useful for maintainers but inconsistent with other docstrings that focus on BASIC syntax. Most other parse_* methods don't mention lexer token details.

---

#### code_vs_comment

**Description:** Comment in serialize_let_statement says 'LET or assignment statement' but method only handles assignment

**Affected files:**
- `src/position_serializer.py`

**Details:**
Method comment: "Serialize LET or assignment statement"
But the method signature is: def serialize_let_statement(self, stmt: ast_nodes.LetStatementNode)

The node type is 'LetStatementNode' not 'AssignmentStatementNode'. However, in _adjust_statement_positions, the code checks for 'AssignmentStatementNode':

if stmt_type == 'AssignmentStatementNode':
    _adjust_expression_positions(stmt.variable, offset)
    _adjust_expression_positions(stmt.expression, offset)

This suggests either:
1. There are two different node types (LetStatementNode and AssignmentStatementNode)
2. The node was renamed and some references weren't updated

---

#### code_vs_comment

**Description:** Module docstring says 'AST is the source of truth' but implementation attempts to preserve original token positions

**Affected files:**
- `src/position_serializer.py`

**Details:**
Module docstring states:
"Serializes AST nodes back to source text while attempting to preserve original token positions and spacing."

And in serialize_line method comment:
"AST is the single source of truth for content - serialize from AST while attempting to preserve original token positions/spacing"

This creates tension: if AST is the single source of truth, why preserve original positions? The positions are metadata, not content. The comment should clarify that:
- AST is source of truth for CONTENT (what tokens exist, their values)
- Original positions are HINTS for formatting (where to place tokens)
- When positions conflict, content wins (hence PositionConflict tracking)

---

#### code_vs_comment

**Description:** Comment says 'preserve' policy should not call apply_keyword_case_policy but function handles it anyway

**Affected files:**
- `src/position_serializer.py`

**Details:**
In apply_keyword_case_policy:
elif policy == "preserve":
    # Preserve is handled by caller passing in original case - caller should not call this function
    # However, we handle it defensively: if called with "preserve", return capitalize as fallback

This defensive programming contradicts the comment. Either:
1. Remove the defensive handling and raise an error
2. Update comment to say 'preserve is handled by caller, but we provide a fallback'

The current code suggests this was added after discovering callers were incorrectly passing 'preserve'.

---

#### documentation_inconsistency

**Description:** Comment says 'MBASIC 5.21 compatibility' for max_string_length but doesn't explain why 255 bytes is the limit

**Affected files:**
- `src/resource_limits.py`

**Details:**
Multiple places say:
max_string_length=255,              # 255 bytes (MBASIC 5.21 compatibility)

But in create_unlimited_limits:
max_string_length=1024*1024,        # 1MB strings (for testing/development - not MBASIC compatible)

The comment '(MBASIC 5.21 compatibility)' appears without explanation of WHY 255 is the MBASIC limit. Was this a hardware limitation? A design choice? This context would help developers understand if/when to override it.

---

#### code_vs_comment

**Description:** estimate_size docstring says 'var_type: TypeInfo (INTEGER, SINGLE, DOUBLE, STRING) or VarType enum' but only checks TypeInfo

**Affected files:**
- `src/resource_limits.py`

**Details:**
Docstring:
"Args:
    value: The actual value (number, string, array)
    var_type: TypeInfo (INTEGER, SINGLE, DOUBLE, STRING) or VarType enum"

But implementation only checks:
if var_type == TypeInfo.INTEGER:
if var_type == TypeInfo.SINGLE:
if var_type == TypeInfo.DOUBLE:
if var_type == TypeInfo.STRING:

No handling for 'VarType enum'. Either:
1. Remove 'or VarType enum' from docstring
2. Add handling for VarType enum in code

---

#### code_vs_comment

**Description:** renumber_with_spacing_preservation docstring says 'AST is the single source of truth' but then says 'Text is regenerated from AST by position_serializer'

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring:
"AST is the single source of truth. This function:
1. Updates line numbers in the AST
2. Updates all line number references (GOTO, GOSUB, etc.)
3. Adjusts token column positions to account for line number length changes
4. Text is regenerated from AST by position_serializer"

Point 4 is misleading - this function doesn't regenerate text, it only updates the AST. The caller must call position_serializer separately. Should say:
"4. Text can then be regenerated from updated AST by position_serializer"

---

#### code_vs_comment

**Description:** Docstring for get_array_element() says 'optionally tracking read access' but token parameter determines tracking, not optional behavior

**Affected files:**
- `src/runtime.py`

**Details:**
Docstring says:
"Get array element value, optionally tracking read access."

But the implementation shows:
```python
# Track read access if token is provided
if token is not None:
    # Track at array level (for variables window display)
    tracking_info = {...}
```

The tracking is not 'optional' in the sense of a flag - it's determined by whether token is provided. The wording suggests there might be a parameter to control tracking, but there isn't.

---

#### documentation_inconsistency

**Description:** Module docstring lists 'case_variants' in variable storage but implementation uses '_variable_case_variants' as separate dict

**Affected files:**
- `src/runtime.py`

**Details:**
Module docstring at top:
"Variable storage (PRIVATE - use get_variable/set_variable methods)
Each variable is stored as: name_with_suffix -> {'value': val, 'last_read': {...}, 'last_write': {...}, 'original_case': str, 'case_variants': [...]}"

But implementation shows:
```python
self._variables = {}  # name_with_suffix -> {'value': val, 'last_read': {...}, 'last_write': {...}, 'original_case': str}
self._variable_case_variants = {}  # Maps normalized name (lowercase) to list of all case variants
```

The 'case_variants' is not stored in each variable entry, but in a separate tracking dict.

---

#### code_vs_comment

**Description:** Comment says 'Note: Type defaults (DEFINT, DEFSNG, etc.) are handled by parser' but _resolve_variable_name() accepts def_type_map parameter

**Affected files:**
- `src/runtime.py`

**Details:**
Comment at line ~100:
"# Note: Type defaults (DEFINT, DEFSNG, etc.) are handled by parser's def_type_map
# at parse time (Parser class), not at runtime"

But _resolve_variable_name() method:
```python
@staticmethod
def _resolve_variable_name(name, type_suffix, def_type_map=None):
    # ...
    # No explicit suffix - check DEF type map
    if def_type_map:
        first_letter = name[0]
        if first_letter in def_type_map:
            from parser import TypeInfo
            var_type = def_type_map[first_letter]
```

The runtime does handle DEF type defaults via def_type_map parameter, contradicting the comment that says it's only handled at parse time.

---

#### code_vs_comment

**Description:** Missing 'stmt' field in FOR loop example in get_execution_stack() docstring

**Affected files:**
- `src/runtime.py`

**Details:**
The docstring example shows:
"Example with nested control flow:
[
    {'type': 'FOR', 'var': 'I', 'current': 1, 'end': 10, 'step': 1, 'line': 100},
    {'type': 'GOSUB', 'from_line': 130, 'return_line': 130},
    {'type': 'WHILE', 'line': 500}
]"

But the documented FOR loop structure includes:
"For FOR loops:
{
    'type': 'FOR',
    'var': 'I',
    'current': 5,
    'end': 10,
    'step': 1,
    'line': 100,
    'stmt': 0             # Statement offset
}"

The example is missing the 'stmt' field that is documented and implemented in the actual code.

---

#### code_vs_comment

**Description:** Missing 'return_stmt' field in GOSUB example in get_execution_stack() docstring

**Affected files:**
- `src/runtime.py`

**Details:**
The docstring example shows:
"{'type': 'GOSUB', 'from_line': 130, 'return_line': 130}"

But the documented GOSUB structure includes:
"For GOSUB calls:
{
    'type': 'GOSUB',
    'from_line': 60,
    'return_line': 60,
    'return_stmt': 0      # Statement offset to return to
}"

The example is missing the 'return_stmt' field that is documented and implemented in the actual code.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for statement offset indexing in docstrings

**Affected files:**
- `src/runtime.py`

**Details:**
In set_breakpoint() docstring:
"stmt_offset: Optional statement offset (0-based). If None, breaks on entire line."
"set_breakpoint(100, 2)        # Statement-level (line 100, 3rd statement)"

This shows stmt_offset=2 refers to the "3rd statement" (1-based description) but the parameter is described as "0-based". While technically correct (offset 2 = 3rd item), the mixed terminology could be confusing. The same pattern appears in get_gosub_stack() docstring:
"- line 500, statement 2 (third statement on line 500)"

Consistency in describing offsets vs ordinal positions would improve clarity.

---

#### code_vs_comment_conflict

**Description:** Comment says 'Tab key is used for window switching in curses UI, not indentation' but there's no evidence of this in the codebase

**Affected files:**
- `src/settings_definitions.py`

**Details:**
Comment states:
# Note: Tab key is used for window switching in curses UI, not indentation
# Removed editor.tab_size setting as it's not relevant for BASIC

However, searching the codebase shows no tab_size setting was ever defined, and the curses UI implementation details aren't visible in provided files. This comment may be outdated or referring to future functionality.

---

#### code_vs_comment_conflict

**Description:** Comment claims 'Line numbers are always shown' but this is a design decision comment, not a removed setting

**Affected files:**
- `src/settings_definitions.py`

**Details:**
Comment states:
# Note: Line numbers are always shown - they're fundamental to BASIC!
# Removed editor.show_line_numbers setting as it makes no sense for BASIC

This implies a setting was removed, but there's no evidence it ever existed. The comment is more of a design rationale than documentation of removed code.

---

#### code_vs_documentation_inconsistency

**Description:** Module docstring says 'first wins doesn't make sense for keywords' but this contradicts variable handling philosophy

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
simple_keyword_case.py docstring states:
"Unlike variables, 'first wins' doesn't make sense for keywords since
the interpreter registers them at startup."

However, variables.case_conflict setting supports 'first_wins' policy. The distinction is valid but could be clearer - keywords are predefined while variables are user-defined, so the policies differ for good reason. This isn't really an inconsistency but could confuse users.

---

#### documentation_inconsistency

**Description:** Comment says 'Try to import urwid-based curses UI' but doesn't mention urwid is optional

**Affected files:**
- `src/ui/__init__.py`

**Details:**
The __init__.py has:
# Try to import urwid-based curses UI (optional dependency)
try:
    from .curses_ui import CursesBackend
    _has_curses = True
except ImportError:
    # Curses UI not available
    _has_curses = False
    CursesBackend = None

The comment mentions urwid but there's no documentation about how to install it or what happens when it's missing. Users might not know urwid is the dependency name.

---

#### code_vs_documentation_inconsistency

**Description:** AutoSaveManager docstring example shows 'get_content_callback' but parameter is named 'get_content_callback' in method signature

**Affected files:**
- `src/ui/auto_save.py`

**Details:**
Module docstring shows:
Usage:
    manager = AutoSaveManager(autosave_dir=Path.home() / '.mbasic' / 'autosave')
    manager.start_autosave('foo.bas', get_content_callback, interval=30)

Method signature:
def start_autosave(
    self,
    filepath: str,
    get_content_callback: Callable[[], str],
    interval: int = 30
):

This is actually consistent - not an inconsistency. False alarm.

---

#### code_vs_comment_conflict

**Description:** Comment says 'flatten nested settings dict for JSON storage' but the flattening is bidirectional

**Affected files:**
- `src/settings.py`

**Details:**
_flatten_settings docstring:
"""Flatten nested settings dict for JSON storage.

Converts: {'editor': {'auto_number': True}}
To: {'editor.auto_number': True}
"""

There's also _unflatten_settings that does the reverse, but the comment only explains one direction. The load() method uses unflattening but doesn't call _unflatten_settings - it directly accesses data.get('settings', {}), suggesting the stored format might already be nested, not flat. This is confusing.

---

#### Code vs Documentation inconsistency

**Description:** Settings widget footer documentation says it shows keyboard shortcuts 'instead of button widgets', but the actual footer text shows 'Enter=OK ESC/^P=Cancel ^A=Apply ^R=Reset' while the keypress handler accepts 'esc' OR 'ctrl p' for cancel.

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
Footer text: "Enter=OK  ESC/^P=Cancel  ^A=Apply  ^R=Reset"

Keypress handler:
if key == 'esc' or key == 'ctrl p':
    self._on_cancel()
    return None

The footer shows '^P' (Ctrl+P) as an alternative to ESC for cancel, but the comment in the code says '(instead of button widgets)' which doesn't explain why Ctrl+P is used. This is potentially confusing since Ctrl+P is typically 'Parse program' in the editor context.

---

#### Code vs Comment conflict

**Description:** The _add_debug_help method has a TODO comment saying 'Integrate debug commands with help system' but the method is called during initialization, suggesting incomplete implementation.

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
def _add_debug_help(self):
    """Add debug commands to help system (not yet implemented)"""
    # TODO: Integrate debug commands with help system
    pass

This method is called in _register_commands() during __init__, but does nothing. It's unclear if this is intentional (placeholder for future work) or if it should be removed.

---

#### Code vs Comment conflict

**Description:** The _on_reset method comment says 'Handle Reset to Defaults action (Ctrl+R keyboard shortcut)' but the implementation only updates widgets without actually applying the defaults to the settings system.

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
def _on_reset(self):
    """Handle Reset to Defaults action (Ctrl+R keyboard shortcut)."""
    # Set all widgets to default values
    for key, defn in SETTING_DEFINITIONS.items():
        if key in self.widgets:
            widget = self.widgets[key]

            if defn.type == SettingType.BOOLEAN:
                widget.set_state(defn.default)
            # ... etc

The method updates the widget display to show default values, but doesn't call set_setting() to actually apply them. The user would need to press Apply or OK after Reset for the defaults to take effect. This behavior should be documented in the comment.

---

#### Code vs Documentation inconsistency

**Description:** The _create_setting_widget method creates radio buttons for ENUM settings and strips 'force_' prefix for display, but the comment doesn't explain why this prefix stripping is necessary or what it means.

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
Code shows:
# Create display label (strip force_ prefix for cleaner display)
display_label = choice.replace('force_', '')
rb = urwid.RadioButton(group, display_label, state=(choice == current_value))
# Store the actual value as user_data for later retrieval
rb._actual_value = choice

The comment says 'for cleaner display' but doesn't explain what 'force_' means in the context of enum choices. This suggests there's a naming convention for enum values that isn't documented.

---

#### code_vs_comment

**Description:** Comment in _parse_line_numbers() mentions 5-char formatting but code doesn't use it consistently

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _parse_line_numbers() method:
Comment says: "line_num_formatted = f"{num_str:>5}""

This suggests 5-char right-justified formatting is used, but elsewhere in the same method and in _format_line(), variable-width formatting is used. The code is inconsistent about whether it uses fixed or variable width.

---

#### code_vs_comment

**Description:** Comment says 'target_column=7 for code area' but variable width would make this incorrect

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _sort_and_position_line() method:
"target_column: Column to position cursor at (default: 7 for code area)"

If line numbers are variable width (as claimed elsewhere), column 7 would not consistently be the code area. For a 3-digit line number like '100', the code area would start at column 5 (status + '100' + space). For a 1-digit line number like '5', it would be at column 3.

---

#### code_vs_comment

**Description:** Comment says 'SNNNNN CODE' format but code doesn't pad line numbers to 5 digits

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _format_line() docstring:
"Returns:
    Formatted string or urwid markup: 'SNNNNN CODE' with optional highlighting"

But the actual code does:
line_num_str = f"{line_num}"
prefix = f"{status}{line_num_str} "

This produces 'S10 CODE' not 'S00010 CODE'. The NNNNN notation suggests 5-digit padding which isn't implemented.

---

#### code_vs_comment

**Description:** Comment in _update_display() describes format inconsistently with implementation

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment says:
"Format: 'SNN ' where S=status (1 space), NN=line# (variable), space (1)"

The notation 'NN' suggests 2 digits, but the comment says 'variable'. This is confusing notation. Should either say 'S<num> ' or 'SN+ ' to indicate variable-length number.

---

#### code_vs_comment

**Description:** Comment says toolbar removed but method still exists

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~155: '# Toolbar removed from UI layout - use Ctrl+U menu instead for keyboard navigation\n# (_create_toolbar method still exists but is not called)'
The _create_toolbar method is defined (lines ~130-175) but never called. This is intentional per the comment, but creates dead code that should potentially be removed entirely rather than kept with a comment.

---

#### code_vs_comment

**Description:** Comment about 'immediate mode executor' but unclear what immediate mode is

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple references to 'immediate mode' and 'ImmediateExecutor' but no clear documentation of what immediate mode is vs regular execution mode. Comments mention:
- 'Initialize immediate mode executor' (line ~85)
- 'Immediate mode UI widgets' (line ~73)
- 'immediate mode input field' (line ~195)

But there's no high-level comment explaining the distinction between immediate mode and program execution mode, making the architecture unclear.

---

#### code_vs_comment

**Description:** Comment says 'Use unlimited limits for immediate mode' but unclear why

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~66: '# Use unlimited limits for immediate mode (runs will use local limits)'
This suggests immediate mode has different resource limits than program runs, but there's no explanation of why this design choice was made or what the implications are. The distinction between 'immediate mode limits' and 'run limits' is not documented.

---

#### code_vs_comment

**Description:** Comment about PC setting timing is confusing and potentially misleading

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _setup_program() around line 1070:
Comment: '# If start_line is specified, set PC AFTER start() has called setup()'
Comment: '# because setup() resets PC to first line'

This comment suggests setup() resets PC, but the actual method called is start() on the interpreter. The comment should clarify whether it's interpreter.start() or runtime.setup() that resets PC, as the wording is ambiguous.

---

#### code_vs_comment

**Description:** Comment says 'Urwid will redraw automatically' but code elsewhere forces draw_screen()

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_output() around line 1330:
Comment: '# Urwid will redraw automatically - no need to force draw_screen()'

But in _update_output_with_lines() around line 1350:
Code: 'if hasattr(self, 'loop') and self.loop and self.loop_running:'
Code: '    self.loop.draw_screen()'

This inconsistency suggests either the comment is wrong (urwid doesn't always redraw automatically) or the explicit draw_screen() call is unnecessary. The two similar methods have different approaches.

---

#### internal_inconsistency

**Description:** Inconsistent error handling between user errors and internal errors

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _execute_tick() around line 1180:
The code has two different error handling paths:
1. User program errors (is_user_error=True): Don't log to stderr, format nicely
2. Internal errors: Log to stderr with debug_log_error()

However, the distinction relies on checking 'state.error_info is not None' which may not reliably distinguish between user errors and internal errors. An internal error could also set error_info, making the classification unreliable.

---

#### code_vs_comment

**Description:** Comment about 'dummy handler' is misleading

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _set_variables_filter() around line 890:
Code: 'urwid.connect_signal(edit, 'change', lambda _w, _t: None)  # dummy handler'

The comment says 'dummy handler' but doesn't explain why a dummy handler is needed or what it's for. This makes the code's intent unclear. If it's truly dummy/unused, it should be removed or the comment should explain its purpose.

---

#### code_vs_comment

**Description:** Comment says 'No state checking - just ask the interpreter' but this is misleading about what has_work() does

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment: '# Check if interpreter has work to do (after RUN statement)
# No state checking - just ask the interpreter
has_work = self.interpreter.has_work() if self.interpreter else False'

The comment 'No state checking' is confusing because has_work() itself likely checks internal interpreter state. The comment seems to mean 'no external state checking' but is unclear.

---

#### code_vs_comment

**Description:** Comment says 'This is what the tick loop does after executing a statement' but doesn't verify this is actually true

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment: '# If statement set NPC (like RUN/GOTO), move it to PC
# This is what the tick loop does after executing a statement'

This comment makes a claim about tick loop behavior without verification. If the tick loop behavior changes, this comment could become outdated.

---

#### code_vs_comment

**Description:** Docstring example shows {{kbd:help}} but implementation shows it searches all sections, not just a 'help' section

**Affected files:**
- `src/ui/help_macros.py`

**Details:**
help_macros.py lines 7-8:
"Example:
  {{kbd:help}} → looks up 'help' key in keybindings for current UI"

help_macros.py lines 95-102:
"def _expand_kbd(self, key_name: Optional[str]) -> str:
    ...
    # Search in all sections of keybindings
    for section_name, section in self.keybindings.items():
        if key_name in section:
            return section[key_name]['primary']"

The example suggests 'help' is a key name, but the implementation searches across all sections. The example should clarify that 'help' is an action name that exists in some section (e.g., 'editor' section).

---

#### code_vs_comment

**Description:** Comment says 'Ctrl+L is context-sensitive' but there's no CTRL_L constant defined

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py lines 260-262:
"# Note: Ctrl+L is context-sensitive in curses UI:
# - When debugging: Step Line (execute all statements on current line)
# - When editing: List program (same as LIST_KEY)"

This comment describes Ctrl+L behavior but there's no CTRL_L_KEY constant defined. The comment seems to be explaining that LIST_KEY (which is Ctrl+K according to the code) has context-sensitive behavior, but it mentions Ctrl+L instead. This is either a typo or outdated comment.

---

#### code_vs_documentation

**Description:** HelpMacros._expand_macro returns hardcoded version '5.21' but this should likely come from a config or constant

**Affected files:**
- `src/ui/help_macros.py`

**Details:**
help_macros.py lines 68-69:
"elif name == 'version':
    return "5.21"  # MBASIC version"

The version is hardcoded in the macro expansion. This should probably come from a central version constant or config file to avoid version mismatches across the codebase.

---

#### code_vs_comment

**Description:** Docstring says 'Search across three-tier help system' but the code shows four tier labels (Language, MBASIC, UI, Other)

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
help_widget.py lines 4-9:
"Provides:
- Up/Down scrolling through help content
- Enter to follow links
- ESC/Q to exit
- Navigation breadcrumbs
- Search across three-tier help system (/)"

help_widget.py lines 96-99 and 115-120 show four tiers: Language (📕), MBASIC (📗), UI (📘), and Other (📙).

The docstring should say 'four-tier' or list the actual tiers.

---

#### code_vs_documentation

**Description:** KEYBINDINGS_BY_CATEGORY shows 'Shift+Ctrl+V' for Save As and 'Shift+Ctrl+O' for Recent files, but these are not defined as constants

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py lines 289-294:
"'Program Management': [
    (RUN_DISPLAY, 'Run program'),
    (NEW_DISPLAY, 'New program'),
    (OPEN_DISPLAY, 'Open/Load program'),
    (SAVE_DISPLAY, 'Save program'),
    ('Shift+Ctrl+V', 'Save As'),
    ('Shift+Ctrl+O', 'Recent files'),
]"

These keybindings are hardcoded in the documentation but not defined as constants like the others. They should either be defined as constants (SAVE_AS_DISPLAY, RECENT_FILES_DISPLAY) or loaded from the JSON config.

---

#### code_vs_comment

**Description:** Comment says 'title=None creates border without title text (still has top border line)' but this is misleading - title=None creates a LineBox with no title, which is the standard behavior

**Affected files:**
- `src/ui/keymap_widget.py`

**Details:**
Line 48-49:
# Wrap in line box with black background
# title=None creates border without title text (still has top border line)
linebox = urwid.LineBox(
    urwid.AttrMap(self.listbox, 'body'),
    title=None
)

The comment suggests something special about title=None, but this is just the default LineBox behavior. The comment is unnecessarily explanatory.

---

#### code_vs_documentation

**Description:** Help browser implements ESC key to close in-page search but this is not documented in tk_keybindings.json

**Affected files:**
- `src/ui/tk_help_browser.py`
- `src/ui/tk_keybindings.json`

**Details:**
tk_help_browser.py line 91:
self.inpage_search_entry.bind('<Escape>', lambda e: self._inpage_search_close())

tk_keybindings.json has no entry for ESC in help_browser section

---

#### code_duplication

**Description:** Both files implement _format_table_row() with identical logic - code duplication without shared utility

**Affected files:**
- `src/ui/markdown_renderer.py`
- `src/ui/tk_help_browser.py`

**Details:**
markdown_renderer.py lines 107-127:
def _format_table_row(self, line: str) -> str:
    """Format a markdown table row for terminal display."""
    parts = [p.strip() for p in line.strip().split('|')]
    parts = [p for p in parts if p]
    if all(set(p) <= set('-: ') for p in parts):
        return ''
    formatted_parts = []
    for part in parts:
        part = re.sub(r'\*\*([^*]+)\*\*', r'\1', part)
        part = re.sub(r'`([^`]+)`', r'\1', part)
        formatted_parts.append(part.ljust(15))
    return '  '.join(formatted_parts)

tk_help_browser.py lines 569-585:
def _format_table_row(self, line: str) -> str:
    """Format a markdown table row for display."""
    parts = [p.strip() for p in line.strip().split('|')]
    parts = [p for p in parts if p]
    if all(set(p) <= set('-: ') for p in parts):
        return ''
    formatted_parts = []
    for part in parts:
        part = re.sub(r'\*\*([^*]+)\*\*', r'\1', part)
        part = re.sub(r'`([^`]+)`', r'\1', part)
        formatted_parts.append(part.ljust(15))
    return '  '.join(formatted_parts)

Identical implementation should be extracted to shared utility

---

#### code_vs_comment

**Description:** Docstring says 'Note: Not thread-safe (no locking mechanism)' but this is obvious from the implementation and doesn't add value

**Affected files:**
- `src/ui/recent_files.py`

**Details:**
Lines 11-12:
- Records full path and last access timestamp
- Automatically creates config directory if needed
- Cross-platform (uses pathlib)
- Note: Not thread-safe (no locking mechanism)

This note is unnecessary as thread-safety is not claimed and most Python file I/O operations are not thread-safe by default unless explicitly stated.

---

#### code_vs_comment

**Description:** Comment says 'Allow menu to be dismissed' but the code that follows doesn't actually dismiss the menu - it just sets up bindings

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Lines 543-545:
# Allow menu to be dismissed
def dismiss_menu():
    try:
        menu.unpost()
    except:
        pass

The comment is placed before the dismiss_menu function definition, but the actual dismissal setup happens later (lines 552-554). The comment placement is misleading.

---

#### code_vs_comment

**Description:** Comment says 'Release grab immediately (tk_popup handles menu interaction)' but there's no explicit grab_release() call - it's in the finally block

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Lines 547-551:
try:
    menu.tk_popup(event.x_root, event.y_root)
finally:
    # Release grab immediately (tk_popup handles menu interaction)
    menu.grab_release()

The comment says 'tk_popup handles menu interaction' but then explicitly calls grab_release(), which contradicts the implication that tk_popup handles it automatically.

---

#### code_vs_comment

**Description:** Comment says dialog is 'non-blocking' but implementation uses grab_set() which blocks input to other windows

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Line 33 comment: '# Make modal (grab input focus, but non-blocking - no wait_window())'
Line 34 code: 'self.grab_set()'

The comment claims the dialog is 'non-blocking' because it doesn't call wait_window(), but grab_set() still makes it modal by blocking input to other windows in the application. The dialog is modal (blocks other windows) but doesn't block code execution (no wait_window). The comment is misleading about what 'non-blocking' means in this context.

---

#### code_vs_comment

**Description:** Comment describes inline help as 'not a hover tooltip' but doesn't explain what it actually is

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Line 157 comment: '# Show short help as inline label (not a hover tooltip, just a gray label)'

The comment emphasizes what it's NOT (a hover tooltip) rather than clearly describing what it IS. This is confusing and suggests the comment may have been written during refactoring when tooltips were replaced with labels. The parenthetical clarification seems defensive rather than descriptive.

---

#### code_internal_inconsistency

**Description:** Redundant type checking in _get_current_widget_values method

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Lines 177-182:
    for key, widget in self.widgets.items():
        if isinstance(widget, tk.Variable):
            values[key] = widget.get()
        else:
            values[key] = widget.get()

Both branches of the if/else statement do exactly the same thing (widget.get()). The isinstance check serves no purpose and suggests incomplete refactoring or misunderstanding of the widget storage pattern. All items in self.widgets are tk.Variable instances based on the _create_setting_widget implementation.

---

#### documentation_inconsistency

**Description:** Module docstring claims to provide 'a GUI dialog' but class can create multiple instances

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Module docstring (lines 1-5): 'Provides a GUI dialog for modifying settings.'

The singular 'a GUI dialog' suggests a singleton pattern, but the SettingsDialog class can be instantiated multiple times with no prevention mechanism. The docstring should say 'GUI dialogs' (plural) or 'a GUI dialog class' to be accurate.

---

#### code_vs_comment

**Description:** Comment about dummy widgets contradicts their actual usage

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment says: '# Create dummy immediate_history and immediate_status for compatibility
# (some code still references these)'

But then sets: 'self.immediate_history = None' and 'self.immediate_status = None'

If code references these, setting them to None would cause AttributeError. Either the comment is wrong about code referencing them, or the implementation should provide actual dummy objects instead of None.

---

#### code_vs_comment

**Description:** Comment about removed utility buttons references wrong menu paths

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment says: '# Utility buttons removed - use menus instead:
# - List → Run > List Program
# - Clear Prog → File > New
# - Clear Out → Run > Clear Output'

But the menu creation code shows 'Clear Output' is at 'Run > Clear Output' which matches, but there's no evidence these buttons were ever in the toolbar. The comment may be outdated or from a different version.

---

#### code_vs_comment

**Description:** Comment about arrow click width doesn't match variable name

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment says: '# Click on arrow area (left 20 pixels) = toggle sort direction'

But constant is named: 'ARROW_CLICK_WIDTH = 20'

The comment describes behavior (left 20 pixels) while the constant name suggests it's a width. These are semantically the same but the naming could be clearer (e.g., ARROW_CLICK_THRESHOLD).

---

#### documentation_inconsistency

**Description:** Docstring example code references undefined variables

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Usage example in class docstring:

'from src.iohandler.console import ConsoleIOHandler
from editing import ProgramManager
from src.ui.tk_ui import TkBackend

io = ConsoleIOHandler()
program = ProgramManager(def_type_map)'

The variable 'def_type_map' is not defined in the example. Should either define it or explain where it comes from.

---

#### code_vs_comment

**Description:** Comment about keyboard shortcut binding location is misleading

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment in _create_menu: '# Note: Ctrl+I is bound in start() after editor is created'

But in start() method, the binding is: 'self.editor_text.text.bind('<Control-i>', self._on_ctrl_i)'

The comment says 'in start()' but doesn't clarify it's bound to the editor text widget specifically, not the root window. This could be confusing when debugging keybinding issues.

---

#### code_vs_comment

**Description:** Docstring says 'Edit any array element by typing subscripts' but implementation shows last accessed element by default

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring at line ~68:
"""Edit any array element by typing subscripts.

Args:
    variable_name: Array name with type suffix (e.g., "A%")
    type_suffix: Type character ($, %, !, #, or empty)
    value_display: Display string like "Array(10x10) [5,3]=42"
"""

The docstring doesn't mention that the dialog pre-fills with the last accessed subscripts and value, which is a key feature shown in the code at lines ~85-88 and ~95-105.

---

#### code_vs_comment

**Description:** Comment says 'No formatting is applied' but code does apply formatting in some contexts

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment in _refresh_editor at line ~1009:
# Insert line exactly as stored - no formatting
# This preserves compatibility with real MBASIC

However, in _update_variables (lines ~600-650), the code formats numbers naturally:
if var['type_suffix'] != '$' and isinstance(value, (int, float)) and value == int(value):
    value = str(int(value))

And in _update_stack (lines ~850-870), similar formatting is applied. The comment is misleading about 'no formatting' being a universal principle.

---

#### code_vs_comment

**Description:** Comment says 'immediate per-line validation' but implementation validates on multiple triggers

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment in _validate_editor_syntax at line ~1090:
# Check each line independently (immediate per-line validation)

But the method is called from multiple places:
- _on_cursor_move (line ~1150): after 100ms delay
- _on_mouse_click (line ~1160): after 100ms delay
- _on_focus_out (line ~1170): on focus loss

The validation is not truly 'immediate' but delayed/batched, and the comment doesn't reflect this.

---

#### code_vs_comment

**Description:** Docstring says 'Sync program to runtime without resetting PC' but code explicitly sets PC to halted when not running

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring in _sync_program_to_runtime at line ~1040:
"""Sync program to runtime without resetting PC.

Updates runtime's statement_table and line_text_map from self.program,
but preserves current PC/execution state.
"""

But code at lines ~1070-1075:
else:
    # No execution in progress - ensure halted
    self.runtime.pc = PC.halted_pc()
    self.runtime.halted = True

The method does reset PC to halted when not running, contradicting the 'without resetting PC' claim. The docstring should clarify this conditional behavior.

---

#### code_vs_comment

**Description:** Inconsistent comment style for 'Fixed' annotations

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In cmd_cont(), inline comments use '# Fixed: was X' format:
self.running = True  # Fixed: was self.is_running
self._execute_tick()  # Fixed: was self._tick()

This style is not used elsewhere in the file for similar corrections, making it unclear if this is a recent fix or historical note.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate() says 'don't echo the command or add Ok' but doesn't explain why

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment: '# Execute (don't echo the command or add "Ok" - just show results)'

This is a design decision that differs from typical BASIC immediate mode behavior (which does echo commands and show 'Ok'). The comment states what NOT to do but doesn't explain the rationale, making it unclear if this is intentional or a TODO.

---

#### code_vs_comment

**Description:** Comment in _on_key_press() explains clearing statement highlight to prevent 'half yellow line' issue but doesn't explain what causes it

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment: '# Clear yellow statement highlight when user starts editing
# This prevents the "half yellow line" issue when editing error/breakpoint lines'

The comment mentions a specific visual bug ('half yellow line') but doesn't explain:
1. What causes the half yellow line
2. Why clearing on key press fixes it
3. Whether this is a workaround or proper fix

---

#### code_vs_comment

**Description:** Comment in _check_line_change() has complex logic explanation that may be outdated after refactoring

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment: '# Trigger sort if:
# 1. Line number changed on existing line (both old and new are not None), OR
# 2. Line number was removed (old was not None, new is None and line has content)
# DON'T sort if just clicking around without editing (old is None means we're just tracking)'

The logic is complex and the comment suggests it evolved over time ('DON'T sort if just clicking around' implies this was a bug). The comment doesn't explain:
1. Why old_line_num being None means 'just tracking'
2. Whether this is the final design or still has edge cases
3. What 'clicking around' means specifically

---

#### code_vs_comment

**Description:** TkIOHandler.clear_screen() comment says GUI output not clearable, but this may be outdated

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Method comment: "Clear screen - no-op for Tk UI (GUI output not clearable like terminal)."
However, GUI text widgets in Tkinter ARE clearable (using widget.delete('1.0', tk.END)). The comment suggests a design decision rather than a technical limitation, but doesn't explain why clearing is not desired in the GUI context.

---

#### code_vs_comment

**Description:** Comment about INPUT statement parsing is ambiguous

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In TkIOHandler.input() docstring: "Used by INPUT statement to read user input (raw string). Comma-separated parsing happens at interpreter level."
This comment suggests that input() returns a raw string and comma parsing is done elsewhere. However, it's unclear if this is documenting current behavior or explaining a design decision. The method does return a raw string, so the comment is accurate, but the phrase 'Comma-separated parsing happens at interpreter level' seems like it's explaining something that might have been confusing in the past.

---

#### code_vs_comment

**Description:** Canvas width comment says '20px for one status character' but actual width is set to 20 without unit specification

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment states:
"# Width: 20px for one status character (●, ?, or space)"

But code uses:
self.canvas = tk.Canvas(
    self,
    width=20,
    ...
)

In Tkinter, the width parameter is in pixels by default, so the comment is technically correct, but the 'px' notation suggests CSS/web context rather than Tkinter convention.

---

#### code_vs_comment

**Description:** Blank line removal feature is implemented but not documented in class docstring

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
The class implements automatic blank line removal when cursor moves away from a blank line:
- _on_cursor_move() method tracks cursor movement
- _delete_line() method removes blank lines
- Bindings set up for '<KeyPress>' and '<ButtonPress-1>'

However, the class docstring only documents:
"Layout: [Status (●/?/ )][ Code with line numbers ]

Status symbols:
- ● : Breakpoint set on this line
- ? : Parse error on this line
- ' ': Normal line (no breakpoint, no error)"

The blank line removal behavior is a significant feature that affects user experience but is not mentioned in the documentation.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for line number types - 'BASIC line number' vs 'editor line' vs 'text widget line number'

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
The code uses multiple terms for different line number concepts:
- 'BASIC line number' (the actual line number in BASIC code like 10, 20, 30)
- 'editor line' (mentioned in _on_status_click)
- 'text widget line number' (mentioned in _delete_line docstring)
- 'line_num' variable used for both BASIC and Tkinter line numbers

This creates confusion. For example:
- line_metadata uses BASIC line numbers as keys
- Tkinter text widget uses 1-based sequential line numbers
- Comments don't always clarify which type is being used

---

#### code_vs_comment

**Description:** Comment in update_line_references() describes 'Two-pass regex approach' but implementation uses pattern.sub() which is single-pass, then a second pattern for commas

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment says:
"# Two-pass regex approach:
# Pass 1: Match keyword + first line number (GOTO/GOSUB/THEN/ELSE/ON...GOTO/ON...GOSUB)
# Pass 2: Match comma-separated line numbers (for ON...GOTO/GOSUB lists)"

This is technically accurate but misleading - it's not two passes over the same pattern, it's two different patterns applied sequentially. The comment could be clearer.

---

#### code_vs_documentation

**Description:** Function serialize_statement() has fallback for unknown statement types that returns 'REM {stmt_type}' but this could create invalid BASIC code

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Code at line ~1030:
else:
    # Try to reconstruct from the original source if possible
    # For now, return a placeholder
    return f"REM {stmt_type}"

Comment says "Try to reconstruct from the original source if possible" but the code doesn't actually try - it immediately returns a placeholder. This could silently corrupt programs during RENUM if new statement types are added but not handled in serialize_statement().

---

#### documentation_inconsistency

**Description:** Module docstring claims 'No UI-specific dependencies allowed' but function list_files() uses glob and os modules which are filesystem-specific

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Module docstring:
"This module contains UI-agnostic helper functions that can be used by any UI (CLI, Tk, Web, Curses). No UI-specific dependencies allowed."

Function list_files() at line ~700 imports and uses:
import glob
import os

While these aren't UI-specific, they are platform/filesystem-specific. The claim of 'no dependencies' is technically incorrect, though the spirit (no Tk/curses/web dependencies) is maintained.

---

#### code_vs_comment

**Description:** Function serialize_line() comment about preserving indentation mentions 'RELATIVE indentation' but the calculation may not handle all edge cases

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment at line ~850:
"# Preserve RELATIVE indentation (spaces after line number) from original source
# This ensures indentation survives RENUM when line numbers change width"

Code extracts indentation with:
match = re.match(r'^(\d+)(\s+)', line_node.source_text)

However, if source_text is not available or doesn't match the pattern, it falls back to relative_indent = 1. This could cause inconsistent indentation if some lines have source_text and others don't (e.g., after programmatic line insertion).

---

#### code_vs_documentation

**Description:** Function cycle_sort_mode() comment says it 'matches the Tk UI implementation' but this creates coupling between supposedly independent modules

**Affected files:**
- `src/ui/variable_sorting.py`

**Details:**
Comment at line ~25:
"The cycle order is: accessed -> written -> read -> name -> (back to accessed)
This matches the Tk UI implementation."

The module is supposed to provide common logic for ALL UIs, but the comment suggests it's specifically matching one UI's behavior. This could cause confusion if other UIs want different cycle orders.

---

#### code_vs_documentation

**Description:** Function get_sort_key_function() has fallback comment mentioning 'old type/value modes' but these modes are not documented anywhere

**Affected files:**
- `src/ui/variable_sorting.py`

**Details:**
Code at line ~75:
else:
    # Default to name sorting (unknown modes fall back to this, e.g., old 'type'/'value')
    return lambda v: v['name'].lower()

Comment mentions 'old type/value modes' but:
1. These modes are not in get_variable_sort_modes()
2. No documentation explains what these old modes were
3. No migration guide for code using old modes

This suggests incomplete refactoring or missing documentation.

---

#### code_vs_documentation

**Description:** cmd_run() docstring says 'Override or use this implementation' but the method creates Runtime and Interpreter which requires knowledge of internal structure

**Affected files:**
- `src/ui/visual.py`

**Details:**
The docstring suggests this is a usable base implementation:
"Override or use this implementation:
1. Create Runtime and Interpreter from ProgramManager
2. Run the program
3. Handle errors and display output"

However, the implementation imports 'create_local_limits' from 'resource_limits' module without showing the import at the top of the file, and uses internal attributes like 'self.program.line_asts' and 'self.program.lines' which may not be part of ProgramManager's public API. This makes it unclear if subclasses can actually 'use this implementation' as-is.

---

#### documentation_inconsistency

**Description:** Class docstring mentions 'Use self.program for program management' but doesn't document what self.program is or its type

**Affected files:**
- `src/ui/visual.py`

**Details:**
The docstring says:
"6. Use self.program for program management"

But there's no documentation of what self.program is, its type (presumably ProgramManager based on __init__ parameter), or what methods are available. The __init__ method receives 'program_manager' parameter but doesn't show it being assigned to self.program.

---

#### code_vs_documentation

**Description:** get_cursor_position() docstring says it returns placeholder but doesn't document that it's not actually functional

**Affected files:**
- `src/ui/web/codemirror5_editor.py`

**Details:**
The method docstring says:
"Get current cursor position (placeholder implementation).

Returns:
    Dict with 'line' and 'column' keys (always returns {0, 0} - not implemented)"

While it does mention 'not implemented' in parentheses, the docstring format suggests this is a working method. The comment inside says:
"# This would need async support, for now return placeholder"

This is inconsistent - a placeholder/unimplemented method should probably raise NotImplementedError or be more clearly marked as non-functional in the docstring.

---

#### code_vs_comment

**Description:** Comment about event args being dict conflicts with type hints suggesting string value

**Affected files:**
- `src/ui/web/codemirror5_editor.py`

**Details:**
In the value property getter:
"if isinstance(self._value, dict):
    # Sometimes event args are dict - return empty string
    return ''"

But the __init__ method shows:
"def _internal_change_handler(e):
    self._value = e.args  # CodeMirror sends new value as args"

The comment says 'CodeMirror sends new value as args' suggesting it should be a string, but then the property getter handles the case where it's a dict. This suggests either:
1. The event handling is buggy and sometimes receives unexpected dict values
2. The comment is wrong about what CodeMirror sends
3. There's an undocumented edge case

---

#### code_vs_comment

**Description:** Comment says input handler 'already echoes the input with newline' but SimpleWebIOHandler.input() doesn't echo anything

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In SimpleWebIOHandler.input() method (lines 60-70):
Comment says: '# The inline input handler already echoes the input with newline\n# So we don't need to echo it again here'
But the input() method code shows:
```
def input(self, prompt=""):
    # Don't print prompt here - _enable_inline_input will add it
    # Get input from UI (this will block until user enters input)
    result = self.input_callback(prompt)
    # The inline input handler already echoes the input with newline
    # So we don't need to echo it again here
    return result
```
The method doesn't call self.output() to echo anything. The comment suggests echoing happens elsewhere (_enable_inline_input), but this creates confusion about where echoing actually occurs.

---

#### code_vs_comment

**Description:** Docstring says 'Uses asyncio.Future for coordination' but no Future is visible in the code

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In SimpleWebIOHandler.input() docstring (lines 54-59):
"""Get input from user via inline input field.

Uses asyncio.Future for coordination between synchronous interpreter
and async web UI. The input field appears below the output pane,
allowing users to see all previous output while typing.
"""
The method implementation doesn't show any asyncio.Future usage:
```
def input(self, prompt=""):
    result = self.input_callback(prompt)
    return result
```
The Future coordination likely happens inside input_callback, but the docstring makes it sound like it's in this method.

---

#### code_vs_comment

**Description:** Comment about 'Content change handlers via CodeMirror's on_change callback' is incomplete

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
At line 1046-1053:
```
# Content change handlers via CodeMirror's on_change callback
# The _on_editor_change method (defined below) handles:
# - Removing blank lines
# - Auto-numbering
# - Placeholder clearing

# Click and blur handlers registered separately
self.editor.on('click', self._on_editor_click, throttle=0.05)
self.editor.on('blur', self._on_editor_blur)
```
The comment says '_on_editor_change method (defined below)' but the method definition is not shown in the provided code snippet. This makes it impossible to verify if the listed behaviors are actually implemented.

---

#### documentation_inconsistency

**Description:** Module docstring mentions 'Breakpoint support' but no breakpoint-related code is visible

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Class docstring (lines 906-922) lists features:
"Features:
- Web-based interface accessible via browser
- Modern, responsive design
- Split-pane editor and output
- Menu system
- File management
- Execution controls
- Variables window
- Breakpoint support

Based on TK UI feature set (see docs/dev/TK_UI_FEATURE_AUDIT.md)."

The 'Breakpoint support' feature is mentioned but no breakpoint-related methods, UI elements, or functionality is shown in the provided code. This could mean the feature is not yet implemented or the code is incomplete.

---

#### code_vs_comment

**Description:** Comment about 'Current line indicator' is incomplete/cut off

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
At line 1056, the code ends with:
```
# Current line indicator
```
This comment appears to be incomplete as there's no code following it. The file seems to be truncated or the comment is orphaned from a code block that was removed.

---

#### code_vs_comment

**Description:** Comment says 'matches Tk UI defaults' but no verification of what those defaults are

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In VariablesDialog.__init__ (lines 118-120):
```
# Sort state (matches Tk UI defaults)
self.sort_mode = 'accessed'  # Current sort mode
self.sort_reverse = True  # Sort direction
```
The comment claims these values match 'Tk UI defaults' but there's no reference to where these defaults are defined or documented. Without seeing the Tk UI code or documentation, this claim cannot be verified.

---

#### code_vs_comment

**Description:** Comment mentions inline input handling but implementation uses immediate_entry input box

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~142-145: Comments mention 'inline input handling' and 'inline input in output textarea'
Line ~147: 'Set up Enter key handler for inline input in output textarea'
But in _handle_step_result() and _execute_tick(), the code focuses immediate_entry input box:
self.immediate_entry.props('placeholder="Input: "')
self.immediate_entry.run_method('focus')
The implementation doesn't use inline editing in the output textarea.

---

#### code_vs_comment

**Description:** Comment says 'interpreter/runtime reused to preserve session state' but runtime is reset

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~1283 in _menu_step_line(): '# Create new IO handler for execution (interpreter/runtime reused to preserve session state)'
But line ~1291: 'self.runtime.reset_for_run(self.program.line_asts, self.program.lines)'
The reset_for_run() call contradicts 'reused to preserve session state' - it resets the runtime state.

---

#### code_vs_comment

**Description:** Comment says 'Don't append prompt' but unclear if this is correct behavior

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~1207 and ~1223 in _execute_tick(): '# Don't append prompt - interpreter already printed it via io.output()'
This comment appears twice when handling input_prompt state. However, it's unclear if the interpreter actually prints the prompt or if this is an assumption that may not hold.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate says 'Don't sync editor from AST' but this is architectural explanation, not describing what code does

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment block starting with '# Don't sync editor from AST after immediate command - editor text is the source!' is actually explaining the overall architecture (editor text → AST → execution) rather than describing what the code at that location does. The comment is correct but placed where it might confuse readers looking for what the next code block does.

---

#### code_vs_comment

**Description:** Comment in _remove_blank_lines says 'except the current line where cursor is' but implementation keeps last line regardless

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Docstring: 'Remove blank lines from editor except the current line where cursor is. This prevents removing the blank line user just created with Enter.'

Code:
```
for i, line in enumerate(lines):
    if line.strip() or i == len(lines) - 1:
        non_blank_lines.append(line)
```

The code keeps the last line even if blank, but doesn't actually check cursor position. It assumes cursor is on last line, which may not always be true if user clicks elsewhere.

---

#### code_vs_comment

**Description:** Comment about CP/M EOF marker handling mentions specific characters but doesn't explain why

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _save_editor_to_program():
```
# Normalize line endings and remove CP/M EOF markers
# \r\n -> \n (Windows line endings)
# \r -> \n (old Mac line endings)
# \x1a (Ctrl+Z, CP/M EOF marker)
text = text.replace('\r\n', '\n').replace('\r', '\n').replace('\x1a', '')
```

The comment explains what each character is but doesn't explain why CP/M EOF markers would appear in a web editor. This seems like legacy code from a file-loading context that may not be relevant for web textarea input.

---

#### documentation_inconsistency

**Description:** Inconsistent help key documentation

**Affected files:**
- `docs/help/common/editor-commands.md`
- `docs/help/common/getting-started.md`

**Details:**
editor-commands.md shows '**F1** or **H**' for opening help, while getting-started.md references '^P' (Ctrl+P) in the Quick Start section: '**^P** - Show this help'. The index.md also shows '^P' for help.

---

#### code_comment_conflict

**Description:** Comment describes deprecated class but implementation still functional

**Affected files:**
- `src/ui/web_help_launcher.py`

**Details:**
The comment says '# Legacy class kept for compatibility - new code should use direct web URL instead' and the class is named 'WebHelpLauncher_DEPRECATED', but the class has a full implementation with methods like _build_help(), _start_help_server(), etc. The comment suggests it's deprecated but the code is complete and functional.

---

#### documentation_inconsistency

**Description:** Inconsistent menu shortcut documentation

**Affected files:**
- `docs/help/common/index.md`
- `docs/help/common/editor-commands.md`

**Details:**
index.md shows '**^X** - Open menu' in Quick Start, but editor-commands.md doesn't document this shortcut anywhere in its tables.

---

#### code_vs_documentation

**Description:** Version information not referenced in documentation

**Affected files:**
- `src/version.py`
- `docs/help/common/compiler/optimizations.md`

**Details:**
version.py contains VERSION = '1.0.653' and detailed version information including PROJECT_NAME = 'MBASIC-2025' and MBASIC_VERSION = '5.21', but none of the documentation files reference or display this version information to users.

---

#### documentation_inconsistency

**Description:** Missing visual backend clarification in main help index

**Affected files:**
- `docs/help/README.md`
- `docs/help/common/index.md`

**Details:**
README.md states '**Note:** The visual backend is part of the web UI implementation.' but common/index.md doesn't mention this or provide any guidance about the visual backend vs web UI distinction.

---

#### code_comment_conflict

**Description:** Stderr debug output in production code

**Affected files:**
- `src/ui/web_help_launcher.py`

**Details:**
The open_help_in_browser() function contains multiple sys.stderr.write() calls for debugging (e.g., 'sys.stderr.write(f"BROWSER ERROR: No browser available - {e}\n")'), which suggests this is debug code that should either be removed or converted to proper logging.

---

#### documentation_inconsistency

**Description:** ASCII table shows DEL (127) in two different locations

**Affected files:**
- `docs/help/common/language/appendices/ascii-codes.md`

**Details:**
The ASCII codes documentation shows DEL (decimal 127, hex 7F) in two places:
1. In the 'Printable Characters (32-126)' table at position Dec 127, Hex 7F
2. In a separate 'Special Character: DEL' section

DEL is technically not a printable character and should only appear in the special section, not in the printable characters table.

---

#### documentation_inconsistency

**Description:** CVI/CVS/CVD documentation has incomplete example and broken reference

**Affected files:**
- `docs/help/common/language/functions/cvi-cvs-cvd.md`

**Details:**
The example in cvi-cvs-cvd.md is incomplete:
'70 FIELD #1,4 AS N$, 12 AS B$, •••
80 GET #1
90 Y=CVS (N$)
See also MKI$r MKS$, MKD$, Section 3.25 and Appendix B.'

The example uses '•••' placeholder and the 'See also' text references 'Section 3.25 and Appendix B' which don't exist in this documentation structure. Also 'MKI$r' appears to be a typo for 'MKI$,'.

---

#### documentation_inconsistency

**Description:** EOF example code is incomplete

**Affected files:**
- `docs/help/common/language/functions/eof.md`

**Details:**
The example in eof.md is incomplete:
'10 OPEN "I",l,"DATA"
20 C=O
30 IF EOF(l) THEN 100
40 INPUT #l,M(C)
50 C=C+l:GOTO 30'

The example doesn't show line 100 or any closing of the file, making it an incomplete example. Also uses lowercase 'l' for file number which could be confused with '1'.

---

#### documentation_inconsistency

**Description:** HEX$ example has formatting issues

**Affected files:**
- `docs/help/common/language/functions/hex_dollar.md`

**Details:**
In hex_dollar.md example:
'30 PRINT X "DECIMAL IS II A$ " HEXADECIMAL II'

The string concatenation syntax appears malformed with 'II' instead of proper quote marks or semicolons. Should likely be:
'30 PRINT X; "DECIMAL IS "; A$; " HEXADECIMAL"'

---

#### documentation_inconsistency

**Description:** Character set documentation mentions version-dependent underscore support without clarification

**Affected files:**
- `docs/help/common/language/character-set.md`

**Details:**
In character-set.md:
'_ | Underscore | Allowed in variable names (some versions)'

This states underscore is allowed 'in some versions' but doesn't clarify which versions (8K, Extended, Disk) support it, creating ambiguity for users.

---

#### documentation_inconsistency

**Description:** INKEY$ documentation states Control-C terminates the program, but adds a note that with BASIC Compiler it's passed through. This creates ambiguity about the current interpreter's behavior.

**Affected files:**
- `docs/help/common/language/functions/inkey_dollar.md`

**Details:**
Documentation states: 'No characters will be echoed and all characters are passed through to the program except for Control-C, which terminates the program. (With the BASIC Compiler, Control-C is also passed through to the program.)'

This is unclear for the Python implementation - which behavior is implemented?

---

#### documentation_inconsistency

**Description:** INP documentation references 'Section 2.47' for OUT statement, but uses relative path links elsewhere

**Affected files:**
- `docs/help/common/language/functions/inp.md`

**Details:**
Documentation states: 'INP is the complementary function to the OUT statement, Section 2.47.'

Other docs use markdown links like [OUT](../statements/out.md) instead of section numbers.

---

#### documentation_inconsistency

**Description:** INPUT$ documentation states Control-C interrupts execution, while INKEY$ says it terminates the program

**Affected files:**
- `docs/help/common/language/functions/input_dollar.md`

**Details:**
INPUT$ doc: 'all control characters are passed through except Control-C, which is used to interrupt the execution of the INPUT$ function.'

INKEY$ doc: 'all characters are passed through to the program except for Control-C, which terminates the program.'

Inconsistent behavior description for Control-C handling.

---

#### documentation_inconsistency

**Description:** INSTR example shows error message format that's inconsistent with modern error handling

**Affected files:**
- `docs/help/common/language/functions/instr.md`

**Details:**
Documentation shows: 'NOTE: If I=0 is specified, error message "ILLEGAL ARGUMENT IN <line number>" will be returned.'

This old-style error format may not match the Python implementation's error messages.

---

#### documentation_inconsistency

**Description:** INT documentation references FIX and CINT functions but doesn't link to them in See Also

**Affected files:**
- `docs/help/common/language/functions/int.md`

**Details:**
Documentation states: 'See the FIX and CINT functions which also return integer values.'

But the See Also section includes FIX and CINT, so this sentence is redundant.

---

#### documentation_inconsistency

**Description:** LEFT$ example output formatting is inconsistent

**Affected files:**
- `docs/help/common/language/functions/left_dollar.md`

**Details:**
Example shows:
'10 A$ = "BASIC-80"
 20 B$ = LEFT$(A$,5)
 30 PRINT B$
 BASIC
 Ok'

The spacing and 'Ok' prompt format is inconsistent with other examples.

---

#### documentation_inconsistency

**Description:** LEN example output shows 'Ok' on separate line inconsistently

**Affected files:**
- `docs/help/common/language/functions/len.md`

**Details:**
Example shows:
'10 X$ = "PORTLAND, OREGON"
 20 PRINT LEN (X$)
 16
 Ok'

Other examples format 'Ok' differently.

---

#### documentation_inconsistency

**Description:** MID$ example has inconsistent spacing in LIST output

**Affected files:**
- `docs/help/common/language/functions/mid_dollar.md`

**Details:**
Example shows:
'LIST
 10 A$="GOOD "
 20 B$="MORNING EVENING AFTERNOON"
 30 PRINT A$;MID$(B$,9,7)'

Spacing before line numbers is inconsistent with other examples.

---

#### documentation_inconsistency

**Description:** MID$ documentation has duplicate note about I=0 error that appears in INSTR as well

**Affected files:**
- `docs/help/common/language/functions/mid_dollar.md`

**Details:**
Both MID$ and INSTR docs state: 'NOTE: If I=0 is specified, error message "ILLEGAL ARGUMENT IN <line number>" will be returned.'

This suggests a pattern but the exact error message format should be verified.

---

#### documentation_inconsistency

**Description:** MKI$/MKS$/MKD$ documentation has malformed See Also section with unrelated content

**Affected files:**
- `docs/help/common/language/functions/mki_dollar-mks_dollar-mkd_dollar.md`

**Details:**
The See Also section includes: 'See also CVI, CVS, CVD, Section 3.9 and Appendix B.
3.27 OCT$
PRINT OCT$ (24)
30
Ok
See the HEX $ function for hexadecimal conversion.
3.2S PEEK
A=PEEK (&H5AOO)'

This appears to be corrupted text from multiple sections merged together.

---

#### documentation_inconsistency

**Description:** POS example shows output that may not match actual implementation

**Affected files:**
- `docs/help/common/language/functions/pos.md`

**Details:**
Example shows:
'10 PRINT "Hello";
20 PRINT "Position:"; POS(0)
30 IF POS(0) > 60 THEN PRINT CHR$(13)

Output:
HelloPosition: 6'

The output format suggests no space after the semicolon, but BASIC typically adds a space.

---

#### documentation_inconsistency

**Description:** RND documentation uses inconsistent capitalization for 'RUN'

**Affected files:**
- `docs/help/common/language/functions/rnd.md`

**Details:**
Documentation states: 'The same sequence of random numbers is generated each time the program is RUN'

RUN is capitalized as if it's a command, but in context it's describing the action.

---

#### documentation_inconsistency

**Description:** SGN example has incomplete comment

**Affected files:**
- `docs/help/common/language/functions/sgn.md`

**Details:**
Example shows: 'ON SGN(X)+2 GOTO 100,200,300 branches to 100 if X is negative, 200 if X is 0 and 300 if X is positive.'

This is formatted as code but reads like a comment. Should be split into code and explanation.

---

#### documentation_inconsistency

**Description:** SIN documentation has typo in COS formula

**Affected files:**
- `docs/help/common/language/functions/sin.md`

**Details:**
Documentation states: 'COS(X)=SIN(X+3.l4l59/2)'

The value '3.l4l59' appears to have a lowercase 'l' instead of '1', should be '3.14159'.

---

#### documentation_inconsistency

**Description:** STR$ example is incomplete and unclear

**Affected files:**
- `docs/help/common/language/functions/str_dollar.md`

**Details:**
Example shows:
'5 REM ARITHMETIC FOR KIDS
10 INPUT "TYPE A NUMBER";N
20 ON LEN(STR$(N)) GOSUB 30,100,200,300,400,500
Also see the VAL function.'

The example is cut off and doesn't show what the subroutines do. The 'Also see' text is merged with the example.

---

#### documentation_inconsistency

**Description:** USR documentation references 'Appendix x' which is unclear

**Affected files:**
- `docs/help/common/language/functions/usr.md`

**Details:**
Documentation states: 'See Appendix x.'

The 'x' should probably be a specific appendix letter or number.

---

#### documentation_inconsistency

**Description:** Typo in VAL function example - missing closing parenthesis

**Affected files:**
- `docs/help/common/language/functions/val.md`

**Details:**
In the Description section, the example text reads:
"For example, VAL (" -3) returns -3."

Should be:
"For example, VAL (" -3") returns -3."

The closing quote and parenthesis are missing.

---

#### documentation_inconsistency

**Description:** Incomplete example code in VAL function documentation

**Affected files:**
- `docs/help/common/language/functions/val.md`

**Details:**
The example section contains incomplete/malformed BASIC code:

```basic
10 READ NAME$,CITY$,STATE$,ZIP$
 20 IF VAL(ZIP$) <90000 OR VAL(ZIP$) >96699 THEN
 PRINT NAME$ TAB(25) "OUT OF STATE"
 30 IF VAL(ZIP$) >=90801 AND VAL(ZIP$) <=90815 THEN
 PRINT NAME$ TAB(25) "LONG BEACH"
 See the STR$ function for numeric to string
 conversion.
```

Issues:
1. Line 20 has no line continuation or THEN clause body
2. Line 30 has no line continuation or THEN clause body
3. The last sentence appears to be documentation text mixed into the code example
4. Missing line numbers for some statements

---

#### documentation_inconsistency

**Description:** Inconsistent spacing in DATA statement remarks

**Affected files:**
- `docs/help/common/language/statements/data.md`

**Details:**
The remarks section contains inconsistent formatting:
"DATA statements are nonexecutable and may be placed anywhere in the program. A DATA statement may contain as many constants as will fit on a line (separated by commas), and any number of DATA statements may be used in a program.

The READ statements access the DATA statements in order (by line number) and the data contained therein may be thought of as one continuous list of items, regardless of how many items are on a line or where the lines are placed in the program."

The phrase "continuous list" appears to have extra spaces in the original: "one continuous list"

---

#### documentation_inconsistency

**Description:** Inconsistent documentation of DEF FN multi-character name support

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`

**Details:**
The DEF FN documentation states this is an extension:
"**Original MBASIC 5.21**: Function names were limited to a single character after FN"
"**This implementation (extension)**: Function names can be multiple characters"

However, the documentation doesn't clearly indicate whether this is a documented extension or an undocumented behavior. The "Implementation Note" pattern used in other files (VARPTR, CALL, USR) is not used here, suggesting this might be intentional but the documentation style is inconsistent.

---

#### documentation_inconsistency

**Description:** Inconsistent spacing and formatting in DIM example

**Affected files:**
- `docs/help/common/language/statements/dim.md`

**Details:**
The example section has inconsistent indentation:
```basic
10 DIM A(20)
             20 FOR 1=0 TO 20
             30 READ A(I)
             40 NEXT I
                 •
```

Lines 20-40 have excessive leading spaces, and there's a bullet point (•) at the end which appears to be a formatting artifact.

---

#### documentation_inconsistency

**Description:** Incomplete EDIT command documentation

**Affected files:**
- `docs/help/common/language/statements/edit.md`

**Details:**
The EDIT documentation mentions edit mode commands but doesn't provide complete details:
"In traditional MBASIC, EDIT mode provided special single-character commands:
- **I** - Insert mode
- **D** - Delete characters
- **C** - Change characters
- **L** - List the line
- **Q** - Quit edit mode
- **Space** - Move cursor forward
- **Enter** - Accept changes"

Then states: "Modern MBASIC implementations often provide full-screen editing capabilities instead of the traditional line editor."

This doesn't clarify which behavior this implementation uses, creating ambiguity.

---

#### documentation_inconsistency

**Description:** Inconsistent spacing in CLOSE example section

**Affected files:**
- `docs/help/common/language/statements/close.md`

**Details:**
The example section contains:
```basic
See PART II, Chapter 3, MBASIC       Disk
              I/O, of the MBASIC User's Guide.
```

This has excessive spaces between "MBASIC" and "Disk" and unusual line breaking, suggesting a formatting issue from the original documentation.

---

#### documentation_inconsistency

**Description:** Inconsistent formatting in DELETE examples

**Affected files:**
- `docs/help/common/language/statements/delete.md`

**Details:**
The example section has inconsistent alignment:
```basic
DELETE 40         Deletes line 40
                DELETE 40-100     Deletes lines 40 through
                                  100, inclusive
                DELETE-40         Deletes all lines up to
                                  and including line 40
```

The first example has different indentation than the subsequent examples.

---

#### documentation_inconsistency

**Description:** Missing file extension information in CHAIN documentation

**Affected files:**
- `docs/help/common/language/statements/chain.md`

**Details:**
The CHAIN documentation states:
"- **filename** - Name of the program to chain to (with or without .BAS extension)"

But doesn't specify what happens if no extension is provided - does it default to .BAS? This should be clarified for consistency with other file operations.

---

#### documentation_inconsistency

**Description:** Inconsistent spacing in CONT remarks

**Affected files:**
- `docs/help/common/language/statements/cont.md`

**Details:**
The remarks contain:
"Execution resumes at the point where the break occurred.   If the break occurred after a prompt from an INPUT statement, execution continues with the reprinting of the prompt (7 or prompt string) •"

There are multiple spaces after the period, and the phrase "(7 or prompt string)" is unclear - the "7" appears to be a typo or OCR error. There's also a bullet point (•) at the end.

---

#### documentation_inconsistency

**Description:** Inconsistent formatting in cassette tape command documentation

**Affected files:**
- `docs/help/common/language/statements/cload.md`
- `docs/help/common/language/statements/csave.md`

**Details:**
Both CLOAD and CSAVE documentation have unusual spacing and formatting issues:

CSAVE: "Each program or array saved         on    tape    is identified by a filename."
(excessive spaces)

CLOAD: "CLOAD* loads a numeric array that has been saved on tape.    The data on tape is loaded..."
(multiple spaces after period)

These appear to be OCR or formatting artifacts from the original documentation.

---

#### documentation_inconsistency

**Description:** Missing operator in operators documentation title

**Affected files:**
- `docs/help/common/language/operators.md`

**Details:**
The operators.md file documents arithmetic, comparison, and logical operators, but the title in the index.md refers to it as "Operators and Expressions" while the actual file title is "Operators and Expressions". The content covers operators but doesn't have a dedicated section on expressions as a concept, which might be expected given the title.

---

#### documentation_inconsistency

**Description:** ERASE documentation references OPTION BASE but doesn't link to it in See Also

**Affected files:**
- `docs/help/common/language/statements/erase.md`
- `docs/help/common/language/statements/dim.md`

**Details:**
erase.md See Also section lists:
- [DIM](dim.md)
- [OPTION BASE](option-base.md)

However, the ERASE remarks don't mention OPTION BASE behavior. The See Also should either explain why OPTION BASE is relevant or remove it if not applicable.

---

#### documentation_inconsistency

**Description:** GET documentation mentions INPUT# and LINE INPUT# usage after GET but doesn't explain the interaction

**Affected files:**
- `docs/help/common/language/statements/field.md`
- `docs/help/common/language/statements/get.md`

**Details:**
get.md states:
'After a GET statement, INPUT# and LINE INPUT# may be used to read characters from the random file buffer.'

However, field.md warns:
'Do not use a FIELDed variable name in an INPUT or LET statement.'

The relationship between using INPUT# after GET and the FIELD warning about INPUT is unclear. Are these different INPUT operations or is there a conflict?

---

#### documentation_inconsistency

**Description:** FOR...NEXT documentation has contradictory statement about loop execution

**Affected files:**
- `docs/help/common/language/statements/for-next.md`

**Details:**
for-next.md states:
'2. If variable exceeds ending value (y), loop terminates'

But then also states:
'Loop always executes at least once if start equals end'

This is contradictory. If the loop checks if variable exceeds ending value before executing, and start equals end, the loop should execute once. But if start > end (with positive STEP), it should not execute at all. The 'always executes at least once' statement needs clarification about STEP direction.

---

#### documentation_inconsistency

**Description:** Missing cross-reference between GOSUB and ON...GOSUB

**Affected files:**
- `docs/help/common/language/statements/gosub-return.md`
- `docs/help/common/language/statements/on-gosub-on-goto.md`

**Details:**
gosub-return.md See Also includes:
'- [ON...GOSUB/ON...GOTO](on-gosub-on-goto.md)'

But the link text is 'on-gosub-on-goto.md' while the actual file referenced in other docs is sometimes 'on-gosub' or 'on-goto'. The file naming should be consistent.

---

#### documentation_inconsistency

**Description:** INPUT# documentation has formatting issues and unclear text

**Affected files:**
- `docs/help/common/language/statements/input_hash.md`

**Details:**
input_hash.md Remarks section contains:
'<variable list> contains the vari?lble names' (typo: vari?lble)
'The data items in the file should appear just as they would if data were being typed in response to an INPUT statement.    with numeric values' (lowercase 'with' after period)

Multiple formatting and typo issues suggest OCR errors from original documentation.

---

#### documentation_inconsistency

**Description:** LINE INPUT# example has unclear formatting

**Affected files:**
- `docs/help/common/language/statements/inputi.md`

**Details:**
inputi.md example shows:
'10 OPEN "O",l,"LIST"'

Using lowercase 'l' instead of '1' for file number, which could be confusing. Should use consistent numeric formatting.

---

#### documentation_inconsistency

**Description:** LET example has formatting issues

**Affected files:**
- `docs/help/common/language/statements/let.md`

**Details:**
let.md example shows:
'120 LET E=12A2'

This appears to be '12^2' but shows as '12A2', likely an OCR or formatting error. Should be '12^2' or clarified.

---

#### documentation_inconsistency

**Description:** LIST documentation has unclear format description

**Affected files:**
- `docs/help/common/language/statements/list.md`

**Details:**
list.md shows:
'Format 2:     LIST [<line number>[-[<line number>]]] Extended, Disk'

The 'Extended, Disk' text appears to be misplaced version information that should be on a separate line or formatted differently.

---

#### documentation_inconsistency

**Description:** Inconsistent capitalization of 'R' option in LOAD

**Affected files:**
- `docs/help/common/language/statements/load.md`
- `docs/help/common/language/statements/merge.md`

**Details:**
load.md uses:
'if the nRn option is used' and 'LOAD with the nRn option'

This unusual notation 'nRn' should be clarified - it appears to mean the letter R as an option, but the 'n' characters are confusing. Should be written as ',R' to match the syntax.

---

#### documentation_inconsistency

**Description:** Index page lists FILES statement but FILES.md doesn't exist in provided files

**Affected files:**
- `docs/help/common/language/statements/index.md`

**Details:**
index.md lists:
'- [FILES](files.md) - Displays the directory of files on disk'

But files.md is provided in the documentation set. However, the index categorizes it under 'File Management' but it could also be under 'System'. Categorization should be reviewed.

---

#### documentation_inconsistency

**Description:** Index page has inconsistent statement categorization

**Affected files:**
- `docs/help/common/language/statements/index.md`

**Details:**
index.md categorizes statements but some could fit multiple categories:
- LIMITS is under 'System' but could be 'Program Control' or 'Diagnostics'
- HELPSETTING is under 'System' but could be 'Documentation'
- FILES is under 'File Management' but could be 'System'

While not strictly wrong, the categorization scheme should be documented or made more consistent.

---

#### documentation_inconsistency

**Description:** MID$ assignment documentation has incorrect 'related' link

**Affected files:**
- `docs/help/common/language/statements/mid-assignment.md`

**Details:**
The 'related' field lists 'mid_dollar' but should link to the function version. The link format appears inconsistent with other documentation files which use full paths like '../functions/mid_dollar.md'.

---

#### documentation_inconsistency

**Description:** NAME statement example has inconsistent formatting

**Affected files:**
- `docs/help/common/language/statements/name.md`

**Details:**
The example section contains:
```basic
Ok
              NAME "ACCTS" AS "LEDGER"
              Ok
              In this example, the file that was
              formerly named ACCTS will now be named LEDGER.
```
The indentation and 'Ok' prompts are inconsistent with other documentation examples. Most other docs show clean examples without the 'Ok' prompts or have them consistently formatted.

---

#### documentation_inconsistency

**Description:** NULL statement example has inconsistent formatting

**Affected files:**
- `docs/help/common/language/statements/null.md`

**Details:**
The example section contains:
```basic
Ok
              NULL 2
              Ok
              100 INPUT X
              200 IF X<50 GOTO 800
              Two null characters will be printed after each
              line.
```
The indentation and mixing of 'Ok' prompts with code is inconsistent with other documentation examples.

---

#### documentation_inconsistency

**Description:** OPTION BASE documentation has incomplete syntax description

**Affected files:**
- `docs/help/common/language/statements/option-base.md`

**Details:**
The syntax section states:
```basic
OPTION BASE n
where n is 1 or 0
```
This formatting is inconsistent with other docs which typically put the 'where' clause in the Remarks section rather than the Syntax section.

---

#### documentation_inconsistency

**Description:** OUT statement syntax description formatting inconsistent

**Affected files:**
- `docs/help/common/language/statements/out.md`

**Details:**
The syntax section contains:
```basic
OUT I,J
where I and J are    integer   expressions     in   the
range 0 to 255.
```
The 'where' clause has irregular spacing and should be in Remarks section per documentation standards.

---

#### documentation_inconsistency

**Description:** POKE statement has inconsistent remarks formatting

**Affected files:**
- `docs/help/common/language/statements/poke.md`

**Details:**
The Remarks section has irregular spacing and line breaks:
'The integer expression I is the address of the memory   location to be POKEd.      The integer expression J is the data to be POKEd.'
Multiple spaces between words suggest OCR or formatting issues.

---

#### documentation_inconsistency

**Description:** PRINT# documentation incomplete See Also reference

**Affected files:**
- `docs/help/common/language/statements/printi-printi-using.md`

**Details:**
The See Also section references 'PRINT USING' as 'print.md' but PRINT USING is actually documented in 'lprint-lprint-using.md' based on the title. This creates a broken or misleading reference.

---

#### documentation_inconsistency

**Description:** PUT statement has duplicate text in Purpose section

**Affected files:**
- `docs/help/common/language/statements/put.md`

**Details:**
The Purpose section contains:
'To write a record from a random buffer to a random file. disk file.'
The phrase 'disk file' is duplicated, suggesting a copy-paste error.

---

#### documentation_inconsistency

**Description:** RANDOMIZE example has inconsistent formatting

**Affected files:**
- `docs/help/common/language/statements/randomize.md`

**Details:**
The example section has irregular indentation and spacing:
'10 RANDOMIZE
             20 FOR 1=1 TO 5'
The leading spaces are inconsistent with other documentation examples.

---

#### documentation_inconsistency

**Description:** READ documentation has incomplete See Also reference

**Affected files:**
- `docs/help/common/language/statements/read.md`

**Details:**
The See Also section references DATA with description 'To store the numeric and string constants that are accessed by the program~s READ statement(s)' - note the tilde (~) instead of apostrophe (') in 'program~s', suggesting encoding issue.

---

#### documentation_inconsistency

**Description:** REM example has inconsistent formatting

**Affected files:**
- `docs/help/common/language/statements/rem.md`

**Details:**
The example section contains:
'..
             120 REM CALCULATE AVERAGE VELOCITY'
The '..' at the start and irregular indentation are inconsistent with other documentation examples.

---

#### documentation_inconsistency

**Description:** RESUME documentation references non-existent file

**Affected files:**
- `docs/help/common/language/statements/resume.md`

**Details:**
The See Also section references 'ERR/ERL Variables' as 'err-erl-variables.md' but this file path format is inconsistent with the function documentation pattern which would be '../functions/err.md' and '../functions/erl.md' or similar.

---

#### documentation_inconsistency

**Description:** PRINT documentation has inconsistent aliases field

**Affected files:**
- `docs/help/common/language/statements/print.md`

**Details:**
The PRINT documentation includes 'aliases: ["?"]' in the frontmatter, but this field is not present in other statement documentation files. This inconsistency in metadata fields should be standardized.

---

#### documentation_inconsistency

**Description:** MID$ assignment examples show inconsistent output formatting

**Affected files:**
- `docs/help/common/language/statements/mid-assignment.md`

**Details:**
The examples show:
'RUN
GOODB WORLD
Ok'
The 'Ok' prompt placement is inconsistent - sometimes it appears after output, sometimes on same line. This should be standardized across all documentation.

---

#### documentation_inconsistency

**Description:** Inconsistent 'See Also' section formatting and completeness

**Affected files:**
- `docs/help/common/language/statements/showsettings.md`
- `docs/help/common/language/statements/stop.md`

**Details:**
showsettings.md has a 'See Also' section with markdown links like [SETSETTING](setsetting.md), while stop.md has similar links but different formatting. However, showsettings.md references [LIMITS](limits.md) which is not documented anywhere in the provided files.

---

#### documentation_inconsistency

**Description:** WIDTH documentation contradicts itself on LPRINT support

**Affected files:**
- `docs/help/common/language/statements/width.md`

**Details:**
The Implementation Note says: 'The "WIDTH LPRINT" syntax is not supported (parse error). Only the simple "WIDTH <number>" form is accepted.'

But the Syntax section shows:
```basic
WIDTH <integer expression>
```

And then states: 'Original MBASIC 5.21 also supported:
```basic
WIDTH LPRINT <integer expression>  ' NOT SUPPORTED in this implementation
```'

The Remarks section from original docs says: 'If the LPRINT option is omitted, the line width is set at the terminal. If LPRINT is included, the line width is set at the line printer.' This creates confusion about what is actually supported.

---

#### documentation_inconsistency

**Description:** Inconsistent file naming convention for WRITE# documentation

**Affected files:**
- `docs/help/common/language/statements/write.md`
- `docs/help/common/language/statements/writei.md`

**Details:**
The WRITE statement for screen output is in 'write.md' with title 'WRITE (Screen)', while the file I/O variant is in 'writei.md' with title 'WRITE# (File)'. The 'See Also' section in write.md references 'WRITE#' with link [WRITE#](writei.md), using 'writei.md' as filename. This naming convention (using 'i' for '#') is inconsistent with other file I/O statements like PRINT# which would presumably be in 'printi.md'.

---

#### documentation_inconsistency

**Description:** Keyboard shortcuts documented in multiple places with potential conflicts

**Affected files:**
- `docs/help/common/shortcuts.md`
- `docs/help/common/ui/curses/editing.md`

**Details:**
shortcuts.md documents editor shortcuts like '^R - Run program', '^P - Show help', '^Q - Quit IDE', etc.

curses/editing.md says 'See your UI's keyboard shortcuts documentation for the complete list' and then lists 'Common shortcuts: Ctrl+R - Run program, Ctrl+N - New program (clear), Ctrl+S - Save program, Ctrl+L - Load program, Ctrl+P - Help'.

The shortcuts.md file doesn't mention Ctrl+N, Ctrl+S, or Ctrl+L, creating inconsistency about which shortcuts are actually available.

---

#### documentation_inconsistency

**Description:** Inconsistent 'See Also' sections between related statements

**Affected files:**
- `docs/help/common/language/statements/system.md`
- `docs/help/common/language/statements/stop.md`

**Details:**
system.md has an extensive 'See Also' section with 8 items: CHAIN, CLEAR, COMMON, CONT, END, NEW, RUN, STOP.

stop.md has a 'See Also' section with 6 items: CONT, END, CHAIN, CLEAR, RUN, SYSTEM.

Both reference each other, but system.md includes COMMON and NEW which stop.md doesn't, while both should logically have similar related commands since they're both program control statements.

---

#### documentation_inconsistency

**Description:** TRON-TROFF documentation missing 'See Also' section

**Affected files:**
- `docs/help/common/language/statements/tron-troff.md`

**Details:**
Most statement documentation files include a 'See Also' section with related commands. tron-troff.md has a minimal 'See Also' with only 4 items (STOP, CONT, ON ERROR GOTO, REM), but is missing other debugging-related commands that would be relevant like EDIT, LIST, or other debugging features.

---

#### documentation_inconsistency

**Description:** SWAP example has inconsistent formatting

**Affected files:**
- `docs/help/common/language/statements/swap.md`

**Details:**
The example in swap.md shows:
```basic
LIST
              10 A$=" ONE " : B$=" ALL " : C$="FOR"
              20 PRINT A$ C$ B$
              30 SWAP A$, B$
              40 PRINT A$ C$ B$
              RUN
              Ok
               ONE FOR ALL
               ALL FOR ONE
              Ok
```

The excessive indentation and spacing is inconsistent with other examples in the documentation which use clean, left-aligned formatting.

---

#### documentation_inconsistency

**Description:** Different counts of optimizations in semantic analyzer

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/features.md`

**Details:**
architecture.md states: "The semantic analyzer implements **18 distinct optimizations**" and lists all 18.

features.md states: "The interpreter includes an advanced semantic analyzer with 18 optimizations" and also lists all 18.

While both documents agree on the count, the wording differs slightly ("implements" vs "includes"). This is minor but could be standardized for consistency.

---

#### documentation_inconsistency

**Description:** Installation instructions reference non-existent repository

**Affected files:**
- `docs/help/mbasic/getting-started.md`

**Details:**
getting-started.md states: "git clone https://github.com/avwohl/mbasic.git"

This appears to be a placeholder URL. The actual repository URL should be verified and updated, or this should be noted as an example that needs to be replaced with the actual URL.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for line ending support

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/compatibility.md`

**Details:**
architecture.md states: "All line ending formats (CR, LF, CRLF)"

compatibility.md states: "Line ending support: More permissive than MBASIC 5.21" and explains: "This implementation: Recognizes CRLF, LF (`\n`), and CR (`\r`)"

While both convey the same information, the order of listing differs (CR, LF, CRLF vs CRLF, LF, CR). For consistency, the same order should be used throughout documentation.

---

#### documentation_inconsistency

**Description:** Find/Replace availability inconsistency across UIs

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/cli/find-replace.md`

**Details:**
feature-reference.md for Curses UI states 'Find/Replace (Not yet implemented)' and says 'See [Find/Replace](find-replace.md) (available via menu)'. However, cli/find-replace.md explicitly states 'The CLI backend does not have built-in Find/Replace commands' and recommends using Tk UI for this feature. The reference to find-replace.md from Curses docs suggests it might be available via menu, but the CLI docs say it's not available at all.

---

#### documentation_inconsistency

**Description:** String garbage collection documentation depth mismatch

**Affected files:**
- `docs/help/mbasic/implementation/string-allocation-and-garbage-collection.md`
- `docs/help/mbasic/index.md`

**Details:**
The string-allocation-and-garbage-collection.md provides extremely detailed technical documentation about CP/M MBASIC's O(n²) garbage collection algorithm, including assembly code references, performance tables, and implementation details. However, mbasic/index.md only briefly mentions this document as 'String Allocation and Garbage Collection - How CP/M MBASIC managed string memory' without indicating the depth of technical detail. Users looking for implementation guidance might not realize this is a comprehensive technical reference.

---

#### documentation_inconsistency

**Description:** Settings commands not listed in CLI index

**Affected files:**
- `docs/help/ui/cli/settings.md`
- `docs/help/ui/cli/index.md`

**Details:**
cli/settings.md documents SHOWSETTINGS and SETSETTING commands in detail, but cli/index.md does not list these commands under 'Common Commands' or anywhere else in the main CLI help. Users might not discover these commands exist.

---

#### documentation_inconsistency

**Description:** List Program feature access method unclear

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
feature-reference.md lists 'List Program (Menu only)' under Execution & Control and states 'Display the program listing in the editor. Access through the menu bar.' However, no documentation of the menu bar navigation or structure is provided in the Curses UI docs, making it unclear how to actually access this feature.

---

#### documentation_inconsistency

**Description:** Target audience unclear for technical implementation doc

**Affected files:**
- `docs/help/mbasic/implementation/string-allocation-and-garbage-collection.md`

**Details:**
string-allocation-and-garbage-collection.md provides deep technical details about CP/M MBASIC's internal implementation including assembly code, O(n²) complexity analysis, and 8080-specific register usage. The 'Implementation for Modern Emulation' section suggests this is for implementers, but the document is in the user help directory (docs/help/mbasic/) rather than developer docs (docs/dev/). Users looking for help might be confused by assembly code and implementation details.

---

#### documentation_inconsistency

**Description:** Missing List Program keyboard shortcut

**Affected files:**
- `docs/help/ui/curses/running.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
running.md states: 'Access through the menu bar to list the program to the output window.'

quick-reference.md shows: '**Menu only** | List program'

This is consistent, but other documents suggest there might be a keyboard shortcut that's not documented.

---

#### documentation_inconsistency

**Description:** Inconsistent default UI documentation

**Affected files:**
- `docs/help/ui/tk/getting-started.md`
- `docs/help/ui/tk/index.md`

**Details:**
getting-started.md states: 'Or to use the default curses UI: ```bash mbasic [filename.bas] ```'

index.md states: 'mbasic                # Default UI mbasic --ui curses'

Both suggest curses is the default, which is consistent, but the phrasing in getting-started.md ('Or to use the default') is confusing since it's in the Tk getting-started guide.

---

#### documentation_inconsistency

**Description:** Variable editing capability inconsistency between UIs

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/tk/features.md`

**Details:**
curses/variables.md states: '### Current Status
⚠️ **Partial Implementation**: Variable editing in Curses UI is limited.

### What Doesn't Work Yet
- Cannot edit values directly in window'

tk/features.md states: '### Edit Variable Value
Double-click a variable in the Variables window to edit its value during debugging.'

This is actually consistent (different UIs have different capabilities), but could be clearer in the comparison tables.

---

#### documentation_inconsistency

**Description:** Incomplete feature comparison table

**Affected files:**
- `docs/help/ui/index.md`

**Details:**
The comparison table in index.md shows: '| Variables Window | ✓ | ✗ | ✓ | ✗ |'

But curses/variables.md extensively documents a Variables Window for Curses UI with Ctrl+W shortcut. The table incorrectly shows Curses as having it (✓) but Web as not having it (✗), yet the actual implementation status is unclear.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut references for Smart Insert

**Affected files:**
- `docs/help/ui/tk/tips.md`
- `docs/help/ui/tk/workflows.md`

**Details:**
tips.md states: 'Use **Ctrl+I** (Smart Insert) to add details under each section without calculating line numbers!'

workflows.md states: 'Press **Ctrl+I** (Smart Insert) to insert blank line'

Both reference Ctrl+I for Smart Insert, which is consistent, but the descriptions differ slightly (one says 'add details', the other says 'insert blank line'). This is minor but could be more consistent.

---

#### documentation_inconsistency

**Description:** Minor inconsistency in renumber keyboard shortcut description

**Affected files:**
- `docs/help/ui/tk/workflows.md`
- `docs/help/ui/tk/tips.md`

**Details:**
workflows.md states: 'Press **Ctrl+E** (Renumber)'

tips.md states: 'Renumber Before Sharing... but renumber (**Ctrl+E**) before sharing code'

Both correctly reference Ctrl+E, but workflows.md capitalizes 'Renumber' while tips.md uses lowercase 'renumber'. This is a minor style inconsistency.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for loading files in web UI

**Affected files:**
- `docs/help/ui/web/web-interface.md`
- `docs/library/*/index.md`

**Details:**
web-interface.md uses:
'Load a .bas file from your computer (via browser file picker)'

library docs use:
'Click File → Open, select the downloaded file using browser file picker'

Both describe same action but use different menu names: 'Open' vs 'Load'

---

#### documentation_inconsistency

**Description:** Library statistics count mismatch

**Affected files:**
- `docs/library/index.md`
- `docs/library/*/index.md`

**Details:**
docs/library/index.md states:
'Total Programs: 114+'

But counting all programs listed in category index files:
- Games: 141 programs
- Utilities: 18 programs
- Education: 3 programs
- Business: 8 programs
- Electronics: 13 programs
- Ham Radio: 7 programs
- Data Management: 5 programs
- Telecommunications: 5 programs
- Demos: 5 programs
Total: 205 programs

The '114+' count is significantly lower than actual count.

---

#### documentation_inconsistency

**Description:** Category count mismatch in library statistics

**Affected files:**
- `docs/library/index.md`

**Details:**
Library index states:
'Categories: 9'

But lists 9 categories in the page. This is actually consistent, but the phrasing 'Categories: 9' appears after listing all 9, making it redundant rather than a summary.

---

#### documentation_inconsistency

**Description:** Settings dialog mentioned but not documented in menu sections

**Affected files:**
- `docs/help/ui/web/web-interface.md`

**Details:**
web-interface.md Auto-Numbering section mentions:
'Use the Settings dialog (⚙️ icon) to change the increment or disable auto-numbering entirely'

But the Menu Functions section does not list a Settings menu or ⚙️ icon option. Users won't know where to find this feature.

---

#### documentation_inconsistency

**Description:** Malformed program entry in utilities index

**Affected files:**
- `docs/library/utilities/index.md`

**Details:**
One entry shows:
'### Remarks:  This program will con

**Year:** 1980s
**Tags:** 

**[Download hex2data.bas](hex2data.bas)**'

The title 'Remarks: This program will con' appears to be truncated program comments rather than a proper title. Should likely be '### Hex2data' or similar.

---

#### documentation_inconsistency

**Description:** Inconsistent program entry formatting

**Affected files:**
- `docs/library/utilities/index.md`

**Details:**
Most entries have format:
'### ProgramName

**Year:** 1980s
**Tags:**'

But some have additional fields:
'### Survival

**Author:** R Logan & Ian Lycholm CBASIC 2 VER
**Year:** 1982'

'### Un-Prot

Fixup for ** UN.COM **

**Year:** 1980s'

'### Xextract

0 -->END PAGE / 1-20 -->EXTRACT ITEM / 21 -->RESTART'

Inconsistent metadata structure across entries.

---

#### documentation_inconsistency

**Description:** Duplicate calendar program in games and utilities

**Affected files:**
- `docs/library/games/index.md`

**Details:**
Calendar.bas appears in both:
- docs/library/games/index.md
- docs/library/utilities/index.md

Same filename, both from 1980s. Unclear if this is intentional (same program in multiple categories) or an error.

---

#### documentation_inconsistency

**Description:** Inconsistent dependency information for UI options

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`
- `docs/user/INSTALL.md`

**Details:**
CHOOSING_YOUR_UI.md states:
- Curses 'Requires urwid'
- Web 'Requires nicegui'

INSTALL.md Step 4 states: 'pip install -r requirements.txt' and 'Note: Since this project has no external dependencies, this step mainly verifies your Python environment is working correctly.'

This is contradictory - if urwid and nicegui are required for certain UIs, then the project does have external dependencies.

---

#### documentation_inconsistency

**Description:** Inconsistent feature availability claims for Find/Replace

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
In the 'UI Comparison at a Glance' table:
- Curses: 'Avoid If: You need Find/Replace yet'

In 'Detailed UI Profiles' for Curses:
- Limitations: 'No Find/Replace yet'

In 'Decision Matrix' table:
- Curses Find/Replace: ❌
- Tk Find/Replace: ✅
- Web Find/Replace: ❌

The word 'yet' in the Curses section implies it's planned, but this is inconsistent with the definitive ❌ in the decision matrix. The Web UI also shows ❌ but without 'yet', suggesting it's not planned there.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for line ending types

**Affected files:**
- `docs/user/FILE_FORMAT_COMPATIBILITY.md`

**Details:**
The document uses multiple terms for the same line ending types:
- 'Unix-style line endings' and 'Unix/Linux' and 'LF'
- 'Windows' and 'DOS/Windows-style' and 'CRLF'
- 'Old Mac' and 'CR'

While technically correct, mixing terminology (especially 'DOS/Windows-style' appearing only once in the CP/M section) could confuse readers. Standardizing on one primary term with alternatives in parentheses would improve clarity.

---

#### documentation_inconsistency

**Description:** README lists files that may not exist or are placeholders

**Affected files:**
- `docs/user/README.md`

**Details:**
The README.md lists several files:
- TK_UI_QUICK_START.md
- keyboard-shortcuts.md
- UI_FEATURE_COMPARISON.md
- CASE_HANDLING_GUIDE.md
- sequential-files.md

These files are not provided in the documentation set, so it's unclear if they exist. If they don't exist, the README should note them as planned/TODO. If they do exist, they should be included in documentation reviews.

---

#### documentation_inconsistency

**Description:** Mouse support inconsistency for Curses UI

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
In 'UI Comparison at a Glance' table:
- Curses 'Avoid If: You need mouse support'

In 'Detailed UI Profiles' for Curses:
- Limitations: 'Limited mouse support'

In 'Decision Matrix' table:
- Curses Mouse support: ⚠️ (warning symbol)

'No mouse support' vs 'Limited mouse support' are different claims. The ⚠️ symbol suggests partial support, which aligns with 'Limited' but contradicts the 'Avoid If' section that implies no support.

---

#### documentation_inconsistency

**Description:** Inconsistent Python command usage

**Affected files:**
- `docs/user/INSTALL.md`

**Details:**
INSTALL.md uses both 'python3' and 'python' commands throughout:
- Prerequisites section: 'python3 --version'
- Method 1 (Linux/Mac): 'python3 -m venv venv'
- Method 1 (Windows): 'python -m venv venv'
- Method 2: 'python3 mbasic'
- Troubleshooting: 'Try using python instead of python3'

While the troubleshooting section acknowledges this, the inconsistent usage in examples could confuse users. A consistent approach with a note about platform differences would be clearer.

---

#### documentation_inconsistency

**Description:** Inconsistent boolean value format in examples

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
Under 'SET Command' examples:
'SET "editor.show_line_numbers" true'

Under 'Type Conversion':
'Booleans: true or false (lowercase, no quotes)'

However, in JSON configuration file examples:
'"editor.auto_number": true' (in JSON, which is correct)

The documentation should clarify that:
1. In SET commands: true/false without quotes
2. In JSON files: true/false (JSON boolean syntax)

The current mixing of contexts could confuse users about when to use quotes.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation of Variables window shortcut

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md documents two different shortcuts for Variables window:
| **Ctrl+V** | Show/hide Variables window |
| **Ctrl+W** | Show/hide Variables & Resources window |

keyboard-shortcuts.md (Curses) documents:
| `Ctrl+W` | Toggle variables watch window |

UI_FEATURE_COMPARISON.md shows:
| **Variables** | WATCH | Ctrl+W | Ctrl+V | Ctrl+Alt+V |

It's unclear if Ctrl+V and Ctrl+W do the same thing in Tk UI, or if they show different windows. The 'Variables & Resources window' terminology in TK_UI_QUICK_START.md is not explained elsewhere.

---

#### documentation_inconsistency

**Description:** Save shortcut inconsistency between UIs

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md documents:
| **Ctrl+S** | Save file |

keyboard-shortcuts.md (Curses) documents:
| `Ctrl+V` | Save program |
| `Shift+Ctrl+V` | Save As |

This is confusing because Ctrl+V is documented as 'Show/hide Variables window' in Tk UI, but as 'Save program' in Curses UI. The UI_FEATURE_COMPARISON.md confirms both UIs have Ctrl+S for Save, suggesting the Curses documentation may be incorrect.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for execution control shortcuts

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
TK_UI_QUICK_START.md uses different terms for the same shortcuts:

In 'Essential Keyboard Shortcuts' table:
| **Ctrl+T** | Step through code (next statement) |
| **Ctrl+L** | Step through code (next line) |
| **Ctrl+G** | Continue execution (go) |

In 'Improved Debugging Features' section:
'Use **Ctrl+T** (step statement)'
'Use **Ctrl+L** (step line)'

In 'Debugging Shortcuts' comparison:
| **Step** | STEP | F10 | F10 | F10 |
| **Continue** | CONT | F5 | F5 | F5 |

The table shows F10 for Step and F5 for Continue, but the Tk column in Essential Shortcuts shows Ctrl+T/L/G. It's unclear if both sets of shortcuts work or if there's an error.

---

#### documentation_inconsistency

**Description:** Ambiguous date format in 'Improved Debugging Features' section

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
TK_UI_QUICK_START.md header states:
'## Improved Debugging Features (October 2025)'

And earlier:
'## Variable Case Preservation (New in October 2025)'

October 2025 is in the future (from typical documentation perspective). This might be a typo for 2024, or the documentation is dated for a future release. The UI_FEATURE_COMPARISON.md shows 'Recently Added (2025-10-29)' which uses a different date format and confirms 2025.

---

#### documentation_inconsistency

**Description:** Incomplete cross-reference in sequential-files.md

**Affected files:**
- `docs/user/sequential-files.md`

**Details:**
sequential-files.md 'See Also' section references:
'[Compatibility Guide](../help/mbasic/compatibility.md)'

However, this file is not provided in the documentation set, so we cannot verify if the link is correct or if the referenced information exists.

---


## Summary

- Total issues found: 704
- Code/Comment conflicts: 237
- Other inconsistencies: 467
