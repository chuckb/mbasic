---
category: system
description: Display current interpreter settings
keywords: ['show', 'settings', 'display', 'list', 'configuration', 'options']
syntax: SHOW SETTINGS ["pattern"]
title: SHOW SETTINGS
type: statement
related: ['setsetting', 'helpsetting']
---

# SHOW SETTINGS

## Syntax

```basic
SHOW SETTINGS ["pattern"]
```

**Versions:** MBASIC Extension

## Purpose

To display current interpreter settings and their values.

## Remarks

SHOW SETTINGS lists all interpreter settings and their current values. An optional pattern string can filter the display to show only matching settings.

The display typically includes:
- Setting name (in dotted notation)
- Current value
- Setting scope (session, user, system)
- Brief description (if available)

If a pattern is provided, only settings whose names contain the pattern string are shown.

## Example

```basic
SHOW SETTINGS
' Lists all settings

SHOW SETTINGS "display"
' Shows only display-related settings

10 SHOW SETTINGS "editor"
20 INPUT "Change a setting (Y/N)"; A$
```

## Notes

- This is a modern extension not present in original MBASIC 5.21
- Pattern matching is case-insensitive
- Settings are organized by category (display, editor, runtime, etc.)
- Some settings may be read-only

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
- [TRON/TROFF](tron-troff.md) - To trace the execution of program statements
- [USR](../functions/usr.md) - Calls the user's assembly language subroutine with the argument X
- [VARPTR](../functions/varptr.md) - Returns the memory address of a variable
- [WIDTH](width.md) - To set the printed line width in number        of characters for the terminal or line printer
