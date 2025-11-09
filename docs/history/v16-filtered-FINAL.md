# Enhanced Consistency Report (Code + Documentation)

Generated: 2025-11-09 13:49:51
Analyzed: Source code (.py, .json) and Documentation (.md)

**Note:** This report has been filtered to remove 209 previously reviewed/ignored issues. Original report had 434 total issues.

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


**Description:** Module docstring references SimpleKeywordCase in src/simple_keyword_case.py but this file is not provided in the source code files

**Affected files:**
- `src/keyword_case_manager.py`

**Details:**
Module docstring says: "For simpler force-based policies in the lexer, see SimpleKeywordCase (src/simple_keyword_case.py) which only supports force_lower, force_upper, and force_capitalize."

But src/simple_keyword_case.py is not included in the provided source files, making this reference unverifiable and potentially broken.

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


**Description:** Incomplete ASCII reference in character-set.md

**Affected files:**
- `docs/help/common/language/character-set.md`
- `docs/help/common/language/appendices/ascii-codes.md`

**Details:**
character-set.md provides a brief 'Control Characters' table with only 7 entries (BEL, BS, TAB, LF, CR, ESC) and says 'Use CHR$() to include control characters in strings.' However, it references ascii-codes.md for complete reference. The ascii-codes.md has a full table of all 32 control characters (0-31). This is not necessarily an inconsistency but character-set.md could be clearer that it's showing only commonly used control characters.

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


**Description:** Contradictory information about tkinter installation

**Affected files:**
- `docs/user/INSTALL.md`

**Details:**
Under 'System Package Requirements', the document states tkinter is 'OPTIONAL for Tkinter GUI Backend' and 'Only needed if you want to use the Tkinter GUI backend'. However, under 'Python Package Dependencies' it says 'Tk mode: Requires tkinter (usually pre-installed with Python)'. Later under 'Method 2: Direct Installation' it says 'For other UIs (Curses, Tk, Web), you'll need to install their dependencies via pip install -r requirements.txt'. This is contradictory - tkinter is a system package (python3-tk), not a pip package, and wouldn't be in requirements.txt.

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


**Description:** Comment in execute_midassignment() states 'start_idx == len(current_value) is considered out of bounds' but this contradicts typical string indexing behavior

**Affected files:**
- `src/interpreter.py`

**Details:**
Comment states: 'Note: start_idx == len(current_value) is considered out of bounds (can't start replacement past end)'

Code implements: if start_idx < 0 or start_idx >= len(current_value): return

This means MID$(A$, LEN(A$)+1, 1) = 'X' does nothing, which is correct for MBASIC 5.21 but the comment's phrasing 'can't start replacement past end' might be clearer as 'can't start replacement at or past end' since start_idx == len is also rejected.

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


**Description:** Comment about Tk Text widget design is explanatory but could be clearer

**Affected files:**
- `src/ui/tk_ui.py`

**Details:**
In _remove_blank_lines method around line 1571:
Comment says: "Removes blank lines to keep program clean, but preserves the final\nline. Tk Text widgets always end with a newline character (Tk design -\ntext content ends at last newline, so there's always an empty final line)."

The phrase "text content ends at last newline" is slightly confusing - it could be clearer to say "Tk Text widgets always have a trailing newline, so the final line appears empty".

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


## Summary

- Total issues in filtered report: 225
- Issues filtered out (already reviewed): 209
- Original total: 434

Filtered on: 2025-11-09 14:31:59
