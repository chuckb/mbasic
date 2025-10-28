# Work in Progress

## Current Status: Ready for Next Task

**Version**: 1.0.138 (as of 2025-10-28)

### Recently Completed (v1.0.104-138)

Major work completed on settings system, case handling, documentation system, and help build validation.

**Summary:**
- ✅ Settings infrastructure with CLI commands (SET, SHOW SETTINGS, HELP SET)
- ✅ Variable case conflict handling (5 policies: first_wins, error, prefer_upper, prefer_lower, prefer_mixed)
- ✅ Keyword case handling with table-based architecture (6 policies)
- ✅ Test organization planning (Phase 1 complete: 35 tests inventoried)
- ✅ Critical documentation improvements (real MBASIC testing, test inventory)
- ✅ TK UI help system restructured (582 lines → 95 line index with subsections)
- ✅ Checkpoint script auto-rebuilds help indexes when docs/help/ changes
- ✅ Help build validates macro expansion, fails on unexpanded {{kbd:...}} macros
- ✅ TK keybindings JSON file completed with all editor/view shortcuts

**See:**
- `docs/history/SESSION_2025_10_28_SETTINGS_AND_CASE_HANDLING.md` - Settings system work
- `docs/dev/GITHUB_DOCS_WORKFLOW_EXPLAINED.md` - GitHub Pages deployment explanation

---

## Active Work: Test Organization (Phase 2+)

**Started:** 2025-10-28
**Task:** Organize 35 test files into proper test structure

### Status

- ✅ Phase 1: Inventory complete (35 tests categorized)
- ⏳ Phase 2: Create structure (in progress)
- ⏸️ Phase 3: Move tests to appropriate locations
- ⏸️ Phase 4: Create test runner script
- ⏸️ Phase 5: Documentation

### Files Being Modified

- Creating: `tests/regression/` (subdirectories)
- Creating: `tests/manual/`
- Creating: `tests/debug/` with .gitignore
- Moving: Test files from root → tests/regression/
- Moving: Test files from utils/ → tests/regression/

### Next Steps

1. ✅ Create directory structure
2. Move regression tests from root directory
3. Move regression tests from utils/
4. Create test runner script
5. Document test organization

### Potential Next Tasks

1. **Test Organization (Phase 2+)**
   - Create tests/ directory structure
   - Move 25 regression tests to appropriate locations
   - Create test runner script
   - See: `docs/dev/TESTING_SYSTEM_ORGANIZATION_TODO.md`

2. **Keyword Case Error Policy**
   - Implement `error` policy checking at parse/edit time
   - Currently all policies except `error` are working

3. **PyPI Distribution**
   - Package and publish to PyPI
   - See: `docs/dev/SIMPLE_DISTRIBUTION_APPROACH.md`

4. **Additional UI Integration**
   - Add settings UI to curses/TK interfaces
   - Currently settings work via CLI commands only

5. **Pretty Printer Settings**
   - Add configurable spacing options

---

## Instructions

When starting new work:
1. Update this file with task description and status
2. List files being modified
3. Track progress with checkmarks
4. When complete, move to `docs/history/` and clear this file
