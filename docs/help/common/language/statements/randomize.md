---
category: system
description: To reseed the random number generator
keywords: ['command', 'for', 'function', 'if', 'next', 'number', 'print', 'program', 'randomize', 'return']
syntax: RANDOMIZE [<expression>]
title: RANDOMIZE
type: statement
---

# RANDOMIZE

## Syntax

```basic
RANDOMIZE [<expression>]
```

## Purpose

To reseed the random number generator.

## Remarks

If <expression> is    omitted, BASIC-80 suspends program execution     and asks for a value by printing Random Number Seed (-32768 to 32767)? before executing RANDOMIZE. If the random number generator is not reseeded, the RND function returns the same sequence of random numbers each time the program is RUN. To change the sequence of random numbers every time the program is RUN, place a RANDOMIZE statement at the beginning of the program and change the argument with each RUN.

## Example

```basic
10 RANDOMIZE
             20 FOR 1=1 TO 5
             30 PRINT RND;
             40 NEXT I
             RUN
             Random Number Seed (-32768    to 32767)? 3     (user
             types 3)
              .88598 .484668 .586328       .119426    .709225
             Ok
             RUN
             Random Number Seed (-32768    to 32767)? 4 (user
             types 4 for new sequence)
              .803506 .162462 .929364       .292443    .322921
             Ok
             RUN
             Random Number Seed (-32768    to 32767)? 3 (same
             sequence as first RUN)
              .88598 .484668 .586328       .119426    .709225
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
- [REM](rem.md) - To allow explanatory remarks to be inserted in a program
- [SET (setting)](setsetting.md) - Configure interpreter settings at runtime
- [SHOW SETTINGS](showsettings.md) - Display current interpreter settings
- [TRON/TROFF](tron-troff.md) - To trace the execution of program statements
- [USR](../functions/usr.md) - Calls the user's assembly language subroutine with the argument X
- [VARPTR](../functions/varptr.md) - Returns the memory address of a variable
- [WIDTH](width.md) - To set the printed line width in number        of characters for the terminal or line printer
