# Documentation Inconsistencies Report v11 - Complete Analysis

**Report File:** `/home/wohl/cl/mbasic/docs/history/docs_inconsistencies_report-v11.md`
**Generated:** 2025-11-06 04:33:42
**Total Lines:** 4806

---

## Executive Summary

### Issue Counts by Severity

| Severity | Count | Percentage |
|----------|-------|------------|
| **High** | 20 | 8.0% |
| **Medium** | 101 | 40.2% |
| **Low** | 130 | 51.8% |
| **TOTAL** | 251 | 100% |

### Issue Types (Top 10)

| Issue Type | Count |
|------------|-------|
| code_vs_comment | 154 |
| documentation_inconsistency | 43 |
| code_vs_comment_conflict | 10 |
| Code vs Documentation inconsistency | 10 |
| code_vs_documentation | 8 |
| Code vs Comment conflict | 7 |
| Documentation inconsistency | 5 |
| code_internal_inconsistency | 4 |
| code_inconsistency | 4 |
| code_vs_documentation_inconsistency | 3 |

---

## High Severity Issues (20 total)

### Critical Code/Comment Conflicts - Immediate Attention Required

#### 1. src/case_string_handler.py (1 issue)
- **Lines 13-33:** Comment claims identifiers preserve case but implementation returns original_text without using identifier_table
  - Type: code_vs_comment

#### 2. src/editing/manager.py (1 issue)
- **Lines 34-53:** Contradictory documentation about ProgramManager file I/O methods (with src/file_io.py)
  - Type: documentation_inconsistency

#### 3. src/immediate_executor.py (1 issue)
- **Lines 54-82:** Comment describes validation behavior that doesn't exist in the code
  - Type: code_vs_comment

#### 4. src/interactive.py (2 issues)
- **Lines 83-104:** RENUM documentation claims conservative behavior but implementation may incorrectly renumber arithmetic
  - Type: code_vs_comment
- **Lines 105-123:** CONT command docstring doesn't mention GOSUB/FOR stack clearing on edit
  - Type: code_vs_comment

#### 5. src/interpreter.py (3 issues)
- **Lines 124-158:** Comment about error_info being set contradicts actual flow
  - Type: code_vs_comment
- **Lines 159-181:** Comment about 'bare except: pass below' but code is right there, not 'below'
  - Type: code_vs_comment
- **Lines 182-201:** Comment describes behavior distinction but doesn't verify it works
  - Type: code_vs_comment

#### 6. src/parser.py (1 issue)
- **Lines 202-223:** Docstring incomplete for INPUT statement (missing INPUT; and LINE modifier)
  - Type: code_vs_comment

#### 7. src/ui/curses_ui.py (5 issues)
- **Lines 224-244:** Comment claims fixed 5-char width but code uses variable width
  - Type: code_vs_comment
- **Lines 245-264:** Inconsistent line number formatting between methods
  - Type: internal_inconsistency
- **Lines 265-280:** Contradictory comments about main widget storage
  - Type: code_vs_comment
- **Lines 281-297:** Comment about PC reset contradicts implementation
  - Type: code_vs_comment
- **Lines 298-315:** Comment contradicts itself about interpreter.start() calls
  - Type: code_vs_comment

#### 8. src/ui/help_widget.py (1 issue)
- **Lines 316-336:** Comment claims keys are hardcoded but HelpMacros loads keybindings
  - Type: code_vs_comment_conflict

#### 9. src/ui/tk_ui.py (3 issues)
- **Lines 337-363:** Comment about OPTION BASE invalid value handling unclear
  - Type: code_vs_comment
- **Lines 364-386:** Code uses stop_line/stop_stmt_index without checking if they exist
  - Type: code_vs_comment
- **Lines 387-404:** Comment says don't call start() but then manually replicates it
  - Type: code_vs_comment

#### 10. src/ui/tk_widgets.py (1 issue)
- **Lines 405-420:** Misleading comment about pixels in Tkinter
  - Type: code_vs_comment

#### 11. src/ui/ui_helpers.py (1 issue)
- **Lines 421-441:** Fallback creates REM comments with WARNING but no error handling
  - Type: code_vs_comment

---

## Medium Severity Issues (101 total)

### Files with Most Medium Severity Issues

#### src/ui/tk_ui.py (14 issues)
- Lines: 2046-2069, 2070-2087, 2088-2111, 2112-2132, 2133-2149, 2150-2169, 2170-2190, 2191-2212, 2213-2229, 2230-2258, 2259-2276, 2277-2293, 2294-2308, 2309-2323

#### src/interpreter.py (13 issues)
- Lines: 763-788, 789-815, 816-848, 849-875, 876-895, 896-918, 919-937, 938-961, 962-980, 981-1002, 1013-1030, 1031-1045, 2945-2960

#### src/ui/curses_ui.py (12 issues)
- Lines: 1649-1667, 1668-1686, 1687-1705, 1706-1735, 1736-1758, 1759-1775, 1776-1800, 1801-1827, 1828-1846, 1847-1864, 1865-1897, 1898-1932

#### src/parser.py (10 issues)
- Lines: 1148-1168, 1169-1190, 1191-1211, 1212-1226, 1227-1241, 1242-1259, 1260-1280, 1281-1298, 1299-1313, 1314-1330

#### src/interactive.py (5 issues)
- Lines: 670-685, 686-701, 702-716, 717-742, 743-762

#### src/runtime.py (4 issues)
- Lines: 1431-1453, 1454-1475, 1476-1507, 1508-1528

#### src/ui/keybindings.py (4 issues)
- Lines: 1949-1964, 1965-1984, 1985-2005, 2006-2027

#### src/basic_builtins.py (3 issues)
- Lines: 503-516, 517-535, 536-551

#### src/lexer.py (3 issues)
- Lines: 1091-1105, 1106-1127, 1128-1147

#### src/position_serializer.py (3 issues)
- Lines: 1344-1360, 1361-1377, 1378-1393

#### src/immediate_executor.py (3 issues)
- Lines: 614-629, 630-646, 647-669

#### src/ui/ui_helpers.py (3 issues)
- Lines: 2369-2383, 2384-2399, 2400-2418

#### src/ui/tk_widgets.py (3 issues)
- Lines: 2323-2338, 2339-2352, 2353-2368

#### Other files with 1-2 medium issues:
- src/ast_nodes.py (2): Lines 460-480, 481-502
- src/resource_limits.py (2): Lines 1394-1408, 1409-1430
- src/editing/manager.py (1): Lines 592-613
- src/file_io.py (1): Lines 552-572, 573-592
- src/filesystem/sandboxed_fs.py (1): Lines 552-572
- src/pc.py (1): Lines 1331-1343
- src/ui/cli_debug.py (3): Lines 1583-1604, 1605-1628, 1629-1649
- src/ui/help_macros.py (2): Lines 1898-1914, 1915-1932
- src/ui/interactive_menu.py (1): Lines 1915-1932
- src/ui/keymap_widget.py (1): Lines 2006-2027
- src/ui/tk_help_browser.py (1): Lines 2028-2045
- And others...

---

## Low Severity Issues (130 total)

### Files with Most Low Severity Issues

#### src/interpreter.py (11 issues)
- Lines: 2775-2797, 2798-2816, 2832-2851, 2852-2867, 2868-2884, 2885-2902, 2903-2916, 2917-2935, 2936-2947, 2948-2960, 3958-3977

#### src/ui/tk_ui.py (11 issues)
- Lines: 4111-4119, 4120-4142, 4143-4159, 4160-4183, 4184-4198, 4199-4217, 4218-4239, 4240-4256, 4257-4277, 4278-4291, 4292-4310

#### src/parser.py (11 issues)
- Lines: 3164-3189, 3190-3214, 3215-3233, 3234-3253, 3254-3271, 3272-3287, 3288-3306, 3307-3327, 3328-3346, 3347-3370, 3371-3391

#### src/ui/curses_ui.py (10 issues)
- Lines: 3730-3746, 3747-3774, 3796-3817, 3818-3834, 3930-3945, 3946-3964, 3965-3986, 3987-4004, 4005-4023, 4024-4043

#### src/runtime.py (7 issues)
- Lines: 3526-3542, 3543-3563, 3564-3581, 3582-3598, 3599-3615, 3616-3631, 3632-3649

#### src/ui/keybindings.py (7 issues)
- Lines: 4183-4198, 4199-4217, 4218-4232, 4233-4251, 4252-4270, 4271-4286, 4287-4301

#### Other files with 3-7 low severity issues:
- src/ast_nodes.py (4): Lines 2435-2455, 2456-2474, 2475-2494, 2495-2518
- src/basic_builtins.py (4): Lines 2519-2532, 2533-2549, 2550-2564, 2565-2582
- src/lexer.py (4): Lines 3086-3106, 3107-3124, 3125-3143, 3144-3164
- src/position_serializer.py (4): Lines 3392-3405, 3406-3419, 3420-3436, 3437-3451
- src/resource_limits.py (4): Lines 3452-3470, 3471-3486, 3487-3510, 3511-3525
- src/immediate_executor.py (2): Lines 2659-2677, 2678-2708
- src/interactive.py (4): Lines 2709-2727, 2728-2739, 2740-2754, 2755-2774
- src/ui/ui_helpers.py (5): Lines 4682-4699, 4700-4717, 4718-4732, 4733-4750, 4751-4770
- src/ui/tk_widgets.py (3): Lines 4634-4649, 4650-4668, 4669-4681

And many other files with 1-3 low severity issues each.

---

## Issues by Affected File (Top 30)

| Rank | File | Total | High | Med | Low | Line Ranges in Report |
|------|------|-------|------|-----|-----|----------------------|
| 1 | src/ui/tk_ui.py | 28 | 3 | 14 | 11 | 337-363, 364-386, 387-404... |
| 2 | src/interpreter.py | 27 | 3 | 13 | 11 | 124-158, 159-181, 182-201... |
| 3 | src/ui/curses_ui.py | 27 | 5 | 12 | 10 | 224-244, 245-264, 265-280... |
| 4 | src/parser.py | 22 | 1 | 10 | 11 | 202-223, 1148-1168, 1169-1190... |
| 5 | src/interactive.py | 11 | 2 | 5 | 4 | 83-104, 105-123, 670-685... |
| 6 | src/runtime.py | 11 | 0 | 4 | 7 | 1431-1453, 1454-1475, 1476-1507... |
| 7 | src/ui/keybindings.py | 11 | 0 | 4 | 7 | 1949-1964, 1965-1984, 1985-2005... |
| 8 | src/ui/ui_helpers.py | 9 | 1 | 3 | 5 | 421-441, 2369-2383, 2384-2399... |
| 9 | src/ui/tk_widgets.py | 7 | 1 | 3 | 3 | 405-420, 2323-2338, 2339-2352... |
| 10 | src/basic_builtins.py | 7 | 0 | 3 | 4 | 503-516, 517-535, 536-551... |
| 11 | src/lexer.py | 7 | 0 | 3 | 4 | 1091-1105, 1106-1127, 1128-1147... |
| 12 | src/position_serializer.py | 7 | 0 | 3 | 4 | 1344-1360, 1361-1377, 1378-1393... |
| 13 | src/immediate_executor.py | 6 | 1 | 3 | 2 | 54-82, 614-629, 630-646... |
| 14 | src/ast_nodes.py | 6 | 0 | 2 | 4 | 460-480, 481-502, 2435-2455... |
| 15 | src/resource_limits.py | 6 | 0 | 2 | 4 | 1394-1408, 1409-1430, 3452-3470... |
| 16 | src/ui/tk_help_browser.py | 5 | 0 | 1 | 4 | 2028-2045, 4311-4326, 4327-4347... |
| 17 | src/ui/help_widget.py | 4 | 1 | 1 | 2 | 316-336, 1932-1948, 4120-4142... |
| 18 | src/settings.py | 4 | 0 | 1 | 3 | 1529-1545, 3674-3687, 3688-3704... |
| 19 | src/ui/cli_debug.py | 4 | 0 | 3 | 1 | 1583-1604, 1605-1628, 1629-1649... |
| 20 | src/ui/curses_settings_widget.py | 4 | 0 | 0 | 4 | 3835-3855, 3856-3872, 3892-3913... |

---

## Systematic Fixing Strategy

### Phase 1: High Severity (20 issues - Est. 2-3 days)

**Priority Order by File Impact:**

1. **src/ui/curses_ui.py** (5 issues, lines 224-336)
   - Fix line number formatting inconsistencies
   - Resolve widget storage contradictions
   - Clarify PC reset and interpreter.start() behavior

2. **src/interpreter.py** (3 issues, lines 124-201)
   - Fix error_info flow documentation
   - Correct except: pass comment placement
   - Add verification for behavior distinction

3. **src/ui/tk_ui.py** (3 issues, lines 337-404)
   - Fix OPTION BASE documentation
   - Add existence checks for stop_line/stop_stmt_index
   - Clarify interpreter.start() replication logic

4. **src/interactive.py** (2 issues, lines 83-123)
   - Fix RENUM ERL expression documentation
   - Document GOSUB/FOR stack clearing in CONT

5. **Remaining single-issue files** (7 issues)
   - src/case_string_handler.py
   - src/editing/manager.py + src/file_io.py
   - src/immediate_executor.py
   - src/parser.py
   - src/ui/help_widget.py
   - src/ui/tk_widgets.py
   - src/ui/ui_helpers.py

### Phase 2: Medium Severity (101 issues - Est. 5-7 days)

**Batch by file to maximize efficiency:**

**Week 1:**
- src/ui/tk_ui.py: 14 issues (lines 2046-2323)
- src/interpreter.py: 13 issues (lines 763-1045, 2945-2960)
- src/ui/curses_ui.py: 12 issues (lines 1649-1932)

**Week 2:**
- src/parser.py: 10 issues (lines 1148-1330)
- src/interactive.py: 5 issues (lines 670-762)
- src/runtime.py: 4 issues (lines 1431-1528)
- src/ui/keybindings.py: 4 issues (lines 1949-2027)

**Week 3:**
- All remaining files with 1-3 medium issues each

### Phase 3: Low Severity (130 issues - Est. 7-10 days)

**Group by common patterns:**

**Batch 1 - Code vs Comment (63 issues):**
- Process all code_vs_comment issues file by file
- Priority: src/interpreter.py (11), src/ui/tk_ui.py (11), src/parser.py (11)

**Batch 2 - Documentation Inconsistencies (37 issues):**
- Standardize terminology and phrasing
- Focus on API documentation clarity

**Batch 3 - Remaining types (30 issues):**
- code_vs_comment_conflict (6)
- Code vs Comment conflict (6)
- Code vs Documentation inconsistency (6)
- Others (12)

---

## Issue Type Definitions

### code_vs_comment (154 issues)
Comments that contradict, are incomplete, or don't match the actual code implementation.

### documentation_inconsistency (43 issues)
Inconsistent terminology, contradictory documentation across files, or version numbering issues.

### code_vs_comment_conflict (10 issues)
Serious conflicts where code and comments describe completely different behavior.

### Code vs Documentation inconsistency (10 issues)
Mismatches between code implementation and external/API documentation.

### code_vs_documentation (8 issues)
Documentation claims features or behavior that code doesn't implement.

### code_internal_inconsistency (4 issues)
Code implements the same concept differently in different places (e.g., autosave interval hardcoded).

### internal_inconsistency (1 issue)
Internal implementation contradictions.

---

## Testing Strategy After Fixes

1. **After each HIGH severity fix:**
   - Run full test suite
   - Manual test affected functionality
   - Verify comments now match code

2. **After each file in MEDIUM batch:**
   - Run tests for that module
   - Check for regressions
   - Commit per file

3. **After LOW severity batches:**
   - Automated documentation checks
   - Sample testing
   - Batch commits by issue type

---

## Tools for Systematic Fixing

### Recommended Workflow

```bash
# For each issue, view context in report
sed -n '<start_line>,<end_line>p' docs/history/docs_inconsistencies_report-v11.md

# Edit affected file(s)
# Run tests
# Commit with reference to report line numbers
```

### Commit Message Format

```
Fix docs inconsistency: <brief description>

- Report: docs_inconsistencies_report-v11.md lines <start>-<end>
- Severity: <High/Medium/Low>
- Type: <issue_type>
- Files: <affected files>

<Details of the fix>
```

---

## Estimated Timeline

- **Phase 1 (High):** 2-3 days (20 issues)
- **Phase 2 (Medium):** 5-7 days (101 issues)
- **Phase 3 (Low):** 7-10 days (130 issues)

**Total estimated time:** 14-20 days of focused work

**Recommended pace:** Fix 15-20 issues per day to complete in ~2-3 weeks
