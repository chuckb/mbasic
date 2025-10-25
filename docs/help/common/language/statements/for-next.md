# FOR-NEXT Loop

Repeat a block of code a specific number of times.

## Syntax

```basic
FOR variable = start TO end [STEP increment]
  statements...
NEXT [variable]
```

## Description

The FOR-NEXT loop executes a block of code repeatedly, incrementing a counter variable each time through the loop.

- **variable** - Loop counter (any numeric variable)
- **start** - Initial value
- **end** - Final value (inclusive)
- **increment** - Amount to add each iteration (default: 1)

## Examples

### Count from 1 to 10
```basic
10 FOR I = 1 TO 10
20   PRINT I
30 NEXT I
```

### Count by 2s
```basic
10 FOR I = 0 TO 20 STEP 2
20   PRINT I
30 NEXT I
```
Output: 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20

### Count Backwards
```basic
10 FOR I = 10 TO 1 STEP -1
20   PRINT I
30 NEXT I
40 PRINT "Blastoff!"
```

### Nested Loops
```basic
10 FOR I = 1 TO 3
20   FOR J = 1 TO 3
30     PRINT I; "x"; J; "="; I*J
40   NEXT J
50 NEXT I
```

## Notes

- Loop executes when start ≤ end (for positive STEP)
- Loop executes when start ≥ end (for negative STEP)
- Variable name after NEXT is optional but recommended
- Loops can be nested
- Don't modify the loop variable inside the loop

## See Also

- [WHILE-WEND](while-wend.md) - Condition-based loops
- [GOTO-GOSUB](goto-gosub.md) - Unconditional jumps
