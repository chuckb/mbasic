# CLI Variable Inspection

Learn how to inspect and monitor variables while debugging BASIC programs in the CLI.

## Variable Inspection with PRINT

The CLI uses the PRINT statement for variable inspection during debugging:

```basic
PRINT A            ' Show single variable
PRINT A, B, C$     ' Show multiple variables
PRINT A; " = "; A  ' Show with label
```

**Example session:**
```
Ready
10 A = 5
20 B = 10
30 C$ = "Hello"
RUN
Ready
PRINT A
 5
Ready
PRINT A, B, C$
 5            10           Hello
Ready
```

## Checking Variables During Debugging

When you hit a breakpoint or use STEP, you can inspect variables with PRINT:

```
Ready
10 FOR I = 1 TO 5
20   A = A + I
30 NEXT I
40 PRINT "Sum:"; A
BREAK 30           ' Set breakpoint
RUN
[Break at line 30]
PRINT I, A         ' Check loop variables
 1            1
STEP
[Break at line 30]
PRINT I, A         ' Check after iteration
 2            3
```

## Variable Types

MBASIC has four variable types:

### Integer Variables
```basic
A% = 100
PRINT A%
 100
```

### Single-Precision (Float)
```basic
A! = 3.14159
PRINT A!
 3.14159
```

### Double-Precision
```basic
A# = 3.141592653589793
PRINT A#
 3.141592653589793
```

### String Variables
```basic
A$ = "Hello, World!"
PRINT A$
Hello, World!
```

## Arrays

Arrays require DIM and can be inspected element by element:

```basic
10 DIM ARR(5)
20 FOR I = 1 TO 5
30   ARR(I) = I * 10
40 NEXT I
RUN
Ready
PRINT ARR(1), ARR(2), ARR(3)
 10           20           30
```

## Variables Window (GUI UIs Only)

The CLI does not have a Variables Window feature. For visual variable inspection, use:
- **Curses UI** - Full-screen terminal with Variables Window ({{kbd:toggle_variables:curses}})
- **Tk UI** - Desktop GUI with Variables Window
- **Web UI** - Browser-based with Variables Window

## Tips for Variable Inspection

1. **Use meaningful names** - Makes debugging clearer
2. **PRINT with labels** - `PRINT "A="; A` shows what you're checking
3. **Check at breakpoints** - Use BREAK then PRINT to inspect state
4. **Use STEP and PRINT** - Step through code and print variables
5. **Format output** - Use semicolons and commas for readability

## Example: Debugging with PRINT

```basic
Ready
10 FOR I = 1 TO 10
20   F = F + 1
30   N = N + F
40 NEXT I
50 PRINT "Result:"; N
Ready
BREAK 30
RUN
[Break at line 30]
PRINT I, F, N
 1            1            0
STEP
[Break at line 30]
PRINT I, F, N
 2            2            1
```

## Common Patterns

### Check Multiple Variables
```basic
PRINT "I="; I, "Sum="; S, "Avg="; A
```

### Check Array Elements
```basic
PRINT A(1), A(2), A(3)
```

### Check String Variables
```basic
PRINT "Name: "; N$; " Age: "; A%
```

## Best Practices

1. **PRINT after RUN** - Variables persist after program ends
2. **Use PRINT for quick checks** - Faster than running the whole program
3. **Label your output** - Makes it clear what you're inspecting
4. **Use debugging commands** - Combine with BREAK, STEP, STACK

## See Also

- [Debugging Commands](debugging.md) - BREAK, STEP, STACK commands
- [CLI Index](index.md) - Full CLI command reference
