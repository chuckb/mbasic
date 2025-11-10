# CLI Debugging Commands

The CLI backend provides powerful debugging commands for interactive debugging of BASIC programs.

## Overview

The CLI debugger allows you to:
- Set and manage breakpoints
- Single-step through program execution
- View the execution stack
- Control program flow during debugging
- Inspect variables using PRINT statement

## Debugging Commands

### BREAK - Breakpoint Management

Set, clear, and list breakpoints in your program.

**Syntax:**
```
BREAK [line_number]     - Set breakpoint at line
BREAK                   - List all breakpoints
BREAK CLEAR            - Clear all breakpoints
BREAK CLEAR line_number - Clear specific breakpoint
```

**Examples:**
```
Ready
BREAK 100              # Set breakpoint at line 100
Breakpoint set at line 100
Ready
BREAK 200              # Set another breakpoint
Breakpoint set at line 200
Ready
BREAK                  # List all breakpoints
Breakpoints: 100, 200
Ready
BREAK CLEAR 100        # Clear breakpoint at line 100
Breakpoint cleared at line 100
Ready
BREAK CLEAR            # Clear all breakpoints
All breakpoints cleared
Ready
```

**Notes:**
- Breakpoints pause execution before the specified line executes
- When a breakpoint is hit, you enter debug mode
- Use CONT to continue execution from a breakpoint
- Breakpoints persist until cleared or the program is modified

### STEP - Single-Step Execution

Execute the program one statement at a time.

**Syntax:**
```
STEP [n]               - Execute n statements (default: 1)
```

**Planned (not yet implemented):**
```
STEP INTO             - Step into subroutines (planned)
STEP OVER             - Step over subroutine calls (planned)
```

**Examples:**
```
Ready
10 PRINT "Starting"
20 A = 10
30 B = 20
40 PRINT A + B
RUN
Starting
[Break at line 20]
Ready
STEP                   # Execute line 20
[Break at line 30]
Ready
STEP 2                 # Execute lines 30 and 40
30
[Program ended]
Ready
```

**Notes:**
- STEP without arguments executes one statement
- Useful for understanding program flow
- Shows current line before execution
- Can be combined with breakpoints

### STACK - Call Stack Inspection

View the current execution stack including GOSUB calls and FOR loops.

**Syntax:**
```
STACK                  - Show full call stack
STACK GOSUB           - Show only GOSUB stack
STACK FOR             - Show only FOR loop stack
```

**Examples:**
```
Ready
10 FOR I = 1 TO 3
20   GOSUB 100
30 NEXT I
40 END
100 PRINT "In subroutine"
110 STACK
120 RETURN
RUN
In subroutine
Call Stack:
  GOSUB from line 20 to line 100
  FOR I from line 10 (I = 1, limit = 3, step = 1)
Ready
```

**Notes:**
- Shows nested subroutine calls
- Displays FOR loop variables and limits
- Helpful for debugging complex program flow
- Updates in real-time during execution

## Debug Mode

When a breakpoint is hit or during STEP execution, you enter debug mode.

**In debug mode you can:**
- Examine variables with PRINT
- Modify variables with assignment statements
- Set/clear additional breakpoints
- View the stack with STACK
- Continue execution with CONT
- Step to next statement with STEP
- Stop debugging with STOP

## Debugging Workflow

### Basic Debugging Session

```
Ready
LOAD "program.bas"     # Load your program
LIST                   # Review the code
BREAK 50               # Set breakpoint at suspicious line
RUN                    # Run program
[Break at line 50]
PRINT A, B, C          # Check variables
STEP                   # Execute one statement
PRINT A                # Check specific variable
CONT                   # Continue execution
```

### Finding Logic Errors

```
Ready
10 FOR I = 1 TO 10
20   A = A + I
30   B = B + A
40 NEXT I
50 PRINT "A ="; A; "B ="; B
Ready
BREAK 30               # Break inside loop
RUN
[Break at line 30]
PRINT I, A, B          # Check loop variables
STEP                   # Step through iterations
PRINT I, A, B          # See values change
CONT                   # Continue to next iteration
```

### Debugging Subroutines

```
Ready
100 GOSUB 200
110 PRINT "Done"
120 END
200 REM Subroutine
210 X = 10
220 Y = 20
230 RETURN
Ready
BREAK 200              # Break at subroutine entry
RUN
[Break at line 200]
STACK                  # See where we came from
STEP 3                 # Execute subroutine
PRINT X, Y             # Check subroutine variables
CONT                   # Return to main program
```

## Tips and Best Practices

1. **Start with LIST**: Review your program before debugging
2. **Use meaningful breakpoints**: Set them before suspicious code
3. **Print key variables**: Use PRINT to monitor variables that control program flow
4. **Step through loops once**: Understand loop behavior before continuing
5. **Check the stack**: Useful when debugging nested subroutines
6. **Clear breakpoints when done**: Use BREAK CLEAR to remove all

## Limitations

- Breakpoints don't persist across program edits
- STEP INTO/OVER not yet implemented (use STEP)
- No conditional breakpoints (must check conditions manually)
- Variable inspection uses PRINT statement (no dedicated inspection command)

## See Also

- [CLI Commands Reference](index.md)
- [Running Programs](../common/running.md)
- [Error Messages](../common/errors.md)