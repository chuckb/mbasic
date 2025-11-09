# Enhanced Consistency Report (Code + Documentation)

Generated: 2025-11-09 13:49:51
Analyzed: Source code (.py, .json) and Documentation (.md)

**Note:** This report has been filtered to remove 2 previously reviewed/ignored issues. Original report had 434 total issues.

### Other Issues

#### code_vs_comment


**Description:** CONT command docstring claims editing clears execution state, but clear_execution_state() doesn't clear stopped flag

**Affected files:**
- `src/interactive.py`

**Details:**
The cmd_cont() docstring at line ~280 states:
'IMPORTANT: CONT will fail with "?Can't continue" if the program has been edited (lines added, deleted, or renumbered) because editing clears the GOSUB/RETURN and FOR/NEXT stacks to prevent crashes from invalidated return addresses and loop contexts. See clear_execution_state() for details.'

However, clear_execution_state() at line ~100 does:
if self.program_runtime:
    self.program_runtime.gosub_stack.clear()
    self.program_runtime.for_loops.clear()
    self.program_runtime.stopped = False

The stopped flag is cleared, which means CONT would NOT fail after editing - it would succeed but with cleared stacks. The docstring claims CONT will fail, but the code allows it to continue (just with invalid state). This is a significant inconsistency about critical behavior.

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


**Description:** serialize_let_statement docstring claims it 'ALWAYS outputs the implicit assignment form (A=5) without the LET keyword' but this contradicts the function name and the LetStatementNode's purpose. The comment suggests the AST doesn't track whether LET was present, but this is a design decision that may not match user expectations.

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring states:
'LetStatementNode represents both explicit LET statements and implicit assignments in the AST. However, this serializer ALWAYS outputs the implicit assignment form (A=5) without the LET keyword, regardless of whether the original source used LET.

This is because:
- The AST doesn\'t track whether LET was originally present
- LET is optional in MBASIC and functionally equivalent to implicit assignment
- Both forms use the same AST node type for consistency throughout the codebase'

This means source code with 'LET A=5' will be serialized as 'A=5', losing the original syntax. This is a significant behavior that should be verified as intentional.

---

#### code_vs_comment


**Description:** emit_keyword docstring requires lowercase input but apply_keyword_case_policy docstring says it accepts any case. These two functions have conflicting requirements.

**Affected files:**
- `src/position_serializer.py`

**Details:**
emit_keyword docstring:
'Args:
    keyword: The keyword to emit (must be normalized lowercase by caller, e.g., "print", "for")'

And:
'Note: This function requires lowercase input because it looks up the display case from the keyword case manager using the normalized form.'

But apply_keyword_case_policy docstring:
'Args:
    keyword: The keyword to transform (may be any case)'

If emit_keyword calls apply_keyword_case_policy (or vice versa), there's a contract mismatch.

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

This is a design smell - having two fields with overlapping purposes that are only separated by convention (not type system) is error-prone. The comment acknowledges this but doesn't explain why this design was chosen over alternatives like:
1. A union type
2. Separate Token subclasses
3. A single original_case field with token type determining interpretation

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


**Description:** Settings widget keybindings don't match curses_keybindings.json

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
curses_settings_widget.py implements these keybindings in keypress():
- ESC_KEY or SETTINGS_KEY: Cancel
- ENTER_KEY: OK
- SETTINGS_APPLY_KEY: Apply
- SETTINGS_RESET_KEY: Reset

But curses_keybindings.json does NOT define SETTINGS_KEY, SETTINGS_APPLY_KEY, or SETTINGS_RESET_KEY. It only has general editor commands. The settings widget has its own keybindings that are not documented in the keybindings JSON file.

---

#### internal_inconsistency


**Description:** Inconsistent handling of line number width constraints across methods

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple methods reference different maximum line numbers:

1. keypress() method uses 99999 as max:
   if next_num >= 99999 or attempts > 10:

2. _parse_line_numbers() uses 999999 as fallback:
   parsed_lines.append((999999 + idx, line))

3. Class docstring mentions '1-5 digits' (max 99999)

4. No explicit validation of line number range in add_line() or set_program_text()

This creates inconsistent behavior where some code paths allow 6-digit line numbers while others don't.

---

#### code_vs_comment


**Description:** Status bar update comment contradicts actual implementation in multiple debug methods

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Multiple methods have comments like:
# (No status bar update - execution will show output in output window)
# (No status bar update - output will show in output window)

But the code DOES update the status bar in these same methods:
- _debug_step() line ~665: self.status_bar.set_text(f"Paused at {pc_display}...")
- _debug_step_line() line ~745: self.status_bar.set_text(f"Paused at {pc_display}...")

The comments claim no status bar updates happen, but the code clearly updates the status bar with pause information.

---

#### code_vs_comment


**Description:** Comment in _sync_program_to_runtime claims PC is reset to halted when paused_at_breakpoint=True to prevent accidental resumption, but this contradicts the actual breakpoint continuation mechanism

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Lines ~1195-1200:
Comment: '# Restore PC only if execution is running AND not paused at breakpoint
# When paused_at_breakpoint=True, we reset PC to halted to prevent accidental
# resumption. When the user continues from a breakpoint (via _debug_continue),
# the interpreter's state already has the correct PC and simply clears the halted flag.'

This comment describes resetting PC to halted when paused at breakpoint, but if PC is halted, how can _debug_continue resume from the correct location? The comment claims 'interpreter's state already has the correct PC' but if runtime.pc is halted, that information would be lost.

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


**Description:** Variables window heading text doesn't match initial sort state

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Code in _create_variables_window (lines 1088-1091):
# Set initial heading text with down arrow (matches self.variables_sort_column='accessed', descending)
tree.heading('#0', text='↓ Variable (Last Accessed)')
tree.heading('Value', text='  Value')
tree.heading('Type', text='  Type')

Initialization in __init__ (lines 109-110):
self.variables_sort_column = 'accessed'  # Current sort column (default: 'accessed' for last-accessed timestamp)
self.variables_sort_reverse = True  # Sort direction: False=ascending, True=descending (default descending for timestamps)

The comment says 'down arrow (matches ... descending)' but down arrow (↓) typically indicates descending sort, which matches variables_sort_reverse=True. However, the heading text says 'Last Accessed' which implies sorting by access time, but the actual behavior depends on the sort_variables function which is imported but not shown. Need to verify if 'accessed' mode actually sorts by last-accessed timestamp.

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


**Description:** _delete_line() docstring describes line_num parameter incorrectly - claims it uses 'dual numbering' but the method only uses Tkinter editor line numbers, not BASIC line numbers

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Docstring says:
"Args:
    line_num: Tkinter text widget line number (1-based sequential index),
             not BASIC line number (e.g., 10, 20, 30).
             Note: This class uses dual numbering - editor line numbers for
             text widget operations, BASIC line numbers for line_metadata lookups."

But the code implementation:
line_text = self.text.get(f'{line_num}.0', f'{line_num}.end')
if line_text.strip() == '':
    self.text.delete(f'{line_num}.0', f'{line_num + 1}.0')

The method ONLY uses editor line numbers (line_num parameter). It never looks up or uses BASIC line numbers. The 'dual numbering' note is misleading in this context since this specific method doesn't interact with line_metadata at all.

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


**Description:** Help system documentation contradicts implementation - README says web UI help may be served externally, but web_help_launcher.py shows help is served at http://localhost/mbasic_docs

**Affected files:**
- `docs/help/README.md`
- `src/ui/web_help_launcher.py`

**Details:**
README.md states: 'Web UI help may be served externally rather than through the built-in help system.'

But web_help_launcher.py shows:
HELP_BASE_URL = "http://localhost/mbasic_docs"

The code clearly expects help to be served at a specific local URL, not 'externally'. The documentation should clarify that web help is served locally at /mbasic_docs, not externally.

---

#### documentation_inconsistency


**Description:** Misleading example comment about FIX usage with array indexing

**Affected files:**
- `docs/help/common/language/functions/fix.md`

**Details:**
The fix.md example states 'Note: FIX is useful for converting floating-point results to array indices, ensuring truncation toward zero rather than rounding down (which INT does for negative numbers).' However, the example uses X = 3.7 and INDEX = FIX(X) which gives 3. The comment says 'Truncate to 3, not 4' but neither FIX nor INT would give 4 for 3.7 - CINT would round to 4. This example doesn't demonstrate the difference between FIX and INT since both would return 3 for positive 3.7. A negative example would better illustrate the difference.

---

#### documentation_inconsistency


**Description:** LINE INPUT# documentation has incorrect filename and title

**Affected files:**
- `docs/help/common/language/statements/inputi.md`
- `docs/help/common/language/statements/line-input.md`

**Details:**
File inputi.md has:
- title: "LINE INPUT# (File)"
- syntax: LINE INPUT#<file number>,<string variable>

But the filename is 'inputi.md' which suggests INPUT# not LINE INPUT#. The 'See Also' section in line-input.md references it as 'inputi.md' for LINE INPUT#, but inputi.md should be for INPUT# based on naming convention. The content describes LINE INPUT# but the filename doesn't match.

---

#### documentation_inconsistency


**Description:** Variable name significance documentation contradicts itself about 2-character vs full-name significance

**Affected files:**
- `docs/help/common/language/variables.md`
- `docs/help/common/settings.md`

**Details:**
variables.md states: 'Note on Variable Name Significance: In the original MBASIC 5.21, only the first 2 characters of variable names were significant (AB, ABC, and ABCDEF would be the same variable). This Python implementation uses the full variable name for identification, allowing distinct variables like COUNT and COUNTER.'

However, settings.md describes variables.case_conflict setting which implies full variable names ARE used for comparison: 'BASIC is case-insensitive by default (Count = COUNT = count are the same variable)'

If full names are used, then COUNT and COUNTER would be different variables, which contradicts the 2-character limitation mentioned.

---

#### documentation_inconsistency


**Description:** Variables.md contradicts itself about variable name significance

**Affected files:**
- `docs/help/common/language/variables.md`

**Details:**
The document states: 'Note on Variable Name Significance: In the original MBASIC 5.21, only the first 2 characters of variable names were significant (AB, ABC, and ABCDEF would be the same variable). This Python implementation uses the full variable name for identification, allowing distinct variables like COUNT and COUNTER.'

But then later states: 'Case Sensitivity: Variable names are not case-sensitive by default (Count = COUNT = count)'

If full names are used, the example 'COUNT and COUNTER' being distinct is correct. But the case sensitivity note implies the full name matters for case comparison, which is consistent with full-name significance. The documentation should clarify that this implementation DOES use full names (not just 2 chars) and that case-insensitivity applies to the full name.

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


**Description:** Contradictory information about WIDTH statement

**Affected files:**
- `docs/help/mbasic/compatibility.md`

**Details:**
Compatibility.md states 'WIDTH is parsed for compatibility but performs no operation' and 'The "WIDTH LPRINT" syntax is not supported'. However, it's unclear if WIDTH with no arguments or WIDTH with numeric argument are both no-ops, or if only certain forms are accepted. The statement is ambiguous.

---

#### documentation_inconsistency


**Description:** Find/Replace feature availability contradiction

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/find-replace.md`

**Details:**
features.md under 'Tkinter GUI' section states: 'Find and Replace - Search and replace text ({{kbd:find:tk}}/{{kbd:replace:tk}})'

cli/find-replace.md states: 'The CLI backend does not have built-in Find/Replace commands' and recommends: 'For built-in Find/Replace, use the Tk UI'

This is consistent for CLI not having it and Tk having it. However, features.md doesn't mention whether Curses UI or Web UI have Find/Replace, creating an incomplete picture.

---

#### documentation_inconsistency


**Description:** String memory management implementation unclear

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/implementation/string-allocation-and-garbage-collection.md`

**Details:**
features.md states under 'Compiler Features': 'These optimizations improve execution speed while maintaining 100% MBASIC compatibility.'

string-allocation-and-garbage-collection.md provides extensive detail about CP/M MBASIC's O(n²) garbage collection algorithm and states: 'Understanding this system is crucial for: Accurate emulation of period systems... Implementing compatible interpreters for modern systems'

It's unclear whether this Python implementation actually uses the O(n²) algorithm for compatibility or uses Python's native garbage collection. features.md mentions 'Python memory management vs. CP/M' under 'Intentional Differences' but doesn't clarify the string GC approach.

This is critical for understanding performance characteristics and true compatibility claims.

---

#### documentation_inconsistency


**Description:** Contradictory information about variable inspection methods between Curses and CLI UIs

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/cli/variables.md`

**Details:**
docs/help/ui/curses/variables.md states: 'The Curses UI provides a visual variable inspector window for viewing and managing variables during program execution and debugging.' with keyboard shortcut {{kbd:toggle_variables:curses}}.

However, docs/help/ui/cli/variables.md states: 'The CLI uses the PRINT statement for variable inspection during debugging' and explicitly says 'The CLI does not have a Variables Window feature.'

But then docs/help/ui/cli/variables.md also says: 'For visual variable inspection, use: - **Curses UI** - Full-screen terminal with Variables Window ({{kbd:toggle_variables:curses}})'

This creates confusion about whether the Variables Window is a Curses-only feature or available in CLI mode.

---

#### documentation_inconsistency


**Description:** Contradictory information about variable editing capability

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
docs/help/ui/curses/variables.md states: '### Direct Editing Not Available
⚠️ **Not Implemented**: You cannot edit variable values directly in the variables window.'

But docs/help/ui/curses/feature-reference.md states: '### Edit Variable Value (Not implemented)
⚠️ Variable editing is not available in Curses UI. You cannot directly edit values in the variables window. Use immediate mode commands to modify variable values instead.'

Both agree it's not implemented, which is consistent. However, the comparison table in variables.md shows:
'| Feature | Curses | CLI | Tk | Web |
| Edit values | ❌ | ❌ | ✅ | ✅ |'

This suggests Tk and Web UIs CAN edit values, but there's no documentation confirming this feature exists in those UIs.

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

This appears to be a typo - should likely be '{{kbd:file_save:tk}}+Shift+B' or 'Shift+B' alone. The 'hift' fragment suggests a copy-paste error where 'S' was replaced with the kbd macro.

---

#### documentation_inconsistency


**Description:** Stop/Interrupt shortcut conflicts with Cut operation

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
feature-reference.md states:
'Stop/Interrupt ({{kbd:cut:tk}}): Stop a running program immediately.'

But also states:
'Cut/Copy/Paste ({{kbd:cut:tk}}/C/V): Standard clipboard operations'

The same shortcut {{kbd:cut:tk}} is assigned to both Stop Program and Cut text. This is a serious conflict.

---

#### documentation_inconsistency


**Description:** Contradictory information about function key shortcuts

**Affected files:**
- `docs/help/ui/web/debugging.md`

**Details:**
debugging.md states:
'**Note:** Function key shortcuts ({{kbd:continue:web}}, {{kbd:step:web}}, {{kbd:help:web}}1, etc.) are not implemented in the Web UI.'

But then in the Keyboard Shortcuts section lists:
'**Currently Implemented:**
- {{kbd:run:web}} - Run program
- {{kbd:continue:web}} - Continue
- {{kbd:step:web}} - Step statement
- {{kbd:step_line:web}} - Step line
- {{kbd:stop:web}} - Stop execution'

And then in **Planned for Future Releases:** lists some of the same shortcuts again:
'- {{kbd:continue:web}} - Start/Continue debugging
- {{kbd:step:web}} - Step over'

This is contradictory - are these shortcuts implemented or not?

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


**Description:** Contradictory compatibility claims about line ending support

**Affected files:**
- `docs/user/sequential-files.md`

**Details:**
The document states 'This MBASIC implementation supports **all three line ending formats**' and shows '✅ Yes' for CRLF, LF, and CR support. However, under 'Comparison with CP/M MBASIC 5.21', it states:
'MBASIC 5.21 line ending compatibility | ⚠️ More permissive (MBASIC only accepts CRLF)'
This creates confusion: if the implementation is 'more permissive' than MBASIC 5.21, it's technically incompatible (accepts files MBASIC 5.21 would reject), yet the summary table shows compatibility as a warning rather than explaining this is an intentional enhancement.

---

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


**Description:** Inconsistent documentation of type_suffix and explicit_type_suffix relationship in VariableNode

**Affected files:**
- `src/ast_nodes.py`

**Details:**
VariableNode lines 893-906:
'Type suffix handling:
- type_suffix: The actual suffix character ($, %, !, #) when present
- explicit_type_suffix: Boolean indicating the origin of type_suffix:
    * True: suffix appeared in source code (e.g., "X%" in "X% = 5")
    * False: suffix inferred from DEFINT/DEFSNG/DEFDBL/DEFSTR (e.g., "X" with DEFINT A-Z)

Example: In "DEFINT A-Z: X=5", variable X has type_suffix=\'%\' and explicit_type_suffix=False.
The suffix must be tracked for type checking but not regenerated in source code.
Both fields must always be examined together to correctly handle variable typing.'

The comment says 'when present' for type_suffix but then shows an example where type_suffix='%' even when explicit_type_suffix=False (inferred). This is confusing - it's unclear if type_suffix can be None when explicit_type_suffix=False, or if it's always populated.

---

#### code_vs_comment_conflict


**Description:** Comment claims trailing_minus_only adds 1 char total, but code adds 1 char to content_width regardless of sign value

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line 232 comment: 'trailing_minus_only: - at end, adds - for negative OR space for non-negative (1 char total)'
Line 327-328 code: 'if spec['leading_sign'] or spec['trailing_sign'] or spec['trailing_minus_only']:
    content_width += 1'
The comment says trailing_minus_only adds 1 char total (implying it's conditional), but the code unconditionally adds 1 to content_width for trailing_minus_only, same as trailing_sign. The behavior is actually correct (always reserves space), but the comment's phrasing '(1 char total)' vs '(2 chars total)' for trailing_sign is misleading.

---

#### code_vs_comment_conflict


**Description:** EOF function comment describes mode 'I' as binary input but doesn't clarify relationship to OPEN statement syntax

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line 717-723 comment: 'Note: For binary input files (mode 'I' from OPEN statement), respects ^Z (ASCII 26)
as EOF marker (CP/M style). In MBASIC syntax, mode 'I' stands for "Input" but is
specifically BINARY INPUT mode, implemented as 'rb' by execute_open() in interpreter.py.
This binary mode allows ^Z detection for CP/M compatibility. Text mode files (output,
append) use standard Python EOF detection without ^Z checking.'
Line 738-741 code: 'if file_info['mode'] == 'I':'
The comment explains mode 'I' is binary input opened as 'rb', but the code checks file_info['mode'] == 'I' which suggests the mode is stored as 'I' not 'rb'. This creates confusion about whether 'I' is the BASIC syntax mode or the Python file mode. The comment references execute_open() in interpreter.py but that file is not provided for verification.

---

#### code_vs_comment_conflict


**Description:** Comment claims identifier_table infrastructure exists but is not used, yet get_identifier_table method creates and returns a table

**Affected files:**
- `src/case_string_handler.py`

**Details:**
Line 48-55 comment: 'Identifiers always preserve their original case in display.
Unlike keywords, which can be forced to a specific case policy,
identifiers (variable/function names) retain their case as typed.
This matches MBASIC 5.21 behavior where identifiers are case-insensitive
for matching but preserve display case.
Note: We return original_text directly. An identifier_table infrastructure
exists (see get_identifier_table) but is not currently used for identifiers,
as they always preserve their original case without policy enforcement.'
Line 24-28 code: '@classmethod
def get_identifier_table(cls, policy: str = "force_lower") -> CaseKeeperTable:
    """Get or create the identifier case keeper table."""
    if cls._identifier_table is None:
        cls._identifier_table = CaseKeeperTable(policy=policy)
    return cls._identifier_table'
The comment says the identifier_table infrastructure 'is not currently used', but the get_identifier_table method actively creates and manages a CaseKeeperTable with a policy parameter. This suggests the infrastructure is implemented and ready for use, contradicting the 'not currently used' claim.

---

#### Documentation inconsistency


**Description:** Contradictory information about storage location in SandboxedFileIO

**Affected files:**
- `src/file_io.py`

**Details:**
The docstring states:
"Storage location: Python server memory (NOT browser localStorage)."

But earlier in the same file's module docstring, it says:
"SandboxedFileIO: Python server memory virtual filesystem (Web UI)"

And later:
"Acts as an adapter to backend.sandboxed_fs (SandboxedFileSystemProvider from src/filesystem/sandboxed_fs.py), which provides an in-memory virtual filesystem."

While these are consistent about server memory, the emphasis on "NOT browser localStorage" seems to contradict an unstated assumption that it might be in browser localStorage. This creates confusion about what the alternative was.

---

#### Code vs Documentation inconsistency


**Description:** Documentation claims math library support but implementation may not handle all cases

**Affected files:**
- `src/codegen_backend.py`

**Details:**
In get_compiler_command() docstring:
"# -lm links the math library for floating point support"

And the code includes '-lm' flag. However, the _generate_binary_op() method only handles the POWER operator with pow() function. The comment suggests broader floating point support, but there's no evidence of other math functions (sin, cos, sqrt, etc.) being implemented or documented as supported.

---

#### Code vs Documentation inconsistency


**Description:** ProgramManager.load_from_file() and merge_from_file() use direct file I/O despite FileIO abstraction existing

**Affected files:**
- `src/editing/manager.py`

**Details:**
The manager.py docstring explains:
"FILE I/O ARCHITECTURE:
This manager provides direct Python file I/O methods (load_from_file, save_to_file) for local UIs (CLI, Curses, Tk) to load/save .BAS program files via UI menus/dialogs. This is separate from the two filesystem abstractions..."

But the code in load_from_file() and merge_from_file() uses:
"with open(filename, 'r') as f:"

This direct file access means ProgramManager cannot work with SandboxedFileIO for web UI, contradicting the file_io.py documentation that says FileIO.load_file() provides file content for loading. The architecture has three separate file I/O mechanisms (ProgramManager direct I/O, FileIO abstraction, FileSystemProvider abstraction) when two would suffice.

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
    """Flush write buffers (no-op for in-memory files)..."""
    # StringIO/BytesIO have flush() methods (no-ops) - hasattr check for safety
    if hasattr(self.file_obj, 'flush'):
        self.file_obj.flush()

The comment says flush() is a no-op, but the code actually calls file_obj.flush(). While StringIO/BytesIO.flush() are indeed no-ops, the docstring's claim that "flush() has no effect" is misleading since the code does execute a method call.

---

#### code_vs_comment


**Description:** Comment about numbered line editing says 'UI.program must have add_line() and delete_line() methods (validated, errors if missing)' but validation only checks hasattr, not actual method signatures or functionality

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Comment claims: "This feature requires the following UI integration:
- interpreter.interactive_mode must reference the UI object (checked with hasattr)
- UI.program must have add_line() and delete_line() methods (validated, errors if missing)"

Code implementation:
if not hasattr(ui, 'program') or not ui.program:
    return (False, "Cannot edit program lines: UI program manager not available\n")
if line_content and not hasattr(ui.program, 'add_line'):
    return (False, "Cannot edit program lines: add_line method not available\n")
if not line_content and not hasattr(ui.program, 'delete_line'):
    return (False, "Cannot edit program lines: delete_line method not available\n")

The validation only checks if methods exist (hasattr), not if they have correct signatures or will work properly. The comment's use of 'validated' is stronger than what the code actually does.

---

#### code_vs_comment


**Description:** Comment claims digits are 'silently ignored' in EDIT mode, but code doesn't implement this behavior

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~730 states:
'INTENTIONAL BEHAVIOR: When digits are entered, they are silently ignored (no output, no cursor movement, no error). This preserves MBASIC compatibility where digits are reserved for count prefixes in the full EDIT implementation.'

However, the cmd_edit() implementation has no code to handle digit input (0-9). The while loop at line ~760 only handles specific commands (Space, D, I, X, H, E, Q, L, A, C, CR/LF). Any unhandled character (including digits) would fall through with no action, but this is not explicitly implemented as 'silent ignore' behavior - it's just missing handling.

---

#### code_vs_comment


**Description:** Comment about RENUM ERL handling describes broader behavior than MBASIC manual specifies

**Affected files:**
- `src/interactive.py`

**Details:**
Comment at line ~580 states:
'ERL handling: ERL expressions with ANY binary operators (ERL+100, ERL*2, ERL=100) have all right-hand numbers renumbered, even for arithmetic operations. This is intentionally broader than the MBASIC manual (which only specifies comparison operators) to avoid missing line references.'

The _renum_erl_comparison() docstring at line ~650 repeats this and labels it 'INTENTIONAL DEVIATION FROM MANUAL'.

This is documented as intentional, but creates a potential bug: arithmetic expressions like 'IF ERL+100 THEN...' will incorrectly renumber the 100 if it's an old line number. The comment acknowledges this is 'rare in practice' but it's still a deviation that could cause unexpected behavior.

---

#### code_vs_comment


**Description:** Comment about bare except being acceptable doesn't match Python best practices

**Affected files:**
- `src/interactive.py`

**Details:**
At line ~850 in _read_char(), there's a bare except with this comment:
'# Fallback for non-TTY/piped input or any terminal errors.
# Bare except is acceptable here because we're degrading gracefully to basic read()
# on any error (AttributeError, termios.error, ImportError on Windows, etc.)'

While the comment explains the rationale, bare except catches ALL exceptions including SystemExit and KeyboardInterrupt, which should not be caught. The code should use 'except Exception:' instead to avoid catching system-level exceptions. The comment justifies behavior that is considered a Python anti-pattern.

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
"# Check for strictly greater than (== len is OK)"

This is consistent, so this may not be an inconsistency. However, the verbose explanation in the comment block could be clearer about what 'inclusive' means.

---

#### code_vs_comment


**Description:** InterpreterState docstring describes input_prompt as 'THE CRITICAL STATE' but doesn't explain why it's more critical than error_info

**Affected files:**
- `src/interpreter.py`

**Details:**
Docstring at line 38 says:
"# Input handling (THE CRITICAL STATE - blocks execution)"

But the recommended checking order at lines 31-34 says:
"For UI/callers checking completed state (recommended order):
- error_info: Non-None if an error occurred (highest priority for display)
- input_prompt: Non-None if waiting for input (set during statement execution)
- runtime.halted: True if stopped (paused/done/at breakpoint)"

This suggests error_info has 'highest priority for display', but input_prompt is labeled 'THE CRITICAL STATE'. The distinction between 'critical for blocking' vs 'highest priority for display' could be clearer.

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

The code doesn't handle the case where line_text_map might be out of sync:
- No validation that line_text_map contains all lines in statement_table
- No fallback if a line is missing from line_text_map
- No warning to user if inconsistency is detected

Code just silently skips lines not in line_text_map: 'if line_num in self.runtime.line_text_map:'

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
Module docstring says: "For simpler force-based policies in the lexer, see SimpleKeywordCase (src/simple_keyword_case.py) which only supports force_lower, force_upper, and force_capitalize."

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


**Description:** Comment describes LINE_INPUT tokenization behavior that contradicts actual lexer behavior

**Affected files:**
- `src/parser.py`

**Details:**
In parse_input() method around line 1150:

Comment states: "Note: The lexer tokenizes LINE keyword as LINE_INPUT token both when standalone (LINE INPUT statement) and when used as modifier (INPUT...LINE). The parser distinguishes these cases by context - LINE INPUT is a statement, INPUT...LINE uses LINE as a modifier within the INPUT statement."

However, this comment describes the lexer creating a single LINE_INPUT token in both contexts. The code then checks for TokenType.LINE_INPUT when parsing the LINE modifier within INPUT statement. This suggests the lexer does tokenize LINE as LINE_INPUT in both contexts, but the comment's phrasing "The parser distinguishes these cases by context" is misleading - the lexer has already tokenized it the same way, and the parser just uses it in different statement contexts.

---

#### code_vs_comment


**Description:** Comment about def_type_map behavior contradicts when updates occur

**Affected files:**
- `src/parser.py`

**Details:**
In parse_deftype() method around line 2070:

Comment states: "Note: This method always updates def_type_map during parsing. The type map is shared across all statements (both in interactive mode where statements are parsed one at a time, and in batch mode where the entire program is parsed). The type map affects variable type inference throughout the program. The AST node is created for program serialization/documentation."

This comment claims the method "always updates def_type_map during parsing", but this creates a logical issue: if parsing happens before execution, then DEFINT statements would affect variable types before the program runs, which is incorrect behavior. DEFINT should only take effect when executed. The comment suggests the parser is doing semantic analysis (type inference) during parsing, which violates separation of concerns. Either the comment is wrong about when updates occur, or the code is implementing incorrect BASIC semantics.

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

#### documentation_inconsistency


**Description:** apply_keyword_case_policy function has inconsistent documentation about input requirements. The docstring says 'may be any case' but the Note says 'callers should pass lowercase keywords for consistency'.

**Affected files:**
- `src/position_serializer.py`

**Details:**
Function docstring:
'Args:
    keyword: The keyword to transform (may be any case)'

But the Note says:
'Note: While this function can handle keywords in any case, callers should pass lowercase keywords for consistency (emit_keyword() requires lowercase). The first_wins policy normalizes to lowercase for lookup. Other policies transform based on input case.'

This creates ambiguity about the contract - can callers pass any case or should they normalize first?

---

#### code_vs_comment


**Description:** serialize_rem_statement uses stmt.comment_type but the logic suggests it should be uppercase ('APOSTROPHE', 'REM', 'REMARK') while emit_keyword expects lowercase. There's a case mismatch in the flow.

**Affected files:**
- `src/position_serializer.py`

**Details:**
Code:
'if stmt.comment_type == "APOSTROPHE":
    result = self.emit_token("\'", stmt.column, "RemKeyword")
else:
    # Apply keyword case to REM/REMARK
    result = self.emit_keyword(stmt.comment_type.lower(), stmt.column, "RemKeyword")'

The comparison uses uppercase 'APOSTROPHE' but then calls .lower() for emit_keyword. This suggests comment_type is stored in uppercase, but it's not documented whether this is consistent across the codebase.

---

#### code_vs_comment


**Description:** PositionSerializer.__init__ accepts keyword_case_manager parameter but the docstring describes it as 'KeywordCaseManager instance (from parser) with keyword case table' without explaining what happens if it's None (which is the default).

**Affected files:**
- `src/position_serializer.py`

**Details:**
Code:
'def __init__(self, debug=False, keyword_case_manager=None):
    ...
    # Store reference to keyword case manager from parser
    self.keyword_case_manager = keyword_case_manager'

And in emit_keyword:
'if self.keyword_case_manager:
    keyword_with_case = self.keyword_case_manager.get_display_case(keyword)
else:
    # Fallback if no manager (shouldn\'t happen)
    keyword_with_case = keyword.lower()'

The comment says 'shouldn\'t happen' but None is the default value, suggesting this is expected to happen in some contexts.

---

#### code_vs_comment_conflict


**Description:** Comment in check_array_allocation() claims to account for MBASIC array sizing convention, but the actual array creation is delegated to execute_dim() in interpreter.py. The comment suggests this function handles the convention, but it only uses it for limit checking.

**Affected files:**
- `src/resource_limits.py`

**Details:**
Comment says: 'This calculation accounts for the MBASIC array sizing convention for limit checking. The actual array creation/initialization is done by execute_dim() in interpreter.py.'

The comment is somewhat misleading because it first says 'accounts for' which could imply full handling, then clarifies it's only for limit checking. The code does: total_elements *= (dim_size + 1)  # +1 for 0-based indexing (0 to N)

This is correct for limit checking but the comment could be clearer about the division of responsibility.

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
Lines 257-270 docstring: "Args:
    ...
    token: REQUIRED - Token object for tracking (ValueError raised if None).

           Token object is required but its attributes are optional:
           - token.line: Preferred for tracking, falls back to self.pc.line_num if missing
           - token.position: Preferred for tracking, falls back to None if missing

           This allows robust handling of tokens from various sources (lexer, parser,
           fake tokens) while enforcing that some token object must be provided."

This creates ambiguity: the token object is 'REQUIRED' but can be essentially empty (no line, no position). The fallback to self.pc.line_num means even a completely empty token object would work. This contradicts the strong 'REQUIRED' language and the ValueError threat.

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


**Description:** Module docstring claims SimpleKeywordCase is used by lexer but doesn't explain relationship with KeywordCaseManager

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
Module docstring states:
'This is a simplified keyword case handler used by the lexer (src/lexer.py). It supports only three force-based policies...'

And:
'For advanced policies (first_wins, preserve, error) via CaseKeeperTable, see KeywordCaseManager (src/keyword_case_manager.py) which is used by src/parser.py and src/position_serializer.py.'

However, the docstring doesn't explain:
1. Why two separate systems exist
2. How they interact (if at all)
3. Whether they can conflict
4. Why the lexer can't use KeywordCaseManager

This creates confusion about the architecture.

---

#### code_vs_documentation


**Description:** RedisSettingsBackend.load_project() and save_project() are no-ops but this limitation isn't documented in create_settings_backend()

**Affected files:**
- `src/settings_backend.py`

**Details:**
RedisSettingsBackend has:
def load_project(self) -> Dict[str, Any]:
    """Load project settings (returns empty in Redis mode).
    In Redis mode, all settings are session-scoped, not project-scoped.
    """
    return {}

def save_project(self, settings: Dict[str, Any]) -> None:
    """Save project settings (no-op in Redis mode).
    In Redis mode, all settings are session-scoped, not project-scoped.
    """
    pass

However, create_settings_backend() docstring doesn't mention this limitation:
'Factory function to create appropriate settings backend.'

Users calling create_settings_backend() with Redis won't know that project settings are silently ignored. This should be documented in the factory function.

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

This suggests the implementation may NOT actually do statement-level stepping as claimed in the main docstring and cmd_step() documentation.

---

#### Code vs Documentation inconsistency


**Description:** Ctrl+A keybinding conflict between documentation and readline behavior

**Affected files:**
- `src/ui/cli.py`
- `src/ui/cli_keybindings.json`

**Details:**
cli_keybindings.json documents:
"edit": {"keys": ["Ctrl+A"], "description": "Edit line (last line or Ctrl+A followed by line number)"}

But get_additional_keybindings() function states:
"# Note: Ctrl+A is overridden by MBASIC to trigger edit mode"

And also lists in the returned dict:
"move_end_of_line": {"keys": ["Ctrl+E"], "description": "Move cursor to end of line"}

The comment implies Ctrl+A normally moves to start of line (standard readline/Emacs binding) but MBASIC overrides it. However, there's no documentation of what happens to the 'move to start of line' functionality - is it lost or remapped?

---

#### Code vs Comment conflict


**Description:** Comment about actual value vs display label is inconsistent with implementation

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
In _on_reset() method, comment states:
"# Note: Compares actual value (stored in _actual_value) not display label
# since display labels have 'force_' prefix stripped (see _create_setting_widget)"

But in _create_setting_widget(), the code shows:
"display_label = choice.removeprefix('force_') if hasattr(str, 'removeprefix') else (choice[6:] if choice.startswith('force_') else choice)"

The fallback logic "choice[6:] if choice.startswith('force_') else choice" means if the choice doesn't start with 'force_', the display label IS the actual value (no stripping occurs). So the comment's blanket statement that "display labels have 'force_' prefix stripped" is not always true.

---

#### Code vs Documentation inconsistency


**Description:** CapturingIOHandler is used by 'various UI backends' but only documented in its own file

**Affected files:**
- `src/ui/capturing_io_handler.py`
- `src/ui/base.py`

**Details:**
capturing_io_handler.py docstring: "This module provides a simple IO handler that captures output to a buffer, used by various UI backends for executing commands and capturing their output."

However, base.py (which documents the UIBackend interface) makes no mention of CapturingIOHandler or output buffering. None of the backend implementations (cli.py) reference it. It's unclear which 'various UI backends' actually use this class.

---

#### Documentation inconsistency


**Description:** Ctrl+S unavailable explanation is incomplete

**Affected files:**
- `src/ui/curses_keybindings.json`

**Details:**
save command description: "Save program (Ctrl+S unavailable - terminal flow control)"

This mentions Ctrl+S is unavailable due to terminal flow control (XON/XOFF), but doesn't explain:
1. Whether this affects all terminals or just some
2. Whether users can disable flow control to use Ctrl+S
3. Why Ctrl+V was chosen as the alternative (V for saVe?)

This is important information for users expecting standard Ctrl+S behavior.

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


**Description:** Comment claims bare identifiers are rejected, but code allows them in some cases

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _check_line_syntax() method:
Comment: "Reject bare identifiers (the parser treats them as implicit REMs for
old BASIC compatibility, but in the editor we want to be stricter)"

Code checks:
if (first_token.type == TokenType.IDENTIFIER and
    second_token.type in (TokenType.EOF, TokenType.COLON)):
    return (False, f"Invalid statement: '{first_token.value}' is not a BASIC keyword")

However, this only rejects bare identifiers followed by EOF or COLON. A bare identifier followed by other tokens (like operators or parentheses) would pass this check and potentially be treated as an implicit REM by the parser.

---

#### code_vs_comment


**Description:** Comment about pasted lines starting with digits conflicts with BASIC expression syntax

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _parse_line_numbers() method:
"# In this context, we assume lines starting with digits are numbered program lines (e.g., '10 PRINT').
# Note: While BASIC statements can start with digits (numeric expressions), when pasting
# program code, lines starting with digits are conventionally numbered program lines."

The code treats ANY line starting with a digit as a numbered program line:
if line[0].isdigit():
    # Raw pasted line like '10 PRINT' - reformat it

This creates ambiguity: if a user pastes a line like '123 + 456' (a numeric expression), it would be incorrectly reformatted as line number 123 with code '+ 456'. The comment acknowledges this issue but the code doesn't handle it.

---

#### code_vs_comment


**Description:** Comment claims editor_lines stores execution state while editor.lines stores editing state, but code shows they serve overlapping purposes

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~130 says:
# Note: self.editor_lines stores execution state (lines loaded from file for RUN)
# self.editor.lines (in ProgramEditorWidget) stores the actual editing state
# These serve different purposes and are synchronized as needed

However, _save_editor_to_program() (line ~95) syncs FROM editor.lines TO program manager, and _refresh_editor() (line ~165) syncs FROM program manager TO editor.lines. The editor_lines dict appears to be a redundant copy that's not consistently maintained - it's only populated in _sync_program_to_editor() which is called once at startup.

---

#### code_vs_comment


**Description:** Comment says status bar stays at default but code updates it with error/completion messages

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _debug_step() and _debug_step_line(), comments say:
# Status bar stays at default (STATUS_BAR_SHORTCUTS) - error message is in output
# Status bar stays at default (STATUS_BAR_SHORTCUTS) - completion message is in output

But earlier in the same methods, the code updates status bar:
self.status_bar.set_text(f"Paused at {pc_display} - {key_to_display(STEP_KEY)}=Step...")

The comments suggest the status bar is left unchanged, but it's actually updated with pause/step information.

---

#### code_vs_comment


**Description:** Comment about cursor positioning contradicts actual behavior in _delete_current_line

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~810 says:
# Position cursor at beginning of next line (or previous if at end)
# Always position at column 1 (start of line number field)

But the code at line ~820 does:
if line_index < len(lines):
    # Position at start of line that moved up (column 1)
    if line_index > 0:
        new_cursor_pos = sum(len(lines[i]) + 1 for i in range(line_index)) + 1
    else:
        new_cursor_pos = 1  # First line, column 1
else:
    # Was last line, position at end of previous line
    if lines:
        new_cursor_pos = sum(len(lines[i]) + 1 for i in range(len(lines) - 1)) + len(lines[-1])

The else branch positions at END of previous line, not column 1 as the comment claims.

---

#### code_vs_comment


**Description:** Docstring for _refresh_editor doesn't mention error cleanup behavior

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
The _refresh_editor() docstring at line ~165 says:
"""Refresh the editor display from program manager.

Called by immediate executor after adding/deleting lines via commands like "20 PRINT".
Syncs the editor widget's line storage with the program manager's lines.
"""

But the code also does:
# Clean up any empty auto-numbered lines left in the editor
current_text = self.editor.edit_widget.get_edit_text()
new_text = self.editor._parse_line_numbers(current_text)
if new_text != current_text:
    self.editor.edit_widget.set_edit_text(new_text)

This cleanup behavior is not documented in the docstring.

---

#### code_vs_comment


**Description:** Comment claims column 7 is start of code area, but code uses variable code_start from _parse_line_number

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _insert_line_after_current():
Comment says: '# Position cursor on the new line, at the code area (column 7)'
and 'new_cursor_pos = 7  # Column 7 is start of code area'

But in _toggle_breakpoint_current_line(), the code uses:
line_number, code_start = self.editor._parse_line_number(line)
code_area = line[7:] if len(line) > 7 else ""

This suggests column 7 is hardcoded in some places but _parse_line_number returns a variable code_start in others. The comment may be outdated if line number width is variable.

---

#### code_vs_comment


**Description:** Comment about breakpoint storage contradicts implementation details

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _setup_program() comment:
'Note: reset_for_run() clears variables and resets PC. Breakpoints are STORED in the editor (self.editor.breakpoints) as the authoritative source, not in runtime. This allows them to persist across runs. After reset_for_run(), we re-apply them to the interpreter below via set_breakpoint() calls so execution can check them.'

But the code shows breakpoints are re-applied AFTER interpreter.start():
'# Start interpreter (sets up statement table, etc.)
state = self.interpreter.start()
...
# Re-apply breakpoints from editor
for line_num in self.editor.breakpoints:
    self.interpreter.set_breakpoint(line_num)'

The comment says 'below' but doesn't clarify that it's after start(), which is important because start() might clear breakpoints. The timing is critical but not clearly documented.

---

#### code_internal_inconsistency


**Description:** Inconsistent status bar update strategy across error handling paths

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _setup_program() and _run_program(), parse errors and startup errors show:
'# Status bar stays at default - error is displayed in output'

But in _execute_tick() for runtime errors:
'# Status bar stays at default - error is displayed in output'

However, when program completes successfully:
'self._update_status_with_errors("Ready")'

And when paused:
'self.status_bar.set_text(f"Paused at line {state.current_line} - ...")''

The comment pattern '# Status bar stays at default' appears multiple times but it's unclear what 'default' means - is it STATUS_BAR_SHORTCUTS? The code doesn't explicitly set it to any default value in error cases.

---

#### code_vs_comment


**Description:** Comment claims ESC sets stopped=True similar to STOP statement, but code actually sets runtime.stopped=True which is the correct field

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Line ~1086-1088:
Comment: '# Note: This sets stopped=True similar to a BASIC STOP statement, but the semantics'
Code: 'self.runtime.stopped = True'
The comment says 'stopped=True' without the 'runtime.' prefix, which could be misleading about what field is being set.

---

#### code_vs_comment


**Description:** Comment in _execute_immediate claims immediate executor already called interpreter.start() for RUN commands, but this may not be accurate for all RUN scenarios

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Lines ~1550-1555:
Comment: '# NOTE: Don't call interpreter.start() here - the immediate executor already
# called it if needed (e.g., 'RUN 120' called interpreter.start(start_line=120)
# to set PC to line 120). Calling it again would reset PC to the beginning.'

This assumes immediate executor handles all RUN initialization, but the code then checks 'if not hasattr(self.interpreter, 'state') or self.interpreter.state is None' and creates InterpreterState. This suggests there may be cases where start() wasn't called, making the comment potentially misleading.

---

#### code_internal_inconsistency


**Description:** Inconsistent handling of CapturingIOHandler creation - comment says 'duplicates definition in _run_program' but then imports from shared module

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Lines ~1545-1549:
Comment: '# Need to create the CapturingIOHandler class inline
# (duplicates definition in _run_program - consider extracting to shared location)'
Code immediately after: 'from .capturing_io_handler import CapturingIOHandler'

The comment suggests inline duplication is needed, but the code actually imports from a shared module, making the comment incorrect and confusing.

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
Class docstring (lines 22-29):
'This class is instantiated when editing variables via the variable inspector
(see _on_variable_edit() around line 1194).'

The file shown only goes to line 1194 in the partial view, but the actual method referenced is _edit_simple_variable at line 1194. The comment says '_on_variable_edit()' but no such method exists in the visible code. The actual method that uses this token appears to be _edit_simple_variable or similar.

---

#### code_vs_comment


**Description:** Comment about toolbar simplification references removed features but doesn't match menu structure

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment in _create_toolbar (lines 481-486):
'# Note: Toolbar has been simplified to show only essential execution controls.
# Additional features are accessible via menus:
# - List Program → Run > List Program
# - New Program (clear) → File > New
# - Clear Output → Run > Clear Output'

The comment lists 'New Program (clear)' as if it's a separate feature from 'New', but the menu only has 'File > New' (line 357). The comment suggests there was a 'New Program (clear)' button that was removed, but it's unclear if 'New' and 'New Program (clear)' are the same feature or different.

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

This comment describes current behavior but doesn't explain why it's limited to Enter key only. If blank line removal is desirable, why not after paste? The comment suggests this might be incomplete implementation rather than intentional design, but doesn't clarify.

---

#### code_vs_comment


**Description:** Comment about validation timing doesn't match all call sites

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _validate_editor_syntax method around line 1502:
Comment says: "# Note: This method is called:\n# - With 100ms delay after cursor movement/clicks (to avoid excessive validation during rapid editing)\n# - Immediately when focus leaves editor (to ensure validation before switching windows)"

However, looking at the code:
- _on_cursor_move calls it with 100ms delay (matches comment)
- _on_mouse_click calls it with 100ms delay (matches comment)
- _on_focus_out calls it immediately (matches comment)
- But _on_enter_key at line 1652 calls it via _save_editor_to_program, which is not mentioned in the comment

The comment is incomplete about all the places validation occurs.

---

#### code_vs_comment


**Description:** Comment about error display logic contradicts single-error case handling

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _validate_editor_syntax method around line 1524:
Comment says: "# Only show full error list in output if there are multiple errors.\n# For single errors, the red ? icon in the editor is sufficient feedback.\n# This avoids cluttering the output pane with repetitive messages during editing."

But then the code shows status bar message for all error counts:
error_count = len(errors_found)
plural = "s" if error_count > 1 else ""
self._set_status(f"Syntax error{plural} in program - cannot run")

So single errors DO get feedback in the status bar, not just the red ? icon. The comment is misleading about "sufficient feedback" being only the icon.

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

But _on_status_click() code shows:
if error_msg:
    messagebox.showerror(...)
else:
    # Has breakpoint, not error
    if metadata.get('has_breakpoint'):
        messagebox.showinfo(...)

This suggests only one symbol is shown at a time (consistent with docstring), but the comment '# Has breakpoint, not error' implies mutual exclusivity in display, which aligns with the docstring.

---

#### code_vs_comment


**Description:** _parse_line_number() docstring claims MBASIC 5.21 requires whitespace between line number and statement, but regex allows end-of-string which means standalone line numbers are valid

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment in _parse_line_number() says:
"# Valid: '10 PRINT' (whitespace after), '10' (end after), '  10  REM' (leading whitespace ok)
# Invalid: '10REM' (no whitespace), 'ABC10' (non-digit prefix), '' (empty after strip)
# MBASIC 5.21 requires whitespace (or end of line) between line number and statement"

The regex: r'^(\d+)(?:\s|$)'

The comment says 'MBASIC 5.21 requires whitespace (or end of line)' but then lists '10' (standalone number) as valid. This is technically consistent (end-of-string counts), but the phrasing 'between line number and statement' is misleading when there's no statement. Should clarify that standalone line numbers (no statement) are valid.

---

#### documentation_inconsistency


**Description:** Class docstring describes automatic blank line removal feature but doesn't mention that it only removes lines when cursor moves AWAY from them, not when they're created

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Class docstring says:
"Automatic blank line removal:
- When cursor moves away from a blank line, that line is automatically deleted
- This helps keep BASIC programs clean by removing accidental blank lines
- Implemented via _on_cursor_move() tracking cursor movement"

This is accurate but could be clearer about the timing: blank lines are NOT removed immediately when created (e.g., pressing Enter on an empty line), only when the cursor moves to a different line. A user might expect immediate removal based on the description.

---

#### code_vs_comment


**Description:** _on_status_click() docstring says it shows 'confirmation message for ●' but the actual message is more informational/instructional than confirmatory

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Docstring says:
"Handle click on status column (show error details for ?, confirmation message for ●).

Displays informational messages about line status:
- For error markers (?): Shows error message in a message box
- For breakpoint markers (●): Shows confirmation message that breakpoint is set"

Actual message shown:
messagebox.showinfo(
    f'Breakpoint on Line {line_num}',
    f'Line {line_num} has a breakpoint set.\n\nUse the debugger menu or commands to manage breakpoints.'
)

This is more of an informational/help message than a 'confirmation'. The term 'confirmation message' typically implies confirming an action just taken, but this is showing status of an existing breakpoint.

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

#### code_vs_documentation


**Description:** Settings dialog implemented in web UI but not documented in editor commands or any help files

**Affected files:**
- `src/ui/web/web_settings_dialog.py`
- `docs/help/common/editor-commands.md`

**Details:**
web_settings_dialog.py implements a full settings dialog with:
- Auto-numbering enable/disable
- Auto-number step configuration
- Resource limits viewing

But editor-commands.md only mentions 'Program Management', 'Debugging', 'Editing', and 'Help Navigation' categories. No mention of settings/preferences/configuration commands.

The help system should document how to access and use the settings dialog.

---

#### code_vs_documentation


**Description:** Session state tracks auto-save settings but debugging documentation doesn't mention auto-save feature

**Affected files:**
- `src/ui/web/session_state.py`
- `docs/help/common/debugging.md`

**Details:**
session_state.py includes:
auto_save_enabled: bool = True
auto_save_interval: int = 30

But debugging.md and other help files never mention auto-save functionality. Users should be informed about:
- Whether auto-save is enabled
- How often it saves
- Where auto-saved files go
- How to recover from auto-save

---

#### documentation_inconsistency


**Description:** Debugging documentation uses placeholder kbd tags that don't match actual keybindings

**Affected files:**
- `docs/help/common/debugging.md`
- `src/ui/web_keybindings.json`

**Details:**
debugging.md uses placeholders like:
{{kbd:step:curses}}
{{kbd:continue:curses}}
{{kbd:quit:curses}}
{{kbd:toggle_stack:tk}}
{{kbd:step_line:curses}}

But web_keybindings.json shows actual keys:
"step": {"keys": ["F10"], "primary": "F10"}
"continue": {"keys": ["F5"], "primary": "F5"}
"stop": {"keys": ["Esc"], "primary": "Esc"}

The documentation should either:
1. Replace placeholders with actual keys for each UI
2. Explain the placeholder system
3. Reference the keybindings.json file

---

#### code_vs_documentation


**Description:** Session state tracks recent files list but no documentation for recent files feature

**Affected files:**
- `src/ui/web/session_state.py`
- `docs/help/common/debugging.md`

**Details:**
session_state.py includes:
current_file: Optional[str] = None
recent_files: List[str] = field(default_factory=list)
max_recent_files: int = 10

This suggests a 'recent files' menu or feature exists, but:
- No help documentation mentions recent files
- No documentation on how to access recent files
- No documentation on the 10-file limit

Users should be informed about this feature.

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


**Description:** Incomplete ASCII reference in character-set.md

**Affected files:**
- `docs/help/common/language/character-set.md`
- `docs/help/common/language/appendices/ascii-codes.md`

**Details:**
character-set.md provides a brief 'Control Characters' table with only 7 entries (BEL, BS, TAB, LF, CR, ESC) and says 'Use CHR$() to include control characters in strings.' However, it references ascii-codes.md for complete reference. The ascii-codes.md has a full table of all 32 control characters (0-31). This is not necessarily an inconsistency but character-set.md could be clearer that it's showing only commonly used control characters.

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
Both INKEY$ and INPUT$ mention Control-C behavior, but with slightly different wording:

INKEY$: 'Note: Control-C behavior varied in original implementations. In MBASIC 5.21 interpreter mode, Control-C would terminate the program. This implementation passes Control-C through (CHR$(3)) for program detection and handling, allowing programs to detect and handle it explicitly.'

INPUT$: 'Note: Control-C behavior: This implementation passes Control-C through (CHR$(3)) for program detection and handling, allowing programs to detect and handle it explicitly.'

The INPUT$ note is shorter and doesn't mention the historical MBASIC 5.21 behavior. These should be consistent.

---

#### documentation_inconsistency


**Description:** CLEAR documentation has conflicting information about parameter meanings between MBASIC 5.21 and earlier versions

**Affected files:**
- `docs/help/common/language/statements/clear.md`

**Details:**
The documentation states:

'In MBASIC 5.21 (BASIC-80 release 5.0 and later):
- expression1: If specified, sets the highest memory location available for BASIC to use
- expression2: Sets the stack space reserved for BASIC'

But then notes:

'Historical note: In earlier versions of BASIC-80 (before release 5.0), the parameters had different meanings:
- expression1 set the amount of string space
- expression2 set the end of memory'

This is confusing because the documentation is for MBASIC 5.21 but includes historical information that contradicts the current behavior. The syntax section doesn't clarify which version's behavior is being documented.

---

#### documentation_inconsistency


**Description:** DATA statement documentation has incomplete example explanation

**Affected files:**
- `docs/help/common/language/statements/data.md`

**Details:**
The example shows:
'10 DATA 12, 3.14159, "Hello", WORLD'

But the remarks state: 'String constants in DATA statements must be surrounded by double quotation marks only if they contain commas, colons or significant leading or trailing spaces. Otherwise, quotation marks are not needed.'

The example shows 'Hello' with quotes and WORLD without quotes, but doesn't explain why this difference exists or what makes WORLD not need quotes while Hello does. This could confuse readers about when quotes are required.

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


**Description:** LINE INPUT# documentation references non-existent input_hash.md file

**Affected files:**
- `docs/help/common/language/statements/inputi.md`

**Details:**
In inputi.md 'See Also' section:
- [INPUT#](input_hash.md) - Read data from sequential file

But there is no input_hash.md file in the provided documentation. This should likely reference a file about INPUT# statement for sequential file reading.

---

#### documentation_inconsistency


**Description:** PRINT# documentation references non-existent input_hash.md file

**Affected files:**
- `docs/help/common/language/statements/printi-printi-using.md`

**Details:**
In printi-printi-using.md 'See Also' section:
- [INPUT#](input_hash.md) - Read data from sequential file

But there is no input_hash.md file in the provided documentation.

---

#### documentation_inconsistency


**Description:** OPEN documentation references non-existent input_hash.md file

**Affected files:**
- `docs/help/common/language/statements/open.md`

**Details:**
In open.md 'See Also' section:
- [INPUT#](input_hash.md) - Read from sequential file

But there is no input_hash.md file in the provided documentation.

---

#### documentation_inconsistency


**Description:** PRINT# documentation missing WRITE# reference in See Also

**Affected files:**
- `docs/help/common/language/statements/printi-printi-using.md`

**Details:**
The printi-printi-using.md file mentions WRITE# in the remarks:
"PRINT#, PRINT# USING, and WRITE# may be used to put characters in the random file buffer"

But the 'See Also' section includes:
- [WRITE#](writei.md) - Write data with automatic delimiters

However, no writei.md file is provided in the documentation set, so this reference is broken.

---

#### documentation_inconsistency


**Description:** Contradictory information about file closing behavior

**Affected files:**
- `docs/help/common/language/statements/load.md`
- `docs/help/common/language/statements/merge.md`

**Details:**
load.md states:
"LOAD (without ,R): Closes all open files"
"LOAD with ,R option: all open data files are kept open"
"Compare with MERGE: Never closes files"

merge.md states:
"Unlike LOAD (without ,R), MERGE does NOT close open files. Files that are open before MERGE remain open after MERGE completes."

This is consistent, but the emphasis and wording differs. load.md says MERGE "Never closes files" while merge.md says it "does NOT close open files". The information is the same but could be more consistently worded.

---

#### documentation_inconsistency


**Description:** Cross-reference inconsistency: RESET warns not to confuse with RSET, but RSET warns not to confuse with RESET. Both should use consistent wording.

**Affected files:**
- `docs/help/common/language/statements/reset.md`
- `docs/help/common/language/statements/rset.md`

**Details:**
RESET.md says: 'Do not confuse RESET with [RSET](rset.md), which right-justifies strings in random file fields.'

RSET.md says: 'Do not confuse RSET with [RESET](reset.md), which closes all open files.'

Both warnings are correct but could be more consistent in phrasing.

---

#### documentation_inconsistency


**Description:** Inconsistent description of file closing behavior across program termination commands

**Affected files:**
- `docs/help/common/language/statements/run.md`
- `docs/help/common/language/statements/stop.md`
- `docs/help/common/language/statements/system.md`

**Details:**
RUN.md: 'All open files are closed (unlike STOP, which keeps files open)'

STOP.md: 'Unlike the END statement, the STOP statement does not close files.'

SYSTEM.md: 'When SYSTEM is executed: All open files are closed'

This is consistent but could be clearer about which commands close files: RUN (yes), STOP (no), END (yes), SYSTEM (yes)

---

#### documentation_inconsistency


**Description:** WIDTH documentation shows unsupported syntax but doesn't clearly mark all limitations

**Affected files:**
- `docs/help/common/language/statements/width.md`

**Details:**
The doc shows 'WIDTH LPRINT <integer expression>' marked as unsupported, but the implementation note says 'The simple "WIDTH <number>" statement parses and executes successfully' which implies it's a no-op.

The doc should clarify: Does 'WIDTH 80' parse and do nothing, or does it cause an error? The implementation note says it's a no-op, but this should be clearer in the main documentation.

---

#### documentation_inconsistency


**Description:** Settings scope precedence mentions 'File scope (future feature)' but doesn't explain what this means or when it will be available

**Affected files:**
- `docs/help/common/settings.md`

**Details:**
Settings.md lists: '1. File scope (highest priority) - Per-file settings (future feature)'

This should clarify: Is this planned? Is it partially implemented? Should users expect this feature?

---

#### documentation_inconsistency


**Description:** SETSETTING and SHOWSETTINGS marked as 'MBASIC Extension' but settings.md doesn't clearly state this at the top

**Affected files:**
- `docs/help/common/language/statements/setsetting.md`
- `docs/help/common/language/statements/showsettings.md`
- `docs/help/common/settings.md`

**Details:**
setsetting.md: 'Versions: MBASIC Extension'
showsettings.md: 'Versions: MBASIC Extension'

settings.md mentions: 'Note: The settings system is a MBASIC Extension - not present in original MBASIC 5.21.'

This is consistent but the note appears mid-document. It should be more prominent.

---

#### documentation_inconsistency


**Description:** File extension handling inconsistency between SAVE and RUN commands

**Affected files:**
- `docs/help/common/language/statements/save.md`
- `docs/help/common/language/statements/run.md`

**Details:**
save.md: 'With CP/M, the default extension .BAS is supplied'

run.md: 'File extension defaults to .BAS if not specified'

Both mention .BAS default but SAVE specifically mentions CP/M while RUN doesn't. Should be consistent about OS-specific behavior.

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


**Description:** Inconsistent description of Web UI filename handling

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/extensions.md`

**Details:**
Compatibility.md states 'Automatically uppercased by the virtual filesystem (CP/M style)' and 'The uppercasing is a programmatic transformation for CP/M compatibility, not evidence of persistent storage'. However, extensions.md doesn't mention this uppercasing behavior at all when describing Web UI file limitations. This could confuse users about whether filenames are case-sensitive.

---

#### documentation_inconsistency


**Description:** Inconsistent information about PEEK behavior

**Affected files:**
- `docs/help/mbasic/architecture.md`
- `docs/help/mbasic/compatibility.md`

**Details:**
Architecture.md states 'PEEK: Returns random integer 0-255 (for RNG seeding compatibility)' while compatibility.md states the exact same thing. However, neither document explains WHY this specific behavior was chosen or whether it's deterministic randomness or true randomness. This could affect programs that rely on PEEK for seeding.

---

#### documentation_inconsistency


**Description:** Missing cross-reference for debugging commands

**Affected files:**
- `docs/help/mbasic/extensions.md`
- `docs/help/common/ui/cli/index.md`

**Details:**
Extensions.md mentions 'See [CLI Debugging](../ui/cli/debugging.md)' but the CLI index.md doesn't mention or link to this debugging documentation. Users reading CLI docs won't discover the debugging features.

---

#### documentation_inconsistency


**Description:** Inconsistent UI selection paths in main help index

**Affected files:**
- `docs/help/index.md`
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/curses/editing.md`
- `docs/help/common/ui/tk/index.md`

**Details:**
Main index lists UI paths as:
- [Tk (Desktop GUI)](ui/tk/index.md)
- [Curses (Terminal)](ui/curses/index.md)
- [Web Browser](ui/web/index.md)
- [CLI (Command Line)](ui/cli/index.md)

But the actual doc files are at:
- docs/help/common/ui/tk/index.md
- docs/help/common/ui/curses/editing.md
- docs/help/common/ui/cli/index.md

The paths in index.md are missing the 'common/' prefix and may be incorrect.

---

#### documentation_inconsistency


**Description:** Inconsistent information about auto-save behavior

**Affected files:**
- `docs/help/mbasic/compatibility.md`
- `docs/help/mbasic/extensions.md`

**Details:**
Extensions.md states 'Auto-save behavior varies by UI' and lists different behaviors for CLI/Tk/Curses vs Web UI. However, compatibility.md doesn't mention auto-save at all when discussing file operations. Users may not understand that file persistence differs by UI.

---

#### documentation_inconsistency


**Description:** Inconsistent UI listing - Web UI mentioned in some places but not others

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`
- `docs/help/mbasic/index.md`

**Details:**
features.md lists four UIs: 'MBASIC supports four interfaces: Curses UI (Default), CLI Mode, Tkinter GUI, Web UI' with detailed Web UI section.

getting-started.md lists four UIs: 'MBASIC supports four interfaces: Curses UI (Default), CLI Mode, Tkinter GUI, Web UI'

index.md only mentions three UIs: 'Choice of user interfaces (CLI, Curses, Tkinter)' and 'UI-Specific Guides' section only links to Curses, CLI, and Tk - no Web UI link.

The Quick Links section in index.md says 'Choose your UI: [CLI](../ui/cli/index.md), [Curses](../ui/curses/index.md), [Tk](../ui/tk/index.md), or Web' but 'Web' is not a link.

---

#### documentation_inconsistency


**Description:** Debugging features availability inconsistency

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/debugging.md`

**Details:**
features.md states under Debugging section: 'Breakpoints - Set/clear breakpoints (available in all UIs; access method varies)' and similar for step execution, variable viewing, and stack viewer.

cli/debugging.md documents BREAK, STEP, and STACK commands for CLI, confirming these are available.

However, features.md says 'See UI-specific documentation for details: [CLI Debugging](../ui/cli/debugging.md), [Curses UI](../ui/curses/feature-reference.md), [Tk UI](../ui/tk/feature-reference.md)' but the Curses and Tk links point to 'feature-reference.md' which may not exist or may not be the correct debugging documentation path.

---

#### documentation_inconsistency


**Description:** Keyboard shortcut notation inconsistency

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
features.md uses template notation: '{{kbd:run:curses}}', '{{kbd:save:curses}}', '{{kbd:help:curses}}', '{{kbd:quit:curses}}', '{{kbd:find:tk}}', '{{kbd:replace:tk}}', '{{kbd:step_line:curses}}'

getting-started.md also uses template notation in 'Common keyboard shortcuts (Curses UI)' section with same format.

However, these appear to be template placeholders that should be replaced with actual key combinations (like 'F5', 'Ctrl+S', etc.) but are left as templates in the documentation. This makes the docs less useful for end users.

---

#### documentation_inconsistency


**Description:** Statement count inconsistency

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
features.md doesn't provide a total count of implemented statements.

not-implemented.md references: '[Statements](../../common/language/statements/index.md) - All 63 statements' in the CLI help index.

features.md should clarify if all 63 statements are from MBASIC 5.21 or if this includes some that aren't in the original MBASIC 5.21 spec.

---

#### documentation_inconsistency


**Description:** Error code count inconsistency

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/ui/cli/index.md`

**Details:**
features.md doesn't specify how many error codes are supported.

cli/index.md states: '[Error Codes](../../common/language/appendices/error-codes.md) - All 68 error codes'

features.md should mention this count in its 'Error Handling' section for completeness.

---

#### documentation_inconsistency


**Description:** Incomplete STEP command documentation

**Affected files:**
- `docs/help/ui/cli/debugging.md`

**Details:**
cli/debugging.md documents STEP command with syntax: 'STEP [n] - Execute n statements (default: 1)\nSTEP INTO - Step into subroutines\nSTEP OVER - Step over subroutine calls'

But later under 'Limitations' it states: 'STEP INTO/OVER not yet implemented (use STEP)'

This is contradictory - the syntax section implies these work, but limitations say they don't. The syntax section should mark these as 'planned' or remove them entirely.

---

#### documentation_inconsistency


**Description:** Installation instructions inconsistency

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
getting-started.md shows installation with: 'git clone https://github.com/avwohl/mbasic.git'

features.md doesn't provide installation instructions but references getting-started.md.

However, the repository URL should be verified - 'avwohl' may not be the correct GitHub username/organization. This could lead users to a non-existent repository.

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


**Description:** Placeholder documentation conflicts with detailed UI-specific documentation

**Affected files:**
- `docs/help/ui/common/running.md`
- `docs/help/ui/curses/running.md`

**Details:**
docs/help/ui/common/running.md is marked as '**Status:** PLACEHOLDER - Documentation in progress' and says 'For UI-specific instructions: - CLI: `docs/help/ui/cli/` - Curses: `docs/help/ui/curses/running.md`'

However, docs/help/ui/curses/running.md is a complete, detailed guide with full instructions. This suggests the placeholder status in common/running.md is outdated, or the common doc should be updated to reference the complete UI-specific docs.

---

#### documentation_inconsistency


**Description:** Inconsistent information about Renumber keyboard shortcut

**Affected files:**
- `docs/help/ui/curses/feature-reference.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
docs/help/ui/curses/feature-reference.md states: '### Renumber ({{kbd:renumber:curses}})
Renumber all program lines with consistent increments. Opens a dialog to specify start line and increment.'

But docs/help/ui/curses/quick-reference.md under 'Editing' states: '**Menu only** | Renumber all lines (RENUM)'

This is contradictory - either Renumber has a keyboard shortcut ({{kbd:renumber:curses}}) or it's menu-only.

---

#### documentation_inconsistency


**Description:** Inconsistent shortcut notation for Search Help

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
feature-reference.md shows:
'Search Help ({{kbd:file_save:tk}}hift+F)'

Similar typo as above - should likely be 'Shift+F' or '{{kbd:file_save:tk}}+Shift+F'. The pattern suggests {{kbd:file_save:tk}} macro was incorrectly used.

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

Delete Lines is listed under File Operations but is actually an Edit operation (mentioned as 'Edit → Delete Lines menu'). This makes the count misleading.

---

#### documentation_inconsistency


**Description:** Inconsistent keyboard shortcut references for Run Program

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/getting-started.md`

**Details:**
feature-reference.md states:
'Run Program ({{kbd:run_program:tk}} or F5)'

But getting-started.md uses:
'{{kbd:run_program}}' (without :tk suffix)

Inconsistent macro usage across documents.

---

#### documentation_inconsistency


**Description:** Settings dialog implementation status unclear

**Affected files:**
- `docs/help/ui/tk/settings.md`

**Details:**
settings.md states at the top:
'**Implementation Status:** The Tk (Tkinter) desktop GUI is planned to provide the most comprehensive settings dialog. **The features described in this document represent planned/intended implementation and are not yet available.**'

But then later states:
'**Note:** Settings storage is implemented, but the settings dialog itself is not yet available in the Tk UI.'

This creates confusion - is settings storage implemented or not? The document needs clarification on what exactly is implemented vs planned.

---

#### documentation_inconsistency


**Description:** Inconsistent keyboard shortcut macro usage

**Affected files:**
- `docs/help/ui/tk/workflows.md`
- `docs/help/ui/tk/tips.md`

**Details:**
workflows.md uses:
- {{kbd:file_new:tk}}
- {{kbd:run_program:tk}}
- {{kbd:file_save:tk}}
- {{kbd:smart_insert:tk}}
- {{kbd:toggle_variables:tk}}
- {{kbd:renumber:tk}}

tips.md uses:
- {{kbd:smart_insert:tk}}
- {{kbd:toggle_variables:tk}}
- {{kbd:toggle_stack:tk}}
- {{kbd:run_program:tk}}
- {{kbd:file_save:tk}}

Both use :tk suffix consistently, but getting-started.md and features.md sometimes omit the :tk suffix. There should be a consistent pattern.

---

#### documentation_inconsistency


**Description:** Inconsistent implementation status markers

**Affected files:**
- `docs/help/ui/web/debugging.md`

**Details:**
debugging.md uses multiple different markers for implementation status:
- '**Implementation Status:**' (for Variable Inspector)
- '**Currently Implemented**' (for Debug Controls)
- '**Note:**' (for various features)
- '(Planned)' suffix on section headers
- '(Future)' suffix on section headers

There should be a consistent way to mark implementation status throughout the document.

---

#### documentation_inconsistency


**Description:** Quick Reference table has inconsistent shortcut information

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`

**Details:**
The Quick Reference table shows:
- '{{kbd:run_program:tk}} / F5' for Run Program
- '{{kbd:cut:tk}}' for Stop Program
- 'F10' for Step Line
- '(toolbar)' for Step Statement and Continue

But earlier in the document:
- Stop/Interrupt shows '{{kbd:cut:tk}}' which conflicts with Cut operation
- Continue shows 'No keyboard shortcut'
- Step Statement shows 'No keyboard shortcut'

The Quick Reference should match the detailed descriptions.

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


**Description:** Unclear scope precedence for settings

**Affected files:**
- `docs/user/SETTINGS_AND_CONFIGURATION.md`

**Details:**
The document states settings are applied in order: '1. File scope - Per-file settings (future feature) 2. Project scope - .mbasic/settings.json in project directory 3. Global scope - ~/.mbasic/settings.json in home directory 4. Default - Built-in defaults' with '(most specific wins)'. However, 'File scope' is listed as #1 (most specific) but is also marked as '(future feature)', meaning it doesn't actually exist yet. This could confuse users about current behavior.

---

#### documentation_inconsistency


**Description:** Contradictory information about tkinter installation

**Affected files:**
- `docs/user/INSTALL.md`

**Details:**
Under 'System Package Requirements', the document states tkinter is 'OPTIONAL for Tkinter GUI Backend' and 'Only needed if you want to use the Tkinter GUI backend'. However, under 'Python Package Dependencies' it says 'Tk mode: Requires tkinter (usually pre-installed with Python)'. Later under 'Method 2: Direct Installation' it says 'For other UIs (Curses, Tk, Web), you'll need to install their dependencies via pip install -r requirements.txt'. This is contradictory - tkinter is a system package (python3-tk), not a pip package, and wouldn't be in requirements.txt.

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


**Description:** LineNode documentation mentions position_serializer module but doesn't explain the regeneration mechanism fully

**Affected files:**
- `src/ast_nodes.py`

**Details:**
LineNode lines 127-137:
'Design note: This class intentionally does not have a source_text field to avoid maintaining duplicate copies that could get out of sync with the AST during editing. Text regeneration is handled by the position_serializer module which reconstructs source text from statement nodes and their token information. Each StatementNode has char_start/char_end offsets that indicate the character position within the regenerated line text.'

This references position_serializer module and mentions char_start/char_end offsets, but doesn't explain how tokens preserve original_case or how the regeneration actually works. The mechanism is split across multiple comments (LineNode, PrintStatementNode) making it hard to understand the complete picture.

---

#### Documentation inconsistency


**Description:** ChainStatementNode delete_range type annotation inconsistency

**Affected files:**
- `src/ast_nodes.py`

**Details:**
ChainStatementNode lines 577-578:
'delete_range: Optional[Tuple[int, int]] = None  # (start_line_number, end_line_number) for DELETE option - tuple of int line numbers'

The comment redundantly states 'tuple of int line numbers' when the type annotation already clearly specifies 'Tuple[int, int]'. This is unnecessarily verbose and could become inconsistent if the type changes.

---

#### Documentation inconsistency


**Description:** InputStatementNode documentation has confusing explanation of suppress_question flag

**Affected files:**
- `src/ast_nodes.py`

**Details:**
InputStatementNode lines 213-227:
'Note: The suppress_question field controls "?" display:
- suppress_question=False (default): Adds "?" after prompt
  Examples: INPUT var → "? ", INPUT "Name", var → "Name? ", INPUT "Name"; var → "Name? "
- suppress_question=True: No "?" added, no prompt displayed
  Examples: INPUT; var → "" (no prompt, no "?")

Semicolon usage:
- INPUT; var → semicolon immediately after INPUT (suppress_question=True, no "?")
- INPUT "prompt"; var → semicolon after prompt is just separator (suppress_question=False, shows "?")'

The explanation conflates two different uses of semicolon: one immediately after INPUT (which suppresses the question mark) and one after the prompt (which is just a separator). The examples show 'INPUT "Name"; var → "Name? "' with suppress_question=False, which seems to contradict the semicolon usage explanation.

---

#### Documentation inconsistency


**Description:** ResumeStatementNode uses 0 to mean RESUME NEXT but documentation is ambiguous

**Affected files:**
- `src/ast_nodes.py`

**Details:**
ResumeStatementNode lines 711-720:
'RESUME statement - continue after error

Syntax:
    RESUME                  - Retry statement that caused error
    RESUME NEXT             - Continue at next statement
    RESUME line_number      - Continue at specific line

line_number: Optional[int]  # None means RESUME, 0 means RESUME NEXT'

Using 0 to represent RESUME NEXT is confusing because 0 could also be interpreted as line number 0. A better design would use a separate boolean flag or an enum to distinguish between RESUME, RESUME NEXT, and RESUME line_number.

---

#### Code vs Documentation inconsistency


**Description:** setup.py excludes 'basic' directory but doesn't document what it contains

**Affected files:**
- `setup.py`

**Details:**
setup.py line 23:
'packages=find_packages(exclude=["tests", "basic", "doc", "utils", "bin"])'

The setup.py excludes a 'basic' directory from packaging, but there's no documentation explaining what this directory contains or why it's excluded. This could be sample BASIC programs, test files, or something else.

---

#### code_vs_comment_conflict


**Description:** Comment describes sign determination logic but references wrong line number after code changes

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line 274 comment: 'Determine sign - preserve negative sign for values that round to zero.
Use original_negative (captured at line 272 before rounding)...'
However, original_negative is actually captured at line 270, not line 272. The comment references an outdated line number from before code was modified.

---

#### code_vs_comment_conflict


**Description:** Comment about leading sign padding behavior contradicts general padding logic

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line 336-337 comment: '# For leading sign: padding comes first, then sign immediately before number
if spec['leading_sign']:
    # Add padding first (but only spaces, not asterisks for leading sign)'
Line 341-345 code: 'if spec['asterisk_fill']:
    result_parts.append('*' * max(0, padding_needed))
else:
    result_parts.append(' ' * max(0, padding_needed))'
The comment at line 337 says 'but only spaces, not asterisks for leading sign', but the code at lines 341-345 is in the else block (no leading sign), so it applies asterisk_fill when there's NO leading sign. The comment placement suggests asterisk_fill is disabled for leading_sign, but the code structure shows asterisk_fill only applies when leading_sign is False.

---

#### documentation_inconsistency


**Description:** Module docstring references tokens.py for MBASIC 5.21 specification but tokens.py is not provided

**Affected files:**
- `src/basic_builtins.py`

**Details:**
Line 1-8 docstring: 'Built-in functions for MBASIC 5.21 (CP/M era MBASIC-80).

BASIC built-in functions (SIN, CHR$, INT, etc.) and formatting utilities (TAB, SPC, USING).

Note: Version 5.21 refers to BASIC-80 Reference Manual Version 5.21. See tokens.py for
complete MBASIC 5.21 specification reference.'
The docstring directs readers to 'tokens.py for complete MBASIC 5.21 specification reference' but tokens.py is not included in the provided source files, making this reference unverifiable.

---

#### Code vs Comment conflict


**Description:** Comment about GOSUB return mechanism doesn't match implementation complexity

**Affected files:**
- `src/codegen_backend.py`

**Details:**
In _generate_gosub() method comment:
"# Each GOSUB gets a unique return label"

But the implementation is more complex: it uses a stack (gosub_stack) and a switch statement in _generate_return() to handle multiple return points. The comment oversimplifies the mechanism. The actual implementation uses:
1. A counter for unique return IDs
2. A stack to track return addresses
3. A switch statement to jump to the correct return point

This is more sophisticated than just "unique return labels".

---

#### Documentation inconsistency


**Description:** Duplicate two-letter error codes documented but handling not explained

**Affected files:**
- `src/error_codes.py`

**Details:**
Module docstring states:
"Note: Some two-letter codes are duplicated (e.g., DD, CN, DF) across different numeric error codes. This matches the original MBASIC 5.21 specification where the two-letter codes alone are ambiguous - the numeric code is authoritative. All error handling in this implementation uses numeric codes for lookups, so the duplicate two-letter codes do not cause ambiguity in practice."

However, examining ERROR_CODES dict:
- DD appears at codes 10 and 68
- CN appears at codes 17 and 69
- DF appears at codes 25 and 61

The format_error() function uses two_letter code in output, which could be confusing to users seeing "?DD Error" without knowing which of the two DD errors occurred. The documentation claims no ambiguity but doesn't explain how users distinguish between duplicate codes in error messages.

---

#### Code vs Comment conflict


**Description:** Comment says 'Skip arrays for now' but doesn't explain why or when they'll be supported

**Affected files:**
- `src/codegen_backend.py`

**Details:**
In _generate_variable_declarations():
"if var_info.is_array:
    # Skip arrays for now - not supported in initial implementation
    continue"

But the class docstring says:
"Future:
- String support (requires runtime library)
- Arrays
- More complex expressions"

The comment implies arrays are temporarily skipped, but there's no indication of when or how they'll be implemented. The 'Future' list suggests it's planned but provides no timeline or implementation notes.

---

#### code_vs_comment


**Description:** ImmediateExecutor.execute() docstring mentions state names like 'idle', 'paused', 'at_breakpoint', 'done', 'error', 'waiting_for_input', 'running' but these are not actual enum values

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Docstring says: "State names used in documentation (not actual enum values):
- 'idle' - No program loaded (halted=True)
- 'paused' - User hit Ctrl+Q/stop (halted=True)
- 'at_breakpoint' - Hit breakpoint (halted=True)
- 'done' - Program finished (halted=True)
- 'error' - Program encountered error (error_info is not None)
- 'waiting_for_input' - Waiting for INPUT (input_prompt is not None)
- 'running' - Program executing (halted=False) - DO NOT execute immediate mode

Note: The actual implementation checks boolean flags (halted, error_info, input_prompt),
not string state values."

This is technically correct but potentially confusing. The docstring explicitly states these are "not actual enum values" and that the implementation uses boolean flags, so this is more of a documentation style issue than a true inconsistency.

---

#### documentation_inconsistency


**Description:** ImmediateExecutor._show_help() help text claims 'Multi-statement lines (: separator) are fully supported' but this is not demonstrated or validated in the code

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Help text states: "• Multi-statement lines (: separator) are fully supported"

The execute() method builds a program with "0 " + statement and parses it, then executes each statement in line_node.statements. While this suggests multi-statement support should work (since the parser would handle : separators), there's no explicit test or validation that this actually works correctly in immediate mode. This is a minor documentation claim without clear code evidence.

---

#### code_vs_comment


**Description:** Comment says 'add_line expects complete line text with line number' but then constructs the line by concatenating line_num and line_content

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Comment: "# Add/update line - add_line expects complete line text with line number"

Code:
complete_line = f"{line_num} {line_content}"
success, error = ui.program.add_line(line_num, complete_line)

If add_line expects "complete line text with line number", why does it also take line_num as a separate first parameter? This suggests either the comment is wrong about what add_line expects, or the API design is redundant (passing line number twice).

---

#### code_vs_comment


**Description:** OutputCapturingIOHandler.input() docstring says 'INPUT statements are parsed and executed normally, but fail at runtime' but the method immediately raises RuntimeError without any parsing/execution

**Affected files:**
- `src/immediate_executor.py`

**Details:**
Docstring: "Input not supported in immediate mode.

Note: INPUT statements are parsed and executed normally, but fail
at runtime when the interpreter calls this input() method."

Code:
def input(self, prompt=""):
    """Input not supported in immediate mode..."""
    raise RuntimeError("INPUT not allowed in immediate mode")

The docstring's note about "parsed and executed normally" is misleading. The INPUT statement is parsed and the interpreter begins execution, but when it calls this input() method, it immediately fails. The docstring makes it sound like more execution happens than actually does.

---

#### documentation_inconsistency


**Description:** Module docstring mentions 'Implementation note: Uses standard Python type hints (e.g., tuple[str, bool]) which require Python 3.9+' but doesn't specify what the project's minimum Python version is or if this is a problem

**Affected files:**
- `src/input_sanitizer.py`

**Details:**
Docstring: "Implementation note: Uses standard Python type hints (e.g., tuple[str, bool])
which require Python 3.9+. For earlier Python versions, use Tuple[str, bool] from typing."

This note warns about Python 3.9+ requirement but doesn't indicate:
1. What the project's actual minimum Python version is
2. Whether this is acceptable or needs to be changed
3. Whether other files in the project use the older Tuple syntax

This creates uncertainty about whether the code is consistent with project requirements.

---

#### code_vs_comment


**Description:** Module docstring claims 'There is intentional overlap between the two abstractions' for list_files() and delete() but doesn't explain why this design choice was made or if it could cause confusion

**Affected files:**
- `src/filesystem/base.py`

**Details:**
Docstring: "Note: There is intentional overlap between the two abstractions.
Both provide list_files() and delete() methods, but serve different contexts:
FileIO is for interactive commands (FILES/KILL), FileSystemProvider is for
runtime access (though not all BASIC dialects support runtime file operations)."

While the docstring acknowledges the overlap is intentional, it doesn't explain:
1. Why this duplication is necessary/beneficial
2. Whether the implementations should behave identically
3. What happens if they diverge
4. Whether this could cause maintenance issues

This is more of a design documentation gap than a true inconsistency, but it could lead to confusion.

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
3. Partially implemented (silent ignore vs full count prefix support)

The two statements appear contradictory.

---

#### code_vs_comment


**Description:** Comment about readline availability doesn't match actual behavior check

**Affected files:**
- `src/interactive.py`

**Details:**
At line ~30, the code imports readline and sets READLINE_AVAILABLE flag:
try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

The start() method at line ~120 prints a message if readline is not available:
if not READLINE_AVAILABLE:
    print('(Note: readline not available - line editing limited)')

However, the _setup_readline() method at line ~140 is only called if READLINE_AVAILABLE is True, but it imports readline again without checking if it's already imported. This is redundant but not a bug - just inconsistent with the earlier import pattern.

---

#### documentation_inconsistency


**Description:** Module docstring lists commands in inconsistent categories

**Affected files:**
- `src/interactive.py`

**Details:**
The module docstring at line ~1 states:
'Implements the interactive REPL with:
- Line entry and editing
- Direct commands: AUTO, EDIT, HELP (handled specially, not parsed as BASIC statements)
- Immediate mode statements: RUN, LIST, SAVE, LOAD, NEW, MERGE, FILES, SYSTEM, DELETE, RENUM, etc.
  (parsed as BASIC statements and executed in immediate mode)'

However, the execute_command() method at line ~200 shows that AUTO, EDIT, and HELP are handled before parsing, while everything else goes through execute_immediate(). But DELETE and RENUM have their own cmd_delete() and cmd_renum() methods, suggesting they might not be 'parsed as BASIC statements' either. The categorization in the docstring may be oversimplified or outdated.

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

However, the code doesn't explicitly check for or reject drive letter syntax - it just passes the filespec to list_files(). If someone tries 'FILES "A:*.*"', the behavior is undefined (likely an error from list_files, but not explicitly handled).

---

#### code_vs_comment_conflict


**Description:** Comment about Runtime initialization mentions line_text_map purpose but doesn't explain why it's acceptable to omit it

**Affected files:**
- `src/interactive.py`

**Details:**
Comment: 'Pass empty line_text_map since immediate mode uses temporary line 0 (no source line text available for error reporting, but this is fine for immediate mode where the user just typed the statement)'

The justification 'this is fine' is weak - error reporting would actually be better WITH the source text. The real reason might be architectural (Runtime expects a dict of line numbers to text, and line 0 is temporary), but this isn't clearly explained.

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
Comment at lines 669-673 says:
"# OLD EXECUTION METHODS REMOVED (version 1.0.299)
# Note: The project has an internal implementation version (tracked in src/version.py)
# which is separate from the MBASIC 5.21 language version being implemented."

This references src/version.py but that file is not provided in the source code files. The comment mentions version 1.0.299 but doesn't clarify if this is the current version or the version when methods were removed.

---

#### code_vs_comment


**Description:** Comment about NEXT variable processing order may be misleading

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment at lines 1063-1071 says:
"NEXT I, J, K processes variables left-to-right: I first, then J, then K.
For each variable, _execute_next_single() is called to increment it and check if
the loop should continue. If _execute_next_single() returns True (loop continues),
execution jumps back to the FOR body and remaining variables are not processed.
If it returns False (loop finished), that loop is popped and the next variable is processed.

This differs from separate statements (NEXT I: NEXT J: NEXT K) which would
always execute sequentially, processing all three NEXT statements."

The code at lines 1084-1092 shows:
```python
for var_node in var_list:
    var_name = var_node.name + (var_node.type_suffix or "")
    should_continue = self._execute_next_single(var_name, var_node=var_node)
    if should_continue:
        return
```

However, _execute_next_single() at line 1095 has return type documented as:
"Returns:
    True if loop continues (jumped back), False if loop finished"

But looking at the implementation (not shown in this file part), it's unclear if _execute_next_single() actually returns a boolean. The comment assumes it does, but this should be verified.

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


**Description:** Comment in execute_midassignment() states 'start_idx == len(current_value) is considered out of bounds' but this contradicts typical string indexing behavior

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment states: 'Note: start_idx == len(current_value) is considered out of bounds (can't start replacement past end)'

Code implements: if start_idx < 0 or start_idx >= len(current_value): return

This means MID$(A$, LEN(A$)+1, 1) = 'X' does nothing, which is correct for MBASIC 5.21 but the comment's phrasing 'can't start replacement past end' might be clearer as 'can't start replacement at or past end' since start_idx == len is also rejected.

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


**Description:** Backward compatibility comment for print() method says it was renamed to avoid conflicts with Python's built-in, but Python's print is a function not a method, so there's no actual conflict

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Comment says: "This method was renamed from print() to output() to avoid conflicts with Python's built-in print function."

But self.print() as a method doesn't conflict with the built-in print() function - they're in different namespaces. The rename was likely for consistency with IOHandler base class, not to avoid conflicts.

---

#### Code vs Comment conflict


**Description:** get_char() backward compatibility comment claims it preserves non-blocking behavior, but input_char() parameter is ignored in web implementation

**Affected files:**
- `src/iohandler/web_io.py`

**Details:**
Comment says: "The original get_char() implementation was non-blocking, so this preserves that behavior for backward compatibility."

But input_char() docstring says: "NOTE: This parameter is accepted for interface compatibility but is ignored in the web UI implementation." and "Note: Character input not supported in web UI. This method always returns an empty string immediately, regardless of the blocking parameter value."

So get_char() calling input_char(blocking=False) doesn't actually preserve any behavior - the parameter is ignored anyway.

---

#### Documentation inconsistency


**Description:** Inconsistent fallback behavior documentation for Windows without msvcrt

**Affected files:**
- `src/iohandler/console.py`

**Details:**
For input_char(blocking=False), the code warns: "msvcrt not available on Windows - non-blocking input_char() not supported" and returns ""

For input_char(blocking=True), the code warns: "msvcrt not available on Windows - input_char() falling back to input() (waits for Enter, not single character)" and calls input()

The non-blocking case silently fails (returns "") while blocking case falls back to input(). This asymmetry is not explained in the docstring.

---

#### Documentation inconsistency


**Description:** input_line() limitation note is inconsistent across implementations

**Affected files:**
- `src/iohandler/base.py`
- `src/iohandler/console.py`
- `src/iohandler/curses_io.py`
- `src/iohandler/web_io.py`

**Details:**
base.py says: "KNOWN LIMITATION (not a bug - platform limitation): Current implementations (console, curses, web) CANNOT fully preserve leading/trailing spaces"

console.py says: "Note: Current implementation does NOT preserve leading/trailing spaces as documented in base class. Python's input() automatically strips them."

curses_io.py says: "Note: Current implementation does NOT preserve leading/trailing spaces as documented in base class. curses getstr() strips trailing spaces."

web_io.py says: "Note: Current implementation does NOT preserve leading/trailing spaces as documented in base class. HTML input fields strip spaces."

The base.py says Python input() strips trailing newline/spaces, but console.py says it strips them (implying both leading and trailing). The exact stripping behavior differs by platform but documentation is vague.

---

#### Code vs Documentation inconsistency


**Description:** GUIIOHandler docstring example shows incorrect string escaping in docstring

**Affected files:**
- `src/iohandler/gui.py`

**Details:**
Docstring example shows:
    def output(self, text, end='\\n'):
        self.output_widget.append(text + end)

The double backslash \\n in the docstring is meant to show a literal \n in the rendered documentation, but in the actual code signature it should be just '\n'. This could confuse developers copying the example.

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

However, the code at lines 377-382 shows:
"self.advance()
# If there's more after the semicolon (except another colon or newline), it's an error
if not self.at_end_of_line() and not self.match(TokenType.COLON):
    token = self.current()
    raise ParseError(f'Expected : or newline after ;, got {token.type.name}', token)"

The comment says semicolons between statements are NOT valid, but the code allows a trailing semicolon at end of line. This is technically consistent but the phrasing 'NOT valid' is misleading since trailing semicolons ARE allowed.

---

#### code_vs_comment


**Description:** Comment about comma after file number in PRINT statement doesn't match implementation flexibility

**Affected files:**
- `src/parser.py`

**Details:**
Comment at lines 1217-1222 states:
"# Optionally consume comma after file number
# Note: MBASIC 5.21 typically uses comma (PRINT #1, 'text').
# Our parser makes the comma optional for flexibility.
# If semicolon appears instead of comma, it will be treated as an item
# separator in the expression list below (not as a file number separator)."

This suggests the comma is optional, but the actual MBASIC 5.21 behavior may require it. The comment acknowledges 'typically uses comma' but doesn't clarify if this is a deviation from the standard or if MBASIC 5.21 actually allows omitting it.

---

#### documentation_inconsistency


**Description:** Inconsistent terminology for 'end of line' vs 'end of statement' in method names and comments

**Affected files:**
- `src/parser.py`

**Details:**
The parser has two methods:
- at_end_of_line() at line 158: 'Check if at end of logical line (NEWLINE or EOF)'
- at_end_of_statement() at line 169: 'Check if at end of current statement'

The comment at line 163-165 for at_end_of_line() states:
'Note: This method does NOT check for comment tokens (REM, REMARK, APOSTROPHE)
or statement separators (COLON). Use at_end_of_statement() when parsing statements
that should stop at comments/colons.'

However, throughout the code, both methods are used somewhat interchangeably in contexts where the distinction matters. For example, in parse_print() at line 1227, the code uses 'not self.at_end_of_line()' but also checks for COLON and REM tokens separately, suggesting at_end_of_statement() might be more appropriate.

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

This comment suggests the lexer strips the $ and creates a MID token, but it's unclear if the token value contains 'MID' or 'MID$'. The inline comment "represents 'MID$' from source" adds ambiguity. This could confuse developers about what the actual token value is.

---

#### code_vs_comment


**Description:** Incomplete comment about function name normalization

**Affected files:**
- `src/parser.py`

**Details:**
In parse_deffn() method around line 2110:

Comment states: "Function name normalization: All function names are normalized to lowercase with 'fn' prefix (e.g., "FNR" becomes "fnr", "FNA$" becomes "fna$") for consistent lookup. This matches the lexer's identifier normalization and ensures function"

The comment is cut off mid-sentence ("ensures function"). This appears to be truncated documentation that should explain what the normalization ensures (likely "ensures function names are case-insensitive" or similar).

---

#### documentation_inconsistency


**Description:** Comment about MBASIC 5.21 behavior lacks verification context

**Affected files:**
- `src/parser.py`

**Details:**
In parse_dim() method around line 1890:

Comment states: "Dimension expressions: This implementation accepts any expression for array dimensions (e.g., DIM A(X*2, Y+1)), with dimensions evaluated at runtime. This matches MBASIC 5.21 behavior. Note: Some compiled BASICs (e.g., QuickBASIC) may require constants only."

This comment claims to match MBASIC 5.21 behavior but provides no reference or verification. It also mentions QuickBASIC as a contrast, but doesn't clarify if this implementation is specifically targeting MBASIC 5.21 compatibility or a more general BASIC dialect. This could lead to confusion about the intended compatibility target.

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

#### code_vs_comment


**Description:** apply_keyword_case_policy 'preserve' policy documentation says it's 'typically handled at a higher level' but then provides fallback behavior, creating ambiguity about when this code path executes.

**Affected files:**
- `src/position_serializer.py`

**Details:**
Code comment:
'elif policy == "preserve":
    # The "preserve" policy is typically handled at a higher level (keywords passed with
    # original case preserved). If this function is called with "preserve" policy, we
    # return the keyword as-is if already properly cased, or capitalize as a safe default.
    # Note: This fallback shouldn\'t normally execute in correct usage.
    return keyword.capitalize()'

The phrase 'shouldn\'t normally execute in correct usage' suggests this is defensive code for an error condition, but it's not clear if this is a bug or expected fallback.

---

#### documentation_inconsistency


**Description:** renumber_with_spacing_preservation docstring says 'Caller should serialize these LineNodes using serialize_line()' but doesn't specify which serialize_line function (method vs module function).

**Affected files:**
- `src/position_serializer.py`

**Details:**
Docstring:
'Returns:
    Dict of new_line_number -> LineNode (with updated positions)
    Caller should serialize these LineNodes using serialize_line() to regenerate text'

There's both PositionSerializer.serialize_line() (instance method) and serialize_line_with_positions() (module function). The documentation should clarify which to use.

---

#### documentation_inconsistency


**Description:** Inconsistent terminology for string length limits across docstrings and comments

**Affected files:**
- `src/resource_limits.py`

**Details:**
In __init__ docstring: 'Maximum byte length for a string variable (UTF-8 encoded). MBASIC 5.21 limit is 255 bytes.'

In check_string_length() docstring: 'String limits are measured in bytes (UTF-8 encoded), not character count. This matches MBASIC 5.21 behavior which limits string storage size.'

The first says 'byte length' and the second says 'bytes' and 'storage size' - while technically consistent, the terminology varies slightly. Both correctly identify UTF-8 encoding and byte-based measurement.

---

#### code_vs_comment_conflict


**Description:** Comment about DIM A(N) creating N+1 elements appears twice with slightly different context

**Affected files:**
- `src/resource_limits.py`

**Details:**
First occurrence in check_array_allocation():
'# Note: DIM A(N) creates N+1 elements (0 to N) in MBASIC 5.21'
'# This calculation accounts for the MBASIC array sizing convention for limit checking.'

Second occurrence inline:
'total_elements *= (dim_size + 1)  # +1 for 0-based indexing (0 to N)'

The first note says 'MBASIC 5.21' convention, the inline comment says '0-based indexing'. These describe the same behavior but use different terminology. The inline comment's '0-based indexing' is slightly misleading since MBASIC arrays are 0-indexed but the size calculation is about the inclusive range.

---

#### documentation_inconsistency


**Description:** create_unlimited_limits() has inconsistent string length limit documentation

**Affected files:**
- `src/resource_limits.py`

**Details:**
In create_unlimited_limits():
max_string_length=1024*1024,        # 1MB strings (for testing/development - not MBASIC compatible)

This is the only preset that explicitly notes 'not MBASIC compatible' for string length. The other two presets (create_web_limits and create_local_limits) both use 255 bytes with comment '# 255 bytes (MBASIC 5.21 compatibility)' but don't explicitly state they ARE compatible.

The documentation is inconsistent in explicitly stating compatibility vs incompatibility.

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


**Description:** Comment about DIM tracking rationale may not match actual debugger behavior expectations

**Affected files:**
- `src/runtime.py`

**Details:**
Lines 711-719 comment: "# Note: DIM is tracked as both read and write to provide consistent debugger display.
# While DIM is technically allocation/initialization (write-only operation), setting
# last_read to the DIM location ensures that debuggers/inspectors can show 'Last accessed'
# information even for arrays that have never been explicitly read. Without this, an
# unaccessed array would show no last_read info, which could be confusing. The DIM location
# provides useful context about where the array was created."

This justification assumes debuggers would be confused by null last_read, but it's debatable whether DIM should count as a 'read' operation. This creates semantic confusion - DIM is not actually reading the array, it's allocating it. A debugger could show 'Never read' or 'Allocated at line X' instead.

---

#### documentation_inconsistency


**Description:** Inconsistent documentation of _resolve_variable_name() usage context

**Affected files:**
- `src/runtime.py`

**Details:**
Line 163 docstring: "This is the standard method for determining the storage key for a variable,
applying BASIC type resolution rules (explicit suffix > DEF type > default).
For special cases like system variables (ERR%, ERL%), see set_variable_raw()."

But set_variable_raw() (line 437) actually calls set_variable() which internally uses _resolve_variable_name() via split_variable_name_and_suffix(). So set_variable_raw() is not an alternative to _resolve_variable_name(), it's a wrapper that still uses it. The docstring implies they are separate paths.

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

This date (2025-10-25) is in the future relative to typical software development timelines, suggesting either:
1. The date format is incorrect (should be 2024-10-25)
2. This is placeholder documentation
3. The codebase uses a non-standard dating convention

The date should be verified for accuracy.

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

#### code_vs_comment


**Description:** SimpleKeywordCase.__init__ has defensive fallback for invalid policy but doesn't document this behavior

**Affected files:**
- `src/simple_keyword_case.py`

**Details:**
In SimpleKeywordCase.__init__:
if policy not in ["force_lower", "force_upper", "force_capitalize"]:
    # Fallback for invalid/unknown policy values (defensive programming)
    policy = "force_lower"

This fallback behavior is not documented in the docstring. Users passing an invalid policy will silently get force_lower instead of an error, which could hide bugs. The docstring should document this behavior or the code should raise ValueError.

---

#### documentation_inconsistency


**Description:** SettingScope.FILE is defined and partially implemented but no documentation explains its intended use case

**Affected files:**
- `src/settings.py`
- `src/settings_definitions.py`

**Details:**
SettingScope.FILE is defined in settings_definitions.py:
FILE = "file"          # Per-file metadata

And settings.py has infrastructure for it (file_settings dict, set() supports FILE scope), but:
1. No settings are defined with FILE scope in SETTING_DEFINITIONS
2. No documentation explains what 'per-file metadata' means in BASIC context
3. No documentation explains when/how FILE scope would be used
4. The class docstring says it's 'reserved for future use' but doesn't explain the vision

This creates confusion about whether FILE scope is:
- Abandoned/deprecated
- Planned for future
- Available for use but undocumented

---

#### code_vs_comment


**Description:** SettingsManager class docstring mentions FILE scope infrastructure but doesn't explain why it exists if unused

**Affected files:**
- `src/settings.py`

**Details:**
Class docstring states:
'Note: File-level settings infrastructure is partially implemented (file_settings dict, FILE scope support in get/set/reset methods for runtime manipulation), but persistence is not implemented (load() doesn\'t populate it, save() doesn\'t persist it). No settings are defined with FILE scope in settings_definitions.py. This infrastructure is reserved for future use.'

This is good documentation of current state, but doesn't explain:
1. What the future use case is
2. Why the infrastructure was added before it's needed
3. Whether users should avoid using it
4. Whether it's stable API or subject to change

Without this context, users don't know if they can rely on FILE scope or if it might be removed.

---

#### Documentation inconsistency


**Description:** UIBackend docstring mentions 'BatchBackend' and 'headless' execution but then contradicts itself

**Affected files:**
- `src/ui/base.py`

**Details:**
Docstring states: "Future/potential backend types (not yet implemented):
- WebBackend: Browser-based interface
- BatchBackend: Non-interactive execution mode for running programs from command line
             (Note: 'headless' typically means no UI, which seems contradictory to UIBackend purpose;
             batch/non-interactive execution may be better handled outside the UIBackend abstraction)"

This is self-contradictory documentation - it lists BatchBackend as a potential backend type, then immediately questions whether it should be a backend at all.

---

#### Code vs Comment conflict


**Description:** Comment about removeprefix() fallback is misleading

**Affected files:**
- `src/ui/curses_settings_widget.py`

**Details:**
Comment states: "Note: Both removeprefix() and the fallback [6:] only strip from the beginning, ensuring we don't modify 'force_' appearing elsewhere in the string"

This is technically correct but misleading. The [6:] fallback doesn't "ensure" anything - it's just string slicing that happens to work correctly because it only removes the first 6 characters. The comment makes it sound like there's special logic to avoid modifying 'force_' elsewhere, when really it's just the natural behavior of slicing from the start.

---

#### Documentation inconsistency


**Description:** BREAK command documentation says it can be used 'at any time' but doesn't clarify interaction with running programs

**Affected files:**
- `src/ui/cli_debug.py`

**Details:**
cmd_break() docstring: "Breakpoints can be set at any time (before or during execution). They are checked during program execution at each statement. Use RUN to start the program, and it will pause when reaching breakpoints."

This suggests you can set breakpoints while a program is running, but there's no documentation about:
1. How to access the BREAK command while a program is running (programs typically block the REPL)
2. Whether breakpoints set during execution take effect immediately or only on next RUN
3. The interaction between BREAK and STEP commands

---

#### Code vs Comment conflict


**Description:** get_additional_keybindings() docstring says keybindings 'aren't in the JSON file' but some overlap

**Affected files:**
- `src/ui/cli.py`

**Details:**
Function docstring: "Return additional keybindings for CLI that aren't in the JSON file. These are readline keybindings that are handled by Python's readline module, not by the keybinding system."

But the function returns keybindings like "tab_complete" with Tab key, and cli_keybindings.json already documents Tab in the context of line editing. There's potential overlap/confusion about which keybindings are 'additional' vs 'primary'.

---

#### code_vs_comment


**Description:** Comment about target_column default value doesn't match actual column calculation

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In keypress() method comment:
"Note: Methods like _sort_and_position_line use a default target_column of 7,
which assumes typical line numbers (status=1 char + number=5 digits + space=1 char)."

But the calculation '1 + 5 + 1 = 7' assumes fixed 5-digit line numbers. Since line numbers are variable width, the actual code start position varies. For line 10, it would be at column 4 (status=1 + '10'=2 + space=1), not column 7.

---

#### code_vs_comment


**Description:** Comment about line 0 edge case doesn't match actual BASIC line number constraints

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_syntax_errors() method:
"# Note: line_number > 0 check handles edge case of line 0 (if present)"

But BASIC line numbers typically start at 1, and the auto-numbering code uses self.auto_number_start which defaults to 10. Line 0 would be invalid in standard BASIC. The comment suggests line 0 is a valid edge case, but the code doesn't explicitly validate or reject it.

---

#### code_vs_comment


**Description:** Bug fix comment references wrong behavior about next_auto_line_num

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_display() method:
"# DON'T increment counter here - that happens only on Enter
# Bug fix: Incrementing here caused next_auto_line_num to advance prematurely,
# displaying the wrong line number before the user typed anything"

But the code in keypress() for Enter DOES increment next_auto_line_num:
self.next_auto_line_num = next_num + self.auto_number_increment

The comment suggests incrementing in _update_display() was the bug, but doesn't clarify that incrementing DOES happen elsewhere (in keypress). This could be confusing for future maintainers.

---

#### code_vs_comment


**Description:** Comment says ImmediateExecutor is recreated in start() but doesn't explain why it's created twice

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Comment at line ~155 says:
# ImmediateExecutor Lifecycle:
# Created here with temporary IO handler (to ensure attribute exists),
# then recreated in start() with a fresh OutputCapturingIOHandler.

This creates the executor twice - once in __init__ and once in start(). The comment explains WHAT happens but not WHY this double-creation pattern is necessary. The 'to ensure attribute exists' reason is weak since start() is always called before use.

---

#### documentation_inconsistency


**Description:** Inconsistent documentation of unused _create_toolbar method

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
The _create_toolbar() method at line ~230 has a detailed docstring:
"""Create toolbar with common action buttons.

STATUS: UNUSED - not called anywhere in current implementation.

The toolbar was removed from the UI in favor of Ctrl+U menu for better keyboard
navigation. This fully-implemented method is retained for reference in case toolbar
functionality is desired in the future. Can be safely removed if no plans to restore.
"""

This is good documentation of unused code, but the method is fully implemented (50+ lines) and never called. This creates maintenance burden - the method references other methods that could be refactored, breaking this dead code silently.

---

#### code_vs_comment


**Description:** Comment about TAB_KEY behavior doesn't mention cursor redraw side effect

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
The TAB_KEY handler at line ~420 has comment:
# Toggle between editor (position 1) and output (position 2)

But the code also does:
# Force screen redraw to ensure cursor appears in newly focused pane
if self.loop and self.loop_running:
    self.loop.draw_screen()
# Keep the startup status bar message (don't change it)

The comment doesn't mention the forced screen redraw or the status bar preservation, which are important behaviors.

---

#### code_vs_comment


**Description:** Comment about main widget storage strategy is inconsistent with actual implementation

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _activate_menu() comment:
'Main widget storage: Unlike _show_help/_show_keymap/_show_settings which close existing overlays first (and thus can use self.base_widget directly), this method extracts base_widget from self.loop.widget to unwrap any existing overlay.'

But _show_help() does NOT close existing overlays first - it directly uses self.base_widget:
'overlay = urwid.Overlay(
    urwid.AttrMap(help_widget, 'body'),
    self.base_widget,  # Uses self.base_widget directly
    ...'

The comment claims _show_help closes overlays first, but the code shows it just uses self.base_widget directly without any closing logic.

---

#### code_vs_comment


**Description:** Comment about statement-level precision uses inconsistent terminology

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _update_stack_window():
'# Show statement-level precision for GOSUB return address
# return_stmt is statement offset (0-based index): 0 = first statement, 1 = second, etc.'

But later in the same function:
'stmt = entry.get('stmt', 0)'

The comment uses 'return_stmt' but the code uses 'stmt'. While this might be intentional (different keys for different stack entry types), the comment specifically about GOSUB uses 'return_stmt' terminology that doesn't appear in the actual GOSUB formatting code.

---

#### code_vs_comment


**Description:** Comment about overlay closing behavior in _show_help is misleading

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
In _show_help() docstring:
'Help widget closes via ESC/Q keys which call the on_close callback.'

And in the comment block:
'Main widget retrieval: Use self.base_widget (stored at UI creation time in __init__) rather than self.loop.widget (which reflects the current widget and might be a menu or other overlay). This approach works for _show_help, _show_keymap, and _show_settings because these methods close any existing overlays first (via on_close callbacks) before creating new ones, ensuring self.base_widget is the correct base for the new overlay.'

But the code in _show_help() does NOT close existing overlays first - it directly creates a new overlay using self.base_widget. There's no call to any on_close callback or overlay closing logic before creating the help overlay.

---

#### code_vs_comment


**Description:** Comment in cmd_delete and cmd_renum says 'Updates self.program immediately (source of truth), then syncs to runtime' but runtime parameter is passed as None

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Lines ~1605 and ~1625:
Comment: 'Note: Updates self.program immediately (source of truth), then syncs to runtime.'
Code: 'deleted = delete_lines_from_program(self.program, args, runtime=None)'
and: 'old_lines, line_map = renum_program(..., runtime=None)'

The comment claims syncing to runtime, but runtime=None is passed to the helper functions. The actual sync happens via self._sync_program_to_runtime() call after, not within the helper functions.

---

#### code_vs_comment


**Description:** Comment in _on_autosave_recovery_response describes filtering blank lines but implementation details don't match comment clarity

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Lines ~1445-1447:
Comment: '# Filter out blank lines (lines with only line number, no code)'
Code then has complex logic checking 'if code:' and 'elif line.strip():' with different handling.

The comment oversimplifies what the code does - it's not just filtering blank lines, it's also preserving non-numbered lines with content, which isn't mentioned in the comment.

---

#### code_vs_comment


**Description:** Comment in _sync_program_to_runtime says 'This allows LIST and other commands to see the current program without starting execution' but LIST doesn't require runtime sync

**Affected files:**
- `src/ui/curses_ui.py`

**Details:**
Lines ~1177-1180:
Comment: 'Sync program to runtime without resetting PC... This allows LIST and other commands to see the current program without starting execution.'

LIST command (cmd_list) calls _list_program() which only reads from self.editor_lines, not from runtime. The comment suggests LIST needs runtime sync, but it doesn't use runtime at all.

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

#### Code inconsistency


**Description:** Inconsistent handling of missing JSON keys - some use if/else with defaults, others just use defaults

**Affected files:**
- `src/ui/keybindings.py`

**Details:**
Most keybindings use pattern:
_key_from_json = _get_key('editor', 'action')
KEY = _ctrl_key_to_urwid(_key_from_json) if _key_from_json else 'ctrl x'

But some keys like CLEAR_BREAKPOINTS_KEY, DELETE_LINE_KEY, RENUMBER_KEY, INSERT_LINE_KEY, STOP_KEY, SETTINGS_KEY, MAXIMIZE_OUTPUT_KEY are hardcoded without checking JSON at all. This creates inconsistency in which keys can be configured via JSON.

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

#### Code inconsistency


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

This dismiss behavior is a feature of the context menu but isn't mentioned in the module docstring's feature list.

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


**Description:** Comment about Ctrl+I binding location is inconsistent with actual binding

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment in _create_menu (line 424):
'# Note: Ctrl+I is bound directly to editor text widget in start() (not root window)
# to prevent tab key interference - see editor_text.text.bind('<Control-i>', ...)'

Code in start() (line 195):
# Bind Ctrl+I for smart insert line (must be on text widget to prevent tab)
self.editor_text.text.bind('<Control-i>', self._on_ctrl_i)

The comment is accurate, but it's placed in _create_menu() which is called before start(), so the forward reference 'see editor_text.text.bind' is confusing since that code hasn't executed yet when the comment is read.

---

#### documentation_inconsistency


**Description:** Docstring example shows TkIOHandler created without backend but code shows backend parameter

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Docstring (lines 54-61):
'Usage:
    from src.ui.tk_ui import TkBackend, TkIOHandler
    from src.editing.manager import ProgramManager

    io = TkIOHandler()  # TkIOHandler created without backend reference initially
    def_type_map = {}  # Type suffix defaults for variables (DEFINT, DEFSNG, etc.)
    program = ProgramManager(def_type_map)
    backend = TkBackend(io, program)'

Code in start() (line 308):
tk_io = TkIOHandler(self._add_output, self.root, backend=self)

The docstring example shows TkIOHandler() called with no arguments and a comment saying 'created without backend reference initially', but the actual code creates it with three arguments including backend=self. This suggests the usage example is outdated or incorrect.

---

#### code_vs_comment


**Description:** Comment about variable display format doesn't match actual parsing code

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Comment in _on_variable_double_click (lines 1173-1174):
'# Parse variable name and type
# Format examples: "A%", "NAME$", "X", "A%(10x10) [5,3]=42"'

The comment shows format examples including array notation 'A%(10x10) [5,3]=42', but the code immediately after (lines 1175-1181) only checks if 'Array' is in value_display, not if the variable_display contains array notation. This suggests the parsing logic may not match the documented format.

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

If OPTION BASE truly only allows 0 or 1 and this is validated, the else clause should never execute. The comment acknowledges this but the defensive code suggests uncertainty about whether validation is complete.

---

#### code_vs_comment


**Description:** Comment about Tk Text widget design is explanatory but could be clearer

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _remove_blank_lines method around line 1571:
Comment says: "Removes blank lines to keep program clean, but preserves the final\nline. Tk Text widgets always end with a newline character (Tk design -\ntext content ends at last newline, so there's always an empty final line)."

The phrase "text content ends at last newline" is slightly confusing - it could be clearer to say "Tk Text widgets always have a trailing newline, so the final line appears empty".

---

#### code_vs_comment


**Description:** Comment about clearing yellow highlight timing is imprecise

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _on_mouse_click method around line 1560:
Comment says: "# Clear yellow statement highlight when clicking (allows text selection to be visible).\n# The highlight is restored when execution resumes or when stepping to the next statement."

The comment says highlight is restored "when execution resumes" but doesn't specify what happens if execution never resumes (e.g., user just clicks around while paused). The behavior is probably correct but the comment could be more precise about the state machine.

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


**Description:** Comment about preventing default Enter behavior is redundant

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
Multiple locations in _on_enter() end with:
Comment: "return 'break'  # Prevent default Enter behavior"

This comment appears 3+ times in the same function. After the first occurrence, it's redundant since the pattern is established. This is a minor code style issue.

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


**Description:** _on_cursor_move() comment explains scheduling deletion 'after_idle' to avoid event conflicts, but doesn't mention it also prevents issues when the line being deleted is the current line

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
Comment says:
"# Schedule deletion after current event processing to avoid interfering
# with ongoing key/mouse event handling (prevents cursor position issues,
# undo stack corruption, and widget state conflicts during event processing)"

This is accurate but incomplete. When deleting the current line immediately during cursor movement, it can cause the cursor position tracking (self.current_line) to become invalid. The after_idle also prevents this self-reference issue.

---

#### code_vs_comment


**Description:** _on_status_click() uses a simplified regex pattern that differs from _parse_line_number()'s more strict pattern

**Affected files:**
- `src/ui/tk_widgets.py`

**Details:**
_parse_line_number() uses:
match = re.match(r'^(\d+)(?:\s|$)', line_text)

_on_status_click() uses:
match = re.match(r'^\s*(\d+)', line_text)

The _on_status_click() pattern allows leading whitespace (\s*) and doesn't enforce whitespace or end-of-string after the number. This means it could match '10REM' as line 10, while _parse_line_number() would reject it. This inconsistency could cause the status click handler to identify a different line number than the status drawing logic.

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

This comment references a parsing behavior (REMARK -> REM conversion) but doesn't clarify whether the AST will ever contain comment_type='REMARK' or if it's always normalized to 'REM' by the parser. The code only checks for 'APOSTROPHE' vs else (defaulting to REM), suggesting REMARK is already converted, but the comment doesn't make this clear.

---

#### code_vs_documentation


**Description:** cycle_sort_mode() docstring claims to match Tk UI implementation but no verification of actual Tk UI behavior

**Affected files:**
- `src/ui/variable_sorting.py`

**Details:**
Docstring states: "The cycle order is: accessed -> written -> read -> name -> (back to accessed)
This matches the Tk UI implementation."

The comment claims this matches Tk UI but there's no reference to where in the Tk UI this is verified, and no mechanism to ensure they stay in sync if either changes. This is a maintenance risk for consistency.

---

#### code_vs_comment


**Description:** serialize_expression() docstring note about ERR/ERL describes behavior but doesn't explain why they're special

**Affected files:**
- `src/ui/ui_helpers.py`

**Details:**
Docstring note states: "ERR and ERL are special system variables that are serialized without
parentheses (e.g., 'ERR' not 'ERR()') when they appear as FunctionCallNode
with no arguments, matching MBASIC 5.21 syntax."

The note describes the behavior but doesn't explain WHY ERR and ERL are treated specially (they're system variables, not functions, despite appearing as FunctionCallNode in the AST). This could confuse maintainers who might think it's a bug that FunctionCallNode is serialized without parentheses.

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

The docstring mentions it 'Always returns a string, even if internal value is dict or None' but doesn't explain WHY the internal value might be a dict (event args issue) or when this would occur. The inline comment provides more context than the docstring.

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

The comment claims the threshold is 'arbitrary' but then provides specific reasoning for why 5 was chosen. If there's reasoning, it's not arbitrary - it's a heuristic with justification.

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


**Description:** Architecture comment about not auto-syncing editor from AST appears in _execute_immediate but this decision affects multiple methods

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _execute_immediate() method:

Comment says: "# Architecture: We do NOT auto-sync editor from AST after immediate commands.
# This preserves one-way data flow (editor → AST → execution) and prevents
# losing user's formatting/comments. Commands that modify code (like RENUM)
# update the editor text directly."

This architectural decision affects multiple methods (_save_editor_to_program, _load_program_to_editor, etc.) but is only documented in one place. Should be documented at class level or in a central architecture comment.

---

#### code_vs_comment


**Description:** Comment in _serialize_runtime says 'Handles complex objects like AST nodes using pickle' but no pickle usage is visible in the shown code

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _serialize_runtime() method:

Docstring says: "Serialize runtime state.

Handles complex objects like AST nodes using pickle."

The method imports pickle but the shown code only returns a dict with simple data structures (variables, arrays, variable_case_variants). No pickle usage is visible. Either the comment is outdated or the pickle usage is in code not shown.

---

#### code_vs_comment


**Description:** Comment in _on_enter_key says method is called by _on_editor_change but the method body is empty/pass

**Affected files:**
- `src/ui/web/nicegui_backend.py`

**Details:**
In _on_enter_key() method:

Docstring says: "Handle Enter key press in editor - triggers auto-numbering.

Note: This method is called internally by _on_editor_change when a new line
is detected. The actual auto-numbering logic is in _add_next_line_number."

But the method body only contains a comment and pass statement. If the method does nothing, why does it exist? Either it should be removed or the comment should explain why it's a placeholder.

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


**Description:** Session state tracks find/replace state but no documentation exists for find/replace feature

**Affected files:**
- `src/ui/web/session_state.py`
- `docs/help/common/debugging.md`

**Details:**
session_state.py includes:
last_find_text: str = ""
last_find_position: int = 0
last_case_sensitive: bool = False

This suggests a find/replace feature exists in the web UI, but:
- editor-commands.md doesn't mention find/replace
- debugging.md doesn't mention it
- No help documentation for this feature exists

Users need documentation on how to use find/replace functionality.

---

#### code_comment_conflict


**Description:** Comment says class is deprecated but provides migration guide suggesting it's still in use

**Affected files:**
- `src/ui/web_help_launcher.py`

**Details:**
Comment states:
# Legacy class kept for compatibility - new code should use direct web URL instead
# The help site is already built and served at http://localhost/mbasic_docs
#
# Migration guide for code using this class:
# OLD: launcher = WebHelpLauncher(); launcher.open_help("statements/print")
# NEW: Open http://localhost/mbasic_docs/statements/print.html directly in browser

But then the class WebHelpLauncher_DEPRECATED is fully implemented with methods like _build_help(), _start_help_server(), etc.

If it's truly deprecated and shouldn't be used, why provide a full implementation? If code still uses it, it's not really deprecated. This needs clarification.

---

#### code_vs_documentation


**Description:** Keybindings JSON shows F5 for both 'run' and 'continue' which could be confusing

**Affected files:**
- `src/ui/web_keybindings.json`
- `docs/help/common/debugging.md`

**Details:**
web_keybindings.json shows:
"run": {"keys": ["Ctrl+R", "F5"]}
"continue": {"keys": ["F5"]}

F5 is listed for both run and continue. The documentation should clarify:
- Does F5 run when stopped and continue when paused?
- Is this context-dependent?
- Could this cause confusion?

debugging.md mentions both commands but doesn't explain the F5 dual-purpose behavior.

---

#### documentation_inconsistency


**Description:** Inconsistent code block formatting - some use 'basic' language tag, some don't

**Affected files:**
- `docs/help/common/examples/loops.md`
- `docs/help/common/examples/hello-world.md`

**Details:**
hello-world.md uses:
```basic
10 PRINT "Hello, World!"
```

But loops.md uses:
```
10 FOR I = 1 TO 10
```

Inconsistent markdown code block language tags. Should standardize on either 'basic' or no language tag throughout all examples.

---

#### documentation_inconsistency


**Description:** Compiler documentation exists but version.py shows this is an interpreter, not a compiler

**Affected files:**
- `docs/help/common/compiler/index.md`
- `docs/help/common/compiler/optimizations.md`

**Details:**
compiler/index.md and optimizations.md document 27 compiler optimizations in detail.

But version.py shows:
PROJECT_NAME = "MBASIC-2025"
MBASIC_VERSION = "5.21"  # The MBASIC version we implement
COMPATIBILITY = "100% MBASIC 5.21 compatible with optional extensions"

MBASIC 5.21 was an interpreter, not a compiler. The documentation should clarify:
- Is this a future compiler feature?
- Is this documentation for a planned compiler?
- Why document compiler features for an interpreter?

optimizations.md even states: 'Status: In Progress' and 'actual code transformations will be applied during code generation (currently in development)'

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


**Description:** Missing cross-reference to error handling statements

**Affected files:**
- `docs/help/common/language/appendices/index.md`
- `docs/help/common/language/appendices/error-codes.md`

**Details:**
index.md says 'Error handling references (see [Error Handling](../statements/index.md#error-handling) for detailed examples)' but error-codes.md has a 'See Also' section that links to individual error handling statements rather than the index. Both approaches are valid but inconsistent in style.

---

#### documentation_inconsistency


**Description:** Incomplete keyboard shortcut table

**Affected files:**
- `docs/help/common/index.md`

**Details:**
The Quick Start table shows keyboard shortcuts using template syntax like {{kbd:run:cli}} but doesn't explain what these templates mean or how they're rendered. Users seeing the raw documentation might be confused by this syntax.

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

RIGHT$ example has extra spaces in the code:
```basic
10 A$="DISK BASIC-80"
 20 PRINT RIGHT$(A$,8)
 RUN
 BASIC-80
 Ok
```
(Note the leading space before line 20 and the output lines)

MID$ example uses different variable names and structure.

These could be more consistently formatted.

---

#### documentation_inconsistency


**Description:** Inconsistent error documentation for zero offset parameter

**Affected files:**
- `docs/help/common/language/functions/instr.md`
- `docs/help/common/language/functions/mid_dollar.md`

**Details:**
Both INSTR and MID$ document that using 0 for the position parameter causes an error, but with different formatting:

INSTR: 'Note: If I=0 is specified, an "Illegal function call" error will occur.'

MID$: 'Note: If I=0 is specified, an "Illegal function call" error will occur.'

These are actually identical, but INSTR places this note after the example while MID$ places it after the example as well. The placement is consistent, so this is actually not an inconsistency - false alarm on my part.

---

#### documentation_inconsistency


**Description:** SPACE$ references STRING$ but not vice versa

**Affected files:**
- `docs/help/common/language/functions/space_dollar.md`
- `docs/help/common/language/functions/string_dollar.md`

**Details:**
In space_dollar.md, the description says: 'This is equivalent to STRING$(I, 32) since 32 is the ASCII code for a space character.'

However, string_dollar.md does not mention SPACE$ as a related function or special case. The cross-reference is one-way only.

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


**Description:** Inconsistent formatting of 'Remarks' section - some use heading, some don't

**Affected files:**
- `docs/help/common/language/statements/auto.md`
- `docs/help/common/language/statements/chain.md`

**Details:**
auto.md has '## Remarks' as a heading
chain.md has '## Remarks' as a heading

But the content structure varies - some have subsections (like chain.md with '### Parameters:', '### Variable Passing:', '### Memory:') while others (like auto.md) have plain paragraph text. This inconsistency in documentation structure makes it harder to scan.

---

#### documentation_inconsistency


**Description:** CLOAD and CSAVE documentation note they are 'not included in all implementations' but don't specify which implementations include them

**Affected files:**
- `docs/help/common/language/statements/cload.md`
- `docs/help/common/language/statements/csave.md`

**Details:**
Both documents state:
'NOTE: CLOAD and CSAVE are not included in all implementations of BASIC.'

But the version information at the top says:
'Versions: 8K (cassette), Extended (cassette)'
'Note: This command is not included in the DEC VT180 version or modern disk-based systems.'

The 'NOTE' at the bottom is redundant and less specific than the version information already provided.

---

#### documentation_inconsistency


**Description:** CLS documentation states it works 'in all UI backends' but doesn't define what UI backends exist

**Affected files:**
- `docs/help/common/language/statements/cls.md`

**Details:**
The documentation states:
'Note: CLS is implemented in MBASIC and works in all UI backends.'

However, there's no reference to what UI backends are available or where to find more information about them. This leaves the reader unclear about what 'all UI backends' means.

---

#### documentation_inconsistency


**Description:** CONT example references another section but doesn't provide the actual example

**Affected files:**
- `docs/help/common/language/statements/cont.md`

**Details:**
The Example section states:
'See example Section 2.61, STOP.'

This is a reference to the original manual's section numbering, which doesn't exist in this documentation structure. The example should either be included or the reference should point to the actual STOP documentation file.

---

#### documentation_inconsistency


**Description:** Operators documentation mentions 'Type Conversion Functions' in See Also but doesn't link to a specific page

**Affected files:**
- `docs/help/common/language/operators.md`

**Details:**
The See Also section includes:
'- [Type Conversion Functions](functions/index.md#type-conversion-functions)'

This links to an anchor (#type-conversion-functions) that may or may not exist in the functions/index.md file. Without seeing that file, we can't verify if this anchor exists or if the link will work.

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


**Description:** Inconsistent spacing guidance in syntax examples

**Affected files:**
- `docs/help/common/language/statements/def-fn.md`

**Details:**
def-fn.md shows multiple 'Alternative forms (all valid)' with different spacing, then under 'Spacing' section states 'Space after FN is optional. Both styles are valid' and gives examples. However, the 'Alternative forms' section at the top already shows this, creating redundancy. Additionally, Example 6 comment says 'First call: Y=5, A=10, result = 15' but 5+10=15 is correct, and 'Second call: Y=5, A=20, result = 25' where 5+20=25 is correct, so the examples are accurate.

---

#### documentation_inconsistency


**Description:** LINE INPUT# documentation has inconsistent keyword list

**Affected files:**
- `docs/help/common/language/statements/inputi.md`

**Details:**
The keywords list includes 'inputi' which is the filename, not a BASIC keyword:
keywords: ['close', 'command', 'data', 'field', 'file', 'for', 'if', 'input', 'inputi', 'line']

'inputi' should not be in the keywords list as it's not a valid BASIC statement or keyword.

---

#### documentation_inconsistency


**Description:** LPRINT documentation references non-existent printi-printi-using.md for PRINT#

**Affected files:**
- `docs/help/common/language/statements/lprint-lprint-using.md`

**Details:**
In lprint-lprint-using.md 'See Also' section:
- [PRINT#](printi-printi-using.md) - To write data to a sequential disk file

This creates a circular reference since the current file IS printi-printi-using.md. The reference should point to itself or be removed.

---

#### documentation_inconsistency


**Description:** Inconsistent spacing in 'See Also' references

**Affected files:**
- `docs/help/common/language/statements/list.md`
- `docs/help/common/language/statements/llist.md`

**Details:**
In list.md:
- [AUTO](auto.md) - To generate a line number   automatically     after every carriage return

In llist.md:
- [AUTO](auto.md) - To generate a line number   automatically     after every carriage return

Both have excessive spacing between 'number' and 'automatically' and between 'automatically' and 'after'. This appears to be a formatting error.

---

#### documentation_inconsistency


**Description:** MERGE documentation has inconsistent spacing in title

**Affected files:**
- `docs/help/common/language/statements/merge.md`

**Details:**
The description field has extra spaces:
"To merge a specified disk file into the      program currently in memory"

Should be:
"To merge a specified disk file into the program currently in memory"

---

#### documentation_inconsistency


**Description:** PRINT documentation has inconsistent alias format

**Affected files:**
- `docs/help/common/language/statements/print.md`

**Details:**
The print.md file has:
aliases: ['?']

But the syntax section shows:
"? - Shorthand for PRINT"

The alias is documented but not clearly indicated in the main syntax section. The syntax should show both forms:
"PRINT [<list of expressions>]
? [<list of expressions>]"

---

#### documentation_inconsistency


**Description:** PUT documentation references PRINT# and WRITE# without clear context

**Affected files:**
- `docs/help/common/language/statements/put.md`

**Details:**
The note in put.md states:
"PRINT#, PRINT# USING, and WRITE# may be used to put characters in the random file buffer before a PUT statement."

This is confusing because PUT is for random files, but PRINT# is typically for sequential files. The note should clarify that this is a special case or advanced usage, or explain the context more clearly.

---

#### documentation_inconsistency


**Description:** Similar command names (RESTORE vs RESUME) could cause confusion but no explicit cross-reference warning exists

**Affected files:**
- `docs/help/common/language/statements/restore.md`
- `docs/help/common/language/statements/resume.md`

**Details:**
RESTORE resets DATA pointer, RESUME continues after error. These are completely different commands with similar names but no warning exists like the RESET/RSET pair has.

---

#### documentation_inconsistency


**Description:** WAIT statement marked as not implemented but documentation preserved

**Affected files:**
- `docs/help/common/language/statements/wait.md`

**Details:**
Implementation note clearly states: 'Not Implemented: This feature requires direct hardware I/O port access and is not implemented in this Python-based interpreter. Behavior: Statement is parsed but no operation is performed'

This is well-documented but should be consistent with how WIDTH is documented (both are no-ops/not implemented).

---

#### documentation_inconsistency


**Description:** Keyboard shortcuts use template syntax {{kbd:...}} that may not render correctly in all contexts

**Affected files:**
- `docs/help/common/shortcuts.md`

**Details:**
The shortcuts.md file uses syntax like '{{kbd:run:cli}}' which appears to be a template placeholder. The documentation should clarify if this is meant to be processed by a template engine or if it's the actual display format.

---

#### documentation_inconsistency


**Description:** RESUME documentation includes extensive testing verification note that other commands lack

**Affected files:**
- `docs/help/common/language/statements/resume.md`

**Details:**
resume.md includes: 'Testing RESUME

Verified behavior against real MBASIC 5.21:
- ✅ RESUME retries error line
- ✅ RESUME NEXT skips to next statement
...'.

This level of verification detail is not present in other command documentation. Should this be standardized across all commands or removed for consistency?

---

#### documentation_inconsistency


**Description:** Inconsistent description of MERGE command availability

**Affected files:**
- `docs/help/common/ui/cli/index.md`
- `docs/help/common/ui/tk/index.md`

**Details:**
CLI docs list 'MERGE "addon.bas"' as a file operation command, but Tk docs don't mention MERGE at all in the File Menu or file operations sections. This suggests either:
1. MERGE is CLI-only
2. MERGE is available in Tk but undocumented
3. The feature availability differs by UI

---

#### documentation_inconsistency


**Description:** Inconsistent description of immediate/direct mode

**Affected files:**
- `docs/help/common/ui/curses/editing.md`
- `docs/help/common/ui/tk/index.md`

**Details:**
Curses docs call it 'Direct Mode' while Tk docs call it 'Immediate Mode Panel'. Both describe the same feature (executing commands without line numbers), but the terminology differs. The CLI docs use 'Direct Mode' matching Curses.

---

#### documentation_inconsistency


**Description:** Incomplete information about semantic analyzer usage

**Affected files:**
- `docs/help/mbasic/architecture.md`

**Details:**
Architecture.md shows how to run analyze_program.py but doesn't specify the full path or whether it's in the repository. Users may not know where to find this tool or if it's included in the distribution.

---

#### documentation_inconsistency


**Description:** Inconsistent function count - features.md says '50+' but not-implemented.md implies different count

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
features.md states: 'Functions (50+)' and lists categories of functions.

not-implemented.md has a 'String Enhancements' section listing functions from 'Later BASIC' that aren't in MBASIC 5.21, but doesn't provide a definitive count of what IS available.

The '50+' claim should be verifiable against the actual function list, but no comprehensive enumeration is provided in either document.

---

#### documentation_inconsistency


**Description:** CLS implementation status unclear

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/not-implemented.md`

**Details:**
features.md does not explicitly list CLS in the 'Program Control' or 'Input/Output' sections.

not-implemented.md states: 'Note: Basic CLS (clear screen) IS implemented in MBASIC - see [CLS](../common/language/statements/cls.md). The GW-BASIC extended CLS with optional parameters is not implemented.'

This creates confusion - CLS should be listed in features.md if it's implemented, but it's only mentioned in the 'not-implemented' document as a clarification.

---

#### documentation_inconsistency


**Description:** Semantic analyzer optimization count mismatch in same document

**Affected files:**
- `docs/help/mbasic/features.md`

**Details:**
features.md states: 'The interpreter includes an advanced semantic analyzer with 18 optimizations:' and then lists exactly 18 numbered items (1-18).

This is internally consistent, but should be verified against actual implementation to ensure all 18 are truly implemented.

---

#### documentation_inconsistency


**Description:** LPRINT behavior documentation inconsistency

**Affected files:**
- `docs/help/mbasic/features.md`
- `docs/help/mbasic/getting-started.md`

**Details:**
features.md states: 'LPRINT - Line printer output (Note: Statement is parsed but produces no output - see [LPRINT](../common/language/statements/lprint-lprint-using.md) for details)'

getting-started.md doesn't mention LPRINT at all in its examples or quick reference.

This is a significant behavior difference (parsed but no output) that should be highlighted more prominently, especially in getting-started.md where users might try to use it.

---

#### documentation_inconsistency


**Description:** Settings file location may be incomplete

**Affected files:**
- `docs/help/ui/cli/settings.md`

**Details:**
cli/settings.md states: 'Settings file location:\n- Linux/Mac: ~/.mbasic/settings.json\n- Windows: %APPDATA%\mbasic\settings.json'

This doesn't account for WSL (Windows Subsystem for Linux) which is listed as a tested platform in features.md. WSL users would likely use the Linux path, but this should be explicitly stated.

---

#### documentation_inconsistency


**Description:** Web UI limitations incomplete

**Affected files:**
- `docs/help/mbasic/features.md`

**Details:**
features.md lists Web UI limitations: '50 file limit maximum\n1MB per file maximum\nNo path support (simple filenames only)\nNo persistent storage across sessions'

But doesn't mention whether Web UI supports all debugging features (breakpoints, step, stack) that are listed as 'available in all UIs' earlier in the document. The note says 'Basic debugging - Simple breakpoint support via menu' which contradicts 'available in all UIs'.

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


**Description:** Inconsistent explanation of Save keyboard shortcut

**Affected files:**
- `docs/help/ui/curses/files.md`
- `docs/help/ui/curses/quick-reference.md`

**Details:**
docs/help/ui/curses/files.md states: '1. Press **{{kbd:save:curses}}** to save (Ctrl+S unavailable - terminal flow control)'

But docs/help/ui/curses/quick-reference.md states: '**{{kbd:save:curses}}** | Save program (Ctrl+S unavailable - terminal flow control)'

Both mention Ctrl+S is unavailable, but neither explains what {{kbd:save:curses}} actually resolves to. The feature-reference.md clarifies: 'Note: Uses {{kbd:save:curses}} because {{kbd:save:curses}} is reserved for terminal flow control.' but this still doesn't tell users what key to actually press.

---

#### documentation_inconsistency


**Description:** Inconsistent information about Variables Window availability across UIs

**Affected files:**
- `docs/help/ui/curses/variables.md`
- `docs/help/ui/index.md`

**Details:**
docs/help/ui/curses/variables.md under 'Comparison with Other UIs' shows:
'| Feature | Curses | CLI | Tk | Web |
|---------|--------|-----|-----|-----|
| Visual window | ✅ | ❌ | ✅ | ✅ |'

But docs/help/ui/index.md under 'Comparison' shows:
'| Feature | Curses | CLI | Tkinter | Web |
|---------|--------|-----|---------|-----|
| Variables Window | ✓ | ✗ | ✓ | ✓ |'

These tables use different symbols (✅/❌ vs ✓/✗) for the same information, which is inconsistent formatting.

---

#### documentation_inconsistency


**Description:** Inconsistent information about List Program access method

**Affected files:**
- `docs/help/ui/curses/quick-reference.md`
- `docs/help/ui/curses/feature-reference.md`

**Details:**
docs/help/ui/curses/quick-reference.md under 'Program Management' states: '**Menu only** | List program'

But docs/help/ui/curses/feature-reference.md states: '### List Program (Menu only)
Display the program listing in the editor. Access through the menu bar.'

Both say menu-only, but docs/help/ui/curses/running.md says: 'Access through the menu bar to list the program to the output window.'

This suggests LIST outputs to the output window, not the editor as feature-reference states.

---

#### documentation_inconsistency


**Description:** Inconsistent feature count claims

**Affected files:**
- `docs/help/ui/tk/feature-reference.md`
- `docs/help/ui/tk/features.md`

**Details:**
feature-reference.md claims specific feature counts:
- File Operations (8 features)
- Execution & Control (6 features)
- Debugging (6 features)
- Variable Inspection (6 features)
- Editor Features (7 features)
- Help System (4 features)

Total: 37 features claimed

But features.md only highlights a subset without claiming completeness. The relationship between 'Essential Features' and 'Complete Feature Reference' is unclear.

---

#### documentation_inconsistency


**Description:** Inconsistent command line examples

**Affected files:**
- `docs/help/ui/tk/index.md`
- `docs/help/ui/tk/getting-started.md`

**Details:**
index.md shows:
'mbasic --ui tk [filename.bas]'

getting-started.md shows:
'mbasic --ui tk [filename.bas]'
Or to use the default curses UI:
'mbasic [filename.bas]'

The second document provides more context about the default UI, which would be helpful in index.md as well for consistency.

---

#### documentation_inconsistency


**Description:** Incomplete keyboard shortcut information for debugging

**Affected files:**
- `docs/help/ui/tk/features.md`

**Details:**
features.md states:
'**Debug with:**
- {{kbd:step_statement}} - Execute next statement
- {{kbd:step_line}} - Execute next line
- {{kbd:continue_execution}} - Continue to next breakpoint'

But feature-reference.md states that Step Statement and Continue have 'No keyboard shortcut' and only toolbar buttons. The macro names used ({{kbd:step_statement}}, {{kbd:continue_execution}}) suggest shortcuts exist, creating confusion.

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
Most library category pages use 'How to Use' as the section header, but the content is identical. However, ham_radio/index.md has:
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
The document uses both 'toolbar button' and 'toolbar buttons' when referring to Step/Stmt/Cont/Stop controls. In the 'Essential Keyboard Shortcuts' table, it says 'Step, Continue, and Stop are available via toolbar buttons'. Later in 'Mid-Line Statement Stepping' it says 'Click the **Stmt** toolbar button' and 'Click the **Step** toolbar button'. The exact names and whether 'Stmt' is a separate button from 'Step' could be clearer.

---

#### documentation_inconsistency


**Description:** Redundant installation documentation files

**Affected files:**
- `docs/user/README.md`
- `docs/user/INSTALLATION.md`

**Details:**
INSTALLATION.md exists as a redirect file stating 'This is a redirect file. For complete installation instructions, see INSTALL.md'. README.md lists both 'INSTALL.md' and 'INSTALLATION.md' under 'Getting Started'. This redundancy could confuse users about which file to read, though the redirect does clarify the relationship.

---

#### documentation_inconsistency


**Description:** Inconsistent capitalization of UI name

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
The document title uses 'Tk UI' but the text sometimes refers to 'TK UI' (all caps) and sometimes 'Tk UI' (mixed case). Examples: 'MBASIC Tk UI - Quick Start Guide' (title), 'The Tk UI is the default' (text), 'TK UI' in '{{kbd:toggle_variables}} in TK UI'. Should be consistent throughout.

---

#### documentation_inconsistency


**Description:** Keyboard shortcut template notation without definition

**Affected files:**
- `docs/user/QUICK_REFERENCE.md`

**Details:**
QUICK_REFERENCE.md uses {{kbd:...}} notation extensively (e.g., '{{kbd:new}}', '{{kbd:open}}', '{{kbd:save}}') but never explains what this notation means or how it maps to actual keys. Users seeing this document might not understand these are placeholders for actual keyboard shortcuts.

---

#### documentation_inconsistency


**Description:** Execution Stack Window keyboard shortcut inconsistency

**Affected files:**
- `docs/user/TK_UI_QUICK_START.md`

**Details:**
The document shows '{{kbd:toggle_stack}}' as the keyboard shortcut to toggle the Execution Stack Window in multiple places, but in the 'Essential Keyboard Shortcuts' table, it's listed as '**{{kbd:toggle_stack}}** | Show/hide Execution Stack Window'. The actual key binding is never revealed (it's a template placeholder), making it unclear what key the user should actually press.

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

- Total issues found: 667
- Code/Comment conflicts: 233
- Other inconsistencies: 434


## Summary

- Total issues in filtered report: 432
- Issues filtered out (already reviewed): 2
- Original total: 434

Filtered on: 2025-11-09 14:22:54
