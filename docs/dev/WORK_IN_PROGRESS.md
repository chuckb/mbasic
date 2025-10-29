# Work in Progress

## No Active Work

Last session completed: 2025-10-29 - NPC architecture refactoring at v1.0.300

All work committed and pushed.

### Session Summary - 2025-10-29 - NPC Architecture Refactoring

**Problem Identified:**
- Previous DE_NONEIFY work (has_pending_jump) made architecturally wrong code look semantic
- tick() loop handled NPC from PREVIOUS iteration at TOP of loop (one iteration late)
- Fundamentally misunderstood NPC pattern

**Root Cause:**
- NPC is not a "pending jump flag" - it's ALWAYS the next PC
- Should be: statement sets NPC (or defaults to next), then at END: `pc = npc`
- Was: check NPC at START (from previous iteration), conditionally advance

**Solution (v1.0.300):**
- Moved NPC handling from top of loop (lines 277-280) to end of iteration (lines 352-356)
- Simple pattern: if NPC set, use it; else advance to next sequential statement
- Removed has_pending_jump() method (was obscuring the architectural problem)
- Fixed error handler flow to fall through to NPC handling instead of continue

**Files Modified:**
- src/interpreter.py: Refactored tick_pc() loop, fixed execute_if() None checks
- src/runtime.py: Removed has_pending_jump() method

**Impact:**
- All control flow now handles NPC at correct time (end of iteration, not beginning)
- FOR/WHILE loops work correctly
- GOTO/GOSUB/RETURN work correctly
- Error handling (ON ERROR GOTO, RESUME NEXT) works correctly
- All tests passing

---

### Session Summary - 2025-10-29 - Code Quality Cleanup

**Part 1: Vulture Cleanup (v1.0.299)**
- Fixed syntax error in nicegui_backend.py (`.futures` → `import concurrent.futures`)
- Cleaned 22 unused variables (renamed to `_` prefix per Python convention)
- Files: basic_builtins.py, interpreter.py, semantic_analyzer.py, curses_settings_widget.py, curses_ui.py

**Part 2: DE_NONEIFY Phase 4 (v1.0.299)**
- Replaced NPC None checks with `has_pending_jump()` semantic method
- interpreter.py:277: `npc is not None` → `has_pending_jump()`
- interpreter.py:357: `npc is None` → `not has_pending_jump()`
- Moved DE_NONEIFY_TODO.md → history/DE_NONEIFY_DONE.md (substantially complete)

**Impact**:
- All vulture issues resolved (33 total)
- ~12 None checks replaced with semantic methods
- Improved code readability and maintainability
- All tests passing

---

## Previous Sessions

See docs/history/ for past session summaries.
