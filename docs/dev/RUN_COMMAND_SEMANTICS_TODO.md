# TODO: Fix RUN Command Semantics and Remove Bogus UI Checks

## Problem

RUN is currently treated as "special" in the UIs with incorrect checks:

1. **Web UI** checks `if self.running: return` - prevents RUN from working at breakpoints
2. **Web UI** checks if program is empty and shows error - real MBASIC allows RUN on empty program
3. **UIs treat RUN as special** - it's not! RUN is just CLEAR + GOTO

## Real MBASIC Behavior

In real MBASIC 5.21:
- **RUN always works** - no "can't RUN while running" error
- **RUN on empty program is fine** - just clears variables
- **RUN at a breakpoint** restarts the program from the top
- **RUN is just:** `RUN = CLEAR + GOTO (first line or specified line)`

Example from real MBASIC on CP/M emulator:
```
Ok
100 files
run
[lists files - works fine]

Ok
run
[works again - no error]

Ok
[empty program]
run
[no error - just clears and has nothing to execute]
```

## Current Wrong Behavior

**src/ui/web/nicegui_backend.py:1684-1686:**
```python
if self.running:
    self._set_status('Program already running')
    return
```
**WRONG:** This prevents RUN from working when at a breakpoint or during execution.

**src/ui/web/nicegui_backend.py:1694-1696:**
```python
if not self.program.lines:
    self._set_status('No program loaded')
    self._notify('No program in editor. Add some lines first.', type='warning')
    return
```
**WRONG:** RUN on empty program should be allowed (just clears variables).

## The Confusion: self.running Flag

The `self.running` boolean flag in UIs is **misleading** and causes incorrect logic:

- UIs think: "Can't RUN because already running"
- Reality: RUN is always valid - it just does CLEAR + GOTO

**The running flag should only be used for UI display (spinner, status message), NOT for controlling program logic.**

## Correct Semantics

**RUN (no arguments):**
1. Call `runtime.reset_for_run()` - clears variables, rebuilds statement table, preserves breakpoints
2. If program has lines: Start execution from first line
3. If program is empty: Just return (variables are cleared, nothing to execute)

**RUN line_number:**
1. Call `runtime.reset_for_run()`
2. GOTO specified line number
3. Start execution from there

**RUN "filename":**
1. LOAD "filename"
2. RUN (as above)

## What Needs Fixing

### 1. Web UI (_menu_run)
- **Remove** `if self.running: return` check (lines 1684-1686)
- **Remove** empty program error check (lines 1694-1696)
- **Keep** `self.running = True` for display purposes (spinner), but don't let it control logic

### 2. TK UI (cmd_run)
Check if TK UI has similar bogus checks - fix if needed.

### 3. Curses UI (cmd_run)
Check if Curses UI has similar bogus checks - fix if needed.

### 4. Interpreter (execute_run)
Verify interpreter correctly implements RUN = CLEAR + GOTO:
- `runtime.reset_for_run()` for CLEAR
- Set PC to first line (or specified line)
- Start execution

## Usage of self.running

**Correct usage (DISPLAY ONLY):**
```python
self.running = True  # Show spinner/busy indicator
try:
    # Execute program tick by tick
    ...
finally:
    self.running = False  # Hide spinner
```

**Incorrect usage (CONTROL LOGIC):**
```python
if self.running:  # WRONG - don't prevent commands based on this
    return
```

**Only CONT (continue) should check state:**
```python
if state.status not in ('paused', 'at_breakpoint'):
    raise RuntimeError("Can't continue - no program stopped")
```

## Related Issues

- Interpreter has `state.status` which is the real execution state
- UIs duplicate this with `self.running` boolean
- This violates "no copy" rule and causes sync issues
- Consider: UIs should just check `interpreter.state.status` instead of maintaining separate `running` flag

## Files to Fix

- `src/ui/web/nicegui_backend.py` - _menu_run (lines 1682-1740)
- `src/ui/tk_ui.py` - cmd_run (check for similar issues)
- `src/ui/curses_ui.py` - cmd_run (check for similar issues)
- `src/interpreter.py` - execute_run (verify correct semantics)

## Priority

High - this breaks fundamental BASIC semantics (RUN always works)

## Date Created

2025-11-01
