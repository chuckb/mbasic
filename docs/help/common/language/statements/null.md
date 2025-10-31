---
category: system
description: To set the number of nulls to be printed at   the end of each line
keywords: ['command', 'for', 'goto', 'if', 'input', 'line', 'null', 'number', 'print', 'put']
syntax: NULL <integer expression>
title: NULL
type: statement
---

# NULL

## Syntax

```basic
NULL <integer expression>
```

## Purpose

To set the number of nulls to be printed at   the end of each line.

## Remarks

For    10-character-per-second  tape    punches, <integer expression> should be >=3. When tapes are not being punched, <integer expression> should    be   0   or    1  for  Teletypes   and Teletype-compatible CRTs. <integer expression> should be 2 or 3 for 30 cps hard copy printers. The default value is O.

## Example

```basic
Ok
              NULL 2
              Ok
              100 INPUT X
              200 IF X<50 GOTO 800
              Two null characters will be printed after each
              line.
```

## See Also
- [FRE](../functions/fre.md) - Arguments to FRE are dummy arguments
- [HELP SET](helpsetting.md) - Display help for a specific setting
- [INKEY$](../functions/inkey_dollar.md) - Returns either a one-character string cont~ining a character read from the terminal or a null string if no character is pending at the terminal
- [INP](../functions/inp.md) - Returns the byte read from port I
- [LIMITS](limits.md) - Display resource usage and interpreter limits
- [PEEK](../functions/peek.md) - Returns the byte (decimal integer in the range 0 to 255) read from memory location I
- [RANDOMIZE](randomize.md) - To reseed the random number generator
- [REM](rem.md) - To allow explanatory remarks to be inserted in a program
- [SET (setting)](setsetting.md) - Configure interpreter settings at runtime
- [SHOW SETTINGS](showsettings.md) - Display current interpreter settings
- [TRON/TROFF](tron-troff.md) - To trace the execution of program statements
- [USR](../functions/usr.md) - Calls the user's assembly language subroutine with the argument X
- [VARPTR](../functions/varptr.md) - Returns the memory address of a variable
- [WIDTH](width.md) - To set the printed line width in number        of characters for the terminal or line printer
