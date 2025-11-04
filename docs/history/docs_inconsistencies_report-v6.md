# Enhanced Consistency Report (Code + Documentation)

Generated: 2025-11-04 01:06:52
Analyzed: Source code (.py, .json) and Documentation (.md)

## 🔧 Code vs Comment Conflicts


## 📋 General Inconsistencies

### 🔴 High Severity

#### code_implementation

**Description:** Missing method implementation: CaseKeeperTable.register() is called but not defined

**Affected files:**
- `src/case_string_handler.py`
- `src/case_keeper.py`

**Details:**
case_string_handler.py line 62 calls 'table.register(text, original_text, line, column)' but CaseKeeperTable only implements 'set()', 'get()', 'contains()', 'clear()' methods. The register() method does not exist.

---

#### code_vs_documentation

**Description:** Duplicate and conflicting file I/O abstractions exist in the codebase

**Affected files:**
- `src/editing/manager.py`
- `src/file_io.py`
- `src/filesystem/base.py`

**Details:**
Two separate file I/O abstraction systems exist:
1. src/file_io.py defines FileIO abstract class with RealFileIO and SandboxedFileIO implementations
2. src/filesystem/ package defines FileSystemProvider abstract class with RealFileSystemProvider and SandboxedFileSystemProvider implementations

Both provide the same functionality (list_files, load_file/open, save_file, delete_file, file_exists) but with different APIs. The manager.py uses direct file operations (open, with statements) rather than either abstraction. This creates confusion about which system should be used.

---

#### code_vs_comment

**Description:** Comment claims 'Don't restore PC' but there's no code that would restore PC in the first place

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Line ~200 has comment '# Don't restore PC - let statements like RUN change execution position' but there is no PC save/restore code visible. The comment suggests code was removed but comment remained, or the comment is explaining why something ISN'T done when it's not obvious that it would be done.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of line_text_map between Runtime initialization calls

**Affected files:**
- `src/interactive.py`

**Details:**
Line 186: 'runtime = Runtime(self.line_asts, self.lines)' passes line_text_map. Line 398: 'runtime = Runtime(self.line_asts)' does NOT pass line_text_map. Line 1009: 'self.runtime = Runtime(ast)' does NOT pass line_text_map. This inconsistency means error messages may not show source lines in some execution paths (cmd_chain, execute_immediate).

---

#### code_vs_comment

**Description:** Docstring for cmd_delete says it uses ui_helpers, but implementation shows direct delegation without error handling details

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 545-553: Docstring says 'DELETE - Delete line or range of lines using ui_helpers'. Implementation (lines 558-564) calls delete_lines_from_program() and catches ValueError and generic Exception, but doesn't document what delete_lines_from_program() returns or how it modifies state. The comment 'Success - deleted will contain list of deleted line numbers' (line 561) suggests a return value that isn't used.

---

#### code_internal_inconsistency

**Description:** Inconsistent PC handling in execute_immediate could break stopped programs

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 1107-1115: Code saves old_pc, executes statements, then restores old_pc. Comment on line 1108 says 'Save old PC (important for stopped programs)'. However, if any statement modifies PC (like GOTO in immediate mode), the restoration would override that change. This could break legitimate PC modifications while trying to preserve stopped program state.

---

#### code_vs_comment

**Description:** Comment claims error_info is set by caller, but code shows it's set in multiple places

**Affected files:**
- `src/interpreter.py`

**Details:**
In _invoke_error_handler() at line ~1050, comment says '# Note: error_info is already set by caller (in tick_pc exception handler)' but the code in tick_pc() shows error_info is set in multiple exception handlers (line ~730, ~750, ~1000), and _invoke_error_handler() itself doesn't set it. The comment suggests a single point of setting, but implementation has multiple.

---

#### code_vs_comment

**Description:** Comment about error handler clearing conflicts with actual clearing location

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_goto() at line ~1150, comment says '# If we're in an error handler and GOTOing out, clear the error state' and code clears error_info. Same pattern in execute_ongoto() at line ~1190 and execute_return() at line ~1330. However, _invoke_error_handler() comment at line ~1050 says error_info is 'already set by caller' and 'We're now in the error handler', suggesting error_info should remain set during handler execution. The clearing logic in GOTO/RETURN suggests error_info is used to track 'currently in error handler' state, but this isn't documented in ErrorInfo or InterpreterState docstrings.

---

#### code_vs_comment

**Description:** execute_input comment describes state machine behavior but doesn't explain what happens when input_buffer is empty vs when input_prompt is set

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: 'In tick-based execution mode, this may transition to 'waiting_for_input' state instead of blocking.'
Code sets 'self.state.input_prompt' but comment mentions 'waiting_for_input' state. The relationship between input_prompt being set and the actual state is unclear. Does setting input_prompt automatically transition to waiting_for_input state, or is that handled elsewhere?

---

#### code_vs_comment

**Description:** execute_run comment says 'CLEAR variables' but code calls runtime.clear_variables() which may do more than just variables

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: 'Execute RUN statement - CLEAR variables and restart/goto'
Code: 'self.runtime.clear_variables()'
The comment says only variables are cleared, but clear_variables() might also clear other state. Need to verify if this matches the documented behavior or if the comment should say 'CLEAR all state'.

---

#### code_vs_comment

**Description:** execute_midassignment comment says 'If start is beyond the string length, no replacement occurs' but doesn't handle negative start values

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: 'If start is beyond the string length, no replacement occurs'
Code: 'if start_idx < 0 or start_idx >= len(current_value): return'
The code handles negative start values (after converting to 0-based), but the comment doesn't mention this case. Should document what happens with start < 1.

---

#### code_vs_comment

**Description:** execute_stop docstring describes detailed state preservation but doesn't show implementation of FOR loop stack or GOSUB return stack preservation

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring lists: '- GOSUB return stack\n- FOR loop stack\n- Current execution position'. However, the execute_stop implementation only sets runtime.stopped=True and runtime.stop_pc. There's no explicit code showing that GOSUB and FOR stacks are preserved (they may be preserved implicitly by not clearing them, but this isn't clear from the code shown).

---

#### code_vs_documentation

**Description:** Method name inconsistency: base.py defines 'output()' but web_io.py implements 'print()'

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/console.py`
- `src/iohandler/curses_io.py`
- `src/iohandler/web_io.py`

**Details:**
base.py IOHandler abstract class defines 'output(self, text: str, end: str = '\n')' as the required method. However, web_io.py WebIOHandler implements 'print(self, text="", end="\n")' instead of 'output()'. This violates the interface contract. ConsoleIOHandler and CursesIOHandler correctly implement 'output()'.

---

#### code_vs_documentation

**Description:** Method name inconsistency: base.py defines 'input_char()' but web_io.py implements 'get_char()'

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/web_io.py`

**Details:**
base.py IOHandler defines 'input_char(self, blocking: bool = True) -> str' as the required method. web_io.py WebIOHandler implements 'get_char(self)' with no blocking parameter. This violates the interface contract.

---

#### code_vs_documentation

**Description:** Missing required methods in WebIOHandler

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/web_io.py`

**Details:**
base.py IOHandler defines required abstract methods: error(), debug(), locate(), get_cursor_position(). web_io.py WebIOHandler implements set_cursor_position() and get_screen_size() instead, and is missing error() and debug() methods entirely.

---

#### code_internal_inconsistency

**Description:** Duplicate parse_stop() method definition with different implementations

**Affected files:**
- `src/parser.py`

**Details:**
The parse_stop() method is defined twice in the parser. First definition at line ~1050 returns StopStatementNode with just line_num and column. Second definition at line ~1450 has identical implementation but includes a docstring about STOP preserving state. Both create the same node type with same parameters.

---

#### code_vs_comment

**Description:** renumber_with_spacing_preservation docstring contradicts its behavior regarding text regeneration

**Affected files:**
- `src/position_serializer.py`

**Details:**
Lines 502-507 say 'AST is the single source of truth. This function: 1. Updates line numbers in the AST 2. Updates all line number references 3. Adjusts token column positions 4. Text is regenerated from AST by position_serializer' - but the function only returns updated LineNodes, it doesn't actually regenerate text. The caller must call serialize_line separately.

---

#### code_vs_comment

**Description:** Docstring for get_variable() says token is REQUIRED but implementation allows None in some cases

**Affected files:**
- `src/runtime.py`

**Details:**
Line 289 docstring: 'This method MUST be called with a token for normal program execution.' and 'Raises: ValueError: If token is None'. However, line 296 only raises ValueError if token is None, but then lines 313-314 have fallback logic: 'line': getattr(token, 'line', self.pc.line_num if self.pc and not self.pc.halted() else None)', suggesting the code is designed to handle token being None in some scenarios.

---

#### code_vs_comment

**Description:** get_array_element() docstring contradicts implementation regarding auto-dimensioning

**Affected files:**
- `src/runtime.py`

**Details:**
Line 527 docstring says 'Get array element value, optionally tracking read access' with no mention of auto-dimensioning. However, lines 543-549 implement auto-dimensioning: 'Auto-dimension array to (10) if not explicitly dimensioned (MBASIC behavior)'. This is a significant behavior not documented in the method's docstring.

---

#### code_vs_comment

**Description:** set_array_element() docstring also missing auto-dimensioning documentation

**Affected files:**
- `src/runtime.py`

**Details:**
Line 591 docstring says 'Set array element value, optionally tracking write access' with no mention of auto-dimensioning. However, lines 607-613 implement the same auto-dimensioning behavior as get_array_element(). This critical behavior should be documented.

---

#### code_vs_comment

**Description:** get_gosub_stack() docstring example shows statement offsets (100.0, 500.2, 1000.1) but the actual return format uses tuples not decimal notation

**Affected files:**
- `src/runtime.py`

**Details:**
Docstring says: "Example: [(100, 0), (500, 2), (1000, 1)]  # Called GOSUB at 100.0, 500.2, 1000.1" - The comment uses decimal notation (100.0, 500.2) to describe line.statement format, but the actual return value is a list of tuples [(100, 0), (500, 2), (1000, 1)]. This could confuse users about the actual data structure returned.

---

#### code_vs_documentation

**Description:** CLI debug commands use different terminology than curses UI keybindings for stepping functionality

**Affected files:**
- `src/ui/cli_debug.py`
- `src/ui/curses_keybindings.json`

**Details:**
cli_debug.py implements 'STEP' command with docstring 'STEP command - execute one line/statement' and 'STEP n - Execute n lines'. However, curses_keybindings.json distinguishes between 'step_line' (Ctrl+K: 'Step Line (execute all statements on current line)') and 'step' (Ctrl+T: 'Step statement (execute one statement)'). The CLI STEP command appears to execute lines, not statements, but the docstring says 'line/statement' ambiguously.

---

#### code_vs_comment

**Description:** Breakpoint handler implementation conflicts with its described behavior

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
In _install_breakpoint_handler, the breakpoint_execute function checks for breakpoints and then 'return # Pause execution' to pause. However, this return statement only exits the breakpoint_execute wrapper, not the actual interpreter loop. The comment suggests execution pauses, but the code doesn't show how the interpreter loop is actually stopped. The original_execute() is only called if no breakpoint is hit, but there's no mechanism shown to resume execution after a breakpoint.

---

#### code_vs_comment

**Description:** Comment describes format 'SNN CODE' but code implements variable-width line numbers

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line 1082 comment says 'Format new line: " NN " (with status space)' suggesting 2-digit line numbers, but the code uses variable-width line numbers. The format string is 'f"\n {next_num} "' which doesn't enforce any width.

---

#### internal_inconsistency

**Description:** Inconsistent line number formatting: some code uses fixed 5-char width, other code uses variable width

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line 1449 and 1476 format line numbers as 5-char right-aligned ('{num_str:>5}'), but _format_line at line 1009 uses variable width ('{line_num}'), and _parse_line_number expects variable width by finding the space delimiter. This creates internal format inconsistency.

---

#### code_vs_comment

**Description:** Comment says 'No state checking - just ask the interpreter' but code doesn't actually check interpreter state safely

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line '# No state checking - just ask the interpreter' followed by 'has_work = self.interpreter.has_work() if self.interpreter else False'. However, the subsequent code block checks 'if self.interpreter and has_work:' and then accesses self.interpreter.state without verifying it exists. Later code does check 'if not hasattr(self.interpreter, 'state') or self.interpreter.state is None:' but only after already assuming interpreter exists. The comment suggests no state checking is needed, but the code shows it is needed.

---

#### Code vs Documentation inconsistency

**Description:** Help widget uses hardcoded 'curses' UI name but keybindings.py defines HELP_KEY as 'ctrl f' (Ctrl+F), while help_widget.py comment says 'ESC/Q to exit' and footer shows '/=Search' but keybindings.py shows HELP_KEY as Ctrl+F for help

**Affected files:**
- `src/ui/help_widget.py`
- `src/ui/keybindings.py`

**Details:**
help_widget.py line 13: 'ESC/Q to exit' and line 68: footer shows '/=Search' but keybindings.py line 48-50 defines HELP_KEY = 'ctrl f', HELP_CHAR = '\x06', HELP_DISPLAY = '^F'. The help widget doesn't use the keybindings module for its own key handling.

---

#### Code vs Documentation inconsistency

**Description:** VARIABLES_KEY defined as 'ctrl w' but VARIABLES_DISPLAY shows 'Ctrl+W', inconsistent with other keys loaded from JSON that use the JSON format

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py line 96-98: VARIABLES_KEY = 'ctrl w', VARIABLES_CHAR = '\x17', VARIABLES_DISPLAY = 'Ctrl+W' - hardcoded instead of loaded from JSON like other keys. Comment says '(not in JSON, hardcoded)' but this creates inconsistency with the keybinding system

---

#### Code vs Documentation inconsistency

**Description:** MAXIMIZE_OUTPUT_KEY defined as 'ctrl o' conflicts with OPEN_KEY which is also loaded as 'Ctrl+O' from JSON

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py line 131: _open_key = _get_key('editor', 'open') or 'Ctrl+O' and line 217-219: MAXIMIZE_OUTPUT_KEY = 'ctrl o', MAXIMIZE_OUTPUT_CHAR = '\x0f', MAXIMIZE_OUTPUT_DISPLAY = '^O' - both use Ctrl+O, creating a key conflict

---

#### code_vs_comment

**Description:** Incomplete code in _edit_simple_variable method

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
The _edit_simple_variable method ends abruptly with 'self.runtime.set_variable(base_name,' without completing the function call or the method. The code is cut off mid-statement, making it impossible to determine the intended behavior. This appears to be a truncation issue in the provided source code.

---

#### code_vs_comment

**Description:** Comment says 'clears red ? when line is fixed' but there's no indication in the code that a red '?' is used for error marking

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~1050: Comment says '# Also validate syntax after clicking (clears red ? when line is fixed)' but the error marking system uses 'self.editor_text.set_error()' and 'self.editor_text.clear_all_errors()' with no mention of a '?' character. The actual error marking mechanism is not visible in this code snippet.

---

#### code_vs_comment

**Description:** Comment says 'insert BEFORE current line' but code inserts AT current line's position

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _smart_insert_line method, comment says 'Insert blank line BEFORE current line (at current line's position)' and 'The new line will be inserted at the current line's text position, pushing the current line down' but the insert_index is set to current_line_index, which means it inserts at that position. The comment is confusing about whether it's 'before' or 'at' the current line.

---

#### code_vs_comment

**Description:** Docstring for cmd_cont says 'Invalid if program was edited after stopping' but no validation code exists

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
The cmd_cont docstring states 'Invalid if program was edited after stopping' but the implementation doesn't check if the program was edited. It only checks if runtime.stopped is true.

---

#### code_implementation

**Description:** Status click handler suggests breakpoint toggling functionality that doesn't exist

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
In _on_status_click, the info message states: 'Click the ● again to toggle it off.' However, the _on_status_click method only displays messages and does not implement any breakpoint toggling logic. There is no code that calls set_breakpoint() in response to clicks. This is a functional inconsistency where the UI tells users they can do something that isn't actually implemented.

---

#### code_vs_comment

**Description:** renum_program() docstring says renum_callback should handle statement updates, but code also calls serialize_line() which may duplicate work

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring: 'renum_callback: Function that takes (stmt, line_map) to update statement references. Should handle GOTO, GOSUB, ON GOTO, ON GOSUB, IF THEN/ELSE line numbers'. Code then does: 'new_lines[new_num] = serialize_line(line_node)'. The serialize_line() function will serialize the statements that were already updated by renum_callback. However, serialize_statement() for GotoStatementNode just uses 'stmt.line_number' directly - it doesn't know about the mapping. This suggests either: (1) renum_callback must mutate the AST nodes in place, or (2) serialize_statement needs the mapping too. The docstring doesn't clarify this critical detail.

---

#### code_vs_documentation

**Description:** Statement-level breakpoint and highlighting support inconsistency between VisualBackend documentation and CodeMirror implementations

**Affected files:**
- `src/ui/visual.py`
- `src/ui/web/codemirror5_editor.py`
- `src/ui/web/codemirror_editor.py`

**Details:**
VisualBackend.cmd_run() docstring states 'Get program AST from ProgramManager' and calls 'program_ast = self.program.get_program_ast()' but this variable is never used. Both CodeMirror5Editor and CodeMirrorEditor implement statement-level breakpoints with char_start/char_end parameters (add_breakpoint(line_num, char_start, char_end) and set_current_statement(line_num, char_start, char_end)), but VisualBackend has no documentation or implementation showing how to use these statement-level features. The base class documentation doesn't mention statement-level debugging capabilities that the actual editor components support.

---

#### code_vs_comment

**Description:** Comment claims RUN is always valid and can be called at a breakpoint, but code checks self.running flag which prevents RUN from working when paused

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~1050: 'RUN is always valid - it's just CLEAR + GOTO first line. RUN on empty program is fine (just clears variables). RUN at a breakpoint restarts from the beginning.' However, the _menu_run method doesn't handle the case where self.running=True and self.paused=True (paused at breakpoint). The method would start a new execution timer without stopping the old one or resetting the paused state.

---

#### code_internal_inconsistency

**Description:** Breakpoint storage type inconsistency between PC objects and plain integers

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _toggle_breakpoint, breakpoints are stored as PC objects: 'pc = PC(line_num, stmt_offset); self.runtime.breakpoints.add(pc)'. But in _do_toggle_breakpoint (the dialog fallback), breakpoints are stored as plain integers: 'if line_num in self.runtime.breakpoints: self.runtime.breakpoints.remove(line_num)'. The _update_breakpoint_display method tries to handle both: 'if isinstance(item, PC)' but this mixing of types in the same set is problematic.

---

#### code_vs_documentation

**Description:** Help system URL mismatch - code points to localhost/mbasic_docs but documentation describes localhost:8000 with MkDocs server

**Affected files:**
- `src/ui/web_help_launcher.py`
- `docs/help/README.md`

**Details:**
Code uses HELP_BASE_URL = 'http://localhost/mbasic_docs' (line 17) but WebHelpLauncher_DEPRECATED class describes starting a local server on port 8000 (line 56). Documentation in README.md describes help being served at different paths. The deprecated class shows the old approach (build MkDocs, serve on port 8000) while the new approach uses a pre-configured web server at /mbasic_docs.

---

#### documentation_inconsistency

**Description:** Missing SETSETTING statement documentation

**Affected files:**
- `docs/help/common/settings.md`
- `docs/help/common/language/statements/showsettings.md`

**Details:**
settings.md extensively describes using 'SETSETTING' command (e.g., 'SETSETTING editor.auto_number_step 100') and showsettings.md lists 'SETSETTING' in 'See Also', but there is no setsetting.md file documenting the SETSETTING statement syntax and usage.

---

#### documentation_inconsistency

**Description:** Contradictory information about PEEK behavior

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/compatibility.md`

**Details:**
architecture.md states 'PEEK does NOT return values written by POKE' and describes PEEK as returning random values. However, compatibility.md states 'PEEK: Returns random integer 0-255 (for RNG seeding compatibility)' and 'PEEK does NOT return values written by POKE'. Both agree PEEK doesn't return POKE values, but architecture.md doesn't mention the random return value behavior that compatibility.md describes.

---

#### documentation_inconsistency

**Description:** Conflicting information about compiler implementation status

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/features.md`

**Details:**
architecture.md states 'Current Implementation: ✅ Interpreter (fully functional), Semantic Analyzer: ✅ Complete (18 optimizations), Code Generation: ❌ Not implemented (future work)'. features.md has a 'Compiler Features' section listing 'Semantic Analyzer' with 18 optimizations, implying these are active features. The architecture doc clarifies these are 'analysis only (no code generation yet)', but features.md presents them as if they're production features without this caveat.

---

#### documentation_inconsistency

**Description:** Contradictory statements about MBASIC 5.21 compatibility

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/extensions.md`

**Details:**
architecture.md states 'MBASIC is a runtime interpreter for MBASIC-80 programs' and describes it as implementing MBASIC-80. extensions.md states 'This is MBASIC-2025, a modern implementation of Microsoft BASIC-80 5.21 (CP/M era)'. The version numbering is inconsistent - is it MBASIC-80 or MBASIC 5.21? These may be the same thing, but the documentation should be consistent.

---

#### documentation_inconsistency

**Description:** Ctrl+X shortcut conflict

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
feature-reference.md documents two different functions for Ctrl+X: 'Stop/Interrupt (Ctrl+X): Stop a running program immediately' under Execution & Control, and in the Cut/Copy/Paste section it says 'Ctrl+X is used for Stop/Interrupt' explaining why cut isn't available. However, it also says 'Ctrl+C exits the program' which conflicts with standard terminal behavior where Ctrl+C typically interrupts execution.

---

#### documentation_inconsistency

**Description:** Tk settings documentation claims more configuration options than Web UI, but Web UI settings.md shows only auto-numbering and limits tabs, missing many settings described in Tk docs

**Affected files:**
- `docs/help/ui/tk/settings.md`
- `docs/help/ui/web/settings.md`

**Details:**
Tk settings.md describes tabs: Editor, Interpreter, Keywords, Variables, UI. Web settings.md only shows: Editor (auto-numbering only), Limits (view-only). Missing: Keywords tab (Case Style), Variables tab (Case Conflict, Show Types), Interpreter tab (Strict Mode, Max Execution Time, Debug Mode), UI tab (Theme, Font Size). The claim 'Web UI focuses on the most commonly used settings' contradicts the extensive feature list in Tk docs.

---

#### documentation_inconsistency

**Description:** Settings file location contradicts between Tk and Web implementations

**Affected files:**
- `docs/help/ui/tk/settings.md`
- `docs/help/ui/web/settings.md`

**Details:**
Tk settings.md states: 'Location: Linux/Mac: ~/.mbasic/settings.json, Windows: %APPDATA%\mbasic\settings.json'. Web settings.md states: 'Web UI settings are stored in your browser's localStorage' and 'To share settings across browsers or with CLI: ...save to ~/.mbasic/settings.json'. This implies Web UI does NOT use the same settings file as Tk/CLI, but the export instructions suggest they should be compatible. The relationship between localStorage settings and file-based settings is unclear.

---

#### documentation_inconsistency

**Description:** Step execution buttons described differently

**Affected files:**
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/debugging.md`

**Details:**
getting-started.md describes toolbar buttons: 'Step Line - Execute all statements on current line, then pause (⏭️ button), Step Stmt - Execute one statement, then pause (↻ button)'. debugging.md under 'Debug Controls' describes: 'Step over (F10), Step into (F11), Step out (Shift+F11)' without mentioning 'Step Line' or 'Step Stmt'. These appear to be different features or different names for the same features, creating confusion about what's actually available.

---

#### documentation_inconsistency

**Description:** Self-contradictory information about CLI Save functionality

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
UI_FEATURE_COMPARISON.md shows conflicting information: In the 'File Operations' table, it shows CLI has '❌' for 'Save (with prompt)' but '✅' for 'Save As'. In the 'Known Gaps' section, it states 'CLI: No Save without prompt'. In the 'Keyboard Shortcuts Comparison' table under 'Common Shortcuts', it shows CLI 'Save' as 'N/A' but 'Save As' as 'SAVE "file"'. This is contradictory - if CLI can do 'Save As' with SAVE command, the distinction between 'Save' and 'Save As' is unclear.

---

### 🟡 Medium Severity

#### code_internal_inconsistency

**Description:** Duplicate StopStatementNode definition with different docstrings

**Affected files:**
- `src/ast_nodes.py`

**Details:**
StopStatementNode is defined twice in ast_nodes.py. First definition at line ~450 has docstring 'STOP statement - halt execution (for debugging)'. Second definition at line ~700 has docstring 'STOP statement - pause program execution' with more detailed explanation about CONT. The second definition appears to be more complete and accurate.

---

#### code_vs_comment

**Description:** Method name mismatch between docstring and implementation

**Affected files:**
- `src/case_keeper.py`

**Details:**
CaseKeeperTable.set() method is documented and implemented, but case_string_handler.py calls table.register() which doesn't exist. The docstring in case_keeper.py shows 'set()' but case_string_handler.py line calls 'display_case = table.register(text, original_text, line, column)'

---

#### code_vs_comment

**Description:** Comment about negative zero handling may not match implementation

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line 267 comment says 'Determine sign BEFORE rounding (for negative zero handling)' and line 276 says 'use original sign for values that round to zero', but the logic at line 277-280 only preserves negative sign for rounded zero, not positive sign. This asymmetry may be intentional for BASIC compatibility but is not clearly documented.

---

#### code_implementation

**Description:** Identifier case handling not implemented despite comment

**Affected files:**
- `src/case_string_handler.py`

**Details:**
Lines 54-56 say 'Identifier case handling would go here if needed' and 'For now, identifiers preserve their original case', but the function is called with setting_prefix='idents' suggesting it should be implemented. The get_identifier_table() method exists but is never used.

---

#### code_vs_comment

**Description:** SandboxedFileIO docstring claims it's a stub but provides implementation details

**Affected files:**
- `src/file_io.py`

**Details:**
Class docstring says: 'Uses browser localStorage for file storage. Files are stored per-user session with 'mbasic_file_' prefix. No access to server filesystem - all files are client-side only.'

But the NOTE section says: 'NOTE: This is a STUB implementation. ui.run_javascript() requires async/await which can't be used from synchronous interpreter code. For now, returns empty results.'

All methods raise IOError or return empty results, contradicting the detailed implementation description in the docstring.

---

#### code_vs_comment

**Description:** SandboxedFileIO.list_files() implementation contradicts its docstring stub note

**Affected files:**
- `src/file_io.py`

**Details:**
The NOTE in the class docstring says 'For now, returns empty results' and mentions it's a STUB implementation. However, list_files() has actual implementation code:
```python
if hasattr(self.backend, 'sandboxed_fs'):
    pattern = filespec.strip().strip('"').strip("'") if filespec else None
    files = self.backend.sandboxed_fs.list_files(pattern)
    # Convert to expected format
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
This is not a stub - it delegates to backend.sandboxed_fs which appears to be the src/filesystem/sandboxed_fs.py implementation.

---

#### code_vs_documentation

**Description:** ProgramManager doesn't use FileIO abstraction despite its existence

**Affected files:**
- `src/editing/manager.py`
- `src/file_io.py`

**Details:**
ProgramManager.save_to_file() and load_from_file() use direct Python file operations:
```python
def save_to_file(self, filename: str) -> None:
    with open(filename, 'w') as f:
        for line_number in sorted(self.lines.keys()):
            f.write(self.lines[line_number] + '\n')
```

But src/file_io.py provides FileIO abstraction specifically for this purpose. The FileIO docstring says: 'Different UIs provide different implementations: - Local UIs (TK/Curses/CLI): RealFileIO (direct filesystem) - Web UI: SandboxedFileIO (browser localStorage)'

ProgramManager should accept a FileIO instance to support different UI backends, but it doesn't.

---

#### code_vs_documentation

**Description:** ProgramManager.merge_from_file() is not documented in class docstring

**Affected files:**
- `src/editing/manager.py`

**Details:**
The ProgramManager class docstring lists operations under 'This class handles:' including 'File operations (SAVE, LOAD)' and 'Line editing (NEW, DELETE, RENUM)'. However, merge_from_file() is a significant file operation that is not mentioned. The Usage section also doesn't show merge_from_file() despite showing save_to_file() and load_from_file().

---

#### code_vs_comment

**Description:** Docstring claims 'Cannot use multi-statement lines (no : separator)' but code doesn't enforce this limitation

**Affected files:**
- `src/immediate_executor.py`

**Details:**
The _show_help() method's help text states 'Cannot use multi-statement lines (no : separator)' under LIMITATIONS, but the execute() method parses and executes all statements in line_node.statements without checking for or rejecting multiple statements. The parser would handle ':' separators normally.

---

#### code_vs_comment

**Description:** Help text claims 'Cannot use GOTO, GOSUB, or control flow statements' but code doesn't enforce this

**Affected files:**
- `src/immediate_executor.py`

**Details:**
The _show_help() method lists 'Cannot use GOTO, GOSUB, or control flow statements' as a limitation, but the execute() method calls interpreter.execute_statement(stmt) without any filtering or validation of statement types. GOTO/GOSUB would be executed if parsed.

---

#### code_vs_comment

**Description:** Help text claims 'Cannot define or call functions (DEF FN)' but code doesn't enforce this

**Affected files:**
- `src/immediate_executor.py`

**Details:**
The _show_help() method lists 'Cannot define or call functions (DEF FN)' as a limitation, but the execute() method would execute DEF FN statements if parsed, as it calls interpreter.execute_statement(stmt) without filtering.

---

#### code_vs_comment

**Description:** Docstring claims numbered lines edit the program, but implementation has conditional logic that may not work

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Line ~125 comment says 'In real MBASIC, typing a numbered line in immediate mode adds/edits that line' and the code attempts to handle this, but it checks 'if hasattr(self.interpreter, 'interactive_mode')' which is a very specific attribute that may not exist. The fallback returns 'Cannot edit program lines in this mode' suggesting the feature may not work in all contexts despite being documented as a general feature.

---

#### code_vs_comment

**Description:** Comment claims RENUM uses AST-based approach, but implementation delegates to ui_helpers without showing AST usage

**Affected files:**
- `src/interactive.py`

**Details:**
Line 663-670: Docstring says 'Uses AST-based approach: 1. Parse program to AST 2. Build line number mapping (old -> new) 3. Walk AST and update all line number references 4. Serialize AST back to source'. However, cmd_renum() just calls renum_program() from ui_helpers and passes self._renum_statement callback. The AST walking is not visible in this method.

---

#### code_vs_comment

**Description:** Comment claims lines/line_asts are properties delegating to program manager, but they're actually direct dictionary access

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 59-61: Comment says '# For backward compatibility, provide direct access to lines/line_asts (These are now properties that delegate to program manager)'. Lines 75-82 show @property decorators that return self.program.lines and self.program.line_asts, which are direct dictionary references, not delegation methods.

---

#### code_vs_comment

**Description:** Comment about readline Ctrl+A binding conflicts with actual MBASIC Ctrl+A handling

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 138-140: Comment says 'Bind Ctrl+A to insert itself (so we can detect it in input). This overrides the default Ctrl+A (beginning-of-line) for MBASIC compatibility'. However, lines 163-178 show Ctrl+A handling in start() method that checks for character code 0x01, suggesting the readline binding may not work as described since readline would consume the Ctrl+A before it reaches the input string.

---

#### code_vs_comment

**Description:** Docstring for cmd_cont describes tick-based loop but doesn't mention state management details

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 289-291: Docstring says 'CONT - Continue execution after STOP or Break'. Implementation shows complex state management (lines 297-324) including stopped flag clearing, PC restoration, and error handling, but docstring doesn't mention these critical details. This could mislead developers about the complexity of CONT implementation.

---

#### code_internal_inconsistency

**Description:** Inconsistent error handling between cmd_run and cmd_cont

**Affected files:**
- `src/interactive.py`

**Details:**
cmd_run (lines 186-227) has try/except with print_error(e, runtime) at the end. cmd_cont (lines 289-324) also has try/except with print_error(e, self.program_runtime). However, cmd_run handles KeyboardInterrupt specially within the tick loop (lines 214-218), while cmd_cont has identical KeyboardInterrupt handling (lines 311-315). The duplication suggests these should be refactored into a shared method.

---

#### code_vs_comment

**Description:** Comment about ERL comparison handling doesn't match actual implementation scope

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 730-741: Docstring says 'Handle ERL = line_number patterns in expressions. According to MBASIC manual: if ERL appears on the left side of =, the number on the right side is treated as a line number reference. Also handles: ERL <> line, ERL < line, ERL > line, etc.' However, implementation only checks for BinaryOpNode and doesn't verify the operator type, so it would renumber 'ERL + 100' or 'ERL * 2' which are not line number references.

---

#### code_vs_comment

**Description:** EDIT command docstring describes full character-by-character editor but implementation may not handle all subcommands

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 813-829: Docstring lists many edit subcommands including '[n]D: Delete n characters', '[n]S<ch>: Search for nth occurrence', '[n]K<ch>: Kill up to nth occurrence', '[n]C: Change next n characters'. However, implementation (lines 875-936) only shows simple 'D' (delete one char) and 'C' (change one char) without count prefix support. The 'S' and 'K' commands are not implemented at all.

---

#### code_vs_comment

**Description:** Docstring for execute_immediate describes runtime selection logic that may not match actual behavior

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 1073-1079: Docstring says 'Uses persistent runtime so variables persist between statements. If a program has been run (or stopped), use the program runtime so immediate mode can examine/modify program variables.' However, lines 1091-1094 show 'if self.program_runtime is not None:' which would be true even if program finished (not just stopped), potentially causing confusion about when program vs immediate runtime is used.

---

#### code_vs_comment

**Description:** Comment about NEXT processing order conflicts with actual implementation behavior

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_next() at line ~1230, comment says 'NEXT I, J, K is equivalent to: NEXT I: NEXT J: NEXT K' and 'If any loop continues (not finished), we jump back and stop processing.' However, the code at line ~1250 processes variables in order and returns early if a loop continues, which means NEXT I,J would only process J if I's loop finished. This is correct BASIC behavior but the comment's 'equivalent to' phrasing is misleading - they're not truly equivalent since separate NEXT statements would each check their own loop.

---

#### code_vs_comment

**Description:** Docstring for InterpreterState says 'no complex status modes' but then lists multiple status indicators

**Affected files:**
- `src/interpreter.py`

**Details:**
InterpreterState docstring at line ~30 says 'State is now simplified - no complex status modes' but then immediately lists checking runtime.halted, input_prompt, and error_info as different states. The class also has pause_requested, skip_next_breakpoint_check, and is_first_line fields. This contradicts the 'simplified' claim.

---

#### code_vs_comment

**Description:** Comment about return_stmt validation is imprecise about boundary condition

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_return() at line ~1320, comment says 'return_stmt can be == len(statements), meaning "past the end, go to next line"' but then checks 'if return_stmt > len(line_statements)'. The comment suggests == len is valid (past the end), but the validation only rejects > len. This is correct code (== len is valid for 'next statement after last'), but comment could be clearer that the check is for strictly greater than.

---

#### documentation_inconsistency

**Description:** InterpreterState docstring references 'breakpoints are stored in Runtime' but doesn't mention skip_next_breakpoint_check field purpose

**Affected files:**
- `src/interpreter.py`

**Details:**
InterpreterState docstring at line ~40 says '# Debugging (breakpoints are stored in Runtime, not here)' but then has skip_next_breakpoint_check field without explaining its relationship to breakpoints. The field is used in tick_pc() to allow execution past a breakpoint after hitting it, but this isn't documented in the state class.

---

#### code_vs_comment

**Description:** Comment about 'old-style stack' suggests deprecated approach but no alternative mentioned

**Affected files:**
- `src/interpreter.py`

**Details:**
In execute_gosub() at line ~1180, comment says '# Use old-style stack for compatibility (stores line, offset from PC)'. The phrase 'old-style' and 'for compatibility' suggests this is deprecated or temporary, but there's no indication of what the 'new-style' would be or why this is kept. This creates confusion about whether this is technical debt or intentional design.

---

#### code_vs_comment

**Description:** execute_resume comment says 'RESUME or RESUME 0' but code checks for 'stmt.line_number is None or stmt.line_number == 0'

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: '# RESUME or RESUME 0 - retry the statement that caused the error'
Code: 'if stmt.line_number is None or stmt.line_number == 0:'
The comment suggests RESUME 0 is valid, but the code treats both None and 0 the same way. This is ambiguous about whether RESUME 0 is actually a valid syntax or if 0 is just a sentinel value.

---

#### code_vs_comment

**Description:** execute_optionbase comment says 'MBASIC 5.21 behavior' but doesn't document what other versions do

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: 'Must be executed BEFORE any arrays are DIM'd (MBASIC 5.21 behavior).'
This implies other versions might behave differently, but doesn't document what those differences are or why 5.21 was chosen as the reference.

---

#### code_vs_comment

**Description:** _read_line_from_file has extensive CP/M documentation but doesn't explain why latin-1 encoding is used

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment extensively documents CP/M ^Z behavior but the line 'return line_bytes.decode('latin-1', errors='replace')' doesn't explain why latin-1 is chosen. CP/M used ASCII, so this encoding choice should be documented.

---

#### code_vs_comment

**Description:** execute_clear comment says 'as requested' for ignoring parameters but doesn't reference where this was requested

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: '# Note: We ignore string_space and stack_space parameters as requested'
This references a request but doesn't cite where (issue number, design doc, etc.). Future maintainers won't know why this decision was made.

---

#### code_vs_comment

**Description:** execute_open comment says 'not fully supported' for random access but doesn't specify what's missing

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: 'OPEN "R", #4, "filename", 128   - Open for random access (not fully supported)'
Doesn't document which features of random access are supported and which aren't. The code appears to implement GET, PUT, FIELD, LSET, RSET, so it's unclear what's missing.

---

#### code_vs_comment

**Description:** execute_list comment doesn't mention that it uses line_text_map, which may not match the AST

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment describes LIST behavior but doesn't mention that it outputs from line_text_map rather than regenerating from AST. This could be inconsistent if line_text_map gets out of sync with the AST.

---

#### code_vs_comment

**Description:** Comment in execute_stop says 'use npc which points to next statement' but code uses self.runtime.npc without verifying it points to the correct next statement

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: '# Save PC position for CONT (use npc which points to next statement)' followed by 'self.runtime.stop_pc = self.runtime.npc'. However, there's no verification that npc is correctly set or that it actually points to the next statement after STOP. The comment assumes npc behavior that may not be guaranteed.

---

#### documentation_inconsistency

**Description:** execute_cont docstring says 'CONT resumes execution after a STOP or Break (Ctrl+C)' but only STOP is implemented, not Ctrl+C break handling

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring: 'CONT resumes execution after a STOP or Break (Ctrl+C).' However, the execute_stop method only handles explicit STOP statements. There's no visible Ctrl+C/Break handling in this code that would set runtime.stopped=True, so CONT cannot actually resume from Ctrl+C breaks as documented.

---

#### code_vs_comment

**Description:** execute_step docstring says 'STEP executes one or more statements, then pauses' but implementation does nothing

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring: 'STEP executes one or more statements, then pauses.' Implementation: 'self.io.output(f"STEP {count} - Debug stepping not fully implemented")' followed by comment 'For now, just acknowledge the command'. The function doesn't execute any statements or pause, contradicting its documented behavior.

---

#### code_vs_documentation

**Description:** Method signature mismatch for locate/set_cursor_position

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/web_io.py`

**Details:**
base.py defines 'locate(self, row: int, col: int) -> None' but web_io.py implements 'set_cursor_position(self, row, col)' with different name. Additionally, base.py documents locate() as optional (non-abstract) while web_io.py treats it as if it were required.

---

#### code_vs_documentation

**Description:** Extra method not in interface: get_screen_size()

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/web_io.py`

**Details:**
web_io.py implements 'get_screen_size(self)' which is not defined in the IOHandler base class interface. This method is not part of the abstract interface contract.

---

#### code_vs_comment

**Description:** Comment claims KeywordCaseManager but code uses SimpleKeywordCase

**Affected files:**
- `src/lexer.py`

**Details:**
lexer.py line 'self.keyword_case_manager = keyword_case_manager or SimpleKeywordCase(policy="force_lower")' and function 'create_keyword_case_manager() -> SimpleKeywordCase' use SimpleKeywordCase class. However, src/keyword_case_manager.py defines a different class called KeywordCaseManager. The comment in lexer.py says '# Keyword case manager - simple policy-based handler' suggesting it should use KeywordCaseManager, but actually uses SimpleKeywordCase.

---

#### code_vs_documentation

**Description:** Two different keyword case management implementations exist

**Affected files:**
- `src/lexer.py`
- `src/keyword_case_manager.py`

**Details:**
src/keyword_case_manager.py defines KeywordCaseManager class with register_keyword() and get_display_case() methods. However, src/lexer.py imports and uses SimpleKeywordCase (not shown in provided files but referenced). This suggests duplicate/conflicting implementations of the same functionality.

---

#### code_vs_comment

**Description:** Comment states APOSTROPHE is not treated as end-of-line, but code implementation treats it as end-of-statement

**Affected files:**
- `src/parser.py`

**Details:**
In at_end_of_line() docstring: 'Note: APOSTROPHE is now treated as a statement (comment), not end-of-line, so it can be preserved in the AST.' However, at_end_of_statement() includes APOSTROPHE in the list of tokens that end a statement: 'return token.type in (TokenType.NEWLINE, TokenType.EOF, TokenType.COLON, TokenType.REM, TokenType.REMARK, TokenType.APOSTROPHE)'. This creates ambiguity about whether APOSTROPHE ends a line/statement or is just a statement type.

---

#### code_vs_comment

**Description:** Inconsistent handling of semicolon as statement separator vs trailing separator

**Affected files:**
- `src/parser.py`

**Details:**
In parse_line(), semicolon is handled specially: 'elif self.match(TokenType.SEMICOLON): # Allow trailing semicolon (treat as no-op, like some dialects)' with error if more follows. However, in parse_print() and parse_lprint(), semicolon is treated as a normal separator between expressions. The comment suggests semicolon should only be trailing, but print statements use it as an item separator.

---

#### code_vs_comment

**Description:** Comment about MID$ detection logic doesn't match actual implementation complexity

**Affected files:**
- `src/parser.py`

**Details:**
In parse_statement() around line 550, the comment says 'MID$ is tokenized as single MID token ($ is part of the keyword)' and 'We need to peek past the parentheses to see if there's an ='. However, the code then has a try/except block that advances through tokens, counts parentheses, and restores position. The comment suggests a simpler peek operation than what's actually implemented.

---

#### code_vs_comment

**Description:** Comment about RND and INKEY$ without parentheses contradicts general function parsing pattern

**Affected files:**
- `src/parser.py`

**Details:**
In parse_builtin_function(), special cases are made for RND and INKEY$ to be called without parentheses: 'RND can be called without parentheses' and 'INKEY$ can be called without parentheses'. However, the general pattern established earlier is that functions require parentheses. This special casing is implemented but not mentioned in the module-level documentation about expression parsing.

---

#### code_implementation

**Description:** Inconsistent handling of type suffix in variable names across different parsing contexts

**Affected files:**
- `src/parser.py`

**Details:**
In parse_variable_or_function(), type suffix is stripped from 'name' and 'original_case', and explicit_type_suffix is set. However, in parse_fn_call(), the type suffix is stripped from raw_name but there's no tracking of whether it was explicit. In get_variable_type(), the suffix check uses 'name[-1]' but doesn't account for whether the name has already been stripped of its suffix in prior processing.

---

#### code_comment_conflict

**Description:** Comment about prompt_separator variable that is never used

**Affected files:**
- `src/parser.py`

**Details:**
In parse_input() around line 50-60, the code sets prompt_separator = ';' or ',' based on token type, with comment 'Check separator after prompt (comma or semicolon both show "?")'. However, the prompt_separator variable is assigned but never used or passed to InputStatementNode. The node only receives suppress_question boolean.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of InputStatementNode parameters

**Affected files:**
- `src/parser.py`

**Details:**
The parse_input() method creates InputStatementNode with parameters: prompt, variables, file_number, suppress_question, line_num, column. However, it sets prompt_separator variable (line ~60) which is never passed to the node constructor. The suppress_question parameter is set but prompt_separator is computed and discarded.

---

#### code_internal_inconsistency

**Description:** Inconsistent comment about ERASE statement in parse_erase() docstring

**Affected files:**
- `src/parser.py`

**Details:**
The parse_erase() docstring at line ~1330 shows example 'ERASE M:DIM M(64)' suggesting ERASE and DIM can be on same line with colon separator. However, the parse_erase() implementation breaks on TokenType.COLON (line ~1340), which would prevent parsing the DIM part. This suggests the example is misleading or the implementation doesn't match the documented capability.

---

#### code_vs_comment

**Description:** parse_call docstring describes MBASIC 5.21 standard syntax as only accepting numeric addresses, but implementation accepts extended syntax with arguments

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states 'Standard MBASIC 5.21 Syntax: CALL address - Call machine code at numeric address' and 'Note: Also accepts extended syntax for other BASIC dialects.' However, the code implementation fully parses arguments: 'if isinstance(target, VariableNode) and target.subscripts: arguments = target.subscripts' and 'elif isinstance(target, FunctionCallNode): arguments = target.arguments'. The comment suggests this is an extension, but the code treats it as primary functionality without any dialect checking.

---

#### code_vs_comment

**Description:** parse_resume docstring comment about line number 0 validity conflicts with special value usage

**Affected files:**
- `src/parser.py`

**Details:**
Comment states 'line_number = -1  # -1 means RESUME NEXT (0 is a valid line number)' suggesting 0 is a valid line number. However, using -1 as a special sentinel value when 0 is valid could be confusing. In BASIC, line number 0 is typically not used, so this comment may be misleading about what constitutes a 'valid' line number in practice.

---

#### code_vs_comment

**Description:** StatementTable uses regular dict but comment claims it uses ordered dict

**Affected files:**
- `src/pc.py`

**Details:**
Line 93 comment says 'Uses Python 3.7+ ordered dict' but line 96 initializes with `self.statements = {}` which is just a regular dict literal. While dicts are ordered in Python 3.7+, the comment is misleading as it suggests special handling.

---

#### code_vs_comment

**Description:** Docstring says 'preserving the original token positions and spacing' but implementation may create conflicts

**Affected files:**
- `src/position_serializer.py`

**Details:**
Module docstring (line 1-6) says 'Serializes AST nodes back to source text while preserving the original token positions and spacing' but the PositionConflict class and conflict tracking throughout suggests positions are NOT always preserved - conflicts occur when expected_column < current_column.

---

#### code_vs_comment

**Description:** Comment says 'TODO: track operator position' but no tracking mechanism exists

**Affected files:**
- `src/position_serializer.py`

**Details:**
Line 327 has comment '# Equals sign (TODO: track operator position)' but there's no issue tracking system referenced, no data structure for storing operator positions, and the emit_token call passes None for column.

---

#### code_vs_comment

**Description:** Comment says 'MBASIC 5.21 limit' for string length but no verification this matches actual MBASIC behavior

**Affected files:**
- `src/resource_limits.py`

**Details:**
Lines 28, 88, 149, 169, 189 all reference '255 bytes (MBASIC 5.21 limit)' for max_string_length, but there's no source citation or verification that MBASIC 5.21 actually had this limit. This could be incorrect historical information.

---

#### code_vs_comment

**Description:** Comment claims _resolve_variable_name is 'the ONLY correct way' but code shows multiple direct access patterns

**Affected files:**
- `src/runtime.py`

**Details:**
Line 91 comment states: 'This is the ONLY correct way to determine the storage key for a variable.' However, the code contains methods like get_variable_raw() and set_variable_raw() that bypass this resolution, and internal code directly accesses self._variables with full names. The comment overstates the exclusivity.

---

#### code_vs_comment

**Description:** Comment about error state tracking contradicts actual implementation

**Affected files:**
- `src/runtime.py`

**Details:**
Lines 182-186 state: 'Note: Error state tracking removed - use state.error_info instead' and 'error_occurred = (state.error_info is not None)'. However, the code still maintains self.error_handler and self.error_handler_is_gosub attributes (lines 180-181), suggesting error handling state is partially maintained in Runtime, not fully removed.

---

#### code_vs_comment

**Description:** Comment about ERR and ERL initialization placement is confusing

**Affected files:**
- `src/runtime.py`

**Details:**
Lines 188-191: 'ERR and ERL are system variables (integer type), not functions. Initialize them in the variable table with % suffix (lowercase). Note: Must do this after _variables is created but before methods are called. We'll initialize these after other attributes are set up.' This comment suggests initialization happens later, but lines 203-204 show initialization happens immediately: 'self.set_variable_raw('err%', 0)' and 'self.set_variable_raw('erl%', 0)'.

---

#### documentation_inconsistency

**Description:** Module docstring lists features that may not all be implemented in this file

**Affected files:**
- `src/runtime.py`

**Details:**
Lines 3-12 list features managed by this module including 'File I/O state' and 'Program counter (PC) based execution'. While self.files and self.field_buffers exist (lines 178-179), and PC attributes exist (lines 159-162), the actual file I/O operations and PC execution logic are not visible in this code snippet, suggesting they may be implemented elsewhere.

---

#### code_vs_comment

**Description:** set_variable_raw() docstring says 'Use this only for special cases' but then calls set_variable() internally

**Affected files:**
- `src/runtime.py`

**Details:**
Lines 447-449: 'Use this only for special cases like system variables. For normal variables, use set_variable() instead.' But then lines 451-452: 'This now calls set_variable() internally for uniform handling.' This creates confusion about when to use which method, since set_variable_raw() is now just a wrapper.

---

#### code_vs_comment

**Description:** Inconsistent documentation of what 'debugger_set' parameter means

**Affected files:**
- `src/runtime.py`

**Details:**
Line 338 docstring: 'debugger_set: True if this set is from debugger, not program execution'. But line 369 comment: 'Debugger/prompt set: use line -1 as sentinel'. The term 'prompt' is not mentioned in the parameter documentation, creating ambiguity about whether interactive prompt sets should use debugger_set=True.

---

#### code_vs_comment

**Description:** get_execution_stack() docstring says 'from_line' is the line where GOSUB was called, but code sets it to 'return_line' (where execution will resume after RETURN)

**Affected files:**
- `src/runtime.py`

**Details:**
Docstring says: "'from_line': 50" in example where 50 is described as where GOSUB was called. But code does: "'from_line': entry.get('return_line', 0),  # Line to return to" - the comment explicitly says this is the return line, not the calling line. The docstring example shows 'from_line': 50, 'return_line': 60, suggesting they should be different values, but the code sets both to the same value.

---

#### code_vs_comment

**Description:** reset_for_run() comment says 'NOTE: self.common_vars is NOT cleared' but there is no self.common_vars attribute visible in the code

**Affected files:**
- `src/runtime.py`

**Details:**
At the end of reset_for_run(), there's a comment: "# NOTE: self.common_vars is NOT cleared - preserved for CHAIN compatibility" but the code never references self.common_vars anywhere in the visible portion. This could be a reference to code in another part of the file, or an outdated comment.

---

#### code_vs_documentation

**Description:** Settings definition for keywords.case_style includes 'force_capitalize' option but simple_keyword_case.py documentation says keywords only need three policies without explaining what they are

**Affected files:**
- `src/settings_definitions.py`
- `src/simple_keyword_case.py`

**Details:**
settings_definitions.py defines choices=['force_lower', 'force_upper', 'force_capitalize'] with description 'lowercase (MBASIC 5.21), UPPERCASE (classic), or Capitalize (modern)'. simple_keyword_case.py docstring says 'Keywords only need three policies' and lists them, but doesn't explain the rationale as clearly as the settings definition does.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation about setting key format between modules

**Affected files:**
- `src/settings.py`
- `src/settings_definitions.py`

**Details:**
settings.py docstrings use examples like 'variables.case_conflict' and 'editor.auto_number', while settings_definitions.py uses the same format. However, the _flatten_settings and _unflatten_settings methods suggest nested dict storage internally, but this internal representation is not clearly documented in the module docstring.

---

#### code_vs_comment

**Description:** Comment says 'Fallback for old policies' but doesn't document what the old policies were

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
In __init__ method: 'if policy not in ["force_lower", "force_upper", "force_capitalize"]: # Fallback for old policies policy = "force_lower"'. This suggests there were previous policy names that are no longer supported, but they're not documented.

---

#### code_vs_comment

**Description:** Comment says 'for backward compatibility' but doesn't explain what changed or when

**Affected files:**
- `src/ui/cli.py`

**Details:**
CLIBackend docstring: 'Currently wraps the existing InteractiveMode for backward compatibility. In the future, this could be refactored to use UIBackend interface more directly.' This suggests a transition period but doesn't document the timeline or what the old interface was.

---

#### missing_reference

**Description:** CLIBackend imports from 'interactive' and 'editing' modules that are not provided in the source files

**Affected files:**
- `src/ui/cli.py`

**Details:**
CLIBackend imports 'from interactive import InteractiveMode' and references 'from editing import ProgramManager' in usage example, but these modules are not included in the provided source files. This makes it impossible to verify consistency.

---

#### missing_reference

**Description:** CLIBackend imports from '.cli_debug' module that is not provided

**Affected files:**
- `src/ui/cli.py`

**Details:**
CLIBackend.__init__ imports 'from .cli_debug import add_debug_commands' but this module is not included in the provided source files.

---

#### code_vs_documentation

**Description:** CLI debug has BREAK command but curses UI uses 'toggle_breakpoint' terminology

**Affected files:**
- `src/ui/cli_debug.py`
- `src/ui/curses_keybindings.json`

**Details:**
cli_debug.py implements 'BREAK' command for setting/clearing/listing breakpoints. curses_keybindings.json has 'toggle_breakpoint' (Ctrl+B) which implies different behavior (toggle vs set/clear/list). The CLI version supports 'BREAK 100' to set, 'BREAK 100-' to clear, 'BREAK CLEAR' to clear all, and 'BREAK' to list. The curses version only mentions 'Toggle breakpoint' which is a subset of functionality.

---

#### code_vs_documentation

**Description:** CLI debug has STACK command but no equivalent in curses keybindings

**Affected files:**
- `src/ui/cli_debug.py`
- `src/ui/curses_keybindings.json`

**Details:**
cli_debug.py implements 'cmd_stack' to show GOSUB call stack and FOR loop stack. curses_keybindings.json has no corresponding keybinding for viewing the stack, suggesting this debugging feature is missing from the curses UI.

---

#### code_vs_comment

**Description:** Docstring for _on_apply says 'Handle Apply button' but there is no Apply button widget

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
Methods _on_apply, _on_ok, _on_cancel, and _on_reset all have docstrings saying 'Handle [X] button' but these are actually keyboard shortcut handlers (Ctrl+A for apply, Enter for OK, ESC for cancel, Ctrl+R for reset) as shown in keypress() method and footer text. The docstrings incorrectly describe them as button handlers.

---

#### code_vs_comment

**Description:** enhance_run_command docstring describes 'start_line' parameter but original_run signature is unknown

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
The enhanced_run function has docstring 'Args: start_line: Optional line number to start execution at' and calls 'original_run(start_line=start_line)'. However, we don't see the original cmd_run implementation to verify it actually accepts this parameter. The code assumes this parameter exists but it's not validated.

---

#### code_internal_inconsistency

**Description:** STEP command checks program_interpreter.state.program_ended but STACK command only checks program_runtime existence

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
In cmd_step: 'if self.interactive.program_interpreter.state.program_ended' but in cmd_stack: 'if not self.interactive.program_runtime'. These use different attributes to check program state, suggesting inconsistent state management or one check is incomplete.

---

#### code_vs_comment

**Description:** Comment describes 5-character line number column but code implements variable-width line numbers

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line 1009 comment says 'Line number column (5 chars, right-aligned)' and formats as 'line_num_str = f"{line_num}"' without padding, but earlier comments at line 1000 say 'Format: "SNNNNN CODE"' suggesting fixed 5-char width. The actual implementation uses variable width (no padding/formatting).

---

#### code_vs_comment

**Description:** Docstring describes 3-column layout with 5-char line numbers but code implements variable-width

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
ProgramEditorWidget docstring at line 176 says 'Columns: 1. Status (1 char)... 2. Line number (5 chars)... 3. Program text (rest)' but the implementation uses variable-width line numbers throughout (no 5-char formatting).

---

#### code_vs_comment

**Description:** Comment describes 'SNNNNN CODE' format but _update_display creates variable-width format

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line 1119 comment says 'Format: "SNN " where S=status (1 space), NN=line# (variable), space (1)' which correctly describes variable width, but this contradicts the docstring and other comments that say 5 chars.

---

#### code_vs_comment

**Description:** Code reformats with fixed-width but parser expects variable-width

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line 1449 does 'line_num_formatted = f"{num_str:>5}"' (right-aligned 5 chars) but the _parse_line_number method and other code expects variable-width. This creates inconsistency in the internal format.

---

#### code_vs_comment

**Description:** Comment says 'Create one interpreter for the session - don't create multiple!' but code creates new interpreter instances in start() method

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In __init__: comment says 'Create one interpreter for the session - don't create multiple!' and creates self.interpreter. But in start() method: 'immediate_io = OutputCapturingIOHandler()' and 'self.immediate_executor = ImmediateExecutor(self.runtime, self.interpreter, immediate_io)' creates new OutputCapturingIOHandler and reinitializes immediate_executor, suggesting the interpreter might be recreated or reinitialized.

---

#### code_vs_comment

**Description:** Comment describes inserting line BEFORE current, but variable naming suggests inserting BETWEEN previous and current

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _smart_insert_line() method: comment says 'Find the next line after current (to insert between prev and current)' and 'We want to insert BEFORE current, so find line before current'. Later comment says 'Insert blank line BEFORE current line (at current line's position)'. The logic finds prev_line_num and calculates midpoint between prev and current, which would insert BETWEEN them, not strictly BEFORE current.

---

#### code_vs_comment

**Description:** Comment says 'Wrap in AttrMap to force black background when redrawing' but this only happens in one branch

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _activate_menu() method's menu_input handler: comment says '# Wrap in AttrMap to force black background when redrawing' but this wrapping only occurs in the else branch when no overlay/settings/keymap is open. The other branches don't wrap in AttrMap, creating inconsistent behavior.

---

#### code_vs_comment

**Description:** Comment says 'RUN = CLEAR + GOTO first line' but code behavior differs when start_line is specified

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _setup_program(), comment states: '# Reset runtime with current program - RUN = CLEAR + GOTO first line'. However, when start_line parameter is provided, the code sets PC to that line instead of the first line. The comment should clarify that start_line overrides the default 'first line' behavior, or the comment is describing only the default RUN behavior without arguments.

---

#### code_vs_comment

**Description:** Comment about PC restoration logic doesn't match actual condition

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _sync_program_to_runtime(), comment says '# Restore PC only if execution is actually running' but the condition checks 'if self.running and not self.paused_at_breakpoint'. This means PC is NOT restored when paused at breakpoint, even though execution is technically 'running' (just paused). The comment should clarify this distinction or the logic may be incorrect.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of empty program between _setup_program and _run_program

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _setup_program(), when program.lines is empty, it sets 'self.running = False' and returns False. However, the comment says 'If empty program, just show Ready (variables cleared, nothing to execute)' but doesn't actually show 'Ready' - that's done by the caller. The status_bar.set_text('Ready') is only set in _execute_tick when program completes, not for empty programs in _setup_program.

---

#### code_vs_comment

**Description:** Comment about 'statement-level precision' for GOSUB but code shows statement index as 'return_stmt'

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_stack_window(), comment says '# Show statement-level precision for GOSUB return address' and code uses 'return_stmt = entry.get('return_stmt', 0)'. However, the display format 'line {entry['from_line']}.{return_stmt}' suggests this is a statement offset/index, not a 'statement number'. The terminology is inconsistent - is it 'statement-level', 'statement offset', or 'statement index'?

---

#### code_vs_comment

**Description:** Comment claims 'don't reset PC' but code behavior may not preserve PC correctly

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line comment says '# Sync program to runtime (but don't reset PC - keep current execution state)' followed by call to '_sync_program_to_runtime()'. Without seeing the implementation of _sync_program_to_runtime(), it's unclear if this method actually preserves PC or resets it. The comment suggests preservation is important but there's no visible code ensuring this.

---

#### code_vs_comment

**Description:** Comment says 'Don't call interpreter.start()' but then manually manipulates state in a way that may be fragile

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line '# NOTE: Don't call interpreter.start() because it resets PC!' followed by manual state initialization: 'if not hasattr(self.interpreter, 'state') or self.interpreter.state is None: self.interpreter.state = InterpreterState(_interpreter=self.interpreter)'. This suggests the normal start() method exists but can't be used, requiring manual workaround. This is fragile and may break if InterpreterState initialization requirements change.

---

#### code_vs_comment

**Description:** Comment claims output goes to 'output window' but variable name suggests 'output pane'

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment says '# Log the command to output window (not separate immediate history)' and '# Log the result to output window', but uses 'output_walker' which typically refers to a pane or list widget. The terminology inconsistency (window vs pane) may indicate confusion about the UI structure.

---

#### code_vs_comment

**Description:** Comment describes behavior 'This is what the tick loop does' but doesn't verify consistency

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment says '# This is what the tick loop does after executing a statement' when moving npc to pc. This suggests the code is mimicking behavior from elsewhere, but there's no verification that the two implementations stay in sync. If the tick loop changes, this code may become inconsistent.

---

#### code_vs_comment

**Description:** Comment says 'Switch interpreter IO to a capturing handler' but doesn't explain why or when this is necessary

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line '# Switch interpreter IO to a capturing handler that outputs to the output pane' followed by complex logic to create/reuse CapturingIOHandler. The comment doesn't explain why this switch is needed at this point, or what the IO handler was before, making the code's intent unclear.

---

#### Code vs Documentation inconsistency

**Description:** help_widget.py hardcodes 'curses' UI name when initializing HelpMacros, but HelpMacros is designed to work with any UI name passed to constructor

**Affected files:**
- `src/ui/help_widget.py`
- `src/ui/help_macros.py`

**Details:**
help_widget.py line 42: self.macros = HelpMacros('curses', help_root) - hardcoded 'curses' instead of accepting ui_name parameter. HelpMacros.__init__ expects ui_name parameter to load correct keybindings.

---

#### Code vs Comment conflict

**Description:** Comment says 'Ctrl+K reassigned to step line' but LIST_KEY is loaded from JSON as 'step_line' action, suggesting it may not be hardcoded reassignment

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py line 103: '# Execution stack window (menu only - Ctrl+K reassigned to step line)' but line 123-126 shows LIST_KEY loaded from JSON config with action 'step_line', not a reassignment

---

#### Code vs Documentation inconsistency

**Description:** keybindings.py shows STACK_DISPLAY as 'Menu only' but interactive_menu.py shows it with a keyboard shortcut in the menu

**Affected files:**
- `src/ui/keybindings.py`
- `src/ui/interactive_menu.py`

**Details:**
keybindings.py line 105-107: STACK_KEY = '', STACK_CHAR = '', STACK_DISPLAY = 'Menu only'. But interactive_menu.py line 67: (f'Execution Stack  {fmt_key(kb.STACK_DISPLAY)}', '_toggle_stack_window') will display 'Menu only' as if it were a key

---

#### Code vs Comment conflict

**Description:** Comment says 'Keymap window - accessible via menu only' but KEYBINDINGS_BY_CATEGORY doesn't list it anywhere

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py line 59: '# Keymap window - accessible via menu only (no dedicated key to avoid conflicts with typing)' but this feature is not documented in KEYBINDINGS_BY_CATEGORY dictionary (lines 237-283)

---

#### Code vs Documentation inconsistency

**Description:** CONTINUE_KEY loaded from 'goto_line' action but described as 'Continue execution (Go)' in comments and documentation

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py line 186: _continue_key = _get_key('editor', 'goto_line') or 'Ctrl+G' - loads from 'goto_line' action but line 185 comment says '# Continue execution (Go)' and line 274 shows '(CONTINUE_DISPLAY, "Continue execution (Go)")'. Action name doesn't match usage.

---

#### Code vs Documentation inconsistency

**Description:** help_widget.py footer shows 'U=Back' but keypress handler checks for both 'u' and 'U' (case insensitive)

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
help_widget.py line 68: footer shows 'U=Back' (uppercase) but line 330: elif key == 'u' or key == 'U': handles both cases. Documentation should clarify case insensitivity or use lowercase in display.

---

#### Code vs Documentation inconsistency

**Description:** interactive_menu.py imports keybindings as kb and uses kb.NEW_DISPLAY, kb.OPEN_DISPLAY etc., but these are defined in keybindings.py which loads from JSON - circular dependency risk

**Affected files:**
- `src/ui/interactive_menu.py`
- `src/ui/keybindings.py`

**Details:**
interactive_menu.py line 5: 'from . import keybindings as kb' and uses kb.NEW_DISPLAY (line 30), kb.OPEN_DISPLAY (line 31), etc. These values are loaded from JSON in keybindings.py, but if JSON is missing, fallback values are used. Menu display may not match actual keybindings.

---

#### Code vs Comment conflict

**Description:** Comment says 'Ctrl+L is context-sensitive' but LIST_KEY is defined as step_line action without context handling shown

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py line 209-211: '# Note: Ctrl+L is context-sensitive in curses UI: # - When debugging: Step Line (execute all statements on current line) # - When editing: List program (same as LIST_KEY)' but the keybinding definition doesn't show context-sensitive handling

---

#### code_vs_comment

**Description:** LineBox title parameter comment contradicts implementation

**Affected files:**
- `src/ui/keymap_widget.py`

**Details:**
Comment says 'Set title to None to suppress the title line space' but LineBox is created with title=None. The comment suggests this is intentional to suppress space, but the actual behavior of urwid.LineBox with title=None should be verified - it may still show a title line or may not suppress space as intended.

---

#### code_internal_inconsistency

**Description:** get_recent_files filter logic has bug in saving filtered results

**Affected files:**
- `src/ui/recent_files.py`

**Details:**
In get_recent_files(), the code filters out non-existent files and then tries to save the filtered list. However, the save logic is: 'self._save_recent_files([{'path': path, 'timestamp': item.get('timestamp', '')} for item, path in zip(recent, existing)])'. This zips 'recent' (unfiltered list) with 'existing' (filtered paths), which will create mismatched pairs if any files were filtered out. Should zip the filtered items, not the original 'recent' list.

---

#### code_vs_documentation

**Description:** Duplicate keybinding definitions for same actions

**Affected files:**
- `src/ui/tk_keybindings.json`

**Details:**
In tk_keybindings.json, 'new_program' and 'file_new' both map to Ctrl+N with same description 'New file'. Similarly, 'save_file' and 'file_save' both map to Ctrl+S. This duplication suggests inconsistent naming conventions or leftover aliases that should be consolidated.

---

#### code_vs_comment

**Description:** Comment says 'Make modal' but only grab_set() is called, not wait_window()

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Line comment: '# Make modal' followed by 'self.transient(parent)' and 'self.grab_set()'. However, to truly make a Tkinter dialog modal, you typically need to call 'self.wait_window()' or 'parent.wait_window(self)' after grab_set(). The current implementation makes it appear modal (grabs input) but doesn't block execution, so it's not truly modal in the traditional sense.

---

#### missing_implementation

**Description:** Help text tooltip implementation is incomplete

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
In _create_setting_widget(), short help text is displayed as a label with comment '# Show short help as tooltip-style label', but it's not actually a tooltip - it's just a gray label. True tooltips would appear on hover. The comment suggests tooltip functionality but the implementation is just a static label.

---

#### code_internal_inconsistency

**Description:** Inconsistent error handling between _on_apply and _on_ok methods

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
_on_apply() shows a success messagebox after applying settings, but _on_ok() silently closes the dialog on success. This inconsistency in user feedback could be confusing - users might not know if OK actually saved their changes or not.

---

#### code_vs_comment

**Description:** Comment describes variables_tree columns in wrong order compared to actual implementation

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _create_variables_window(), the comment says 'tree.heading('Value', text='  Value')' and 'tree.heading('Type', text='  Type')' suggesting Value is column #1 and Type is column #2. However, in _on_variable_heading_click(), the code comments say '# Value column (swapped to be first)' and '# Type column (swapped to be second)', and in _on_variable_double_click() the code accesses 'item_data['values'][0]' with comment '# Value column (swapped to first)' and 'item_data['values'][1]' with comment '# Type column (swapped to second)'. The 'swapped' comments suggest the columns were reordered at some point, but the actual column definitions don't show any swapping.

---

#### code_vs_comment

**Description:** Comment about immediate mode components contradicts actual implementation

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In start() method, after creating immediate_frame, there's a comment '# Immediate mode input (just the prompt and entry, no header or history)' and later '# Create dummy immediate_history and immediate_status for compatibility (some code still references these)'. However, the docstring at the top of the class describes 'Split pane: editor on left, output on right' without mentioning immediate mode at all, and the comment suggests these are dummy/compatibility attributes rather than functional components.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of statement offset in breakpoint status messages

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _toggle_breakpoint(), the code shows 'statement {stmt_offset + 1}' when stmt_offset > 0. In _menu_step_line() and _menu_step(), similar logic is used. However, the PC class uses 0-based stmt_offset internally, and the +1 conversion for display is applied inconsistently - sometimes checking 'if stmt_offset > 0' before showing, sometimes checking 'if pc and pc.stmt_offset > 0'. This could lead to confusion about whether statement 1 or statement 0 is the first statement.

---

#### code_vs_comment

**Description:** Comment says 'OPTION BASE 0: use all zeros' but code uses array_base variable which could be 0 or 1

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~150: Comment says '# OPTION BASE 0: use all zeros' but the code checks 'if array_base == 0:' which means it's dynamically checking the runtime value, not assuming it's always 0. The comment makes it sound like this branch is specifically for BASE 0, but the code is correctly handling whichever base is currently set.

---

#### code_vs_comment

**Description:** Comment says 'Enforce 4 dimension display limit' but code shows '...' for arrays with MORE than 4 dimensions

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~470: Comment says '# Enforce 4 dimension display limit' but the code 'dims = var['dimensions'][:4] if len(var['dimensions']) <= 4 else var['dimensions'][:4] + ['...']' shows that it displays first 4 dimensions plus '...' when there are MORE than 4. The comment should say 'Display up to 4 dimensions' or 'Truncate dimension display at 4'.

---

#### code_vs_comment

**Description:** Comment says 'This ensures the editor can NEVER contain blank lines' but the code explicitly keeps the last blank line

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~1060: Comment says 'Remove all blank lines from the editor. This ensures the editor can NEVER contain blank lines.' but the code at line ~1075 says '# But keep the last line (which is always empty in Tk Text widget)' and the filter keeps blank lines when 'i == len(lines) - 1'. So the editor CAN contain one blank line (the last one).

---

#### code_vs_comment

**Description:** Comment says 'prevent blank lines' but the action is to break/return, not to prevent the blank line from being created

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~1130: Comment says '# If line is completely blank, don't do anything (prevent blank lines)' but the code just returns 'break' which prevents the default Enter behavior. It doesn't actively remove or prevent blank lines - it just doesn't create a new one. The comment could be clearer about what 'prevent' means here.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of type_suffix parameter in _edit_array_element

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
The function receives 'type_suffix' parameter from the Type column display (line ~570), but then extracts suffix again from variable_name (line ~150: 'suffix = variable_name[-1] if variable_name[-1] in '$%!#' else None'). This could lead to inconsistency if the Type column display doesn't match the variable name suffix.

---

#### code_vs_comment

**Description:** Comment says 'Tk UI doesn't have a persistent runtime' but code shows runtime is persistent

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In cmd_renum method, comment says 'runtime=None  # Tk UI doesn't have a persistent runtime' but throughout the file, self.runtime is used persistently (e.g., in cmd_run, _execute_tick, cmd_cont, _execute_immediate). The runtime is created and maintained as an instance variable.

---

#### code_vs_comment

**Description:** Comment says 'DON'T sort if just clicking around without editing' but logic doesn't distinguish clicking from editing

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _check_line_change method, comment says 'DON'T sort if just clicking around without editing (old is None means we're just tracking)' but the code sets should_sort based on line number changes, not on whether actual editing occurred. The old_line_num being None just means first time tracking, not that no editing happened.

---

#### code_vs_comment

**Description:** Comment about RUN = CLEAR + GOTO contradicts actual behavior

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In cmd_run method, comment says 'Reset runtime with current program - RUN = CLEAR + GOTO first line' and 'This preserves breakpoints but clears variables' but CLEAR in BASIC typically clears the program entirely, not just variables. The comment should say 'RUN clears variables and starts execution' without the CLEAR comparison.

---

#### code_vs_comment

**Description:** Comment says 'Don't call interpreter.start()' but doesn't explain why halted flag clearing is sufficient

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_immediate method, comment says 'NOTE: Don't call interpreter.start() because it resets PC! RUN 120 already set PC to line 120, so just clear halted flag' but this assumes the interpreter is already initialized. If this is the first RUN after program load, the statement table may not be built.

---

#### code_vs_comment

**Description:** Comment about 'using microprocessor model' is vague and not explained

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_tick method, comment says 'Handle state using microprocessor model' and in _update_immediate_status comment says 'Update prompt label color based on current state using microprocessor model' but there's no explanation of what this 'microprocessor model' is or how it differs from other approaches.

---

#### code_vs_comment

**Description:** input() method docstring says it's for INPUT statement with comma-separated values, but implementation doesn't handle comma-separated parsing

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring: 'Input from user via inline input field. Used by INPUT statement for reading comma-separated values.' However, the code just returns the raw string from input_queue.get() without any comma-separated value parsing. The parsing would need to happen at a higher level.

---

#### code_inconsistency

**Description:** Inconsistent INPUT handling between input() and input_line() methods

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
input() method uses backend._show_input_row() for inline input with fallback to dialog, while input_line() always uses simpledialog.askstring(). This creates inconsistent user experience where INPUT uses inline field but LINE INPUT uses modal dialog.

---

#### code_vs_comment

**Description:** Docstring claims line numbers should be part of text content (not drawn separately), but code still parses line numbers from text and uses them for status display

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Class docstring states: 'Note: Line numbers should be part of the text content (not drawn separately). This requires Phase 2 refactoring to integrate line numbers into text.' However, the _redraw() method comment says 'Note: Line numbers are no longer drawn in canvas - they should be part of the text content itself (Phase 2 of editor refactoring).' The code actually does parse line numbers from text content via _parse_line_number() and uses them to map status symbols. The implementation already treats line numbers as part of text content, making the 'Phase 2' note misleading.

---

#### code_vs_comment

**Description:** Blank line removal feature is implemented but not documented in class docstring

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
The class implements automatic blank line removal when cursor moves away from a blank line (via _on_cursor_move, _delete_line methods and related bindings), but this behavior is not mentioned in the class docstring. The docstring only describes status symbols and layout, not this editing behavior.

---

#### code_vs_comment

**Description:** update_line_references() docstring claims to handle 'ON <expr> GOTO/GOSUB' but the regex pattern implementation is incomplete

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring says: 'Also handles: ON <expr> GOTO/GOSUB'. The regex pattern is: r'\b(GOTO|GOSUB|THEN|ELSE|ON\s+[^G]+\s+GOTO|ON\s+[^G]+\s+GOSUB)\s+(\d+)'. However, this pattern will NOT match 'ON X GOTO 10,20' correctly because it only captures the first line number after the keyword. The comma-separated handling comes from a separate regex that runs afterward, but the docstring doesn't explain this two-pass approach. The comment 'Handle comma-separated line lists (ON...GOTO/GOSUB)' appears later, suggesting the first pattern alone is insufficient.

---

#### code_vs_comment

**Description:** serialize_statement() for RemarkStatementNode has comment about 'REMARK is converted to REM' but code doesn't show this conversion

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment: '# Preserve comments using original syntax (REM or ') # Note: REMARK is converted to REM for consistency'. However, the code checks 'stmt.comment_type' and returns either "' {text}" or 'REM {text}'. There's no handling of 'REMARK' as a distinct case. Either the conversion happens elsewhere (in parser/lexer) and the comment is misleading about where it happens, or the comment is outdated.

---

#### code_vs_documentation

**Description:** delete_lines_from_program() docstring says it updates runtime.line_table but code updates runtime.statement_table

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring: 'runtime: Optional runtime object with line_table and line_order to update'. Code: 'if hasattr(runtime, 'statement_table'): runtime.statement_table.delete_line(line_num)'. The docstring mentions 'line_table' and 'line_order' but the implementation only uses 'statement_table'. Either the docstring is outdated or the implementation is incomplete.

---

#### code_vs_comment

**Description:** serialize_expression() for FunctionCallNode has special case for ERR/ERL but comment doesn't explain why

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Code: '# ERR and ERL are special - they're not functions and don't use () if expr.name in ('ERR', 'ERL') and len(expr.arguments) == 0: return expr.name'. This is a significant special case that affects serialization behavior, but there's no explanation of why ERR and ERL are treated differently. Are they keywords? Variables? The comment should explain the BASIC language semantics that require this special handling.

---

#### code_vs_comment

**Description:** Unused variable in cmd_run method contradicts docstring

**Affected files:**
- `src/ui/visual.py`

**Details:**
In VisualBackend.cmd_run(), the docstring says '1. Get program AST from ProgramManager' and the code executes 'program_ast = self.program.get_program_ast()', but this variable is never used. The actual execution uses 'self.runtime = Runtime(self.program.line_asts, self.program.lines)' which accesses line_asts directly, not through the program_ast variable.

---

#### code_vs_documentation

**Description:** Inconsistent breakpoint API between CodeMirror5Editor and CodeMirrorEditor

**Affected files:**
- `src/ui/web/codemirror5_editor.py`
- `src/ui/web/codemirror_editor.py`

**Details:**
CodeMirror5Editor.add_breakpoint() accepts optional char_start and char_end parameters for statement-level breakpoints: 'add_breakpoint(self, line_num: int, char_start: Optional[int] = None, char_end: Optional[int] = None)', while CodeMirrorEditor.add_breakpoint() only accepts line_num: 'add_breakpoint(self, line_num: int)'. This creates an inconsistent API between the two editor implementations for the same feature.

---

#### code_vs_documentation

**Description:** Inconsistent set_current_statement API between CodeMirror5Editor and CodeMirrorEditor

**Affected files:**
- `src/ui/web/codemirror5_editor.py`
- `src/ui/web/codemirror_editor.py`

**Details:**
CodeMirror5Editor.set_current_statement() accepts optional char_start and char_end parameters: 'set_current_statement(self, line_num: Optional[int], char_start: Optional[int] = None, char_end: Optional[int] = None)', while CodeMirrorEditor.set_current_statement() only accepts line_num: 'set_current_statement(self, line_num: Optional[int])'. This creates an inconsistent API for statement-level highlighting between the two editor implementations.

---

#### code_vs_comment

**Description:** Docstring says 'Based on TK UI feature set' but references non-existent documentation file

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~933: Docstring states 'Based on TK UI feature set (see docs/dev/TK_UI_FEATURE_AUDIT.md).' but this documentation file is not provided in the source files, making it impossible to verify if the implementation matches the documented TK UI features.

---

#### code_vs_comment

**Description:** Comment says 'self.running' is for display only but code logic depends on it

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Multiple comments state 'self.running = False  # For display only (spinner)' and 'Mark as running (for display only - spinner, status indicator). This should NOT control program logic - RUN is always valid'. However, _menu_continue checks 'if self.running and self.paused' to determine if continue is valid, and _menu_step_line/_menu_step_stmt check 'if not self.running and not self.paused' to determine behavior. This means self.running DOES control program logic, contradicting the comments.

---

#### code_vs_comment

**Description:** Comment in _execute_tick says not to check self.running but then explains why it doesn't persist

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~1120: 'Don't check self.running - it seems to not persist correctly in NiceGUI callbacks. Just check if we have an interpreter'. This suggests self.running is unreliable in callbacks, but other methods like _menu_continue and step methods rely on self.running being accurate.

---

#### code_vs_comment

**Description:** Comment says _sync_program_to_runtime preserves PC but then conditionally resets it

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Docstring says 'Sync program to runtime without resetting PC. Updates runtime's statement_table and line_text_map from self.program, but preserves current PC/execution state.' However, the code has logic: 'if self.exec_timer and self.exec_timer.active: self.runtime.pc = old_pc else: self.runtime.pc = PC.halted_pc()'. So it only preserves PC if timer is active, otherwise it resets to halted.

---

#### code_internal_inconsistency

**Description:** Inconsistent error output formatting

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Error messages are formatted inconsistently: sometimes '--- Error: {e} ---', sometimes '--- Setup error: {error_msg} ---', sometimes '--- Tick error: {e} ---', and sometimes '--- Program stopped ---'. The dashes and capitalization vary.

---

#### code_vs_comment

**Description:** Comment says _get_input returns empty string and interpreter handles it, but the method shows input UI and returns empty string without clear interpreter state transition handling

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment in _get_input() says: 'Return empty string - the interpreter will handle this by transitioning to waiting_for_input state, and execution will pause until the user provides input via _submit_input()'. However, the code just returns empty string without any explicit state transition code visible. The _submit_input() method does call interpreter.provide_input(value) but there's no clear connection showing how the empty string triggers the state transition.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate says not to sync editor from AST, but provides unclear TODO about future architecture

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment says: 'Don't sync editor from AST - editor text is the source! TODO: Future architecture: parse lines immediately into AST, text only kept for syntax errors'. This suggests current behavior but the TODO implies a different future design. The relationship between editor text, AST, and program state is unclear from the comments.

---

#### code_internal_inconsistency

**Description:** Inconsistent handling of editor placeholder between different event handlers

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
_on_editor_change() clears placeholder by setting editor_has_been_used flag but doesn't call props(). _on_paste() both sets the flag AND calls self.editor.props('placeholder=""'). _on_key_released() sets flag and calls props(). This inconsistent approach suggests refactoring left some handlers partially updated.

---

#### code_vs_comment

**Description:** Comment about ImmediateExecutor constructor parameters doesn't match actual usage

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment says: 'Create immediate executor (runtime, interpreter, io_handler)' but the actual code is: 'immediate_executor = ImmediateExecutor(runtime, interpreter, output_io)'. The parameter name 'output_io' vs 'io_handler' is inconsistent with the comment.

---

#### code_vs_documentation

**Description:** Settings dialog keyboard shortcuts not documented

**Affected files:**
- `src/ui/web/web_settings_dialog.py`
- `docs/help/common/debugging.md`

**Details:**
web_settings_dialog.py implements a settings dialog with Save/Cancel buttons but debugging.md documents keyboard shortcuts for other UIs (Tk: Ctrl+B for breakpoints, Curses: 'b' for breakpoints) without mentioning Web UI settings access. The debugging.md mentions 'Use the "Breakpoint" button in the toolbar' for Web UI but doesn't document how to access settings.

---

#### documentation_inconsistency

**Description:** Incomplete cross-referencing between debugging and editor commands

**Affected files:**
- `docs/help/common/debugging.md`
- `docs/help/common/editor-commands.md`

**Details:**
debugging.md says 'For debugging-specific commands like breakpoints and stepping, see [Debugging Features](debugging.md)' in editor-commands.md, but editor-commands.md only has a brief 'Debugging Commands' section that refers back to debugging.md. The keyboard shortcuts table in editor-commands.md doesn't include debugging shortcuts like Ctrl+T (Step), Ctrl+G (Continue), Ctrl+Q (Stop) which are documented in debugging.md.

---

#### code_vs_documentation

**Description:** Help system architecture mismatch

**Affected files:**
- `src/ui/web_help_launcher.py`
- `docs/help/README.md`

**Details:**
README.md describes help structure with /common, /ui/cli, /ui/curses, /ui/tk, /ui/visual, /ui/web directories and says 'UIs should: 1. Load common help content for all users 2. Add UI-specific help sections'. However, web_help_launcher.py open_help_in_browser() function constructs URLs like 'http://localhost/mbasic_docs/ui/{ui_type}/' suggesting the help is pre-built and served statically, not dynamically loaded by UIs.

---

#### documentation_inconsistency

**Description:** ASCII codes documentation references non-existent Appendix M

**Affected files:**
- `docs/help/common/language/appendices/ascii-codes.md`
- `docs/help/common/language/functions/asc.md`

**Details:**
In asc.md: 'Returns a numerical value that is the ASCII code of the first character of the string X$. (See Appendix M for ASCII codes.)' However, the actual ASCII codes are documented in 'docs/help/common/language/appendices/ascii-codes.md', not 'Appendix M'. The reference should point to the correct location.

---

#### documentation_inconsistency

**Description:** Error code reference links to non-existent page

**Affected files:**
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
In error-codes.md, the 'See Also' section links to '[ERR and ERL Variables](../statements/err-erl-variables.md)' but the actual filename should match the link target. Need to verify if this file exists or if the link is incorrect.

---

#### documentation_inconsistency

**Description:** Function count mismatch in index

**Affected files:**
- `docs/help/common/language/index.md`
- `docs/help/common/language/functions/index.md`

**Details:**
The index.md states '40 intrinsic functions' but doesn't provide a complete list to verify this count. The actual number of functions should be verified against the functions directory.

---

#### documentation_inconsistency

**Description:** Statement count mismatch in index

**Affected files:**
- `docs/help/common/language/index.md`
- `docs/help/common/language/statements/index.md`

**Details:**
The index.md states '63 commands and statements' but doesn't provide a complete list to verify this count. The actual number of statements should be verified against the statements directory.

---

#### documentation_inconsistency

**Description:** Incomplete example reference in CLOSE statement

**Affected files:**
- `docs/help/common/language/statements/close.md`

**Details:**
The example section states 'See PART II, Chapter 3, MBASIC Disk I/O, of the MBASIC User's Guide.' but doesn't provide an actual code example, which is inconsistent with other statements that provide inline examples.

---

#### documentation_inconsistency

**Description:** Extension documentation vs original MBASIC behavior

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`

**Details:**
The DEF FN documentation extensively describes multi-character function names as an extension, but doesn't clearly indicate whether this is implemented in this Python interpreter or just documented for reference. The 'Syntax Notes' section describes it as 'This implementation (extension)' but it's unclear if this refers to the Python implementation or the original MBASIC 5.21.

---

#### documentation_inconsistency

**Description:** Inconsistent punctuation in DIM remarks

**Affected files:**
- `docs/help/common/language/statements/dim.md`

**Details:**
The remarks section has 'If a subscript is used that is greater than the maximum specified, ,a "Subscript out of range" error occurs.' with a double comma (,a) which is a typo.

---

#### documentation_inconsistency

**Description:** Conflicting documentation paths for ERR and ERL

**Affected files:**
- `docs/help/common/language/statements/error.md`
- `docs/help/common/language/statements/err-erl-variables.md`

**Details:**
error.md references 'ERR' and 'ERL' with path '../functions/err-erl.md', but the actual documentation file is 'err-erl-variables.md' in the statements directory with type: statement. The cross-reference paths are incorrect.

---

#### documentation_inconsistency

**Description:** Missing LIMITS command in alphabetical listing

**Affected files:**
- `docs/help/common/language/statements/index.md`

**Details:**
index.md includes LIMITS in the 'Modern Extensions' category and has a dedicated limits.md file, but LIMITS does not appear in the alphabetical listing under 'L' section. The alphabetical listing shows LLIST, LOAD, LPRINT but skips LIMITS.

---

#### documentation_inconsistency

**Description:** Conflicting documentation for LINE INPUT vs LINE INPUT#

**Affected files:**
- `docs/help/common/language/statements/line-input.md`
- `docs/help/common/language/statements/inputi.md`

**Details:**
line-input.md documents 'LINE INPUT' for keyboard input with syntax 'LINE INPUT [;"prompt string";]<string variable>', while inputi.md documents 'LINE INPUT#' for file input with syntax 'LINE INPUT#<file number>,<string variable>'. However, line-input.md's See Also references 'LINE INPUT#' as 'input_hash.md' which is actually the INPUT# documentation file, not LINE INPUT#.

---

#### documentation_inconsistency

**Description:** RENUM documentation has duplicate line numbers in example

**Affected files:**
- `docs/help/common/language/statements/renum.md`

**Details:**
Example 6 shows: '1000 PRINT "OPTION 1"
1100 END
1100 PRINT "OPTION 2"
1200 END
1200 PRINT "OPTION 3"' with duplicate line numbers 1100 and 1200. This appears to be a typo - should likely be 1000, 1100, 1200, 1300 or similar sequential numbering.

---

#### documentation_inconsistency

**Description:** SHOWSETTINGS documentation shows different command names in different files

**Affected files:**
- `docs/help/common/language/statements/showsettings.md`
- `docs/help/common/settings.md`

**Details:**
showsettings.md shows 'HELPSETTING' as a related command, but settings.md shows 'SETSETTING' as the command to change settings. The 'HELPSETTING' command is not documented anywhere else in the provided files.

---

#### documentation_inconsistency

**Description:** WIDTH implementation note contradicts syntax documentation

**Affected files:**
- `docs/help/common/language/statements/width.md`

**Details:**
The implementation note says 'The "WIDTH LPRINT" syntax is not supported (parse error)' but the Syntax section still shows 'WIDTH [LPRINT] <integer expression>' as if LPRINT is optional and supported. The syntax section should clearly indicate LPRINT is not supported.

---

#### documentation_inconsistency

**Description:** Keyboard shortcuts documentation incomplete and inconsistent

**Affected files:**
- `docs/help/common/ui/curses/editing.md`
- `docs/help/common/shortcuts.md`

**Details:**
shortcuts.md shows '^R' for Run, '^P' for Help, '^Q' for Quit, but curses/editing.md mentions 'Ctrl+R', 'Ctrl+N', 'Ctrl+S', 'Ctrl+L', 'Ctrl+P' without documenting what '^N', '^S', '^L' do in shortcuts.md. Also, shortcuts.md uses caret notation (^R) while editing.md uses Ctrl+ notation.

---

#### documentation_inconsistency

**Description:** Broken documentation links

**Affected files:**
- `docs/help/index.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
index.md references '[Getting Started](mbasic/getting-started.md)' but the actual path based on the file structure should be 'common/getting-started.md' or the file is missing. Also references '[About MBASIC](mbasic/index.md)' which may not exist.

---

#### documentation_inconsistency

**Description:** Keyboard shortcut conflicts between UIs

**Affected files:**
- `docs/help/common/ui/tk/index.md`
- `docs/help/common/shortcuts.md`

**Details:**
tk/index.md shows 'Ctrl+C' for Copy, but shortcuts.md (which appears to be for curses UI) shows '^C' for Cancel/Close dialogs. This creates ambiguity about what Ctrl+C does in different contexts.

---

#### documentation_inconsistency

**Description:** Settings storage location inconsistency

**Affected files:**
- `docs/help/common/settings.md`

**Details:**
settings.md states settings are stored in '~/.mbasic/settings.json' (Linux/Mac) and '%APPDATA%\mbasic\settings.json' (Windows), but uses forward slashes in the Windows path description which should be backslashes for consistency.

---

#### documentation_inconsistency

**Description:** Inconsistent project naming

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/extensions.md`

**Details:**
architecture.md consistently refers to 'MBASIC' throughout. extensions.md introduces 'MBASIC-2025' and lists alternative names under consideration: 'Visual MBASIC 5.21', 'MBASIC++', 'MBASIC-X'. The documentation doesn't clarify which is the official name or if these are just proposals.

---

#### documentation_inconsistency

**Description:** Conflicting information about debugging command availability

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/extensions.md`

**Details:**
features.md lists 'Debugging' features including 'Breakpoints', 'Step execution', 'Variable watch', 'Stack viewer' with '(UI-dependent)' notes. extensions.md provides detailed BREAK/STEP/STACK command syntax and states 'Availability: CLI (command form), Curses (Ctrl+B), Tk (UI controls)'. However, features.md doesn't mention these are extensions or provide the specific command syntax that extensions.md documents.

---

#### documentation_inconsistency

**Description:** Web UI features listed differently

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/extensions.md`

**Details:**
features.md lists 'Web UI' with features like 'Browser-based IDE', 'Syntax highlighting', 'Auto-save', 'Three-panel layout', 'In-memory filesystem', 'Basic debugging'. extensions.md mentions Web UI but doesn't provide the same level of detail about its specific features, only mentioning it as one of the GUI interfaces that are extensions.

---

#### documentation_inconsistency

**Description:** Missing Web UI in getting-started guide

**Affected files:**
- `docs/help/mbasic/getting-started.md`
- `docs/help/mbasic/extensions.md`

**Details:**
getting-started.md lists three interfaces: 'Curses UI (Default)', 'CLI Mode', and 'Tkinter GUI'. It doesn't mention the Web UI that is documented in both features.md and extensions.md. The 'Choosing a User Interface' section is incomplete.

---

#### documentation_inconsistency

**Description:** Inconsistent description of line ending support

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/compatibility.md`

**Details:**
architecture.md doesn't mention line ending support in its 'Interpreter Mode' section. compatibility.md has detailed 'Line ending support' section stating 'More permissive than MBASIC 5.21' and lists CR, LF, CRLF support. This is a significant compatibility feature that should be mentioned in the architecture overview.

---

#### documentation_inconsistency

**Description:** Conflicting information about POKE behavior

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/compatibility.md`

**Details:**
features.md lists 'PEEK, POKE - Memory access (emulated)' under System functions. compatibility.md provides detailed explanation: 'POKE: Parsed and executes successfully, but performs no operation (no-op)'. features.md implies POKE is functional (emulated), while compatibility.md clarifies it's a no-op.

---

#### documentation_inconsistency

**Description:** Incomplete semantic analyzer usage documentation

**Affected files:**
- `docs/help/mbasic/architecture.md`

**Details:**
architecture.md shows commands 'python3 analyze_program.py myprogram.bas' but doesn't specify the full path or whether this tool is included in the distribution. The 'Using the Analyzer' section references a tool that may not exist or may be in a different location.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut documentation for Delete Lines

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/editing.md`

**Details:**
feature-reference.md states 'Delete Lines (Ctrl+D)' as a file operation, but editing.md describes deleting lines by 'Delete all text after the line number' or 'type just the line number' with no mention of Ctrl+D. The methods described are incompatible - one is a keyboard shortcut, the other is a manual editing process.

---

#### documentation_inconsistency

**Description:** Conflicting information about clipboard operations

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
feature-reference.md states 'Cut/Copy/Paste (Not implemented)' and explains 'Standard clipboard operations are not available in the Curses UI' but then says 'Use your terminal's native copy/paste functions instead (typically Shift+Ctrl+C/V or mouse selection)'. This is contradictory - either clipboard operations work (via terminal) or they don't.

---

#### documentation_inconsistency

**Description:** Inconsistent statement count

**Affected files:**
- `docs/help/ui/cli/index.md`
- `docs/help/mbasic/index.md`

**Details:**
cli/index.md states 'Statements - All 63 statements' while mbasic/index.md doesn't specify a count. This could become inconsistent if the actual number differs.

---

#### documentation_inconsistency

**Description:** Execution Stack access method unclear

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
feature-reference.md lists 'Execution Stack (Menu only)' under Variable Inspection features and in the quick reference table, but doesn't specify which menu or how to access it. The description says 'Access through the menu bar' but no specific menu name or path is given.

---

#### documentation_inconsistency

**Description:** List Program access method unclear

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
feature-reference.md lists 'List Program (Menu only)' under Execution & Control but doesn't specify which menu or how to access it. Only says 'Access through the menu bar' with no specific path.

---

#### documentation_inconsistency

**Description:** Variable editing capability unclear

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
feature-reference.md states 'Edit Variable Value (Limited - Not fully implemented)' with a warning that 'You cannot directly edit values in the variables window' but then says to 'Use immediate mode commands to modify variable values instead'. This makes it unclear if the feature exists at all or if it's just not available in the variables window specifically.

---

#### documentation_inconsistency

**Description:** Settings documentation cross-reference incomplete

**Affected files:**
- `docs/help/ui/cli/settings.md`
- `docs/help/common/settings.md`

**Details:**
cli/settings.md references 'For a complete list of available settings, see [Settings System Overview](../../common/settings.md)' but the common/settings.md file is not provided in the documentation set, making it impossible to verify if the settings listed in cli/settings.md are complete or accurate.

---

#### documentation_inconsistency

**Description:** Tk settings.md describes Debug Mode checkbox in Interpreter tab, but web/debugging.md describes debug features without mentioning this setting

**Affected files:**
- `docs/help/ui/tk/settings.md`
- `docs/help/ui/web/debugging.md`

**Details:**
Tk settings.md: 'Debug Mode | Checkbox | - | Enable debug output' in Interpreter Tab. Web debugging.md describes extensive debug features (breakpoints, stepping, variable inspection) but never mentions a Debug Mode setting that needs to be enabled. Either the setting doesn't exist in Web UI or the debugging.md is incomplete.

---

#### documentation_inconsistency

**Description:** Breakpoint implementation status contradicts between documents

**Affected files:**
- `docs/help/ui/web/debugging.md`
- `docs/help/ui/web/getting-started.md`

**Details:**
debugging.md states under 'Setting Breakpoints': 'Currently Implemented: 1. Use Run → Toggle Breakpoint menu option' and later 'Note: Advanced features like clicking line numbers to set breakpoints... are planned for future releases but not yet implemented.' However, getting-started.md under 'Debugging Features' says 'Set breakpoints to pause execution at specific lines: 1. Use Run → Toggle Breakpoint menu option' without mentioning the limitation about clicking line numbers. The getting-started.md implies full breakpoint support without caveats.

---

#### documentation_inconsistency

**Description:** Auto-save functionality described differently

**Affected files:**
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/settings.md`

**Details:**
getting-started.md states: 'Note: The Web UI uses browser localStorage for auto-save functionality and downloads for explicit saves to your computer.' and 'Auto-save enabled: Your work is automatically saved to browser localStorage every 30 seconds'. However, settings.md under 'Settings Storage' only mentions 'Settings persist across page reloads' and 'Settings are per-browser, per-domain' without mentioning program auto-save. It's unclear if auto-save applies to programs, settings, or both.

---

#### documentation_inconsistency

**Description:** Variable inspector editing capability described inconsistently

**Affected files:**
- `docs/help/ui/web/debugging.md`
- `docs/help/ui/web/features.md`

**Details:**
debugging.md under 'Variable Inspector' describes 'Interactive Editing: 1. Double-click any variable value, 2. Edit dialog appears, 3. Enter new value, 4. Press Enter to apply, 5. Press Esc to cancel'. features.md under 'Variable Inspector' also lists 'Editing: Double-click edit, Type validation, Immediate update'. However, both documents mark many advanced debugging features as 'Planned Features' or 'Future', making it unclear if variable editing is actually implemented or planned.

---

#### documentation_inconsistency

**Description:** Debug console feature status unclear

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/debugging.md`

**Details:**
features.md under 'Advanced Debugging (Planned Features)' lists 'Debug Console (Future): Will provide interactive debugging console: Direct BASIC statement execution, Variable inspection and modification, Debug command support'. debugging.md also lists this under 'Advanced Debugging (Planned Features)'. However, getting-started.md describes a 'Command Area' at the bottom that allows 'immediate commands that don't get added to your program' with examples like 'PRINT 2+2'. This sounds like it could be the debug console, but it's never called that, creating confusion about whether this feature exists or not.

---

#### documentation_inconsistency

**Description:** Execution control buttons described with different capabilities

**Affected files:**
- `docs/help/ui/web/debugging.md`
- `docs/help/ui/web/features.md`

**Details:**
debugging.md under 'Debug Controls' lists: 'Continue (F5), Step Over (F10), Step Into (F11), Step Out (Shift+F11), Stop (Shift+F5)'. features.md under 'Execution Control' lists: 'Step Controls: Step over (F10), Step into (F11), Step out (Shift+F11), Run to cursor' and 'Flow Control: Continue (F5), Pause, Stop (Shift+F5), Restart'. The 'Run to cursor', 'Pause', and 'Restart' options are only in features.md, not debugging.md, suggesting inconsistent documentation or unimplemented features.

---

#### documentation_inconsistency

**Description:** External integration features listed but unlikely to be implemented

**Affected files:**
- `docs/help/ui/web/features.md`

**Details:**
features.md under 'Integration' lists: 'External Tools: Export to GitHub, Import from URL, WebDAV support, Cloud storage'. These features would require backend services and authentication, which contradicts the 'Local storage only, No server uploads' security model described in the same document under 'Security Features'. This is a direct contradiction within the same file.

---

#### documentation_inconsistency

**Description:** Inconsistent instructions for loading files in Web UI vs other UIs

**Affected files:**
- `docs/help/ui/web/web-interface.md`
- `docs/library/business/index.md`
- `docs/library/data_management/index.md`
- `docs/library/demos/index.md`
- `docs/library/education/index.md`
- `docs/library/electronics/index.md`
- `docs/library/games/index.md`
- `docs/library/ham_radio/index.md`
- `docs/library/telecommunications/index.md`
- `docs/library/utilities/index.md`

**Details:**
web-interface.md states 'Open - Load a .bas file from your computer (via browser file picker)' and 'Web/Tkinter UI: Click File → Open, select the downloaded file'. However, all library index.md files say 'Web/Tkinter UI: Click File → Open, select the downloaded file' without mentioning the browser file picker limitation. The web-interface.md also states under Limitations: 'Cannot directly access local filesystem (but can load files via browser file picker)' which suggests a different mechanism than other UIs.

---

#### documentation_inconsistency

**Description:** Case handling guide references features not mentioned in web interface documentation

**Affected files:**
- `docs/user/CASE_HANDLING_GUIDE.md`

**Details:**
CASE_HANDLING_GUIDE.md extensively documents SET, SHOW SETTINGS, and HELP SET commands, as well as configuration files (~/.mbasic/settings.json and .mbasic/settings.json). However, web-interface.md makes no mention of these commands or configuration capabilities, despite being a comprehensive guide to the web interface. This suggests either the web UI doesn't support these features, or the web-interface.md is incomplete.

---

#### documentation_inconsistency

**Description:** Contradictory information about project dependencies

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`
- `docs/user/INSTALL.md`

**Details:**
CHOOSING_YOUR_UI.md states 'Requires urwid' for Curses UI and 'Optional: for auto-open browser' for Web UI. INSTALL.md states 'Since this project has no external dependencies' and 'Note: Since this project has no external dependencies, this step mainly verifies your Python environment is working correctly.' These statements conflict.

---

#### documentation_inconsistency

**Description:** Conflicting information about Web UI requirements

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`
- `docs/user/INSTALL.md`

**Details:**
CHOOSING_YOUR_UI.md lists 'nicegui' as optional for Web UI in the requirements comparison, but INSTALL.md makes no mention of nicegui at all. CHOOSING_YOUR_UI.md Installation Requirements section only mentions webbrowser for Web UI.

---

#### documentation_inconsistency

**Description:** Conflicting information about documentation location

**Affected files:**
- `docs/user/INSTALL.md`
- `docs/user/README.md`

**Details:**
README.md states 'This directory contains documentation intended for end users' and lists specific types. However, INSTALL.md references 'PROJECT_STATUS.md' which is not in the user docs directory and appears to be a project-level document.

---

#### documentation_inconsistency

**Description:** Keyboard shortcut inconsistency for Find/Replace between Tk and Curses documentation

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md states 'Ctrl+H' is 'Find and replace' for Tk UI. However, keyboard-shortcuts.md (for Curses UI) states '^F' is 'This help' and 'Ctrl+H' is also listed as 'Help' under 'Global Commands'. The Tk guide shows Ctrl+H for Find/Replace while Curses uses it for Help, but this distinction is not clearly called out in the comparison guide.

---

#### documentation_inconsistency

**Description:** Variables window keyboard shortcut inconsistency between UIs

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md lists 'Ctrl+V' as 'Show/hide Variables window' for Tk UI. keyboard-shortcuts.md (Curses UI) lists 'Ctrl+V' as 'Save program' and 'Ctrl+W' as 'Toggle variables watch window'. This is a legitimate UI difference but could cause confusion when switching between UIs.

---

#### documentation_inconsistency

**Description:** Execution Stack window keyboard shortcut missing in comparison

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
TK_UI_QUICK_START.md lists 'Ctrl+K' as 'Show/hide Execution Stack window' for Tk UI. UI_FEATURE_COMPARISON.md's keyboard shortcuts comparison table shows 'Variables' shortcuts but does not include the Execution Stack window shortcut comparison across UIs. keyboard-shortcuts.md shows 'Menu only' for toggling execution stack in Curses, suggesting different access methods.

---

#### documentation_inconsistency

**Description:** Variables window shortcut inconsistency in comparison table

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
TK_UI_QUICK_START.md shows 'Ctrl+V' for 'Show/hide Variables window' and 'Ctrl+W' for 'Show/hide Variables & Resources window'. UI_FEATURE_COMPARISON.md's debugging shortcuts table shows 'Variables' action with 'Ctrl+W' for Curses, 'Ctrl+V' for Tk, and 'Ctrl+Alt+V' for Web. The Tk guide mentions both Ctrl+V and Ctrl+W but the comparison only shows Ctrl+V.

---

### 🟢 Low Severity

#### code_internal_inconsistency

**Description:** Duplicate column attribute in DefFnStatementNode

**Affected files:**
- `src/ast_nodes.py`

**Details:**
DefFnStatementNode has 'column: int = 0' defined twice at the end of the class definition (lines appear around line 1050). This is redundant but not harmful in Python dataclasses.

---

#### documentation_inconsistency

**Description:** Version number inconsistency in setup.py comments vs actual version

**Affected files:**
- `setup.py`

**Details:**
setup.py line 13 has comment '# Reflects ~99% implementation status (core complete)' next to version='0.99.0', but this is more of an explanation than an inconsistency. However, the comment suggests the version number is tied to implementation percentage, which may not be standard semantic versioning practice.

---

#### code_comment_conflict

**Description:** LineNode docstring mentions source_text but class doesn't have that field

**Affected files:**
- `src/ast_nodes.py`

**Details:**
LineNode docstring states 'Never store source_text - it creates a duplicate copy that gets out of sync.' This suggests source_text was previously a field but has been removed. The comment is now a warning rather than describing current implementation, which is good, but could be clearer that this is a design decision note.

---

#### code_internal_inconsistency

**Description:** Inconsistent use of Optional type hints

**Affected files:**
- `src/ast_nodes.py`

**Details:**
Some nodes use 'Optional[type]' consistently (e.g., InputStatementNode.prompt), while others use 'type = None' without Optional wrapper (e.g., ShowSettingsStatementNode.filter: Optional[Any] = None vs SetSettingStatementNode.key: Any). This is inconsistent typing style, though functionally equivalent in Python.

---

#### documentation_inconsistency

**Description:** CallStatementNode has conflicting documentation about standard vs extended syntax

**Affected files:**
- `src/ast_nodes.py`

**Details:**
CallStatementNode docstring says 'Standard MBASIC 5.21 Syntax: CALL address' but then mentions 'Parser also accepts extended syntax for compatibility with other BASIC dialects (e.g., CALL ROUTINE(args)), but this is not standard MBASIC 5.21.' The 'arguments' field suggests extended syntax is implemented, but it's unclear if this should be supported or is a compatibility compromise.

---

#### code_internal_inconsistency

**Description:** Inconsistent field naming for token references

**Affected files:**
- `src/ast_nodes.py`

**Details:**
Some statement nodes have 'keyword_token' field (e.g., PrintStatementNode, IfStatementNode, ForStatementNode) while DimStatementNode just has 'token'. This inconsistency in naming convention makes the codebase less uniform.

---

#### code_vs_comment

**Description:** Docstring describes INPUT$ but method is named INPUT

**Affected files:**
- `src/basic_builtins.py`

**Details:**
The INPUT method docstring says 'INPUT$ - Read num characters from keyboard or file' but the method is named INPUT (without $). In BASIC, INPUT$ is the function name, but Python method names can't include $.

---

#### code_vs_comment

**Description:** Inconsistent file handle access in INPUT method

**Affected files:**
- `src/basic_builtins.py`

**Details:**
In INPUT method around line 820, it accesses 'file_handle = self.runtime.files[file_num]' and then calls 'file_handle.read(num)', but earlier in the file (EOF, LOC, LOF methods), files are accessed as dictionaries with 'handle' key: 'file_handle = file_info['handle']'. This suggests INPUT method has a bug.

---

#### documentation

**Description:** Incomplete docstring for MID function

**Affected files:**
- `src/basic_builtins.py`

**Details:**
MID docstring shows 'MID$(string, start)' and 'MID$(string, start, length)' but doesn't mention that start is 1-based, though the comment 'Start is 1-based' appears after the docstring examples.

---

#### code_vs_comment

**Description:** Docstring format inconsistency for CHR function

**Affected files:**
- `src/basic_builtins.py`

**Details:**
CHR method docstring says 'Character from ASCII code' but in BASIC it's CHR$ (with dollar sign). Other string functions like LEFT, RIGHT, MID show the $ in their docstrings.

---

#### code_vs_comment

**Description:** Docstring example shows function that doesn't exist in the file

**Affected files:**
- `src/debug_logger.py`

**Details:**
Module docstring shows 'from debug_logger import debug_log_error, is_debug_mode' but the actual import should be 'from src.debug_logger import ...' based on the file location in src/ directory.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for file listing return types

**Affected files:**
- `src/file_io.py`
- `src/filesystem/base.py`

**Details:**
FileIO.list_files() returns: 'List of (filename, size_bytes, is_dir) tuples'
FileSystemProvider.list_files() returns: 'List of filenames'

Both are file listing operations but return completely different data structures. FileIO includes size and directory flag, FileSystemProvider returns only names.

---

#### code_vs_comment

**Description:** InMemoryFileHandle.flush() docstring is misleading

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
Docstring says: 'Flush write buffers.' with comment 'StringIO/BytesIO don't need explicit flushing, but provide for compatibility'

But the implementation only calls flush if the method exists:
```python
if hasattr(self.file_obj, 'flush'):
    self.file_obj.flush()
```

StringIO and BytesIO DO have flush() methods (they're no-ops but exist), so the hasattr check is unnecessary. The comment suggests they don't have flush() which is incorrect.

---

#### code_vs_comment

**Description:** Comment in parse_single_line() mentions stripping prefix that may not exist

**Affected files:**
- `src/editing/manager.py`

**Details:**
Comment says: '# Remove "Parse error at line N, " prefix since we show the BASIC line number'

But the regex pattern r'^Parse error at line \d+, ' may not match all parser errors. If the parser doesn't include this prefix, the re.sub() will do nothing, which is fine, but the comment implies it always exists.

---

#### documentation_inconsistency

**Description:** Duplicate error code 10 (DD) with different meanings

**Affected files:**
- `src/error_codes.py`

**Details:**
Error code 10 is defined as: 10: ('DD', 'Duplicate definition')
But error code 68 also uses 'DD': 68: ('DD', 'Device unavailable')

Two different errors share the same two-letter code 'DD', which would make error messages ambiguous.

---

#### documentation_inconsistency

**Description:** Duplicate error code 5 (DF) with different meanings

**Affected files:**
- `src/error_codes.py`

**Details:**
Error code 25 is defined as: 25: ('DF', 'Device fault')
But error code 61 also uses 'DF': 61: ('DF', 'Disk full')

Two different errors share the same two-letter code 'DF', which would make error messages ambiguous.

---

#### documentation_inconsistency

**Description:** Duplicate two-letter code 'CN' for different error numbers

**Affected files:**
- `src/error_codes.py`

**Details:**
Error code 17 is defined as: 17: ('CN', 'Can't continue')
But error code 69 also uses 'CN': 69: ('CN', 'Communication buffer overflow')

Two different errors share the same two-letter code 'CN', which would make error messages ambiguous.

---

#### code_vs_comment

**Description:** Comment says 'always available in TK UI' but code handles None cases

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Line ~42 comment says 'runtime: Runtime instance (always available in TK UI)' and line ~43 says 'interpreter: Interpreter instance (always available in TK UI)', but the execute() method at line ~186 checks 'if self.runtime is None or self.interpreter is None' and returns an error. If they're 'always available', this check is unnecessary.

---

#### code_vs_comment

**Description:** Help text says 'Cannot execute during INPUT or program running state' but can_execute_immediate() allows INPUT state

**Affected files:**
- `src/immediate_executor.py`

**Details:**
The _show_help() method lists 'Cannot execute during INPUT or program running state' as a limitation, but can_execute_immediate() at line ~82 returns True when 'state.input_prompt is not None', which means INPUT state is allowed. This contradicts the help text.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation about when immediate mode can execute

**Affected files:**
- `src/immediate_executor.py`

**Details:**
The class docstring lists safe states as 'idle', 'paused', 'at_breakpoint', 'done', 'error' and unsafe states as 'running', 'waiting_for_input'. But can_execute_immediate() checks runtime.halted, state.error_info, and state.input_prompt (which would be waiting_for_input). The help text says 'Cannot execute during INPUT' but the code allows it.

---

#### code_vs_comment

**Description:** Docstring example shows tuple return but doesn't match actual tuple structure

**Affected files:**
- `src/input_sanitizer.py`

**Details:**
The sanitize_and_clear_parity() docstring examples show '('PRINT "Test"', False)' format, but the Returns section describes it as 'Tuple of (sanitized_text, was_modified)' which is correct. The examples are correct but could be clearer about what False/True represent.

---

#### code_vs_comment

**Description:** Comment about restoring yellow highlight is overly specific and may be fragile

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Lines ~147-161 contain very detailed logic to 'Restore yellow highlight if there's a current execution position' with multiple hasattr checks and specific UI method calls. This seems like UI-specific logic embedded in what should be a general-purpose executor class. The comment suggests this is a workaround rather than proper design.

---

#### code_vs_comment

**Description:** Import statement comment references wrong module name

**Affected files:**
- `src/interactive.py`

**Details:**
Line 48: Comment says '# Import TypeInfo here to avoid circular dependency' followed by 'from parser import TypeInfo'. Should be 'from src.parser import TypeInfo' to match project structure, or the comment is misleading about the actual import path.

---

#### code_vs_comment

**Description:** Docstring for cmd_chain mentions delete_range parameter but implementation doesn't show full expression evaluation

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 368-369: Comment says 'delete_range is a tuple of (start_expr, end_expr). We need to evaluate them if they're expressions'. Lines 370-381 show hasattr checks for 'value' attribute and int() conversion, but comment on line 371 says 'For now, assume they're NumberNodes - full implementation would evaluate', indicating incomplete implementation despite docstring suggesting full support.

---

#### code_vs_comment

**Description:** Comment claims everything goes through parser, but AUTO and EDIT are special-cased

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 234-236: Comment says 'Meta-commands (editor commands that manipulate program source). Only AUTO and EDIT are true meta-commands that can't be parsed. Everything else (LIST, DELETE, RENUM, FILES, LOAD, SAVE, etc.) goes through parser'. This is accurate, but then lines 237-244 show AUTO and EDIT being handled specially before the else clause that calls execute_immediate(). The comment is correct but the phrasing 'Everything else...goes through parser' could be clearer that it means 'everything except AUTO and EDIT'.

---

#### code_vs_comment

**Description:** Comment about MERGE preserving variables conflicts with actual implementation

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 451-456: Comment says 'Save variables based on CHAIN options: - MERGE: always preserves all variables (it's an overlay)'. However, lines 457-459 show 'if all_flag or merge: saved_variables = self.program_runtime.get_all_variables()', which suggests MERGE and ALL are treated the same way. The comment implies MERGE automatically preserves variables, but the code shows it only preserves them if there's a program_runtime.

---

#### code_vs_comment

**Description:** Docstring for _serialize_line mentions preserving indentation, but no indentation logic is visible

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 759-766: Docstring says 'Serialize a LineNode back to source text, preserving indentation'. Implementation just delegates to ui_helpers.serialize_line(). Without seeing ui_helpers code, it's unclear if indentation is actually preserved or if the comment is outdated.

---

#### code_vs_comment

**Description:** Comment about fallback for non-TTY in _read_char doesn't match exception handling

**Affected files:**
- `src/interactive.py`

**Details:**
Lines 968-979: Comment on line 977 says 'Fallback for non-TTY (piped input)'. However, the except clause catches all exceptions without specifying which exceptions indicate non-TTY. This could hide real errors like IOError or OSError.

---

#### code_vs_comment

**Description:** Comment about old execution methods removal references wrong version

**Affected files:**
- `src/interpreter.py`

**Details:**
At line ~1000, comment says '# OLD EXECUTION METHODS REMOVED (v1.0.300)' but the file header at line ~3 shows 'MBASIC 5.21 Interpreter'. Version numbering inconsistency between internal comments and public version.

---

#### code_vs_comment

**Description:** Comment about PC halted state check is redundant

**Affected files:**
- `src/interpreter.py`

**Details:**
In tick_pc() at line ~620, comment says '# Check if halted' followed by 'if pc.halted() or self.runtime.halted:' and then '# Ensure runtime.halted is set if PC is halted'. The comment 'Ensure runtime.halted is set' suggests this is a synchronization step, but the code always sets runtime.halted = True regardless of which condition triggered. The comment makes it sound like a conditional sync, but it's unconditional.

---

#### code_vs_comment

**Description:** Comment about char_end calculation explains algorithm but doesn't mention why it's needed

**Affected files:**
- `src/interpreter.py`

**Details:**
In current_statement_char_end property at line ~70, detailed comment explains 'Uses max(char_end, next_char_start - 1) to handle string tokens correctly' with algorithm details, but doesn't explain why string tokens have incorrect char_end in the first place. This suggests a workaround for a bug elsewhere (likely in tokenizer/parser) but doesn't document the root cause.

---

#### code_vs_comment

**Description:** execute_poke comment says 'cannot modify memory in Python interpreter' but this is obvious and the comment doesn't explain why it's kept

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: 'POKE is emulated as a no-op since we cannot write to arbitrary memory'
The comment explains what POKE does but doesn't explain why the statement exists at all if it's a no-op. Should clarify it's for compatibility with programs that use POKE.

---

#### code_vs_comment

**Description:** execute_lineinput comment duplicates execute_input comment about tick-based execution

**Affected files:**
- `src/interpreter.py`

**Details:**
Both execute_input and execute_lineinput have nearly identical comments about tick-based execution and state machine behavior. This duplication could lead to inconsistency if one is updated and the other isn't.

---

#### code_vs_comment

**Description:** execute_close comment says 'Silently ignore closing unopened files (like MBASIC)' but doesn't verify this is actually MBASIC behavior

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment claims this matches MBASIC behavior but doesn't cite a reference or test. Should verify this is actually how MBASIC 5.21 behaves.

---

#### code_vs_comment

**Description:** execute_stop docstring is incomplete - just says 'Execute STOP statement' without describing behavior

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring: 'Execute STOP statement

STOP pauses program execution and returns to interactive mode.'
The docstring is cut off mid-sentence and doesn't describe the actual implementation or how it differs from END.

---

#### code_vs_comment

**Description:** Comment in evaluate_functioncall says 'We use get_variable_for_debugger here because we're saving state' but this contradicts the purpose of get_variable_for_debugger

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: '# Note: We use get_variable_for_debugger here because we're saving state, not actually reading for use'. The function name 'get_variable_for_debugger' suggests it's for debugger inspection, but the comment justifies using it for saving function parameter state during normal execution. This is either a misnamed function or misuse of a debugger-specific function.

---

#### code_vs_comment

**Description:** Comment says 'Use debugger_set=True since this is implementation detail' but this is restoring function parameters, not a debugger operation

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: '# Use debugger_set=True since this is implementation detail, not actual program assignment'. The code is restoring saved parameter values after function execution, which is normal runtime behavior, not a debugger implementation detail. The use of debugger_set=True flag seems incorrect for this use case.

---

#### code_vs_comment

**Description:** Comment in evaluate_variable says 'track access' for array access but no tracking code is shown

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: '# Array access - track access'. The code then calls get_array_element but there's no visible tracking mechanism in this snippet. Either the tracking happens inside get_array_element (making the comment misleading) or tracking is not implemented.

---

#### code_vs_comment

**Description:** Comment in evaluate_binaryop says 'Enforce 255 byte string limit (MBASIC 5.21 compatibility)' but only checks after concatenation

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment: '# Enforce 255 byte string limit (MBASIC 5.21 compatibility)'. The check 'if isinstance(result, str) and len(result) > 255' only applies to string concatenation (PLUS operator). Other string operations in the codebase may not enforce this limit, creating inconsistent behavior.

---

#### code_vs_comment

**Description:** Module docstring mentions 'curses' but imports 'curses_io'

**Affected files:**
- `src/iohandler/__init__.py`

**Details:**
The docstring says 'allowing the interpreter to work with different I/O backends (console, GUI, curses, embedded, etc.)' using lowercase 'curses', but the actual import is 'from .curses_io import CursesIOHandler' and the module is named 'curses_io.py'. This is a minor naming inconsistency in documentation.

---

#### code_vs_documentation

**Description:** GUIIOHandler not exported in __all__

**Affected files:**
- `src/iohandler/__init__.py`
- `src/iohandler/gui.py`

**Details:**
__init__.py exports ['IOHandler', 'ConsoleIOHandler', 'CursesIOHandler'] but gui.py defines GUIIOHandler which is not included. This may be intentional since it's a stub, but creates inconsistency in what's publicly available.

---

#### code_vs_documentation

**Description:** WebIOHandler not exported in __all__

**Affected files:**
- `src/iohandler/__init__.py`
- `src/iohandler/web_io.py`

**Details:**
__init__.py does not export WebIOHandler even though web_io.py is a complete implementation (not just a stub like gui.py). This creates inconsistency in module exports.

---

#### documentation_inconsistency

**Description:** Inconsistent example formatting in docstrings

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/console.py`

**Details:**
base.py uses 'Examples:' section with indented examples like 'output("HELLO")'. console.py docstrings use 'Note:' sections but no 'Examples:' sections. Inconsistent documentation style across the module.

---

#### code_vs_comment

**Description:** Docstring says 'identical to input()' but implementation differs

**Affected files:**
- `src/iohandler/console.py`

**Details:**
console.py input_line() docstring says 'For console, this is identical to input()' but the implementation is 'return self.input(prompt)' which calls the instance method, not Python's built-in input(). While functionally similar, the comment is technically imprecise.

---

#### code_vs_comment

**Description:** Comment mentions color_pair(4) for errors without initialization

**Affected files:**
- `src/iohandler/curses_io.py`

**Details:**
curses_io.py error() method uses 'curses.color_pair(4)' for red error text, but there's no initialization code shown that sets up color pair 4. The comment 'Try to use red color for errors' suggests this should work, but color pairs must be initialized with init_pair() first.

---

#### code_vs_comment

**Description:** Docstring says 'uses dialogs for input' but implementation uses ui.dialog

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
web_io.py class docstring says 'I/O handler that outputs to NiceGUI log and uses dialogs for input' but the actual implementation in input() method creates a custom dialog with ui.dialog(), ui.card(), ui.label(), etc. The docstring is vague about the implementation details.

---

#### code_vs_comment

**Description:** Comment says 'Not yet implemented' but returns empty string

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
web_io.py get_char() has comment 'Note: Not yet implemented for web UI. Returns empty string.' This is accurate but the method should probably raise NotImplementedError instead of silently returning empty string, which could mask bugs.

---

#### code_vs_comment

**Description:** Comment says 'Not applicable' but implements method anyway

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
web_io.py set_cursor_position() has comment 'Note: Not applicable for log-based output.' but still defines the method with 'pass'. Should either raise NotImplementedError or be removed if truly not applicable.

---

#### code_vs_comment

**Description:** Comment in parse_line() states 'Note: We don't store source_text - AST is the single source of truth' but then code tracks char_start and char_end for statement highlighting

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line ~280: '# Note: We don't store source_text - AST is the single source of truth' but immediately after, the code sets stmt.char_start and stmt.char_end with comment '# Set character positions on statement for highlighting'. This suggests source text positions ARE being tracked, contradicting the comment.

---

#### documentation_inconsistency

**Description:** Module docstring mentions 'Key differences from interpreter' but parser doesn't appear to be part of an interpreter comparison

**Affected files:**
- `src/parser.py`

**Details:**
The module docstring states 'Key differences from interpreter: - DEF type statements are applied globally at compile time' suggesting this is a compiler vs interpreter comparison, but there's no interpreter code in the provided files to compare against. This may be outdated documentation from a refactoring.

---

#### code_vs_comment

**Description:** Inconsistent terminology for 'end of input' vs 'end of tokens'

**Affected files:**
- `src/parser.py`

**Details:**
Multiple methods exist with similar but slightly different names and purposes: at_end(), has_more_tokens(), at_end_of_tokens(), at_end_of_line(), at_end_of_statement(). The docstrings and comments use 'end of input', 'end of tokens', and 'exhausted all tokens' interchangeably. For example, at_end() checks for EOF token, while at_end_of_tokens() checks if current() is None, which are different conditions.

---

#### code_vs_comment

**Description:** Comment about ERR and ERL as system variables conflicts with their placement in expression parsing

**Affected files:**
- `src/parser.py`

**Details:**
In parse_primary(), the comment states 'ERR and ERL are system variables (integer type)' and they return VariableNode. However, in is_builtin_function(), there's a note 'Note: ERR and ERL are not functions, they are system variables'. This is consistent, but the placement in parse_primary() as a special case after checking for builtin functions suggests they might have been functions at some point.

---

#### code_vs_comment

**Description:** Comment about LPRINT file number syntax doesn't match MBASIC standard

**Affected files:**
- `src/parser.py`

**Details:**
In parse_lprint(), the comment shows 'LPRINT #filenum, expr1 - Print to file'. However, LPRINT is specifically for line printer output in MBASIC 5.21, and the #filenum syntax is typically for PRINT, not LPRINT. This may be a feature extension not documented in the module header.

---

#### code_comment_conflict

**Description:** Comment mentions LINE modifier but code checks for LINE_INPUT token

**Affected files:**
- `src/parser.py`

**Details:**
In parse_input() around line 65, comment says 'Check for LINE modifier after semicolon: INPUT "prompt";LINE var$' but code checks for TokenType.LINE_INPUT. The comment suggests LINE is a separate keyword/modifier, but implementation treats it as a compound token LINE_INPUT.

---

#### code_comment_conflict

**Description:** Comment about line_mode variable that is set but never used

**Affected files:**
- `src/parser.py`

**Details:**
In parse_input() around line 68, code sets 'line_mode = True' when LINE_INPUT token is matched, with comment 'LINE allows input of entire line including commas'. However, line_mode is never passed to InputStatementNode or used elsewhere in the method.

---

#### code_comment_conflict

**Description:** Comment in parse_common() is incomplete

**Affected files:**
- `src/parser.py`

**Details:**
At the end of parse_common() around line ~1550, there's an incomplete comment: '# (we don't need to do anything special with arrays in COMMON,' - the comment is cut off mid-sentence, suggesting incomplete documentation or refactoring.

---

#### code_vs_comment

**Description:** parse_line_input docstring mentions lexer behavior that may not be accurate

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states 'Note: Lexer produces LINE_INPUT token, but INPUT keyword may follow' and code checks 'if self.match(TokenType.INPUT): self.advance()'. This suggests the lexer might produce both LINE_INPUT and INPUT tokens sequentially, which seems unusual. Either the comment is outdated or the lexer behavior is non-standard.

---

#### code_vs_comment

**Description:** parse_data comment about unquoted strings handling doesn't match implementation complexity

**Affected files:**
- `src/parser.py`

**Details:**
Comment states 'Unquoted strings extend until comma, colon, or end of line' but implementation has complex logic handling MINUS, PLUS, LINE_NUMBER tokens, and keywords with string values. The actual behavior is more nuanced than the comment suggests, accepting tokens like 'E-5' and keywords as part of unquoted strings.

---

#### code_vs_comment

**Description:** parse_clear docstring syntax description incomplete

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states 'Syntax: CLEAR [,][string_space][,stack_space]' but the implementation only handles two arguments (string_space and stack_space), not the leading comma option shown in the syntax. The code does 'if not self.match(TokenType.COMMA): string_space = self.parse_expression()' which suggests optional first argument, but doesn't handle a leading comma as the syntax suggests.

---

#### code_vs_comment

**Description:** Comment says 'AST is the single source of truth' but function name suggests text preservation

**Affected files:**
- `src/position_serializer.py`

**Details:**
Line 476 comment in serialize_line says 'AST is the single source of truth - always serialize from AST' but the function is called 'serialize_line_with_positions' and the module is about 'Position-Aware AST Serialization' suggesting it preserves original text positions, not just regenerates from AST.

---

#### code_vs_comment

**Description:** Comment about 'preserve' policy handling is inconsistent with implementation

**Affected files:**
- `src/position_serializer.py`

**Details:**
Lines 60-62 in apply_keyword_case_policy say 'Preserve is handled by caller passing in original case' and 'This shouldn't be called with "preserve"', but then line 63 returns keyword.capitalize() as fallback. This suggests the function CAN be called with 'preserve' despite the comment.

---

#### documentation_inconsistency

**Description:** Module docstring mentions 'current_line/current_stmt/next_line/next_stmt' but these are never defined or used

**Affected files:**
- `src/pc.py`

**Details:**
Lines 10-11 say 'No need to track current_line/current_stmt/next_line/next_stmt separately' implying these were previous design elements, but they don't appear anywhere in the codebase shown. This is historical context that may confuse readers.

---

#### code_vs_comment

**Description:** Fallback comment mentions ui_helpers but doesn't explain when fallback is used

**Affected files:**
- `src/position_serializer.py`

**Details:**
Lines 313-315 and 442-444 have fallback code using ui_helpers.serialize_statement/serialize_expression, but there's no documentation explaining when these fallbacks are triggered or why they exist alongside the position-aware serialization.

---

#### code_vs_comment

**Description:** Docstring mentions 'tick-based execution' but no explanation of what a 'tick' is

**Affected files:**
- `src/resource_limits.py`

**Details:**
Lines 35, 92 reference 'max_statements_per_tick' and 'For tick-based execution' but there's no documentation explaining what constitutes a 'tick' in this context or which UIs use tick-based execution.

---

#### code_vs_comment

**Description:** Docstring says 'Note: Type defaults (DEFINT, DEFSNG, etc.) are handled by Parser.def_type_map' but Parser is never imported

**Affected files:**
- `src/runtime.py`

**Details:**
Line 176-177: 'Note: Type defaults (DEFINT, DEFSNG, etc.) are handled by Parser.def_type_map at parse time, not at runtime'. However, there's no import of Parser in this file, and the code references 'from parser import TypeInfo' in _resolve_variable_name (line 119), suggesting the module name might be 'parser' not 'Parser'.

---

#### code_vs_comment

**Description:** Inconsistent terminology for 'canonical case' vs 'original_case'

**Affected files:**
- `src/runtime.py`

**Details:**
The code uses both 'canonical_case' (lines 307, 311, 315, 348, 352, 356) and 'original_case' (lines 286, 304, 342, 345, 357, 1001) to refer to the same concept. The variable storage uses key 'original_case' but the local variable is named 'canonical_case', creating confusion about which is the authoritative term.

---

#### code_vs_comment

**Description:** Comment about line -1 sentinel appears in multiple places with slightly different wording

**Affected files:**
- `src/runtime.py`

**Details:**
Line 145: 'Note: line -1 in last_write indicates debugger/prompt/internal set', line 370: 'Debugger/prompt set: use line -1 as sentinel', line 1000: 'Note: line -1 in last_write indicates debugger/prompt set'. The wording varies between 'debugger/prompt/internal' and just 'debugger/prompt', creating ambiguity about what line -1 represents.

---

#### code_vs_comment

**Description:** get_execution_stack() includes 'return_stmt' and 'stmt' fields in returned dictionaries but these are not documented in the docstring

**Affected files:**
- `src/runtime.py`

**Details:**
The code adds 'return_stmt' for GOSUB entries, 'stmt' for FOR entries, and 'stmt' for WHILE entries, but the docstring examples only show: {'type': 'GOSUB', 'from_line': 50, 'return_line': 60} without mentioning the 'return_stmt' field. Similarly for FOR and WHILE, the 'stmt' field is not documented.

---

#### code_vs_comment

**Description:** Comment says 'Note: Tab key is used for window switching in curses UI, not indentation' but there's no evidence of this in the curses UI implementation

**Affected files:**
- `src/settings_definitions.py`

**Details:**
Comment at line after editor.auto_number_step: '# Note: Tab key is used for window switching in curses UI, not indentation'. However, src/ui/__init__.py shows CursesBackend is optional and may not be available. The comment references functionality not visible in provided code.

---

#### code_vs_comment

**Description:** Comment says 'Note: Line numbers are always shown - they're fundamental to BASIC!' but this is a design decision comment, not a code explanation

**Affected files:**
- `src/settings_definitions.py`

**Details:**
Comment after editor.auto_number_step: '# Note: Line numbers are always shown - they're fundamental to BASIC! # Removed editor.show_line_numbers setting as it makes no sense for BASIC'. This explains why a setting was removed but doesn't document current code behavior.

---

#### code_vs_comment

**Description:** Comment mentions settings that are 'available but not shown in UI' without documenting where they are defined

**Affected files:**
- `src/settings_definitions.py`

**Details:**
Comment: '# Note: interpreter.max_execution_time and interpreter.debug_mode are available # but not shown in UI - edit settings file directly if needed'. These settings are not defined in SETTING_DEFINITIONS dict, creating confusion about whether they actually exist.

---

#### code_vs_comment

**Description:** Comment says 'ui.theme not implemented yet' but doesn't indicate if it's planned or just a placeholder

**Affected files:**
- `src/settings_definitions.py`

**Details:**
Comment at end of SETTING_DEFINITIONS: '# Note: ui.theme not implemented yet'. No corresponding setting definition exists, and it's unclear if this is a TODO or just documentation of what's missing.

---

#### code_vs_documentation

**Description:** Docstring says 'first wins doesn't make sense for keywords' but doesn't explain why variables have this option

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
Module docstring: 'Unlike variables, "first wins" doesn't make sense for keywords since the interpreter registers them at startup.' This implies variables have a 'first_wins' policy (confirmed in settings_definitions.py) but doesn't explain the conceptual difference clearly.

---

#### code_vs_documentation

**Description:** Token class has both original_case and original_case_keyword fields but documentation doesn't explain when each is used

**Affected files:**
- `src/tokens.py`

**Details:**
Token dataclass has 'original_case: Any = None  # Original case for identifiers (before lowercasing)' and 'original_case_keyword: str = None  # Original case for keywords'. The __repr__ method shows both can be present, but there's no explanation of why two separate fields are needed or when each is populated.

---

#### code_vs_comment

**Description:** Docstring example shows 'get_content_callback' but parameter name in method is 'get_content_callback'

**Affected files:**
- `src/ui/auto_save.py`

**Details:**
Module docstring shows: 'manager.start_autosave('foo.bas', get_content_callback, interval=30)' which matches the actual parameter name, so this is consistent. However, the internal attribute is named 'self.get_content' which could be confusing.

---

#### code_vs_documentation

**Description:** UIBackend docstring mentions HeadlessBackend but it's not implemented in __init__.py

**Affected files:**
- `src/ui/base.py`

**Details:**
base.py docstring lists 'HeadlessBackend: No UI, for batch processing' as an example implementation, but src/ui/__init__.py only exports UIBackend, CLIBackend, VisualBackend, CursesBackend, and TkBackend. HeadlessBackend is not implemented.

---

#### code_vs_documentation

**Description:** UIBackend docstring mentions MobileBackend and WebBackend but they're not implemented

**Affected files:**
- `src/ui/base.py`

**Details:**
base.py docstring lists 'MobileBackend: Touch-based mobile UI' and 'WebBackend: Browser-based interface' as example implementations, but these are not present in src/ui/__init__.py exports. These appear to be aspirational examples rather than actual implementations.

---

#### code_vs_documentation

**Description:** CLIBackend adds debugger but this is not mentioned in UIBackend base class documentation

**Affected files:**
- `src/ui/cli.py`

**Details:**
CLIBackend.__init__ calls 'from .cli_debug import add_debug_commands' and creates 'self.debugger', but this debugging capability is not mentioned in the UIBackend abstract interface documentation. It's unclear if other backends should also support debugging.

---

#### code_vs_comment

**Description:** Comment says 'Create scrollable list (without buttons)' but there are no buttons in the code at all

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
In curses_settings_widget.py line with comment '# Create scrollable list (without buttons)' - the comment implies buttons were removed or considered, but the entire file shows button functionality is handled via keyboard shortcuts (_on_apply, _on_ok, _on_cancel, _on_reset methods) not actual button widgets. The comment is misleading about the design.

---

#### code_vs_comment

**Description:** Comment says 'strip force_ prefix for cleaner display' but only applies to display, not consistently documented

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
In _create_setting_widget for ENUM type, code has comment '# Create display label (strip force_ prefix for cleaner display)' and later '# Use stored actual value (with force_ prefix) not display label'. This implies enum values have 'force_' prefix but this convention is not documented in the file header or class docstring, making it unclear why this prefix exists or what it means.

---

#### code_vs_comment

**Description:** Comment says 'This would integrate with help system' but provides no implementation or TODO

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
In _add_debug_help method, the only content is comment '# This would integrate with help system' with pass statement. This is a placeholder but doesn't indicate whether it's intentionally deferred, needs implementation, or is a TODO. Should be marked as TODO or FIXME if incomplete.

---

#### documentation_inconsistency

**Description:** Ctrl+C described as 'Continue execution' conflicts with standard terminal behavior

**Affected files:**
- `src/ui/curses_keybindings.json`

**Details:**
curses_keybindings.json maps Ctrl+C to 'continue' with description 'Continue execution'. However, Ctrl+C is the standard terminal interrupt signal. The JSON also notes 'Ctrl+S unavailable - terminal flow control' for save command, showing awareness of terminal control conflicts, but doesn't acknowledge the Ctrl+C conflict.

---

#### code_vs_comment

**Description:** Comment about showing error dialog doesn't match actual implementation

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
In _apply_settings method: 'except Exception as e: # Show error (in real implementation would show dialog) return False'. The comment admits this is not the real implementation and would show a dialog, but the code just returns False silently. This is inconsistent with production-quality code.

---

#### code_vs_comment

**Description:** Comment describes format with fixed-width line numbers but implementation is variable-width

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple comments describe format as 'SNNNNN CODE' (suggesting 5-digit line numbers), but the _parse_line_number method and actual formatting use variable-width line numbers. For example, line 1000 says 'Format: "SNNNNN CODE"' but line 1009 just does 'line_num_str = f"{line_num}"' with no width specification.

---

#### code_vs_comment

**Description:** Comment says 'Variable-width line numbers - no need to right-justify' but earlier comments suggest fixed width

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line 476 has comment 'Variable-width line numbers - no need to right-justify' which contradicts earlier format descriptions like 'SNNNNN CODE' and '5 chars' in docstrings and comments.

---

#### code_vs_comment

**Description:** Comment about column structure mentions fixed positions but code uses variable-width parsing

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line 1398 comment says 'Handles both: - Lines with column structure: " [space]     10 PRINT"' suggesting fixed-width columns, but the _parse_line_number method finds the space dynamically for variable-width line numbers.

---

#### code_vs_comment

**Description:** Comment says 'Extract status, line number column, and code area' but code uses variable-width parsing

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line 1461 comment suggests fixed columns but the code immediately calls _parse_line_number which returns variable positions based on finding the space delimiter.

---

#### code_vs_comment

**Description:** Comment says 'Create a proper ImmediateExecutor (will be re-initialized in start() and _run_program())' but _run_program() is not visible in the provided code

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment in __init__: 'Create a proper ImmediateExecutor (will be re-initialized in start() and _run_program())' but _run_program() method is not shown in the provided code snippet, so cannot verify if it actually reinitializes the executor.

---

#### code_vs_comment

**Description:** Comment says 'Toolbar removed' but _create_toolbar() method still exists and creates toolbar widgets

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _create_ui() method: comment says '# Toolbar removed - use Ctrl+U menu instead for keyboard navigation' but the _create_toolbar() method is still defined and functional in the code, creating New, Open, Save, Run, Stop, Step, Stmt, and Cont buttons.

---

#### code_internal_inconsistency

**Description:** Inconsistent cursor positioning comments in _delete_current_line() method

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment says 'Always position at column 1 (start of line number field)' but then the code calculates 'new_cursor_pos = sum(len(lines[i]) + 1 for i in range(line_index)) + 1' which adds 1 to the sum, and for first line sets 'new_cursor_pos = 1'. However, for the else branch (last line deleted), it positions at 'len(lines[-1])' which is the end of the line, not column 1.

---

#### code_vs_comment

**Description:** Comment in _show_help() says 'Store original widget BEFORE replacing it' but no replacement code follows

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _show_help() method: comment says '# Store original widget BEFORE replacing it' followed by 'main_widget = self.loop.widget' but there is no code after this that actually replaces the widget or uses main_widget. The method appears incomplete.

---

#### code_vs_comment

**Description:** Comment says 'Don't call draw_screen() - it uses default colors (39;49) which may be white' but this is a workaround comment that may be outdated

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _activate_menu() method: comment '# Don't call draw_screen() - it uses default colors (39;49) which may be white' suggests avoiding draw_screen() due to color issues, but this may be a workaround for a bug that should be fixed properly rather than avoided.

---

#### code_vs_comment

**Description:** Comment about preserving breakpoints may be misleading about what reset_for_run does

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment says '# Reset runtime with current program - RUN = CLEAR + GOTO first line
# This preserves breakpoints but clears variables'. The comment implies reset_for_run preserves breakpoints, but breakpoints are actually set separately after reset via 'self.interpreter.set_breakpoint(line_num)' loop. The reset_for_run method itself doesn't preserve breakpoints - they're re-applied from editor.breakpoints.

---

#### code_vs_comment

**Description:** Comment about Urwid automatic redraw contradicts explicit draw_screen call in another method

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_output(), comment states '# Urwid will redraw automatically - no need to force draw_screen()'. However, in _update_output_with_lines(), there's an explicit call to 'self.loop.draw_screen()' with comment '# Force a screen update'. This inconsistency suggests either the automatic redraw isn't reliable in all cases, or one of these methods has unnecessary code.

---

#### code_vs_comment

**Description:** Variable filter dialog shows 'Ctrl+W=toggle' in title but Ctrl+W functionality not shown in code snippet

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_variables_window(), the title includes 'Ctrl+W=toggle' as a keyboard shortcut, but the provided code snippet doesn't show the handler for Ctrl+W or what it toggles. This may be implemented elsewhere, but the inconsistency is that the UI advertises a feature whose implementation isn't visible in context.

---

#### code_vs_comment

**Description:** Comment about 'dummy handler' doesn't explain why it's needed

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _set_variables_filter(), there's a line 'urwid.connect_signal(edit, 'change', lambda _w, _t: None)  # dummy handler'. The comment doesn't explain why this dummy handler is necessary or what would happen without it. This makes the code's intent unclear.

---

#### code_vs_comment

**Description:** Comment says 'Set focus on the walker (not the ListBox)' but doesn't explain why this distinction matters

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_output(), comment states '# Set focus on the walker (not the ListBox)' but doesn't explain the significance of this distinction or what would happen if focus was set on the ListBox instead. This makes the comment less helpful for future maintainers.

---

#### code_vs_comment

**Description:** Comment describes CapturingIOHandler as 'defined in _run_program' but it's duplicated inline

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment says '# (it's defined in _run_program, but we need it here too)' followed by inline class definition. This indicates code duplication - the same class is defined in multiple places, which is a maintenance issue. If the class in _run_program is updated, this copy won't be.

---

#### code_vs_comment

**Description:** Docstring for cmd_run mentions start_line parameter but doesn't explain RUN vs RUN line_number distinction

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Docstring says 'Optional line number to start execution at (for RUN line_number)' but doesn't explain what happens when start_line is None vs when it has a value. The implementation calls '_run_program(start_line=start_line)' but the behavior difference isn't documented.

---

#### code_vs_comment

**Description:** Comment about 'Check if file exists' followed by Path().exists() but no handling of race condition

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment '# Check if file exists' followed by 'if not Path(filepath).exists():' and then later 'try: self._load_program_file(filepath)'. There's a TOCTOU (time-of-check-time-of-use) race condition - the file could be deleted between the exists() check and the load attempt. The comment doesn't acknowledge this limitation.

---

#### Code vs Comment conflict

**Description:** Comment says 'Ctrl+S unavailable - terminal flow control' but then assigns Ctrl+V, suggesting Ctrl+S might work in some terminals

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py line 143-145: '# Save program (Ctrl+S unavailable - terminal flow control) # Use Ctrl+V instead (V for saVe)' - This is a design decision comment but doesn't clarify if this is universal or terminal-specific

---

#### Code vs Documentation inconsistency

**Description:** STATUS_BAR_SHORTCUTS shows '^K stack' but STACK_KEY is empty string and STACK_DISPLAY is 'Menu only'

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py line 286: STATUS_BAR_SHORTCUTS = "MBASIC - ^F help  ^U menu  ^W vars  ^K stack  Tab cycle  ^Q quit" shows ^K for stack, but lines 105-107 define STACK_KEY = '', STACK_DISPLAY = 'Menu only'

---

#### Code vs Comment conflict

**Description:** Comment says 'Ctrl+I unavailable - identical to Tab' but then assigns Ctrl+J for insert line

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
keybindings.py line 175-177: '# Smart Insert Line (Ctrl+I unavailable - identical to Tab) # Use Ctrl+J instead (J for inJect/insert)' - This is informative but the mnemonic 'inJect' is questionable

---

#### Code vs Documentation inconsistency

**Description:** HelpMacros._expand_macro returns hardcoded version '5.21' but no documentation explains where this version comes from or how to update it

**Affected files:**
- `src/ui/help_macros.py`

**Details:**
help_macros.py line 68: return "5.21"  # MBASIC version - hardcoded version string with no reference to where this should be maintained or updated

---

#### Code vs Comment conflict

**Description:** Docstring says 'Search across three-tier help system (/)' but _search_indexes only shows two tiers in tier_labels

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
help_widget.py line 11: docstring mentions 'three-tier help system' but line 127-130: tier_labels only defines 'language' and 'mbasic', with 'ui' being derived from path check. Third tier not clearly documented.

---

#### code_vs_documentation

**Description:** Keymap widget references KEYBINDINGS_BY_CATEGORY but tk_keybindings.json uses different structure

**Affected files:**
- `src/ui/keymap_widget.py`
- `src/ui/tk_keybindings.json`

**Details:**
keymap_widget.py imports 'from .keybindings import KEYBINDINGS_BY_CATEGORY' and expects format like {category: [(key, description), ...]}. However, tk_keybindings.json shows a nested structure with menu/editor/view categories containing objects with 'keys', 'primary', and 'description' fields. The data structures don't match.

---

#### code_vs_comment

**Description:** Comment about thread-safety not reflected in implementation

**Affected files:**
- `src/ui/recent_files.py`

**Details:**
Module docstring claims 'Thread-safe file operations' but the implementation has no locking mechanisms, mutexes, or thread-safety measures. The _load_recent_files and _save_recent_files methods could have race conditions if called from multiple threads.

---

#### code_vs_comment

**Description:** Comment about Ctrl+C and Ctrl+A handling doesn't match full implementation

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Comment in readonly_key_handler says '# Allow copy operations and find' and checks for 'c', 'C', 'a', 'A' with comment 'Ctrl+C, Ctrl+A'. However, the code also handles 'f', 'F' for Ctrl+F (find), which is not mentioned in the initial comment about 'copy operations'.

---

#### code_vs_documentation

**Description:** Help browser Ctrl+F keybinding not documented in keybindings.json

**Affected files:**
- `src/ui/tk_help_browser.py`
- `src/ui/tk_keybindings.json`

**Details:**
tk_help_browser.py implements Ctrl+F for in-page search with self.bind('<Control-f>', lambda e: self._inpage_search_show()), but tk_keybindings.json only documents 'Return' for help_browser category. The Ctrl+F keybinding is missing from the configuration.

---

#### code_duplication_inconsistency

**Description:** Table formatting logic duplicated with identical implementation

**Affected files:**
- `src/ui/markdown_renderer.py`
- `src/ui/tk_help_browser.py`

**Details:**
Both files have _format_table_row() methods with nearly identical implementations. markdown_renderer.py has the method at line ~120, tk_help_browser.py has it at the end. Both strip parts, skip separator rows, clean markdown, and use ljust(15). This duplication could lead to inconsistencies if one is updated without the other.

---

#### code_vs_comment

**Description:** Comment about link path resolution doesn't match all code paths

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
In _follow_link(), comment says 'Absolute paths are relative to help root' but then checks 'if target.startswith('/') or target.startswith('common/') or ':/' in target or ':\\' in target'. The inclusion of ':/' and ':\\' suggests checking for actual absolute filesystem paths (like C:\), not just help-root-relative paths. The comment is misleading about what 'absolute' means in this context.

---

#### code_vs_comment

**Description:** Context menu dismiss logic comment doesn't match implementation complexity

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Comment says '# Release grab after a short delay to allow menu interaction' but the code immediately calls menu.grab_release() with no delay. The comment suggests a delay mechanism that isn't implemented. Additionally, the dismiss_menu function and bindings suggest more complex cleanup than the comment implies.

---

#### code_vs_comment

**Description:** Docstring says 'viewing and modifying settings' but class only supports modifying, not just viewing

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Class docstring: 'Dialog for viewing and modifying MBASIC settings.' However, the dialog is fully interactive with Apply/OK buttons - it's not a read-only viewer. The distinction is minor but the docstring could be more accurate by saying 'Dialog for modifying MBASIC settings' or 'Settings editor dialog'.

---

#### code_internal_inconsistency

**Description:** Inconsistent widget value retrieval in _get_current_widget_values method

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
In _get_current_widget_values(), the code has redundant logic: 'if isinstance(widget, tk.Variable): values[key] = widget.get() else: values[key] = widget.get()'. Both branches do the same thing (widget.get()), making the isinstance check pointless. This suggests either the else branch is unnecessary, or there was intended different handling that wasn't implemented.

---

#### code_vs_comment

**Description:** Comment 'Ignore errors on cancel' doesn't explain why this is safe or desirable

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
In _on_cancel() method: 'except Exception: pass  # Ignore errors on cancel'. The comment states what the code does but doesn't explain the reasoning. If restoring original values fails, the user might be left in an inconsistent state. The comment should clarify whether this is intentional (e.g., 'Ignore errors as settings may have been deleted') or if error handling should be improved.

---

#### code_internal_inconsistency

**Description:** Spinbox range hardcoded without reference to setting definition constraints

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
In _create_setting_widget() for INTEGER type: 'widget = ttk.Spinbox(frame, from_=0, to=1000, textvariable=var, width=10)'. The range 0-1000 is hardcoded, but the SettingDefinition might have min/max constraints that should be used instead. This could allow invalid values to be entered.

---

#### code_vs_comment

**Description:** Inconsistent terminology for column references in variable window code

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_variable_heading_click(), the code calculates column positions with comments like '# Value column (swapped to be first)' and '# Type column (swapped to be second)', but the actual Treeview definition shows columns=('Value', 'Type') which means Value is naturally first and Type is naturally second. The 'swapped' terminology is confusing and suggests a historical change that may no longer be accurate.

---

#### code_vs_documentation

**Description:** Docstring describes 3-pane layout but implementation has 4 panes

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
The class docstring says 'Split pane: editor on left, output on right' and lists features, but the actual implementation in start() creates a vertical PanedWindow with 3 panes: editor_frame (top, weight=3), output_frame (middle, weight=2), and immediate_frame (bottom, weight=1). The docstring doesn't mention the immediate mode pane at all.

---

#### code_vs_comment

**Description:** Comment about pane percentages doesn't match weight ratios

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comments say 'Top pane: Editor with line numbers (60% of space)' and 'Middle pane: Output (30% of space)' but the actual weights are 3, 2, and 1 (for editor, output, and immediate respectively), which would be 50%, 33%, and 17%, not 60% and 30%.

---

#### code_vs_comment

**Description:** Comment about INPUT row visibility contradicts implementation details

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment says '# INPUT row (hidden by default, shown when INPUT statement needs input)' followed by '# Don't pack yet - will be packed when needed'. However, the input_row frame is created with 'height=40' parameter, suggesting it has a fixed size even when not packed, which could be misleading about its 'hidden' state.

---

#### code_vs_comment

**Description:** Comment describes behavior that is actually the opposite branch

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines ~150-156: The comment '# OPTION BASE 0: use all zeros' is followed by code that checks 'if array_base == 0:' and uses zeros, then 'else:' with comment '# OPTION BASE 1: use all ones'. This is correct, but the structure makes it seem like the comments are describing what to do in each case rather than what the current array_base value means.

---

#### code_vs_comment

**Description:** Comment says 'default behavior: delete selection, insert newline' but code does exactly that, making the comment redundant

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~1110: Comment describes what the default behavior would be, then the code implements that exact behavior manually. The comment seems to be explaining why the code exists, but it's unclear if this is intentional override or just documentation.

---

#### code_vs_comment

**Description:** Comment says 'only if no errors' but the code already checked for errors earlier and returned if there were any

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Line ~1175: Comment says '# Refresh to sort lines (only if no errors)' but the code at line ~1168 already has 'if not success: ... return 'break'' which means if we reach line 1175, there are definitely no errors. The comment is technically correct but redundant.

---

#### code_vs_comment

**Description:** Comment about 'half yellow line' issue doesn't match the clearing behavior

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_key_press method, comment says 'This prevents the "half yellow line" issue when editing error/breakpoint lines' but the code clears statement highlight when paused_at_breakpoint is true, which is for execution pausing, not error/breakpoint line editing.

---

#### code_vs_comment

**Description:** Comment says 'No state checking - just ask the interpreter' but code does check has_work()

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_immediate method, comment says 'Check if interpreter has work to do (after RUN statement) No state checking - just ask the interpreter' but calling has_work() IS a form of state checking. The comment is misleading.

---

#### code_vs_comment

**Description:** Comment says 'Lines are displayed exactly as stored' but doesn't account for potential formatting

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _highlight_current_statement method, comment says 'Lines are displayed exactly as stored, so char_start/char_end are relative to the line as displayed' but this assumes no whitespace normalization or other transformations occur during display.

---

#### code_vs_comment

**Description:** input_line() docstring says 'Identical to input() for Tk UI' but implementations differ

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring claims: 'Identical to input() for Tk UI.' However, input() uses inline input row (_show_input_row) with fallback to dialog, while input_line() always uses simpledialog.askstring directly. They are not identical.

---

#### code_vs_comment

**Description:** clear_screen() docstring says 'no-op' but doesn't explain why or if it should be implemented

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Method has comment 'Clear screen - no-op for Tk UI.' with just 'pass'. It's unclear if this is intentional design (Tk UI doesn't support clearing) or a TODO. For a Tk UI, clearing the output_text widget would be feasible.

---

#### code_vs_comment

**Description:** Comment in _add_output_immediate says 'immediate mode has no history widget' but code shows immediate_history widget exists

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Method docstring: 'Add text to main output pane (immediate mode has no history widget).' However, the class clearly has self.immediate_history widget that is used in _setup_immediate_context_menu and related methods. The comment is contradictory.

---

#### code_vs_comment

**Description:** Canvas width comment says '~20px' but code sets width to exactly 20

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment in __init__ says: '# Width: ~20px for one status character (●, ?, or space)' but the code sets 'width=20' exactly. The tilde (~) suggests approximation but the value is precise.

---

#### code_vs_comment

**Description:** Status click handler shows info dialog for breakpoints but this is not documented

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
The _on_status_click method shows an info dialog when clicking on a breakpoint symbol (●): 'messagebox.showinfo(f"Breakpoint on Line {line_num}", f"Line {line_num} has a breakpoint set.\n\nClick the ● again to toggle it off.")'. However, the class docstring only mentions that clicking shows error messages for '?' symbols, not that it shows info for breakpoints. Also, the message says 'Click the ● again to toggle it off' but clicking the status column doesn't actually toggle breakpoints - this appears to be misleading user guidance.

---

#### code_vs_comment

**Description:** Comment in _on_status_click says 'show error message if clicked on ?' but code also handles breakpoint clicks

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Method docstring: 'Handle click on status column (show error message if clicked on ?).' But the implementation also shows info dialogs for breakpoints, not just error messages for '?' symbols.

---

#### code_vs_comment

**Description:** Regex pattern comment doesn't match actual pattern behavior

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
In _parse_line_number, the regex pattern is 'r'^(\d+)(?:\s|$)'' with comment '# Whitespace or end of string'. However, the pattern actually matches digits followed by whitespace OR end of string, but the comment could be clearer that it's an OR condition, not requiring whitespace before end of string.

---

#### code_vs_comment

**Description:** serialize_variable() comment says 'Don't add suffixes that were inferred from DEF statements' but implementation checks 'explicit_type_suffix' attribute

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment: '# Only add type suffix if it was explicit in the original source # Don't add suffixes that were inferred from DEF statements'. Code: 'if var.type_suffix and getattr(var, 'explicit_type_suffix', False):'. The comment implies the code knows about DEF statement inference, but the implementation just checks a boolean flag. The comment should clarify that the flag is set by the parser/type system to distinguish explicit vs inferred suffixes.

---

#### code_vs_comment

**Description:** serialize_line() comment mentions 'inline comment' spacing but implementation uses hardcoded 4 spaces

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment: '# Inline comment - preserve spacing, no colon'. Code: 'parts.append('    ' + stmt_text)'. The comment says 'preserve spacing' but the code uses a hardcoded 4-space indent. This is inconsistent - either the spacing should be preserved from the original source, or the comment should say 'use standard spacing' instead of 'preserve'.

---

#### documentation_inconsistency

**Description:** Module docstring lists 'Error message formatting and display' but some error formatting functions are not UI-agnostic

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Module docstring: 'This module contains UI-agnostic helper functions that can be used by any UI (CLI, Tk, Web, Curses). No UI-specific dependencies allowed.' However, functions like format_error_message() with 'mbasic_style' parameter and format_runtime_error() that format specific output strings are making UI presentation decisions. True UI-agnostic code would return structured error data, not formatted strings.

---

#### code_vs_documentation

**Description:** get_sort_key_function() docstring says it handles 'type' and 'value' but implementation treats them as defaults to 'name'

**Affected files:**
- `src/ui/variable_sorting.py`

**Details:**
Comment in else clause: '# Default to name sorting (includes old 'type' and 'value' for backwards compatibility)'. This suggests 'type' and 'value' were once valid sort modes, but they're not in get_variable_sort_modes(). The comment implies backwards compatibility but doesn't explain what the old behavior was or whether it's actually preserved.

---

#### code_vs_comment

**Description:** serialize_line() preserves 'RELATIVE indentation' but comment doesn't explain what happens when line number width changes

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment: '# Preserve RELATIVE indentation (spaces after line number) from original source # This ensures indentation survives RENUM when line numbers change width'. The code calculates relative_indent from the original source, but if the line number changes from '10' (2 chars) to '100' (3 chars), the absolute position of the code will shift. The comment claims indentation 'survives' but doesn't clarify whether this means visual alignment is preserved or just the space count.

---

#### documentation_inconsistency

**Description:** Different descriptions of current statement highlighting color

**Affected files:**
- `src/ui/web/codemirror5_editor.py`
- `src/ui/web/codemirror_editor.py`

**Details:**
CodeMirror5Editor docstring says 'Current statement highlighting (green background)' and set_current_statement docstring says 'Highlight current executing statement (green background)', while CodeMirrorEditor docstring says 'Current statement highlighting (green/blue background for step debugging)' and set_current_statement says 'Highlight current executing statement during step debugging' without specifying color. This creates ambiguity about the actual visual appearance.

---

#### code_vs_documentation

**Description:** Inconsistent method naming between CodeMirror5Editor and CodeMirrorEditor

**Affected files:**
- `src/ui/web/codemirror5_editor.py`
- `src/ui/web/codemirror_editor.py`

**Details:**
CodeMirrorEditor has both 'get_value()' and 'set_value()' methods in addition to the 'value' property, while CodeMirror5Editor only has the 'value' property. The docstring for CodeMirrorEditor.get_value() says 'Get current editor content (async)' but there's no async/await syntax, creating confusion about the API design pattern.

---

#### code_vs_comment

**Description:** get_cursor_position implementation doesn't match docstring

**Affected files:**
- `src/ui/web/codemirror5_editor.py`

**Details:**
CodeMirror5Editor.get_cursor_position() docstring says 'Returns: Dict with 'line' and 'column' keys (0-based)' but the implementation has a comment '# This would need async support, for now return placeholder' and always returns {'line': 0, 'column': 0}, which doesn't actually get the cursor position.

---

#### documentation_inconsistency

**Description:** Different module descriptions for CodeMirror versions

**Affected files:**
- `src/ui/web/codemirror5_editor.py`
- `src/ui/web/codemirror_editor.py`

**Details:**
CodeMirror5Editor module docstring says 'uses simple script tags instead of ES6 modules (avoiding the module loading conflicts of CodeMirror 6)' and class docstring says 'uses CodeMirror 5 (legacy version) which doesn't require ES6 module loading, making it compatible with NiceGUI's module system', while CodeMirrorEditor module docstring says 'This module provides a custom NiceGUI component wrapping CodeMirror 6' with no mention of module loading issues. This suggests CodeMirror 6 may have compatibility issues that aren't documented in its own file.

---

#### code_vs_comment

**Description:** Comment says 'Event handlers now handled through CodeMirror's on_change callback' but click and blur handlers are still registered separately

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~1050: Comment states '# Event handlers now handled through CodeMirror's on_change callback' followed by '# The _on_editor_change method (defined below) handles:' but then lines ~1057-1058 show: 'self.editor.on('click', self._on_editor_click, throttle=0.05)' and 'self.editor.on('blur', self._on_editor_blur)'. The note says 'click and blur handlers can still work' which contradicts the initial statement that handlers are 'now handled through on_change callback'.

---

#### code_vs_comment

**Description:** Comment references method 'defined below' but method definition is not shown in provided code

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~1051: Comment says '# The _on_editor_change method (defined below) handles:' but the _on_editor_change method is not present in the provided code snippet. This could indicate the comment is outdated or the code is incomplete.

---

#### code_internal_inconsistency

**Description:** Duplicate import statement for 're' module

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line 10: 'import re' and Line 16: 'import re' - The re module is imported twice at the top of the file.

---

#### code_vs_comment

**Description:** Comment says 'Create one interpreter for the session - don't create multiple!' but no code shown that would create multiple interpreters

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~972: Comment warns 'Create one interpreter for the session - don't create multiple!' but there's no visible code pattern in the provided snippet that would suggest multiple interpreters are being created. This comment may be outdated or addressing a non-obvious issue.

---

#### code_vs_comment

**Description:** Comment about 'per-client state' contradicts implementation using instance variables

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Line ~960: Comment says '# Per-client state (now instance variables instead of session storage)' which suggests a change was made from session storage to instance variables. However, the NiceGUI backend is instantiated per-page/session, so 'per-client' and 'instance variables' are effectively the same thing. The comment may be confusing or outdated from a refactoring.

---

#### code_vs_comment

**Description:** Inconsistent handling of execution timer cancellation

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _menu_run, the timer is cancelled at the start: 'if self.exec_timer: self.exec_timer.cancel()'. But in _menu_stop, it's also cancelled. However, in _execute_tick when halted, the timer is cancelled with 'if self.exec_timer: self.exec_timer.cancel(); self.exec_timer = None'. The pattern is inconsistent - sometimes setting to None, sometimes not.

---

#### code_vs_comment

**Description:** Comment about CP/M EOF marker handling in wrong location

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _save_editor_to_program, there's a comment about normalizing line endings and removing CP/M EOF markers (\x1a). The comment is detailed but the actual removal happens in a single line. However, in _handle_file_upload, there's no such normalization despite files potentially having these markers.

---

#### code_vs_comment

**Description:** Comment about KeyboardInterrupt handling references wrong location

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _execute_tick docstring: 'The KeyboardInterrupt handling is done at the top level in mbasic, which wraps start_web_ui() in a try/except.' This references external code not shown in the provided files, making it impossible to verify if this is accurate.

---

#### code_vs_comment

**Description:** Comment about placeholder handling is outdated for CodeMirror

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _on_editor_change(), comment says: 'Clear placeholder once user starts typing (no longer needed for CodeMirror) # CodeMirror doesn't use placeholder prop like textarea'. However, _on_paste() still has code: self.editor.props('placeholder=""') which contradicts the statement that CodeMirror doesn't use placeholder prop.

---

#### code_vs_comment

**Description:** Comment about state checking contradicts the code logic

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _execute_immediate(), comment says: 'Check if interpreter has work to do (after RUN statement) # No state checking - just ask the interpreter'. The comment 'No state checking' is confusing because the very next line does check has_work() which is a form of state checking.

---

#### code_vs_comment

**Description:** Comment about batch flush timing doesn't match code values

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _append_output() docstring: 'Updates are flushed every 50ms or after 100 updates'. However, code shows: 'if self.output_update_count >= 50' (not 100) and timer is 0.05 seconds (which is 50ms, correct). The '100 updates' in the docstring is wrong.

---

#### code_vs_comment

**Description:** Comment in _flush_output_batch contradicts the actual flush frequency

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment before flush check says: 'Flush immediately if batch is getting large (every 50 updates)'. But the code checks 'if self.output_update_count >= 50', meaning it flushes at 50 updates, not 'every 50 updates' (which would imply 50, 100, 150, etc.).

---

#### code_vs_comment

**Description:** Docstring for start() method is misleading about its usage

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
The start() method docstring says 'Start the UI' and 'NOTE: For web backend, use start_web_ui() module function instead. This method is not used for the web backend.' However, the method immediately raises NotImplementedError. The docstring should clearly state this is not implemented rather than suggesting it's a valid method that shouldn't be used.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut documentation format

**Affected files:**
- `docs/help/common/editor-commands.md`
- `docs/help/common/debugging.md`

**Details:**
editor-commands.md uses '**Ctrl+R**' format while debugging.md uses both '**Ctrl+R**' and '^R' formats interchangeably. For example, debugging.md Quick Start section uses '^R' but later sections use 'Ctrl+R'. This creates confusion about the actual key combination.

---

#### code_vs_comment

**Description:** Deprecated class still present with extensive implementation

**Affected files:**
- `src/ui/web_help_launcher.py`

**Details:**
WebHelpLauncher_DEPRECATED class (line 44) has comment 'Legacy class wrapper for compatibility' but contains full implementation with server management, MkDocs building, etc. If truly deprecated for compatibility, it should be a thin wrapper. The comment 'Legacy class removed - using direct web URL instead' (line 41) contradicts the presence of the full class implementation below it.

---

#### code_vs_documentation

**Description:** Settings dialog tabs not documented

**Affected files:**
- `src/ui/web/web_settings_dialog.py`
- `docs/help/common/debugging.md`

**Details:**
web_settings_dialog.py creates tabs for 'Editor' and 'Limits' settings (lines 40-41) but there's no documentation describing what settings are available in the Web UI settings dialog or how to access it. The debugging.md only mentions Variables and Stack windows for Web UI.

---

#### code_vs_comment

**Description:** Duplicate function comment but no duplicate found

**Affected files:**
- `src/ui/web_help_launcher.py`

**Details:**
Line 189 has comment '# Duplicate function removed - the simple version above is used' but there's no evidence of a duplicate function in the visible code. This comment may be outdated from a previous refactoring.

---

#### documentation_inconsistency

**Description:** Inconsistent help navigation instructions

**Affected files:**
- `docs/help/common/index.md`
- `docs/help/common/language.md`

**Details:**
index.md shows navigation with '**↑/↓** - Scroll up/down' and '**B** - Page up' while other help pages don't consistently show these navigation instructions. The language.md file only has '[Back to main help](index.md)' without navigation instructions.

---

#### documentation_inconsistency

**Description:** DEL character listed in two different sections with inconsistent formatting

**Affected files:**
- `docs/help/common/language/appendices/ascii-codes.md`

**Details:**
In ascii-codes.md, DEL (127/7F) appears both at the end of the 'Printable Characters (32-126)' table and in a separate 'Special Character: DEL' section. The printable characters section claims to cover 32-126 but includes 127. This is inconsistent as DEL (127) is technically not a printable character.

---

#### documentation_inconsistency

**Description:** Incomplete example code with ellipsis and unclear reference

**Affected files:**
- `docs/help/common/language/functions/cvi-cvs-cvd.md`

**Details:**
In cvi-cvs-cvd.md, the example shows: '70 FIELD #1,4 AS N$, 12 AS B$, •••' with ellipsis (•••) and then states 'See also MKI$r MKS$, MKD$, Section 3.25 and Appendix B.' The 'MKI$r' appears to be a typo (should be 'MKI$,'), and 'Section 3.25 and Appendix B' are vague references that don't correspond to the current documentation structure.

---

#### documentation_inconsistency

**Description:** Cross-reference formatting inconsistency

**Affected files:**
- `docs/help/common/language/functions/hex_dollar.md`
- `docs/help/common/language/functions/oct_dollar.md`

**Details:**
In hex_dollar.md, the example ends with 'See the OCT$ function for octal conversion.' This is plain text rather than a proper markdown link. The 'See Also' section properly links to oct_dollar.md, making this redundant and inconsistently formatted.

---

#### documentation_inconsistency

**Description:** Incomplete sentence fragment in example section

**Affected files:**
- `docs/help/common/language/functions/asc.md`

**Details:**
In asc.md, after the example code, there's a fragment: 'See the CHR$ function for ASCII-to-string conversion.' This appears to be leftover text that should either be removed (since CHR$ is already in the See Also section) or properly formatted.

---

#### documentation_inconsistency

**Description:** Incomplete example code

**Affected files:**
- `docs/help/common/language/functions/eof.md`

**Details:**
In eof.md, the example code ends abruptly at line 50 without showing the completion of the loop or line 100 that is referenced in line 30: '30 IF EOF(l) THEN 100'. This makes the example incomplete and potentially confusing.

---

#### documentation_inconsistency

**Description:** See Also section references non-standard function name

**Affected files:**
- `docs/help/common/language/functions/eof.md`

**Details:**
In eof.md, the See Also section lists '[LINE INPUT#](../statements/inputi.md)' but the link target 'inputi.md' doesn't match the standard naming convention. Should likely be 'line-input-hash.md' or similar.

---

#### documentation_inconsistency

**Description:** Typo in INKEY$ cross-reference description

**Affected files:**
- `docs/help/common/language/functions/inp.md`

**Details:**
In inp.md, the See Also section references INKEY$ with description 'Returns either a one-character string cont~ining a character' - contains typo 'cont~ining' instead of 'containing'. This same typo appears in peek.md and usr.md.

---

#### documentation_inconsistency

**Description:** Inconsistent spacing in example output

**Affected files:**
- `docs/help/common/language/functions/instr.md`

**Details:**
In instr.md example, the PRINT statement shows 'PRINT INSTR(X$,Y$) ;INSTR(4,X$,Y$)' with semicolon, but output shows '2 6' with space. The semicolon should produce no space between values.

---

#### documentation_inconsistency

**Description:** Inconsistent example formatting

**Affected files:**
- `docs/help/common/language/functions/int.md`

**Details:**
In int.md, examples show 'PRINT INT(99.89)' followed by '99' on next line with 'Ok' after, but other docs show output inline or with different formatting. Not a major issue but inconsistent style.

---

#### documentation_inconsistency

**Description:** Inconsistent example output formatting

**Affected files:**
- `docs/help/common/language/functions/left_dollar.md`

**Details:**
In left_dollar.md, example shows '30 PRINT B$' followed by 'BASIC' then 'Ok' on separate lines, while other docs show different output formatting patterns.

---

#### documentation_inconsistency

**Description:** Inconsistent example output formatting

**Affected files:**
- `docs/help/common/language/functions/len.md`

**Details:**
In len.md, example shows '20 PRINT LEN (X$)' followed by '16' then 'Ok' on separate lines with inconsistent spacing compared to other function examples.

---

#### documentation_inconsistency

**Description:** Inconsistent example output formatting

**Affected files:**
- `docs/help/common/language/functions/log.md`

**Details:**
In log.md, example shows 'PRINT LOG ( 45/7 )' followed by '1.86075' then 'Ok' with inconsistent spacing in function call compared to other examples.

---

#### documentation_inconsistency

**Description:** Inconsistent example output formatting

**Affected files:**
- `docs/help/common/language/functions/mid_dollar.md`

**Details:**
In mid_dollar.md, example shows 'LIST' command before the program listing, which is inconsistent with other function examples that don't show the LIST command.

---

#### documentation_inconsistency

**Description:** Incomplete and confusing See Also reference

**Affected files:**
- `docs/help/common/language/functions/mki_dollar-mks_dollar-mkd_dollar.md`

**Details:**
In mki_dollar-mks_dollar-mkd_dollar.md, the description ends with 'See also CVI, CVS, CVD, Section 3.9 and Appendix B. 3.27 OCT$ PRINT OCT$ (24) 30 Ok See the HEX $ function for hexadecimal conversion. 3.2S PEEK A=PEEK (&H5AOO)' which appears to be corrupted text from multiple sections merged together.

---

#### documentation_inconsistency

**Description:** Inconsistent example output formatting

**Affected files:**
- `docs/help/common/language/functions/oct_dollar.md`

**Details:**
In oct_dollar.md, two separate examples are shown with different RUN outputs, but formatting is inconsistent with spacing and line breaks.

---

#### documentation_inconsistency

**Description:** Inconsistent example output formatting

**Affected files:**
- `docs/help/common/language/functions/rnd.md`

**Details:**
In rnd.md, example shows '20 PRINT INT(RND*100);' followed by '24 30 31 51 5' with inconsistent spacing and line breaks compared to other examples.

---

#### documentation_inconsistency

**Description:** Incomplete example explanation

**Affected files:**
- `docs/help/common/language/functions/sgn.md`

**Details:**
In sgn.md, example shows 'ON SGN(X)+2 GOTO 100,200,300 branches to 100 if X is negative, 200 if X is 0 and 300 if X is positive.' - the explanation is run together with the code without proper formatting.

---

#### documentation_inconsistency

**Description:** Inconsistent example output formatting and typo

**Affected files:**
- `docs/help/common/language/functions/sin.md`

**Details:**
In sin.md, description contains 'COS(X)=SIN(X+3.l4l59/2) •' with '3.l4l59' (lowercase L instead of 1) and a bullet point at the end. Example output shows '.997495' with leading period.

---

#### documentation_inconsistency

**Description:** Inconsistent example output formatting

**Affected files:**
- `docs/help/common/language/functions/sqr.md`

**Details:**
In sqr.md, example shows tabular output with inconsistent spacing between columns compared to other examples.

---

#### documentation_inconsistency

**Description:** Incomplete example code

**Affected files:**
- `docs/help/common/language/functions/str_dollar.md`

**Details:**
In str_dollar.md, example shows '20 ON LEN(STR$(N» GOSUB 30,100,200,300,400,500' with double closing parentheses '»' which appears to be a typo or encoding issue.

---

#### documentation_inconsistency

**Description:** Typo in description

**Affected files:**
- `docs/help/common/language/functions/tan.md`

**Details:**
In tan.md, description contains 'TAN (X) is calculated in single preclslon' with typo 'preclslon' instead of 'precision'.

---

#### documentation_inconsistency

**Description:** Incomplete description reference

**Affected files:**
- `docs/help/common/language/functions/usr.md`

**Details:**
In usr.md, description ends with 'See Appendix x.' where 'x' should likely be a specific appendix letter or number.

---

#### documentation_inconsistency

**Description:** Typo in VAL function example - missing closing parenthesis

**Affected files:**
- `docs/help/common/language/functions/val.md`

**Details:**
In the Description section: 'For example, VAL (" -3) returns -3.' should be 'VAL (" -3") returns -3.'

---

#### documentation_inconsistency

**Description:** Incomplete example code in VAL function

**Affected files:**
- `docs/help/common/language/functions/val.md`

**Details:**
The example code is malformed: '10 READ NAME$,CITY$,STATE$,ZIP$
 20 IF VAL(ZIP$) <90000 OR VAL(ZIP$) >96699 THEN
 PRINT NAME$ TAB(25) "OUT OF STATE"
 30 IF VAL(ZIP$) >=90801 AND VAL(ZIP$) <=90815 THEN
 PRINT NAME$ TAB(25) "LONG BEACH"
 See the STR$ function for numeric to string
 conversion.' - Line 20 is missing THEN clause, line 30 is missing THEN clause, and there's a stray sentence at the end.

---

#### documentation_inconsistency

**Description:** Inconsistent formatting in AUTO example

**Affected files:**
- `docs/help/common/language/statements/auto.md`

**Details:**
The example shows 'AUTO 100,50      Generates line numbers 100,' with irregular spacing and formatting that doesn't match other examples in the documentation.

---

#### documentation_inconsistency

**Description:** Missing version information for CHAIN statement

**Affected files:**
- `docs/help/common/language/statements/chain.md`

**Details:**
CHAIN is marked as 'Versions: Disk' but other statements like CLEAR show 'Versions: 8K, Extended, Disk'. The version availability should be consistent across all statements.

---

#### documentation_inconsistency

**Description:** Inconsistent title formatting for cassette commands

**Affected files:**
- `docs/help/common/language/statements/cload.md`
- `docs/help/common/language/statements/csave.md`

**Details:**
CLOAD title is 'CLOAD THIS COMMAND IS NOT INCLUDED IN THE DEC VT180 VERSION' while CSAVE title is 'CSAVE THIS COMMAND IS NOT INCLUDED IN THE DEC VT180 VERSION' - both have the note in the title rather than in a separate section, which is inconsistent with other commands like VARPTR that use an 'Implementation Note' section.

---

#### documentation_inconsistency

**Description:** Incomplete example reference in CONT statement

**Affected files:**
- `docs/help/common/language/statements/cont.md`

**Details:**
The example section states 'See example Section 2.61, STOP.' but doesn't provide an actual code example, which is inconsistent with other statements that provide inline examples.

---

#### documentation_inconsistency

**Description:** Inconsistent spacing in CSAVE example

**Affected files:**
- `docs/help/common/language/statements/csave.md`

**Details:**
The example shows 'CSAVE "TIMER"
                Saves the program currently in memory on
                cassette under filename "T".' with irregular indentation that doesn't match other examples.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology in DATA remarks

**Affected files:**
- `docs/help/common/language/statements/data.md`

**Details:**
The remarks section uses 'COmmand level' with inconsistent capitalization (capital O in 'COmmand') which appears to be a typo.

---

#### documentation_inconsistency

**Description:** Inconsistent spacing in DELETE example

**Affected files:**
- `docs/help/common/language/statements/delete.md`

**Details:**
The example shows 'DELETE 40         Deletes line 40' with irregular spacing that doesn't match other examples in the documentation.

---

#### documentation_inconsistency

**Description:** Incomplete example in DIM statement

**Affected files:**
- `docs/help/common/language/statements/dim.md`

**Details:**
The example shows '10 DIM A(20)
             20 FOR 1=0 TO 20
             30 READ A(I)' with irregular indentation and uses '1' (number one) instead of 'I' (letter I) in the FOR statement, which is likely a typo.

---

#### documentation_inconsistency

**Description:** Inconsistent cross-reference format for ERR/ERL variables

**Affected files:**
- `docs/help/common/language/statements/end.md`
- `docs/help/common/language/statements/error.md`

**Details:**
end.md does not reference ERR/ERL variables in 'See Also' section, while error.md references them as '../functions/err-erl.md'. However, err-erl-variables.md shows these are documented as statements (type: statement), not functions. The path '../functions/err-erl.md' appears incorrect.

---

#### documentation_inconsistency

**Description:** Inconsistent cross-reference to CVI/CVS/CVD functions

**Affected files:**
- `docs/help/common/language/statements/field.md`
- `docs/help/common/language/statements/get.md`

**Details:**
field.md references 'CVI, CVS, CVD' as '../functions/cvi-cvs-cvd.md' while get.md also references the same path. Both use the same format, so this is consistent, but should verify the actual file exists at that location.

---

#### documentation_inconsistency

**Description:** FILES statement missing from index categorization

**Affected files:**
- `docs/help/common/language/statements/files.md`
- `docs/help/common/language/statements/index.md`

**Details:**
files.md documents the FILES statement, but it does not appear in the 'File Management' category in index.md. The index lists CLOAD, CSAVE, KILL, LOAD, MERGE, NAME, SAVE but omits FILES.

---

#### documentation_inconsistency

**Description:** Inconsistent naming of modern extension commands in index

**Affected files:**
- `docs/help/common/language/statements/helpsetting.md`
- `docs/help/common/language/statements/index.md`

**Details:**
index.md lists 'HELP SET' but the actual file is helpsetting.md with title 'HELPSETTING' (one word). Similarly, 'SHOW SETTINGS' vs showsettings.md. The index uses two-word names while the actual commands appear to be single words.

---

#### documentation_inconsistency

**Description:** Missing HELPSETTING, SETSETTING, SHOWSETTINGS in alphabetical listing

**Affected files:**
- `docs/help/common/language/statements/index.md`

**Details:**
index.md lists modern extensions (HELP SET, LIMITS, SET, SHOW SETTINGS) in the category section but none of these appear in the alphabetical listing sections (H, S). Only LIMITS has a dedicated section reference.

---

#### documentation_inconsistency

**Description:** Inconsistent cross-reference to INPUT$ function

**Affected files:**
- `docs/help/common/language/statements/input.md`
- `docs/help/common/language/statements/line-input.md`

**Details:**
line-input.md references INPUT$ as '../functions/input_dollar.md' in See Also section, but input.md does not reference INPUT$ at all, even though it would be relevant for reading character input.

---

#### documentation_inconsistency

**Description:** Duplicate documentation for LINE INPUT# with different filenames

**Affected files:**
- `docs/help/common/language/statements/inputi.md`
- `docs/help/common/language/statements/input_hash.md`

**Details:**
Both inputi.md and input_hash.md appear to document file input statements. inputi.md documents 'LINE INPUT#' while input_hash.md documents 'INPUT#'. The title in inputi.md is 'LINE INPUT#' but the filename suggests it might be for a different statement.

---

#### documentation_inconsistency

**Description:** Malformed documentation structure in list.md

**Affected files:**
- `docs/help/common/language/statements/list.md`

**Details:**
list.md has 'Format 2:' mentioned in the version line and empty Remarks section. The Examples section contains what should be in Remarks. The structure appears corrupted or improperly formatted.

---

#### documentation_inconsistency

**Description:** Implementation notes inconsistency

**Affected files:**
- `docs/help/common/language/statements/llist.md`
- `docs/help/common/language/statements/lprint-lprint-using.md`

**Details:**
Both llist.md and lprint-lprint-using.md have 'Implementation Note' sections stating features are not implemented. However, the formatting and wording differ slightly. llist.md says 'Statement is parsed but no listing is sent to a printer' while lprint says 'Statement is parsed but no output is sent to a printer'. Should be consistent.

---

#### documentation_inconsistency

**Description:** Inconsistent cross-reference format for MKI$/MKS$/MKD$ functions

**Affected files:**
- `docs/help/common/language/statements/lset.md`
- `docs/help/common/language/statements/field.md`

**Details:**
lset.md references 'MKI$, MKS$, MKD$' as '../functions/mki_dollar-mks_dollar-mkd_dollar.md' while field.md references the same functions with the same path. The underscore vs dollar sign in filename should be verified for consistency.

---

#### documentation_inconsistency

**Description:** MID$ assignment documentation has inconsistent example output

**Affected files:**
- `docs/help/common/language/statements/mid-assignment.md`

**Details:**
Example 2 shows: '10 B$ = "ABCDEFGH"
20 MID$(B$, 3) = "XY"
30 PRINT B$
RUN
ABXYEFGH'. This output is incorrect. If MID$(B$, 3) = "XY" replaces starting at position 3, the result should be 'ABXYEFGH' (replacing 'CD' with 'XY'), but the output shows 'ABXYEFGH' which is correct. However, the documentation states 'only the available characters are replaced' which is ambiguous about what happens to characters after the replacement string ends.

---

#### documentation_inconsistency

**Description:** NAME statement example has formatting issues

**Affected files:**
- `docs/help/common/language/statements/name.md`

**Details:**
The example section shows: 'Ok
              NAME "ACCTS" AS "LEDGER"
              Ok
              In this example, the file that was
              formerly named ACCTS will now be named LEDGER.' The formatting with excessive spaces and the explanation being part of the example block is inconsistent with other documentation files.

---

#### documentation_inconsistency

**Description:** NULL statement example has formatting issues and unclear syntax

**Affected files:**
- `docs/help/common/language/statements/null.md`

**Details:**
Example shows: 'Ok
              NULL 2
              Ok
              100 INPUT X
              200 IF X<50 GOTO 800
              Two null characters will be printed after each
              line.' The formatting is inconsistent, and the example doesn't demonstrate the NULL statement's effect clearly.

---

#### documentation_inconsistency

**Description:** POKE documentation mentions 8K version limitations inconsistently

**Affected files:**
- `docs/help/common/language/statements/poke.md`

**Details:**
Documentation states: 'In the 8K version, I must be less than 32768. In the Extended and Disk versions, I must be in the range 0 to 65536.' Then adds: 'With the 8K version, data may be POKEd into memory locations above 32768 by supplying a negative number for I.' This is contradictory - first it says I must be less than 32768, then explains how to POKE above 32768.

---

#### documentation_inconsistency

**Description:** RANDOMIZE example has excessive formatting spaces

**Affected files:**
- `docs/help/common/language/statements/randomize.md`

**Details:**
The example section has inconsistent spacing: '10 RANDOMIZE
             20 FOR 1=1 TO 5
             30 PRINT RND;
             40 NEXT I
             RUN
             Random Number Seed (-32768    to 32767)? 3     (user
             types 3)' with many extra spaces that are inconsistent with other documentation.

---

#### documentation_inconsistency

**Description:** READ documentation has inconsistent variable naming in remarks

**Affected files:**
- `docs/help/common/language/statements/read.md`

**Details:**
Remarks section mentions 'READ statement variables' and 'variables in the list' but doesn't consistently use terminology. Also states 'Variables in the list may be subscripted' but doesn't explain this is referring to array elements clearly until the next sentence.

---

#### documentation_inconsistency

**Description:** REM example has formatting issues and uses tilde instead of apostrophe

**Affected files:**
- `docs/help/common/language/statements/rem.md`

**Details:**
Example shows: '120 FOR I=l TO 20     ~CALCULATE   AVERAGE VELOCITY' using a tilde (~) instead of an apostrophe (') for the comment marker. The documentation states 'remarks may be added to the end of a line by preceding the remark with a single quotation mark' but the example uses a tilde.

---

#### documentation_inconsistency

**Description:** RESUME documentation references non-existent appendix

**Affected files:**
- `docs/help/common/language/statements/resume.md`

**Details:**
Documentation states 'See [Error Codes](../appendices/error-codes.md) for complete list.' but this file path is not provided in the documentation set, suggesting a missing reference or incorrect path.

---

#### documentation_inconsistency

**Description:** RESUME documentation references test files not in documentation set

**Affected files:**
- `docs/help/common/language/statements/resume.md`

**Details:**
Documentation mentions 'Test file: `tests/test_resume.bas`, `tests/test_resume2.bas`, `tests/test_resume3.bas`' but these test files are not part of the provided documentation, suggesting either missing files or documentation that should be removed.

---

#### documentation_inconsistency

**Description:** Inconsistent description of file closing behavior

**Affected files:**
- `docs/help/common/language/statements/stop.md`
- `docs/help/common/language/statements/system.md`

**Details:**
stop.md states 'Unlike the END statement, the STOP statement does not close files.' However, system.md states 'When SYSTEM is executed: All open files are closed'. The END statement behavior regarding file closing should be consistent across all related documentation.

---

#### documentation_inconsistency

**Description:** Variable name significance length inconsistency

**Affected files:**
- `docs/help/common/language/variables.md`
- `docs/help/common/settings.md`

**Details:**
variables.md states 'Are limited to 40 characters (only first 2 are significant)' and 'Only the first 2 characters are significant. Variables AB, ABC, and ABCDEF are all the same variable.' However, settings.md mentions 'variables.case_conflict' setting with options like 'prefer_mixed' for 'camelCase', which would be meaningless if only 2 characters are significant.

---

#### documentation_inconsistency

**Description:** WRITE statement documentation split across two files with overlapping content

**Affected files:**
- `docs/help/common/language/statements/write.md`
- `docs/help/common/language/statements/writei.md`

**Details:**
write.md documents 'WRITE [<list of expressions>]' for terminal output, while writei.md documents 'WRITE #<file number>, <list of expressions>' for file output. The file naming (writei.md) and organization suggests these should be consolidated or cross-referenced more clearly.

---

#### documentation_inconsistency

**Description:** Inconsistent statement naming in title vs filename

**Affected files:**
- `docs/help/common/language/statements/tron-troff.md`

**Details:**
The file is named 'tron-troff.md' but the title is 'TRON/TROFF' using a slash instead of hyphen. This inconsistency could cause confusion in cross-references.

---

#### documentation_inconsistency

**Description:** Inconsistent alias documentation format

**Affected files:**
- `docs/help/common/language/statements/while-wend.md`

**Details:**
while-wend.md has 'aliases: [while-wend]' in frontmatter, which is redundant since the filename is already 'while-wend.md'. This suggests either the alias system is misunderstood or the alias should point to alternative names.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for file system differences

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/extensions.md`

**Details:**
compatibility.md has a section '2. File System Differences' that discusses CLI/Tk/Curses vs Web UI. extensions.md has '💾 Enhanced File Handling' that discusses similar topics but uses different terminology and organization. Both cover the same ground but present it differently.

---

#### documentation_inconsistency

**Description:** Inconsistent WIDTH statement documentation

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/features.md`

**Details:**
compatibility.md states 'WIDTH is parsed for compatibility but performs no operation. Terminal width is controlled by the UI or OS. The "WIDTH LPRINT" syntax is not supported.' features.md doesn't mention WIDTH at all in its comprehensive feature list, despite it being a parsed statement.

---

#### documentation_inconsistency

**Description:** Installation path inconsistency

**Affected files:**
- `docs/help/mbasic/getting-started.md`

**Details:**
getting-started.md shows 'git clone https://github.com/avwohl/mbasic.git' but doesn't verify this is the actual repository URL. This could be a placeholder or outdated URL.

---

#### documentation_inconsistency

**Description:** Inconsistent default UI documentation

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
features.md lists 'Curses UI (Default)' as the default interface. getting-started.md also states 'Start MBASIC without arguments for the full-screen editor' and shows 'mbasic' launching Curses UI. However, the command examples show 'mbasic --ui curses' as an alternative, which is consistent. Both docs agree on the default.

---

#### documentation_inconsistency

**Description:** Variables Window availability inconsistency

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/cli/variables.md`

**Details:**
cli/variables.md states 'Curses UI - Full-screen terminal with Variables Window (Ctrl+W)' suggesting it's available, while feature-reference.md confirms this. However, cli/variables.md also says 'The CLI does not have a Variables Window feature' which is correct for CLI but the phrasing could be clearer about which UIs do have it.

---

#### documentation_inconsistency

**Description:** Inconsistent function count

**Affected files:**
- `docs/help/ui/cli/index.md`
- `docs/help/mbasic/index.md`

**Details:**
cli/index.md states 'Functions - All 40 functions' while mbasic/index.md doesn't specify a count. This could become inconsistent if the actual number differs.

---

#### documentation_inconsistency

**Description:** Inconsistent error code count

**Affected files:**
- `docs/help/ui/cli/index.md`
- `docs/help/mbasic/index.md`

**Details:**
cli/index.md states 'Error Codes - All 68 error codes' while mbasic/index.md doesn't specify a count. This could become inconsistent if the actual number differs.

---

#### documentation_inconsistency

**Description:** Sort Lines feature description incomplete

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`

**Details:**
feature-reference.md mentions 'Sort Lines: Lines are automatically kept in numerical order. Manual sorting is available if needed.' but doesn't document how to manually sort or when you would need to, given that it's automatic.

---

#### documentation_inconsistency

**Description:** Document describes historical implementation but unclear if current implementation matches

**Affected files:**
- `docs/help/mbasic/implementation/string-allocation-and-garbage-collection.md`

**Details:**
The string-allocation-and-garbage-collection.md document extensively describes 'CP/M era Microsoft BASIC-80 (MBASIC)' historical implementation with O(n²) complexity, but doesn't clearly state whether the current Python implementation replicates this behavior or uses a modern approach. The 'Implementation for Modern Emulation' section suggests this is guidance for implementers, not a description of what's actually implemented.

---

#### documentation_inconsistency

**Description:** Placeholder documentation

**Affected files:**
- `docs/help/ui/common/running.md`

**Details:**
running.md is marked as 'PLACEHOLDER - Documentation in progress' and provides minimal information. This is inconsistent with the completeness of other documentation files.

---

#### documentation_inconsistency

**Description:** Inconsistent description of breakpoint management capabilities

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/debugging.md`

**Details:**
features.md under 'Breakpoints' says 'Currently Implemented: Line breakpoints (toggle via Run menu), Clear all breakpoints, Visual indicators in editor' and 'Management: Toggle via Run menu → Toggle Breakpoint, Clear all via Run menu → Clear All Breakpoints, Persistent within session'. debugging.md says the same but adds more detail about planned features. The 'Persistent within session' claim in features.md is not mentioned in debugging.md, creating uncertainty about whether breakpoints actually persist.

---

#### documentation_inconsistency

**Description:** Keyboard shortcut notation inconsistency

**Affected files:**
- `docs/help/ui/tk/tips.md`
- `docs/help/ui/tk/workflows.md`

**Details:**
tips.md uses template notation like '{{kbd:smart_insert}}', '{{kbd:toggle_variables}}', '{{kbd:run_program}}', etc. workflows.md uses the same notation. However, these templates are never defined or explained in the documents, and it's unclear what actual keyboard shortcuts these represent. This makes the tips unusable without external reference.

---

#### documentation_inconsistency

**Description:** File format support lists differ

**Affected files:**
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/features.md`

**Details:**
getting-started.md under 'Opening a File' says: 'Click to select a .BAS or .TXT file from your computer'. features.md under 'Format Support' lists 'Input Formats: .BAS files, .TXT files, Tokenized BASIC, ASCII text' and 'Output Formats: Standard .BAS, Formatted text, Tokenized format, PDF export'. The getting-started.md is more limited and doesn't mention tokenized BASIC or PDF export, suggesting features.md may be aspirational rather than current.

---

#### documentation_inconsistency

**Description:** Keyboard shortcut for opening settings dialog is vague

**Affected files:**
- `docs/help/ui/tk/settings.md`

**Details:**
Tk settings.md under 'Opening the Settings Dialog' lists 'Methods: 1. Menu: File → Settings, 2. Keyboard shortcut: (check your system's menu)'. The instruction to 'check your system's menu' is unhelpful and suggests the documentation doesn't know what the actual shortcut is. This should either specify the shortcut or state that none exists.

---

#### documentation_inconsistency

**Description:** Keyboard shortcut availability is uncertain

**Affected files:**
- `docs/help/ui/web/settings.md`

**Details:**
Web settings.md under 'Opening Settings' lists 'Use keyboard shortcut: Ctrl+, (if enabled)'. The phrase '(if enabled)' creates uncertainty - is this shortcut always available, configurable, or not implemented? No other documentation explains how to enable/disable this shortcut.

---

#### documentation_inconsistency

**Description:** Collaboration features listed but likely not implemented

**Affected files:**
- `docs/help/ui/web/features.md`

**Details:**
features.md under 'Collaboration' lists: 'Sharing: Share via link, Read-only mode, Collaborative editing, Live output sharing' and 'Version Control: Local history, Snapshot saves, Diff viewer'. These are sophisticated features that would require significant infrastructure. No other documentation mentions these features, and they seem inconsistent with the 'browser localStorage' architecture described elsewhere. These are likely aspirational features incorrectly listed as current capabilities.

---

#### documentation_inconsistency

**Description:** Browser console commands listed without context

**Affected files:**
- `docs/help/ui/web/features.md`

**Details:**
features.md under 'Browser Console Commands' lists JavaScript commands like 'mbasic.getProgram()', 'mbasic.setVariable()', etc. However, no other documentation explains that these exist, how to use them, or what the 'mbasic' global object is. This appears to be developer/debug functionality incorrectly documented as a user feature.

---

#### documentation_inconsistency

**Description:** Inconsistent program count in library statistics

**Affected files:**
- `docs/library/index.md`
- `docs/library/business/index.md`
- `docs/library/data_management/index.md`
- `docs/library/demos/index.md`
- `docs/library/education/index.md`
- `docs/library/electronics/index.md`
- `docs/library/games/index.md`
- `docs/library/ham_radio/index.md`
- `docs/library/telecommunications/index.md`
- `docs/library/utilities/index.md`

**Details:**
docs/library/index.md states 'Total Programs: 114+' but counting all programs listed across all category index files yields a different number. The '+' suggests approximation but the exact count should be verifiable from the category files.

---

#### documentation_inconsistency

**Description:** Missing 'Incompatible' category referenced in documentation

**Affected files:**
- `docs/library/index.md`

**Details:**
docs/library/index.md states under Notes: 'Programs in the "Incompatible" category require CP/M-specific features or graphics hardware' but no 'Incompatible' category is listed in the Categories section or linked anywhere in the library index.

---

#### documentation_inconsistency

**Description:** Missing contribution guidelines link

**Affected files:**
- `docs/library/index.md`

**Details:**
docs/library/index.md states 'Have a classic BASIC program to add? See our contribution guidelines in the project repository.' but no link or path to the contribution guidelines is provided.

---

#### documentation_inconsistency

**Description:** Missing bug report link

**Affected files:**
- `docs/library/index.md`

**Details:**
docs/library/index.md states '⚠️ **Important:** These programs have had minimal testing by humans. If you encounter issues, please submit a bug report (link coming soon).' The link is marked as 'coming soon' which is incomplete documentation.

---

#### documentation_inconsistency

**Description:** Incomplete debugger support description

**Affected files:**
- `docs/help/ui/web/web-interface.md`

**Details:**
web-interface.md states under Limitations: 'Limited debugger support (basic breakpoints only via Run menu)' but the Run Menu section only lists 'Run Program' and 'Stop' with no mention of breakpoints or debugger features.

---

#### documentation_inconsistency

**Description:** Settings dialog mentioned but not documented

**Affected files:**
- `docs/help/ui/web/web-interface.md`

**Details:**
web-interface.md mentions 'Use the Settings dialog (⚙️ icon) to change the increment or disable auto-numbering entirely' but there is no Settings menu item listed in the Menu Functions section, and no description of where the ⚙️ icon appears in the interface.

---

#### documentation_inconsistency

**Description:** Malformed game entry with tab characters

**Affected files:**
- `docs/library/games/index.md`

**Details:**
In games/index.md, one entry reads '### \t\tHANGMAN.BAS\tDEMO' with visible tab escape sequences, while all other entries follow the format '### GameName'. This appears to be a formatting error.

---

#### documentation_inconsistency

**Description:** Duplicate installation documentation with different content

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`
- `docs/user/INSTALLATION.md`

**Details:**
INSTALLATION.md is marked as 'PLACEHOLDER - Documentation in progress' and refers to 'docs/dev/INSTALLATION_FOR_DEVELOPERS.md', but INSTALL.md contains complete installation instructions. This creates confusion about which is the canonical installation guide.

---

#### documentation_inconsistency

**Description:** Inconsistent Web UI dependency information

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
In 'Installation Requirements' section, Web UI shows 'pip install webbrowser' but webbrowser is a standard library module in Python and doesn't need installation. The comment 'Optional: for auto-open browser' is misleading.

---

#### documentation_inconsistency

**Description:** Reference to non-existent files in examples section

**Affected files:**
- `docs/user/QUICK_REFERENCE.md`

**Details:**
QUICK_REFERENCE.md references 'test_continue.bas', 'demo_continue.bas', and 'test_continue_manual.sh' in the Examples section, but these files are not mentioned in any other documentation and their location is not specified.

---

#### documentation_inconsistency

**Description:** References to documentation files that may not exist

**Affected files:**
- `docs/user/QUICK_REFERENCE.md`

**Details:**
QUICK_REFERENCE.md references 'DEBUGGER_COMMANDS.md', 'CONTINUE_FEATURE.md', 'BREAKPOINT_SUMMARY.md', and 'HELP_SYSTEM_SUMMARY.md' in the 'More Information' section, but these files are not present in the provided documentation set.

---

#### documentation_inconsistency

**Description:** Reference to non-existent documentation file

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
SETTINGS_AND_CONFIGURATION.md references 'docs/user/TK_UI_QUICK_START.md' in the 'Related Documentation' section, but this file is not present in the provided documentation set.

---

#### documentation_inconsistency

**Description:** Reference to developer documentation file

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
SETTINGS_AND_CONFIGURATION.md references 'docs/dev/KEYWORD_CASE_HANDLING_TODO.md' which is a developer document, but this is in user documentation. The file may not exist or may be in a different location.

---

#### documentation_inconsistency

**Description:** Inconsistent command syntax in examples

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
Most examples use 'python3 mbasic' but some use './mbasic'. The troubleshooting section mentions 'chmod +x mbasic' and './mbasic' suggesting it's an executable script, but installation instructions treat it as a Python module.

---

#### documentation_inconsistency

**Description:** Find/Replace availability inconsistency

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
TK_UI_QUICK_START.md states 'Ctrl+H' for 'Find and replace' as an essential keyboard shortcut. UI_FEATURE_COMPARISON.md shows 'Find/Replace' as '✅' for Tk and '❌' for Web, but also lists under 'Recently Added (2025-10-29)' as '✅ Tk: Find/Replace functionality' and under 'Coming Soon' as '⏳ Find/Replace in Web UI'. The comparison table shows it's not available in CLI or Curses, which is consistent, but the 'Recently Added' section suggests this is a new feature that may not be fully documented.

---

#### documentation_inconsistency

**Description:** Save keyboard shortcut inconsistency between Tk and Curses

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md shows 'Ctrl+S' for 'Save file' in Tk UI. keyboard-shortcuts.md shows 'Ctrl+V' for 'Save program' in Curses UI. This is a legitimate difference between UIs but the inconsistency in using Ctrl+S vs Ctrl+V for the same operation could be confusing.

---

#### documentation_inconsistency

**Description:** Step execution keyboard shortcut conflict

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`
- `docs/user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md shows 'Ctrl+T' as 'Step through code (next statement)' and 'Ctrl+L' as 'Step through code (next line)' for Tk UI. keyboard-shortcuts.md shows 'Ctrl+K' as 'Step Line' and 'Ctrl+T' as 'Step Statement' for Curses UI. While Ctrl+T is consistent for statement stepping, line stepping uses different keys (Ctrl+L vs Ctrl+K).

---

#### documentation_inconsistency

**Description:** Duplicate help shortcut listings in Curses documentation

**Affected files:**
- `docs/user/keyboard-shortcuts.md`

**Details:**
keyboard-shortcuts.md lists help shortcuts twice: '^F' as 'This help' under 'Global Commands' and 'Ctrl+H/F1' under 'Help' in the same section. It's unclear if both ^F and Ctrl+H trigger help, or if they do different things.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for Variables window

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
TK_UI_QUICK_START.md uses multiple terms: 'Variables window' (Ctrl+V), 'Variables & Resources window' (Ctrl+W), and 'Variables Window' (in section headers). It's unclear if Ctrl+V and Ctrl+W open different windows or the same window with different content.

---


## Summary

- Total issues found: 737
- Code/Comment conflicts: 253
- Other inconsistencies: 484
