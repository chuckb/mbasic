# Work in Progress

## Task: Synchronize Curses UI, Help Files, and Documentation with Current TK/Interpreter

**Started:** 2025-10-28
**Status:** In Progress

### Completed So Far

✅ **Phase 1: Audit** (v1.0.157)
- TK UI Feature Audit: 950 lines documenting 60+ features
- Curses vs TK Gap Analysis: 953 lines identifying gaps
- Critical issues identified: Edit-and-Continue, line number display, statement highlighting

✅ **De-Microsoft Project** (v1.0.158)
- Created MBASIC_HISTORY.md with proper disclaimers
- Updated README.md with clear attribution and disclaimers
- Fixed PyPI metadata (setup.py, pyproject.toml)
- Batch-updated 50+ source/doc files
- Preserved external historical docs
- Down to 70 references (mostly appropriate historical context)

### Problem

Over hundreds/thousands of changes focused on TK client and interpreter rewrites:
- Curses UI is outdated and doesn't match TK functionality
- Help files are outdated (written before recent changes)
- Documentation doesn't reflect current state
- Curses editor has line numbers in separate column (wrong - causes indent spacing issues)

### Source of Truth

**TK UI and Interpreter = Current Implementation**
- Use TK as reference for what features should exist
- Use TK editor design (line numbers embedded in text, not separate column)
- Use interpreter as reference for actual behavior

### Tasks

#### Phase 1: Audit Current State
1. ✅ Document all TK UI features (docs/dev/TK_UI_FEATURE_AUDIT.md - 950 lines)
2. ✅ Document all interpreter features (included in TK audit)
3. ✅ List curses UI features and identify gaps (docs/dev/CURSES_VS_TK_GAP_ANALYSIS.md - 953 lines)
4. ⏸️ Review help files for outdated content
5. ⏸️ Review docs for outdated content

**Findings:**
- 60+ features documented in TK UI
- Critical gap: Edit-and-Continue error recovery missing in curses
- Major issue: Line numbers in separate column (causes indent spacing problems)
- High priority: Statement highlighting, Recent Files menu
- Overall: 85% core parity, 40% advanced feature parity

#### Phase 2a: Web UI Rewrite (NiceGUI)
1. ⏸️ Rename current web UI to `oldweb` (quick prototype, outdated)
2. ⏸️ Create new web UI with NiceGUI from scratch
3. ⏸️ Use TK UI as reference for features
4. ⏸️ Test new web UI

**Rationale:** Current web UI was a quick prototype. Rather than update it to match hundreds of TK changes, faster to rebuild with NiceGUI (impressed with its speed). Can salvage useful code from oldweb.

#### Phase 2b: Update Curses UI
1. ⏸️ Fix editor line number display (embed in text like TK)
2. ⏸️ Add missing TK features to curses
3. ⏸️ Test curses UI matches TK behavior

#### Phase 3: Update Help Files
1. ⏸️ Update help files to reflect current features
2. ⏸️ Test help content is accurate

#### Phase 4: Update Documentation
1. ⏸️ Update docs to reflect current state
2. ⏸️ Remove outdated information

### Key Issues to Address

**Curses Editor Line Numbers:**
- Currently: Separate column for line numbers
- Problem: Causes indent spacing to be wrong vs real MBASIC/TK
- Solution: Embed line numbers in text like TK does

**Feature Parity:**
- TK has many features curses doesn't
- Need to identify and implement missing features

**Documentation Accuracy:**
- Help files describe features that may have changed
- Docs may reference old behavior
