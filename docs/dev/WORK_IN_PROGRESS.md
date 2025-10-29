# Work in Progress

## Current Session (2025-10-29)

### Status: Ready for Checkpoint ✅

All work completed and committed:
- v1.0.295: Documented lexer cleanup issues
- v1.0.296: Reduced tnylpo timeout to 1s
- v1.0.297: Added multiple SYSTEM commands for instant exit

### Completed Work

**1. Lexer Documentation** (v1.0.295)
- Created `docs/dev/LEXER_CLEANUP_TODO.md`
- Documents 4 issues from `/home/wohl/lexer_sux.txt`:
  - Case-keeping string not factored out
  - STATEMENT_KEYWORDS trying to parse old BASIC
  - Multiple identifier tables
  - Suffix stripping with # needs clarification

**2. tnylpo Testing Fix** (v1.0.296 → v1.0.297)
- Updated `tests/HOW_TO_RUN_REAL_MBASIC.md`
- Changed: `echo "RUN"` → `printf "RUN\nSYSTEM\nSYSTEM\nSYSTEM\n"`
- Reduced timeout: 10s → 1s
- Result: 30x faster (0.104s vs 3s for syntax errors)

### Background Tasks Running
Several test programs left running (can be killed on resume):
- Shell 230616: test_resume.bas (RESUME NEXT)
- Shells 78537e, d1a2fe, 2c7edd: test_for.bas
- Shells 51e88c, a7431e: test_ers.bas
- Shell e666cb: test_ers_simple.bas

### Next Steps
Ready to checkpoint or start new work. Lexer cleanup is documented but NOT requested for implementation yet.

---

## Recently Completed

### PC (Program Counter) Refactoring (v1.0.276-283)
✅ **COMPLETE** - Hardware-inspired PC/NPC design implemented

### Web UI Improvements (v1.0.265-274)
✅ **COMPLETE** - All sizing, scrolling, and notification issues resolved
