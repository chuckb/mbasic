---
category: system
description: To trace the execution of program statements
keywords: ['close', 'command', 'execute', 'for', 'line', 'next', 'number', 'print', 'program', 'statement']
syntax: TRON
title: TRON/TROFF
type: statement
---

# TRON/TROFF

## Syntax

```basic
TRON
TROFF
```

## Purpose

To trace the execution of program statements.

## Remarks

As an aid in debugging, the TRON statement (executed in either the direct or indirect mode) enables a trace flag that prints each line number of the program as it is executed. The numbers appear enclosed in square brackets. The trace flag is disabled with the TROFF statement (or when a NEW command is executed).

## Example

```basic
TRON
             Ok
             LIST
             10 K=lO
             20 FOR J=l TO 2
             30 L=K + 10
             40 PRINT J~K~L
             50 K=K+lO
             60 NEXT
             70 END
             Ok
             RUN
             [10] [20] [30] [40] 1   10   20
             [50] [60] [30] [40] 2   20   30
             [50] [60] [70]
             Ok
             TROFF
             Ok
```

## See Also
- [FRE](../functions/fre.md) - Arguments to FRE are dummy arguments
- [HELP SET](helpsetting.md) - Display help for a specific setting
- [INKEY$](../functions/inkey_dollar.md) - Returns either a one-character string cont~ining a character read from the terminal or a null string if no character is pending at the terminal
- [INP](../functions/inp.md) - Returns the byte read from port I
- [LIMITS](limits.md) - Display resource usage and interpreter limits
- [NULL](null.md) - To set the number of nulls to be printed at   the end of each line
- [PEEK](../functions/peek.md) - Returns the byte (decimal integer in the range 0 to 255) read from memory location I
- [RANDOMIZE](randomize.md) - To reseed the random number generator
- [REM](rem.md) - To allow explanatory remarks to be inserted in a program
- [SET (setting)](setsetting.md) - Configure interpreter settings at runtime
- [SHOW SETTINGS](showsettings.md) - Display current interpreter settings
- [USR](../functions/usr.md) - Calls the user's assembly language subroutine with the argument X
- [VARPTR](../functions/varptr.md) - Returns the memory address of a variable
- [WIDTH](width.md) - To set the printed line width in number        of characters for the terminal or line printer
