# PC Cleanup - Remaining Work

**Status:** In Progress (v1.0.291)

## Completed (v1.0.291)

✅ **ErrorInfo now uses PC**
- Changed `error_line: int` to `pc: PC`
- Updated all ErrorInfo creation sites (3 places)
- Updated UI code to use `error_info.pc.line_num`

✅ **Removed dual-mode from execute_* methods**
- GOTO, GOSUB, IF, RETURN now only set `runtime.npc`
- FOR/NEXT now only set `runtime.npc`
- WHILE/WEND now only set `runtime.npc`
- ON GOTO/ON GOSUB now only set `runtime.npc`
- Removed 9+ lines of redundant `runtime.next_line` assignments

## Remaining Work

### 1. Old Execution Methods (Not Using PC)

These methods still use `runtime.current_line`, `runtime.next_line`, etc.:

**src/interpreter.py:**
- `run_from_current()` - line ~527 (used by CONT command)
- `_run_loop()` - line ~636
- `step_once()` - line ~553
- `execute_line()` - line ~570
- `advance_to_next_statement()` - line ~897

**Status:** Used by `interactive.py` for CONT command

**Options:**
1. Convert to PC-based (rewrite to use runtime.pc)
2. Remove and update CONT to use tick-based execution

### 2. RESUME Statement

**src/interpreter.py** `execute_resume()` - line ~1505

Still uses old fields:
```python
self.runtime.next_line = self.runtime.error_line
self.runtime.next_stmt_index = self.runtime.error_stmt_index + 1
```

**Should use:**
```python
# Get error PC from ErrorInfo
error_pc = self.state.error_info.pc
# Calculate next statement
next_pc = self.runtime.statement_table.next_pc(error_pc)
self.runtime.npc = next_pc
```

### 3. RUN Statement

**src/interpreter.py** `execute_run()` - line ~2038

Sets old fields:
```python
self.runtime.next_line = stmt.line_number
```

**Should use:**
```python
self.runtime.npc = PC.from_line(stmt.line_number)
```

### 4. Error Handler Invocation

**src/interpreter.py** `_invoke_error_handler()` - line ~830

Sets old fields:
```python
self.runtime.next_line = self.runtime.error_handler
self.runtime.next_stmt_index = 0
```

**Should use:**
```python
self.runtime.npc = PC.from_line(self.runtime.error_handler)
```

### 5. Runtime Fields Still Exist

**src/runtime.py** still has old fields:
- `current_line: Optional[LineNode]`
- `current_stmt_index: int`
- `next_line: Optional[int]`
- `next_stmt_index: Optional[int]`
- `stop_line` / `stop_stmt_index` (for STOP command)
- `error_line` / `error_stmt_index` (for error handling)

**Should replace with:**
- `stop_pc: PC` (for STOP command)
- Remove current_line, current_stmt_index (use runtime.pc)
- Remove next_line, next_stmt_index (use runtime.npc)
- Remove error_line, error_stmt_index (get from ErrorInfo.pc or store error_pc)

### 6. ERS# System Variable (Not Yet Added)

Need to add:
- Runtime field for error statement offset
- Variable accessor for ERS#
- Set when error occurs

**Implementation:**
```python
# In Runtime:
self.error_pc: Optional[PC] = None  # Set when error occurs

# When accessing ERS# variable:
if var_name == "ERS":
    return self.error_pc.stmt_offset if self.error_pc else 0

# When accessing ERL# variable (update):
if var_name == "ERL":
    return self.error_pc.line_num if self.error_pc else 0
```

## Testing Needed

After completing remaining work:

1. **CONT command** - test STOP/CONT works
2. **RESUME** - test ON ERROR with RESUME
3. **RESUME NEXT** - test statement-level resume
4. **RUN** - test RUN with line number
5. **ERS#** - test error statement reporting
6. **FOR loops** - verify still working
7. **WHILE loops** - verify still working
8. **Error handlers** - test ON ERROR GOTO

## Estimated Remaining Effort

- RESUME updates: 1 hour
- RUN/error handler: 30 min
- Runtime field cleanup: 1 hour
- ERS# variable: 1 hour
- Old execution methods (if keeping): 2 hours
- Testing: 2 hours

**Total:** ~8 hours

## Current Status

About 70% complete. Core execute_* methods are PC-only. Remaining work is mostly in error handling and old execution methods.
