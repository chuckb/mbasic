# Debugger Issues TODO

## Fixed Issues

### 1. STEP command jumps to wrong line after breakpoint ✅
**Status**: FIXED in src/interpreter.py:317-321
**Fix**: Auto-resume PC when in step mode if stopped at BREAK/USER
- When stepping after a breakpoint, PC is now automatically resumed
- Works in both web UI and curses UI

### 2. INPUT statements not highlighted/indicated ✅
**Status**: FIXED in src/ui/web/nicegui_backend.py
**Fix**: Added highlighting and status display at three locations (lines 2090, 2135, 2365)
- INPUT statements now highlighted in CodeMirror editor
- Status shows: "at line 2065: COMMAND?" (line number + prompt)
- Current line label shows: ">>> INPUT at line 2065"

### 3. Breakpoints detected but program ends instead of pausing ✅
**Status**: FIXED in src/pc.py:102-117 (v873)
**Root Cause**: PC is frozen dataclass with default __eq__ that compared all fields
- When breakpoint hits, `pc.stop("BREAK")` creates new PC with stop_reason="BREAK"
- `statement_table.get(stopped_pc)` failed because default equality includes stop_reason
- `__hash__` included stop_reason, violating hash/equality contract when comparing by position only
**Fix**: Added custom `__eq__` and `__hash__` methods to PC class
- Both now only compare/hash position (line, statement), not state (stop_reason, error)
- This allows PC lookups in statement_table and breakpoints to work correctly regardless of PC state
- Line-level breakpoint detection also fixed in interpreter.py:352-355 (v871)
- Changed from `pc.line_num in self.runtime.breakpoints` to loop checking `bp.line == pc.line_num`

## Outstanding Issues

### 3. Curses UI: ^U menu scrolls program to top
**Status**: TODO
**Repro**:
- In curses UI, press ^U to open menu
- **Bug**: Program code scrolls to top
- **Expected**: Should maintain current scroll position

### 4. Curses UI: STEP shows "Paused at None" after breakpoint
**Status**: TODO
**Repro**:
- Set breakpoint at line 2060 in curses UI
- Hit breakpoint
- Press ^T to step
- **Bug**: Shows "Paused at None"
- **Expected**: Should show current line number

## Investigation Notes

- Line 30 in Super Star Trek is just a REM statement
- Line 2060 has: `INPUT"COMMAND";A$`
- Line 2065 has: `ZZ$=A$:gosub 9450:a$=zz$`
- Breakpoint/step issue suggests PC is being reset incorrectly when stepping

## Files to Check

- `src/interpreter.py` - Step command implementation
- `src/ui/web/nicegui_backend.py` - Web UI debugger
- `src/ui/curses_ui.py` - Curses UI debugger
- `src/pc.py` - Program Counter logic
