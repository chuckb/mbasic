# Documentation Inconsistencies Report

Generated: 2025-11-03 14:38:39
Scanned directories: help, library, stylesheets, user

Found 126 inconsistencies:

## 🔴 High Severity

### syntax_inconsistency

**Description:** Syntax section shows 'ASS (X)' instead of 'ABS(X)' - appears to be a typo

**Affected files:**
- `help/common/language/functions/abs.md`

**Details:**
In abs.md, the syntax is listed as 'ASS (X)' but the function name is ABS throughout the rest of the document and all other references

---

### contradictory_information

**Description:** DEF FN documentation contradicts itself about function name length

**Affected files:**
- `help/common/language/statements/def-fn.md`

**Details:**
The documentation states 'Can be one or more characters' and provides examples like FNAREA, FNUCASE$, FNDIST, but also shows examples with single-character names like FNA, FND, FNX. The 'Syntax Notes' section emphasizes multi-character support but doesn't clarify if this is version-dependent. The original MBASIC 5.21 typically only supported single-character function names after FN.

---

### contradictory_information

**Description:** RESUME and RESTORE statements have conflicting 'related' metadata

**Affected files:**
- `help/common/language/statements/resume.md`
- `help/common/language/statements/restore.md`

**Details:**
RESUME.md lists 'related: [error, on-error-goto]' but links to ERROR and ON ERROR GOTO in See Also. RESTORE.md lists 'related: [read, data]' and links match. However, RESUME.md's See Also section includes links to ERROR and ON ERROR GOTO statements, but these don't appear to have corresponding documentation files based on the naming pattern used elsewhere.

---

### contradictory_information

**Description:** Testing reference claims verification but no test files provided

**Affected files:**
- `help/common/language/statements/resume.md`

**Details:**
RESUME.md states 'Test file: `tests/test_resume.bas`, `tests/test_resume2.bas`, `tests/test_resume3.bas`' and claims 'Verified behavior against real MBASIC 5.21' with checkmarks, but these test files are not included in the provided documentation set.

---

### broken_reference

**Description:** Reference to non-existent running.md file

**Affected files:**
- `help/common/ui/curses/editing.md`

**Details:**
The 'See Also' section references '../../../ui/curses/running.md' but this file is not included in the provided documentation set. The correct path should likely be '../../ui/curses/running.md' or the file is missing.

---

### feature_availability_conflict

**Description:** Debugging features availability inconsistency

**Affected files:**
- `help/mbasic/extensions.md`
- `help/mbasic/features.md`

**Details:**
extensions.md states debugging commands (BREAK, STEP, STACK) are 'CLI Only' and exclusive to CLI backend. However, features.md under 'Debugging' section lists 'Breakpoints', 'Step execution', 'Variable watch', and 'Stack viewer' as '(UI-dependent)' suggesting they work in multiple UIs. Additionally, features.md under 'Curses UI' lists 'Variables window (Ctrl+W)' and 'Stack window (Ctrl+K)' which contradicts the CLI-only claim.

---

### contradictory_information

**Description:** File system handling inconsistency for Tk UI

**Affected files:**
- `help/mbasic/compatibility.md`
- `help/common/ui/tk/index.md`

**Details:**
compatibility.md states 'CLI, Tk, and Curses UIs - Real filesystem access' and shows examples of Tk using real paths. However, tk/index.md under 'File Operations' only shows basic Save/Open dialogs without mentioning path support or the filesystem access capabilities described in compatibility.md.

---

### command_inconsistency

**Description:** Ctrl+L shortcut conflict - assigned to both 'List Program' and 'Step Line'

**Affected files:**
- `help/ui/cli/debugging.md`
- `help/ui/curses/feature-reference.md`

**Details:**
In cli/debugging.md, no Ctrl+L is mentioned for CLI. In curses/feature-reference.md, 'List Program (Ctrl+L)' is listed under Execution & Control, but 'Step Line (Ctrl+L when paused)' is listed under Debugging. The same shortcut cannot perform two different actions.

---

### command_inconsistency

**Description:** Ctrl+X shortcut conflict - assigned to both 'Stop/Interrupt' in Curses and 'Cut' operation

**Affected files:**
- `help/ui/cli/debugging.md`
- `help/ui/curses/feature-reference.md`

**Details:**
In curses/feature-reference.md, 'Stop/Interrupt (Ctrl+X)' is listed under Execution & Control, but under Editor Features it states 'Cut: Ctrl+X'. The same shortcut cannot perform two different actions.

---

### keyboard_shortcut_inconsistency

**Description:** Conflicting keyboard shortcuts for loading/opening files

**Affected files:**
- `help/ui/curses/files.md`
- `help/ui/curses/quick-reference.md`

**Details:**
files.md states 'Press **b** or **Ctrl+O**' for loading programs, but quick-reference.md only lists 'Ctrl+O' for Open/Load program. The 'b' key is not mentioned in the quick reference.

---

### keyboard_shortcut_inconsistency

**Description:** Conflicting keyboard shortcuts for saving files

**Affected files:**
- `help/ui/curses/files.md`
- `help/ui/curses/quick-reference.md`

**Details:**
files.md states 'Press **F5** or **Ctrl+S**' for saving, but quick-reference.md shows F5 is mapped to Save ({{kbd:save}}) while Ctrl+S is not mentioned. This creates confusion about which key does what.

---

### keyboard_shortcut_inconsistency

**Description:** Conflicting keyboard shortcuts for running programs

**Affected files:**
- `help/ui/curses/running.md`
- `help/ui/curses/quick-reference.md`

**Details:**
running.md states 'Press **F2** or **Ctrl+R**' to run, but quick-reference.md only shows '{{kbd:run}}' (Ctrl+R) for running programs. F2 is not mentioned in the quick reference.

---

### keyboard_shortcut_inconsistency

**Description:** Conflicting keyboard shortcuts for listing programs

**Affected files:**
- `help/ui/curses/running.md`
- `help/ui/curses/quick-reference.md`

**Details:**
running.md states 'Press **F3** or **Ctrl+L**' to list programs, but quick-reference.md shows Ctrl+L as 'List program (or Step Line when debugging)' without mentioning F3.

---

### feature_availability_conflict

**Description:** Tk settings dialog claims to have 'Interpreter Tab' and 'UI Tab' with multiple settings, but Web settings dialog only has 'Editor Tab' and 'Limits Tab' with much more limited functionality

**Affected files:**
- `help/ui/tk/settings.md`
- `help/ui/web/settings.md`

**Details:**
Tk settings.md lists: 'Editor Tab', 'Keywords Tab', 'Variables Tab', 'Interpreter Tab', 'UI Tab' with settings like 'Strict Mode', 'Max Execution Time', 'Debug Mode', 'Theme', 'Font Size', 'Case Style', 'Case Conflict', etc. Web settings.md only mentions: 'Editor Tab' (auto-numbering only) and 'Limits Tab' (view-only). This suggests major feature disparity or documentation error.

---

### feature_availability_conflict

**Description:** Major discrepancy in debugging features described

**Affected files:**
- `help/ui/web/getting-started.md`
- `help/ui/web/debugging.md`

**Details:**
getting-started.md describes basic stepping: 'Step Line' and 'Step Stmt' buttons with simple functionality. However, debugging.md describes extensive debugging features including: 'Visual breakpoint management', 'Click any line number to set breakpoint', 'Breakpoint Panel', 'Variables Panel' with tree view, 'Call Stack Panel', 'Conditional Breakpoints', 'Logpoints', 'Data Breakpoints', 'Debug Console', 'Performance Profiling'. These advanced features are not mentioned at all in getting-started.md, suggesting either incomplete documentation or features not yet implemented.

---

### contradictory_information

**Description:** Conflicting information about file persistence

**Affected files:**
- `help/ui/web/getting-started.md`
- `help/ui/web/features.md`

**Details:**
getting-started.md states: 'The Web UI doesn't have a built-in filesystem. All saves are downloads to your computer' and 'there's no auto-save'. However, features.md under 'Local Storage' describes 'Automatic Saving: Saves to browser storage, Every 30 seconds, On significant changes, Before running' and 'Session Recovery: Restores last program, Recovers after crash'. These are contradictory statements about file persistence and auto-save capabilities.

---

### keyboard_shortcut_inconsistency

**Description:** Conflicting keyboard shortcuts for Variables window between Tk UI and Curses UI documentation

**Affected files:**
- `user/TK_UI_QUICK_START.md`
- `user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md states 'Ctrl+V' shows Variables window and 'Ctrl+W' shows Variables & Resources window for Tk UI. However, keyboard-shortcuts.md (Curses UI) states 'Ctrl+W' toggles variables watch window. The TK quick start also lists 'Ctrl+K' for Execution Stack, but keyboard-shortcuts.md says 'Menu only' for execution stack window.

---

## 🟡 Medium Severity

### missing_reference

**Description:** README.md lists entry points for common and curses help, but omits tk, cli, and visual backend entry points that are mentioned in the structure section

**Affected files:**
- `help/README.md`
- `help/common/index.md`

**Details:**
README.md states 'Entry Points: **Common Help**: [common/index.md](common/index.md), **Curses Help**: [ui/curses/index.md](ui/curses/index.md)' but earlier describes '/ui/cli', '/ui/tk', and '/ui/visual' directories without providing their index.md entry points

---

### inconsistent_information

**Description:** Conflicting keyboard shortcuts for breakpoint toggling in Tk UI

**Affected files:**
- `help/common/debugging.md`
- `help/common/editor-commands.md`

**Details:**
debugging.md states 'Tk UI: Click the line number gutter next to the line, Or position cursor on the line and press **Ctrl+B**' but editor-commands.md does not list Ctrl+B in the 'Program Commands' section, only showing F-keys and other Ctrl commands

---

### missing_function_reference

**Description:** LOF function is referenced in other files but not listed in the functions index

**Affected files:**
- `help/common/language/functions/index.md`
- `help/common/language/appendices/math-functions.md`

**Details:**
LOF is mentioned in eof.md and input_dollar.md as a related function, but it's not listed in the functions/index.md alphabetical reference or categorized list

---

### missing_function_reference

**Description:** PEEK function is referenced but not listed in the functions index

**Affected files:**
- `help/common/language/functions/index.md`

**Details:**
PEEK is mentioned in inp.md and inkey_dollar.md as a related function, but it's not listed in the functions/index.md alphabetical reference

---

### missing_function_reference

**Description:** OCT$ function is referenced but not listed in the functions index

**Affected files:**
- `help/common/language/functions/index.md`

**Details:**
OCT$ is mentioned as a related function in multiple files (hex_dollar.md, asc.md, etc.) but is not in the alphabetical quick reference in index.md, though it appears in the categorized list

---

### incomplete_description

**Description:** SGN function has 'NEEDS_DESCRIPTION' placeholder in multiple files

**Affected files:**
- `help/common/language/functions/sgn.md`

**Details:**
In abs.md, atn.md, cos.md, exp.md, fix.md, int.md, and math-functions.md, SGN is listed with description 'NEEDS_DESCRIPTION' instead of proper documentation

---

### cross_reference_inconsistency

**Description:** LOF function missing from index but referenced as related function

**Affected files:**
- `help/common/language/functions/index.md`

**Details:**
LOF is listed in 'See Also' sections of eof.md and input_dollar.md, indicating it should be documented, but it's completely absent from the functions index

---

### duplicate_function

**Description:** SPACE$ function is documented twice with different titles and slightly different content

**Affected files:**
- `help/common/language/functions/space_dollar.md`
- `help/common/language/functions/spaces.md`

**Details:**
space_dollar.md has title 'SPACE$' with syntax 'SPACE$(I)' and spaces.md has title 'SPACES' with syntax 'SPACE$(X)'. Both describe the same function but use different parameter names (I vs X) and have different examples. The spaces.md file appears to be a duplicate or alternate documentation.

---

### inconsistent_see_also_sections

**Description:** Program control statements have identical 'See Also' sections listing each other, but CHAIN has empty Remarks section while others have content

**Affected files:**
- `help/common/language/statements/chain.md`
- `help/common/language/statements/clear.md`
- `help/common/language/statements/common.md`
- `help/common/language/statements/cont.md`
- `help/common/language/statements/end.md`

**Details:**
CHAIN.md has 'Remarks' section with no content ('## Remarks' followed immediately by '## See Also'), while CLEAR, COMMON, CONT, and END all have substantive Remarks sections. All five share the exact same See Also list.

---

### incomplete_documentation

**Description:** CHAIN and EDIT statements have empty Remarks sections

**Affected files:**
- `help/common/language/statements/chain.md`
- `help/common/language/statements/edit.md`

**Details:**
CHAIN.md shows syntax 'CHAIN [MERGE] <filename>[,[<line number exp>] [,ALL] [,DELETE<range>]]' but has no explanation in Remarks. EDIT.md has no Remarks content at all. Both are marked as having content but it's missing.

---

### missing_implementation_note

**Description:** CALL has detailed implementation note about not being implemented, but DEF USR only has a brief note

**Affected files:**
- `help/common/language/statements/call.md`
- `help/common/language/statements/def-usr.md`

**Details:**
CALL.md has comprehensive implementation note with sections for Behavior, Why, See Also, and Historical Reference. DEF USR.md only has a brief note under '## Notes' section. Since both relate to assembly language and are not implemented, they should have consistent implementation note formatting.

---

### missing_cross_reference

**Description:** Modern extension statements (HELP SET, LIMITS, SHOW SETTINGS, SET) are not listed in the main index.md file

**Affected files:**
- `help/common/language/statements/index.md`
- `help/common/language/statements/helpsetting.md`
- `help/common/language/statements/limits.md`
- `help/common/language/statements/showsettings.md`

**Details:**
index.md provides a comprehensive listing of all BASIC-80 statements but omits HELP SET, LIMITS, SHOW SETTINGS, and SET (setting) which are documented as 'MBASIC Extension' statements in their respective files. These should be listed in a separate 'Modern Extensions' or 'System Extensions' category in the index.

---

### inconsistent_categorization

**Description:** ERR AND ERL VARIABLES has category 'NEEDS_CATEGORIZATION' while ERROR has 'error-handling'

**Affected files:**
- `help/common/language/statements/err-erl-variables.md`
- `help/common/language/statements/error.md`

**Details:**
err-erl-variables.md has 'category: NEEDS_CATEGORIZATION' and 'description: NEEDS_DESCRIPTION', while the closely related error.md file has 'category: error-handling'. These should both be in the error-handling category since ERR and ERL are error-related variables.

---

### inconsistent_categorization

**Description:** Multiple file I/O related statements have category 'NEEDS_CATEGORIZATION' while similar statements are properly categorized

**Affected files:**
- `help/common/language/statements/input_hash.md`
- `help/common/language/statements/line-input.md`
- `help/common/language/statements/lprint-lprint-using.md`

**Details:**
input_hash.md, line-input.md, and lprint-lprint-using.md all have 'category: NEEDS_CATEGORIZATION', while similar I/O statements like field.md has 'category: file-io' and input.md has 'category: input-output'. These should be consistently categorized.

---

### title_inconsistency

**Description:** File title has unusual tilde prefix '~ INPUTi' that doesn't match filename or syntax

**Affected files:**
- `help/common/language/statements/inputi.md`

**Details:**
inputi.md has title '~ INPUTi' with a leading tilde and space, but the syntax shows 'LINE INPUTi'. The tilde appears to be a formatting artifact or error. The title should be 'LINE INPUT#' or 'LINE INPUTi' without the tilde.

---

### missing_description

**Description:** ERR AND ERL VARIABLES file has placeholder description

**Affected files:**
- `help/common/language/statements/err-erl-variables.md`

**Details:**
err-erl-variables.md has 'description: NEEDS_DESCRIPTION' which is a placeholder that should be replaced with actual documentation describing the ERR and ERL error handling variables.

---

### incomplete_documentation

**Description:** Multiple statements have empty Remarks sections

**Affected files:**
- `help/common/language/statements/error.md`
- `help/common/language/statements/for-next.md`
- `help/common/language/statements/if-then-else-if-goto.md`

**Details:**
error.md, for-next.md, and if-then-else-if-goto.md all have '## Remarks' headers with no content following them. These sections should either be removed or populated with relevant information about the statements.

---

### incomplete_remarks_section

**Description:** Several statements have incomplete or improperly formatted Remarks sections

**Affected files:**
- `help/common/language/statements/print.md`
- `help/common/language/statements/printi-printi-using.md`
- `help/common/language/statements/read.md`

**Details:**
PRINT has 'Remarks' section that starts but content is in Example section. PRINTi has empty Remarks section with just '## See Also'. READ has empty Remarks section. This is inconsistent with other files that have complete Remarks sections.

---

### inconsistent_terminology

**Description:** Inconsistent file mode terminology

**Affected files:**
- `help/common/language/statements/rset.md`
- `help/common/language/statements/writei.md`

**Details:**
RSET.md uses 'mode "O"' and 'mode "A"' while WRITEI.md uses 'mode "O"' and 'mode "A"' consistently, but other files may use different terminology. Need to verify consistency across all file I/O documentation.

---

### missing_reference

**Description:** Reference to non-existent appendix

**Affected files:**
- `help/common/language/statements/resume.md`

**Details:**
RESUME.md states 'See [Error Codes](../appendices/error-codes.md) for complete list.' but no appendices directory or error-codes.md file is provided in the documentation set.

---

### version_information_inconsistency

**Description:** Inconsistent version notation format

**Affected files:**
- `help/common/language/statements/restore.md`
- `help/common/language/statements/run.md`
- `help/common/language/statements/swap.md`

**Details:**
RESTORE.md uses 'SK, Extended, Disk' while RUN.md uses 'SK, Extended, Disk' and SWAP.md uses 'EXtended, Disk' (with inconsistent capitalization). The version notation should be standardized.

---

### missing_reference

**Description:** Reference to non-existent appendix

**Affected files:**
- `help/common/language/statements/save.md`

**Details:**
SAVE.md states 'See also Appendix B.' but no Appendix B is provided in the documentation set.

---

### inconsistent_formatting

**Description:** Malformed syntax section

**Affected files:**
- `help/common/language/statements/write.md`

**Details:**
WRITE.md has 'Ver~ion: Disk' instead of 'Versions: Disk' and uses 'Remark$.:' instead of 'Remarks:'. The entire Remarks section has OCR-style errors like 'te expressions' instead of 'the expressions'.

---

### path_inconsistency

**Description:** Inconsistent path depth in cross-references

**Affected files:**
- `help/common/ui/curses/editing.md`

**Details:**
The file references both '../../../ui/curses/running.md' (3 levels up) and '../../language/statements/auto.md' (2 levels up) from the same location (help/common/ui/curses/editing.md). Given the file structure, references to language should be '../../language/' and references to ui should be '../../../ui/' but this seems inconsistent with the actual file locations shown.

---

### contradictory_information

**Description:** Conflicting information about WATCH command

**Affected files:**
- `help/mbasic/compatibility.md`
- `help/mbasic/extensions.md`

**Details:**
extensions.md does not mention a WATCH command in its list of debugging commands (only BREAK, STEP, STACK). However, features.md mentions 'Variable watch - Monitor variables (UI-dependent)' suggesting a WATCH feature exists, but it's unclear if this is a command or just a UI feature.

---

### missing_reference

**Description:** Missing CLI UI documentation link

**Affected files:**
- `help/index.md`

**Details:**
index.md lists four UI options: 'Tk (Desktop GUI)', 'Curses (Terminal)', 'Web Browser', and 'CLI (Command Line)' with links. However, only help/common/ui/tk/index.md is provided in the documentation set. The curses editing.md exists but not the main curses index.md, and no web or cli index files are provided.

---

### feature_description_conflict

**Description:** Syntax highlighting availability unclear

**Affected files:**
- `help/mbasic/features.md`
- `help/mbasic/extensions.md`

**Details:**
features.md under 'Tkinter GUI' lists 'Syntax highlighting (if available)' suggesting it's optional. extensions.md under 'Editor Enhancements' lists 'Syntax highlighting (Tk, Web)' as a definitive feature. The conditional nature in features.md conflicts with the definitive statement in extensions.md.

---

### feature_availability

**Description:** STEP INTO/OVER commands mentioned as 'not yet implemented' in CLI but not mentioned in Curses

**Affected files:**
- `help/ui/cli/debugging.md`
- `help/ui/curses/feature-reference.md`

**Details:**
cli/debugging.md states under Limitations: 'STEP INTO/OVER not yet implemented (use STEP)'. However, curses/feature-reference.md does not mention STEP INTO or STEP OVER at all, only 'Step Statement' and 'Step Line'. It's unclear if these features exist in any UI.

---

### feature_availability

**Description:** Find/Replace availability inconsistency

**Affected files:**
- `help/ui/cli/find-replace.md`
- `help/ui/curses/feature-reference.md`

**Details:**
cli/find-replace.md states 'The CLI backend does not have built-in Find/Replace commands' and recommends using Tk UI. However, curses/feature-reference.md lists 'Find/Replace (Ctrl+F / Ctrl+H)' as an available feature in Curses UI. The CLI documentation should mention Curses UI as an alternative alongside Tk UI.

---

### command_inconsistency

**Description:** Delete Lines command inconsistency

**Affected files:**
- `help/ui/curses/editing.md`
- `help/ui/curses/feature-reference.md`

**Details:**
In curses/feature-reference.md, 'Delete Lines (Ctrl+D)' is listed as a file operation. However, in curses/editing.md under 'Deleting Lines', it describes manual deletion by removing text and pressing Enter, with no mention of Ctrl+D shortcut.

---

### feature_availability_conflict

**Description:** Variable editing capability inconsistency

**Affected files:**
- `help/ui/curses/variables.md`
- `help/ui/curses/quick-reference.md`

**Details:**
variables.md states 'e or Enter: Edit selected variable value (simple variables and array elements)' in the Variables Window section, but also has a section titled 'Variable Editing (Limited)' that says 'Cannot edit values directly in window' and 'No inline editing'. This is contradictory.

---

### feature_availability_conflict

**Description:** Variables window sorting modes inconsistency

**Affected files:**
- `help/ui/curses/variables.md`
- `help/ui/curses/quick-reference.md`

**Details:**
quick-reference.md lists 6 sort modes (Name, Accessed, Written, Read, Type, Value) while variables.md lists only 4 sort modes (Name A-Z, Type, Value, Last Modified). The modes don't match.

---

### feature_description_conflict

**Description:** Conflicting information about auto-run behavior when loading from command line

**Affected files:**
- `help/ui/curses/files.md`
- `help/ui/curses/getting-started.md`

**Details:**
files.md states that loading from command line will 'Automatically run' the program, but getting-started.md doesn't mention this auto-run behavior when starting with a filename.

---

### keyboard_shortcut_inconsistency

**Description:** Help keyboard shortcut inconsistency

**Affected files:**
- `help/ui/curses/quick-reference.md`
- `help/ui/curses/index.md`

**Details:**
quick-reference.md shows '{{kbd:help}}' for Help, while index.md shows 'Ctrl+P' explicitly. The template variable may not be resolving consistently.

---

### keyboard_shortcut_inconsistency

**Description:** Inconsistent keyboard shortcut notation in Tk documentation

**Affected files:**
- `help/ui/tk/feature-reference.md`
- `help/ui/tk/features.md`

**Details:**
feature-reference.md uses plain text shortcuts like 'Ctrl+N', 'Ctrl+O', while features.md uses template notation like '{{kbd:smart_insert}}', '{{kbd:toggle_breakpoint}}'. This inconsistency in notation style could confuse readers.

---

### ui_comparison_inconsistency

**Description:** UI comparison table inconsistency for variable editing

**Affected files:**
- `help/ui/index.md`
- `help/ui/curses/variables.md`

**Details:**
index.md comparison table doesn't include a 'Variable Editing' row, but variables.md has an entire comparison table showing Curses as '⚠️' for 'Edit values' while Tk and Web show '✅'. This important distinction is missing from the main UI comparison.

---

### keyboard_shortcut_inconsistency

**Description:** Inconsistent keyboard shortcuts for opening settings dialog

**Affected files:**
- `help/ui/tk/settings.md`
- `help/ui/web/settings.md`

**Details:**
Tk settings.md states: 'Keyboard shortcut: (check your system's menu)' - no specific shortcut given. Web settings.md states: 'Use keyboard shortcut: `Ctrl+,` (if enabled)' - specific shortcut provided but marked as conditional.

---

### feature_description_conflict

**Description:** Conflicting information about file system capabilities

**Affected files:**
- `help/ui/web/getting-started.md`
- `help/ui/web/features.md`

**Details:**
getting-started.md states: 'In-memory filesystem - File I/O within browser session' and 'Files stored in memory, persist during session only'. However, features.md under 'File Operations' mentions 'Save to browser', 'Download as file', 'Export to GitHub', 'Share via link' and under 'Format Support' lists multiple input/output formats including 'PDF export', suggesting more persistent file capabilities than just in-memory.

---

### ui_layout_inconsistency

**Description:** Different descriptions of UI panel layout

**Affected files:**
- `help/ui/web/getting-started.md`
- `help/ui/web/features.md`

**Details:**
getting-started.md describes 'simple, vertical layout' with components 'from top to bottom': Menu Bar, Toolbar, Program Editor, Output, Input Area, Command Area, Status Bar. Features.md under 'Layout Options' mentions 'Resizable panels', 'Hide/show panels', 'Horizontal/vertical split', suggesting a more flexible layout than the fixed vertical layout described in getting-started.

---

### feature_availability_conflict

**Description:** Features.md describes many settings not available in settings.md

**Affected files:**
- `help/ui/web/features.md`
- `help/ui/web/settings.md`

**Details:**
features.md under 'Customization' lists 'Editor Settings: Font size, Font family, Tab size, Line wrapping' and 'Behavior Settings: Auto-save interval, Syntax check delay, Execution speed, Debug options'. However, settings.md only documents 'Enable auto-numbering' and 'Line number increment' in the Editor tab, with no mention of these other settings.

---

### UI availability inconsistency

**Description:** Web interface documentation mentions 'Tkinter' and 'Curses' UIs, but library documentation mentions 'Tk' instead of 'Tkinter'

**Affected files:**
- `help/ui/web/web-interface.md`
- `library/business/index.md`
- `library/data_management/index.md`
- `library/demos/index.md`
- `library/education/index.md`
- `library/electronics/index.md`
- `library/games/index.md`
- `library/ham_radio/index.md`
- `library/telecommunications/index.md`
- `library/utilities/index.md`

**Details:**
web-interface.md uses 'Tkinter' (e.g., 'Open MBASIC in your preferred UI (Web, Tkinter, Curses, or CLI)'), while all library index.md files use 'Tk' (e.g., 'GUI (Web/Tk): File → Open'). This inconsistent naming could confuse users about whether these are the same UI or different ones.

---

### Missing menu option documentation

**Description:** Web interface File Menu documentation doesn't include 'Open' option that is referenced in usage instructions

**Affected files:**
- `help/ui/web/web-interface.md`
- `library/business/index.md`

**Details:**
web-interface.md File Menu section lists: 'New', 'Load Example', 'Clear Output' but the library documentation and general usage instructions reference 'File → Open' which is not documented in the menu functions list.

---

### duplicate_documentation

**Description:** Two installation guides exist with overlapping purposes but different content levels

**Affected files:**
- `user/INSTALL.md`
- `user/INSTALLATION.md`

**Details:**
INSTALL.md is a complete installation guide with detailed instructions for virtual environments, multiple installation methods, and troubleshooting. INSTALLATION.md is marked as a PLACEHOLDER with minimal content that redirects to other files. This creates confusion about which file is the authoritative installation guide.

---

### feature_availability_conflict

**Description:** Conflicting information about Curses UI variable editing capabilities

**Affected files:**
- `user/CHOOSING_YOUR_UI.md`
- `user/QUICK_REFERENCE.md`

**Details:**
CHOOSING_YOUR_UI.md states under Curses limitations: 'Partial variable editing'. However, QUICK_REFERENCE.md does not mention any variable editing features at all for the Curses UI, suggesting either the feature doesn't exist or the documentation is incomplete.

---

### feature_availability_conflict

**Description:** Find/Replace availability inconsistency

**Affected files:**
- `user/TK_UI_QUICK_START.md`
- `user/UI_FEATURE_COMPARISON.md`

**Details:**
TK_UI_QUICK_START.md lists 'Ctrl+H' for 'Find and replace' in the Essential Keyboard Shortcuts table. However, UI_FEATURE_COMPARISON.md shows Find/Replace as 'Tk only (new feature)' with checkmark for Tk but X for Web, and states it was 'Recently Added (2025-10-29)'. But the comparison matrix shows 'Find/Replace' with '❌' for Web and '✅' for Tk only.

---

### keyboard_shortcut_inconsistency

**Description:** Help shortcut key conflict

**Affected files:**
- `user/TK_UI_QUICK_START.md`
- `user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md does not list a help shortcut in the Essential Keyboard Shortcuts table, but mentions 'Press F1' in the Getting Help section. keyboard-shortcuts.md (Curses UI) lists '^F' for help and 'Ctrl+H' is listed for help in the Common Shortcuts comparison table in UI_FEATURE_COMPARISON.md for Curses.

---

### keyboard_shortcut_inconsistency

**Description:** Save shortcut inconsistency for Curses UI

**Affected files:**
- `user/keyboard-shortcuts.md`
- `user/UI_FEATURE_COMPARISON.md`

**Details:**
keyboard-shortcuts.md lists 'Ctrl+V' for Save program in Curses UI, but UI_FEATURE_COMPARISON.md lists 'Ctrl+S' as the Save shortcut for Curses in the Common Shortcuts table.

---

## 🟢 Low Severity

### inconsistent_terminology

**Description:** Inconsistent naming of UI backends - 'Curses/Urwid' vs 'Curses'

**Affected files:**
- `help/common/debugging.md`
- `help/common/editor-commands.md`

**Details:**
README.md uses 'Curses/Urwid Backend' and 'full-screen terminal UI (urwid)', while debugging.md and other files consistently use just 'Curses UI'

---

### missing_reference

**Description:** editor-commands.md references shortcuts.md but this file is not included in the provided documentation

**Affected files:**
- `help/common/editor-commands.md`
- `help/common/debugging.md`

**Details:**
editor-commands.md has 'See Also: [Keyboard Shortcuts](shortcuts.md)' and debugging.md references '[Keyboard Shortcuts](shortcuts.md)' but shortcuts.md is not in the file list

---

### missing_reference

**Description:** getting-started.md references UI-specific help files that are not included in the documentation set

**Affected files:**
- `help/common/getting-started.md`

**Details:**
getting-started.md states 'See your UI-specific help for how to type programs: [Curses UI](ui/curses/editing.md), [Tkinter UI](ui/tk/index.md), [CLI](ui/cli/index.md)' but none of these files (ui/curses/editing.md, ui/tk/index.md, ui/cli/index.md) are in the provided file list

---

### missing_reference

**Description:** index.md references language.md which is not in the file list

**Affected files:**
- `help/common/index.md`

**Details:**
index.md has '[BASIC Language Reference](language.md)' but the actual language reference appears to be at 'help/common/language/index.md' based on other files, and 'language.md' is not provided

---

### inconsistent_information

**Description:** Debugging.md mentions Web UI features but README.md does not list a Web UI backend

**Affected files:**
- `help/common/debugging.md`

**Details:**
debugging.md extensively documents 'Web UI' features (e.g., 'Web UI: Click the line number to toggle breakpoint') but README.md only lists cli, curses, tk, and visual backends in the structure section

---

### missing_reference

**Description:** appendices/index.md references math-functions.md which is not included in the file list

**Affected files:**
- `help/common/language/appendices/index.md`

**Details:**
appendices/index.md lists '[Mathematical Functions](math-functions.md)' as an available appendix with detailed description, but this file is not in the provided documentation set

---

### inconsistent_information

**Description:** Optimization count discrepancy in title vs content

**Affected files:**
- `help/common/compiler/optimizations.md`

**Details:**
The document states '27 optimizations implemented' in the summary, and lists exactly 27 optimizations in the content, but the title and description say 'Compiler optimization techniques' without specifying the count - this is minor but could be made consistent

---

### inconsistent_function_listing

**Description:** SPACE$ vs SPACES inconsistency in function index

**Affected files:**
- `help/common/language/functions/index.md`

**Details:**
The categorized list shows 'SPACE$' linking to 'spaces.md', but the alphabetical reference shows 'SPACE$' linking to 'spaces.md'. The actual file reference is inconsistent with the function name.

---

### version_information_inconsistency

**Description:** Version information formatting inconsistency

**Affected files:**
- `help/common/language/functions/hex_dollar.md`

**Details:**
hex_dollar.md shows 'HEX$ (X) Versionsr Extended, Disk' with 'Versionsr' (typo) instead of 'Versions:' as used in other files

---

### syntax_formatting_inconsistency

**Description:** Syntax section has inconsistent formatting

**Affected files:**
- `help/common/language/functions/int.md`

**Details:**
int.md shows 'INT (X) Versions,: 8K, Extended, Disk' with version info in the syntax block, while other files separate syntax from version information

---

### missing_category

**Description:** CVI/CVS/CVD function has 'NEEDS_CATEGORIZATION' placeholder

**Affected files:**
- `help/common/language/functions/cvi-cvs-cvd.md`

**Details:**
The category field shows 'NEEDS_CATEGORIZATION' instead of a proper category like 'type-conversion' or 'file-io'

---

### missing_csng_reference

**Description:** CINT references CSNG in See Also but CSNG doesn't reference CINT back

**Affected files:**
- `help/common/language/functions/cint.md`

**Details:**
cint.md lists CSNG as related, but csng.md doesn't list CINT in its See Also section, creating an asymmetric relationship

---

### inconsistent_parameter_naming

**Description:** SPACE$ function uses inconsistent parameter names across documentation

**Affected files:**
- `help/common/language/functions/space_dollar.md`
- `help/common/language/functions/spaces.md`

**Details:**
space_dollar.md uses 'SPACE$(I)' while spaces.md uses 'SPACE$(X)' for the same function parameter

---

### inconsistent_see_also_lists

**Description:** SPACE$ and SPACES have different 'See Also' sections despite being the same function

**Affected files:**
- `help/common/language/functions/space_dollar.md`
- `help/common/language/functions/spaces.md`

**Details:**
space_dollar.md has a comprehensive list of string functions in 'See Also', while spaces.md has a different list including CLOAD, CSAVE, CDBL, CVI/CVS/CVD, etc. which are not string-related

---

### missing_syntax_section

**Description:** STRING$ function documentation is missing the Syntax section in markdown body

**Affected files:**
- `help/common/language/functions/string_dollar.md`

**Details:**
string_dollar.md has no '## Syntax' section with code block, only '## Description' and '## Example'. Other function docs consistently include a Syntax section.

---

### inconsistent_formatting

**Description:** Example code formatting is inconsistent with extra text mixed into code blocks

**Affected files:**
- `help/common/language/functions/left_dollar.md`
- `help/common/language/functions/mid_dollar.md`
- `help/common/language/functions/right_dollar.md`

**Details:**
left_dollar.md example includes 'Also see the MID$ and RIGHT$ functions.' inside the code block. mid_dollar.md includes 'Also see the LEFT$ and RIGHT$ functions.' and a NOTE inside the code block. right_dollar.md includes 'Also see the MID$ and LEFT$ functions.' and 'BASIC-SO FUNCTIONS Page 3-1S' inside the code block. These should be outside the code blocks.

---

### typo_in_description

**Description:** Typo in LEFT$ description

**Affected files:**
- `help/common/language/functions/left_dollar.md`

**Details:**
Description states 'If I is greater than LEN (X$), the. entire string (X$) will be returned.' - has 'the.' instead of 'the'

---

### inconsistent_range_specification

**Description:** Range specifications use different formats

**Affected files:**
- `help/common/language/functions/left_dollar.md`
- `help/common/language/functions/mid_dollar.md`

**Details:**
left_dollar.md states 'I must be in the range 0 to 255' while mid_dollar.md states 'I and J must be in the range 1 to 255'. The inconsistency is that LEFT$ allows 0 but MID$ starts at 1, which may be correct but should be clearly documented.

---

### inconsistent_versions_format

**Description:** Version information formatting is inconsistent

**Affected files:**
- `help/common/language/functions/len.md`
- `help/common/language/functions/loc.md`
- `help/common/language/functions/lof.md`
- `help/common/language/functions/lpos.md`

**Details:**
len.md uses '**Versions:** 8R, Extended, Disk' while loc.md, lof.md, and lpos.md use '**Versions:** Disk' or '**Versions:** Extended, Disk'. Some files have version info, others don't.

---

### missing_cross_reference

**Description:** DEF FN and DEF USR are related statements but don't cross-reference each other in their 'See Also' sections

**Affected files:**
- `help/common/language/statements/def-fn.md`
- `help/common/language/statements/def-usr.md`

**Details:**
DEF FN has no reference to DEF USR, and DEF USR has a reference to DEF FN but not vice versa. Both define user-extensible functionality and should reference each other.

---

### version_information_inconsistency

**Description:** Inconsistent version notation format across statements

**Affected files:**
- `help/common/language/statements/cls.md`
- `help/common/language/statements/def-usr.md`
- `help/common/language/statements/csave.md`

**Details:**
CLS uses '**Versions:** Extended, Disk', DEF USR uses '**Versions:** Extended, Disk', but CSAVE uses '**Versions:** 8K (cassette), Extended (cassette)' with additional detail in parentheses. The format should be consistent.

---

### inconsistent_terminology

**Description:** Inconsistent reference to USR function vs USR statement

**Affected files:**
- `help/common/language/functions/varptr.md`
- `help/common/language/statements/call.md`

**Details:**
VARPTR.md references 'USR functions' in Historical Context, and CALL.md references 'OSR function' (likely typo for USR). The See Also in VARPTR links to usr.md as a function, while CALL mentions it as 'OSR function, Section 3.40'.

---

### typo

**Description:** Possible typo: 'OSR function' instead of 'USR function'

**Affected files:**
- `help/common/language/statements/call.md`

**Details:**
CALL.md Remarks section states '(See also the OSR function, Section 3.40)' which is likely meant to be 'USR function'

---

### inconsistent_formatting

**Description:** Title formatting inconsistency for cassette-related commands

**Affected files:**
- `help/common/language/statements/cload.md`
- `help/common/language/statements/csave.md`

**Details:**
Both CLOAD and CSAVE have titles that include 'THIS COMMAND IS NOT INCLUDED IN THE DEC VT180 VERSION' but this should probably be in a separate note section rather than the title itself.

---

### inconsistent_see_also_references

**Description:** HELP SET and LIMITS have identical 'See Also' sections that include each other and SET/SHOW SETTINGS, but other related files don't reciprocate

**Affected files:**
- `help/common/language/statements/helpsetting.md`
- `help/common/language/statements/limits.md`

**Details:**
helpsetting.md and limits.md both reference each other and setsetting.md/showsettings.md in their 'See Also' sections, but setsetting.md and showsettings.md are not included in the provided files to verify if they reciprocate these references. This creates potential one-way reference chains.

---

### inconsistent_syntax_formatting

**Description:** Inconsistent use of 'i' vs '#' in syntax for file number operations

**Affected files:**
- `help/common/language/statements/field.md`
- `help/common/language/statements/inputi.md`

**Details:**
field.md uses 'FIELD[i]<file number>' while inputi.md uses 'LINE INPUTi<file number>' but the title is '~ INPUTi' with a tilde. Other files like input_hash.md use 'INPUT#<file number>'. The notation should be consistent - either use '#' or 'i' uniformly.

---

### version_notation_inconsistency

**Description:** Inconsistent version notation formatting

**Affected files:**
- `help/common/language/statements/error.md`
- `help/common/language/statements/for-next.md`

**Details:**
error.md shows '**Versions:** Extend~d,   Disk' with a tilde in 'Extended' and irregular spacing, while for-next.md shows '**Versions:** SK, Extended, Disk' with proper formatting. Version notation should be consistent across all files.

---

### see_also_reference_mismatch

**Description:** Inconsistent 'See Also' reference to LINE INPUT# statement

**Affected files:**
- `help/common/language/statements/field.md`
- `help/common/language/statements/files.md`
- `help/common/language/statements/get.md`
- `help/common/language/statements/inputi.md`

**Details:**
Multiple files reference '~ INPUTi' in their See Also sections (field.md, files.md, get.md) matching the unusual title in inputi.md, but this should consistently reference 'LINE INPUT#' or the proper statement name.

---

### missing_see_also_reference

**Description:** LSET lists RESET in See Also, but RESET does not list LSET in its See Also section

**Affected files:**
- `help/common/language/statements/lset.md`
- `help/common/language/statements/reset.md`

**Details:**
LSET includes: '[RESET](reset.md) - Closes all open files' but RESET's See Also section does not include LSET, despite both being related to random file operations

---

### inconsistent_see_also_sections

**Description:** File I/O related statements have inconsistent See Also sections - some include all related statements while others are incomplete

**Affected files:**
- `help/common/language/statements/lset.md`
- `help/common/language/statements/printi-printi-using.md`
- `help/common/language/statements/put.md`
- `help/common/language/statements/reset.md`
- `help/common/language/statements/open.md`

**Details:**
LSET, OPEN, PUT, and PRINTi all list the same comprehensive set of file I/O related statements in their See Also sections (CLOSE, EOF, FIELD, FILES, GET, INPUT$, LOC, LOF, LPOS, LSET, OPEN, POS, PRINTi, PUT, RESET, RSET, WRITE#, INPUTi). However, RESET only lists a subset (CLOSE, EOF, FIELD, FILES, GET, INPUT$, LOC, LOF, LPOS, LSET, OPEN, POS, PRINTi, PUT, RSET, WRITE#, INPUTi) and is missing itself from the list, which is inconsistent with the pattern.

---

### inconsistent_syntax_formatting

**Description:** Syntax sections have inconsistent formatting for parameter descriptions

**Affected files:**
- `help/common/language/statements/out.md`
- `help/common/language/statements/poke.md`

**Details:**
OUT and POKE include parameter descriptions within the syntax code block ('where I and J are integer expressions...') while other files place parameter descriptions in the Remarks section. For example, LSET, MERGE, NAME, etc. keep syntax blocks clean and describe parameters in Remarks.

---

### missing_related_field

**Description:** Most files lack the 'related' field in frontmatter while some files have it

**Affected files:**
- `help/common/language/statements/merge.md`
- `help/common/language/statements/name.md`
- `help/common/language/statements/new.md`
- `help/common/language/statements/null.md`
- `help/common/language/statements/on-error-goto.md`
- `help/common/language/statements/on-gosub-on-goto.md`
- `help/common/language/statements/open.md`
- `help/common/language/statements/option-base.md`
- `help/common/language/statements/out.md`
- `help/common/language/statements/poke.md`
- `help/common/language/statements/print.md`
- `help/common/language/statements/printi-printi-using.md`
- `help/common/language/statements/put.md`
- `help/common/language/statements/randomize.md`
- `help/common/language/statements/read.md`
- `help/common/language/statements/rem.md`
- `help/common/language/statements/renum.md`

**Details:**
LSET, MID$ Assignment, and RESET have 'related' fields in their frontmatter (e.g., 'related: ['rset', 'field', 'get', 'put', 'open']'), but most other files only have 'See Also' sections without the frontmatter 'related' field. This is inconsistent metadata structure.

---

### inconsistent_version_information

**Description:** ON...GOSUB/GOTO shows versions as 'SK, Extended, Disk' while most other files show just 'Disk' or 'Extended, Disk'

**Affected files:**
- `help/common/language/statements/on-gosub-on-goto.md`

**Details:**
ON...GOSUB/GOTO lists '**Versions:** SK, Extended, Disk' which includes 'SK' (likely 8K version), but this version designation is not used consistently across other files. Most files only mention 'Disk' or 'Extended, Disk'.

---

### inconsistent_formatting

**Description:** Inconsistent syntax formatting in older documentation

**Affected files:**
- `help/common/language/statements/save.md`
- `help/common/language/statements/swap.md`
- `help/common/language/statements/write.md`

**Details:**
SAVE.md uses 'SAVE <filename> [,A   I ,P]' with unusual spacing. SWAP.md uses '<variab1e>' (with number 1 instead of letter l). WRITE.md uses 'WRITE[<list of expressions»' with closing guillemet instead of closing bracket. These appear to be OCR or conversion errors from original documentation.

---

### inconsistent_see_also_links

**Description:** Duplicate and inconsistent See Also sections

**Affected files:**
- `help/common/language/statements/rset.md`
- `help/common/language/statements/writei.md`

**Details:**
Both RSET.md and WRITEI.md have nearly identical See Also sections with many overlapping links. The link descriptions are inconsistent - some use full descriptions while others are truncated or formatted differently (e.g., 'PRINTi AND PRINTi USING' vs 'PRINT').

---

### implementation_note_inconsistency

**Description:** Different implementation note formats

**Affected files:**
- `help/common/language/statements/wait.md`
- `help/common/language/statements/width.md`

**Details:**
WAIT.md uses '⚠️ **Not Implemented**' while WIDTH.md uses '⚠️ **Emulated as No-Op**'. Both are modern extensions but use different warning formats and explanations. Should be standardized.

---

### terminology_inconsistency

**Description:** Inconsistent project naming

**Affected files:**
- `help/mbasic/extensions.md`
- `help/mbasic/features.md`
- `help/index.md`

**Details:**
extensions.md refers to the project as 'MBASIC-2025' and lists it as one of several names 'under consideration' (MBASIC-2025, Visual MBASIC 5.21, MBASIC++, MBASIC-X). However, index.md consistently uses 'MBASIC 5.21' throughout, and features.md uses 'MBASIC interpreter' without version. This creates confusion about the official project name.

---

### missing_cross_reference

**Description:** Missing link to CLI debugging documentation

**Affected files:**
- `help/mbasic/extensions.md`

**Details:**
extensions.md mentions 'See Also: CLI Debugging - Using debug commands' at the end, but this reference path '../ui/cli/debugging.md' is not verified to exist in the documentation set, and no CLI UI documentation was provided.

---

### version_inconsistency

**Description:** Inconsistent version references

**Affected files:**
- `help/index.md`
- `help/mbasic/compatibility.md`
- `help/mbasic/features.md`

**Details:**
index.md title is 'MBASIC 5.21 Help' and consistently uses 'MBASIC 5.21'. compatibility.md uses both 'MBASIC 5.21' and 'MBASIC-80 5.21' interchangeably. features.md uses 'MBASIC 5.21' in some places and just 'MBASIC' in others. The relationship between 'MBASIC', 'MBASIC-80', and 'MBASIC 5.21' is not clearly established.

---

### terminology_inconsistency

**Description:** Inconsistent terminology for line number range

**Affected files:**
- `help/mbasic/getting-started.md`
- `help/ui/curses/editing.md`

**Details:**
getting-started.md states 'Line numbers can be any value 1-65535' in the Tips section, while editing.md states 'Each line starts with a line number (1-65535)'. Both agree on the range, but the phrasing differs slightly. This is consistent information but could be standardized.

---

### missing_reference

**Description:** Web UI mentioned in getting-started.md but not in CLI index

**Affected files:**
- `help/ui/cli/index.md`
- `help/mbasic/getting-started.md`

**Details:**
In cli/variables.md, it mentions 'Web UI - Browser-based with Variables Window' as an alternative to CLI. However, the getting-started.md only mentions three UIs: 'MBASIC supports three interfaces: Curses UI (Default), CLI Mode, Tkinter GUI'. No Web UI is mentioned in the main getting started guide.

---

### path_inconsistency

**Description:** Inconsistent path format for documentation references

**Affected files:**
- `help/ui/cli/settings.md`
- `help/ui/common/errors.md`

**Details:**
settings.md uses relative paths like '../../common/settings.md' while errors.md uses backtick-quoted paths like '`docs/help/common/language/statements/on-error-goto.md`'. The format should be consistent across documentation.

---

### command_line_inconsistency

**Description:** Inconsistent command line syntax for starting MBASIC

**Affected files:**
- `help/ui/curses/files.md`
- `help/ui/tk/getting-started.md`
- `help/ui/index.md`

**Details:**
files.md uses 'python3 mbasic --ui curses myprogram.bas', while tk/getting-started.md and ui/index.md use 'mbasic --ui tk' without 'python3'. This suggests inconsistent installation/execution methods.

---

### feature_availability_conflict

**Description:** Variables window availability inconsistency in comparison table

**Affected files:**
- `help/ui/curses/variables.md`
- `help/ui/index.md`

**Details:**
index.md comparison table shows Variables Window as '✓' for Curses, but variables.md extensively documents limitations and partial implementation, suggesting it should be marked as '⚠️' or 'Limited' instead of full checkmark.

---

### navigation_inconsistency

**Description:** Help navigation key inconsistency

**Affected files:**
- `help/ui/curses/help-navigation.md`
- `help/ui/curses/index.md`

**Details:**
help-navigation.md shows '{{kbd:quit}}' to exit help, while index.md shows 'ESC or Q'. The template variable usage is inconsistent.

---

### feature_count_inconsistency

**Description:** Feature count mismatch in Tk UI documentation

**Affected files:**
- `help/ui/tk/feature-reference.md`
- `help/ui/tk/features.md`

**Details:**
feature-reference.md claims '37 features available' in the title, but the actual count in the document is: File Operations (8) + Execution & Control (6) + Debugging (6) + Variable Inspection (6) + Editor Features (7) + Help System (4) = 37. However, features.md only highlights a subset without mentioning the total count, which could cause confusion.

---

### terminology_inconsistency

**Description:** Inconsistent use of keyboard shortcut notation

**Affected files:**
- `help/ui/tk/tips.md`
- `help/ui/tk/workflows.md`

**Details:**
tk/tips.md uses: '{{kbd:smart_insert}}', '{{kbd:toggle_variables}}', '{{kbd:run_program}}', etc. tk/workflows.md uses the same notation. However, these appear to be template placeholders that should be replaced with actual keyboard shortcuts, suggesting incomplete documentation.

---

### missing_cross_reference

**Description:** Tk settings references CLI settings commands, but Web settings does not

**Affected files:**
- `help/ui/tk/settings.md`
- `help/ui/web/settings.md`

**Details:**
Tk settings.md includes section 'Additional Settings via CLI' with reference to 'See: [CLI Settings Commands](../cli/settings.md)'. Web settings.md has no such reference, though it mentions future export to CLI in 'Exporting Settings (Future)' section.

---

### version_number_inconsistency

**Description:** Specific version number mentioned may become outdated

**Affected files:**
- `help/ui/web/getting-started.md`

**Details:**
getting-started.md states in Status Bar section: 'Version number (v1.0.xxx)'. This hardcoded version reference will become outdated and should be generalized or removed.

---

### File operation instruction inconsistency

**Description:** Inconsistent menu path for loading files in GUI

**Affected files:**
- `help/ui/web/web-interface.md`
- `library/business/index.md`
- `library/data_management/index.md`
- `library/demos/index.md`
- `library/education/index.md`
- `library/electronics/index.md`
- `library/games/index.md`
- `library/ham_radio/index.md`
- `library/telecommunications/index.md`
- `library/utilities/index.md`

**Details:**
web-interface.md states 'Click File → Open, select the downloaded file' under 'How to Use', but library files say 'Web/Tkinter UI: Click File → Open, select the downloaded file'. The web-interface.md's own File Menu section lists 'Load Example' but not 'Open', creating confusion about the actual menu structure.

---

### Terminology inconsistency

**Description:** Inconsistent terminology for graphical interface

**Affected files:**
- `help/ui/web/web-interface.md`
- `library/business/index.md`
- `library/data_management/index.md`
- `library/demos/index.md`
- `library/education/index.md`
- `library/electronics/index.md`
- `library/games/index.md`
- `library/ham_radio/index.md`
- `library/telecommunications/index.md`
- `library/utilities/index.md`

**Details:**
Library files use 'GUI (Web/Tk)' while web-interface.md uses 'Web UI' and mentions 'Tkinter UI' separately. This creates ambiguity about whether 'Web UI' is part of 'GUI' or separate from it.

---

### Reference path inconsistency

**Description:** Different documentation reference styles

**Affected files:**
- `help/ui/web/web-interface.md`
- `user/CASE_HANDLING_GUIDE.md`

**Details:**
web-interface.md uses relative paths with emoji: '[📕 Language Help](../../common/index.md)' and '[📗 MBASIC Help](../../mbasic/index.md)', while CASE_HANDLING_GUIDE.md uses plain text without paths: '`SETTINGS_AND_CONFIGURATION.md`', '`TK_UI_QUICK_START.md`', '`QUICK_REFERENCE.md`'. This inconsistency in documentation linking style could lead to broken references.

---

### missing_reference

**Description:** CHOOSING_YOUR_UI.md is not listed in the user/README.md contents section

**Affected files:**
- `user/CHOOSING_YOUR_UI.md`
- `user/README.md`

**Details:**
user/README.md lists only three documents in its Contents section: QUICK_REFERENCE.md, URWID_UI.md, and FILE_FORMAT_COMPATIBILITY.md. However, CHOOSING_YOUR_UI.md is a substantial user-facing document that should be included in this index.

---

### missing_reference

**Description:** SETTINGS_AND_CONFIGURATION.md is not listed in the user/README.md contents section

**Affected files:**
- `user/SETTINGS_AND_CONFIGURATION.md`
- `user/README.md`

**Details:**
user/README.md does not list SETTINGS_AND_CONFIGURATION.md in its Contents section, despite it being a comprehensive user-facing guide for configuring MBASIC.

---

### inconsistent_terminology

**Description:** Inconsistent naming of the Curses UI

**Affected files:**
- `user/QUICK_REFERENCE.md`
- `user/CHOOSING_YOUR_UI.md`

**Details:**
QUICK_REFERENCE.md refers to 'MBASIC Curses IDE' and 'Curses UI' while CHOOSING_YOUR_UI.md consistently uses 'Curses' or 'Curses (Terminal UI)'. The term 'IDE' is applied to Curses in QUICK_REFERENCE.md but CHOOSING_YOUR_UI.md describes it as a 'TUI' (Terminal UI).

---

### missing_reference

**Description:** References non-existent UI_FEATURE_COMPARISON.md file

**Affected files:**
- `user/CHOOSING_YOUR_UI.md`

**Details:**
At the end of CHOOSING_YOUR_UI.md, under 'More Information', it references '[UI Feature Comparison](UI_FEATURE_COMPARISON.md)' but this file is not included in the provided documentation set.

---

### inconsistent_command_syntax

**Description:** Inconsistent use of python3 vs python command

**Affected files:**
- `user/CHOOSING_YOUR_UI.md`
- `user/INSTALL.md`

**Details:**
CHOOSING_YOUR_UI.md consistently uses 'python3 mbasic' throughout all examples. INSTALL.md uses both 'python3' and 'python' interchangeably, with a troubleshooting section suggesting to try 'python' if 'python3' doesn't work. This inconsistency may confuse users about which command to use.

---

### outdated_reference

**Description:** References example files that may not exist in user documentation directory

**Affected files:**
- `user/QUICK_REFERENCE.md`

**Details:**
QUICK_REFERENCE.md references 'test_continue.bas', 'demo_continue.bas', and 'test_continue_manual.sh' under Examples section, but these files are not present in the user/ directory and their location is not specified.

---

### inconsistent_terminology

**Description:** Inconsistent capitalization of UI names

**Affected files:**
- `user/SETTINGS_AND_CONFIGURATION.md`
- `user/CHOOSING_YOUR_UI.md`

**Details:**
SETTINGS_AND_CONFIGURATION.md refers to 'TK UI' (all caps) in the Related Documentation section, while CHOOSING_YOUR_UI.md uses 'Tk' (mixed case) consistently throughout the document.

---

### terminology_inconsistency

**Description:** Inconsistent naming for Variables window feature

**Affected files:**
- `user/TK_UI_QUICK_START.md`
- `user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md refers to 'Variables window' and 'Variables & Resources window' as separate features (Ctrl+V and Ctrl+W). keyboard-shortcuts.md calls it 'variables watch window' for Curses UI.

---

### feature_availability_conflict

**Description:** Smart Insert feature availability unclear

**Affected files:**
- `user/TK_UI_QUICK_START.md`
- `user/UI_FEATURE_COMPARISON.md`

**Details:**
TK_UI_QUICK_START.md extensively documents Smart Insert (Ctrl+I) as a Tk feature. UI_FEATURE_COMPARISON.md confirms it's 'Tk exclusive feature' with checkmark only for Tk. However, the comparison matrix shows '❌' for CLI, Curses, and Web, which is consistent, but the extensive documentation in TK quick start might suggest it should be more prominently marked as unique.

---

### command_inconsistency

**Description:** Renumber command shortcut inconsistency

**Affected files:**
- `user/TK_UI_QUICK_START.md`
- `user/keyboard-shortcuts.md`

**Details:**
TK_UI_QUICK_START.md lists 'Ctrl+E' for 'Renumber program'. keyboard-shortcuts.md also lists 'Ctrl+E' for 'Renumber all lines (RENUM)' in Curses UI. Both use same shortcut but different descriptions.

---

