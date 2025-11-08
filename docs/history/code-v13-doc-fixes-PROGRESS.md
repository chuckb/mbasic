# Documentation Fixes Progress (code-v13)

## Summary

**Total documentation issues:** 97
**Fixed:** 8
**Remaining:** 89

## Completed Fixes

### 1. ✅ Keyboard Shortcut Inconsistencies (3 files)

**File:** `docs/help/common/editor-commands.md`
- Removed incorrect plain 'b' key for Load and Breakpoint
- Fixed to show only Ctrl+O (load) and Ctrl+B (breakpoint)
- Added UI-specific notes for different shortcuts (e.g., Curses uses Ctrl+V for save)
- Corrected debugging commands table with UI-specific annotations

**File:** `docs/help/common/debugging.md`
- Fixed Curses breakpoint toggle from plain 'b' to **Ctrl+B**
- Now consistent with actual keybindings (src/ui/curses_keybindings.json)

### 2. ✅ Example Code Errors (2 files)

**File:** `docs/help/common/language/statements/renum.md`
- Fixed Example 1 which showed unchanged output after RENUM
- Now uses irregular line numbers (10, 25, 40, 60) as input
- Shows clear before/after with GOTO reference update

**File:** `docs/help/common/language/functions/oct_dollar.md`
- Fixed PRINT statement missing semicolons
- Changed from: `PRINT X "DECIMAL IS " A$ " OCTAL"` (syntax error)
- Changed to: `PRINT X; "DECIMAL IS "; A$; " OCTAL"` (correct)
- Now consistent with HEX$ example style

### 3. ✅ Numeric Range Inconsistencies (1 file)

**File:** `docs/help/common/language/functions/cdbl.md`
- Fixed double-precision range (was showing single-precision range)
- Changed from: 2.938735877055719 x 10^-39 to 1.701411834604692 x 10^38
- Changed to: 2.938736×10^-308 to 1.797693×10^308
- Now consistent with data-types.md

### 4. ✅ Error Code Format (1 file)

**File:** `docs/help/common/language/functions/cvi-cvs-cvd.md`
- Fixed error code format from "FC/5" to "FC"
- Now consistent with error-codes.md table format

### 5. ✅ Code Comment Fixes (2 files)

**File:** `src/ui/tk_widgets.py:323`
- Fixed `_on_status_click()` docstring
- Changed "breakpoint info" to "confirmation message"
- Accurate description of actual behavior

**File:** `src/ui/curses_ui.py:3843`
- Clarified comment about PC reset when paused at breakpoint
- Removed confusing/backwards explanation
- Added clear explanation of breakpoint PC storage

## Remaining Work (89 issues)

### High Priority (~30 issues)

#### Cross-Reference and Link Issues
- Broken links to non-existent sections
- Incorrect file references (e.g., printi-printi-using.md)
- Missing cross-references between related topics
- Inconsistent See Also sections

#### Feature Status Contradictions
- Variable editing in Curses (completely unavailable vs partially implemented)
- Find/Replace availability (implemented vs not implemented vs planned)
- Settings dialog status (Tk UI has vs doesn't have)
- LPRINT support (supported vs not mentioned)
- CLS and LOCATE commands status unclear

#### Keyboard Shortcut Issues
- Ctrl+X conflict in Tk UI documentation
- Variables Window: Ctrl+V (debugging.md) vs Ctrl+W (tk_keybindings.json)
- Execution Stack: different shortcuts across documents
- Cut/Copy/Paste inconsistencies
- Settings dialog access methods

### Medium Priority (~35 issues)

#### UI-Specific Documentation
- Feature count mismatches (37 vs 31 in Tk documentation)
- Implementation status contradictions between UIs
- Default UI inconsistencies
- UI capability comparisons need updates
- Web UI file storage details need consistency

#### Implementation Notes
- Formatting inconsistencies across similar statements
- Detail level varies (some verbose, some sparse)
- Some notes say "not implemented" but features exist
- Platform-specific limitations not clearly marked

### Low Priority (~24 issues)

#### Example and Formatting Issues
- STRING$ output formatting
- DEFINT/SNG/DBL/STR precedence not clearly explained
- CLOAD/CSAVE VT180 version notes formatting
- PI computation precision note wording differences
- RSET vs RESET name similarity not addressed

#### Documentation Organization
- Duplicate basic language information
- Index categorization debatable in some cases
- README organization vs actual file structure
- Settings file location documentation (~/path notation)

## Verification Needed

Some reported issues may not be actual problems:
- ✅ **CLI backend** - Exists (src/ui/cli.py), documentation is correct
- **LPRINT** - Need to verify if implemented or not
- **Web UI features** - Need to check actual implementation status
- **File persistence** - Need to verify behavior across UIs

## Approach for Remaining Work

### Phase 1: Cross-References (Est. 3-4 hours)
1. Extract all broken links programmatically
2. Fix file references and See Also sections
3. Verify all links point to existing files
4. Update index files with correct links

### Phase 2: Feature Status (Est. 4-5 hours)
1. Check actual implementation for each disputed feature
2. Update all documentation to match reality
3. Ensure consistency across UI-specific docs
4. Mark clearly what's implemented/partial/planned

### Phase 3: Keyboard Shortcuts (Est. 2-3 hours)
1. Create master keyboard shortcut matrix from JSON files
2. Update all documentation to match actual bindings
3. Add UI-specific notes where shortcuts differ
4. Fix conflicts and contradictions

### Phase 4: Examples and Formatting (Est. 2-3 hours)
1. Fix remaining example code errors
2. Standardize formatting across similar docs
3. Update implementation note templates
4. Clarify precedence and edge cases

### Phase 5: Organization (Est. 2-3 hours)
1. Remove duplicate content
2. Improve index organization
3. Add missing cross-references
4. Update README files

## Tools Available

- `utils/list_doc_fixes.py` - Lists issues grouped by file
- `docs/history/code-v13-doc-fixes.txt` - Detailed issue descriptions
- `src/ui/curses_keybindings.json` - Curses keyboard bindings
- `src/ui/tk_keybindings.json` - Tk keyboard bindings

## Recommendation

**Option 1: Complete manually** (~15-20 hours total)
- Systematic, file-by-file approach
- High quality, thorough fixes
- Time-consuming but complete

**Option 2: Batch process patterns** (~8-12 hours)
- Create scripts to fix common patterns
- Manual review for complex cases
- Faster but requires validation

**Option 3: Prioritize user-facing** (~5-8 hours)
- Fix only issues users are likely to encounter
- Focus on getting-started, common commands
- Leave advanced topics for later

**Recommended: Option 2** - Batch process where possible, manual for complex cases

## Files Modified So Far

1. `docs/help/common/editor-commands.md`
2. `docs/help/common/debugging.md`
3. `docs/help/common/language/statements/renum.md`
4. `docs/help/common/language/functions/oct_dollar.md`
5. `docs/help/common/language/functions/cdbl.md`
6. `docs/help/common/language/functions/cvi-cvs-cvd.md`
7. `src/ui/tk_widgets.py`
8. `src/ui/curses_ui.py`

## Next Steps

1. Continue with cross-reference fixes (high impact, relatively mechanical)
2. Create keyboard shortcut master matrix from JSON files
3. Batch process feature status issues by checking implementation
4. Tackle remaining example fixes
5. Final pass for formatting consistency

**Estimated time to completion: 10-15 hours of focused work**
