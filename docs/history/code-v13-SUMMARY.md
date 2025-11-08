# Code v13 Processing Summary

## Overview

Processed `docs/history/docs_inconsistencies_report-v13.md` (426 issues total) and split into:

1. **docs-v13.md** (276 issues) - Documentation/comment fixes only
2. **code-v13.md** (150 issues) - Code behavior changes required

## Work Completed

### 1. Split and Categorized All Issues (150 code issues)

Created categorization of all 150 code issues:
- **Global changes (23 issues)** → Extracted to `code-global-v13.md` for review
- **Safe UI/shared fixes (126 issues)** → Can be fixed without breaking UIs
- **Comment-only fixes (5 issues)** → Subset of above, in global files

### 2. Extracted Global Changes for Review

**File:** `docs/history/code-global-v13.md`

Contains 23 issues affecting interpreter/runtime/interactive code that impact ALL UIs:
- 3 High severity (including security validation issue)
- 12 Medium severity
- 8 Low severity

**These require careful review before implementation.**

### 3. Applied Safe Fixes (8 fixes completed)

#### Code Comment Fixes (2 fixes)
1. ✅ `src/ui/tk_widgets.py:323`
   - Fixed `_on_status_click()` docstring
   - Changed "breakpoint info" to "confirmation message"
   - Accurate description of what the function actually does

2. ✅ `src/ui/curses_ui.py:3843`
   - Clarified comment about PC reset logic when paused at breakpoint
   - Removed confusing/backwards explanation
   - Added clear explanation of breakpoint PC storage

#### Documentation Fixes (6 fixes)
3. ✅ `docs/help/common/editor-commands.md`
   - Fixed keyboard shortcut table (removed incorrect plain 'b' keys)
   - Added UI-specific annotations for different shortcuts

4. ✅ `docs/help/common/debugging.md`
   - Fixed Curses breakpoint toggle from 'b' to 'Ctrl+B'

5. ✅ `docs/help/common/language/statements/renum.md`
   - Fixed misleading Example 1 showing unchanged output

6. ✅ `docs/help/common/language/functions/oct_dollar.md`
   - Fixed PRINT statement syntax (added missing semicolons)

7. ✅ `docs/help/common/language/functions/cdbl.md`
   - Fixed double-precision range values (was showing single-precision range)

8. ✅ `docs/help/common/language/functions/cvi-cvs-cvd.md`
   - Fixed error code format from "FC/5" to "FC"

### 4. Created Helper Tools

**Scripts created in `utils/`:**
- `split_report.py` - Split original report into docs/code files
- `categorize_code_issues.py` - Categorize issues by safety/scope
- `extract_global_issues.py` - Extract global issues to separate file
- `list_doc_fixes.py` - List and group documentation fixes

**Tracking documents created:**
- `code-v13-fix-tracking.md` - Overall progress tracker
- `code-v13-categorized.txt` - Categorized issue list
- `code-v13-doc-fixes.txt` - Detailed documentation fixes by file

## Remaining Work

### A. Global Changes (23 issues) - REQUIRES REVIEW

**File:** `docs/history/code-global-v13.md`

**Priority order:**
1. **High: Security** - `src/filesystem/sandboxed_fs.py` user_id validation
2. **High: Logic errors** - Validation flow mismatches, PC reset logic
3. **High: Known bugs** - ERL renumbering behavior documented as "acceptable"
4. **Medium: Error handling** - CLEAR vs RESET inconsistency
5. **Medium: Implementation gaps** - Missing features, stub methods
6. **Low: Comment clarifications** - Runtime, settings, etc.

**Do not implement without review!**

### B. Safe Fixes (126 issues) - CAN DO NOW

**Categories:**

#### Documentation (97 issues) ← LARGEST GROUP
**File:** `docs/history/code-v13-doc-fixes.txt`

Most common issues:
- Cross-reference inconsistencies (broken links, wrong targets)
- Keyboard shortcut documentation conflicts
- Feature status contradictions (implemented vs not implemented)
- UI capability inconsistencies
- Example code errors
- Formatting inconsistencies

**Top files needing fixes:**
- `docs/help/ui/tk/feature-reference.md` (13 issues)
- `docs/help/mbasic/features.md` (10 issues)
- `docs/help/ui/tk/features.md` (6 issues)
- `docs/help/mbasic/extensions.md` (5 issues)

**Recommended approach:**
1. Pick one UI documentation section at a time
2. Read through all files in that section
3. Cross-reference with actual implementation
4. Fix all inconsistencies in one pass
5. Test links and cross-references

#### UI Code (approx. 20 issues)
- Docstring updates (mostly Tk and Web UIs)
- Comment clarifications
- Implementation status updates
- Error message improvements

**Safe to fix** - these don't change behavior, just documentation/comments.

#### Shared Infrastructure (approx. 9 issues)
- `src/file_io.py` docstring clarifications
- `src/filesystem/` comment updates
- `src/iohandler/` implementation notes

**Mostly safe** but verify each one doesn't reveal a code issue.

### C. Verification Needed

Some issues marked as "safe" may actually reveal implementation questions:
- Is feature X actually implemented?
- What's the correct behavior for edge case Y?
- Which documentation is right when they conflict?

**When you encounter these:**
1. Check the actual code implementation
2. Test if possible
3. Update ALL related docs to match reality
4. If implementation is wrong, move to global review

## Next Steps

### Immediate (Do Now)
1. Review `code-global-v13.md` and prioritize global changes
2. Fix high-priority security and logic issues
3. Start working through documentation fixes systematically

### Short Term
1. Fix remaining UI-specific code comments/docstrings
2. Complete documentation consistency pass
3. Test fixes don't break existing functionality

### Tools Available
- Use `utils/list_doc_fixes.py` to see documentation issues by file
- Use `code-v13-fix-tracking.md` to track progress
- Mark fixes complete in tracking doc as you go

## Key Insights

1. **Documentation needs major consistency pass**
   - 97 documentation issues across ~80 files
   - Many cross-references are broken or inconsistent
   - Feature status often contradictory

2. **Most code issues are safe comment/docstring fixes**
   - Only 23 truly global changes need careful review
   - 126 issues are UI-specific or clearly safe

3. **Security issue needs immediate attention**
   - `src/filesystem/sandboxed_fs.py` user_id validation
   - Documentation warns but code doesn't enforce

4. **Some issues aren't actually problems**
   - CLI backend DOES exist (contrary to one issue claim)
   - Some documentation accurately describes stubs
   - Verification needed before "fixing" some issues

## Files Modified

### Code Files (2)
- `src/ui/tk_widgets.py` - Docstring fix
- `src/ui/curses_ui.py` - Comment clarification

### Documentation Files (6)
- `docs/help/common/editor-commands.md` - Keyboard shortcuts
- `docs/help/common/debugging.md` - Keyboard shortcuts
- `docs/help/common/language/statements/renum.md` - Example fix
- `docs/help/common/language/functions/oct_dollar.md` - Example fix
- `docs/help/common/language/functions/cdbl.md` - Range values
- `docs/help/common/language/functions/cvi-cvs-cvd.md` - Error code format

## Files Created

### Tracking Documents
- `docs/history/code-global-v13.md` - Global changes requiring review (23 issues)
- `docs/history/code-v13-fix-tracking.md` - Overall progress tracker
- `docs/history/code-v13-doc-fixes-PROGRESS.md` - Detailed documentation fix progress
- `docs/history/code-v13-categorized.txt` - Categorized issue list
- `docs/history/code-v13-doc-fixes.txt` - Documentation fixes by file (97 issues)

### Helper Scripts
- `utils/split_report.py` - Split original report into docs/code
- `utils/categorize_code_issues.py` - Categorize issues by safety/scope
- `utils/extract_global_issues.py` - Extract global issues
- `utils/list_doc_fixes.py` - List documentation fixes by file

## Conclusion

### Current Status
- ✅ **8/150 code issues fixed** (2 code comments, 6 documentation)
- ✅ **All issues categorized and organized**
- ✅ **Global changes extracted for review** (23 issues in code-global-v13.md)
- 🔄 **89/97 documentation issues remaining**
- 🔄 **~20 UI code comment fixes remaining**

### Work is Well-Organized
- **Global changes** documented in code-global-v13.md - ready for review
- **Documentation fixes** listed by file in code-v13-doc-fixes.txt
- **Progress tracking** in code-v13-doc-fixes-PROGRESS.md
- **Helper tools** available for batch processing

### Focus Areas (Priority Order)
1. **First:** Review and fix global changes (23 issues) - **Requires careful review**
2. **Second:** Documentation fixes (89 remaining)
   - Cross-references and broken links (~20 issues) - High impact
   - Feature status contradictions (~30 issues) - User confusion
   - Keyboard shortcuts (~15 issues) - Quick wins
   - Examples and formatting (~24 issues) - Polish
3. **Third:** UI code comment/docstring fixes (~20 issues) - Straightforward

### Estimated Remaining Effort
- Global changes: 4-8 hours (requires testing across all UIs)
- Documentation: 10-15 hours (see code-v13-doc-fixes-PROGRESS.md for detailed breakdown)
- UI code fixes: 2-4 hours (comment/docstring updates only)

**Remaining: ~15-25 hours of focused work**

### Recommended Next Steps
1. Review `docs/history/code-global-v13.md` for high-priority global fixes
2. Continue documentation fixes using systematic approach in code-v13-doc-fixes-PROGRESS.md
3. Complete remaining UI comment fixes as encountered during development

**See `docs/history/code-v13-doc-fixes-PROGRESS.md` for detailed documentation fix roadmap.**
