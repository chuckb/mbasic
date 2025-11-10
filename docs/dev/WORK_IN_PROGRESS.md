# High Severity Inconsistencies - v21 Fixes

## Task
Fix all HIGH SEVERITY inconsistencies from docs_inconsistencies_report-v21.md (lines 11-860)

## Status: IN PROGRESS

## Fixed Issues

### Code Files (9 fixed)
1. ✅ src/immediate_executor.py - Numbered line editing docstring (UI.program method names)
2. ✅ src/interpreter.py - CLEAR statement OSError/IOError comment clarified
3. ✅ src/interpreter.py - RENUM TODO changed to accurate implementation note
4. ✅ src/interpreter.py - execute_cont() docstring line references updated
5. ✅ src/runtime.py - 'original_case' field comment consistency (3 locations)
6. ✅ src/settings_backend.py - create_settings_backend() docstring fallback notes clarified
7. ✅ src/interactive.py - clear_execution_state PC preservation clarified with cmd_cont relationship
8. ✅ src/interactive.py - GOTO/GOSUB immediate mode comment removed false reference to help text
9. ✅ src/ui/curses_ui.py - Fast path comment clarified (no syntax checking during normal typing)
10. ✅ src/ui/curses_ui.py - Immediate mode status comments updated (4 locations)
11. ✅ src/ui/tk_ui.py - _ImmediateModeToken docstring method reference corrected (line number)

### Documentation Files (7 fixed)
1. ✅ docs/help/common/language/data-types.md - D vs E notation contradiction resolved
2. ✅ docs/help/common/language/statements/for-next.md - Loop termination test wording clarified
3. ✅ docs/help/common/language/statements/llist.md - Formatting standardized
4. ✅ docs/help/common/language/statements/lprint-lprint-using.md - Formatting standardized
5. ✅ docs/help/mbasic/extensions.md - Browser session vs page refresh clarified
6. ✅ docs/help/ui/web/web-interface.md - File storage location clarified (server memory vs browser)

## Remaining HIGH Severity Issues

### Code Issues (still need to check/fix)
- [ ] codegen_backend.py & editing/manager.py - FileIO vs z88dk snap path contradiction
- [ ] file_io.py - SandboxedFileIO.list_files() vs documented purpose
- [ ] curses_ui.py - _sync_program_to_runtime PC preservation logic comment
- [ ] tk_ui.py - Blank line removal attribution comment
- [ ] tk_ui.py - Character position coordinate system assumptions
- [ ] tk_ui.py - Duplicate logic fragility comment
- [ ] tk_widgets.py - _delete_line() docstring dual numbering note
- [ ] web/nicegui_backend.py - Step commands output clearing comment
- [ ] web/nicegui_backend.py - _get_input state transition protocol comment

### Documentation Issues (still need to check/fix)
- [ ] help/common/language/statements/wait.md & width.md - Implementation note formatting
- [ ] help/mbasic/compatibility.md & extensions.md - Web UI file persistence consistency
- [ ] help/mbasic/features.md & not-implemented.md - LINE statement clarity
- [ ] help/ui/curses/variables.md & feature-reference.md - Variable editing status
- [ ] help/ui/curses/quick-reference.md & feature-reference.md - Execution Stack shortcut
- [ ] help/ui/tk/feature-reference.md & features.md - Find/Replace functionality description
- [ ] help/ui/index.md & web/debugging.md - Web UI debugger capabilities
- [ ] help/ui/tk/settings.md, workflows.md, tips.md - Settings dialog implementation status
- [ ] help/ui/index.md & tk/feature-reference.md - Variables Window availability
- [ ] help/ui/web/features.md, getting-started.md, settings.md - Program storage consistency
- [ ] docs/user/CHOOSING_YOUR_UI.md & QUICK_REFERENCE.md - CLI debugging documentation

## Files Modified So Far
- src/immediate_executor.py
- src/interpreter.py (3 changes)
- src/runtime.py (2 changes)
- src/settings_backend.py
- src/interactive.py (2 changes)
- src/ui/curses_ui.py (3 changes)
- src/ui/tk_ui.py
- docs/help/common/language/data-types.md
- docs/help/common/language/statements/for-next.md
- docs/help/common/language/statements/llist.md
- docs/help/common/language/statements/lprint-lprint-using.md
- docs/help/mbasic/extensions.md (2 changes)
- docs/help/ui/web/web-interface.md (2 changes)

## Progress
- HIGH SEVERITY issues fixed: 16 out of 39
- Files modified: 13
- Next: Address remaining code issues
