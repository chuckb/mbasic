# Developer Documentation

This section contains implementation notes, design decisions, and development history for the MBASIC project.

**Last Updated:** 2025-11-10
**Total Documents:** 175

## What's Here

This directory contains documentation for developers working on MBASIC:

- **Implementation Notes** - How features were implemented
- **Design Decisions** - Why things work the way they do
- **Testing Documentation** - Test coverage and methodologies
- **Work in Progress** - Current development tasks
- **Bug Fixes** - Historical fixes and their explanations

## Organization

Documents are organized chronologically as they were created during development. Use the search function or browse by topic below.

## For Contributors

If you're contributing to MBASIC:
1. Read `.claude/CLAUDE.md` for coding guidelines
2. Check `WORK_IN_PROGRESS.md` for current tasks
3. Review relevant implementation docs before making changes
4. Add new docs here when implementing significant features

## Browse by Category

### Language Features

- [Keybinding Systems](KEYBINDING_SYSTEMS.md)

### File I/O

- [Keybinding Macros Migration](KEYBINDING_MACROS_MIGRATION.md)
- [Pip Install Resource Location Plan](PIP_INSTALL_RESOURCE_LOCATION_PLAN.md)
- [Redis Per Session Settings](REDIS_PER_SESSION_SETTINGS.md)
- [Redis Session Storage Setup](REDIS_SESSION_STORAGE_SETUP.md)

### Debugging & Errors

- [Import Consistency Fix](IMPORT_CONSISTENCY_FIX.md)
- [Random Fixes Todo](RANDOM_FIXES_TODO.md)
- [Redis Storage Bug Fix](REDIS_STORAGE_BUG_FIX.md)

### Refactoring & Cleanup

- [Architecture Cleanup Todo](ARCHITECTURE_CLEANUP_TODO.md)

## Subdirectories

### claude_if_you_read_in_here_you_loop/

- [Accomplishments](claude_if_you_read_in_here_you_loop/ACCOMPLISHMENTS.md)
- [Array Input Read Fix](claude_if_you_read_in_here_you_loop/ARRAY_INPUT_READ_FIX.md)
- [Ast Serialization](claude_if_you_read_in_here_you_loop/AST_SERIALIZATION.md)
- [Auto Command Implementation](claude_if_you_read_in_here_you_loop/AUTO_COMMAND_IMPLEMENTATION.md)
- [Auto Numbering Implementation](claude_if_you_read_in_here_you_loop/AUTO_NUMBERING_IMPLEMENTATION.md)
- [Auto Numbering Visual Ui Design](claude_if_you_read_in_here_you_loop/AUTO_NUMBERING_VISUAL_UI_DESIGN.md)
- [Auto Numbering Web Ui Fix](claude_if_you_read_in_here_you_loop/AUTO_NUMBERING_WEB_UI_FIX.md)
- [Bad Syntax Analysis](claude_if_you_read_in_here_you_loop/BAD_SYNTAX_ANALYSIS.md)
- [Breakpoints](claude_if_you_read_in_here_you_loop/BREAKPOINTS.md)
- [Breakpoint Display Fix](claude_if_you_read_in_here_you_loop/BREAKPOINT_DISPLAY_FIX.md)
- [Breakpoint Issue Explained](claude_if_you_read_in_here_you_loop/BREAKPOINT_ISSUE_EXPLAINED.md)
- [Breakpoint Not Stopping Debug](claude_if_you_read_in_here_you_loop/BREAKPOINT_NOT_STOPPING_DEBUG.md)
- [Breakpoint Status](claude_if_you_read_in_here_you_loop/BREAKPOINT_STATUS.md)
- [Breakpoint Summary](claude_if_you_read_in_here_you_loop/BREAKPOINT_SUMMARY.md)
- [Broken Links Analysis](claude_if_you_read_in_here_you_loop/BROKEN_LINKS_ANALYSIS.md)
- [Browser Opening Fix](claude_if_you_read_in_here_you_loop/BROWSER_OPENING_FIX.md)
- [Call Implementation](claude_if_you_read_in_here_you_loop/CALL_IMPLEMENTATION.md)
- [Case Conflict With Chain Merge Common](claude_if_you_read_in_here_you_loop/CASE_CONFLICT_WITH_CHAIN_MERGE_COMMON.md)
- [Check Status](claude_if_you_read_in_here_you_loop/CHECK_STATUS.md)
- [Cleanup Summary](claude_if_you_read_in_here_you_loop/CLEANUP_SUMMARY.md)
- [Clean Install Test Results](claude_if_you_read_in_here_you_loop/CLEAN_INSTALL_TEST_RESULTS.md)
- [Codemirror6 Integration Issues](claude_if_you_read_in_here_you_loop/CODEMIRROR6_INTEGRATION_ISSUES.md)
- [Codemirror Integration Progress](claude_if_you_read_in_here_you_loop/CODEMIRROR_INTEGRATION_PROGRESS.md)
- [Code Comment Fixes Applied](claude_if_you_read_in_here_you_loop/CODE_COMMENT_FIXES_APPLIED.md)
- [Code Comment Fixes Remaining](claude_if_you_read_in_here_you_loop/CODE_COMMENT_FIXES_REMAINING.md)
- [Code Comment Fixes Summary](claude_if_you_read_in_here_you_loop/CODE_COMMENT_FIXES_SUMMARY.md)
- [Code Duplication Analysis](claude_if_you_read_in_here_you_loop/CODE_DUPLICATION_ANALYSIS.md)
- [Compiler Memory Optimization](claude_if_you_read_in_here_you_loop/COMPILER_MEMORY_OPTIMIZATION.md)
- [Continue Feature](claude_if_you_read_in_here_you_loop/CONTINUE_FEATURE.md)
- [Continue Fix Summary](claude_if_you_read_in_here_you_loop/CONTINUE_FIX_SUMMARY.md)
- [Continue Implementation](claude_if_you_read_in_here_you_loop/CONTINUE_IMPLEMENTATION.md)
- [Cr Line Ending Fix](claude_if_you_read_in_here_you_loop/CR_LINE_ENDING_FIX.md)
- [Ctrl C Input Handling](claude_if_you_read_in_here_you_loop/CTRL_C_INPUT_HANDLING.md)
- [Curses Feature Parity Complete](claude_if_you_read_in_here_you_loop/CURSES_FEATURE_PARITY_COMPLETE.md)
- [Curses Menu White Background Todo](claude_if_you_read_in_here_you_loop/CURSES_MENU_WHITE_BACKGROUND_TODO.md)
- [Curses Mouse Support Todo](claude_if_you_read_in_here_you_loop/CURSES_MOUSE_SUPPORT_TODO.md)
- [Curses Ui Feature Parity](claude_if_you_read_in_here_you_loop/CURSES_UI_FEATURE_PARITY.md)
- [Curses Ui File Loading Fix](claude_if_you_read_in_here_you_loop/CURSES_UI_FILE_LOADING_FIX.md)
- [Curses Ui Testing](claude_if_you_read_in_here_you_loop/CURSES_UI_TESTING.md)
- [Curses Vs Tk Gap Analysis](claude_if_you_read_in_here_you_loop/CURSES_VS_TK_GAP_ANALYSIS.md)
- [Cursor Fix](claude_if_you_read_in_here_you_loop/CURSOR_FIX.md)
- [Data Statement Fix](claude_if_you_read_in_here_you_loop/DATA_STATEMENT_FIX.md)
- [Debugger Commands](claude_if_you_read_in_here_you_loop/DEBUGGER_COMMANDS.md)
- [Debugger Ui Research](claude_if_you_read_in_here_you_loop/DEBUGGER_UI_RESEARCH.md)
- [Debug Mode](claude_if_you_read_in_here_you_loop/DEBUG_MODE.md)
- [Def Fn Implementation](claude_if_you_read_in_here_you_loop/DEF_FN_IMPLEMENTATION.md)
- [Def Fn Syntax Rules](claude_if_you_read_in_here_you_loop/DEF_FN_SYNTAX_RULES.md)
- [Detokenizer Fixes](claude_if_you_read_in_here_you_loop/DETOKENIZER_FIXES.md)
- [Developer Guide Index](claude_if_you_read_in_here_you_loop/DEVELOPER_GUIDE_INDEX.md)
- [Documentation Coverage](claude_if_you_read_in_here_you_loop/DOCUMENTATION_COVERAGE.md)
- [Documentation Fixes Summary](claude_if_you_read_in_here_you_loop/DOCUMENTATION_FIXES_SUMMARY.md)
- [Documentation Fixes Tracker](claude_if_you_read_in_here_you_loop/DOCUMENTATION_FIXES_TRACKER.md)
- [Editor Fixes 2025 10 30](claude_if_you_read_in_here_you_loop/EDITOR_FIXES_2025_10_30.md)
- [Else Keyword Fix](claude_if_you_read_in_here_you_loop/ELSE_KEYWORD_FIX.md)
- [Explicit Type Suffix With Defsng Issue](claude_if_you_read_in_here_you_loop/EXPLICIT_TYPE_SUFFIX_WITH_DEFSNG_ISSUE.md)
- [Feature Completion Requirements](claude_if_you_read_in_here_you_loop/FEATURE_COMPLETION_REQUIREMENTS.md)
- [Filesystem Security](claude_if_you_read_in_here_you_loop/FILESYSTEM_SECURITY.md)
- [File Io Implementation](claude_if_you_read_in_here_you_loop/FILE_IO_IMPLEMENTATION.md)
- [Functional Testing Methodology](claude_if_you_read_in_here_you_loop/FUNCTIONAL_TESTING_METHODOLOGY.md)
- [Function Key Removal](claude_if_you_read_in_here_you_loop/FUNCTION_KEY_REMOVAL.md)
- [Github Docs Workflow Explained](claude_if_you_read_in_here_you_loop/GITHUB_DOCS_WORKFLOW_EXPLAINED.md)
- [Gosub Stack Test Results](claude_if_you_read_in_here_you_loop/GOSUB_STACK_TEST_RESULTS.md)
- [Gui Library Options](claude_if_you_read_in_here_you_loop/GUI_LIBRARY_OPTIONS.md)
- [Hash File Io Fix](claude_if_you_read_in_here_you_loop/HASH_FILE_IO_FIX.md)
- [Help Build Time Indexes](claude_if_you_read_in_here_you_loop/HELP_BUILD_TIME_INDEXES.md)
- [Help Indexing Options](claude_if_you_read_in_here_you_loop/HELP_INDEXING_OPTIONS.md)
- [Help Indexing Specification](claude_if_you_read_in_here_you_loop/HELP_INDEXING_SPECIFICATION.md)
- [Help Integration Per Client](claude_if_you_read_in_here_you_loop/HELP_INTEGRATION_PER_CLIENT.md)
- [Help Menu Status](claude_if_you_read_in_here_you_loop/HELP_MENU_STATUS.md)
- [Help Migration Plan](claude_if_you_read_in_here_you_loop/HELP_MIGRATION_PLAN.md)
- [Help Migration Status](claude_if_you_read_in_here_you_loop/HELP_MIGRATION_STATUS.md)
- [Help Reorganization Example](claude_if_you_read_in_here_you_loop/HELP_REORGANIZATION_EXAMPLE.md)
- [Help System Completion](claude_if_you_read_in_here_you_loop/HELP_SYSTEM_COMPLETION.md)
- [Help System Diagram](claude_if_you_read_in_here_you_loop/HELP_SYSTEM_DIAGRAM.md)
- [Help System Reorganization](claude_if_you_read_in_here_you_loop/HELP_SYSTEM_REORGANIZATION.md)
- [Help System Summary](claude_if_you_read_in_here_you_loop/HELP_SYSTEM_SUMMARY.md)
- [Help System Web Deployment](claude_if_you_read_in_here_you_loop/HELP_SYSTEM_WEB_DEPLOYMENT.md)
- [Immediate Mode Design](claude_if_you_read_in_here_you_loop/IMMEDIATE_MODE_DESIGN.md)
- [Immediate Mode Safety](claude_if_you_read_in_here_you_loop/IMMEDIATE_MODE_SAFETY.md)
- [Implementation Summary](claude_if_you_read_in_here_you_loop/IMPLEMENTATION_SUMMARY.md)
- [Indent Command Design](claude_if_you_read_in_here_you_loop/INDENT_COMMAND_DESIGN.md)
- [Inkey Lprint Implementation](claude_if_you_read_in_here_you_loop/INKEY_LPRINT_IMPLEMENTATION.md)
- [Input Hash Fix](claude_if_you_read_in_here_you_loop/INPUT_HASH_FIX.md)
- [Installation For Developers](claude_if_you_read_in_here_you_loop/INSTALLATION_FOR_DEVELOPERS.md)
- [Installation Testing Todo](claude_if_you_read_in_here_you_loop/INSTALLATION_TESTING_TODO.md)
- [Interactive Command Test Coverage](claude_if_you_read_in_here_you_loop/INTERACTIVE_COMMAND_TEST_COVERAGE.md)
- [Interpreter Refactor Methods Not Variables Idea](claude_if_you_read_in_here_you_loop/INTERPRETER_REFACTOR_METHODS_NOT_VARIABLES_IDEA.md)
- [Keyword Case Scope Analysis](claude_if_you_read_in_here_you_loop/KEYWORD_CASE_SCOPE_ANALYSIS.md)
- [Keyword Identifier Splitting](claude_if_you_read_in_here_you_loop/KEYWORD_IDENTIFIER_SPLITTING.md)
- [Language Features Test Coverage](claude_if_you_read_in_here_you_loop/LANGUAGE_FEATURES_TEST_COVERAGE.md)
- [Language Testing Progress 2025 10 30](claude_if_you_read_in_here_you_loop/LANGUAGE_TESTING_PROGRESS_2025_10_30.md)
- [Lexer Cleanup Complete](claude_if_you_read_in_here_you_loop/LEXER_CLEANUP_COMPLETE.md)
- [Library Test Results](claude_if_you_read_in_here_you_loop/LIBRARY_TEST_RESULTS.md)
- [Menu Changes](claude_if_you_read_in_here_you_loop/MENU_CHANGES.md)
- [Mid Statement Comments Fix](claude_if_you_read_in_here_you_loop/MID_STATEMENT_COMMENTS_FIX.md)
- [Mid Statement Fix](claude_if_you_read_in_here_you_loop/MID_STATEMENT_FIX.md)
- [Mouse Breakpoint Implementation](claude_if_you_read_in_here_you_loop/MOUSE_BREAKPOINT_IMPLEMENTATION.md)
- [Nicegui Testing Guide](claude_if_you_read_in_here_you_loop/NICEGUI_TESTING_GUIDE.md)
- [Not Implemented](claude_if_you_read_in_here_you_loop/NOT_IMPLEMENTED.md)
- [Optional Dependencies Strategy](claude_if_you_read_in_here_you_loop/OPTIONAL_DEPENDENCIES_STRATEGY.md)
- [Package Dependencies](claude_if_you_read_in_here_you_loop/PACKAGE_DEPENDENCIES.md)
- [Parsed Inconsistencies Readme](claude_if_you_read_in_here_you_loop/PARSED_INCONSISTENCIES_README.md)
- [Pc Cleanup Remaining](claude_if_you_read_in_here_you_loop/PC_CLEANUP_REMAINING.md)
- [Pc Implementation Status](claude_if_you_read_in_here_you_loop/PC_IMPLEMENTATION_STATUS.md)
- [Pc Refactoring Complete](claude_if_you_read_in_here_you_loop/PC_REFACTORING_COMPLETE.md)
- [Popup Dialog Refactor Todo](claude_if_you_read_in_here_you_loop/POPUP_DIALOG_REFACTOR_TODO.md)
- [Publishing To Pypi Guide](claude_if_you_read_in_here_you_loop/PUBLISHING_TO_PYPI_GUIDE.md)
- [Pypi Publishing Checklist](claude_if_you_read_in_here_you_loop/PYPI_PUBLISHING_CHECKLIST.md)
- [Randomize Implementation](claude_if_you_read_in_here_you_loop/RANDOMIZE_IMPLEMENTATION.md)
- [Readme](claude_if_you_read_in_here_you_loop/README.md)
- [Readme Continue](claude_if_you_read_in_here_you_loop/README_CONTINUE.md)
- [Readme Tests Inventory](claude_if_you_read_in_here_you_loop/README_TESTS_INVENTORY.md)
- [Resource Limits Design](claude_if_you_read_in_here_you_loop/RESOURCE_LIMITS_DESIGN.md)
- [Runtime Interpreter Split Todo](claude_if_you_read_in_here_you_loop/RUNTIME_INTERPRETER_SPLIT_TODO.md)
- [Run Statement Implementation](claude_if_you_read_in_here_you_loop/RUN_STATEMENT_IMPLEMENTATION.md)
- [Session 2025 10 26](claude_if_you_read_in_here_you_loop/SESSION_2025_10_26.md)
- [Session 2025 10 28 Summary](claude_if_you_read_in_here_you_loop/SESSION_2025_10_28_SUMMARY.md)
- [Session Storage Audit](claude_if_you_read_in_here_you_loop/SESSION_STORAGE_AUDIT.md)
- [Session Summary 2025 Web Ui And Highlighting](claude_if_you_read_in_here_you_loop/SESSION_SUMMARY_2025_WEB_UI_AND_HIGHLIGHTING.md)
- [Settings Feature Gap Analysis](claude_if_you_read_in_here_you_loop/SETTINGS_FEATURE_GAP_ANALYSIS.md)
- [Simple Test](claude_if_you_read_in_here_you_loop/SIMPLE_TEST.md)
- [Statement Highlighting Implementation](claude_if_you_read_in_here_you_loop/STATEMENT_HIGHLIGHTING_IMPLEMENTATION.md)
- [Status](claude_if_you_read_in_here_you_loop/STATUS.md)
- [Status Bar Updates Review](claude_if_you_read_in_here_you_loop/STATUS_BAR_UPDATES_REVIEW.md)
- [Storage Abstraction Design](claude_if_you_read_in_here_you_loop/STORAGE_ABSTRACTION_DESIGN.md)
- [System Statement Fix](claude_if_you_read_in_here_you_loop/SYSTEM_STATEMENT_FIX.md)
- [Testing Checklist](claude_if_you_read_in_here_you_loop/TESTING_CHECKLIST.md)
- [Testing Guide](claude_if_you_read_in_here_you_loop/TESTING_GUIDE.md)
- [Testing Web Ui Fileio](claude_if_you_read_in_here_you_loop/TESTING_WEB_UI_FILEIO.md)
- [Test Coverage Matrix](claude_if_you_read_in_here_you_loop/TEST_COVERAGE_MATRIX.md)
- [Test Inventory](claude_if_you_read_in_here_you_loop/TEST_INVENTORY.md)
- [Test Run Results 2025-11-02](claude_if_you_read_in_here_you_loop/TEST_RUN_RESULTS_2025-11-02.md)
- [Tk Editor Completion Summary](claude_if_you_read_in_here_you_loop/TK_EDITOR_COMPLETION_SUMMARY.md)
- [Tk Editor Current State](claude_if_you_read_in_here_you_loop/TK_EDITOR_CURRENT_STATE.md)
- [Tk Ui Changes For Other Uis](claude_if_you_read_in_here_you_loop/TK_UI_CHANGES_FOR_OTHER_UIS.md)
- [Tk Ui Enhancement Plan](claude_if_you_read_in_here_you_loop/TK_UI_ENHANCEMENT_PLAN.md)
- [Tk Ui Feature Audit](claude_if_you_read_in_here_you_loop/TK_UI_FEATURE_AUDIT.md)
- [Ui Consolidation Status](claude_if_you_read_in_here_you_loop/UI_CONSOLIDATION_STATUS.md)
- [Ui Development Guide](claude_if_you_read_in_here_you_loop/UI_DEVELOPMENT_GUIDE.md)
- [Ui Feature Parity](claude_if_you_read_in_here_you_loop/UI_FEATURE_PARITY.md)
- [Ui Feature Parity Checklist](claude_if_you_read_in_here_you_loop/UI_FEATURE_PARITY_CHECKLIST.md)
- [Ui Feature Parity Tracking](claude_if_you_read_in_here_you_loop/UI_FEATURE_PARITY_TRACKING.md)
- [Ui Helpers Guide](claude_if_you_read_in_here_you_loop/UI_HELPERS_GUIDE.md)
- [Urwid Completion](claude_if_you_read_in_here_you_loop/URWID_COMPLETION.md)
- [Variable Editing Feature](claude_if_you_read_in_here_you_loop/VARIABLE_EDITING_FEATURE.md)
- [Variable Editing Standardization](claude_if_you_read_in_here_you_loop/VARIABLE_EDITING_STANDARDIZATION.md)
- [Variable Editing Status](claude_if_you_read_in_here_you_loop/VARIABLE_EDITING_STATUS.md)
- [Variable Tracking](claude_if_you_read_in_here_you_loop/VARIABLE_TRACKING.md)
- [Variable Tracking Changes](claude_if_you_read_in_here_you_loop/VARIABLE_TRACKING_CHANGES.md)
- [Variable Type Suffix Behavior](claude_if_you_read_in_here_you_loop/VARIABLE_TYPE_SUFFIX_BEHAVIOR.md)
- [Visual Ui Editor Enhancement](claude_if_you_read_in_here_you_loop/VISUAL_UI_EDITOR_ENHANCEMENT.md)
- [Web Architecture Refactor Todo](claude_if_you_read_in_here_you_loop/WEB_ARCHITECTURE_REFACTOR_TODO.md)
- [Web Ui Dialog Pattern](claude_if_you_read_in_here_you_loop/WEB_UI_DIALOG_PATTERN.md)
- [Web Ui Editor Enhancements](claude_if_you_read_in_here_you_loop/WEB_UI_EDITOR_ENHANCEMENTS.md)
- [Web Ui Feature Parity](claude_if_you_read_in_here_you_loop/WEB_UI_FEATURE_PARITY.md)
- [Web Ui Fixes 2025 10 30](claude_if_you_read_in_here_you_loop/WEB_UI_FIXES_2025_10_30.md)
- [Web Ui Fixes 2025 10 30 Part2](claude_if_you_read_in_here_you_loop/WEB_UI_FIXES_2025_10_30_PART2.md)
- [Web Ui Implementation](claude_if_you_read_in_here_you_loop/WEB_UI_IMPLEMENTATION.md)
- [Web Ui Options](claude_if_you_read_in_here_you_loop/WEB_UI_OPTIONS.md)
- [Web Ui Real Options](claude_if_you_read_in_here_you_loop/WEB_UI_REAL_OPTIONS.md)
- [Web Ui Testing Checklist](claude_if_you_read_in_here_you_loop/WEB_UI_TESTING_CHECKLIST.md)
- [Web Ui Verification Results](claude_if_you_read_in_here_you_loop/WEB_UI_VERIFICATION_RESULTS.md)
- [While Loop Stack Behavior](claude_if_you_read_in_here_you_loop/WHILE_LOOP_STACK_BEHAVIOR.md)
- [Work In Progress](claude_if_you_read_in_here_you_loop/WORK_IN_PROGRESS.md)
- [Work In Progress Template](claude_if_you_read_in_here_you_loop/WORK_IN_PROGRESS_TEMPLATE.md)
- [Test Bp Ui Debug](claude_if_you_read_in_here_you_loop/test_bp_ui_debug.md)

## See Also

- [MBASIC Help](../help/mbasic/index.md) - User-facing documentation
- Search function (top of page) - Find docs by keyword
