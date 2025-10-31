---
category: system
description: Display resource usage and interpreter limits
keywords: ['limits', 'resources', 'memory', 'usage', 'system', 'diagnostics']
syntax: LIMITS
title: LIMITS
type: statement
---

# LIMITS

## Syntax

```basic
LIMITS
```

**Versions:** MBASIC Extension

## Purpose

To display current resource usage and interpreter limits.

## Remarks

LIMITS is a diagnostic statement specific to this MBASIC implementation. It displays information about:
- Memory usage
- Variable storage
- String space
- Stack depth
- Other interpreter resource limits

This command is useful for:
- Debugging programs that approach resource limits
- Understanding program resource requirements
- Optimizing programs for better resource usage

## Example

```basic
LIMITS

100 DIM A(1000)
110 LIMITS
120 PRINT "After allocating array"
```

## Notes

- This is a modern extension not present in original MBASIC 5.21
- Output format is implementation-specific
- Useful for development and debugging

## See Also
- [FRE](../functions/fre.md) - Arguments to FRE are dummy arguments
- [HELP SET](helpsetting.md) - Display help for a specific setting
- [INKEY$](../functions/inkey_dollar.md) - Returns either a one-character string cont~ining a character read from the terminal or a null string if no character is pending at the terminal
- [INP](../functions/inp.md) - Returns the byte read from port I
- [NULL](null.md) - To set the number of nulls to be printed at   the end of each line
- [PEEK](../functions/peek.md) - Returns the byte (decimal integer in the range 0 to 255) read from memory location I
- [RANDOMIZE](randomize.md) - To reseed the random number generator
- [REM](rem.md) - To allow explanatory remarks to be inserted in a program
- [SET (setting)](setsetting.md) - Configure interpreter settings at runtime
- [SHOW SETTINGS](showsettings.md) - Display current interpreter settings
- [TRON/TROFF](tron-troff.md) - To trace the execution of program statements
- [USR](../functions/usr.md) - Calls the user's assembly language subroutine with the argument X
- [VARPTR](../functions/varptr.md) - Returns the memory address of a variable
- [WIDTH](width.md) - To set the printed line width in number        of characters for the terminal or line printer
