# Work in Progress

## Status: Ready for Next Task

**Version**: 1.0.154+ (as of 2025-10-28)

### Recently Completed (v1.0.154+)

**Keyword Case Display Fix** - COMPLETE

Fixed critical bug where keyword case policies were not being applied to keyword display. Keywords now correctly show consistent case throughout the program based on the configured policy.

#### The Bug

Lexer was ignoring the return value from `KeywordCaseManager.register_keyword()`:

**Before (WRONG):**
```python
token.original_case_keyword = ident  # Always used typed case
self.keyword_case_manager.register_keyword(...)  # Return value ignored!
```

**After (CORRECT):**
```python
display_case = self.keyword_case_manager.register_keyword(...)
token.original_case_keyword = display_case  # Use policy-determined case
```

#### Impact

**Before fix:**
- Keywords always displayed as originally typed, regardless of policy
- `first_wins` policy had no effect on display
- Program with mixed case showed mixed case (inconsistent)

**After fix:**
- Keywords display according to policy
- `first_wins`: All keywords use first occurrence's case
- `force_upper/lower/capitalize`: All keywords converted
- Program shows consistent keyword case

#### Example

Program with mixed case:
```basic
10 Print "First"
20 PRINT "Second"
30 print "Third"
```

**Policy: `first_wins`**
- Before: Displayed as `Print`, `PRINT`, `print` (inconsistent)
- After: All display as `Print` (consistent - first wins)

**Policy: `force_upper`**
- Before: Displayed as `Print`, `PRINT`, `print` (ignored policy)
- After: All display as `PRINT` (policy enforced)

#### Files Modified

**Implementation:**
- `src/lexer.py` - Fixed 3 locations where `register_keyword()` is called (lines 245, 272, 303)

**Testing:**
- `tests/regression/lexer/test_keyword_case_display_consistency.py` - 8 tests (✓ ALL PASSING)
- `tests/regression/lexer/test_keyword_case_scope_isolation.py` - 7 tests (✓ ALL PASSING)
- `tests/manual/test_keyword_case_program.bas` - Example program for manual testing

#### Test Results

```bash
$ python3 tests/regression/lexer/test_keyword_case_display_consistency.py
Ran 8 tests in 0.001s
OK

$ python3 tests/run_regression.py --category lexer
✅ ALL REGRESSION TESTS PASSED
```

#### Scope Behavior (Correct)

✅ **Whole program shares one KeywordCaseManager:**
```basic
10 Print "First"
20 PRINT "Second"  → Shows as "Print" (first_wins)
30 print "Third"   → Shows as "Print" (first_wins)
```

✅ **Immediate mode uses separate manager:**
```
Program: 10 RUN
Immediate: run  → No conflict (separate scope)
```

This is correct because:
- Keywords are syntax (should be consistent within program)
- Variables are runtime state (shared between modes)

---

## Previous Work

### Keyword Case Settings Integration
**Completed:** 2025-10-28 (v1.0.153)
- Integrated `keywords.case_style` setting with lexer
- Error policy now surfaces in all UIs
- See: `docs/history/SESSION_2025_10_28_KEYWORD_CASE_INTEGRATION.md`

### Help System Search Improvements
**Completed:** 2025-10-28 (v1.0.151)
- Search ranking, fuzzy matching, in-page search
- See: `docs/history/SESSION_2025_10_28_HELP_SEARCH_IMPROVEMENTS.md`

---

## Potential Next Tasks

1. **Settings UI Integration**
   - Add settings UI to curses/TK interfaces
   - Currently settings work via CLI commands only

**Deferred to future:**
- Pretty Printer Spacing Options
- PyPI Distribution (see `docs/future/PYPI_DISTRIBUTION.md`)
