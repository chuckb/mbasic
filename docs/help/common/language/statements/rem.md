---
category: system
description: To allow explanatory remarks to be inserted in a program
keywords: ['branch', 'command', 'execute', 'for', 'gosub', 'goto', 'line', 'next', 'program', 'put']
syntax: REM <remark>
title: REM
type: statement
---

# REM

## Syntax

```basic
REM <remark>
```

## Purpose

To allow explanatory remarks to be inserted in a program.

## Remarks

REM statements are not executed but are output exactly as entered when the program is listed. REM statements may be branched into (from a GOTO or GOSUB statement), and execution will continue with the first executable statement after the REM statement. In the Extended and Disk versions, remarks may be added to the end of a line by preceding the remark with a single quotation mark instead of : REM.

## Example

```basic
..
             120 REM CALCULATE AVERAGE VELOCITY
             130 FOR I=1 TO 20
             140 SUM=SUM + V(I)
             or, with Extended and Disk versions:
             120 FOR I=l TO 20     ~CALCULATE   AVERAGE VELOCITY
             130 SUM=SUM+V(I)
             140 NEXT I
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
- [SET (setting)](setsetting.md) - Configure interpreter settings at runtime
- [SHOW SETTINGS](showsettings.md) - Display current interpreter settings
- [TRON/TROFF](tron-troff.md) - To trace the execution of program statements
- [USR](../functions/usr.md) - Calls the user's assembly language subroutine with the argument X
- [VARPTR](../functions/varptr.md) - Returns the memory address of a variable
- [WIDTH](width.md) - To set the printed line width in number        of characters for the terminal or line printer
