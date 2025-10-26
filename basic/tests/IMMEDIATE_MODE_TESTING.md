# Immediate Mode Testing Guide

This directory contains test programs for the immediate mode feature in visual UIs (Web, Tk, Curses).

## Test Programs

### 1. `immediate_mode_breakpoint.bas`
**Tests**: Breakpoint inspection and variable modification

**How to test**:
1. Load the program
2. Set a breakpoint at line 130 (click on line number or use Ctrl+B)
3. Run the program (Ctrl+R)
4. When breakpoint hits at line 130, use immediate mode:
   ```
   PRINT X
   PRINT Y
   X = 100
   PRINT X
   ```
5. Continue execution (Ctrl+G)
6. Verify that X=100 is used in subsequent iterations

**Expected behavior**:
- Immediate mode shows green "Ok" status when at breakpoint
- Can inspect variables (PRINT X shows current value)
- Can modify variables (X = 100 changes value)
- Modified values persist when execution continues

### 2. `immediate_mode_stop.bas`
**Tests**: Stop and inspect during execution

**How to test**:
1. Load the program
2. Run the program (Ctrl+R)
3. While it's running, press Stop (Ctrl+X or Ctrl+Q)
4. Use immediate mode:
   ```
   PRINT I
   PRINT TOTAL
   TOTAL = 999
   ```
5. Continue execution (Ctrl+G)
6. Verify modified TOTAL value is used

**Expected behavior**:
- Immediate mode disabled (red "[running]") while program runs
- Immediate mode enabled (green "Ok") after stop
- Can inspect loop variables
- Can modify variables that affect subsequent execution

### 3. `immediate_mode_arrays.bas`
**Tests**: Array inspection and modification

**How to test**:
1. Load the program
2. Set breakpoint at line 130
3. Run the program
4. At breakpoint, use immediate mode:
   ```
   PRINT A(1)
   PRINT A(2)
   A(3) = 999
   PRINT A(3)
   ```
5. Continue execution
6. Verify A(3) = 999 is used in sum calculation

**Expected behavior**:
- Can inspect array elements
- Can modify array elements
- Modified array values persist

### 4. `immediate_mode_strings.bas`
**Tests**: String variable inspection and modification

**How to test**:
1. Load the program
2. Set breakpoint at line 100
3. Run the program
4. At breakpoint, use immediate mode:
   ```
   PRINT NAME$
   PRINT CITY$
   NAME$ = "Modified Name"
   PRINT NAME$
   ```
5. Continue execution
6. Verify modified NAME$ is displayed

**Expected behavior**:
- Can inspect string variables
- Can modify string variables
- Modified strings persist

### 5. `immediate_mode_expressions.bas`
**Tests**: Expression evaluation in immediate mode

**How to test**:
1. Load the program
2. Set breakpoint at line 100
3. Run the program
4. At breakpoint, use immediate mode:
   ```
   PRINT X + Y
   PRINT X * Y
   PRINT SQR(X)
   PRINT X > Y
   Z = X + Y + 5
   PRINT Z
   ```

**Expected behavior**:
- Can evaluate arithmetic expressions
- Can evaluate function calls (SQR, etc.)
- Can evaluate comparisons
- Can create new variables in immediate mode

### 6. `immediate_mode_step.bas`
**Tests**: Immediate mode with single-step debugging

**How to test**:
1. Load the program
2. Use Step (Ctrl+T) to execute one line at a time
3. After each step, inspect variables:
   ```
   PRINT A
   PRINT B
   PRINT C
   ```
4. Watch variables change as you step through

**Expected behavior**:
- Immediate mode enabled after each step
- Can inspect variables after each statement
- Variables show correct values as program progresses

## Safety Tests

### Test 1: Cannot Execute While Running
1. Load any test program
2. Run it (Ctrl+R)
3. Try to type in immediate mode input field
4. **Expected**: Input field is disabled (grayed out)
5. **Expected**: Status shows red "[running]"
6. **Expected**: Cannot execute commands while running

### Test 2: Re-enable After Stop
1. Run a program
2. Stop it (Ctrl+X)
3. **Expected**: Immediate mode re-enabled (green "Ok")
4. **Expected**: Can execute commands

### Test 3: Re-enable After Error
1. Create a program with an error (e.g., divide by zero)
2. Run it
3. When error occurs
4. **Expected**: Immediate mode re-enabled
5. **Expected**: Can inspect variables at error point

## UI-Specific Testing

### Web UI
- Test in browser (http://localhost:8080)
- Verify immediate panel appears below output
- Verify status indicator color changes (green/red)
- Verify input field enable/disable
- Verify history scrolls correctly
- Test with multiple browser tabs (session isolation)

### Tk UI
- Test immediate panel in third pane (bottom 30%)
- Verify ScrolledText history works
- Verify Entry widget Enter key handling
- Verify status label color changes

### Curses UI
- Test immediate panel in urwid layout
- Verify ListBox scrolling works
- Verify Enter key in ImmediateInput widget
- Verify color palette (green/red status)
- Verify urwid focus handling

## Common Issues to Check

1. **State Corruption**: Verify program execution continues correctly after immediate mode modifications
2. **Memory Leaks**: Run long programs with frequent immediate mode usage
3. **Focus Issues**: Verify keyboard focus switches correctly between editor/output/immediate
4. **History Overflow**: Test with many immediate commands (should handle gracefully)
5. **Error Handling**: Try invalid commands in immediate mode (should show error, not crash)

## Test Checklist

- [ ] Load each test program successfully
- [ ] Set breakpoints (Ctrl+B)
- [ ] Run programs (Ctrl+R)
- [ ] Immediate mode disabled while running (red status)
- [ ] Immediate mode enabled at breakpoint (green status)
- [ ] PRINT statements work in immediate mode
- [ ] Variable assignments work in immediate mode
- [ ] Array access works in immediate mode
- [ ] String operations work in immediate mode
- [ ] Expression evaluation works
- [ ] Function calls work (SQR, etc.)
- [ ] Modified values persist after continue
- [ ] Stop (Ctrl+X) enables immediate mode
- [ ] Step (Ctrl+T) enables immediate mode after each step
- [ ] Error messages appear in immediate history
- [ ] History scrolls correctly
- [ ] Input clears after command execution
- [ ] Works in Web UI
- [ ] Works in Tk UI
- [ ] Works in Curses UI

## Example Session

```
# Load immediate_mode_breakpoint.bas
# Set breakpoint at line 130 (click line number)
# Run program (Ctrl+R)

# At breakpoint, immediate mode shows "Ok" (green)
# Type in immediate mode input:
> PRINT X
 10

Ok
> PRINT Y
 20

Ok
> X = 100
Ok
> PRINT X
 100

Ok
# Press Continue (Ctrl+G)
# Program continues with X=100
```

## Reporting Issues

When reporting issues, include:
1. Which UI (Web/Tk/Curses)
2. Test program being run
3. Exact steps to reproduce
4. Expected vs actual behavior
5. Error messages (if any)
6. Screenshots (if UI visual issue)
