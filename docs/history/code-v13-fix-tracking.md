# Code v13 Fix Tracking

## Summary

Total issues in code-v13.md: **150**
- Global changes (requiring review): **23** → Documented in `code-global-v13.md`
- Safe UI/shared code fixes: **126**
- Comment-only fixes: **5** (subset of above, in global files)

## Fixes Completed

### UI Code Fixes
1. ✅ `src/ui/tk_widgets.py:323` - Fixed `_on_status_click()` docstring to say "confirmation message" instead of "breakpoint info"
2. ✅ `src/ui/curses_ui.py:3843` - Clarified comment about PC reset logic when paused at breakpoint

### Documentation Fixes
3. ✅ `docs/help/common/language/functions/cvi-cvs-cvd.md:24` - Fixed error code format from "FC/5" to "FC"

## Fixes Remaining (126 total)

### Category Breakdown

#### Documentation Inconsistencies (~80 issues)
Files primarily in `docs/help/`:
- Variable name significance vs case sensitivity clarification needed
- File persistence behavior across different UIs needs consistent documentation
- Web UI storage limits need consistent documentation across files
- LPRINT support clarification needed
- Curses UI variable editing capability contradictions
- Many more cross-reference and consistency issues

**Recommended approach:**
- Create a script to extract all affected files
- Review each documentation file systematically
- Cross-reference with actual implementation
- Update all docs consistently

#### UI-Specific Code Issues (~30 issues)
Files in `src/ui/`:
- Docstring inaccuracies
- Comment clarifications
- Implementation status updates
- Error message improvements

**Recommended approach:**
- Fix these manually as they're discovered during development
- Or batch-process by reviewing each UI backend file

#### Shared/Infrastructure Code (~16 issues)
Files like `src/file_io.py`, `src/filesystem/`, `src/iohandler/`:
- Minor docstring updates
- Comment clarifications
- Non-breaking improvements

**These are safe to fix** but require careful review to ensure no unintended side effects.

## Global Changes (Requires Review)

**All global changes have been extracted to `code-global-v13.md`**

These affect core interpreter/runtime/interactive code and must be reviewed before implementation:
- Security validation issues (high priority)
- Comment-code mismatches revealing potential bugs
- Error handling inconsistencies
- Implementation status clarifications

## Next Steps

### Immediate (Safe to do now)
1. Fix remaining UI-specific docstrings and comments
2. Fix documentation inconsistencies
3. Update implementation status comments

### Requires Review (Don't do without approval)
1. Review all issues in `code-global-v13.md`
2. For each global issue, determine:
   - Is it a comment fix? (safe)
   - Is it a code bug? (needs testing)
   - Is it a security issue? (high priority)
   - Is it an architectural issue? (needs design review)

### Recommended Workflow

For safe fixes:
```bash
# 1. Read the issue from code-v13.md
# 2. Verify it's truly safe (UI-only or docs-only)
# 3. Make the fix
# 4. Test if it's code (not just comments)
# 5. Mark as done in this tracking doc
```

For global changes:
```bash
# 1. Review issue in code-global-v13.md
# 2. Understand the impact
# 3. Create test cases if needed
# 4. Implement with careful testing
# 5. Verify across all UIs
```

## Files Modified

- `src/ui/tk_widgets.py` - Docstring fix
- `src/ui/curses_ui.py` - Comment clarification
- `docs/help/common/language/functions/cvi-cvs-cvd.md` - Error code format fix

## Notes

- The categorization script identified issues but some categorization may need refinement
- "Safe" doesn't mean "trivial" - always review before applying
- Documentation fixes often reveal implementation questions that need answers
- When in doubt, document the question rather than guessing the answer
