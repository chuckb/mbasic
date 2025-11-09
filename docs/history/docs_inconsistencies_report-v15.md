# Enhanced Consistency Report (Code + Documentation)

Generated: 2025-11-09 11:35:27
Analyzed: Source code (.py, .json) and Documentation (.md)

## 🔧 Code vs Comment Conflicts


## 📋 General Inconsistencies

### 🔴 High Severity

#### Documentation inconsistency

**Description:** Contradictory documentation about FileIO.load_file() return value and usage pattern

**Affected files:**
- `src/file_io.py`
- `src/editing/manager.py`

**Details:**
src/file_io.py docstring says:
"FileIO.load_file() returns raw file content (string), caller passes to ProgramManager"

But src/editing/manager.py docstring says:
"Note: ProgramManager.load_from_file() returns (success, errors) tuple where errors is a list of (line_number, error_message) tuples for direct UI error reporting, while FileIO.load_file() returns raw file text. These serve different purposes: ProgramManager integrates with the editor and provides error details, FileIO provides raw file content for the LOAD command to parse."

The inconsistency: file_io.py says "caller passes to ProgramManager" but ProgramManager.load_from_file() uses Python's open() directly, not FileIO.load_file(). The documented integration pattern doesn't match the implementation.

---

#### Documentation inconsistency

**Description:** Conflicting information about which abstraction handles which operations

**Affected files:**
- `src/file_io.py`
- `src/filesystem/__init__.py`

**Details:**
src/file_io.py says:
"FileSystemProvider (src/filesystem/base.py) - Runtime file I/O (OPEN/CLOSE/INPUT#/PRINT#)
- Also provides: list_files() and delete() for runtime use within programs"

But src/filesystem/__init__.py only exports:
'FileHandle', 'FileSystemProvider', 'RealFileSystemProvider', 'SandboxedFileSystemProvider'

There's no indication in filesystem/__init__.py that FileSystemProvider has list_files() or delete() methods. The documentation in file_io.py claims these methods exist, but they're not documented in the filesystem module itself. This needs verification against src/filesystem/base.py (not provided).

---

#### code_vs_comment

**Description:** Module docstring claims immediate mode statements are 'parsed as BASIC statements', but some commands have special handling that bypasses parser

**Affected files:**
- `src/interactive.py`

**Details:**
Module docstring at line ~5 states:
'- Direct commands: AUTO, EDIT, HELP (handled specially, not parsed as BASIC statements)
- Immediate mode statements: RUN, LIST, SAVE, LOAD, NEW, MERGE, FILES, SYSTEM, DELETE, RENUM, etc.
  (parsed as BASIC statements and executed in immediate mode)'

However, in execute_command() at line ~200, several commands are handled directly without going through the parser:
- AUTO (line ~205)
- EDIT (line ~207)
- HELP (line ~209)

But the comment at line ~211 states:
'# Everything else (including LIST, DELETE, RENUM, FILES, RUN, LOAD, SAVE, MERGE, SYSTEM, NEW, PRINT, etc.)
# goes through the real parser as immediate mode statements'

This is inconsistent with the actual implementation. Looking at the code, commands like LIST, DELETE, RENUM are called directly (cmd_list, cmd_delete, cmd_renum) from execute_immediate(), not parsed as BASIC statements. The module docstring's claim that these are 'parsed as BASIC statements' appears incorrect.

---

#### code_vs_comment

**Description:** Comment about RUN without args says 'halted=True to stop current execution' but doesn't explain restart mechanism

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1550 states:
# In non-interactive context, restart from beginning
# Note: RUN without args sets halted=True to stop current execution.
# The caller (e.g., UI tick loop) should detect halted=True and restart
# execution from the beginning if desired. This is different from
# RUN line_number which sets halted=False to continue execution inline.

This comment describes the behavior but creates an inconsistency: it says the caller 'should detect halted=True and restart execution from the beginning if desired', but doesn't specify HOW the caller knows this is a RUN-initiated halt vs. an END-initiated halt or error halt. The code sets halted=True but provides no mechanism for the caller to distinguish between different halt reasons. This could lead to unexpected behavior where END also causes a restart.

---

#### code_vs_comment

**Description:** serialize_let_statement docstring claims it 'ALWAYS outputs the implicit assignment form (A=5) without the LET keyword' but this contradicts the LetStatementNode's purpose and may not match user expectations for position preservation.

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring states: 'LetStatementNode represents both explicit LET statements and implicit assignments in the AST. However, this serializer ALWAYS outputs the implicit assignment form (A=5) without the LET keyword, regardless of whether the original source used LET.

This is because:
- The AST doesn\'t track whether LET was originally present
- LET is optional in MBASIC and functionally equivalent to implicit assignment
- Both forms use the same AST node type for consistency throughout the codebase'

However, the module docstring says: 'Serializes AST nodes back to source text while attempting to preserve original token positions and spacing.'

If the goal is position preservation, losing the LET keyword contradicts this goal. The AST should track whether LET was present if position preservation is a design goal.

---

#### code_vs_comment

**Description:** Token dataclass docstring describes convention for original_case vs original_case_keyword but implementation doesn't enforce it

**Affected files:**
- `src/tokens.py`

**Details:**
Token dataclass docstring states:
'Note: By convention, these fields are used for different token types:
- original_case: For IDENTIFIER tokens (user variables) - preserves what user typed
- original_case_keyword: For keyword tokens - stores policy-determined display case

The dataclass does not enforce this convention (both fields can technically be set on the same token) to allow implementation flexibility.'

This is a design smell - having two fields with overlapping purposes that rely on convention rather than type safety. The comment acknowledges this but doesn't explain why this design was chosen over alternatives like:
1. A single original_case field used for both
2. Separate Token subclasses (KeywordToken, IdentifierToken)
3. A union type for the original_case field

---

#### Code vs Documentation inconsistency

**Description:** STEP command behavior differs between implementation and keybindings documentation

**Affected files:**
- `src/ui/cli_debug.py`
- `src/ui/cli_keybindings.json`

**Details:**
cli_debug.py cmd_step() docstring: "Executes a single statement (not a full line). If a line contains multiple statements separated by colons, each statement is executed separately. This implements statement-level stepping similar to the curses UI 'Step Statement' command (Ctrl+T)."

cli_keybindings.json: "step": {"keys": ["STEP"], "description": "Step to next statement"}

However, curses_keybindings.json shows TWO different step commands:
- "step": Ctrl+T - "Step statement (execute one statement)"
- "step_line": Ctrl+K - "Step Line (execute all statements on current line)"

The CLI only implements statement-level stepping (STEP command) but has no equivalent to curses' line-level stepping (Ctrl+K).

---

#### Code vs Documentation inconsistency

**Description:** SHOW SETTINGS and SET commands documented but implementation not shown

**Affected files:**
- `src/ui/cli_keybindings.json`

**Details:**
cli_keybindings.json documents:
- "show_settings": "SHOW SETTINGS" - "View all settings or filter by pattern (e.g., SHOW SETTINGS \"auto\")"
- "set_setting": "SET \"setting\" value" - "Change a setting (e.g., SET \"editor.auto_number_start\" 100)"

However, these commands are not implemented in cli.py or cli_debug.py. The CLIBackend class doesn't have cmd_show_settings() or cmd_set() methods, and InteractiveMode (which it wraps) is not shown to have these commands either.

---

#### code_vs_comment

**Description:** STATUS: UNUSED comment for _create_toolbar() contradicts its actual implementation status

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~290 says:
STATUS: UNUSED - not called anywhere in current implementation.

The toolbar was removed from the UI in favor of Ctrl+U menu for better keyboard
navigation. This fully-implemented method is retained for reference in case toolbar
functionality is desired in the future. Can be safely removed if no plans to restore.

However, the method is fully implemented with working button callbacks (line ~295-335). The comment suggests it's dead code that 'can be safely removed', but if it's truly unused and removable, it should be removed rather than kept with a comment. If it's kept for reference, the comment should clarify this is intentional technical debt.

---

#### code_vs_comment

**Description:** Comment in _sync_program_to_runtime claims PC is reset to halted when paused_at_breakpoint=True to prevent accidental resumption, but this contradicts the stated behavior that interpreter's state already has correct PC

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment states: "# When paused_at_breakpoint=True, we reset PC to halted to prevent accidental
# resumption. When the user continues from a breakpoint (via _debug_continue),
# the interpreter's state already has the correct PC and simply clears the halted flag."

This is contradictory - if interpreter's state has the correct PC, resetting to halted would lose it. The comment suggests two conflicting behaviors.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate claims 'Don't call interpreter.start() here' because immediate executor already called it, but this assumption may not hold for all immediate commands

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment: "# NOTE: Don't call interpreter.start() here - the immediate executor already
# called it if needed (e.g., 'RUN 120' called interpreter.start(start_line=120)
# to set PC to line 120). Calling it again would reset PC to the beginning."

This assumes the immediate executor always calls start() when needed, but there's no verification that this contract is maintained. If immediate executor changes, this could break silently.

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

The comment is technically correct that help_widget.py's keypress() method uses hardcoded keys, but the comment's claim about avoiding circular dependencies is misleading since HelpMacros does load the JSON (just for different purposes).

---

#### code_vs_comment_conflict

**Description:** Comment claims link pattern matches both formats but regex only matches one

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at line ~234 states:
"Links are marked with [text] or [text](url) in the rendered output. This method finds ALL such patterns for display/navigation using regex r'\\[([^\\]]+)\\](?:\\([^)]+\\))?', which matches both formats."

However, the actual regex pattern used in the code at line ~251 is:
link_pattern = r'\[([^\]]+)\](?:\([^)]+\))?'

The comment shows escaped backslashes (\\[) but the actual code uses single backslashes (\[). While both are functionally equivalent in raw strings, the comment's representation is misleading. More importantly, the comment correctly describes the regex functionality, so this is just a documentation formatting issue.

---

#### code_vs_comment

**Description:** Variables window heading text inconsistency between initialization and sort state

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _create_variables_window() (lines 1091-1093):
tree.heading('#0', text='↓ Variable (Last Accessed)')
# Comment: Set initial heading text with down arrow (matches self.variables_sort_column='accessed', descending)

However, in __init__ (lines 109-110):
self.variables_sort_column = 'accessed'  # Current sort column (default: 'accessed' for last-accessed timestamp)
self.variables_sort_reverse = True  # Sort direction: False=ascending, True=descending (default descending for timestamps)

The heading shows '↓ Variable (Last Accessed)' with a down arrow, which typically indicates descending sort. The code sets variables_sort_reverse=True (descending). However, the heading text says 'Last Accessed' but the column is the Variable column (#0), not a separate 'Last Accessed' column. This creates confusion about what is being sorted.

---

#### code_vs_comment

**Description:** Comment about clearing yellow highlight contradicts when it's actually restored

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_mouse_click method around line 1560:
Comment says: "# Clear yellow statement highlight when clicking (allows text selection to be visible).\n# The highlight is restored when execution resumes or when stepping to the next statement."

This comment claims the highlight is restored when "execution resumes" but there's no code visible in this file that shows this restoration logic. The comment makes a promise about behavior that isn't implemented in the visible code, suggesting either:
1. The restoration logic is elsewhere and should be referenced
2. The comment is outdated and restoration doesn't work as described
3. The feature is incomplete

---

#### internal_inconsistency

**Description:** Inconsistent error handling between cmd_run and _execute_tick for interpreter errors

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In cmd_run() (line ~1950):
- Sets self.paused_at_breakpoint = False (not set to True on error)
- Does not call _highlight_current_statement() on error
- Does not update stack/variables on error
- Error handling is minimal

In _execute_tick() (line ~2070):
- Sets self.paused_at_breakpoint = True on error
- Calls _highlight_current_statement() to show error location
- Updates stack and variables with if self.stack_visible / if self.variables_visible
- Comprehensive error handling with context gathering

Both handle interpreter errors but with different UI state updates and user feedback mechanisms.

---

#### code_vs_comment

**Description:** TkIOHandler.input() docstring contradicts implementation regarding preference for inline input field

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Class docstring says: "Input strategy:\n- INPUT statement: Uses inline input field when backend available, otherwise uses modal dialog (not a preference, but availability-based)"

But input() method docstring says: "Prefers inline input field below output pane when backend is available, but falls back to modal dialog if backend is not available."

The word 'prefers' implies a preference/choice, while 'not a preference, but availability-based' explicitly denies this is a preference. These statements contradict each other.

---

#### code_vs_comment

**Description:** _on_status_click() docstring says it does NOT toggle breakpoints, but the comment says it shows 'confirmation message for ●' which is misleading about the actual functionality

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Method docstring states:
"Handle click on status column (show error details for ?, confirmation message for ●).

Displays informational messages about line status:
- For error markers (?): Shows error message in a message box
- For breakpoint markers (●): Shows confirmation message that breakpoint is set

Note: This displays information messages only. It does NOT toggle breakpoints -
that's handled by the UI backend's breakpoint toggle command
(e.g., TkBackend._toggle_breakpoint(), accessed via ^B in Tk UI or menu)."

The phrase 'confirmation message for ●' in the first line suggests it confirms an action, but it actually just shows information about an existing breakpoint. The detailed description clarifies this, but the summary line is misleading.

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

**Description:** README.md claims MBASIC supports four UI backends (CLI, Curses, Tk, Web), but the codebase only shows three backends (Curses, Tk, Web). No CLI backend exists in the source code.

**Affected files:**
- `docs/help/README.md`
- `docs/help/common/editor-commands.md`

**Details:**
README.md states: 'MBASIC supports four UI backends: CLI (command-line interface), Curses (terminal full-screen), Tk (desktop GUI), and Web (browser-based)'

However, the source code only contains:
- src/ui/web/ (Web backend)
- Tk backend (referenced in docs)
- Curses backend (referenced in docs)

No CLI backend directory or implementation exists. The docs also reference 'ui/cli/index.md' which would be for a non-existent backend.

---

#### code_vs_comment

**Description:** Code comment claims help is served at http://localhost/mbasic_docs, but the deprecated class implementation uses http://localhost:8000. Conflicting URLs for help system.

**Affected files:**
- `src/ui/web_help_launcher.py`

**Details:**
Module constant:
HELP_BASE_URL = 'http://localhost/mbasic_docs'

But WebHelpLauncher_DEPRECATED class uses:
self.server_port = 8000
base_url = f'http://localhost:{self.server_port}'

Comment says: 'The help site is already built and served at http://localhost/mbasic_docs'

But deprecated class starts its own server on port 8000. Which is correct?

---

#### documentation_inconsistency

**Description:** FIX function example contains misleading comment about array indexing

**Affected files:**
- `docs/help/common/language/functions/fix.md`

**Details:**
The fix.md example states 'Note: FIX is useful for converting floating-point results to array indices, ensuring truncation toward zero rather than rounding down (which INT does for negative numbers).' However, the example uses X = 3.7 and INDEX = FIX(X) which gives 3. The comment says 'Truncate to 3, not 4' but neither FIX nor INT would give 4 for 3.7. INT(3.7) = 3 and FIX(3.7) = 3. The distinction only matters for negative numbers. The example should use a negative number to demonstrate the difference.

---

#### documentation_inconsistency

**Description:** Contradictory information about LINE INPUT# syntax in title vs actual syntax

**Affected files:**
- `docs/help/common/language/statements/inputi.md`
- `docs/help/common/language/statements/line-input.md`

**Details:**
inputi.md has title 'LINE INPUT# (File)' and syntax 'LINE INPUT#<file number>,<string variable>' but the filename is 'inputi.md' which doesn't match the command name. The line-input.md file is for the keyboard version 'LINE INPUT' without the #. There should be consistency in naming - either the file should be 'line-input-hash.md' or 'line-inputi.md' to match the pattern used for other file I/O commands.

---

#### documentation_inconsistency

**Description:** Contradictory information about EDIT command availability

**Affected files:**
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/curses/editing.md`

**Details:**
CLI docs state 'The CLI includes a line editor accessed with the EDIT command' and references 'See: [EDIT Command](../../language/statements/edit.md)', but Curses docs do not mention EDIT command at all despite being a full-screen editor. This suggests either:
1. EDIT is CLI-only and Curses docs should clarify this
2. EDIT works differently in Curses and needs documentation
3. The CLI reference to EDIT is incorrect

---

#### documentation_inconsistency

**Description:** Contradictory information about Web UI file persistence

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/extensions.md`

**Details:**
Compatibility.md states 'Note: Settings (not files) can persist via Redis if configured - see [Web UI Settings](../ui/web/settings.md)' suggesting some persistence mechanism exists. However, extensions.md clearly states 'Files persist during browser session only (lost on page refresh)' and 'No persistent storage across sessions'. The mention of Redis persistence for settings creates confusion about what can and cannot persist.

---

#### documentation_inconsistency

**Description:** Missing referenced documentation file

**Affected files:**
- `docs/help/mbasic/compatibility.md`

**Details:**
Compatibility.md references 'See [Sequential Files Guide](../../user/sequential-files.md)' but this file path is not provided in the documentation set. This is a broken link that will confuse users.

---

#### documentation_inconsistency

**Description:** Missing referenced Web UI Settings documentation

**Affected files:**
- `docs/help/mbasic/compatibility.md`

**Details:**
Compatibility.md references 'see [Web UI Settings](../ui/web/settings.md)' but this file is not provided in the documentation set. This broken link is particularly important since it relates to Redis persistence configuration.

---

#### documentation_inconsistency

**Description:** Contradictory information about GET/PUT implementation

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
features.md under 'File I/O' section lists: 'Random files: FIELD, GET, PUT, LSET, RSET' - suggesting GET and PUT are implemented for file I/O.
not-implemented.md under 'Graphics (Not in MBASIC 5.21)' states: 'GET/PUT - Graphics block operations (not the file I/O GET/PUT which ARE implemented)'
This creates confusion because features.md doesn't distinguish between graphics GET/PUT and file I/O GET/PUT, while not-implemented.md explicitly makes this distinction. Users might think graphics GET/PUT is available based on features.md alone.

---

#### documentation_inconsistency

**Description:** LINE statement ambiguity

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
not-implemented.md states: 'LINE - Draw line (GW-BASIC graphics version - not the LINE INPUT statement which IS implemented)'
features.md lists 'LINE INPUT - Full line input' under Console I/O, confirming LINE INPUT is implemented.
However, features.md doesn't clarify that there's no graphics LINE command, which could confuse users familiar with GW-BASIC who might expect graphics capabilities.

---

#### documentation_inconsistency

**Description:** Contradictory information about variable inspection methods between Curses and CLI documentation

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/cli/variables.md`

**Details:**
docs/help/ui/curses/variables.md states: 'The Curses UI provides a visual variable inspector window for viewing and managing variables during program execution and debugging.' and describes opening it with a keyboard shortcut.

docs/help/ui/cli/variables.md states: 'The CLI uses the PRINT statement for variable inspection during debugging' and explicitly says 'The CLI does not have a Variables Window feature.'

However, docs/help/ui/cli/variables.md also contains this contradictory section: '## Variables Window (GUI UIs Only)

The CLI does not have a Variables Window feature. For visual variable inspection, use:
- **Curses UI** - Full-screen terminal with Variables Window ({{kbd:toggle_variables:curses}})'

This creates confusion because the CLI variables doc references the Curses variables window feature, but the reference format and context suggests this might be outdated or incorrectly placed.

---

#### documentation_inconsistency

**Description:** Broken cross-reference links in error handling documentation

**Affected files:**
- `docs/help/ui/common/errors.md`
- `docs/help/ui/curses/index.md`

**Details:**
docs/help/ui/common/errors.md contains these 'See Also' links:
- [ON ERROR GOTO](../../common/language/statements/on-error-goto.md)
- [ERR and ERL](../../common/language/statements/err-erl-variables.md)
- [RESUME](../../common/language/statements/resume.md)
- [Error Codes](../../common/language/appendices/error-codes.md)

These paths suggest a different documentation structure than what's shown in the curses/index.md, which references:
- [Statements Index](../../common/language/statements/index.md)
- [Functions Index](../../common/language/functions/index.md)
- [Error Codes](../../common/language/appendices/error-codes.md)

The errors.md references individual statement pages (on-error-goto.md, err-erl-variables.md, resume.md) that may not exist, while index.md only references the statements index page.

---

#### documentation_inconsistency

**Description:** Contradictory information about Find/Replace keyboard shortcuts and functionality

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/features.md`

**Details:**
feature-reference.md states:
- Find: {{kbd:find:tk}}
- Replace: {{kbd:replace:tk}}
- Find Next: F3

But features.md states:
- Find text ({{kbd:find:tk}}): Opens Find dialog
- Replace text ({{kbd:replace:tk}}): Opens combined Find/Replace dialog
- Note: {{kbd:find:tk}} opens the Find dialog. {{kbd:replace:tk}} opens the Find/Replace dialog which includes both Find and Replace functionality.

This suggests {{kbd:replace:tk}} opens a combined dialog, but feature-reference.md lists them as separate shortcuts.

---

#### documentation_inconsistency

**Description:** Typo in keyboard shortcut for Clear All Breakpoints

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
feature-reference.md shows:
'Clear All Breakpoints ({{kbd:file_save:tk}}hift+B)'

This appears to be a typo - should likely be '{{kbd:file_save:tk}}+Shift+B' or 'Shift+B' alone. The 'hift' is concatenated incorrectly with the kbd template.

---

#### documentation_inconsistency

**Description:** Stop/Interrupt shortcut conflicts with Cut operation

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
feature-reference.md states:
'### Stop/Interrupt ({{kbd:cut:tk}})
Stop a running program immediately.
- Menu: Run → Stop
- Shortcut: {{kbd:cut:tk}}'

But later in the same document:
'### Cut/Copy/Paste ({{kbd:cut:tk}}/C/V)
Standard clipboard operations with native OS clipboard integration.
- Cut: {{kbd:cut:tk}}'

The same shortcut {{kbd:cut:tk}} is assigned to both Stop Program and Cut operation, which is a conflict.

---

#### documentation_inconsistency

**Description:** Contradictory implementation status for Tk GUI features

**Affected files:**
- `docs/help/ui/tk/settings.md`
- `docs/help/ui/tk/index.md`
- `docs/help/ui/tk/features.md`

**Details:**
settings.md clearly states:
'**Implementation Status:** The Tk (Tkinter) desktop GUI is planned to provide the most comprehensive settings dialog. **The features described in this document represent planned/intended implementation and are not yet available.**'

However, index.md, features.md, and other docs describe Tk GUI features as if they are fully implemented, with no warnings about planned vs. actual features. For example:
- index.md: 'The Tkinter GUI provides powerful features for BASIC development.'
- features.md describes Smart Insert, Breakpoints, Variables Window as current features
- feature-reference.md lists 37 features without implementation status warnings

---

#### documentation_inconsistency

**Description:** Contradictory information about function key shortcuts in Web UI

**Affected files:**
- `docs/help/ui/web/debugging.md`

**Details:**
debugging.md states:
'**Note:** Function key shortcuts ({{kbd:continue:web}}, {{kbd:step:web}}, {{kbd:help:web}}1, etc.) are not implemented in the Web UI.'

But earlier in the same document it lists:
'**Currently Implemented:**
- **Run ({{kbd:run:web}})** - Start program from beginning
- **Continue ({{kbd:continue:web}})** - Run to next breakpoint
- **Step Statement ({{kbd:step:web}})** - Execute one statement'

This is contradictory - it says function keys are not implemented, but then lists them as currently implemented.

---

#### documentation_inconsistency

**Description:** Contradictory information about program persistence and auto-save functionality

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/settings.md`

**Details:**
features.md states under 'Local Storage > Currently Implemented': 'Programs stored in Python server memory (session-only, lost on page refresh)' and 'Recent files list stored in browser localStorage'. However, it also states under 'Automatic Saving (Planned)': 'Saves programs to browser localStorage for persistence'.

In getting-started.md under 'Saving a File', it says: 'Note: The Web UI uses browser downloads for saving program files to your computer. Auto-save of programs to browser localStorage is planned for a future release. (Settings ARE saved to localStorage - see Settings)'

In settings.md under 'Settings Storage > Local Storage (Default)', it confirms: 'Settings persist across page reloads' and 'Settings stay in your browser'.

The inconsistency: Programs are described as both 'stored in Python server memory (session-only)' AND as potentially being saved to localStorage (planned). The current state is unclear - are programs in server memory or localStorage? The note in getting-started.md clarifies that SETTINGS are in localStorage but PROGRAMS are not, but features.md doesn't make this distinction clear.

---

#### documentation_inconsistency

**Description:** Settings storage mechanism contradicts features documentation

**Affected files:**
- `docs/help/ui/web/settings.md`
- `docs/help/ui/web/features.md`

**Details:**
settings.md describes two storage mechanisms:
1. 'Local Storage (Default)' - 'settings are stored in your browser's localStorage'
2. 'Redis Session Storage (Multi-User Deployments)' - 'If the web server is configured with NICEGUI_REDIS_URL, settings are stored in Redis'

However, features.md under 'Local Storage > Currently Implemented' only mentions: 'Recent files list stored in browser localStorage' and doesn't mention Redis at all.

Also, settings.md states settings can be 'per-session' in Redis mode ('Settings are session-based (cleared when session expires)'), but features.md under 'Session Recovery (Planned)' suggests session recovery is a planned feature, not currently implemented.

The actual current implementation of settings storage needs clarification.

---

#### documentation_inconsistency

**Description:** Missing UI_FEATURE_COMPARISON.md file referenced in README

**Affected files:**
- `docs/user/INSTALL.md`
- `docs/user/README.md`

**Details:**
docs/user/README.md lists under 'Reference Documentation': '- **[UI_FEATURE_COMPARISON.md](UI_FEATURE_COMPARISON.md)** - Feature comparison across UIs'. However, this file is not included in the provided documentation files. This is a broken reference.

---

#### documentation_inconsistency

**Description:** Missing keyboard-shortcuts.md file referenced in README and other docs

**Affected files:**
- `docs/user/README.md`
- `docs/user/QUICK_REFERENCE.md`
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
docs/user/README.md lists: '- **[keyboard-shortcuts.md](keyboard-shortcuts.md)** - Keyboard shortcuts reference (Curses UI specific)'. TK_UI_QUICK_START.md references it: '- **Keyboard Shortcuts**: See [Tk Keyboard Shortcuts](keyboard-shortcuts.md)'. However, this file is not included in the provided documentation files. This is a broken reference.

---

#### documentation_inconsistency

**Description:** Contradictory compatibility claims about line ending support

**Affected files:**
- `docs/user/sequential-files.md`

**Details:**
The document states 'This MBASIC implementation supports **all three line ending formats**' and shows '✅ Yes' for CRLF, LF, and CR support. However, under 'Comparison with CP/M MBASIC 5.21', it states:
'MBASIC 5.21 line ending compatibility | ⚠️ More permissive (MBASIC only accepts CRLF)'
This creates confusion: if the implementation is 'more permissive' than MBASIC 5.21, it's technically incompatible (accepts files MBASIC 5.21 would reject), yet the summary table shows compatibility as a warning rather than explaining this is an intentional enhancement.

---

### 🟡 Medium Severity

#### Documentation inconsistency

**Description:** Version number inconsistency between setup.py and ast_nodes.py documentation

**Affected files:**
- `setup.py`
- `src/ast_nodes.py`

**Details:**
setup.py line 3: 'Setup script for MBASIC 5.21 Interpreter (version 0.99.0)'
setup.py line 5: 'Package version 0.99.0 reflects approximately 99% implementation status (core complete).'
setup.py line 14: 'version="0.99.0"'
setup.py line 51: 'Development Status :: 3 - Alpha'

ast_nodes.py line 3: 'Note: 5.21 refers to the Microsoft BASIC-80 language version, not this package version.'

The setup.py claims version 0.99.0 is '~99% implementation status (core complete)' but classifies it as 'Development Status :: 3 - Alpha'. Alpha status typically indicates early development, not 99% complete. This is contradictory.

---

#### Documentation inconsistency

**Description:** LineNode documentation claims AST is single source of truth but doesn't explain how char_start/char_end are maintained during editing

**Affected files:**
- `src/ast_nodes.py`

**Details:**
LineNode lines 127-138:
'The AST is the single source of truth. Text is always regenerated from the AST using statement token information (each statement has char_start/char_end and tokens preserve original_case for keywords and identifiers).

Design note: This class intentionally does not have a source_text field to avoid maintaining duplicate copies that could get out of sync with the AST during editing. Text regeneration is handled by the position_serializer module which reconstructs source text from statement nodes and their token information. Each StatementNode has char_start/char_end offsets that indicate the character position within the regenerated line text.'

The documentation states char_start/char_end indicate positions in 'regenerated line text', but doesn't explain how these offsets are kept synchronized when the AST is modified. If text is always regenerated, how are the offsets maintained correctly?

---

#### Code vs Comment conflict

**Description:** RemarkStatementNode comment_type default value documentation contradicts usage description

**Affected files:**
- `src/ast_nodes.py`

**Details:**
RemarkStatementNode lines 677-684:
'Note: comment_type preserves the original comment syntax used in source code.
The parser sets this to "REM", "REMARK", or "APOSTROPHE" based on input.
Default value "REM" is used only when creating nodes programmatically.'

Line 686:
'comment_type: str = "REM"  # Tracks original syntax: "REM", "REMARK", or "APOSTROPHE"'

The comment says the default is 'used only when creating nodes programmatically', but this creates ambiguity: if a node is created programmatically with default value, how do we know if it represents a REM statement or just wasn't initialized properly? The design seems fragile.

---

#### code_vs_comment

**Description:** Comment claims identifiers preserve original case but code returns original_text directly without using identifier_table

**Affected files:**
- `src/basic_builtins.py`

**Details:**
In case_string_handler.py, the case_keepy_string method for 'idents' has a long comment explaining:
"Identifiers always preserve their original case in display...
Note: We return original_text directly. An identifier_table infrastructure
exists (see get_identifier_table) but is not currently used for identifiers,
as they always preserve their original case without policy enforcement."

However, the get_identifier_table method exists and accepts a policy parameter, suggesting it was designed to support policy-based case handling for identifiers. The comment acknowledges this infrastructure exists but isn't used, which may indicate incomplete implementation or refactoring.

---

#### code_vs_comment

**Description:** Comment about negative zero handling may not match actual behavior for all edge cases

**Affected files:**
- `src/basic_builtins.py`

**Details:**
In format_numeric_field method:
"# Determine sign BEFORE rounding (for negative zero handling)
original_negative = value < 0

# Round to precision
if precision > 0:
    rounded = round(value, precision)
else:
    rounded = round(value)

# Determine sign - preserve negative sign for values that round to zero.
# original_negative was captured before rounding (see above)
# This allows us to detect cases like -0.001 which round to 0 but should display as '-0' (not '0').
# This matches BASIC behavior. Positive values that round to zero display as '0'.
if rounded == 0 and original_negative:
    is_negative = True
else:
    is_negative = rounded < 0"

The comment claims this matches BASIC behavior, but the logic only preserves negative sign if the value was originally negative AND rounds to exactly zero. However, for values like -0.5 with precision=0, round(-0.5) returns 0 in Python 3 (banker's rounding), so original_negative=True and rounded==0, resulting in is_negative=True. But -0.5 should arguably display as '-1' not '-0'. This may be correct BASIC behavior but the comment doesn't clarify this edge case.

---

#### code_vs_comment

**Description:** EOF function comment references execute_open() in interpreter.py but this file is not provided

**Affected files:**
- `src/basic_builtins.py`

**Details:**
In EOF method docstring:
"Note: For binary input files (mode 'I' from OPEN statement), respects ^Z (ASCII 26)
as EOF marker (CP/M style). In MBASIC syntax, mode 'I' stands for 'Input' but is
specifically BINARY INPUT mode, implemented as 'rb' by execute_open() in interpreter.py."

The comment references execute_open() in interpreter.py, but interpreter.py is not included in the provided files. This makes it impossible to verify the claim that mode 'I' is implemented as 'rb' mode.

---

#### Code vs Documentation inconsistency

**Description:** SandboxedFileIO methods documented as STUB but some are actually implemented

**Affected files:**
- `src/file_io.py`

**Details:**
Documentation says:
"Implementation status:
- list_files(): IMPLEMENTED - delegates to backend.sandboxed_fs
- load_file(): STUB - raises IOError (requires async refactor)
- save_file(): STUB - raises IOError (requires async refactor)
- delete_file(): STUB - raises IOError (requires async refactor)
- file_exists(): STUB - raises IOError (requires async refactor)"

However, list_files() is fully implemented with working code that accesses backend.sandboxed_fs, not just a stub. The documentation correctly identifies it as IMPLEMENTED, but groups it with the stubs in a way that's confusing.

---

#### Code vs Comment conflict

**Description:** Comment says GOSUB return stack size is 100 but no overflow checking implemented

**Affected files:**
- `src/codegen_backend.py`

**Details:**
In Z88dkCBackend.generate():
code.append(self.indent() + 'int gosub_stack[100];  /* Return line numbers */')
code.append(self.indent() + 'int gosub_sp = 0;      /* Stack pointer */')

The generated C code allocates a fixed-size stack of 100 entries but never checks for overflow. If a program has deeply nested GOSUBs (>100 levels), it will cause undefined behavior (buffer overflow). The comment documents the size but the implementation doesn't validate against it.

---

#### Code vs Documentation inconsistency

**Description:** Documentation claims floating point support but implementation has limitations

**Affected files:**
- `src/codegen_backend.py`

**Details:**
Class docstring says:
"Supports:
- Integer variables (BASIC ! suffix maps to C int)
- FOR/NEXT loops
- PRINT statements for integers

Future:
- String support (requires runtime library)
- Arrays
- More complex expressions"

But the code actually implements SINGLE and DOUBLE types:
- _generate_variable_declarations() handles VarType.SINGLE (float) and VarType.DOUBLE (double)
- _get_format_specifier() returns '%g' for SINGLE and '%lg' for DOUBLE
- get_compiler_command() includes '-lm' flag for math library

The docstring says only integers are supported, but the implementation clearly supports floating point. The docstring is outdated.

---

#### Code vs Documentation inconsistency

**Description:** get_compiler_command() docstring doesn't mention -lm flag but implementation includes it

**Affected files:**
- `src/codegen_backend.py`

**Details:**
Method docstring:
"Return z88dk.zcc command for CP/M compilation"
# z88dk.zcc +cpm source.c -create-app -o output
# This generates OUTPUT.COM (uppercase .COM file)

But actual implementation:
return ['/snap/bin/z88dk.zcc', '+cpm', source_file, '-create-app', '-lm', '-o', output_file]

The inline comment documents the command without -lm, but the code includes it. The -lm flag is important for math library support (mentioned in another comment about floating point), so the docstring should document it.

---

#### code_vs_comment

**Description:** InMemoryFileHandle.flush() docstring claims it's a no-op and content is only saved on close(), but the code actually calls file_obj.flush() which could have side effects

**Affected files:**
- `src/filesystem/sandboxed_fs.py`

**Details:**
Docstring says: "Note: This calls StringIO/BytesIO flush() which are no-ops.
Content is only saved to the virtual filesystem on close().
Unlike standard file flush() which persists buffered writes to disk,
in-memory file writes are already in memory, so flush() has no effect."

Code implementation:
def flush(self):
    # StringIO/BytesIO have flush() methods (no-ops) - hasattr check for safety
    if hasattr(self.file_obj, 'flush'):
        self.file_obj.flush()

The docstring is technically correct that StringIO/BytesIO.flush() are no-ops, but the comment is misleading about the implementation's behavior.

---

#### code_vs_comment

**Description:** Comment about numbered line editing states 'This feature requires the following UI integration' with specific requirements, but the actual validation in code is less comprehensive than documented

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Comment claims:
"This feature requires the following UI integration:
- interpreter.interactive_mode must reference the UI object (checked with hasattr)
- UI.program must have add_line() and delete_line() methods (validated, errors if missing)
- UI._refresh_editor() method to update the display (optional, checked with hasattr)
- UI._highlight_current_statement() for restoring execution highlighting (optional, checked with hasattr)"

But the code only validates add_line/delete_line when they're about to be used:
if line_content and not hasattr(ui.program, 'add_line'):
    return (False, "Cannot edit program lines: add_line method not available\n")
if not line_content and not hasattr(ui.program, 'delete_line'):
    return (False, "Cannot edit program lines: delete_line method not available\n")

The validation is conditional on line_content, not comprehensive upfront validation as the comment suggests.

---

#### code_vs_comment

**Description:** OutputCapturingIOHandler.input() docstring says 'INPUT statements are parsed and executed normally, but fail at runtime' but this contradicts the LIMITATIONS section in help text which says 'INPUT statement will fail at runtime in immediate mode'

**Affected files:**
- `src/immediate_executor.py`

**Details:**
OutputCapturingIOHandler.input() docstring:
"Input not supported in immediate mode.

Note: INPUT statements are parsed and executed normally, but fail
at runtime when the interpreter calls this input() method."

Help text in _show_help():
"LIMITATIONS:
...
  • INPUT statement will fail at runtime in immediate mode (use direct assignment instead)"

Both say the same thing but the phrasing 'will fail' vs 'not supported' could be more consistent. This is a minor wording inconsistency.

---

#### code_vs_comment

**Description:** Comment claims digits are 'silently ignored' in EDIT mode, but code doesn't implement this behavior

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~730 states:
'INTENTIONAL BEHAVIOR: When digits are entered, they are silently ignored (no output, no cursor movement, no error). This preserves MBASIC compatibility where digits are reserved for count prefixes in the full EDIT implementation.'

However, the cmd_edit() implementation has no code to handle digit input (0-9). The while loop at line ~760 only handles specific commands (Space, D, I, X, H, E, Q, L, A, C, CR/LF). Any unhandled character (including digits) would fall through with no action, but this is not explicitly coded as 'silent ignore' behavior - it's just missing handling.

---

#### code_vs_comment

**Description:** CONT docstring claims editing clears execution state, but doesn't mention STOP state is also cleared

**Affected files:**
- `src/interactive.py`

**Details:**
The cmd_cont() docstring at line ~240 states:
'IMPORTANT: CONT will fail with "?Can't continue" if the program has been edited (lines added, deleted, or renumbered) because editing clears the GOSUB/RETURN and FOR/NEXT stacks to prevent crashes from invalidated return addresses and loop contexts.'

However, clear_execution_state() at line ~130 also clears the stopped flag:
'self.program_runtime.stopped = False'

This means editing not only clears stacks but also clears the STOP state itself, making CONT impossible. The docstring should mention that the stopped flag is cleared, not just the stacks.

---

#### code_vs_comment_conflict

**Description:** Comment claims GOTO/GOSUB in immediate mode are 'not recommended' but code fully supports them with special semantics

**Affected files:**
- `src/interactive.py`

**Details:**
Comment says: 'This is the intended behavior but may be unexpected, hence "not recommended".' However, the code implements full support for GOTO/GOSUB with careful PC restoration logic. The comment suggests discouragement but the implementation is deliberate and complete.

---

#### code_vs_comment_conflict

**Description:** Comment describes GOTO/GOSUB behavior that contradicts the stated purpose of PC restoration

**Affected files:**
- `src/interactive.py`

**Details:**
Comment says: 'They execute and jump during execute_statement(), but we restore the original PC afterward to preserve CONT functionality. This means:
- The jump happens and target code runs during execute_statement()
- The final PC change is then reverted, preserving the stopped position'

This is confusing because if the jump happens and target code runs, but then PC is restored, it implies the target code execution is somehow preserved despite PC restoration. The actual behavior needs clarification - does the GOTO actually execute the target line or not?

---

#### code_vs_comment

**Description:** Comment describes skip_next_breakpoint_check behavior incorrectly regarding when it's set and cleared

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line 56-59 says:
"Set to True AFTER halting at a breakpoint (set after returning state).
On next execution, if still True, allows stepping past the breakpoint once,
then is cleared to False. Prevents re-halting on same breakpoint."

But code at lines 398-404 shows:
- It's checked BEFORE halting: `if not self.state.skip_next_breakpoint_check:`
- It's set to True WHEN halting: `self.state.skip_next_breakpoint_check = True`
- It's cleared AFTER skipping: `self.state.skip_next_breakpoint_check = False`

The comment implies it's set after returning state (externally), but the code sets it internally during tick_pc().

---

#### code_vs_comment

**Description:** Comment about return_stmt validation range is incorrect

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at lines 1009-1017 says:
"return_stmt is 0-indexed offset into statements array.
Valid range: 0 to len(statements) (inclusive).
- 0 to len(statements)-1: Normal statement positions
- len(statements): Special sentinel - GOSUB was last statement on line, so RETURN
  continues at next line. This value is valid because PC can point one past the
  last statement to indicate 'move to next line' (handled by statement_table.next_pc).
Values > len(statements) indicate the statement was deleted (validation error)."

But the validation code at line 1018 checks:
`if return_stmt > len(line_statements):`

This means return_stmt == len(line_statements) is VALID (not an error), but return_stmt > len(line_statements) is invalid. The comment correctly describes this, but then the comment at line 1018 says:
"Check for strictly greater than (== len is OK)"

This is consistent, so this may not be an inconsistency. However, the phrasing 'Special sentinel' suggests this is a documented special case, but there's no evidence in the code that return_stmt is ever intentionally set to len(statements) as a sentinel value.

---

#### code_vs_comment

**Description:** Docstring for execute_for describes string variable behavior incorrectly

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring at lines 1027-1037 says:
"The loop variable typically has numeric type suffixes (%, !, #). The variable
type determines how values are stored. String variables ($) are syntactically
valid (parser accepts them) but cause a 'Type mismatch' error at runtime when
set_variable() attempts to assign numeric loop values to a string variable."

This describes the behavior but doesn't match what the code actually does. The code at lines 1040-1053 calls set_variable() with the start value, which would indeed cause a type mismatch if the variable is a string type. However, the comment implies this is expected behavior, but there's no try/except to handle this case specifically. If this is truly 'syntactically valid but runtime error', the code should either:
1. Validate the type before the FOR loop and raise a clear error
2. Let set_variable() raise the error (current behavior)

The comment suggests option 2 is intentional, but it's unclear if this is the desired behavior or a limitation.

---

#### code_vs_comment

**Description:** Comment about NEXT variable processing order contradicts itself

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at lines 1073-1082 says:
"NEXT I, J, K processes variables left-to-right: I first, then J, then K.
For each variable, _execute_next_single() is called to increment it and check if
the loop should continue. If _execute_next_single() returns True (loop continues),
execution jumps back to the FOR body and remaining variables are not processed.
If it returns False (loop finished), that loop is popped and the next variable is processed.

This differs from separate statements (NEXT I: NEXT J: NEXT K) which would
always execute sequentially, processing all three NEXT statements."

But then at lines 1095-1102, the code shows:
```python
for var_node in var_list:
    var_name = var_node.name + (var_node.type_suffix or "")
    should_continue = self._execute_next_single(var_name, var_node=var_node)
    if should_continue:
        return
```

The comment says 'If _execute_next_single() returns True (loop continues), execution jumps back to the FOR body', but the code just returns from execute_next(), which would continue to the next statement after NEXT, not jump back to FOR. The jump back to FOR must happen inside _execute_next_single() by setting runtime.npc.

---

#### code_vs_comment

**Description:** Comment describes RESUME 0 as distinct from RESUME, but code treats them identically

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1090 states:
# RESUME or RESUME 0 - retry the statement that caused the error
# Note: MBASIC allows both 'RESUME' and 'RESUME 0' as equivalent syntactic forms.
# Parser preserves the distinction (None vs 0) for source text regeneration,
# but runtime execution treats both identically.

However, the code checks:
if stmt.line_number is None or stmt.line_number == 0:

This suggests the comment is accurate about treating them identically, but the phrasing 'Parser preserves the distinction (None vs 0)' implies there might be a distinction that isn't actually preserved in execution behavior.

---

#### code_vs_comment

**Description:** Comment about valid return_stmt range conflicts with actual validation logic

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~950 states:
# return_stmt is 0-indexed offset into statements array.
# Valid range:
#   - 0 to len(statements)-1: Normal statement positions (existing statements)
#   - len(statements): Special sentinel value - FOR was last statement on line,
#                      continue execution at next line (no more statements to execute on current line)
#   - > len(statements): Invalid - indicates the statement was deleted
#
# Validation: Check for strictly greater than (== len is OK as sentinel)

But the validation code is:
if return_stmt > len(line_statements):
    raise RuntimeError(f"NEXT error: FOR statement in line {return_line} no longer exists")

This validation allows return_stmt == len(line_statements) as valid (the sentinel), but the comment's description of '> len(statements): Invalid' suggests that values strictly greater than len should be invalid. The code and comment agree on the logic, but the comment's phrasing could be clearer that the validation is 'if return_stmt > len' which makes 'len' valid and 'len+1' invalid.

---

#### code_vs_comment

**Description:** Comment about CLEAR file close error handling contradicts RESET comment

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1340 states:
# Close all open files
# Note: Errors during file close are silently ignored (bare except: pass).
# This differs from RESET which allows errors to propagate to the caller.

And comment at line ~1850 states:
# Note: Unlike CLEAR (which silently ignores file close errors), RESET allows
# errors during file close to propagate to the caller. This is intentional
# different behavior between the two statements.

However, the CLEAR code shows:
for file_num in list(self.runtime.files.keys()):
    try:
        file_obj = self.runtime.files[file_num]
        if hasattr(file_obj, 'close'):
            file_obj.close()
    except:
        pass

While RESET code shows:
for file_num in list(self.runtime.files.keys()):
    self.runtime.files[file_num]['handle'].close()
    del self.runtime.files[file_num]

The comments are consistent with each other and with the code. However, there's a subtle inconsistency: CLEAR accesses file_obj directly from runtime.files, while RESET accesses file_obj['handle']. This suggests CLEAR might be using an older data structure format where files[file_num] is the file object directly, not a dict with 'handle' key. This is an inconsistency in how the two methods access the file structure.

---

#### code_vs_comment

**Description:** Comment about _read_line_from_file encoding mentions CP437/CP850 but doesn't explain why latin-1 is used

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1480 states:
Encoding:
Uses latin-1 (ISO-8859-1) to preserve byte values 128-255 unchanged.
CP/M and MBASIC used 8-bit characters; latin-1 maps bytes 0-255 to
Unicode U+0000-U+00FF, allowing round-trip byte preservation.
Note: CP/M systems often used code pages like CP437 or CP850 for characters
128-255, which do NOT match latin-1. Latin-1 preserves the BYTE VALUES but
not necessarily the CHARACTER MEANING for non-English CP/M text. Conversion
may be needed for accurate display of non-English CP/M files.

This comment explains that latin-1 doesn't match CP437/CP850 and that conversion may be needed, but doesn't explain WHY latin-1 was chosen over CP437/CP850. The comment should clarify that latin-1 is used for byte preservation (round-trip guarantee) rather than character accuracy, and that applications needing accurate CP/M character display should convert from latin-1 to the appropriate code page after reading.

---

#### code_vs_comment

**Description:** Comment in execute_stop() claims 'BreakException handler does not update PC', but this behavior is not verified in the visible code

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment states: 'Note: execute_stop() moves NPC to PC for resume, while BreakException handler does not update PC, which affects whether CONT can resume properly.'

This comment references BreakException handler behavior that is not visible in the provided code snippet. The comment may be outdated if the BreakException handler was changed, or it may be documenting behavior in a different file.

---

#### code_vs_comment

**Description:** Comment in evaluate_functioncall() describes debugger_set parameter usage, but the actual set_variable call doesn't use this parameter

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment states: 'Restore parameter values (use debugger_set=True to avoid tracking)'

Code shows: self.runtime.set_variable(base_name, type_suffix, saved_value, debugger_set=True)

However, earlier in the same function when setting parameters, the code uses: self.runtime.set_variable(param.name, param.type_suffix, args[i], token=call_token, limits=self.limits)

This doesn't use debugger_set=True, which seems inconsistent with the comment's explanation that parameter setting is 'internal function call machinery, not user-visible variable access'.

---

#### code_vs_comment

**Description:** Comment in execute_list() warns about ProgramManager sync issues but doesn't specify what happens if sync fails

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment states: 'If ProgramManager fails to maintain this sync, LIST output may show stale or incorrect line text.'

The code doesn't have any error handling or validation to detect when line_text_map is out of sync with the AST. If a line number exists in the statement table but not in line_text_map, the code silently skips it (the 'if line_num in self.runtime.line_text_map' check). This behavior isn't documented in the comment.

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

#### Code vs Documentation inconsistency

**Description:** Module docstring references SimpleKeywordCase in src/simple_keyword_case.py but this file is not provided in the source code files

**Affected files:**
- `src/keyword_case_manager.py`

**Details:**
Docstring says: "For simpler force-based policies in the lexer, see SimpleKeywordCase (src/simple_keyword_case.py) which only supports force_lower, force_upper, and force_capitalize."

But src/simple_keyword_case.py is not included in the provided source files, making this reference unverifiable and potentially broken.

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

**Description:** Comment claims RND and INKEY$ are the only functions that can be called without parentheses in MBASIC 5.21, but this is contradicted by the code implementation

**Affected files:**
- `src/parser.py`

**Details:**
Comment at line 11-12 states:
"Exception: Only RND and INKEY$ can be called without parentheses in MBASIC 5.21
  (this is specific to these two functions, not a general MBASIC feature)"

However, the code at lines 1088-1091 shows RND can be called without parentheses:
"if func_token.type == TokenType.RND and not self.match(TokenType.LPAREN):
    # RND without parentheses - valid in MBASIC 5.21"

And at lines 1094-1098 shows INKEY$ can be called without parentheses:
"if func_token.type == TokenType.INKEY and not self.match(TokenType.LPAREN):
    # INKEY$ without parentheses - valid in MBASIC 5.21"

But the comment says these are exceptions, while the code structure suggests this is a general pattern that could apply to other functions. The comment may be outdated or the implementation may be incomplete.

---

#### code_vs_comment

**Description:** Comment about MID$ statement detection strategy doesn't match the actual lookahead implementation

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines 677-680 states:
"# Lookahead strategy: scan past balanced parentheses, check for = sign"

But the actual code at lines 681-700 shows a more complex strategy:
1. It saves position
2. Advances past MID token
3. Checks for LPAREN
4. Scans to find matching RPAREN with depth tracking
5. Checks for EQUAL after RPAREN
6. Has try-catch for lookahead failures
7. Restores position in multiple scenarios

The comment oversimplifies the implementation and doesn't mention the error handling, position restoration, or the fallback behavior when lookahead fails.

---

#### code_vs_comment

**Description:** Comment describes LINE_INPUT tokenization behavior that contradicts actual lexer behavior

**Affected files:**
- `src/parser.py`

**Details:**
In parse_input() method around line 1150:

Comment states: "Note: The lexer tokenizes LINE keyword as LINE_INPUT token both when standalone (LINE INPUT statement) and when used as modifier (INPUT...LINE). The parser distinguishes these cases by context - LINE INPUT is a statement, INPUT...LINE uses LINE as a modifier within the INPUT statement."

However, this comment describes the lexer creating a single LINE_INPUT token in both contexts. The code then checks for TokenType.LINE_INPUT when parsing the LINE modifier within INPUT statement. This suggests the lexer does tokenize LINE as LINE_INPUT in both contexts, but the comment's phrasing "The parser distinguishes these cases by context" is misleading - the lexer has already tokenized it the same way, and the parser just uses it in different statement contexts.

---

#### code_vs_comment

**Description:** Comment about def_type_map behavior contradicts when map updates occur

**Affected files:**
- `src/parser.py`

**Details:**
In parse_deftype() method around line 2070:

Comment states: "Note: This method always updates def_type_map during parsing. The type map is shared across all statements (both in interactive mode where statements are parsed one at a time, and in batch mode where the entire program is parsed)."

However, the comment in parse_deffn() around line 2110 states: "Function name normalization: All function names are normalized to lowercase with 'fn' prefix (e.g., "FNR" becomes "fnr", "FNA$" becomes "fna$") for consistent lookup. This matches the lexer's identifier normalization and ensures function"

The parse_deffn comment is incomplete (cuts off mid-sentence), but more importantly, if def_type_map is updated during parsing as stated in parse_deftype(), this could affect how variables are typed in parse_for() and parse_next() methods which check def_type_map. The timing of when DEF statements are parsed vs when variables are parsed could lead to inconsistent behavior depending on statement order in the program.

---

#### code_vs_comment

**Description:** Comment claims RESUME 0 means 'retry error statement' but code stores 0 as a line number without special handling

**Affected files:**
- `src/parser.py`

**Details:**
In parse_resume() method:

Comment says: "Note: RESUME 0 means 'retry error statement' (interpreter treats 0 and None equivalently)"

But code does:
if self.match(TokenType.LINE_NUMBER, TokenType.NUMBER):
    line_number = int(self.advance().value)

This stores 0 as a regular line number value, not as a special sentinel. The comment suggests 0 should be treated like None (no argument), but the code treats it as line number 0.

---

#### code_vs_comment

**Description:** parse_call() docstring claims MBASIC 5.21 primarily uses simple numeric address form, but implementation treats all forms equally

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states:
"Note: MBASIC 5.21 primarily uses the simple numeric address form, but this
parser fully supports both forms for broader compatibility."

However, the implementation doesn't distinguish between MBASIC 5.21 syntax and extended syntax - it parses both identically without any version-specific handling or warnings. The comment suggests a preference that isn't reflected in the code behavior.

---

#### code_vs_comment

**Description:** parse_def_fn() comment about case-insensitive matching contradicts implementation that normalizes to lowercase

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states:
"Function names are case-insensitive. The parser normalizes function names to ensure
calls match their definitions regardless of case."

The implementation normalizes to lowercase ('fn' prefix), but the comment says 'regardless of case' which could imply case-preserving behavior. The actual behavior is case-folding to lowercase, not case-insensitive comparison.

---

#### code_vs_comment

**Description:** PC class docstring describes stmt_offset as '0-based index' but also calls it an 'offset' which could be confusing. The note clarifies it's a list index, not byte offset, but the parameter name 'stmt_offset' suggests offset semantics.

**Affected files:**
- `src/pc.py`

**Details:**
Docstring says: 'The stmt_offset is a 0-based index into the statements list for a line.'
But also: 'Note: Throughout the codebase, stmt_offset is consistently used as a list index (0, 1, 2, ...) not an offset in bytes. The parameter name uses "offset" for historical/semantic reasons (it offsets from the start of the line\'s statement list).'

The examples show: 'PC(10, 0)  - First statement on line 10 (stmt_offset=0)' and 'PC(10, 2)  - Third statement on line 10 (stmt_offset=2)'

This is internally consistent but the terminology mixing 'offset' and 'index' could cause confusion.

---

#### code_vs_comment

**Description:** apply_keyword_case_policy docstring says 'callers should pass lowercase keywords for consistency' but then describes handling 'keywords in any case'

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring states: 'Note: While this function can handle keywords in any case, callers should pass lowercase keywords for consistency (emit_keyword() requires lowercase). The first_wins policy normalizes to lowercase for lookup. Other policies transform based on input case.'

This creates ambiguity - if the function can handle any case, why should callers pass lowercase? The emit_keyword docstring reinforces this: 'keyword: The keyword to emit (must be normalized lowercase by caller, e.g., "print", "for")'

The inconsistency is that apply_keyword_case_policy is defensive (handles any case) but emit_keyword requires lowercase. This should be clarified.

---

#### code_vs_comment

**Description:** PositionConflict tracking claims to preserve positions but serialize_let_statement explicitly discards LET keyword position information

**Affected files:**
- `src/position_serializer.py`

**Details:**
Module docstring: 'Key principle: AST is the single source of truth for CONTENT (what tokens exist and their values). Original token positions are HINTS for formatting (where to place tokens). When positions conflict with content, content wins and a PositionConflict is recorded.'

However, serialize_let_statement doesn't record a PositionConflict when it drops the LET keyword - it silently discards it. This is inconsistent with the stated principle that position conflicts should be tracked.

If LET was at a specific position in the original source, dropping it is a position conflict that should be recorded.

---

#### code_vs_comment

**Description:** renumber_with_spacing_preservation docstring says 'AST is the single source of truth' but then modifies AST in place, which could violate immutability expectations

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring: 'AST is the single source of truth. This function:
1. Updates line numbers in the AST
2. Updates all line number references (GOTO, GOSUB, etc.)
3. Adjusts token column positions to account for line number length changes'

The function modifies the AST nodes in place (line_node.line_number = new_num, stmt.column += offset, etc.) rather than creating new nodes. This could be problematic if:
1. The original AST is still referenced elsewhere
2. The caller expects immutable AST nodes (as suggested by PC class being immutable)

The PC class docstring emphasizes immutability: 'Immutable program counter - identifies a statement by (line_num, stmt_offset).' If PC is immutable for safety, shouldn't AST nodes follow the same pattern?

---

#### code_vs_comment_conflict

**Description:** Comment in check_array_allocation() claims to account for MBASIC array sizing convention, but the actual array creation is delegated to execute_dim() in interpreter.py. The comment suggests this function handles the sizing, but it only does limit checking.

**Affected files:**
- `src/resource_limits.py`

**Details:**
Comment says: "# Note: DIM A(N) creates N+1 elements (0 to N) in MBASIC 5.21
# This calculation accounts for the MBASIC array sizing convention for limit checking.
# The actual array creation/initialization is done by execute_dim() in interpreter.py."

The comment is somewhat contradictory - it says "This calculation accounts for" but then says the actual creation is done elsewhere. The calculation does account for it (total_elements *= (dim_size + 1)), but the phrasing could be clearer.

---

#### code_vs_comment

**Description:** Comment claims 'original_case' field stores original case as first typed, but code actually stores canonical case resolved by case_conflict policy

**Affected files:**
- `src/runtime.py`

**Details:**
Line 48-51 comment: "Note: The 'original_case' field stores the canonical case for display (determined by case_conflict policy).
       Despite its misleading name, this field contains the policy-resolved canonical case variant,
       not the original case as first typed. See _check_case_conflict() for resolution logic."

This comment acknowledges the field name is misleading. Multiple locations in code confirm this:
- Line 289: "# Note: Despite the field name, this stores canonical case not original (see module header)"
- Line 336: "'original_case': canonical_case  # Canonical case for display (field name is historical, see module header)"
- Line 348: "# Note: Despite the field name, this stores canonical case not original (see module header)"

The field name 'original_case' contradicts its actual purpose of storing the canonical/resolved case.

---

#### code_vs_comment

**Description:** get_variable() docstring says token is REQUIRED but implementation allows token attributes to be missing

**Affected files:**
- `src/runtime.py`

**Details:**
Lines 257-270 docstring says:
"Args:
    ...
    token: REQUIRED - Token object for tracking (ValueError raised if None).

           Token object is required but its attributes are optional:
           - token.line: Preferred for tracking, falls back to self.pc.line_num if missing
           - token.position: Preferred for tracking, falls back to None if missing

           This allows robust handling of tokens from various sources (lexer, parser,
           fake tokens) while enforcing that some token object must be provided."

But then lines 289-291 show the actual tracking code:
"'line': getattr(token, 'line', self.pc.line_num if self.pc and not self.pc.halted() else None),
'position': getattr(token, 'position', None),"

The docstring says token is REQUIRED but then says its attributes are optional with fallbacks. This is confusing - if token can be an empty object with no attributes, what's the point of requiring it? The implementation allows a token with no line/position attributes, which seems to contradict the 'REQUIRED' emphasis.

---

#### Code vs Documentation inconsistency

**Description:** get_variables() docstring claims to return array 'value' but implementation doesn't include it

**Affected files:**
- `src/runtime.py`

**Details:**
Docstring states each dict contains:
"- 'value': Current value (scalars only)"

But for arrays, the code returns:
- 'last_accessed_value': value of last accessed cell
- 'last_accessed_subscripts': subscripts of last accessed cell

The docstring doesn't mention 'last_accessed_value', 'last_accessed_subscripts', 'last_read_subscripts', or 'last_write_subscripts' fields that are actually returned for arrays. The example in the docstring also doesn't show these fields.

---

#### code_vs_comment

**Description:** Comment claims _get_global_settings_path() and _get_project_settings_path() are 'not currently used' but they are called in __init__ via backend attributes

**Affected files:**
- `src/settings.py`

**Details:**
Comment in _get_global_settings_path() says: 'Note: This method is not currently used. Path resolution has been delegated to the backend...'

However, __init__ does use these paths:
self.global_settings_path = getattr(backend, 'global_settings_path', None)
self.project_settings_path = getattr(backend, 'project_settings_path', None)

The FileSettingsBackend calls these methods in its __init__:
self.global_settings_path = self._get_global_settings_path()
self.project_settings_path = self._get_project_settings_path()

---

#### code_vs_comment

**Description:** get() method docstring claims file_settings has highest precedence but notes it's not populated in normal usage, creating confusion

**Affected files:**
- `src/settings.py`

**Details:**
The get() method docstring states:
'Precedence order: file > project > global > definition default > provided default'

But then the Note says:
'Note: File-level settings (first in precedence) are not populated in normal usage. The file_settings dict can be set programmatically and is checked first, but no persistence layer exists (not saved/loaded) and no UI/command manages per-file settings. In practice, precedence is: project > global > definition default > provided default.'

This creates confusion about what the actual precedence is. The docstring should either:
1. Document only the practical precedence (project > global > default)
2. Or clearly mark file-level as 'reserved for future use' in the main precedence line

---

#### code_vs_comment

**Description:** register_keyword() docstring says 'original_case' parameter is 'ignored for keywords' but this contradicts the purpose of keyword case handling

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
In SimpleKeywordCase.register_keyword():
Docstring says: 'original_case: Original case as typed (ignored for keywords)'

But the entire purpose of this class is to handle keyword case. The parameter name 'original_case' and the comment 'ignored for keywords' is confusing. If it's truly ignored, why is it a parameter?

Looking at the implementation, it just calls apply_case() which ignores the original_case parameter entirely. This suggests the parameter exists for API compatibility with KeywordCaseManager but serves no purpose in SimpleKeywordCase.

---

#### code_vs_documentation

**Description:** SettingsManager class docstring mentions FILE scope infrastructure but doesn't explain it's incomplete/reserved

**Affected files:**
- `src/settings.py`

**Details:**
Class docstring says:
'Note: File-level settings infrastructure is partially implemented (file_settings dict, FILE scope support in get/set/reset methods for runtime manipulation), but persistence is not implemented (load() doesn\'t populate it, save() doesn\'t persist it). No settings are defined with FILE scope in settings_definitions.py. This infrastructure is reserved for future use.'

This is good documentation, but it's buried in the class docstring. The module docstring at the top only mentions 'global settings and project settings' without mentioning FILE scope at all. This creates an inconsistency where the module-level docs don't match the class-level docs.

---

#### Documentation inconsistency

**Description:** Auto-save feature is documented and implemented but not mentioned in any keybindings or UI backend documentation

**Affected files:**
- `src/ui/auto_save.py`
- `src/ui/curses_keybindings.json`

**Details:**
auto_save.py provides comprehensive auto-save functionality with Emacs-style #filename# naming, but there are no keybindings defined for auto-save operations in either CLI or curses keybindings. The feature appears to be implemented but not integrated into any UI backend.

---

#### Code vs Comment conflict

**Description:** Comment about statement-level granularity contradicts the implementation claim

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
In _execute_single_step() method:

Docstring claims: "Execute a single statement (not a full line)."

But then the Note says: "Note: The actual statement-level granularity depends on the interpreter's implementation of tick()/execute_next(). These methods are expected to advance the program counter by one statement, handling colon-separated statements separately. If the interpreter executes full lines instead, this method will behave as line-level stepping rather than statement-level."

This indicates uncertainty about whether statement-level stepping is actually implemented, contradicting the confident claim in cmd_step() docstring that it "implements statement-level stepping".

---

#### Code vs Documentation inconsistency

**Description:** Readline keybindings documentation is separate from main keybindings file

**Affected files:**
- `src/ui/cli.py`
- `src/ui/cli_keybindings.json`

**Details:**
cli.py contains get_additional_keybindings() function that returns readline keybindings (Ctrl+E, Ctrl+K, Ctrl+U, etc.) with comment: "These are readline keybindings that are handled by Python's readline module, not by the keybinding system. They're documented here for completeness."

However, cli_keybindings.json only documents MBASIC-specific commands (RUN, SAVE, LOAD, etc.) and doesn't include these readline bindings. This creates two separate sources of truth for CLI keybindings, which could lead to incomplete documentation.

---

#### Documentation inconsistency

**Description:** Settings widget keybindings don't match curses keybindings file

**Affected files:**
- `src/ui/curses_settings_widget.py`
- `src/ui/curses_keybindings.json`

**Details:**
curses_settings_widget.py footer shows keybindings:
- Enter = OK
- ESC/Ctrl+S = Cancel
- Ctrl+A = Apply
- Ctrl+R = Reset

But curses_keybindings.json doesn't have a 'settings' section documenting these keybindings. The main editor section shows Ctrl+R is used for "Run program", which conflicts with the settings widget using Ctrl+R for "Reset to Defaults".

---

#### Code vs Documentation inconsistency

**Description:** CLIBackend delegates to InteractiveMode but base class suggests backends should implement logic directly

**Affected files:**
- `src/ui/cli.py`
- `src/ui/base.py`

**Details:**
base.py UIBackend docstring describes backends as combining "IOHandler for input/output, ProgramManager for program storage/editing, InterpreterEngine for execution, UI-specific interaction loop"

However, cli.py CLIBackend doesn't implement any of this logic directly - it just wraps InteractiveMode and delegates everything to it. The comment in cli.py says "Implementation: Wraps the existing InteractiveMode class to reuse its command parsing and execution logic."

This suggests CLIBackend is more of an adapter pattern than a true implementation of the UIBackend interface as described.

---

#### code_vs_comment

**Description:** Comment claims line numbers use 1-5 digits, but code implements variable-width line numbers

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Class docstring says:
"Display format: 'S<linenum> CODE' where:
- Field 1 (1 char): Status
- Field 2 (variable width): Line number (1-5 digits, no padding)"

But implementation in _format_line() uses:
line_num_str = f"{line_num}"

This allows line numbers beyond 5 digits (up to 99999 based on code in keypress method). The '1-5 digits' constraint is not enforced.

---

#### code_vs_comment

**Description:** Comment in _parse_line_number says 'NN' for line number but implementation supports variable width

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Method docstring says:
"Format: 'SNN CODE' where S=status, NN=line number (variable width)"

The 'NN' notation suggests 2 digits, but the comment correctly says '(variable width)'. However, the example is misleading. The implementation actually supports 1-5+ digits based on the code.

---

#### internal_inconsistency

**Description:** Inconsistent line number maximum limits throughout code

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In keypress() method for auto-numbering:
if next_num >= 99999 or attempts > 10:

In _parse_line_numbers() method:
parsed_lines.append((999999 + idx, line))

Two different maximum values used: 99999 for auto-numbering limit, but 999999 as a sentinel value for unparseable lines. This suggests inconsistent assumptions about maximum line numbers.

---

#### code_vs_comment

**Description:** Comment about 'is None' check doesn't match the actual concern

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _display_syntax_errors():
"# Check if output walker is available (use 'is None' instead of 'not' to avoid false positive on empty walker)
if self._output_walker is None:

The comment suggests an empty walker would cause 'not self._output_walker' to be True, but walkers are objects and would be truthy even when empty. The 'is None' check is correct, but the justification in the comment is misleading.

---

#### code_vs_comment

**Description:** Comment claims editor_lines stores execution state while editor.lines stores editing state, but code shows they are synchronized and serve overlapping purposes

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~200 says:
# Note: self.editor_lines stores execution state (lines loaded from file for RUN)
# self.editor.lines (in ProgramEditorWidget) stores the actual editing state
# These serve different purposes and are synchronized as needed

However, _save_editor_to_program() (line ~165) syncs editor.lines -> program, and _refresh_editor() (line ~230) syncs program -> editor.lines. The _sync_program_to_editor() method (referenced line ~1050) would sync program -> editor_lines. This suggests both store similar line data, not clearly different 'execution' vs 'editing' states.

---

#### code_vs_comment

**Description:** Comment claims ImmediateExecutor is recreated in start() but interpreter is reused, yet both are recreated together

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~248 says:
# ImmediateExecutor Lifecycle:
# Created here with temporary IO handler (to ensure attribute exists),
# then recreated in start() with a fresh OutputCapturingIOHandler.
# Note: The interpreter (self.interpreter) is created once here and reused.
# Only the executor and its IO handler are recreated in start().

However, code at line ~1021 shows:
self.immediate_executor = ImmediateExecutor(self.runtime, self.interpreter, immediate_io)

The interpreter is passed to the new executor, so it IS reused (comment is correct), but the phrasing 'Only the executor and its IO handler are recreated' could be clearer that the interpreter reference is passed to the new executor.

---

#### code_vs_comment

**Description:** Comment claims status bar stays at default but code shows status bar is updated in multiple places

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple comments claim 'Status bar stays at default (STATUS_BAR_SHORTCUTS)' but code shows status bar is actively updated:

Line ~1330: self.status_bar.set_text(f"Paused at {pc_display} - ...")
Line ~1338: # Status bar stays at default (STATUS_BAR_SHORTCUTS) - error message is in output
Line ~1344: # Status bar stays at default (STATUS_BAR_SHORTCUTS) - completion message is in output

Similar pattern at lines ~1390, ~1398, ~1404 and ~1430, ~1438, ~1444.

The comments say status bar 'stays at default' but code shows it's set to specific messages during pause states. The comments appear to be outdated or incorrect.

---

#### code_vs_comment

**Description:** Comment about positioning cursor at column 1 contradicts actual positioning logic

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1510 says:
# Always position at column 1 (start of line number field)

But code at lines ~1512-1518 shows:
if line_index > 0:
    new_cursor_pos = sum(len(lines[i]) + 1 for i in range(line_index)) + 1
else:
    new_cursor_pos = 1  # First line, column 1

The calculation 'sum(...) + 1' positions at column 1 of the target line (after newlines), but the comment suggests this is always column 1 of the line number field. The code is correct but the comment is misleading about what 'column 1' means in this context.

---

#### code_vs_comment

**Description:** Comment claims breakpoints are stored in editor as authoritative source and re-applied after reset, but code shows breakpoints are cleared during reset_for_run() and then re-applied from editor.breakpoints

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1157 states:
"Note: reset_for_run() clears variables and resets PC. Breakpoints are STORED in
the editor (self.editor.breakpoints) as the authoritative source, not in runtime.
This allows them to persist across runs. After reset_for_run(), we re-apply them
to the interpreter below via set_breakpoint() calls so execution can check them."

This is accurate and matches the code at lines ~1185-1188:
"# Re-apply breakpoints from editor
# Breakpoints are stored in editor UI state and must be re-applied to interpreter
# after reset_for_run (which clears them)
for line_num in self.editor.breakpoints:
    self.interpreter.set_breakpoint(line_num)"

However, the comment's phrasing could be clearer about the two-phase storage model.

---

#### code_vs_comment

**Description:** Comment about statement-level precision for GOSUB contradicts the actual display format

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1099 states:
"# Show statement-level precision for GOSUB return address
# return_stmt is statement offset (0-based index): 0 = first statement, 1 = second, etc."

But the code at line ~1102 displays:
"line = f\"{indent}GOSUB from line {entry['from_line']}.{return_stmt}\""

This shows the statement offset in the display, which matches the comment. However, the comment's emphasis on 'statement-level precision' might be misleading since it's just displaying the raw offset value without additional context about what statement that represents.

---

#### internal_inconsistency

**Description:** Inconsistent handling of status bar updates after errors across different error paths

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Parse errors (line ~1149): "# Status bar stays at default - error is displayed in output"
Startup errors (line ~1213): "# Status bar stays at default (STATUS_BAR_SHORTCUTS) - error is in output"
Undefined line errors (line ~1244): "# Status bar stays at default (STATUS_BAR_SHORTCUTS) - error is in output"
Runtime errors (line ~1336): "# Status bar stays at default - error is displayed in output"

But unexpected errors (line ~1306): "self.status_bar.set_text('Internal error - See output')"

The inconsistency is that most error paths leave status bar unchanged (relying on default STATUS_BAR_SHORTCUTS), but unexpected errors explicitly set a status message. This creates an inconsistent user experience.

---

#### code_vs_comment

**Description:** Comment claims ESC sets stopped=True similar to STOP statement, but code actually sets runtime.stopped=True which is the correct field

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _get_input_for_interpreter method:
Comment says: "# Note: This sets stopped=True similar to a BASIC STOP statement, but the semantics"
But code does: "self.runtime.stopped = True"
The comment is imprecise - it should say "sets runtime.stopped=True" not just "stopped=True"

---

#### code_vs_comment

**Description:** Comment in _execute_immediate says 'No state checking - just ask the interpreter' but then immediately checks self.interpreter existence

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment: "# Check if interpreter has work to do (after RUN statement)
# No state checking - just ask the interpreter"
Code: "has_work = self.interpreter.has_work() if self.interpreter else False
if self.interpreter and has_work:"

The code does check self.interpreter state twice, contradicting the 'no state checking' comment.

---

#### code_vs_comment

**Description:** Comment in cmd_delete and cmd_renum says 'Updates self.program immediately (source of truth), then syncs to runtime' but passes runtime=None to helper functions

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In cmd_delete:
Comment: "Note: Updates self.program immediately (source of truth), then syncs to runtime."
Code: "deleted = delete_lines_from_program(self.program, args, runtime=None)"

In cmd_renum:
Comment: "Note: Updates self.program immediately (source of truth), then syncs to runtime."
Code: "old_lines, line_map = renum_program(..., runtime=None)"

Passing runtime=None suggests the helper functions don't sync to runtime directly, which matches the code calling _sync_program_to_runtime() afterward. The comment is misleading about when/how syncing happens.

---

#### internal_inconsistency

**Description:** Inconsistent handling of self.io_handler initialization - checked with hasattr in _execute_immediate but not in _run_program

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _execute_immediate:
"if not hasattr(self, 'io_handler') or self.io_handler is None:"

This suggests io_handler might not exist as an attribute, but _run_program likely creates it without this check. This could lead to inconsistent state.

---

#### code_vs_comment_conflict

**Description:** Maintenance comment lists incorrect line numbers for footer text assignments

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at line ~73 states:
"MAINTENANCE: If help navigation keys change, update:
1. All footer text assignments (search for 'self.footer' in this file - multiple locations):
   - Initial footer (line ~73 below)
   - _cancel_search() around line ~166
   - _execute_search() around lines ~185, ~204, ~212
   - _start_search() around line ~159
   - keypress() search mode around lines ~444, ~448"

These line numbers appear to be outdated. The actual locations in the provided code are:
- Initial footer: line ~73 (correct)
- _cancel_search(): line ~166 (needs verification)
- _execute_search(): lines ~185, ~204, ~212 (needs verification)
- _start_search(): line ~159 (needs verification)
- keypress() search mode: lines ~444, ~448 (needs verification)

The line numbers may have shifted during code evolution.

---

#### code_vs_comment_conflict

**Description:** Comment about tier label determination doesn't match code logic

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at line ~143 states:
"Note: Tier labels are determined from tier_labels dict ('language', 'mbasic'), startswith('ui/') check for UI tiers ('ui/curses', 'ui/tk'), or '📙 Other' fallback."

But the actual code at lines ~157-162 shows:
tier_name = file_info.get('tier', '')
if tier_name.startswith('ui/'):
    tier_label = '📘 UI'
else:
    tier_label = tier_labels.get(tier_name, '📙 Other')

The comment mentions 'ui/curses' and 'ui/tk' as examples, but the code only checks startswith('ui/') and assigns '📘 UI' to all UI tiers, not distinguishing between specific UIs. The comment is slightly misleading about the granularity.

---

#### code_vs_documentation_inconsistency

**Description:** Both files load keybindings from JSON but have different explanatory comments about their purpose

**Affected files:**
- `src/ui/help_macros.py`
- `src/ui/keybinding_loader.py`

**Details:**
help_macros.py comment at line ~28:
"Note: This loads the same keybinding JSON files as keybinding_loader.py, but for a different purpose: macro expansion in help content (e.g., {{kbd:run}} -> \"^R\") rather than runtime event handling. This is separate from help_widget.py which uses hardcoded keys for navigation within the help system itself."

keybinding_loader.py comment at line ~28:
"Note: This loads keybindings for runtime event handling (binding keys to actions). help_macros.py loads the same JSON files but for macro expansion in help content (e.g., {{kbd:run}} -> \"^R\"). Both read the same data but use it differently: KeybindingLoader for runtime key event handling, HelpMacros for documentation display."

Both comments correctly describe the relationship, but they're slightly redundant. The help_macros.py comment also mentions help_widget.py using hardcoded keys, which creates a three-way relationship that could be confusing.

---

#### code_vs_comment_conflict

**Description:** Comment about link mapping doesn't match actual implementation behavior

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at line ~289 states:
"Build a mapping from visual link indices (all [text] patterns) to renderer link indices (only links with targets). This allows us to show all [text] as clickable, but only follow the ones that have actual targets from the renderer."

However, the code at lines ~313-318 shows:
if key in renderer_links_map:
    self.visual_to_renderer_link[visual_idx] = renderer_links_map[key]
else:
    self.visual_to_renderer_link[visual_idx] = None
    if link_url:
        self.visual_link_urls[visual_idx] = link_url

The implementation actually handles [text](url) patterns by extracting the URL directly, not just mapping to renderer links. The comment should mention this dual behavior: mapping to renderer links when available, OR extracting direct URLs from [text](url) format.

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

Comment doesn't explain that QUIT_KEY is None but QUIT_ALT_KEY is used in the help display. Also, STOP_KEY comment says it's shown in debugger context, but looking at line 250, STOP_KEY IS included in the Debugger category.

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

#### code_vs_comment

**Description:** Comment states immediate_history and immediate_status are 'always None' but code sets them to None explicitly

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Lines 293-297 comment: 'Note: immediate_history and immediate_status are always None in Tk UI (see lines 293-297)'
Lines 293-297 code:
# Set immediate_history and immediate_status to None
# These attributes are not currently used but are set to None for defensive programming
# in case future code tries to access them (will get None instead of AttributeError)
self.immediate_history = None
self.immediate_status = None

The comment at line 293 references itself ('see lines 293-297'), creating a circular reference. The comment also says they are 'always None' but the code comment says they're set 'for defensive programming', suggesting they might be used in the future.

---

#### code_vs_comment

**Description:** Comment about _ImmediateModeToken usage references wrong line number

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Class docstring for _ImmediateModeToken (lines 20-27):
'This class is instantiated when editing variables via the variable inspector
(see _on_variable_edit() around line 1194).'

However, the provided code only goes up to line 1194 and does not show _on_variable_edit() method. The method _edit_simple_variable is shown starting at line 1186, which may be the intended reference. The line number reference appears to be outdated or incorrect.

---

#### code_vs_comment

**Description:** Comment about arrow click width uses pixel value but doesn't explain why that specific value

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_variable_heading_click() (lines 1127-1128):
'# Determine click action based on horizontal position within column header:
# - Left 20 pixels (arrow area) = toggle sort direction
# - Rest of header = cycle/set sort column
ARROW_CLICK_WIDTH = 20  # Width of clickable arrow area in pixels'

The comment documents the behavior but doesn't explain why 20 pixels was chosen. This magic number should be justified (e.g., 'typical arrow icon width', 'matches Tkinter default', etc.).

---

#### code_vs_comment

**Description:** Comment claims formatting may occur elsewhere, but contradicts itself about editor formatting

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _refresh_editor method around line 1247:
Comment says: "# Insert line exactly as stored from program manager - no formatting applied here\n# to preserve compatibility with real MBASIC for program text.\n# (Note: \"formatting may occur elsewhere\" refers to the Variables and Stack windows,\n# which DO format data for display - not the editor/program text itself)"

This comment is confusing because it says "no formatting applied here" but then mentions "formatting may occur elsewhere" which could be misread as applying to the editor. The clarification helps but the phrasing is awkward.

---

#### code_vs_comment

**Description:** Comment about when _remove_blank_lines is called contradicts potential future usage

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _remove_blank_lines method around line 1577:
Comment says: "Currently called only from _on_enter_key (after each Enter key press), not\nafter pasting or other modifications."

This comment describes current behavior but doesn't explain why it's limited to Enter key only. If blank line removal is desirable, why not after paste? The comment suggests this might be incomplete implementation rather than intentional design.

---

#### code_vs_comment

**Description:** Comment about showing error list contradicts the condition logic

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _validate_editor_syntax method around line 1523:
Comment says: "# Only show full error list in output if there are multiple errors.\n# For single errors, the red ? icon in the editor is sufficient feedback.\n# This avoids cluttering the output pane with repetitive messages during editing."

Then code:
should_show_list = len(errors_found) > 1
if should_show_list:
    self._add_output("\n=== Syntax Errors ===\n")
    ...

The comment says "multiple errors" but the code checks > 1, which means 2 or more. This is technically correct but the comment could be clearer. More importantly, the comment doesn't explain why single errors shouldn't be shown - it just asserts they're sufficient with the icon.

---

#### code_vs_comment

**Description:** Comment claims CONT clears stopped/halted flags and resumes tick-based execution, but code only clears flags without actually resuming execution

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment at line ~2180 says:
"Clear stopped and halted flags to resume execution"
and
"When CONT is executed, tick() will continue from runtime.pc"

But the code only does:
self.runtime.stopped = False
self.runtime.halted = False

There is no call to start tick-based execution (no self.running = True, no self.root.after() to schedule _execute_tick). The comment implies execution will resume automatically, but the code doesn't actually restart the execution loop.

---

#### code_vs_comment

**Description:** Comment claims _smart_insert_line won't save blank numbered line to program, but doesn't explain why this is safe

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
At line ~1780 in _smart_insert_line():
Comment: "DON'T save to program yet - the line only has a line number with no statement, so _save_editor_to_program() will skip it (only saves lines with statements)."

This creates an inconsistency: the editor shows a line that doesn't exist in the program. The comment explains the line won't be saved, but doesn't address potential issues:
1. What if user clicks away without typing?
2. What if _check_line_change() triggers and tries to sort a line that doesn't exist in program?
3. The line won't be removed by _remove_blank_lines() because it has a line number, creating a persistent ghost line.

---

#### code_vs_comment

**Description:** Comment claims cursor moves to end of current line on parse error, but code uses different index format

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_enter() at line ~1230:
Comment: "Just move cursor to end of current line"
Code: self.editor_text.text.mark_set(tk.INSERT, f'{current_line_index}.end')

The code uses '.end' which is a Tk text widget index meaning 'end of line', but the comment doesn't clarify this is a Tk-specific index format. This could be confusing since earlier in the same function, numeric column indices are used (e.g., f'{insert_at_index}.{len(str(new_line_num)) + 1}').

---

#### code_vs_comment

**Description:** Comment claims GUI design choice deviates from typical BASIC by not echoing commands, but this contradicts the actual behavior where input IS echoed to output

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_immediate() method:
Comment says: "Execute without echoing (GUI design choice that deviates from typical BASIC behavior: command is visible in entry field, and 'Ok' prompt is unnecessary in GUI context - only results are shown. Traditional BASIC echoes to output.)"

But later in the same method when handling INPUT:
Code: self._add_output(value + '\n')  # Echoes input to output

And in TkIOHandler.input():
Code: self.output(result)  # Echoes input to output

The comment describes not echoing commands, but the code clearly echoes INPUT responses to output.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate() describes checking has_work() as 'the only location' but doesn't clarify if this is enforced or just observational

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment: "Use has_work() to check if the interpreter is ready to execute (e.g., after RUN command). This is the only location in tk_ui.py that calls has_work()."

This comment makes a claim about being 'the only location' but doesn't explain why this constraint exists or if it's enforced. If it's a critical design constraint, it should be documented more clearly. If it's just an observation, the phrasing is misleading.

---

#### code_vs_comment

**Description:** Comment about input_line() says it ALWAYS uses modal dialog, but this contradicts the class-level docstring that says it's availability-based

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
input_line() docstring: "Unlike input() which prefers inline input field, this ALWAYS uses a modal dialog regardless of backend availability."

But class-level docstring says: "LINE INPUT statement: Always uses modal dialog for consistent UX"

The method docstring emphasizes 'regardless of backend availability' suggesting this is a deliberate choice even when backend IS available, but the class docstring says it's 'for consistent UX' without mentioning the availability aspect. The reasoning is inconsistent.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate() about not calling interpreter.start() explains avoiding PC reset, but the subsequent code only sets halted flag and is_first_line without explaining why this is sufficient

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment: "NOTE: Don't call interpreter.start() because it calls runtime.setup() which resets PC to the first statement. The RUN command has already set PC to the correct line (e.g., RUN 120 sets PC to line 120). We only need to clear the halted flag and mark this as first line. This avoids the full initialization that start() does:\n  - runtime.setup() (rebuilds tables, resets PC)\n  - Creates new InterpreterState\n  - Sets up Ctrl+C handler"

Code only does:
self.runtime.halted = False
self.interpreter.state.is_first_line = True

The comment lists 3 things that start() does, but doesn't explain why skipping 'Creates new InterpreterState' and 'Sets up Ctrl+C handler' is safe. This could lead to bugs if those are actually needed.

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

But _on_status_click() implementation shows:
```python
error_msg = self.get_error_message(line_num)
if error_msg:
    messagebox.showerror(...)
else:
    # Has breakpoint, not error
    metadata = self.line_metadata.get(line_num, {})
    if metadata.get('has_breakpoint'):
        messagebox.showinfo(...)
```

This suggests the UI can display information about breakpoints when errors are cleared, which matches the docstring. However, the comment '# Has breakpoint, not error' in the else block confirms the priority system works as documented.

---

#### code_vs_comment

**Description:** _delete_line() docstring has confusing explanation about dual numbering that may not match actual usage

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Docstring says:
"Args:
    line_num: Tkinter text widget line number (1-based sequential index),
             not BASIC line number (e.g., 10, 20, 30).
             Note: This class uses dual numbering - editor line numbers for
             text widget operations, BASIC line numbers for line_metadata lookups."

However, the method is only called from _on_cursor_move() with self.current_line, which is set from:
```python
cursor_pos = self.text.index(tk.INSERT)
new_line = int(cursor_pos.split('.')[0])
```

This is indeed a Tkinter line number (editor line), so the docstring is correct. But the 'Note' about dual numbering seems unnecessary here since this method only uses editor line numbers, never BASIC line numbers.

---

#### code_vs_comment

**Description:** _redraw() docstring mentions _parse_line_number() validation details that are implementation-specific and may become outdated

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Docstring says:
"Note: BASIC line numbers are part of the text content (not drawn separately
in the canvas). See _parse_line_number() for the regex-based extraction logic
that validates line number format (requires whitespace or end-of-string after
the number)."

This duplicates implementation details from _parse_line_number(). If the regex changes, this comment becomes outdated. The reference to 'see _parse_line_number()' is sufficient without repeating the validation rules.

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

However, the code only sets relative_indent=1 as initial default before checking source_text. If source_text exists but doesn't match the pattern, relative_indent remains 1 (the default), but this is not because of an explicit fallback - it's because the if match: block never executes. The comment implies a deliberate fallback mechanism, but the code just uses the initial default value.

---

#### code_vs_comment

**Description:** Comment in serialize_statement() describes prevention strategy but implementation may not handle all statement types

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment states: "Prevention strategy: Explicitly fail (with ValueError) rather than silently omitting
statements during RENUM, which would corrupt the program.
All statement types must be handled above - if we reach here, serialization failed."

The else clause raises ValueError for unhandled statement types, which is good. However, the comment claims "All statement types must be handled above" but there's no verification that the handled types match all possible statement types in the AST. If new statement types are added to the parser, they won't be caught until runtime during RENUM.

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

**Description:** Comment claims PC preservation logic prevents accidental execution starts, but code actually handles state preservation during statement table rebuilds

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _sync_program_to_runtime() method:

Comment says: "# This logic is about PRESERVING vs RESETTING state, not about preventing accidental starts"

But earlier comment says: "# Otherwise (no active execution): Resets PC to halted state, preventing
# unexpected execution when LIST/edit commands modify the program."

The word 'preventing' in the second comment contradicts the clarification that this is 'not about preventing accidental starts'. The logic resets PC when timer is inactive to maintain halted state after program modifications, which does prevent unexpected execution.

---

#### code_vs_comment

**Description:** Comment describes dual input mechanism but doesn't explain why both are needed or when each is used

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _handle_output_enter() method:

Comment says: "# Provide input to interpreter via TWO mechanisms (we check both in case either is active):
# 1. interpreter.provide_input() - Used when interpreter is waiting synchronously
#    (checked via interpreter.state.input_prompt). Stores input for retrieval.
# 2. input_future.set_result() - Used when async code is waiting via asyncio.Future
#    (see _get_input_async method). Only one path will be active at a time, but we
#    check both to handle whichever path the interpreter is currently using."

The comment says 'Only one path will be active at a time' but then says 'we check both in case either is active'. This is confusing - if only one is active, why check both? The comment should clarify that we don't know which path is active, so we try both.

---

#### code_vs_comment

**Description:** Comment in _serialize_runtime says 'Handles complex objects like AST nodes using pickle' but the shown code doesn't demonstrate pickle usage

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _serialize_runtime() method:

Docstring says: "Serialize runtime state.

Handles complex objects like AST nodes using pickle.

Returns:
    dict: Serialized runtime state"

The code shown imports pickle and closes files, but the actual serialization of AST nodes using pickle is not visible in the provided code snippet. This makes it unclear if pickle is actually used or if the comment is outdated.

---

#### code_vs_comment

**Description:** Comment claims 'errors are caught and logged, won't crash the UI' but the timer callback save_state_periodic() catches exceptions internally, so the comment is accurate for the timer but potentially misleading about general error handling

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment at line ~470: '# Save state periodically (errors are caught and logged, won't crash the UI)'
Code shows save_state_periodic() does catch exceptions:
    def save_state_periodic():
        try:
            app.storage.client['session_state'] = backend.serialize_state()
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to save session state: {e}\n")
            sys.stderr.flush()

The comment is accurate but could be clearer that it refers specifically to the timer callback's error handling.

---

#### code_vs_comment

**Description:** Comment says 'Save state on disconnect' but the callback save_on_disconnect() is registered with on_disconnect which may not fire reliably in all disconnect scenarios (browser crash, network loss, etc.)

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
At line ~474:
        # Save state on disconnect
        def save_on_disconnect():
            try:
                app.storage.client['session_state'] = backend.serialize_state()
            except Exception as e:
                sys.stderr.write(f"Warning: Failed to save final session state: {e}\n")
                sys.stderr.flush()

        ui.context.client.on_disconnect(save_on_disconnect)

The comment doesn't mention that this is best-effort and may not fire in all disconnect scenarios. The periodic save (every 5 seconds) provides backup, but the comment could be clearer about reliability.

---

#### documentation_inconsistency

**Description:** Debugging documentation uses placeholder syntax {{kbd:step:curses}} for keyboard shortcuts, but web_keybindings.json shows actual keybindings. Documentation should reference actual keys or explain the placeholder system.

**Affected files:**
- `docs/help/common/debugging.md`
- `src/ui/web_keybindings.json`

**Details:**
debugging.md uses: '{{kbd:step:curses}}', '{{kbd:continue:curses}}', '{{kbd:quit:curses}}', '{{kbd:toggle_stack:tk}}'

web_keybindings.json shows actual keys:
- step: F10
- continue: F5
- stop: Esc
- toggle_variables: Ctrl+Alt+V

The placeholder syntax suggests a template system that should be resolved before display, but this is not explained.

---

#### code_vs_documentation

**Description:** SessionState class tracks auto_save_enabled and auto_save_interval, but these features are not documented in any help files.

**Affected files:**
- `src/ui/web/session_state.py`
- `docs/help/common/debugging.md`

**Details:**
session_state.py defines:
    auto_save_enabled: bool = True
    auto_save_interval: int = 30

These configuration options are not mentioned in:
- debugging.md
- editor-commands.md
- Any settings documentation

Users cannot discover or configure these features.

---

#### code_vs_comment

**Description:** Migration guide comment suggests using ui.navigate.to() for NiceGUI, but this function is not imported or available in the module.

**Affected files:**
- `src/ui/web_help_launcher.py`

**Details:**
Comment states:
'NEW: In NiceGUI backend, use: ui.navigate.to(\'/mbasic_docs/statements/print.html\', new_tab=True)'

However, the module only imports:
from pathlib import Path
from typing import Optional

No NiceGUI imports exist. The comment provides guidance for code that cannot be executed from this module.

---

#### code_vs_documentation

**Description:** Settings dialog exists in code with auto-numbering configuration, but no documentation explains how to access or use the settings dialog.

**Affected files:**
- `src/ui/web/web_settings_dialog.py`
- `docs/help/common/debugging.md`
- `docs/help/common/editor-commands.md`

**Details:**
web_settings_dialog.py implements:
- Settings dialog with tabs (Editor, Limits)
- Auto-numbering enable/disable
- Auto-number step configuration
- Save/Cancel functionality

No documentation covers:
- How to open settings dialog
- What settings are available
- How settings affect editor behavior
- Where settings are stored

The dialog references 'backend.settings_manager' but settings system is not documented.

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

**Description:** Inconsistent information about ATN precision and PI calculation

**Affected files:**
- `docs/help/common/language/functions/atn.md`
- `docs/help/common/language/appendices/math-functions.md`

**Details:**
atn.md states 'the evaluation of ATN is always performed in single precision (~7 significant digits)' and includes a note about using CDBL for higher precision PI. However, math-functions.md shows 'PI# = ATN(CDBL(1)) * 4' in the 'Computing Pi' section but also shows 'PI = ATN(1) * 4' with comment 'Single-precision approximation'. The atn.md note says 'For higher precision, use ATN(CDBL(1)) * 4 to get double precision' which contradicts the statement that ATN is always single precision.

---

#### documentation_inconsistency

**Description:** Inconsistent precision specifications for SINGLE and DOUBLE types

**Affected files:**
- `docs/help/common/language/data-types.md`
- `docs/help/common/language/functions/cdbl.md`
- `docs/help/common/language/functions/csng.md`

**Details:**
data-types.md states SINGLE has 'approximately 7 digits' precision and DOUBLE has 'approximately 16 digits'. However, cdbl.md says 'approximately 16 digits of precision' for DOUBLE (consistent) but csng.md says 'approximately 7 digits of precision' for SINGLE (consistent). The ranges differ slightly: data-types.md shows '±2.938736×10^-39 to ±1.701412×10^38' for SINGLE, while csng.md shows '±2.938736×10^-39 to ±1.701412×10^38' (same). For DOUBLE, data-types.md shows '±2.938736×10^-308 to ±1.797693×10^308' while cdbl.md shows '±2.938736×10^-308 to ±1.797693×10^308' (same). Actually these are consistent - no issue here.

---

#### documentation_inconsistency

**Description:** Duplicate ASCII information with different levels of detail

**Affected files:**
- `docs/help/common/language/character-set.md`
- `docs/help/common/language/appendices/ascii-codes.md`

**Details:**
character-set.md has a 'Control Characters' section listing common control characters (7, 8, 9, 10, 13, 27) while ascii-codes.md has a complete 'Control Characters (0-31)' table. The character-set.md should reference the complete table in ascii-codes.md rather than duplicating partial information.

---

#### documentation_inconsistency

**Description:** LOF function missing from index.md categorization but has its own documentation file

**Affected files:**
- `docs/help/common/language/functions/index.md`
- `docs/help/common/language/functions/lof.md`

**Details:**
The index.md file lists LOF in the alphabetical quick reference at the bottom, but does not include it in the 'File I/O Functions' category section at the top. LOF is documented in lof.md as a Disk version function that returns file length in bytes.

---

#### documentation_inconsistency

**Description:** Inconsistent Control-C behavior documentation

**Affected files:**
- `docs/help/common/language/functions/inkey_dollar.md`
- `docs/help/common/language/functions/input_dollar.md`

**Details:**
Both INKEY$ and INPUT$ document Control-C behavior, but with slightly different wording:

INKEY$: 'Note: Control-C behavior varied in original implementations. In MBASIC 5.21 interpreter mode, Control-C would terminate the program. This implementation passes Control-C through (CHR$(3)) for program detection and handling, allowing programs to detect and handle it explicitly.'

INPUT$: 'Note: Control-C behavior: This implementation passes Control-C through (CHR$(3)) for program detection and handling, allowing programs to detect and handle it explicitly.'

The INPUT$ version is shorter and doesn't mention the historical MBASIC 5.21 behavior. These should be consistent.

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

This is confusing because the documentation is for MBASIC 5.21 but includes historical information that contradicts the current behavior. The syntax section shows 'CLEAR [,[<expression1>] [,<expression2>]]' but doesn't clearly indicate which version's semantics apply.

---

#### documentation_inconsistency

**Description:** Index page claims 45 intrinsic functions and 77 statements but doesn't provide verification

**Affected files:**
- `docs/help/common/language/index.md`
- `docs/help/common/language/operators.md`

**Details:**
The index.md states:
'- [Functions](functions/index.md) - 45 intrinsic functions
- [Statements](statements/index.md) - 77 commands and statements'

These specific counts should be verifiable by counting the actual documented functions and statements, but no such verification is provided. If these numbers are from the original manual, they may not match the current implementation.

---

#### documentation_inconsistency

**Description:** DEF FN documentation shows inconsistent categorization

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`
- `docs/help/common/language/statements/index.md`

**Details:**
In def-fn.md, the category is 'functions' but in index.md it's listed under 'Functions' section. However, index.md also lists 'DEF USR' under 'Functions' while def-usr.md has category 'subroutines'. This creates confusion about whether DEF statements are categorized as functions or their own category.

---

#### documentation_inconsistency

**Description:** Contradictory information about CONT behavior after END

**Affected files:**
- `docs/help/common/language/statements/end.md`
- `docs/help/common/language/statements/stop.md`

**Details:**
end.md states: 'Can be continued with CONT (execution resumes at next statement after END)' and 'Note: Files remain closed if CONT is used after END'. However, this creates a logical inconsistency - if files are closed by END, continuing execution after END would resume with closed files, which could cause errors. The documentation doesn't clarify what happens to file operations after CONT following END.

---

#### documentation_inconsistency

**Description:** Inconsistent information about ERR reset behavior

**Affected files:**
- `docs/help/common/language/statements/err-erl-variables.md`
- `docs/help/common/language/statements/error.md`

**Details:**
err-erl-variables.md states 'ERR is reset to 0 when: RESUME statement is executed, A new RUN command is issued, An error handling routine ends normally (without error)'. However, it also states 'Both ERR and ERL persist after an error handler completes, until the next error or RESUME'. These two statements appear contradictory - does ERR reset when the error handler ends normally, or does it persist?

---

#### documentation_inconsistency

**Description:** Inconsistent information about INPUT# usage with random files

**Affected files:**
- `docs/help/common/language/statements/field.md`
- `docs/help/common/language/statements/get.md`

**Details:**
field.md states in remarks: 'FIELD does NOT place any data in the random file buffer. (See LSET/RSET and GET.)' but get.md states: 'After a GET statement, INPUT# and LINE INPUT# may be used to read characters from the random file buffer.' This suggests INPUT# can be used with random files after GET, but FIELD documentation doesn't mention this capability.

---

#### documentation_inconsistency

**Description:** See Also section references input_hash.md but uses inconsistent naming

**Affected files:**
- `docs/help/common/language/statements/inputi.md`

**Details:**
The 'See Also' section in inputi.md references:
- [INPUT#](input_hash.md) - Read data from sequential file

This uses 'input_hash.md' as the filename, but the current file is named 'inputi.md' (using 'i' suffix instead of '_hash'). There's an inconsistency in the naming convention for file I/O commands with #.

---

#### documentation_inconsistency

**Description:** Filename uses 'printi' but references use 'print_hash' pattern inconsistently

**Affected files:**
- `docs/help/common/language/statements/printi-printi-using.md`

**Details:**
The file is named 'printi-printi-using.md' but in other files' See Also sections, it's referenced as both:
- [PRINT#](printi-printi-using.md) in some places
- The pattern is inconsistent with input_hash.md reference in inputi.md

There should be a consistent naming convention: either all use '_hash' suffix or all use 'i' suffix for file I/O commands.

---

#### documentation_inconsistency

**Description:** Contradictory information about file closing behavior

**Affected files:**
- `docs/help/common/language/statements/load.md`
- `docs/help/common/language/statements/merge.md`

**Details:**
load.md states:
'**LOAD** (without ,R): Closes all open files and deletes all variables and program lines currently in memory before loading'
'**LOAD** with **,R** option: Program is RUN after loading, and all open data files are **kept open** for program chaining'
'Compare with **MERGE**: Never closes files (see [MERGE](merge.md))'

But merge.md states:
'**File handling:** Unlike LOAD (without ,R), MERGE does **NOT close open files**. Files that are open before MERGE remain open after MERGE completes. (Compare with [LOAD](load.md) which closes files except when using the ,R option.)'

The comparison statements are consistent, but the emphasis and wording could be clearer about the three cases: LOAD without ,R (closes files), LOAD with ,R (keeps files open), and MERGE (keeps files open).

---

#### documentation_inconsistency

**Description:** Implementation notes use different formatting and terminology

**Affected files:**
- `docs/help/common/language/statements/llist.md`
- `docs/help/common/language/statements/lprint-lprint-using.md`
- `docs/help/common/language/statements/out.md`
- `docs/help/common/language/statements/poke.md`

**Details:**
Multiple files have 'Implementation Note' sections for unimplemented features, but they use inconsistent formatting:

llist.md: '⚠️ **Not Implemented**: This feature requires line printer hardware...'
lprint-lprint-using.md: '⚠️ **Not Implemented**: This feature requires line printer hardware...'
out.md: '⚠️ **Emulated as No-Op**: This feature requires direct hardware I/O port access...'
poke.md: '⚠️ **Emulated as No-Op**: This feature requires direct memory access...'

The terms 'Not Implemented' vs 'Emulated as No-Op' should be used consistently. Both describe features that are parsed but don't perform their original function.

---

#### documentation_inconsistency

**Description:** Incomplete documentation of OPEN modes

**Affected files:**
- `docs/help/common/language/statements/open.md`

**Details:**
open.md states modes are 'O', 'I', 'R' but doesn't mention 'A' for append mode, which is referenced in printi-printi-using.md:

'PRINT# writes data to a sequential file opened for output (mode "O") or append (mode "A").'

The OPEN documentation should include all valid modes including append.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation for stopping AUTO mode

**Affected files:**
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/curses/editing.md`

**Details:**
CLI docs use '{{kbd:stop:cli}}' for stopping AUTO mode, while Curses docs use '{{kbd:continue:curses}}' for the same purpose. The placeholder syntax suggests these should resolve to actual key combinations, but the inconsistency in the placeholder names (stop vs continue) is confusing.

---

#### documentation_inconsistency

**Description:** Inconsistent information about Find and Replace availability

**Affected files:**
- `docs/help/common/ui/tk/index.md`
- `docs/help/mbasic/extensions.md`

**Details:**
Tk docs state 'Find and replace' as an editor feature and list 'Find' ({{kbd:find:tk}}) in keyboard shortcuts, but extensions.md states 'Find and Replace (Tk only)' in the comparison table. However, the Tk docs don't mention Replace command or shortcut explicitly, only Find.

---

#### documentation_inconsistency

**Description:** Inconsistent description of Web UI file naming behavior

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/extensions.md`

**Details:**
Compatibility.md states 'Automatically uppercased by the virtual filesystem (CP/M style)' and 'The uppercasing is a programmatic transformation for CP/M compatibility, not evidence of persistent storage'. This detailed explanation of uppercasing behavior is not mentioned at all in extensions.md's Web UI file storage section, which only mentions 'simple filenames only' without the uppercasing detail.

---

#### documentation_inconsistency

**Description:** Inconsistent PEEK behavior description

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/compatibility.md`

**Details:**
Architecture.md states 'PEEK: Returns random integer 0-255 (for RNG seeding compatibility)' while compatibility.md states the exact same thing. However, architecture.md is in a 'Hardware Compatibility Notes' section suggesting it's a general note, while compatibility.md presents it as an 'Intentional Difference'. The framing differs but content is identical.

---

#### documentation_inconsistency

**Description:** Incomplete STEP command documentation

**Affected files:**
- `docs/help/mbasic/extensions.md`

**Details:**
Extensions.md shows 'STEP INTO' and 'STEP OVER' with '(planned)' status, but doesn't clarify if basic 'STEP' and 'STEP 5' are fully implemented or also planned. The availability line says 'CLI (command form), Curses ({{kbd:step:curses}}/{{kbd:step_line:curses}}), Tk (UI controls)' suggesting implementation, but the planned features create ambiguity.

---

#### documentation_inconsistency

**Description:** Missing CLI debugging documentation reference

**Affected files:**
- `docs/help/common/ui/cli/index.md`
- `docs/help/mbasic/extensions.md`

**Details:**
CLI docs reference 'See Also: [CLI Debugging](../ui/cli/debugging.md)' but extensions.md also references the same file. However, this file is not provided in the documentation set, creating a broken link in multiple places.

---

#### documentation_inconsistency

**Description:** Inconsistent UI selection documentation structure

**Affected files:**
- `docs/help/index.md`
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/curses/editing.md`
- `docs/help/common/ui/tk/index.md`

**Details:**
The main index.md lists four UIs: 'Tk (Desktop GUI)', 'Curses (Terminal)', 'Web Browser', and 'CLI (Command Line)'. However, the actual documentation structure shows:
- cli/index.md exists
- curses/editing.md exists (but no curses/index.md)
- tk/index.md exists
- No web/ directory at all
This suggests either missing documentation or incorrect index references.

---

#### documentation_inconsistency

**Description:** Inconsistent count of user interfaces supported

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`
- `docs/help/mbasic/index.md`

**Details:**
features.md lists 'four interfaces' (CLI, Curses, Tkinter, Web) in the 'Choosing a User Interface' section.
getting-started.md also mentions 'four interfaces' and lists all four.
However, index.md states 'Choice of user interfaces (CLI, Curses, Tkinter)' - only three interfaces, omitting Web UI.
The Quick Start section in getting-started.md shows commands for all four UIs including Web.

---

#### documentation_inconsistency

**Description:** Conflicting information about CLS implementation

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
features.md lists CLS under 'Program Control' section without any caveats, suggesting full implementation.
not-implemented.md states: 'Basic CLS (clear screen) IS implemented in MBASIC - see [CLS](../common/language/statements/cls.md). The GW-BASIC extended CLS with optional parameters is not implemented.'
This clarification about 'basic CLS' vs 'extended CLS' is not mentioned in features.md, which could mislead users about what CLS features are available.

---

#### documentation_inconsistency

**Description:** Inconsistent STEP command capabilities

**Affected files:**
- `docs/help/ui/cli/debugging.md`
- `docs/help/mbasic/features.md`

**Details:**
cli/debugging.md documents STEP command with syntax: 'STEP [n]', 'STEP INTO', 'STEP OVER'
However, under 'Limitations' section it states: 'STEP INTO/OVER not yet implemented (use STEP)'
This is contradictory - the syntax section suggests these are available commands, but limitations say they're not implemented.
features.md lists 'Step execution' as available but doesn't clarify which STEP variants work.

---

#### documentation_inconsistency

**Description:** Inconsistent function count

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
features.md section 'Functions (50+)' claims '50+' functions are available.
However, getting-started.md links to 'Functions' documentation stating 'All 40 functions' in the CLI index.
This is a significant discrepancy (50+ vs 40) that needs clarification about the actual number of implemented functions.

---

#### documentation_inconsistency

**Description:** Unclear relationship between documented string management and implementation

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/implementation/string-allocation-and-garbage-collection.md`

**Details:**
features.md lists 'String' functions and operations but doesn't mention garbage collection or memory management behavior.
string-allocation-and-garbage-collection.md provides extensive detail about CP/M MBASIC's O(n²) garbage collection algorithm.
It's unclear whether this Python implementation uses the same algorithm, emulates it for compatibility, or uses Python's native garbage collection.
The doc states 'For implementing a compatible garbage collector for 8080 compilation' suggesting this is reference material, but doesn't clarify what the current Python implementation actually does.

---

#### documentation_inconsistency

**Description:** Unclear LOCATE implementation status

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
not-implemented.md states: 'LOCATE - Cursor positioning with row/column parameters (GW-BASIC version)' is not implemented.
features.md does not mention LOCATE at all, neither as implemented nor as not implemented.
This creates ambiguity about whether any form of LOCATE exists, or if cursor positioning is handled differently.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`
- `docs/help/ui/cli/index.md`

**Details:**
getting-started.md uses template notation: '{{kbd:run:curses}}', '{{kbd:save:curses}}', '{{kbd:help:curses}}', '{{kbd:quit:curses}}'
This suggests these are placeholders that should be replaced with actual key combinations.
features.md also uses this notation: '{{kbd:step_line:curses}}', '{{kbd:help:curses}}'
cli/index.md doesn't use this notation at all.
It's unclear whether this is intentional template syntax for a documentation build system, or if these should be replaced with actual keyboard shortcuts like 'F5', 'Ctrl+S', etc.

---

#### documentation_inconsistency

**Description:** Inconsistent information about variable editing capability

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/variables.md`

**Details:**
docs/help/ui/curses/feature-reference.md states under 'Variable Inspection (6 features)': '### Edit Variable Value (Not implemented)
⚠️ Variable editing is not available in Curses UI. You cannot directly edit values in the variables window. Use immediate mode commands to modify variable values instead.'

docs/help/ui/curses/variables.md states: '### Direct Editing Not Available
⚠️ **Not Implemented**: You cannot edit variable values directly in the variables window.'

Both documents agree the feature is not implemented, but feature-reference.md lists it as a feature (with 'Not implemented' tag), while variables.md describes it as a limitation. This is inconsistent categorization of the same missing functionality.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut documentation for Execution Stack

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
docs/help/ui/curses/feature-reference.md states: '### Execution Stack
View the call stack showing:

**Access methods:**
- Via menu: Ctrl+U → Debug → Execution Stack
- Via command: Type `STACK` in immediate mode (same as CLI)'

docs/help/ui/curses/quick-reference.md lists under 'Global Commands': '| **Menu only** | Toggle execution stack window |'

The feature-reference says 'Ctrl+U → Debug → Execution Stack' (menu navigation) while quick-reference says 'Menu only' without specifying the path. Additionally, feature-reference mentions the STACK command which is not mentioned in quick-reference.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut for Settings Widget

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/settings.md`

**Details:**
docs/help/ui/curses/feature-reference.md states: '### Settings Widget (Menu only)
Interactive settings dialog for configuring MBASIC behavior. Adjust auto-numbering, keyword case style, variable handling, themes, and more.
**Note:** Access via menu only - no keyboard shortcut assigned.'

docs/help/ui/curses/settings.md states: '## Opening the Settings Widget

**Keyboard shortcut:** `Ctrl+,`

Or navigate to the settings menu item if available in your version.'

These directly contradict each other - one says menu only, the other documents Ctrl+, as the keyboard shortcut.

---

#### documentation_inconsistency

**Description:** Inconsistent sort mode descriptions

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
docs/help/ui/curses/variables.md states: '**Sort Modes:**
- **Accessed**: Most recently accessed (read or written) - default, newest first
- **Written**: Most recently written to - newest first
- **Read**: Most recently read from - newest first
- **Name**: Alphabetically by variable name - A to Z'

docs/help/ui/curses/feature-reference.md states: '### Variable Sorting (s key in variables window)
Cycle through different sort orders:
- **Accessed**: Most recently accessed (read or written) - newest first
- **Written**: Most recently written to - newest first
- **Read**: Most recently read from - newest first
- **Name**: Alphabetically by variable name'

The 'Name' sort description differs slightly - variables.md says 'A to Z' while feature-reference.md just says 'Alphabetically by variable name'. Also, variables.md says Accessed is 'default' but feature-reference.md doesn't mention which is default.

---

#### documentation_inconsistency

**Description:** Inconsistent save keyboard shortcut documentation

**Affected files:**
- `docs/help/ui/curses/quick-reference.md`
- `docs/help/ui/curses/files.md`

**Details:**
docs/help/ui/curses/quick-reference.md states: '| **{{kbd:save:curses}}** | Save program (Ctrl+S unavailable - terminal flow control) |'

docs/help/ui/curses/files.md states: '1. Press **{{kbd:save:curses}}** to save (Ctrl+S unavailable - terminal flow control)'

Both documents mention Ctrl+S is unavailable but use {{kbd:save:curses}} template. The actual key is not clearly documented - readers don't know what key to press. The template should resolve to an actual key combination.

---

#### documentation_inconsistency

**Description:** Inconsistent count of File Operations features

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/features.md`

**Details:**
feature-reference.md header states '## File Operations (8 features)' but then lists:
1. New Program
2. Open/Load File
3. Save File
4. Save As
5. Recent Files
6. Auto-Save
7. Delete Lines
8. Merge Files

However, 'Delete Lines' is listed under 'Edit' menu in the description, not 'File' menu, suggesting it may not belong in File Operations category.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut references for Run Program

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/getting-started.md`

**Details:**
feature-reference.md states:
'### Run Program ({{kbd:run_program:tk}} or F5)'

But getting-started.md uses:
'{{kbd:run_program}}' (without :tk suffix)

This inconsistency in template usage may cause rendering issues.

---

#### documentation_inconsistency

**Description:** Continue operation has no keyboard shortcut but is listed in shortcuts table

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
feature-reference.md states:
'### Continue
Resume execution after pausing at a breakpoint.
- Menu: Run → Continue
- Toolbar: "Cont" button
- No keyboard shortcut'

But in the Quick Reference table, Continue is listed with '(toolbar)' which is inconsistent with other entries that show actual shortcuts.

---

#### documentation_inconsistency

**Description:** Step Statement has no keyboard shortcut but is listed in shortcuts table

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
feature-reference.md states:
'### Step Statement
Execute one BASIC statement at a time.
- Menu: Run → Step Statement
- Toolbar: "Stmt" button
- No keyboard shortcut'

But it's listed in the Quick Reference table with '(toolbar)' which suggests it should have a shortcut or shouldn't be in a shortcuts table.

---

#### documentation_inconsistency

**Description:** Inconsistent warnings about feature implementation status

**Affected files:**
- `docs/help/ui/tk/workflows.md`
- `docs/help/ui/tk/tips.md`

**Details:**
workflows.md includes:
'**Note:** Some features described below (Smart Insert, Variables Window, Execution Stack, Renumber dialog) are documented here based on the Tk UI design specifications. Check [Settings](settings.md) for current implementation status...'

tips.md includes:
'**Note:** Some features described below (Smart Insert, Variables Window, Execution Stack) are documented here based on the Tk UI design specifications...'

But other Tk docs (feature-reference.md, features.md, getting-started.md) have no such warnings, creating confusion about what is actually implemented.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut references in Web UI docs

**Affected files:**
- `docs/help/ui/web/debugging.md`

**Details:**
debugging.md uses inconsistent kbd template formats:
- Sometimes: {{kbd:run:web}}
- Sometimes: {{kbd:continue:web}}
- Sometimes: {{kbd:help:web}}1, {{kbd:help:web}}2

The {{kbd:help:web}}1 and {{kbd:help:web}}2 formats appear unusual - likely should be F11, F12 or similar standard function keys.

---

#### documentation_inconsistency

**Description:** Duplicate keyboard shortcuts section with different information

**Affected files:**
- `docs/help/ui/web/debugging.md`

**Details:**
debugging.md has two 'Keyboard Shortcuts' sections:

First section (under 'Debug Controls'):
'**Currently Implemented:**
- {{kbd:run:web}} - Run program
- {{kbd:continue:web}} - Continue (run to next breakpoint)
- {{kbd:step:web}} - Step statement
- {{kbd:step_line:web}} - Step line
- {{kbd:stop:web}} - Stop execution'

Second section (later in doc):
'## Keyboard Shortcuts
**Currently Implemented:**
- {{kbd:run:web}} - Run program
- {{kbd:continue:web}} - Continue (run to next breakpoint)
- {{kbd:step:web}} - Step statement
- {{kbd:step_line:web}} - Step line
- {{kbd:stop:web}} - Stop execution

**Planned for Future Releases:**
- {{kbd:continue:web}} - Start/Continue debugging
- {{kbd:toggle_breakpoint:web}} - Toggle breakpoint'

The 'Planned' section lists {{kbd:continue:web}} again, which is already in 'Currently Implemented'.

---

#### documentation_inconsistency

**Description:** Inconsistent description of Find vs Replace functionality

**Affected files:**
- `docs/help/ui/tk/features.md`

**Details:**
features.md states:
'**Find text ({{kbd:find:tk}}):**
- Opens Find dialog with search options
- Case sensitive and whole word matching
- Press F3 to find next occurrence

**Replace text ({{kbd:replace:tk}}):**
- Opens combined Find/Replace dialog
- Find and replace single or all occurrences
- Visual highlighting of matches
- Shows replacement count

**Note:** {{kbd:find:tk}} opens the Find dialog. {{kbd:replace:tk}} opens the Find/Replace dialog which includes both Find and Replace functionality.'

This suggests two separate dialogs, but the note says Replace opens a 'combined' dialog that includes Find functionality. This is confusing - are there two dialogs or one combined dialog?

---

#### documentation_inconsistency

**Description:** Inconsistent information about breakpoint management interface

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`

**Details:**
features.md under 'Breakpoints > Currently Implemented' states: 'Line breakpoints (toggle via Run menu)' and 'Management: Toggle via Run menu → Toggle Breakpoint'.

However, getting-started.md under 'Debugging Features > Breakpoints' describes a different interface: 'Set breakpoints to pause execution at specific lines:
1. Use Run → Toggle Breakpoint menu option
2. Enter the line number
3. Program will pause when reaching that line'

This suggests an input dialog for entering line numbers, but features.md doesn't mention this dialog-based interface. The actual implementation method is unclear.

---

#### documentation_inconsistency

**Description:** Contradictory information about file I/O implementation and persistence

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
features.md under 'File Operations > Currently Implemented' states: 'Load .BAS files from local filesystem' and 'Save/download programs as .BAS files'.

However, web-interface.md under 'File I/O' provides more detailed information: 'File operations in the web UI work with an in-memory filesystem: Files are stored in browser memory only, Each user has their own isolated filesystem, Files persist during your session (but are cleared when session ends), No access to the server's real filesystem (security)'.

The contradiction: features.md says 'Load .BAS files from local filesystem' which could be interpreted as server filesystem access, but web-interface.md clarifies 'No access to the server's real filesystem'. The actual mechanism (browser File API) is only mentioned in getting-started.md.

---

#### documentation_inconsistency

**Description:** Inconsistent description of Command area functionality and auto-numbering behavior

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
features.md doesn't explicitly document the Command area as a separate feature.

getting-started.md under 'Command Area' states: 'Use this for immediate commands that don't get added to your program' and 'Important: The Command area does NOT auto-number. It executes immediately.'

web-interface.md under 'Command (Bottom)' states: 'No automatic line numbering - commands run immediately'.

However, features.md under 'Line Management > Smart Line Numbering (Currently Implemented)' only mentions: 'Auto-increment by configurable step (default 10)' and 'Manual line number entry supported' without clarifying that this ONLY applies to the Program Editor and NOT the Command area.

This could confuse users about where auto-numbering applies.

---

#### documentation_inconsistency

**Description:** Menu structure inconsistency between documents

**Affected files:**
- `docs/help/ui/web/web-interface.md`
- `docs/help/ui/web/getting-started.md`

**Details:**
web-interface.md under 'Menu Functions' lists these menus: 'File Menu', 'Edit Menu', 'Run Menu', 'View Menu', 'Help Menu'.

However, getting-started.md under 'Menu Bar' only lists: 'File - New, Open, Save, Save As, Recent Files, Exit', 'Run - Run Program, Stop, Step, Continue, List Program, Show Variables, Show Stack, Clear Output', 'Help - Help Topics, About'.

getting-started.md is missing the 'Edit Menu' and 'View Menu' entirely. Also, the 'Run Menu' items differ between the two documents:
- getting-started.md: 'Step, Continue, List Program, Show Variables, Show Stack'
- web-interface.md: 'Toggle Breakpoint, Clear All Breakpoints, Continue, Step Line, Step Statement'

The 'Show Variables' location also differs: getting-started.md puts it in 'Run Menu', web-interface.md puts it in 'View Menu'.

---

#### documentation_inconsistency

**Description:** Execution control buttons and keyboard shortcuts inconsistency

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/getting-started.md`

**Details:**
features.md under 'Execution Control > Currently Implemented' lists: 'Run ({{kbd:run:web}})', 'Continue ({{kbd:continue:web}})', 'Step statement ({{kbd:step:web}})', 'Step line ({{kbd:step_line:web}})', 'Stop ({{kbd:stop:web}})'.

However, getting-started.md under 'Toolbar' describes buttons with different labels:
- 'Run - Parse and execute the program (▶️ green button, {{kbd:run:web}})'
- 'Stop - Stop running program (⏹️ red button, {{kbd:stop:web}})'
- 'Step Line - Execute all statements on current line, then pause (⏭️ button, {{kbd:step_line:web}})'
- 'Step Stmt - Execute one statement, then pause (↻ button, {{kbd:step:web}})'
- 'Continue - Resume normal execution after stepping (▶️⏸️ button, {{kbd:continue:web}})'

The inconsistency: features.md uses 'Step statement' while getting-started.md uses 'Step Stmt'. Also, getting-started.md provides visual button indicators (▶️, ⏹️, etc.) that features.md doesn't mention.

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

The limitation says 'No visual debugging (text commands only)' which could be misinterpreted as 'no debugging', when it actually means 'debugging via text commands, not visual interface'. The phrasing could be clearer.

---

#### documentation_inconsistency

**Description:** Contradictory information about assembly source file line endings

**Affected files:**
- `docs/user/FILE_FORMAT_COMPATIBILITY.md`

**Details:**
The document states:
'MBASIC saves all program files using **Unix-style line endings** (`\n`, also called LF).'

But then later states:
'**Note**: Assembly source files (`.mac`) in the `docs/history/original_mbasic_src/` directory retain their original CRLF line endings because they are intended for use with the CP/M M80 assembler, which requires CRLF format.'

This creates confusion about whether MBASIC saves ALL files with LF or if .mac files are an exception. The first statement should be qualified to exclude .mac files or clarify that it applies only to .bas files.

---

#### documentation_inconsistency

**Description:** Decision matrix uses warning symbol for Curses mouse support but doesn't explain what 'Limited' means

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
In the Decision Matrix table:
| Mouse support | ❌ | ⚠️ Limited | ✅ | ✅ |

The Curses column shows '⚠️ Limited' but the document doesn't clearly explain what 'limited mouse support' means in the context of Curses. Earlier in the document under Curses limitations it says 'Limited mouse support' but doesn't elaborate on what works and what doesn't.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut notation format between documents

**Affected files:**
- `docs/user/INSTALL.md`
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
INSTALL.md uses plain text for keyboard shortcuts (e.g., 'F9', 'ESC'), while TK_UI_QUICK_START.md uses template notation (e.g., '{{kbd:run_program}}', '{{kbd:file_save}}'). QUICK_REFERENCE.md also uses {{kbd:...}} notation. This creates inconsistency in how shortcuts are presented to users.

---

#### documentation_inconsistency

**Description:** Different debugging workflows and keyboard shortcuts between Curses and Tk UIs

**Affected files:**
- `docs/user/QUICK_REFERENCE.md`
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
QUICK_REFERENCE.md (Curses) shows breakpoint debugging with keys 'b' or 'F9' to toggle, and 'c', 's', 'e' for continue/step/end during execution. TK_UI_QUICK_START.md shows '{{kbd:toggle_breakpoint}}' for breakpoints and mentions 'Step', 'Continue', 'Stop' are 'available via toolbar buttons or the Run menu (no keyboard shortcuts)'. This is a legitimate UI difference but could confuse users switching between UIs.

---

#### documentation_inconsistency

**Description:** Inconsistent boolean value format in SET command examples vs JSON examples

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
In SET command examples, booleans are shown as: 'SET "editor.show_line_numbers" true' (lowercase, no quotes). In JSON file examples, booleans are shown as: '"editor.auto_number": true' (lowercase, no quotes). However, the 'Type Conversion' section states: 'Booleans: true or false (lowercase, no quotes in commands; use true/false in JSON files)' - this is redundant/confusing since both use the same format. The distinction being made is unclear.

---

#### documentation_inconsistency

**Description:** Missing CHOOSING_YOUR_UI.md file referenced in README and INSTALL

**Affected files:**
- `docs/user/README.md`
- `docs/user/INSTALL.md`

**Details:**
docs/user/README.md lists: '- **[CHOOSING_YOUR_UI.md](CHOOSING_YOUR_UI.md)** - Guide to selecting the right UI'. INSTALL.md references it in QUICK_REFERENCE.md: 'Visit [CHOOSING_YOUR_UI.md](CHOOSING_YOUR_UI.md) for UI comparison'. However, this file is not included in the provided documentation files.

---

#### documentation_inconsistency

**Description:** Missing multiple files referenced in README contents list

**Affected files:**
- `docs/user/README.md`

**Details:**
docs/user/README.md references several files not provided: CASE_HANDLING_GUIDE.md, FILE_FORMAT_COMPATIBILITY.md, sequential-files.md. These are listed in the Contents section but files are not included.

---

#### documentation_inconsistency

**Description:** Unclear scope precedence for settings

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
The document states settings are applied in order: '1. File scope - Per-file settings (future feature) 2. Project scope 3. Global scope 4. Default'. However, it also says 'most specific wins', which would suggest File > Project > Global > Default. The phrase 'most specific wins' combined with numbered list creates ambiguity about whether #1 has highest or lowest priority.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut documentation for Curses UI - Save command differs between documents

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`
- `docs/user/keyboard-shortcuts.md`

**Details:**
UI_FEATURE_COMPARISON.md shows Save shortcut as {{kbd:save:curses}} (template variable), while keyboard-shortcuts.md explicitly documents it as 'Ctrl+V' with explanation '(Ctrl+S unavailable - terminal flow control)'. The comparison table uses template variables that may not resolve to Ctrl+V, creating potential confusion.

---

#### documentation_inconsistency

**Description:** Contradictory information about Find/Replace in Web UI

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
In the 'Editing Features' table, Find/Replace for Web is marked as '⚠️' with note 'Tk: implemented, Web: planned'. However, in 'Coming Soon' section, it lists '⏳ Find/Replace in Web UI' as a future feature. The warning symbol suggests partial implementation, but the Coming Soon section suggests it's not implemented at all.

---

#### documentation_inconsistency

**Description:** Incomplete keyboard shortcut documentation - missing UI context

**Affected files:**
- `docs/user/keyboard-shortcuts.md`

**Details:**
The keyboard-shortcuts.md file is titled 'MBASIC Curses UI Keyboard Shortcuts' but doesn't clarify if these shortcuts are exclusive to Curses or shared with other UIs. The UI_FEATURE_COMPARISON.md suggests different shortcuts across UIs, but keyboard-shortcuts.md doesn't cross-reference or clarify the scope.

---

### 🟢 Low Severity

#### Code vs Comment conflict

**Description:** Comment claims keyword_token fields are not currently used, but doesn't explain why they exist or if they should be removed

**Affected files:**
- `src/ast_nodes.py`

**Details:**
PrintStatementNode line 186-189:
'Note: keyword_token fields are present in some statement nodes (PRINT, IF, FOR) but not others. These were intended for case-preserving keyword regeneration but are not currently used by position_serializer, which handles keyword case through case_keepy_string() instead. The fields remain for potential future use and backward compatibility.'

Similar comments appear in:
- IfStatementNode (lines 234-236)
- ForStatementNode (lines 250-252)

These fields exist in the code but are documented as unused. This creates maintenance burden and confusion about whether they should be populated or removed.

---

#### Code vs Comment conflict

**Description:** CALL statement 'arguments' field documented as unused but still present in code

**Affected files:**
- `src/ast_nodes.py`

**Details:**
CallStatementNode lines 733-747:
'Implementation Note: The \'arguments\' field is currently unused (always empty list). It exists for potential future support of BASIC dialects that allow CALL with arguments (e.g., CALL ROUTINE(args)). Standard MBASIC 5.21 only accepts a single address expression in the \'target\' field. Code traversing the AST can safely ignore the \'arguments\' field for MBASIC 5.21 programs.'

The field is defined but documented as always empty. This creates confusion about whether code should populate it or check it.

---

#### Documentation inconsistency

**Description:** Inconsistent documentation style for statement nodes - some have detailed syntax examples, others don't

**Affected files:**
- `src/ast_nodes.py`

**Details:**
Some nodes have extensive syntax documentation:
- InputStatementNode (lines 202-220): Detailed explanation of suppress_question and semicolon usage
- ChainStatementNode (lines 522-538): Multiple syntax examples and parameter explanations
- RenumStatementNode (lines 619-632): Detailed parameter documentation

Others have minimal documentation:
- EndStatementNode (lines 577-583): Just 'END' syntax
- TronStatementNode (lines 586-592): Just 'TRON' syntax
- SystemStatementNode (lines 603-612): Brief description

This inconsistency makes the documentation less useful for understanding complex statements.

---

#### Documentation inconsistency

**Description:** VariableNode documentation has complex explanation of type_suffix vs explicit_type_suffix that could be clearer

**Affected files:**
- `src/ast_nodes.py`

**Details:**
VariableNode lines 869-883:
'Type suffix handling:
- type_suffix: The actual suffix character ($, %, !, #) when present
- explicit_type_suffix: Boolean indicating the origin of type_suffix:
    * True: suffix appeared in source code (e.g., "X%" in "X% = 5")
    * False: suffix inferred from DEFINT/DEFSNG/DEFDBL/DEFSTR (e.g., "X" with DEFINT A-Z)

Example: In "DEFINT A-Z: X=5", variable X has type_suffix=\'%\' and explicit_type_suffix=False.
The suffix must be tracked for type checking but not regenerated in source code.
Both fields must always be examined together to correctly handle variable typing.'

The phrase 'Both fields must always be examined together' is vague. What happens if code only checks one field? The documentation should be more explicit about the consequences.

---

#### Documentation inconsistency

**Description:** ChainStatementNode delete_range type annotation inconsistent with description

**Affected files:**
- `src/ast_nodes.py`

**Details:**
ChainStatementNode line 535:
'delete_range: Optional[Tuple[int, int]] = None  # (start_line_number, end_line_number) for DELETE option - tuple of int line numbers'

The comment redundantly states 'tuple of int line numbers' when the type annotation already specifies Tuple[int, int]. The comment should add value beyond what the type annotation provides, such as explaining the semantics (inclusive/exclusive range, etc.).

---

#### Documentation inconsistency

**Description:** TypeInfo class documentation describes it as both utility class and compatibility layer without clear guidance on which to use

**Affected files:**
- `src/ast_nodes.py`

**Details:**
TypeInfo lines 1009-1020:
'Type information utilities for variables

Provides convenience methods for working with VarType enum and converting between type suffixes, DEF statement tokens, and VarType enum values.

This class serves two purposes:
1. Static helper methods for type conversions
2. Compatibility layer: Class attributes (INTEGER, SINGLE, etc.) alias VarType enum values to support legacy code using TypeInfo.INTEGER instead of VarType.INTEGER'

The documentation doesn't indicate which approach is preferred for new code. Should developers use VarType.INTEGER or TypeInfo.INTEGER? The compatibility layer suggests TypeInfo.INTEGER is legacy, but this isn't stated explicitly.

---

#### code_vs_comment

**Description:** EOF function comment describes mode 'I' as 'Input' but clarifies it means 'BINARY INPUT mode'

**Affected files:**
- `src/basic_builtins.py`

**Details:**
In EOF method docstring:
"Note: For binary input files (mode 'I' from OPEN statement), respects ^Z (ASCII 26)
as EOF marker (CP/M style). In MBASIC syntax, mode 'I' stands for 'Input' but is
specifically BINARY INPUT mode, implemented as 'rb' by execute_open() in interpreter.py."

The comment is internally consistent but potentially confusing - it says mode 'I' stands for 'Input' but then clarifies it's specifically 'BINARY INPUT mode'. This could be clearer by stating upfront that 'I' means binary input mode in MBASIC, not just generic input.

---

#### documentation_inconsistency

**Description:** Module docstring references 'tokens.py' for MBASIC 5.21 specification but tokens.py is not in the provided files

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Module docstring states:
"Note: Version 5.21 refers to BASIC-80 Reference Manual Version 5.21. See tokens.py for
complete MBASIC 5.21 specification reference."

However, tokens.py is not included in the provided source files, making this reference unverifiable. This could be a missing file or an outdated reference.

---

#### code_vs_comment

**Description:** Comment about sign behavior in parse_numeric_field may be incomplete

**Affected files:**
- `src/basic_builtins.py`

**Details:**
In parse_numeric_field method docstring:
"Sign behavior:
- leading_sign: + at start, adds + or - sign (2 chars total)
- trailing_sign: + at end, adds + or - sign (2 chars total)
- trailing_minus_only: - at end, adds - for negative OR space for non-negative (1 char total)"

The comment says leading_sign and trailing_sign add '2 chars total', but this is ambiguous. Looking at the code in format_numeric_field:
"if spec['leading_sign'] or spec['trailing_sign'] or spec['trailing_minus_only']:
    field_width += 1  # Sign takes up one position"

The code adds 1 to field_width, not 2. The comment '2 chars total' likely means the sign character plus the number, but this is unclear and potentially misleading.

---

#### code_vs_comment

**Description:** INPUT function docstring describes file_num parameter but implementation doesn't validate it's an integer from BASIC

**Affected files:**
- `src/basic_builtins.py`

**Details:**
In INPUT method:
"INPUT$ - Read num characters from keyboard or file.
(Method name is INPUT since Python doesn't allow $ in names)

BASIC syntax:
    INPUT$(n) - read n characters from keyboard
    INPUT$(n, #filenum) - read n characters from file

Python call syntax (from interpreter):
    INPUT(n) - read n characters from keyboard
    INPUT(n, filenum) - read n characters from file

Note: The # prefix in BASIC syntax is stripped by the parser before calling this method."

The docstring says the # prefix is stripped by the parser, but the code does 'file_num = int(file_num)' which suggests it might receive a string or other type. The comment doesn't clarify what type the parser passes.

---

#### code_vs_comment

**Description:** CaseKeeperTable docstring example shows 'first_wins' behavior but doesn't mention it's the default

**Affected files:**
- `src/case_keeper.py`

**Details:**
Class docstring states:
"Example (with default 'first_wins' policy):
    table = CaseKeeperTable()
    table.set('PRINT', 'Print')  # Key: 'print', Display: 'Print'
    table.get('print')  # Returns: 'Print'
    table.get('PRINT')  # Returns: 'Print' (same - case insensitive)
    table.set('print', 'PRINT')  # Ignored - first wins, keeps 'Print'"

The example mentions 'default first_wins policy' in the comment, and the __init__ method shows policy='first_wins' as default, so this is consistent. However, the example comment could be clearer that CaseKeeperTable() with no arguments uses first_wins.

---

#### Documentation inconsistency

**Description:** Duplicate two-letter error codes acknowledged but potential ambiguity not fully addressed

**Affected files:**
- `src/error_codes.py`

**Details:**
Module docstring states:
"Note: Some two-letter codes are duplicated (e.g., DD, CN, DF) across different numeric error codes. This matches the original MBASIC 5.21 specification where the two-letter codes alone are ambiguous - the numeric code is authoritative. All error handling in this implementation uses numeric codes for lookups, so the duplicate two-letter codes do not cause ambiguity in practice."

However, the ERROR_CODES dict shows:
10: ("DD", "Duplicate definition")
61: ("DF", "Disk full")
68: ("DD", "Device unavailable")

The function get_error_message() only takes error_code (numeric) as input, confirming numeric codes are authoritative. But format_error() uses two_letter codes in output, which could be confusing to users if they see the same two-letter code for different errors. Documentation acknowledges this but doesn't explain user-facing implications.

---

#### Code vs Comment conflict

**Description:** Comment says 'use >= instead of <=' for negative steps but code doesn't implement it

**Affected files:**
- `src/codegen_backend.py`

**Details:**
In _generate_for():
# Determine comparison operator based on step
if stmt.step_expr:
    # If step is negative, use >= instead of <=
    # For now, assume positive step (TODO: handle negative steps)
    comp = '<='
else:
    comp = '<='

The comment describes logic for handling negative steps, but the code always uses '<=' regardless. The TODO confirms this is incomplete, but the comment is misleading because it describes what should happen, not what does happen.

---

#### Documentation inconsistency

**Description:** Docstring mentions 'DEF type map' but parameter is named 'def_type_map'

**Affected files:**
- `src/editing/manager.py`

**Details:**
In ProgramManager.__init__() docstring:
"Args:
    def_type_map: Dictionary mapping first letter to TypeInfo
              (from DEFINT/DEFSNG/DEFDBL/DEFSTR statements)"

The description says 'Dictionary mapping first letter to TypeInfo' but doesn't specify what TypeInfo is or where it's defined. This is a minor documentation clarity issue - the type should be fully qualified or explained.

---

#### Code vs Comment conflict

**Description:** Comment says 'For simplicity, use the type of the left operand' but doesn't explain type promotion

**Affected files:**
- `src/codegen_backend.py`

**Details:**
In _get_expression_type():
elif isinstance(expr, BinaryOpNode):
    # For simplicity, use the type of the left operand
    # In reality, we'd need type promotion rules
    return self._get_expression_type(expr.left)

The comment acknowledges that proper type promotion isn't implemented, but doesn't explain what happens when mixing types (e.g., INTEGER + SINGLE). This could lead to incorrect code generation for mixed-type expressions.

---

#### code_vs_comment

**Description:** ImmediateExecutor.execute() docstring states 'IMPORTANT: For tick-based interpreters, this should only be called when can_execute_immediate() returns True' but the code does check this condition at the start of execute()

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Docstring warning: "IMPORTANT: For tick-based interpreters, this should only be called when
can_execute_immediate() returns True. Calling while the program is actively
running (halted=False) may corrupt the interpreter state."

Code implementation:
def execute(self, statement):
    # Check if safe to execute (for tick-based interpreters)
    if not self.can_execute_immediate():
        return (False, "Cannot execute immediate mode while program is running\n")

The docstring implies the caller must check, but the code defensively checks anyway. This is good defensive programming but the docstring could be updated to reflect that the method performs its own safety check.

---

#### documentation_inconsistency

**Description:** Module docstring mentions 'TWO SEPARATE FILESYSTEM ABSTRACTIONS' but describes overlap and intentional duplication in a way that could be clearer about the architectural decision

**Affected files:**
- `src/filesystem/base.py`

**Details:**
The docstring states:
"Note: There is intentional overlap between the two abstractions.
Both provide list_files() and delete() methods, but serve different contexts:
FileIO is for interactive commands (FILES/KILL), FileSystemProvider is for
runtime access (though not all BASIC dialects support runtime file operations)."

This is documentation-only (no code conflict), but the explanation of why there are two separate abstractions with overlapping functionality could be more explicit about whether this is technical debt or intentional design.

---

#### code_vs_comment

**Description:** ImmediateExecutor class docstring describes state names as documentation-only ('not actual enum values') but this could confuse readers about the actual implementation

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Docstring states:
"State names used in documentation (not actual enum values):
- 'idle' - No program loaded (halted=True)
- 'paused' - User hit Ctrl+Q/stop (halted=True)
...

Note: The actual implementation checks boolean flags (halted, error_info, input_prompt),
not string state values."

This is clear but verbose. The disconnect between documented 'state names' and actual boolean flags could be simplified or the state names could be removed entirely since they're never used in the code.

---

#### code_vs_comment

**Description:** Comment in execute() method states 'Note: We do not save/restore the PC before/after execution' but doesn't explain why this design choice was made

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Comment: "# Note: We do not save/restore the PC before/after execution.
# This allows statements like RUN to change execution position.
# Control flow statements (GOTO, GOSUB) can also modify PC but may produce
# unexpected results (see help text). Normal statements (PRINT, LET) don't modify PC."

The comment explains what happens but not why this design was chosen over alternatives. This is more of a documentation quality issue than an inconsistency.

---

#### code_vs_comment

**Description:** Module docstring mentions 'Implementation note: Uses standard Python type hints (e.g., tuple[str, bool]) which require Python 3.9+' but doesn't specify what the project's minimum Python version is

**Affected files:**
- `src/input_sanitizer.py`

**Details:**
Docstring states:
"Implementation note: Uses standard Python type hints (e.g., tuple[str, bool])
which require Python 3.9+. For earlier Python versions, use Tuple[str, bool] from typing."

This is a helpful note, but without knowing the project's minimum Python version requirement (which should be documented elsewhere), it's unclear if this is a compatibility issue or just informational.

---

#### documentation_inconsistency

**Description:** EDIT command documentation lists unimplemented features without clear status

**Affected files:**
- `src/interactive.py`

**Details:**
The cmd_edit() docstring at line ~720 states:
'Note: Count prefixes ([n]D, [n]C) and search commands ([n]S, [n]K) are not yet implemented.'

This is followed by a paragraph about 'INTENTIONAL BEHAVIOR' for digits. The documentation should clarify whether digit handling is:
1. Not implemented (as 'not yet implemented' suggests)
2. Intentionally ignored (as 'INTENTIONAL BEHAVIOR' suggests)
3. Partially implemented (silent ignore as placeholder)

The two statements appear contradictory.

---

#### code_vs_comment

**Description:** Comment about ERL renumbering describes broader behavior than manual specifies, but doesn't explain all implications

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~590 in _renum_erl_comparison() states:
'INTENTIONAL DEVIATION FROM MANUAL:
This implementation renumbers for ANY binary operator with ERL on left, including arithmetic operators (ERL + 100, ERL * 2, etc.), not just comparison operators.'

The comment explains the rationale and known limitation for arithmetic expressions. However, it doesn't address what happens with logical operators (AND, OR, NOT) or other binary operators. The code at line ~610 checks for 'BinaryOpNode' without filtering operator type, so it would also renumber:
- ERL AND 100
- ERL OR 100
- ERL MOD 100

These cases are not mentioned in the comment's explanation or known limitations.

---

#### code_vs_comment

**Description:** Comment about readline configuration mentions Ctrl+A override but doesn't explain interaction with EDIT mode trigger

**Affected files:**
- `src/interactive.py`

**Details:**
At line ~50, comment states:
'# Bind Ctrl+A to insert the character instead of moving cursor to beginning-of-line
# This overrides default Ctrl+A (beginning-of-line) behavior.
# When user presses Ctrl+A, the terminal sends ASCII 0x01, and 'self-insert'
# tells readline to insert it as-is instead of interpreting it as a command.
# The \x01 character in the input string triggers edit mode (see start() method)'

However, the start() method at line ~150 checks for '\x01' at the beginning of the line to trigger EDIT mode. If readline is configured to 'self-insert' Ctrl+A, it would insert the character into the input buffer, but the check at line ~150 expects it at position [0]. This works, but the comment doesn't explain that readline's self-insert places the character at the current cursor position, which happens to be position 0 at the start of input.

---

#### code_vs_comment_conflict

**Description:** Comment about line_text_map being empty for immediate mode may be misleading

**Affected files:**
- `src/interactive.py`

**Details:**
Comment states: '(no source line text available for error reporting, but this is fine for immediate mode where the user just typed the statement)'

However, the statement text IS available (it's the 'statement' parameter), it's just not being passed to Runtime. This could be improved for better error reporting in immediate mode.

---

#### documentation_inconsistency

**Description:** HELP command lists BREAK but doesn't mention CLEAR BREAK or show how to list breakpoints

**Affected files:**
- `src/interactive.py`

**Details:**
cmd_help shows:
  BREAK line         - Set breakpoint at line

But doesn't document how to remove breakpoints or list existing breakpoints, which are likely supported features.

---

#### code_vs_documentation_inconsistency

**Description:** FILES command docstring mentions drive letter syntax but implementation doesn't validate or handle it

**Affected files:**
- `src/interactive.py`

**Details:**
Docstring says: 'Note: Drive letter syntax (e.g., "A:*.*") is not supported in this implementation.'

However, the code doesn't explicitly check for or reject drive letter syntax - it just passes the filespec to list_files(). If a user tries 'FILES "A:*.*"', the behavior is undefined (likely an error from list_files, but not explicitly handled).

---

#### code_vs_comment_conflict

**Description:** Comment about Runtime initialization mentions line_text_map purpose but doesn't explain why it's acceptable to omit it

**Affected files:**
- `src/interactive.py`

**Details:**
Comment: 'Pass empty line_text_map since immediate mode uses temporary line 0 (no source line text available for error reporting, but this is fine for immediate mode where the user just typed the statement)'

The justification 'this is fine' is weak - error reporting would actually be better WITH the source text. The real reason might be architectural (Runtime expects a dict of all program lines, not single statements), but this isn't explained.

---

#### code_vs_comment

**Description:** Comment about execution order in InterpreterState docstring doesn't match actual code flow

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring at lines 44-51 lists execution order:
"1. pause_requested check - pauses if pause() was called
2. halted check - stops if already halted
3. break_requested check - handles Ctrl+C breaks
4. breakpoints check - pauses at breakpoints
5. trace output - displays [line] or [line.stmt] if TRON is active
6. statement execution - where input_prompt may be set
7. error handling - where error_info is set via exception handlers"

But in tick_pc() (lines 344-470), the actual order is:
1. pause_requested (line 349)
2. halted check (line 355)
3. break_requested (line 363)
4. breakpoints (line 373)
5. trace output (line 388)
6. statement execution (line 401)
7. error handling (line 410)

The order matches, but step 4 (breakpoints) has additional logic with skip_next_breakpoint_check that's not mentioned in the overview.

---

#### documentation_inconsistency

**Description:** Version number comment references internal version but doesn't specify what it is

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at lines 656-660 says:
"OLD EXECUTION METHODS REMOVED (version 1.0.299)
Note: The project has an internal implementation version (tracked in src/version.py)
which is separate from the MBASIC 5.21 language version being implemented."

This references src/version.py but that file is not included in the provided source code, so the actual version cannot be verified. The comment also mentions 'MBASIC 5.21' as the language version being implemented, which appears in the module docstring at line 3.

---

#### code_vs_comment

**Description:** Comment about error_info being set before _invoke_error_handler is misleading

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at lines 691-693 says:
"Note: error_info is set in the exception handler in tick_pc() just before
calling this method. We're now ready to invoke the error handler."

Looking at tick_pc() at lines 410-440, error_info is indeed set at lines 418-423 before calling _invoke_error_handler at line 426. However, the comment in _invoke_error_handler makes it sound like this is a critical precondition, but the method doesn't actually use self.state.error_info - it only sets ERR%, ERL%, ERS% from the parameters passed to it (error_code, error_pc).

---

#### code_vs_comment

**Description:** Comment about CLEAR state preservation mentions user_functions but code doesn't show explicit preservation

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1330 states:
# State preservation for CHAIN compatibility:
#
# PRESERVED by CLEAR (not cleared):
#   - runtime.common_vars (list of COMMON variable names - the list itself, not values)
#   - runtime.user_functions (DEF FN functions)

However, the execute_clear method doesn't show any explicit code to preserve user_functions. The code clears variables and arrays but doesn't touch user_functions, which means they're preserved by omission rather than explicit preservation. This is correct behavior but the comment makes it sound like there's explicit preservation code.

---

#### code_vs_comment

**Description:** Comment about WEND timing mentions popping 'after setting npc above' but the pop happens after the comment

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1030 states:
# Pop the loop from the stack (after setting npc above, before WHILE re-executes).
# Timing: We pop NOW so the stack is clean before WHILE condition re-evaluation.

The comment says 'after setting npc above' but the npc assignment is immediately before this comment, not 'above' it. This is a minor wording issue where 'above' should be 'immediately before this' or the comment should be moved to after the npc assignment.

---

#### code_vs_comment

**Description:** Comment about INPUT state machine mentions three steps but describes four

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at line ~1390 states:
State machine for keyboard input (file input is synchronous):
1. If state.input_buffer has data: Use buffered input (from provide_input())
2. Otherwise: Set state.input_prompt, input_variables, input_file_number and return (pauses execution)
3. UI calls provide_input() with user's input line
4. On next tick(), buffered input is used (step 1) and input_prompt/input_variables are cleared

The comment says 'State machine for keyboard input' and lists 4 steps, but step 3 is not part of the state machine itself - it's an external UI action. The state machine has 2 states (has buffer / needs input), not 4 steps. The comment should clarify that steps 3-4 describe the interaction cycle, not state machine states.

---

#### code_vs_comment

**Description:** Comment in execute_cont() references both STOP and Break (Ctrl+C) setting runtime.stopped, but only STOP behavior is visible

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment states: 'Both STOP and Break (Ctrl+C) set runtime.stopped=True and runtime.halted=True.'

The execute_stop() method is visible and does set these flags, but the Break (Ctrl+C) handling code is not in this snippet. This may be correct but cannot be verified from the provided code.

---

#### documentation_inconsistency

**Description:** execute_step() docstring claims it's a placeholder and not functional, but doesn't explain why it exists or what the migration path is

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring states: 'STEP is intended to execute one or more statements, then pause. IMPORTANT: This method is a placeholder and does NOT actually perform stepping.'

The docstring mentions that tick_pc() has working step infrastructure but doesn't explain:
1. Why this placeholder exists if it doesn't work
2. Whether it should be removed or completed
3. What happens if a user types STEP in immediate mode (does it just print the message and do nothing?)

---

#### code_vs_comment

**Description:** Comment about 255-character string limit mentions LSET/RSET field width limits but doesn't specify what those limits are

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment in evaluate_binaryop() states: 'LSET/RSET have different limits: they enforce field width limits (defined by FIELD statement) rather than the 255-char concatenation limit.'

This comment references field width limits but doesn't specify:
1. What the maximum field width is
2. Whether there's a total buffer size limit
3. Whether individual fields can exceed 255 characters

The execute_lset() and execute_rset() code doesn't show any explicit limit checking beyond the field width itself.

---

#### code_vs_comment

**Description:** Comment in execute_midassignment() describes validation behavior that may not match MBASIC 5.21 exactly

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment states: 'Note: start_idx == len(current_value) is considered out of bounds (can't start replacement past end)'

This is a specific implementation decision that may or may not match MBASIC 5.21 behavior. The comment doesn't cite MBASIC 5.21 documentation or testing to confirm this is the correct behavior. Other parts of the code explicitly mention 'MBASIC 5.21 behavior' or 'MBASIC 5.21 compatibility' when documenting compatibility decisions.

---

#### Documentation inconsistency

**Description:** Module docstring states WebIOHandler is not exported due to nicegui dependency, but web_io.py imports nicegui at module level, making it fail on import if nicegui is not installed

**Affected files:**
- `src/iohandler/__init__.py`
- `src/iohandler/web_io.py`

**Details:**
__init__.py says: "WebIOHandler are not exported here because they have dependencies on their respective UI frameworks (tkinter, nicegui). They should be imported directly from their modules when needed"

But web_io.py has: "from nicegui import ui" at the top level, which will fail immediately if nicegui is not installed, even before WebIOHandler can be instantiated.

---

#### Code vs Comment conflict

**Description:** input_char() docstring says blocking parameter is ignored, but the method signature accepts it for interface compatibility

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Method signature: def input_char(self, blocking=True)

Docstring says: "Args:
    blocking: If True, wait for keypress. If False, return "" if no key ready.
             NOTE: This parameter is accepted for interface compatibility but
             is ignored in the web UI implementation."

Then later: "Note: Character input not supported in web UI. This method always returns an empty string immediately, regardless of the blocking parameter value. The blocking parameter is ignored."

The redundant explanation of ignoring the parameter appears twice in different ways.

---

#### Code vs Comment conflict

**Description:** Backward compatibility alias get_char() comment says it preserves non-blocking behavior, but calls input_char(blocking=False) which always returns empty string anyway

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Comment says: "Note: Always calls input_char(blocking=False) for non-blocking behavior. The original get_char() implementation was non-blocking, so this preserves that behavior for backward compatibility."

But input_char() always returns "" regardless of blocking parameter, so the blocking=False argument is meaningless. The comment implies there's a difference between blocking and non-blocking modes, but there isn't.

---

#### Documentation inconsistency

**Description:** input_char() Windows fallback warning message is inconsistent with the actual fallback behavior

**Affected files:**
- `src/iohandler/console.py`

**Details:**
Warning message says: "msvcrt not available on Windows - input_char() falling back to input() (waits for Enter, not single character)"

But the code then does: "line = input()\nreturn line[:1] if line else """

The warning says it "waits for Enter, not single character" but doesn't mention that it only returns the first character of the line, which is a significant detail.

---

#### Code vs Comment conflict

**Description:** print() method marked as deprecated but no deprecation warning is issued

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Comment says: "Deprecated: Use output() instead. This is a backward compatibility alias. New code should use output()."

But the method doesn't issue any deprecation warning (no warnings.warn() call), so users won't know it's deprecated unless they read the docstring.

---

#### Code vs Comment conflict

**Description:** input_char() non-blocking Windows fallback issues warning but then returns empty string, which may not be the intended behavior

**Affected files:**
- `src/iohandler/console.py`

**Details:**
For non-blocking mode when msvcrt is unavailable:
warnings.warn("msvcrt not available on Windows - non-blocking input_char() not supported", RuntimeWarning)
return ""

The warning says "not supported" but then returns "" which is actually the correct return value for non-blocking mode when no key is available. The warning implies failure, but the behavior is arguably correct.

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

**Description:** Comment about semicolon handling in parse_line() is inconsistent with actual behavior

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines 372-376 states:
"# Allow trailing semicolon at end of line only (treat as no-op).
# Context matters: Semicolons WITHIN PRINT/LPRINT are item separators (parsed there),
# but semicolons BETWEEN statements are NOT valid in MBASIC.
# MBASIC uses COLON (:) to separate statements, not semicolon (;)."

However, the code immediately after (lines 377-382) allows semicolons between statements and only raises an error if there's more content after:
"self.advance()
# If there's more after the semicolon (except another colon or newline), it's an error
if not self.at_end_of_line() and not self.match(TokenType.COLON):
    token = self.current()
    raise ParseError(f'Expected : or newline after ;, got {token.type.name}', token)"

This suggests semicolons ARE allowed between statements (as long as nothing follows), contradicting the comment that says they are NOT valid.

---

#### code_vs_comment

**Description:** Comment about comma being optional after file number contradicts typical MBASIC 5.21 behavior

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines 1217-1222 states:
"# Optionally consume comma after file number
# Note: MBASIC 5.21 typically uses comma (PRINT #1, 'text').
# Our parser makes the comma optional for flexibility.
# If semicolon appears instead of comma, it will be treated as an item
# separator in the expression list below (not as a file number separator)."

This suggests the parser intentionally deviates from MBASIC 5.21 standard behavior for 'flexibility', but the docstring at the top claims this is a 'Parser for MBASIC 5.21' with 'Key differences from interpreter' listed. This deviation is not listed as a key difference, creating ambiguity about whether this is intentional compatibility breaking or a bug.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for 'end of line' vs 'end of statement' in method names and comments

**Affected files:**
- `src/parser.py`

**Details:**
The parser has two similar methods:
1. at_end_of_line() at line 254 - checks for NEWLINE or EOF
2. at_end_of_statement() at line 267 - checks for NEWLINE, EOF, COLON, REM, REMARK, or APOSTROPHE

The comment for at_end_of_line() at lines 256-260 states:
"Note: This method does NOT check for comment tokens (REM, REMARK, APOSTROPHE)
or statement separators (COLON). Use at_end_of_statement() when parsing statements
that should stop at comments/colons."

However, throughout the code, these methods are used inconsistently. For example, in parse_print() at line 1228, the loop condition uses 'at_end_of_line()' but also explicitly checks for COLON and REM tokens, suggesting at_end_of_statement() should have been used instead. This pattern appears in multiple places, indicating confusion about when to use which method.

---

#### code_vs_comment

**Description:** Comment about MID$ tokenization may be misleading about token representation

**Affected files:**
- `src/parser.py`

**Details:**
In parse_mid_assignment() method around line 2050:

Comment states: "Note: The lexer tokenizes 'MID$' in source as a single MID token (the $ is part of the keyword, not a separate token)."

Then the code has:
token = self.current()  # MID token (represents 'MID$' from source)

This comment suggests the lexer strips the $ and creates a MID token, but it's unclear if the token value includes the $ or not. The comment says "the $ is part of the keyword" but then says it's tokenized as "MID token" without the $. This could confuse readers about whether the token's value is 'MID' or 'MID$'.

---

#### documentation_inconsistency

**Description:** Incomplete docstring in parse_deffn() method

**Affected files:**
- `src/parser.py`

**Details:**
The parse_deffn() method docstring is incomplete:

"Function name normalization: All function names are normalized to lowercase with
'fn' prefix (e.g., "FNR" becomes "fnr", "FNA$" becomes "fna$") for consistent
lookup. This matches the lexer's identifier normalization and ensures function"

The sentence cuts off mid-thought after "ensures function" without completing the explanation.

---

#### code_vs_comment

**Description:** Comment about dimension expressions may not match all BASIC implementations

**Affected files:**
- `src/parser.py`

**Details:**
In parse_dim() method around line 1940:

Comment states: "Dimension expressions: This implementation accepts any expression for array dimensions (e.g., DIM A(X*2, Y+1)), with dimensions evaluated at runtime. This matches MBASIC 5.21 behavior. Note: Some compiled BASICs (e.g., QuickBASIC) may require constants only."

This is informational but could be misleading - the comment claims this "matches MBASIC 5.21 behavior" but then notes other BASICs differ. Without seeing the actual MBASIC 5.21 specification or the runtime evaluation code, it's unclear if this implementation truly matches MBASIC 5.21. The comment makes a claim about compatibility that may not be verifiable from this code alone.

---

#### code_vs_comment

**Description:** Comment in parse_resume() duplicates information about RESUME 0 behavior

**Affected files:**
- `src/parser.py`

**Details:**
The docstring states: "Note: RESUME with no argument retries the statement that caused the error.
RESUME 0 also retries the error statement (interpreter treats 0 and None equivalently)."

Then inline comment repeats: "# Note: RESUME 0 means 'retry error statement' (interpreter treats 0 and None equivalently)"

This is redundant documentation of the same behavior.

---

#### code_vs_comment

**Description:** parse_width() docstring mentions MBASIC 5.21 specifics but doesn't explain how it differs from other versions

**Affected files:**
- `src/parser.py`

**Details:**
Docstring states:
"In MBASIC 5.21, common values are file numbers or omitted for console.
The parser accepts any expression; validation occurs at runtime."

This mentions MBASIC 5.21 specifically but doesn't clarify if other versions behave differently or why this version is called out. The implementation doesn't have any version-specific logic.

---

#### documentation_inconsistency

**Description:** parse_def_fn() examples show different spacing conventions without explaining significance

**Affected files:**
- `src/parser.py`

**Details:**
Examples in docstring:
DEF FNR(X) = INT(X*100+.5)/100
DEF FNA$(U,V) = P1$+CHR$(31+U*2)+CHR$(48+V*5)
DEF FNB = 42  (no parameters)

The comment below explains 'DEF FN R' vs 'DEF FNR' spacing matters for tokenization, but the examples don't demonstrate this distinction. All examples use no space between FN and the name.

---

#### documentation_inconsistency

**Description:** emit_keyword and emit_token have different spacing behavior that isn't clearly documented in their relationship

**Affected files:**
- `src/position_serializer.py`

**Details:**
emit_keyword docstring: 'Returns: String with appropriate spacing + keyword text (with case from table)'

emit_token docstring: 'Returns: String with appropriate spacing + token text'

Both delegate to emit_token for positioning, but emit_keyword applies case policy first. The relationship and call chain isn't explicitly documented in emit_keyword's docstring - it just says 'Use regular emit_token for positioning' in a comment, not the docstring.

---

#### code_vs_documentation

**Description:** serialize_rem_statement uses comment_type attribute but this attribute isn't documented in the function signature or module-level docs

**Affected files:**
- `src/position_serializer.py`

**Details:**
Code: 'if stmt.comment_type == "APOSTROPHE":
    result = self.emit_token("\'", stmt.column, "RemKeyword")
else:
    # Apply keyword case to REM/REMARK
    result = self.emit_keyword(stmt.comment_type.lower(), stmt.column, "RemKeyword")'

The comment_type attribute and its possible values (APOSTROPHE, REM, REMARK) aren't documented. This makes it unclear what the expected AST structure is for RemarkStatementNode.

---

#### code_vs_comment

**Description:** serialize_expression fallback comment says 'use pretty printing' but imports from ui_helpers which may not be 'pretty printing'

**Affected files:**
- `src/position_serializer.py`

**Details:**
In serialize_statement: '# Fallback: Use pretty printing from ui_helpers
from src.ui.ui_helpers import serialize_statement
return " " + serialize_statement(stmt)'

In serialize_expression: '# Fallback: use pretty printing
from src.ui.ui_helpers import serialize_expression
return " " + serialize_expression(expr)'

The comment assumes ui_helpers does 'pretty printing' but this isn't verified. The ui_helpers module isn't included in the provided files, so we can't verify this claim.

---

#### documentation_inconsistency

**Description:** StatementTable.next_pc docstring describes sequential execution but doesn't mention what happens with GOTO/GOSUB/control flow

**Affected files:**
- `src/pc.py`

**Details:**
Docstring: 'Get next PC after given PC (sequential execution).

Sequential execution means:
- Next statement on same line (increment stmt_offset), OR
- First statement of next line (if at end of current line)'

This describes the default case but doesn't clarify that control flow statements (GOTO, GOSUB, IF THEN) would bypass this sequential behavior. The relationship between next_pc() and control flow isn't documented.

---

#### documentation_inconsistency

**Description:** The module docstring and function docstrings consistently mention 'MBASIC 5.21 compatibility' for the 255-byte string limit, but create_unlimited_limits() allows 1MB strings with a comment '(for testing/development - not MBASIC compatible)'. This is intentional but could be more prominently documented in the function's docstring.

**Affected files:**
- `src/resource_limits.py`

**Details:**
create_unlimited_limits() docstring: "Create effectively unlimited limits (for testing)."

But the implementation has: max_string_length=1024*1024,  # 1MB strings (for testing/development - not MBASIC compatible)

The docstring doesn't warn that this configuration breaks MBASIC 5.21 compatibility, which is mentioned throughout the rest of the module.

---

#### documentation_inconsistency

**Description:** Both modules have 'Note:' sections distinguishing themselves from each other, but the phrasing is slightly asymmetric. resource_limits.py says 'This is distinct from resource_locator.py which finds package data files' while resource_locator.py says 'This is distinct from resource_limits.py which enforces runtime execution limits'. The first uses 'finds' (present tense) while the second uses 'enforces' (present tense), which is consistent, but resource_limits.py says 'package data files' while resource_locator.py says 'runtime execution limits' - the descriptions could be more parallel.

**Affected files:**
- `src/resource_limits.py`
- `src/resource_locator.py`

**Details:**
resource_limits.py: "Note: This is distinct from resource_locator.py which finds package data files."

resource_locator.py: "Note: This is distinct from resource_limits.py which enforces runtime execution limits."

These are consistent in meaning but could be more parallel in structure for clarity.

---

#### code_vs_comment_conflict

**Description:** The estimate_size() method has a comment '# String: UTF-8 byte length + 4-byte length prefix' but the actual implementation only adds 4 bytes for the prefix when a string value is provided. For non-string values (None, etc.), it returns 4 bytes total, not 4 bytes plus content. This is likely correct behavior (empty string = 4 bytes), but the comment could be clearer about this edge case.

**Affected files:**
- `src/resource_limits.py`

**Details:**
Comment: "# String: UTF-8 byte length + 4-byte length prefix"

Code:
if isinstance(value, str):
    return len(value.encode('utf-8')) + 4
return 4  # Empty string

The comment doesn't explicitly state that non-string values (or None) return just the 4-byte prefix, though the code comment '# Empty string' clarifies this.

---

#### code_vs_comment

**Description:** Comment about line=-1 usage is incomplete - doesn't mention debugger sets also use line=-1

**Affected files:**
- `src/runtime.py`

**Details:**
Line 52-56 comment: "Note: line -1 in last_write indicates non-program execution sources:
       1. System/internal variables (ERR%, ERL%) via set_variable_raw() with FakeToken(line=-1)
       2. Debugger/interactive prompt via set_variable() with debugger_set=True and token.line=-1
       Both use line=-1, making them indistinguishable from each other in last_write alone.
       However, line=-1 distinguishes these special sources from normal program execution (line >= 0)."

But the set_variable_raw() docstring (lines 437-451) says:
"The line=-1 marker in last_write indicates system/internal variables.
However, debugger sets also use line=-1 (via debugger_set=True),
making them indistinguishable from system variables in last_write alone."

This is consistent, but the module-level comment could be clearer that both paths are indistinguishable.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for case resolution - 'canonical case' vs 'original case'

**Affected files:**
- `src/runtime.py`

**Details:**
The code uses both terms inconsistently:
- Line 48: "'original_case' field stores the canonical case for display"
- Line 289: "Always update to canonical case"
- Line 336: "canonical_case  # Canonical case for display (field name is historical)"

The field is named 'original_case' but stores 'canonical case'. While comments acknowledge this is historical/misleading, it creates confusion. The term 'canonical case' is used in code/comments but 'original_case' is the field name.

---

#### code_vs_comment

**Description:** Comment about DIM tracking rationale may not match actual usage

**Affected files:**
- `src/runtime.py`

**Details:**
Lines 711-719 comment explains why DIM sets both last_read and last_write:
"Note: DIM is tracked as both read and write to provide consistent debugger display.
While DIM is technically allocation/initialization (write-only operation), setting
last_read to the DIM location ensures that debuggers/inspectors can show 'Last accessed'
information even for arrays that have never been explicitly read. Without this, an
unaccessed array would show no last_read info, which could be confusing. The DIM location
provides useful context about where the array was created."

This is a design decision that treats DIM as both read and write for debugger convenience, but it's semantically questionable whether allocation should count as a 'read'. The comment justifies it but the behavior may surprise users expecting read/write to mean actual data access.

---

#### documentation_inconsistency

**Description:** Incomplete docstring for get_all_variables() - cuts off mid-sentence

**Affected files:**
- `src/runtime.py`

**Details:**
Lines 1001-1014 show the docstring for get_all_variables():
"Export all variables with structured type information.

Returns detailed information about each variable including:
- Base name (without type suffix)
- Type suffix character
- For scalars: current value
- For arrays: dimensions and base
- Access tracking: last_read and last_write info

Returns:
    list: List of dictionaries with variable information
          Each dict contains:"

The docstring ends abruptly with 'Each dict contains:' without listing what the dict contains. This is incomplete documentation.

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

While all are technically correct, the varying levels of detail (some show 2 examples, some show 3) create minor inconsistency in documentation style.

---

#### Documentation inconsistency

**Description:** Deprecation notice format inconsistency

**Affected files:**
- `src/runtime.py`

**Details:**
get_loop_stack() has structured deprecation info:
"Deprecated since: 2025-10-25 (commit cda25c84)
Will be removed: No earlier than 2026-01-01"

But the 'from_line' field redundancy note in get_execution_stack() mentions backward compatibility without any deprecation timeline or removal plan, despite being redundant.

---

#### code_vs_comment

**Description:** load() docstring says it loads settings 'as-is without unflattening' but this contradicts the format handling explanation

**Affected files:**
- `src/settings.py`

**Details:**
The load() method docstring states:
'Format handling: Settings are stored on disk in flattened format (e.g., {\'editor.auto_number\': True}) but this method loads them as-is without unflattening.'

This is confusing because:
1. The backend.load_global() and backend.load_project() return already-flattened dicts from JSON
2. The comment says 'loads them as-is' which is correct
3. But then says 'without unflattening' which implies unflattening might be expected
4. The _unflatten_settings() method exists but is never called

The comment should clarify that unflattening is intentionally not performed.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation about Redis TTL duration

**Affected files:**
- `src/settings.py`
- `src/settings_backend.py`

**Details:**
In settings_backend.py RedisSettingsBackend._set_data():
Comment says: '# Set with TTL of 24 hours (matches NiceGUI session expiry)'
Code: self.redis.setex(self.redis_key, 86400, data)

However, there's no documentation in settings.py or the module docstring explaining this 24-hour TTL behavior, which could lead to unexpected data loss for users.

---

#### code_vs_documentation

**Description:** Comments mention settings not included but don't explain why they're documented as excluded

**Affected files:**
- `src/settings_definitions.py`

**Details:**
In settings_definitions.py, there are comments like:
'# Note: editor.tab_size setting not included - BASIC uses line numbers for program structure, not indentation, so tab size is not a meaningful setting for BASIC source code'

And:
'# Note: Line numbers are always shown - they\'re fundamental to BASIC! editor.show_line_numbers setting not included - makes no sense for BASIC'

These are good explanatory comments, but there's no corresponding documentation in the module docstring or settings.py explaining why certain common editor settings are intentionally omitted. Users might expect these settings to exist.

---

#### documentation_inconsistency

**Description:** Module docstrings describe different storage locations with slightly different wording

**Affected files:**
- `src/settings.py`
- `src/settings_backend.py`

**Details:**
settings.py docstring:
'- Global: ~/.mbasic/settings.json (Linux/Mac) or %APPDATA%/mbasic/settings.json (Windows)'

settings_backend.py FileSettingsBackend docstring:
'- Global: ~/.mbasic/settings.json (Linux/Mac) or %APPDATA%/mbasic/settings.json (Windows)'

These are identical, which is good. However, the implementation in _get_global_settings_path() uses:
os.getenv('APPDATA', os.path.expanduser('~'))

This means if APPDATA is not set on Windows, it falls back to home directory, not %APPDATA%. The documentation should mention this fallback behavior.

---

#### code_vs_comment

**Description:** RedisSettingsBackend docstring says 'No disk writes in this mode' but default_settings are loaded from disk

**Affected files:**
- `src/settings_backend.py`

**Details:**
RedisSettingsBackend class docstring states:
'- No disk writes in this mode (Redis is the only storage)'

However, the __init__ method accepts default_settings parameter, and create_settings_backend() loads these from disk:
'# Load default settings from disk
file_backend = FileSettingsBackend(project_dir)
default_settings = file_backend.load_global()'

So there IS a disk read (though no disk write). The docstring should say 'No disk writes in this mode (Redis is the only write target, but defaults may be read from disk on initialization)'

---

#### code_vs_comment

**Description:** Module docstring says lexer uses SimpleKeywordCase but doesn't explain why advanced policies aren't needed in lexer

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
Module docstring states:
'The lexer (src/lexer.py) uses SimpleKeywordCase because keywords only need force-based policies in the tokenization phase. Advanced policies are handled later in the parsing/serialization phase by KeywordCaseManager.'

This explanation is good but incomplete. It doesn't explain WHY keywords only need force-based policies during tokenization. A reader might wonder: why can't the lexer use KeywordCaseManager directly? What's the architectural reason for this split?

The answer (likely) is that the lexer needs to normalize keywords for parsing, while preserving case is only needed for output serialization. But this isn't stated explicitly.

---

#### code_vs_comment

**Description:** _flatten_settings() and _unflatten_settings() are inverse operations but _unflatten_settings() is never called

**Affected files:**
- `src/settings.py`

**Details:**
The SettingsManager class defines both:
- _flatten_settings(): Used in _save_global() and _save_project()
- _unflatten_settings(): Never called anywhere in the codebase

The docstrings describe them as inverse operations:
'Flatten nested settings dict for JSON storage' vs 'Unflatten settings dict for internal storage'

But if _unflatten_settings() is never used, why does it exist? Either:
1. It's dead code that should be removed
2. It's reserved for future use (should be documented)
3. There's a bug where it should be called but isn't

---

#### Documentation inconsistency

**Description:** Incomplete list of backend types in docstring

**Affected files:**
- `src/ui/base.py`

**Details:**
base.py UIBackend docstring lists:
"Different UIs can implement this interface:
- CLIBackend: Terminal-based REPL (interactive command mode)
- CursesBackend: Full-screen terminal UI with visual editor
- TkBackend: Desktop GUI using Tkinter"

However, only CLIBackend is actually implemented in the provided files. CursesBackend and TkBackend are mentioned but not shown. The comment about "Future/potential backend types" mentions WebBackend and BatchBackend, but the main list includes TkBackend which may also be unimplemented.

---

#### Code vs Comment conflict

**Description:** Comment about prefix stripping is overly detailed and potentially confusing

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
In _create_setting_widget() method, when creating enum radio buttons:

Comment: "# Create display label (strip 'force_' prefix from beginning for cleaner display)
# Note: Both removeprefix() and the fallback [6:] only strip from the beginning,
# ensuring we don't modify 'force_' appearing elsewhere in the string"

The second note is unnecessarily defensive - removeprefix() by definition only removes from the beginning, and the fallback code explicitly checks startswith('force_') before slicing. The comment seems to defend against a non-existent concern.

---

#### Code vs Comment conflict

**Description:** Docstring claims breakpoints can be set 'at any time' but implementation may have limitations

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
cmd_break() docstring: "Breakpoints can be set at any time (before or during execution). They are checked during program execution at each statement."

However, the implementation in _install_breakpoint_handler() only installs the breakpoint handler when enhance_run_command() is called, and it modifies the interpreter's execute_next method. This suggests breakpoints may only work if set before RUN is called, or the handler installation happens during RUN. The 'at any time' claim may be misleading.

---

#### Documentation inconsistency

**Description:** Module docstring is minimal and doesn't explain usage context

**Affected files:**
- `src/ui/capturing_io_handler.py`

**Details:**
capturing_io_handler.py docstring: "Capturing IO Handler for output buffering. This module provides a simple IO handler that captures output to a buffer, used by various UI backends for executing commands and capturing their output."

However, none of the provided UI backend files (cli.py, base.py) actually use CapturingIOHandler. The docstring claims it's "used by various UI backends" but there's no evidence of this in the provided code.

---

#### Code vs Comment conflict

**Description:** Comment about comparing actual values is redundant with code

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
In _on_reset() method:

Comment: "# Note: Compares actual value (stored in _actual_value) not display label
# since display labels have 'force_' prefix stripped (see _create_setting_widget)"

The code immediately below: "rb.set_state(rb._actual_value == defn.default)"

The comment explains what the code obviously does. The note about display labels having prefix stripped is useful context, but the first line of the comment just restates the code.

---

#### code_vs_comment

**Description:** Comment about target_column default value doesn't match actual column calculation

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In keypress() method docstring:
"Note: Methods like _sort_and_position_line use a default target_column of 7,
which assumes typical line numbers (status=1 char + number=5 digits + space=1 char)."

But the actual column calculation varies because line numbers are variable width. A line number '10' would have code starting at column 4 (status=1 + '10'=2 + space=1), not column 7. The comment assumes 5-digit line numbers which contradicts the variable-width implementation.

---

#### code_vs_comment

**Description:** Comment about line number width in _format_line contradicts class docstring

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _format_line() docstring:
"Returns:
    Formatted string or urwid markup: 'S<num> CODE' where S is status (1 char),
    <num> is the line number (variable width, no padding)"

But class docstring says:
"Field 2 (variable width): Line number (1-5 digits, no padding)"

One says 'variable width' without limit, the other says '1-5 digits'. The code implementation allows beyond 5 digits (checks for 99999 limit in auto-numbering).

---

#### code_vs_comment

**Description:** Comment in _update_display says format is 'S<num> ' but doesn't mention variable width

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment in _update_display():
"# Format: 'S<num> ' where S=status (1 char space), <num>=line# (variable width), space (1)"

This correctly mentions variable width, but earlier class docstring says '1-5 digits'. The inconsistency is between different comments in the same file.

---

#### code_vs_comment

**Description:** Bug fix comment mentions wrong behavior about next_auto_line_num

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment in _update_display():
"# DON'T increment counter here - that happens only on Enter
# Bug fix: Incrementing here caused next_auto_line_num to advance prematurely,
# displaying the wrong line number before the user typed anything"

But looking at the keypress() method, next_auto_line_num IS incremented after inserting a new line:
self.next_auto_line_num = next_num + self.auto_number_increment

The comment is correct that it shouldn't increment in _update_display(), but the explanation about 'only on Enter' is accurate with current code.

---

#### code_vs_comment

**Description:** Comment says immediate_io is recreated in start() but code shows it's created in both __init__ and start()

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~220 says:
# 2. immediate_io (OutputCapturingIOHandler) - Used for immediate mode commands
#    Created here temporarily, then RECREATED in start() with fresh instance each time

Code shows:
- Line ~235: immediate_io = OutputCapturingIOHandler() in __init__
- Line ~245: self.immediate_executor = ImmediateExecutor(..., immediate_io) in __init__
- Line ~1020: immediate_io = OutputCapturingIOHandler() in start()
- Line ~1021: self.immediate_executor = ImmediateExecutor(..., immediate_io) in start()

Comment is accurate but could clarify that the __init__ creation is intentionally temporary.

---

#### code_vs_comment

**Description:** Comment about toolbar removal references Ctrl+U menu but doesn't explain what Ctrl+U does

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~337 says:
# Toolbar removed from UI layout - use Ctrl+U menu instead for keyboard navigation
# Note: The _create_toolbar method is fully implemented but intentionally not used

The comment assumes reader knows what 'Ctrl+U menu' is, but doesn't explain it's the interactive menu bar. Could be clearer: 'use Ctrl+U interactive menu bar instead'.

---

#### code_vs_comment

**Description:** Comment about clear output removal is inconsistent with implementation

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1150 says:
# Note: Clear output removed from keyboard shortcuts (no dedicated key)
# Clear output still available via menu: Ctrl+U -> Output -> Clear Output

However, _clear_output() method exists at line ~1152 and is fully implemented. The comment suggests the feature was removed from shortcuts but is still available via menu, which is accurate. However, the placement of this comment in _handle_input() is odd since it's not near any clear output handling code.

---

#### code_vs_comment

**Description:** Comment about positioning cursor at column 7 uses hardcoded value inconsistent with variable-width line numbers

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~1620 says:
# Position cursor on the new line, at the code area (column 7)

Code at line ~1623:
new_cursor_pos = sum(len(lines[i]) + 1 for i in range(line_index)) + 7

The hardcoded '+ 7' assumes fixed-width line numbers (status + 5-digit line number + space = 7 chars). However, earlier comments and code (line ~1495, ~1500) mention 'variable width' line numbers. This is inconsistent - either line numbers are variable width (and column 7 is wrong) or they're fixed width (and 'variable width' comments are wrong).

---

#### code_vs_comment

**Description:** Comment about main widget storage strategy differs between methods but implementation is consistent

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple comments explain main widget storage:

1. _show_help (line ~582): "Main widget retrieval: Use self.base_widget (stored at UI creation time in __init__) rather than self.loop.widget (which reflects the current widget and might be a menu or other overlay)."

2. _activate_menu (line ~656): "Extract base widget from current loop.widget to unwrap any existing overlay. This differs from _show_help/_show_keymap/_show_settings which use self.base_widget directly, since menu needs to work even when other overlays are already present."

The comments correctly describe different strategies but could be confusing without understanding the full context of when each method is called.

---

#### code_vs_comment

**Description:** Status bar update comments are inconsistent with actual behavior

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple locations have comments like:
"# Status bar stays at default - error is displayed in output" (lines ~1149, ~1213, ~1244)
"# No status bar update - program output will show in output window" (line ~1218)

However, some error paths DO update the status bar:
Line ~1306: "self.status_bar.set_text('Internal error - See output')"

The comments suggest status bar is never updated for errors, but code shows it is updated in some cases.

---

#### code_vs_comment

**Description:** Comment about PC setting timing is verbose but accurate

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at lines ~1176-1182:
"# If start_line is specified (e.g., RUN 100), set PC to that line
# This must happen AFTER interpreter.start() because start() calls setup()
# which resets PC to the first line in the program. By setting PC here,
# we override that default and begin execution at the requested line."

This comment is accurate and helpful, explaining the timing dependency. Not an inconsistency, but notable for its thoroughness.

---

#### code_vs_comment

**Description:** Comment suggests CapturingIOHandler is duplicated and should be extracted, but then imports it from shared location

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment says: "# (duplicates definition in _run_program - consider extracting to shared location)"
But code immediately does: "# Import shared CapturingIOHandler
from .capturing_io_handler import CapturingIOHandler"

The comment is outdated - the extraction has already been done.

---

#### code_vs_comment

**Description:** Comment in _sync_program_to_runtime says 'Sync program to runtime without resetting PC' but then conditionally resets PC to halted

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Docstring: "Sync program to runtime without resetting PC.

Updates runtime's statement_table and line_text_map from self.program,
but preserves current PC/execution state."

But code does: "else:
    # No execution in progress or paused at breakpoint - ensure halted
    self.runtime.pc = PC.halted_pc()
    self.runtime.halted = True"

The docstring is misleading - PC is conditionally reset, not always preserved.

---

#### code_vs_comment

**Description:** Comment in _on_autosave_recovery_response mentions filtering blank lines but the logic filters lines without code, which is different

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment: "# Filter out blank lines (lines with only line number, no code)"

But code filters: "if code:" where code is the part after line number.

A blank line would be completely empty, but this filters lines that have a line number but no code. The comment is imprecise.

---

#### documentation_inconsistency

**Description:** Docstring example format inconsistency with actual macro format

**Affected files:**
- `src/ui/help_macros.py`

**Details:**
Module docstring shows examples:
"Examples:
  {{kbd:help}} → looks up 'help' action in current UI's keybindings and returns
                  the primary keybinding for that action
  {{kbd:save:curses}} → looks up 'save' action in Curses UI specifically"

But _expand_kbd() docstring at line ~95 shows different format:
"Formats:
- 'action' - searches current UI (e.g., 'help', 'save', 'run')
- 'action:ui' - searches specific UI (e.g., 'save:curses', 'run:tk')"

The module docstring uses {{kbd:save:curses}} format (action:ui), but the method docstring describes it as 'save:curses' (without the kbd prefix). This is confusing because the method receives the argument after 'kbd:' is stripped, but the examples should clarify this.

---

#### code_vs_comment_conflict

**Description:** Version comment mentions separate implementation version but doesn't explain relationship

**Affected files:**
- `src/ui/help_macros.py`

**Details:**
Comment at line ~82:
"# Hardcoded MBASIC version for documentation
# Note: Project has internal implementation version (src/version.py) separate from this
return \"5.21\"  # MBASIC 5.21 language version"

The comment mentions src/version.py but doesn't explain why there are two versions or when to use which. This could lead to confusion about which version to update when releasing. The comment should clarify that 5.21 is the BASIC language dialect version (compatibility target) while src/version.py is the interpreter implementation version.

---

#### code_inconsistency

**Description:** Menu uses keybindings module but doesn't use KeybindingLoader class

**Affected files:**
- `src/ui/interactive_menu.py`

**Details:**
interactive_menu.py imports keybindings module at line ~4:
from . import keybindings as kb
from .keybindings import key_to_display

And uses it throughout to get key constants like kb.NEW_KEY, kb.SAVE_KEY, etc.

However, keybinding_loader.py provides a KeybindingLoader class that loads keybindings from JSON. The interactive_menu.py appears to use a different keybindings module (possibly a legacy module with hardcoded constants) rather than the JSON-based loader.

This creates an inconsistency where some parts of the codebase use JSON-based keybindings (help_macros.py, keybinding_loader.py) while others use a different system (interactive_menu.py).

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for link navigation between comment and code

**Affected files:**
- `src/ui/help_widget.py`

**Details:**
Comment at line ~234 uses term 'visual link' to describe all [text] patterns found in display.

But the code uses multiple terms:
- 'visual_to_renderer_link' (line ~296)
- 'visual_link_urls' (line ~297)
- 'current_links' (line ~52)
- 'link_positions' (line ~53)

The terminology mixing 'visual link', 'renderer link', and just 'link' could be confusing. A consistent naming convention would improve clarity.

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

**Description:** Comment says STOP_KEY is 'Shown in debugger context in the Debugger category' implying it's not in KEYBINDINGS_BY_CATEGORY, but it IS included in the Debugger category

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Line 221 comment:
# - STOP_KEY (Ctrl+X) - Shown in debugger context in the Debugger category

But line 250 in KEYBINDINGS_BY_CATEGORY:
'Debugger (when program running)': [
    (key_to_display(CONTINUE_KEY), 'Continue execution (Go)'),
    (key_to_display(STEP_LINE_KEY), 'Step Line - execute all statements on current line'),
    (key_to_display(STEP_KEY), 'Step Statement - execute one statement at a time'),
    (key_to_display(STOP_KEY), 'Stop execution (eXit)'),
    (key_to_display(VARIABLES_KEY), 'Show/hide variables window'),
]

STOP_KEY is included, so the comment is misleading.

---

#### Code inconsistency

**Description:** Inconsistent handling of missing JSON keys - some use if/else with defaults, others just use defaults in the else clause

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Most keys follow this pattern:
_run_from_json = _get_key('editor', 'run')
RUN_KEY = _ctrl_key_to_urwid(_run_from_json) if _run_from_json else 'ctrl r'

But this pattern is inconsistent - if JSON is the source of truth, why have hardcoded defaults? The module docstring says 'edit that JSON file rather than changing constants here', but the code has fallback defaults.

---

#### Documentation inconsistency

**Description:** Module docstring says keybindings are loaded from JSON and should be edited there, but code has hardcoded fallback defaults for every key

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Lines 3-10:
"""Keyboard binding definitions for MBASIC Curses UI.

This module loads keybindings from curses_keybindings.json and provides them
in the format expected by the Curses UI (urwid key names, character codes, display names).

This ensures consistency between the JSON config, the UI behavior, and the documentation.

File location: curses_keybindings.json is located in the src/ui/ directory (same directory as this module).
If you need to modify keybindings, edit that JSON file rather than changing constants here.
"""

But throughout the code (lines 136-195), every key has a hardcoded default:
RUN_KEY = _ctrl_key_to_urwid(_run_from_json) if _run_from_json else 'ctrl r'

This contradicts the 'single source of truth' claim.

---

#### Code inconsistency

**Description:** MENU_KEY is hardcoded and not loaded from JSON, despite module claiming all keybindings come from JSON

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Line 124:
# Menu system (not in JSON, hardcoded)
MENU_KEY = 'ctrl u'

This is explicitly hardcoded and not in JSON, which contradicts the module's stated purpose of loading all keybindings from JSON.

---

#### Code inconsistency

**Description:** Several keys are hardcoded and not loaded from JSON: CLEAR_BREAKPOINTS_KEY, DELETE_LINE_KEY, RENUMBER_KEY, INSERT_LINE_KEY, STOP_KEY, SETTINGS_KEY, MAXIMIZE_OUTPUT_KEY

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Lines 167-197:
CLEAR_BREAKPOINTS_KEY = 'ctrl shift b'
DELETE_LINE_KEY = 'ctrl d'
RENUMBER_KEY = 'ctrl e'
INSERT_LINE_KEY = 'ctrl y'
STOP_KEY = 'ctrl x'
SETTINGS_KEY = 'ctrl p'
MAXIMIZE_OUTPUT_KEY = 'ctrl shift m'

These are all hardcoded, not loaded from JSON, despite module docstring saying to edit JSON file for keybindings.

---

#### Code inconsistency

**Description:** All navigation and dialog keys are hardcoded, not loaded from JSON

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Lines 203-215 and 260-268:
TAB_KEY = 'tab'
ENTER_KEY = 'enter'
ESC_KEY = 'esc'
BACKSPACE_KEY = 'backspace'
DOWN_KEY = 'down'
UP_KEY = 'up'
LEFT_KEY = 'left'
RIGHT_KEY = 'right'
VARS_SORT_MODE_KEY = 's'
VARS_SORT_DIR_KEY = 'd'
VARS_EDIT_KEY = 'e'
VARS_FILTER_KEY = 'f'
VARS_CLEAR_KEY = 'c'
DIALOG_YES_KEY = 'y'
DIALOG_NO_KEY = 'n'
SETTINGS_APPLY_KEY = 'ctrl a'
SETTINGS_RESET_KEY = 'ctrl r'

All hardcoded, not from JSON.

---

#### Code vs Comment conflict

**Description:** Function _format_key_display converts 'Ctrl+' to '^' notation, but keybindings.py key_to_display() already does this conversion

**Affected files:**
- `src/ui/keymap_widget.py`

**Details:**
keymap_widget.py lines 8-22:
def _format_key_display(key_str):
    """Convert Ctrl+ notation to ^ notation for consistency.

    Args:
        key_str: Key string like "Ctrl+F" or "^F"

    Returns:
        Formatted string using ^ notation like "^F"
    """
    if key_str.startswith('Ctrl+'):
        # Convert "Ctrl+F" to "^F"
        return '^' + key_str[5:]
    elif key_str.startswith('Shift+Ctrl+'):
        # Convert "Shift+Ctrl+V" to "Shift+^V"
        return 'Shift+^' + key_str[11:]
    return key_str

But keybindings.py key_to_display() (lines 107-130) already returns strings like '^F' and '^Shift+B'. The keymap_widget is receiving already-formatted strings from KEYBINDINGS_BY_CATEGORY which uses key_to_display(). This function appears redundant or the input format assumption is wrong.

---

#### Documentation inconsistency

**Description:** Module docstring says 'Not thread-safe (no locking mechanism)' but doesn't explain if this is intentional or a limitation

**Affected files:**
- `src/ui/recent_files.py`

**Details:**
Lines 1-23:
"""Recent Files Manager - Shared module for tracking recently opened files

This module provides a simple, portable way to track recently opened files
across all UIs (Tk, Curses, Web). Files are stored in a JSON file in the
user's config directory.

Features:
- Stores last 10 recently opened files
- Records full path and last access timestamp
- Automatically creates config directory if needed
- Cross-platform (uses pathlib)
- Note: Not thread-safe (no locking mechanism)

The note about thread-safety is mentioned but not explained. Is this a known limitation? Should users be warned about concurrent access issues?

---

#### Code vs Comment conflict

**Description:** Comment describes path normalization duplication but doesn't specify exact maintenance requirements

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Line 289 comment in _follow_link():
Note: Path normalization logic is duplicated in _open_link_in_new_window().
Both methods use similar approach: resolve relative paths, normalize to help_root,
handle path separators. If modification needed, update both methods consistently.

Line 638 comment in _open_link_in_new_window():
Note: Path normalization logic is duplicated from _follow_link().
Both methods resolve paths relative to help_root with similar logic.
If modification needed, update both methods consistently.

The comments acknowledge duplication but the code has not been refactored to eliminate it. This creates a maintenance burden where changes must be synchronized across two methods. The comments warn about this but don't indicate if this is intentional (e.g., for performance) or technical debt.

---

#### Code vs Comment conflict

**Description:** Comment suggests possible duplication with markdown_renderer.py but doesn't confirm if it exists

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Line 673 comment in _format_table_row():
Note: This implementation may be duplicated in src/ui/markdown_renderer.py.
If both implementations exist and changes are needed to table formatting logic,
consider extracting to a shared utility module to maintain consistency.

The comment uses 'may be duplicated' which indicates uncertainty. If the duplication exists, it should be confirmed and addressed. If it doesn't exist, the comment should be removed. The uncertainty creates ambiguity about whether this is a known issue or speculation.

---

#### Code vs Comment conflict

**Description:** Comment about link tag prefixes may be outdated or incomplete

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Line 558 comment in _create_context_menu():
Note: Both "link_" (from _render_line_with_links) and "result_link_"
(from _execute_search) prefixes are checked. Both types are stored
identically in self.link_urls, but the prefixes distinguish their origin.

However, examining the code:
- Line 211: _render_line_with_links creates tags like 'link_{counter}'
- Line 396: _execute_search creates tags like 'result_link_{counter}'
- Line 560: Context menu checks for both 'link_' and 'result_link_' prefixes

The comment is accurate, but the distinction between prefixes serves no functional purpose in the current implementation since both are handled identically. The comment explains the distinction but doesn't explain why it exists or if it's needed.

---

#### Documentation inconsistency

**Description:** Comment about modal behavior is technically imprecise

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Line 42 comment:
# Make modal (prevents interaction with parent, but doesn't block code execution - no wait_window())
self.transient(parent)
self.grab_set()

The comment states the dialog is 'modal' but then clarifies it doesn't block code execution because wait_window() is not called. In Tkinter terminology, a true modal dialog blocks execution with wait_window(). This dialog is more accurately described as 'application-modal' (grab_set prevents interaction with other windows) but not 'execution-modal'. The comment is trying to clarify this distinction but uses imprecise terminology that could confuse readers.

---

#### Code vs Comment conflict

**Description:** Comment describes inline label as 'not a hover tooltip' but this clarification may be unnecessary

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Line 145 comment:
# Show short help as inline label (not a hover tooltip, just a gray label)
if defn.help_text:
    help_label = ttk.Label(frame, text=defn.help_text,
                          foreground='gray', font=('TkDefaultFont', 9))
    help_label.pack(side=tk.LEFT, padx=(10, 0))

The comment explicitly states 'not a hover tooltip' which seems to be clarifying against a potential misunderstanding. However, the code clearly creates a Label widget, not a tooltip. The comment may be addressing a previous implementation or anticipated confusion, but it's unclear why this clarification is needed.

---

#### Code vs Comment conflict

**Description:** Comment about failed restore tracking doesn't explain why tracking is necessary

**Affected files:**
- `src/ui/tk_settings_dialog.py`

**Details:**
Line 197 comment:
# Track failed restores - user should know if settings couldn't be restored
failed_keys.append(key)

The comment explains that failed restores are tracked so the user can be informed, which is shown in the warning dialog at lines 203-210. However, the comment doesn't explain why restores might fail in the first place. If set_setting() can fail during restore, it could also fail during apply, but the apply logic (lines 172-180) shows an error and returns False immediately on first failure, while restore continues and collects all failures. This asymmetry isn't explained.

---

#### Code vs Documentation inconsistency

**Description:** Module docstring lists features but doesn't mention context menu dismiss behavior

**Affected files:**
- `src/ui/tk_help_browser.py`

**Details:**
Module docstring (lines 1-10) lists features:
- Scrollable help content display with markdown rendering
- Clickable links with navigation history (back button and home button)
- Search across multi-tier help system with ranking and fuzzy matching
- Search result display with tier markers (Language/MBASIC/UI)
- In-page search (Ctrl+F) with match highlighting and navigation
- Context menu with copy operations and 'Open in New Window' for links
- Table formatting for markdown tables

However, the context menu implementation (lines 577-580) includes ESC and FocusOut bindings to dismiss the menu:
menu.bind('<FocusOut>', lambda e: dismiss_menu())
menu.bind('<Escape>', lambda e: dismiss_menu())

This dismiss behavior is a feature of the context menu but isn't mentioned in the feature list. While minor, it's part of the user interaction model.

---

#### code_vs_comment

**Description:** Docstring describes 3-pane layout with specific weights but implementation may differ

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring (lines 48-52):
'- 3-pane vertical layout (weights: 3:2:1 = total 6 units):
  * Editor with line numbers (top, ~50% = 3/6 - weight=3)
  * Output pane (middle, ~33% = 2/6 - weight=2)
    - Contains INPUT row (shown/hidden dynamically for INPUT statements)
  * Immediate mode input line (bottom, ~17% = 1/6 - weight=1)'

Code (lines 177-189):
paned.add(editor_frame, weight=3)
paned.add(output_frame, weight=2)
paned.add(immediate_frame, weight=1)

The weights match, but the immediate mode pane contains more than just 'input line' - it has a prompt label, entry, and execute button. The docstring simplifies this as 'input line'.

---

#### code_vs_comment

**Description:** Comment about Ctrl+I binding location conflicts with actual binding location

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment in _create_menu() (lines 424-425):
'# Note: Ctrl+I is bound directly to editor text widget in start() (not root window)
# to prevent tab key interference - see editor_text.text.bind('<Control-i>', ...)'

Actual binding in start() (line 195):
self.editor_text.text.bind('<Control-i>', self._on_ctrl_i)

The comment is accurate about the binding location, but the cross-reference format 'see editor_text.text.bind...' is vague. The comment appears in _create_menu() but could be clearer about the exact line number in start().

---

#### code_vs_comment

**Description:** Toolbar comment mentions removed features but doesn't explain why they were removed

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment in _create_toolbar() (lines 455-459):
'# Note: Toolbar has been simplified to show only essential execution controls.
# Additional features are accessible via menus:
# - List Program → Run > List Program
# - New Program (clear) → File > New
# - Clear Output → Run > Clear Output'

This comment documents that features were removed from the toolbar but doesn't explain the rationale (e.g., 'to reduce clutter', 'based on user feedback', etc.). It's informative but incomplete.

---

#### documentation_inconsistency

**Description:** Docstring example shows TkIOHandler created without backend but doesn't show how backend is set later

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring Usage example (lines 54-62):
'Usage:
    from src.ui.tk_ui import TkBackend, TkIOHandler
    from src.editing.manager import ProgramManager

    io = TkIOHandler()  # TkIOHandler created without backend reference initially
    def_type_map = {}  # Type suffix defaults for variables (DEFINT, DEFSNG, etc.)
    program = ProgramManager(def_type_map)
    backend = TkBackend(io, program)
    backend.start()  # Runs Tk mainloop until window closed'

The comment says 'TkIOHandler created without backend reference initially' but doesn't show how the backend reference is set later. The code in __init__ creates a new TkIOHandler (line 318: tk_io = TkIOHandler(self._add_output, self.root, backend=self)), suggesting the example is incomplete or outdated.

---

#### code_vs_comment

**Description:** Comment about OPTION BASE validation contradicts defensive else clause

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _edit_array_element method around line 1033:
Comment says: "# OPTION BASE only allows 0 or 1 (validated by OPTION statement parser).\n# The else clause is defensive programming for unexpected values."

Then code has:
if array_base == 0:
    default_subscripts = ','.join(['0'] * len(dimensions))
elif array_base == 1:
    default_subscripts = ','.join(['1'] * len(dimensions))
else:
    # Defensive fallback for invalid array_base (should not occur)
    default_subscripts = ','.join(['0'] * len(dimensions))

If OPTION BASE truly only allows 0 or 1 and this is validated, the else clause should never execute. The comment acknowledges this but the defensive code suggests uncertainty about the validation.

---

#### code_vs_comment

**Description:** Comment about validation timing may be outdated or incomplete

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _validate_editor_syntax method around line 1502:
Comment says: "# Note: This method is called:\n# - With 100ms delay after cursor movement/clicks (to avoid excessive validation during rapid editing)\n# - Immediately when focus leaves editor (to ensure validation before switching windows)"

However, looking at the actual call sites:
- _on_cursor_move: calls with 100ms delay (matches comment)
- _on_mouse_click: calls with 100ms delay (matches comment)
- _on_focus_out: calls immediately (matches comment)
- _on_enter_key: calls _save_editor_to_program which validates, but this isn't mentioned in the comment

The comment is incomplete about all the places validation occurs.

---

#### code_vs_comment

**Description:** Comment about Tk Text widget design is explanatory but could be clearer

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _remove_blank_lines method around line 1577:
Comment says: "Removes blank lines to keep program clean, but preserves the final\nline. Tk Text widgets always end with a newline character (Tk design -\ntext content ends at last newline, so there's always an empty final line)."

The parenthetical explanation about Tk design is helpful but the phrasing "text content ends at last newline" is confusing. It would be clearer to say "Tk Text widgets always maintain a trailing newline, so the final line appears empty."

---

#### code_vs_comment

**Description:** Comment about blank line removal scheduling is misleading about timing

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_key_press() at line ~1530:
Comment: "Schedule blank line removal after key is processed"
Code: self.root.after(10, self._remove_blank_lines)

The comment says 'after key is processed' but the 10ms delay is arbitrary and not tied to key processing completion. The key might be processed in <1ms or the scheduled callback might fire before key processing completes.

---

#### code_vs_comment

**Description:** Comment about parity bit clearing is redundant with function name

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_paste() at line ~1370:
Comment: "Sanitize: clear parity bits and filter control characters"
Code: sanitized_text, was_modified = sanitize_and_clear_parity(clipboard_text)

The function name 'sanitize_and_clear_parity' already indicates it clears parity bits, making the comment redundant. This is a minor documentation style issue.

---

#### code_vs_comment

**Description:** Comment about statement highlighting uses ambiguous term 'brief flash effect'

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _execute_tick() at line ~2140:
Comment: "Running - highlight current statement (brief flash effect)"

The term 'brief flash effect' is misleading because:
1. The highlight is applied and stays until the next tick (10ms later)
2. There's no explicit 'flash' animation or rapid on/off toggling
3. The highlight persists during the statement's execution

The comment should say 'highlight current statement during execution' or 'highlight current statement (cleared on next tick)'.

---

#### code_vs_comment

**Description:** Docstring for _add_immediate_output() says it adds to main output pane, but the method name suggests it should add to immediate output pane

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Method: _add_immediate_output()
Docstring: "Add text to main output pane.\n\nNote: This method name is historical/misleading - it actually adds to the main output pane, not a separate immediate output pane."

The docstring acknowledges the name is misleading but the method name hasn't been updated to reflect its actual purpose (e.g., could be renamed to _add_output_from_immediate or similar).

---

#### documentation_inconsistency

**Description:** Dead code documentation for _setup_immediate_context_menu() references related dead code methods but doesn't list all of them

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment says: "DEAD CODE: This method is never called because immediate_history is always None in the Tk UI (see __init__). Retained for potential future use if immediate mode gets its own output widget. Related dead code: _copy_immediate_selection() and _select_all_immediate()."

However, the method _setup_immediate_context_menu() itself is also dead code but isn't listed in its own 'Related dead code' list. This is a minor documentation incompleteness.

---

#### code_vs_comment

**Description:** _parse_line_number() docstring comment about MBASIC 5.21 requirement is informative but not verified in code

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment in _parse_line_number() states:
"# MBASIC 5.21 requires whitespace (or end of line) between line number and statement"

This is a historical/specification note, but there's no verification that this matches actual MBASIC 5.21 behavior. The regex implementation `r'^(\d+)(?:\s|$)'` enforces this rule, but if MBASIC 5.21 actually allows other cases, this would be a bug.

---

#### code_vs_comment

**Description:** _on_cursor_move() has detailed comment about after_idle scheduling that may be overly specific

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment says:
"# Schedule deletion after current event processing to avoid interfering
# with ongoing key/mouse event handling (prevents cursor position issues,
# undo stack corruption, and widget state conflicts during event processing)"

This is very detailed about potential issues (cursor position, undo stack, widget state) but doesn't cite specific bugs or testing that confirmed these issues. If the after_idle is actually just a general best practice, the comment overstates the reasoning.

---

#### documentation_inconsistency

**Description:** Class docstring describes automatic blank line removal but doesn't mention it only happens on cursor movement away from the line

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Class docstring says:
"Automatic blank line removal:
- When cursor moves away from a blank line, that line is automatically deleted
- This helps keep BASIC programs clean by removing accidental blank lines
- Implemented via _on_cursor_move() tracking cursor movement"

This is accurate, but could be clearer that blank lines are NOT removed immediately when created, only when the cursor moves away. A user might expect immediate deletion based on 'automatic blank line removal'.

---

#### code_vs_comment

**Description:** _on_status_click() uses different regex pattern than _parse_line_number() for extracting BASIC line numbers

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
_parse_line_number() uses:
```python
match = re.match(r'^(\d+)(?:\s|$)', line_text)
```

_on_status_click() uses:
```python
match = re.match(r'^\s*(\d+)', line_text)
```

The second pattern allows leading whitespace and doesn't require whitespace/end after the number. This inconsistency means _on_status_click() might match line numbers that _parse_line_number() would reject (e.g., '10REM' would match in _on_status_click but not _parse_line_number). This could cause the click handler to find a line number that has no metadata.

---

#### code_vs_comment

**Description:** Comment in serialize_variable() mentions explicit_type_suffix attribute behavior that may not be consistently set

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment states: "Note: explicit_type_suffix is not always set (depends on parser implementation),
so getattr defaults to False if missing, preventing incorrect suffix output"

This comment acknowledges parser implementation dependency but doesn't clarify when explicit_type_suffix IS set vs when it's missing. The code uses getattr(var, 'explicit_type_suffix', False) to handle missing attribute, but the comment suggests this is a workaround for inconsistent parser behavior rather than intentional design.

---

#### documentation_inconsistency

**Description:** Module docstring claims no UI-framework dependencies but doesn't mention AST node dependencies

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Module docstring states: "No UI-framework dependencies (Tk, curses, web)
are allowed. Standard library modules (os, glob, re) and core interpreter
modules (runtime, parser, AST nodes) are permitted."

The docstring explicitly permits "AST nodes" but many functions (serialize_line, serialize_statement, serialize_expression, etc.) have tight coupling to specific AST node types and their attributes. This creates an implicit dependency on AST node structure that isn't clearly documented as a constraint.

---

#### code_vs_documentation

**Description:** update_line_references() docstring describes two-pattern approach but implementation details differ from description

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring states: "Two-pattern approach (applied sequentially in a single pass):
Pattern 1: Match keyword + first line number (GOTO/GOSUB/THEN/ELSE/ON...GOTO/ON...GOSUB)
Pattern 2: Match comma-separated line numbers (for ON...GOTO/GOSUB lists)"

The description says "single pass" but the code actually applies two separate regex substitutions sequentially (pattern.sub() then comma_pattern.sub()), which is technically two passes over the string. The docstring's "single pass" claim is misleading.

---

#### code_vs_comment

**Description:** Comment in serialize_statement() for RemarkStatementNode mentions REMARK conversion but doesn't explain when it occurs

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Comment states: "Note: REMARK is converted to REM during parsing, not here"

This comment references a parsing behavior (REMARK -> REM conversion) but doesn't clarify whether the AST will ever contain comment_type='REMARK' or if it's always normalized to 'REM' by the parser. The code only checks for 'APOSTROPHE' vs else (which includes REM, REMARK, or default), suggesting the parser might not fully normalize.

---

#### code_vs_documentation

**Description:** cycle_sort_mode() docstring claims to match Tk UI implementation but no verification of actual Tk UI behavior

**Affected files:**
- `src/ui/variable_sorting.py`

**Details:**
Docstring states: "The cycle order is: accessed -> written -> read -> name -> (back to accessed)
This matches the Tk UI implementation."

The comment claims this matches Tk UI but there's no reference to where in the Tk UI this is verified, and no cross-reference to ensure they stay in sync. If Tk UI changes its cycle order, this module won't know.

---

#### code_vs_comment

**Description:** serialize_expression() docstring note about ERR/ERL describes special handling but doesn't explain why they're special

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring note states: "ERR and ERL are special system variables that are serialized without
parentheses (e.g., 'ERR' not 'ERR()') when they appear as FunctionCallNode
with no arguments, matching MBASIC 5.21 syntax."

The note describes the behavior but doesn't explain WHY ERR and ERL are treated differently from other zero-argument functions. Are they the only system variables with this behavior? The comment mentions MBASIC 5.21 compatibility but doesn't clarify if this is a general rule or specific to these two variables.

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

**Description:** Inconsistent terminology for 'immediate mode' vs 'immediate entry' vs 'immediate_entry input box' throughout comments.

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Various comments use different terms:
- 'immediate_entry input box' (line ~1730)
- 'immediate mode input box' (line ~1900)
- 'immediate input box' (line ~1930)

These all refer to the same UI element (self.immediate_entry) but use inconsistent naming in documentation.

---

#### code_vs_comment

**Description:** Docstring for _sync_program_to_runtime describes PC handling as 'conditional preservation' but implementation is actually 'conditional reset'

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Docstring says:
"PC handling (conditional preservation):
- If exec_timer is active (execution in progress): Preserves PC and halted state,
  allowing program to resume from current position after rebuild.
- Otherwise (no active execution): Resets PC to halted state, preventing
  unexpected execution when LIST/edit commands modify the program."

The framing as 'conditional preservation' is misleading - it's actually 'conditional reset'. When timer is active, PC is preserved (no action). When timer is inactive, PC is reset. The primary action is resetting, not preserving.

---

#### code_vs_comment

**Description:** Comment about paste detection threshold claims it's arbitrary but provides specific reasoning

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _on_editor_change() method:

Comment says: "# The 5-char threshold is arbitrary - balances detecting small pastes while avoiding
# false positives from rapid typing (e.g., typing 'PRINT' quickly = 5 chars but not a paste)."

The comment claims the threshold is 'arbitrary' but then provides specific reasoning about balancing paste detection vs rapid typing. If there's reasoning, it's not arbitrary - it's a heuristic with justification.

---

#### code_vs_comment

**Description:** Comment in _execute_immediate says 'Don't create temporary ones!' but doesn't explain why or what the alternative was

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _execute_immediate() method:

Comment says: "# Use the session's single interpreter and runtime
# Don't create temporary ones!"

The emphatic 'Don't create temporary ones!' suggests this was a previous bug or design issue, but there's no context about why temporary instances would be problematic or what issues they caused. This makes the comment less useful for future maintainers.

---

#### documentation_inconsistency

**Description:** Architecture comment about not auto-syncing editor from AST appears in _execute_immediate but doesn't explain what triggers the sync or when it's appropriate

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Comment says: "# Architecture: We do NOT auto-sync editor from AST after immediate commands.
# This preserves one-way data flow (editor → AST → execution) and prevents
# losing user's formatting/comments. Commands that modify code (like RENUM)
# update the editor text directly."

This architectural decision is documented inline but not in a centralized architecture document. The comment also mentions RENUM as an example but doesn't list other commands that modify editor text directly, making it incomplete.

---

#### code_vs_comment

**Description:** Comment in _check_auto_number says 'Don't auto-number if content hasn't changed' but code checks exact equality which may miss semantic equivalence

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _check_auto_number() method:

Comment says: "# Don't auto-number if content hasn't changed
if current_text == self.last_edited_line_text:
    return"

The comment describes intent (content hasn't changed) but the code checks exact string equality. This could miss cases where content is semantically unchanged but has different whitespace or formatting. The comment should be more precise about checking exact text equality.

---

#### code_vs_comment

**Description:** Comment in _sync_program_from_editor uses sys.stderr.write but doesn't import sys at function level

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _sync_program_from_editor() method:

Comment says: "# Using sys.stderr.write directly to ensure output even if logging fails.
sys.stderr.write(f'Warning: Failed to sync program from editor: {e}\n')
sys.stderr.flush()"

The code uses sys.stderr but doesn't show an import statement. While sys may be imported at module level, the comment's emphasis on 'directly' suggests this is critical error handling, so the import should be visible or documented.

---

#### code_vs_comment

**Description:** Docstring for start() method says 'NOT IMPLEMENTED - raises NotImplementedError' but this is redundant with the actual implementation that always raises the exception

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
Docstring at line ~420:
    def start(self):
        """NOT IMPLEMENTED - raises NotImplementedError.

        Web backend cannot be started per-instance. Use start_web_ui() module
        function instead, which creates backend instances per user session.

        Raises:
            NotImplementedError: Always raised
        """
        raise NotImplementedError("Web backend uses start_web_ui() function, not backend.start()")

The docstring is accurate and helpful, but 'NOT IMPLEMENTED' in all caps might be misleading - the method IS implemented, it just intentionally raises an exception. This is more of a style issue than an inconsistency.

---

#### documentation_inconsistency

**Description:** Comment about Redis configuration mentions 'load-balanced instances' but there's no documentation about load balancing setup or requirements

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
At line ~478:
    if redis_url:
        sys.stderr.write(f"Redis storage enabled: {redis_url}\n")
        sys.stderr.write("Session state will be shared across load-balanced instances\n\n")

This implies load balancing is a supported configuration, but there's no documentation about:
- How to set up load balancing
- What load balancer to use
- Any special configuration needed
- Whether sticky sessions are required or not

---

#### code_inconsistency

**Description:** Default storage secret 'dev-default-change-in-production' is used when MBASIC_STORAGE_SECRET is not set, but there's no warning logged about using an insecure default in production

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
At line ~489:
    ui.run(
        title='MBASIC 5.21 - Web IDE',
        port=port,
        storage_secret=os.environ.get('MBASIC_STORAGE_SECRET', 'dev-default-change-in-production'),
        reload=False,
        show=True
    )

The default value name suggests it should be changed in production, but there's no runtime warning if the default is being used. This could be a security issue.

---

#### code_vs_documentation

**Description:** SessionState tracks find/replace state (last_find_text, last_find_position, last_case_sensitive) but find/replace functionality is not documented.

**Affected files:**
- `src/ui/web/session_state.py`
- `docs/help/common/debugging.md`

**Details:**
session_state.py defines:
    last_find_text: str = ''
    last_find_position: int = 0
    last_case_sensitive: bool = False

No documentation exists for:
- How to use find/replace
- Keyboard shortcuts for find/replace
- Find/replace dialog or interface

This suggests an implemented but undocumented feature.

---

#### documentation_inconsistency

**Description:** loops.md explains MBASIC 5.21 lacks EXIT FOR/EXIT WHILE (correct), but debugging.md doesn't mention this limitation when discussing loop debugging.

**Affected files:**
- `docs/help/common/examples/loops.md`
- `docs/help/common/debugging.md`

**Details:**
loops.md correctly states:
'Note: MBASIC 5.21 does not have EXIT FOR or EXIT WHILE statements (those were added in later BASIC versions). GOTO is the standard way to exit loops early in BASIC-80.'

debugging.md section 'Infinite Loops' suggests:
'Press Ctrl+C or Stop button to interrupt'

But doesn't mention that early loop exit requires GOTO, which is relevant for debugging loop logic.

---

#### documentation_inconsistency

**Description:** Compiler documentation exists but version.py shows this is an interpreter (MBASIC 5.21). Unclear if compiler is planned feature or documentation error.

**Affected files:**
- `docs/help/common/compiler/index.md`
- `docs/help/common/compiler/optimizations.md`

**Details:**
version.py states:
MBASIC_VERSION = '5.21'  # The MBASIC version we implement
COMPATIBILITY = '100% MBASIC 5.21 compatible with optional extensions'

MBASIC 5.21 was an interpreter, not a compiler. The compiler documentation describes:
- 27 optimization techniques
- Code generation (marked 'In Progress')
- Semantic analysis phase

This suggests either:
1. Planned compiler extension beyond MBASIC 5.21
2. Documentation from different project
3. Future enhancement documentation

---

#### code_vs_documentation

**Description:** SessionState tracks max_recent_files=10 but recent files feature is not documented anywhere.

**Affected files:**
- `src/ui/web/session_state.py`
- `docs/help/common/debugging.md`

**Details:**
session_state.py defines:
    current_file: Optional[str] = None
    recent_files: List[str] = field(default_factory=list)
    max_recent_files: int = 10

No documentation explains:
- Recent files menu/list
- How to access recent files
- How recent files are tracked
- Maximum limit of 10 files

---

#### documentation_inconsistency

**Description:** Debugging documentation references UI-specific keyboard shortcuts but uses inconsistent placeholder format that may confuse users.

**Affected files:**
- `docs/help/common/debugging.md`

**Details:**
Document uses placeholders like:
- '{{kbd:step:curses}}'
- '{{kbd:continue:curses}}'
- '{{kbd:toggle_stack:tk}}'

But also states:
'See your UI-specific help for keyboard shortcuts (shortcuts vary by UI)'

The placeholder syntax suggests dynamic substitution, but if users see the raw placeholders, they won't know what keys to press. Documentation should either:
1. Explain the placeholder system
2. Use actual key names
3. Always direct to UI-specific help without showing placeholders

---

#### code_vs_comment

**Description:** Comment claims VERSION is auto-incremented by utils/checkpoint.sh, but no verification that this script exists or works as described.

**Affected files:**
- `src/version.py`

**Details:**
Comment states:
'VERSION is automatically incremented by utils/checkpoint.sh after each commit.'
'Manual edits to VERSION will be overwritten by the next checkpoint.'

However:
- No utils/checkpoint.sh file provided in source code
- Cannot verify auto-increment behavior
- Users might manually edit VERSION not knowing it will be overwritten

---

#### documentation_inconsistency

**Description:** Inconsistent statement about line number range

**Affected files:**
- `docs/help/common/getting-started.md`
- `docs/help/common/language.md`

**Details:**
getting-started.md states 'Numbers can be 1-65535' but language.md does not specify the valid range for line numbers. This creates an incomplete reference.

---

#### documentation_inconsistency

**Description:** Inconsistent exponent notation explanation

**Affected files:**
- `docs/help/common/language/data-types.md`

**Details:**
The DOUBLE Precision section states: 'D notation (e.g., 1.5D+10) forces double-precision, required for exponents beyond single-precision range' and 'E notation (e.g., 1.5E+10) uses single-precision by default, converts to double if assigned to # variable'. However, it then says 'For values within single-precision range, D and E are interchangeable when assigned to # variables' which seems to contradict the 'required for exponents beyond single-precision range' statement.

---

#### documentation_inconsistency

**Description:** Incomplete cross-reference in appendices index

**Affected files:**
- `docs/help/common/language/appendices/index.md`
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
appendices/index.md states 'Error handling references (see [Error Handling](../statements/index.md#error-handling) for detailed examples)' but error-codes.md at the bottom has 'See Also' section that links to individual statements like [ON ERROR GOTO](../statements/on-error-goto.md) and [ERR and ERL Variables](../statements/err-erl-variables.md). The index should mention these specific statement references as well.

---

#### documentation_inconsistency

**Description:** Incomplete UI-specific documentation references

**Affected files:**
- `docs/help/common/index.md`

**Details:**
index.md shows a table with keyboard shortcuts for CLI, Curses, Tk, and Web UIs, but the 'For complete shortcuts' section only lists CLI, Curses, Tk, and Web. However, the table shows 'Menu only' for Web's Quit action, suggesting Web might not have all keyboard shortcuts. This inconsistency should be clarified.

---

#### documentation_inconsistency

**Description:** Inconsistent cross-reference descriptions between LOC and LOF

**Affected files:**
- `docs/help/common/language/functions/loc.md`
- `docs/help/common/language/functions/lof.md`

**Details:**
In loc.md, the See Also for LOF says: 'Returns the total file SIZE in bytes (LOC returns current POSITION/record number)'

In lof.md, the See Also for LOC says: 'Returns current file POSITION/record number (LOF returns total SIZE in bytes)'

These are semantically the same but use different formatting and capitalization, which could be standardized for consistency.

---

#### documentation_inconsistency

**Description:** Inconsistent 'See Also' sections across system functions

**Affected files:**
- `docs/help/common/language/functions/fre.md`
- `docs/help/common/language/functions/inkey_dollar.md`
- `docs/help/common/language/functions/inp.md`
- `docs/help/common/language/functions/peek.md`

**Details:**
The system functions (FRE, INKEY$, INP, PEEK) all have nearly identical 'See Also' sections listing each other, but:

1. FRE.md lists 'HELP SET' while others don't
2. The order of items varies between files
3. Some descriptions are slightly different (e.g., VARPTR description)

This suggests these were copy-pasted and manually edited rather than being consistently maintained.

---

#### documentation_inconsistency

**Description:** Similar functions have different example styles

**Affected files:**
- `docs/help/common/language/functions/hex_dollar.md`
- `docs/help/common/language/functions/oct_dollar.md`

**Details:**
HEX$ and OCT$ are parallel functions (convert decimal to hex/octal strings), but their examples are formatted differently:

HEX$ uses:
```basic
10 INPUT X
20 A$ = HEX$(X)
30 PRINT X; "DECIMAL IS "; A$; " HEXADECIMAL"
RUN
? 32
32 DECIMAL IS 20 HEXADECIMAL
Ok

10 PRINT HEX$(255)
RUN
FF
Ok
```

OCT$ uses:
```basic
10 INPUT X
20 A$ = OCT$(X)
30 PRINT X; "DECIMAL IS "; A$; " OCTAL"
RUN
? 64
64 DECIMAL IS 100 OCTAL
Ok

10 PRINT OCT$(255)
RUN
377
Ok
```

These are nearly identical and could be more consistently formatted.

---

#### documentation_inconsistency

**Description:** Mathematical functions have inconsistent 'See Also' sections

**Affected files:**
- `docs/help/common/language/functions/int.md`
- `docs/help/common/language/functions/log.md`
- `docs/help/common/language/functions/sgn.md`
- `docs/help/common/language/functions/sin.md`
- `docs/help/common/language/functions/sqr.md`

**Details:**
The mathematical functions all cross-reference each other in 'See Also' sections, but:

1. INT.md includes CDBL, CINT, CSNG in its See Also
2. LOG.md does NOT include CDBL, CINT, CSNG
3. SGN.md does NOT include CDBL, CINT, CSNG
4. SIN.md does NOT include CDBL, CINT, CSNG
5. SQR.md does NOT include CDBL, CINT, CSNG

This inconsistency suggests INT.md was updated to include type conversion functions but the others were not.

---

#### documentation_inconsistency

**Description:** String extraction functions have inconsistent formatting in examples

**Affected files:**
- `docs/help/common/language/functions/left_dollar.md`
- `docs/help/common/language/functions/right_dollar.md`
- `docs/help/common/language/functions/mid_dollar.md`

**Details:**
LEFT$, RIGHT$, and MID$ are related string extraction functions, but their examples use different formatting:

LEFT$ example has consistent spacing and formatting.

RIGHT$ example has inconsistent spacing:
```basic
10 A$="DISK BASIC-80"
 20 PRINT RIGHT$(A$,8)
 RUN
 BASIC-80
 Ok
```
Note the leading space before line 20 and the output lines.

MID$ example uses different variable names and structure.

These should be more consistently formatted.

---

#### documentation_inconsistency

**Description:** Inconsistent error documentation for I=0 parameter

**Affected files:**
- `docs/help/common/language/functions/instr.md`
- `docs/help/common/language/functions/mid_dollar.md`

**Details:**
Both INSTR and MID$ document that I=0 causes an error, but with different formatting:

INSTR: 'Note: If I=0 is specified, an "Illegal function call" error will occur.'

MID$: 'Note: If I=0 is specified, an "Illegal function call" error will occur.'

These are actually identical, but INSTR places this note after the example while MID$ places it after the example as well. However, the functions behave differently when I is omitted - INSTR defaults to 1, while MID$ returns all characters from position I to the end. This difference could be more clearly documented.

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

**Description:** Inconsistent formatting of version information in frontmatter

**Affected files:**
- `docs/help/common/language/statements/auto.md`
- `docs/help/common/language/statements/chain.md`

**Details:**
auto.md does not have a 'Versions:' field in its content, while chain.md explicitly states '**Versions:** Disk' in the content body. Other documents like string_dollar.md show versions in a consistent format. The version information should be consistently placed either in frontmatter or in a standard location in the content.

---

#### documentation_inconsistency

**Description:** CONT documentation references non-existent example

**Affected files:**
- `docs/help/common/language/statements/cont.md`

**Details:**
The Example section states:
'See example Section 2.61, STOP.'

However, this is a reference to a section number from the original manual that doesn't exist in the current documentation structure. The reference should either point to the actual STOP.md file or include an inline example.

---

#### documentation_inconsistency

**Description:** CLOAD and CSAVE documentation state they are not included in DEC VT180 version but don't clarify modern implementation status

**Affected files:**
- `docs/help/common/language/statements/cload.md`
- `docs/help/common/language/statements/csave.md`

**Details:**
Both documents state:
'**Note:** This command is not included in the DEC VT180 version or modern disk-based systems.'

However, they don't have an 'Implementation Note' section like USR, VARPTR, and CALL do to clearly indicate whether these are implemented in the current Python interpreter. Given they're cassette-specific commands, they likely aren't implemented but this should be explicitly stated.

---

#### documentation_inconsistency

**Description:** CLS documentation states it works in all UI backends but doesn't mention which backends exist

**Affected files:**
- `docs/help/common/language/statements/cls.md`

**Details:**
The documentation states:
'**Note:** CLS is implemented in MBASIC and works in all UI backends.'

This implies multiple UI backends exist but doesn't reference where to find information about them. Other system-level commands don't mention UI backends at all.

---

#### documentation_inconsistency

**Description:** COMMON documentation has incomplete example with ellipsis

**Affected files:**
- `docs/help/common/language/statements/common.md`

**Details:**
The example shows:
'100 COMMON A,B,C,D(),G$
               110 CHAIN "PROG3",10
                    •'

The bullet point (•) and unusual indentation suggest this is a fragment from the original manual that wasn't fully adapted. The example should be complete and properly formatted.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for type specification

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`
- `docs/help/common/language/statements/defint-sng-dbl-str.md`

**Details:**
def-fn.md uses 'type suffix' (e.g., 'Type suffix % forces integer result') while defint-sng-dbl-str.md uses 'type declaration character' (e.g., 'a type declaration character always takes precedence'). Both refer to the same concept (%, $, #, !) but use different terminology.

---

#### documentation_inconsistency

**Description:** Loop iteration count example appears incorrect

**Affected files:**
- `docs/help/common/language/statements/for-next.md`

**Details:**
for-next.md states: 'FOR I = 1 TO 10 executes with I=1,2,3,...,10 (11 iterations)'. This should be 10 iterations, not 11. The loop executes with I=1,2,3,4,5,6,7,8,9,10 which is 10 values. The explanation that follows ('After I=10 executes, NEXT increments to 11, test fails (11 > 10), loop exits') is correct about the termination mechanism but the iteration count is wrong.

---

#### documentation_inconsistency

**Description:** Incomplete syntax documentation for INPUT statement

**Affected files:**
- `docs/help/common/language/statements/input.md`

**Details:**
input.md syntax shows: 'INPUT[;] ["prompt string"[;|,]]variable[,variable...]' but the remarks section mentions 'A semicolon after the prompt string causes the prompt to be displayed without a question mark' without showing this clearly in the syntax. The syntax should more clearly indicate the difference between semicolon and comma after the prompt string.

---

#### documentation_inconsistency

**Description:** Example contains incorrect comment about variable type

**Affected files:**
- `docs/help/common/language/statements/defint-sng-dbl-str.md`

**Details:**
In defint-sng-dbl-str.md example line 70: 'AMOUNT = 100     ' String variable (starts with A, DEFSTR applies)'. The comment says AMOUNT is a string variable, but the value being assigned (100) is numeric. This would cause a type mismatch error. The example should either assign a string value like 'AMOUNT = "100"' or the comment should indicate this would cause an error.

---

#### documentation_inconsistency

**Description:** Missing LINE INPUT# in alphabetical listing

**Affected files:**
- `docs/help/common/language/statements/index.md`

**Details:**
index.md has 'LINE INPUT#' listed under 'I' section with link to 'inputi.md', but the actual file is named 'inputi.md' which suggests it should be 'INPUT#' (line version). The alphabetical listing shows both 'INPUT#' and 'LINE INPUT#' but they link to different files (input_hash.md and inputi.md respectively), yet the descriptions and purposes overlap.

---

#### documentation_inconsistency

**Description:** Inconsistent spacing guidance in DEF FN documentation

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`

**Details:**
def-fn.md states 'Space after FN is optional. Both styles are valid' and shows examples with and without spaces. However, the 'Syntax Notes' section emphasizes this distinction heavily, while the main syntax section shows: 'DEF FN<name>[(<parameter list>)]=<function definition>' which suggests no space. This could confuse users about which is the canonical form.

---

#### documentation_inconsistency

**Description:** Example output formatting inconsistency

**Affected files:**
- `docs/help/common/language/statements/inputi.md`

**Details:**
The example shows:
Output:
```
CUSTOMER INFORMATION? LINDA JONES  234,4  MEMPHIS
LINDA JONES  234,4  MEMPHIS
Ok
```

The 'Ok' prompt at the end is inconsistent with other documentation examples which don't always show the 'Ok' prompt. Some examples show it, others don't.

---

#### documentation_inconsistency

**Description:** Incomplete Remarks section

**Affected files:**
- `docs/help/common/language/statements/list.md`

**Details:**
The list.md file has a '## Remarks' section that is completely empty:

## Remarks


## Example

This should either contain remarks about the LIST command or be removed if there are no special remarks to make.

---

#### documentation_inconsistency

**Description:** Inconsistent metadata formatting in frontmatter

**Affected files:**
- `docs/help/common/language/statements/print.md`

**Details:**
print.md has 'aliases: ['?']' in its frontmatter, but other command files don't use the aliases field even when they have alternative forms (like LET being optional). This inconsistency in metadata should be standardized.

---

#### documentation_inconsistency

**Description:** Syntax section has inconsistent formatting

**Affected files:**
- `docs/help/common/language/statements/renum.md`

**Details:**
renum.md shows syntax in a unique multi-line format:

syntax: "RENUM
RENUM <new_start>
RENUM <new_start>,<old_start>
RENUM <new_start>,<old_start>,<increment>"

Other files use single-line syntax or separate the variations in the body. This should follow the same pattern as other commands with multiple forms.

---

#### documentation_inconsistency

**Description:** LIMITS command marked as MBASIC Extension but unclear if implemented

**Affected files:**
- `docs/help/common/language/statements/limits.md`

**Details:**
limits.md states:
'**Versions:** MBASIC Extension'
'This is a modern extension not present in original MBASIC 5.21'

But unlike LLIST, LPRINT, OUT, and POKE, there's no 'Implementation Note' section indicating whether this is actually implemented or not. The documentation should clarify the implementation status.

---

#### documentation_inconsistency

**Description:** Related field uses function names instead of statement paths

**Affected files:**
- `docs/help/common/language/statements/mid-assignment.md`

**Details:**
mid-assignment.md has:
related: ['mid_dollar', 'left_dollar', 'right_dollar']

But the See Also section properly links to functions:
- [MID$](../functions/mid_dollar.md)

The 'related' field should use consistent paths like '../functions/mid_dollar' or be removed if not used by the documentation system.

---

#### documentation_inconsistency

**Description:** Inconsistent MERGE command documentation

**Affected files:**
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/tk/index.md`

**Details:**
CLI docs mention 'MERGE "addon.bas"' command in the File Operations section, but Tk docs do not mention MERGE at all in the File Menu or anywhere else. This suggests either:
1. MERGE is CLI-only
2. MERGE is available in Tk but undocumented
3. The feature availability differs between UIs

---

#### documentation_inconsistency

**Description:** Ambiguous 'Immediate Mode Panel' documentation

**Affected files:**
- `docs/help/common/ui/tk/index.md`

**Details:**
Tk docs state 'Some Tk configurations include an immediate mode panel' but don't specify:
1. Which configurations include it
2. How to enable/disable it
3. Whether it's a compile-time or runtime option
This creates uncertainty about feature availability.

---

#### documentation_inconsistency

**Description:** Incomplete DELETE command documentation

**Affected files:**
- `docs/help/common/ui/curses/editing.md`

**Details:**
Curses editing docs show 'DELETE 20' and 'DELETE 10-30' examples and reference '[DELETE Command](../../language/statements/delete.md)', but don't explain the range syntax (10-30) or other DELETE options. The reference suggests more complete docs exist elsewhere.

---

#### documentation_inconsistency

**Description:** Inconsistent WIDTH statement documentation

**Affected files:**
- `docs/help/mbasic/compatibility.md`

**Details:**
Compatibility.md states 'WIDTH is parsed for compatibility but performs no operation' and 'The "WIDTH LPRINT" syntax is not supported'. However, it doesn't clarify if 'WIDTH 80' is accepted silently (no-op) or if it produces an error. The phrasing 'Accepted (no-op)' suggests silent acceptance, but this should be explicit.

---

#### documentation_inconsistency

**Description:** Inconsistent description of LPRINT behavior

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/index.md`

**Details:**
features.md states: 'LPRINT - Line printer output (Note: Statement is parsed but produces no output - see [LPRINT](../common/language/statements/lprint-lprint-using.md) for details)'
This suggests LPRINT is parsed but non-functional.
However, cli/index.md does not mention this limitation in its command list, and no other documentation clarifies whether LPRINT actually works or not in different UIs.

---

#### documentation_inconsistency

**Description:** Incomplete debugging feature documentation cross-reference

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/debugging.md`

**Details:**
features.md states: 'See UI-specific documentation for details: [CLI Debugging](../ui/cli/debugging.md), [Curses UI](../ui/curses/feature-reference.md), [Tk UI](../ui/tk/feature-reference.md)'
However, it does not mention Web UI debugging documentation, despite Web UI being listed as a supported interface elsewhere.
This could indicate either missing Web UI debugging docs or that Web UI has limited debugging features that should be documented.

---

#### documentation_inconsistency

**Description:** Missing Find/Replace feature documentation for Web UI

**Affected files:**
- `docs/help/ui/cli/find-replace.md`
- `docs/help/mbasic/features.md`

**Details:**
find-replace.md states: 'For built-in Find/Replace, use the Tk UI' and provides instructions for Tk UI only.
features.md mentions Web UI has 'Syntax highlighting' and 'Three-panel layout' but doesn't mention Find/Replace capabilities.
Given that Web UI is described as a 'Browser-based IDE' with modern features, it's unclear whether Find/Replace is available in Web UI or not.

---

#### documentation_inconsistency

**Description:** Settings commands not mentioned in features list

**Affected files:**
- `docs/help/ui/cli/settings.md`
- `docs/help/mbasic/features.md`

**Details:**
settings.md documents SHOWSETTINGS and SETSETTING commands as available in CLI mode.
features.md has a 'Direct Commands' section listing: RUN, LIST, NEW, SAVE, LOAD, DELETE, RENUM, AUTO
SHOWSETTINGS and SETSETTING are not listed in this section, despite being direct commands available to users.
This omission could cause users to be unaware of these configuration capabilities.

---

#### documentation_inconsistency

**Description:** Inconsistent statement count

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/index.md`

**Details:**
cli/index.md states: 'Statements - All 63 statements'
features.md does not provide a specific count of statements, only listing categories of statements.
This makes it difficult to verify completeness or understand the scope of implementation.

---

#### documentation_inconsistency

**Description:** Inconsistent error code count

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/index.md`

**Details:**
cli/index.md states: 'Error Codes - All 68 error codes'
features.md mentions 'MBASIC error codes and messages' under Compatibility but doesn't specify how many error codes are implemented.
This inconsistency makes it unclear whether all 68 MBASIC 5.21 error codes are truly supported.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut documentation for Variables Window

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
docs/help/ui/curses/feature-reference.md states: '### Variables Window (Menu only)
Open/close the variables inspection window showing all program variables and their current values.
**Note:** Access via menu only - no keyboard shortcut assigned.'

docs/help/ui/curses/quick-reference.md lists under 'Global Commands': '| **Menu only** | Toggle variables window |'

And under 'Debugger (when program running)': '| **Menu only** | Show/hide variables window |'

However, docs/help/ui/curses/variables.md states: '### Keyboard Shortcut
Press `{{kbd:toggle_variables:curses}}` to open the variables window.'

This is contradictory - feature-reference and quick-reference say 'Menu only' while variables.md documents a keyboard shortcut.

---

#### documentation_inconsistency

**Description:** Missing Settings keyboard shortcut in quick reference

**Affected files:**
- `docs/help/ui/curses/quick-reference.md`
- `docs/help/ui/curses/settings.md`

**Details:**
docs/help/ui/curses/settings.md documents: '**Keyboard shortcut:** `Ctrl+,`'

docs/help/ui/curses/quick-reference.md lists under 'Global Commands': '| **Menu only** | Settings |'

If Ctrl+, is the actual shortcut (as documented in settings.md), then quick-reference.md should list it instead of 'Menu only'.

---

#### documentation_inconsistency

**Description:** Inconsistent documentation of delete line shortcut

**Affected files:**
- `docs/help/ui/curses/editing.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
docs/help/ui/curses/editing.md states: '### Quick Delete (^D)
1. Navigate to the line
2. Press **^D**
3. Line is deleted immediately'

docs/help/ui/curses/feature-reference.md states: '### Delete Lines ({{kbd:delete:curses}})
Delete the current line in the editor.'

The editing.md uses '^D' notation while feature-reference.md uses '{{kbd:delete:curses}}' template notation. These should be consistent, and it's unclear if they refer to the same key.

---

#### documentation_inconsistency

**Description:** Placeholder documentation vs actual documentation

**Affected files:**
- `docs/help/ui/common/running.md`
- `docs/help/ui/curses/running.md`

**Details:**
docs/help/ui/common/running.md states: '**Status:** PLACEHOLDER - Documentation in progress

This page will cover:
- How to run BASIC programs
- RUN command
- Program execution
- Stopping programs
- Continuing after STOP'

docs/help/ui/curses/running.md provides complete documentation for running programs in the Curses UI.

The common/running.md placeholder suggests this should be common documentation, but the actual implementation is UI-specific. This may indicate the documentation structure needs review.

---

#### documentation_inconsistency

**Description:** Inconsistent Renumber keyboard shortcut documentation

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
docs/help/ui/curses/feature-reference.md states: '### Renumber ({{kbd:renumber:curses}})
Renumber all program lines with consistent increments. Opens a dialog to specify start line and increment.'

docs/help/ui/curses/quick-reference.md states: '| **Menu only** | Renumber all lines (RENUM) |'

One says there's a keyboard shortcut ({{kbd:renumber:curses}}), the other says 'Menu only'.

---

#### documentation_inconsistency

**Description:** Inconsistent keyboard shortcut template usage

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/features.md`

**Details:**
feature-reference.md consistently uses {{kbd:*:tk}} format (e.g., {{kbd:file_new:tk}}, {{kbd:file_open:tk}})

But features.md uses {{kbd:*}} format without :tk suffix (e.g., {{kbd:smart_insert}}, {{kbd:toggle_breakpoint}})

This inconsistency may indicate different template systems or missing parameters.

---

#### documentation_inconsistency

**Description:** Inconsistent feature count in section headers

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
feature-reference.md shows:
- 'File Operations (8 features)'
- 'Execution & Control (6 features)'
- 'Debugging (6 features)'
- 'Variable Inspection (6 features)'
- 'Editor Features (7 features)'
- 'Help System (4 features)'

Total claimed: 37 features

But the document title states 'Complete Feature Reference' without specifying total count. If this is meant to be comprehensive, the total should be stated clearly.

---

#### documentation_inconsistency

**Description:** Missing 'Open Example' feature mentioned in one doc but contradicted in another

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
web-interface.md under 'File Menu' states: 'Note: An "Open Example" feature to choose from sample BASIC programs is planned for a future release.'

However, features.md under 'File Operations > Open Files (Planned)' lists 'Recent files list' as planned, but getting-started.md under 'Recent Files' states it's currently implemented: 'File → Recent Files shows recently opened files (saved in localStorage, persists across browser sessions)'.

The inconsistency is about what file-related features are implemented vs planned.

---

#### documentation_inconsistency

**Description:** Variable Inspector implementation status unclear

**Affected files:**
- `docs/help/ui/web/features.md`
- `docs/help/ui/web/web-interface.md`

**Details:**
features.md under 'Variable Inspector > Currently Implemented' states: 'Basic variable viewing via Debug menu'.

However, web-interface.md under 'Run Menu' lists: 'Show Variables - Open the Variables Window to view and monitor program variables in real-time' under the 'View Menu' (not Debug menu).

The inconsistency: features.md says 'Debug menu' but web-interface.md says 'View Menu'. Also, features.md says 'Basic variable viewing' while web-interface.md describes it as 'view and monitor program variables in real-time' which sounds more advanced.

---

#### documentation_inconsistency

**Description:** Library index pages have inconsistent metadata and missing information

**Affected files:**
- `docs/library/business/index.md`
- `docs/library/data_management/index.md`
- `docs/library/demos/index.md`
- `docs/library/education/index.md`
- `docs/library/electronics/index.md`

**Details:**
All library index pages (business, data_management, demos, education, electronics) show programs with empty metadata:
- 'Year: 1980s' (vague)
- 'Tags:' (empty for most, except some demos/education with 'test' tag)
- No descriptions
- No author information
- No difficulty level
- No prerequisites

The pages claim 'These programs are from the CP/M and early PC era (1970s-1980s), preserved from historical archives including OAK, Simtel, and CP/M CD-ROMs' but provide no specific provenance for individual programs.

This makes it difficult for users to choose appropriate programs or understand what they do before downloading.

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

**Description:** Inconsistent section headers in 'How to Use' sections

**Affected files:**
- `docs/library/games/index.md`
- `docs/library/ham_radio/index.md`
- `docs/library/telecommunications/index.md`
- `docs/library/utilities/index.md`

**Details:**
Most library pages use 'How to Use' as the section header, but the content is identical. However, ham_radio/index.md has:
## How to Use
...
## About These Ham Radio

While others have:
## How to Use
...
## About These [Category]

The ham_radio page is missing the category name 'Programs' in the 'About' section header.

---

#### documentation_inconsistency

**Description:** Curses UI limitations list includes 'No Find/Replace' but doesn't clarify if this is a current limitation or permanent

**Affected files:**
- `docs/user/CHOOSING_YOUR_UI.md`

**Details:**
Under Curses limitations:
**Limitations:**
- Limited mouse support
- Partial variable editing
- No clipboard integration
- Terminal color limits
- No Find/Replace

The document doesn't clarify whether 'No Find/Replace' is a technical limitation of terminal UIs or simply not yet implemented. Other UIs show which features are fundamental limitations vs. missing features.

---

#### documentation_inconsistency

**Description:** Example code formatting inconsistency in case handling examples

**Affected files:**
- `docs/user/CASE_HANDLING_GUIDE.md`

**Details:**
Throughout the document, example BASIC code is shown with inconsistent formatting. Some examples show:
```basic
10 TargetAngle = 45
```

While others show:
```basic
You type:    10 PRINT "hello"
MBASIC shows: 10 print "hello"
```

The second format with 'You type' and 'MBASIC shows' is clearer for demonstrating case handling behavior, but it's not used consistently throughout the document.

---

#### documentation_inconsistency

**Description:** Inconsistent program descriptions - some have detailed descriptions, others are minimal or missing

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

The quality and completeness of descriptions varies significantly. Some programs have clear descriptions, authors, and tags, while others have cryptic descriptions or empty tags.

---

#### documentation_inconsistency

**Description:** Most game entries have empty descriptions and tags

**Affected files:**
- `docs/library/games/index.md`

**Details:**
The vast majority of game entries follow this pattern:

### 23Matches


**Year:** 1980s
**Tags:** 

**[Download 23matches.bas](23matches.bas)**

With no description text and empty tags. Only a few entries like Calendar have actual descriptions. This inconsistency makes the library less useful for users trying to understand what each game does.

---

#### documentation_inconsistency

**Description:** Different UI focus in installation vs quick reference documents

**Affected files:**
- `docs/user/INSTALL.md`
- `docs/user/QUICK_REFERENCE.md`

**Details:**
INSTALL.md mentions multiple UIs (CLI, Curses, Tk, Web) and states 'CLI mode uses only Python's standard library and requires no external dependencies', but QUICK_REFERENCE.md is specifically titled 'MBASIC Curses IDE - Quick Reference Card' and only covers Curses UI. The relationship between these documents and which UI each applies to could be clearer.

---

#### documentation_inconsistency

**Description:** Settings system status inconsistency

**Affected files:**
- `docs/user/INSTALL.md`
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
INSTALL.md states under 'What Works': '✓ Settings system (SET, SHOW SETTINGS commands with global/project configuration files)' implying full implementation. SETTINGS_AND_CONFIGURATION.md has a status note at the top: 'Status: The settings system is implemented and available in all UIs. Core commands (SET, SHOW SETTINGS, HELP SET) work as documented.' However, multiple individual settings are marked as '🔧 PLANNED - Not yet implemented' (interpreter.strict_mode, interpreter.debug_mode, ui.theme, ui.font_size). This creates confusion about what 'implemented' means.

---

#### documentation_inconsistency

**Description:** Inconsistent terminology for execution control buttons

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
The document uses both 'toolbar buttons' and 'toolbar button' inconsistently. In 'Essential Keyboard Shortcuts' table: 'Step, Continue, and Stop are available via toolbar buttons'. In 'Mid-Line Statement Stepping' section: 'Click the **Stmt** toolbar button' and 'Click the **Step** toolbar button'. The terminology should be consistent.

---

#### documentation_inconsistency

**Description:** Inconsistent Python command examples between platforms

**Affected files:**
- `docs/user/INSTALL.md`

**Details:**
INSTALL.md uses 'python3' for Linux/Mac and 'python' for Windows in most places, but in the 'Troubleshooting' section under '"python3: command not found"', it suggests using 'python' as an alternative on systems where python3 isn't available. This could be clearer about when to use which command.

---

#### documentation_inconsistency

**Description:** Inconsistent capitalization of 'Tk' vs 'TK' in document title and content

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
Document title uses 'MBASIC Tk UI' but filename is 'TK_UI_QUICK_START.md' (all caps). Throughout the document, 'Tk UI' is used in prose. This inconsistency in capitalization could be standardized.

---

#### documentation_inconsistency

**Description:** Inconsistent reference to help documentation location

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
Under 'Next Steps', the document says 'See [Language Reference](../help/common/language/index.md)' and other references to '../help/common/' paths. However, these paths are relative to docs/user/ directory. The actual location of these help files is not confirmed in the provided documentation.

---

#### documentation_inconsistency

**Description:** Different example program paths referenced

**Affected files:**
- `docs/user/INSTALL.md`
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
INSTALL.md uses paths like 'basic/bas_tests1/hello.bas' and 'basic/tests_with_results/test_operator_precedence.bas'. TK_UI_QUICK_START.md uses paths like 'basic/hello.bas', 'basic/loops.bas', 'basic/arrays.bas'. It's unclear if these are different directory structures or if the paths are inconsistent.

---

#### documentation_inconsistency

**Description:** Missing keyboard shortcuts in comparison table that are documented in keyboard-shortcuts.md

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`
- `docs/user/keyboard-shortcuts.md`

**Details:**
keyboard-shortcuts.md documents these Curses shortcuts not in UI_FEATURE_COMPARISON.md:
- Ctrl+G (Go to line)
- Ctrl+P (Parse program)
- Ctrl+K (Step Line)
- Ctrl+X (Stop program execution - different from Esc mentioned in comparison)
The comparison table shows 'Esc' for Stop in Curses, but keyboard-shortcuts.md shows 'Ctrl+X'.

---

#### documentation_inconsistency

**Description:** Inconsistent status indicators for Auto-save feature

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
In 'File Operations' table, Auto-save shows:
- Tk: '⚠️' with note 'Tk: planned/optional, Web: automatic'
This is confusing because '⚠️' means 'Partially implemented' per the legend, but 'planned' suggests not implemented. Should either be '📋' (Planned) or clarify what part is implemented vs planned.

---

#### documentation_inconsistency

**Description:** Ambiguous Recent files status for Web UI

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
Recent files for Web UI is marked '⚠️' with note 'Tk: menu, Web: localStorage'. The warning symbol suggests partial implementation, but the note doesn't clarify what's missing or incomplete about the Web implementation compared to full implementation.

---

#### documentation_inconsistency

**Description:** Missing explanation for CLI keyboard shortcut limitations

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
In 'User Interface' table, CLI shows 'Keyboard shortcuts' as '⚠️' with note 'CLI: limited', but there's no explanation of which shortcuts are available vs missing. The 'Detailed UI Descriptions' section mentions 'Limited UI features' but doesn't specify the keyboard shortcut limitations.

---

#### documentation_inconsistency

**Description:** Inconsistent feature status representation in legend vs usage

**Affected files:**
- `docs/user/UI_FEATURE_COMPARISON.md`

**Details:**
The legend defines ⚠️ as 'Partially implemented (see Notes column for details)', but some uses of ⚠️ in the tables reference 'planned' features (e.g., 'Tk: planned/optional'), which contradicts the 'implemented' part of the definition. 'Planned' features should use 📋 per the legend.

---


## Summary

- Total issues found: 672
- Code/Comment conflicts: 226
- Other inconsistencies: 446
