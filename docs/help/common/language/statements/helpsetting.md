---
category: system
description: Display help for a specific setting
keywords: ['help', 'setting', 'documentation', 'describe']
syntax: HELP SET "setting.name"
title: HELP SET
type: statement
related: ['setsetting', 'showsettings']
---

# HELP SET

## Syntax

```basic
HELP SET "setting.name"
```

**Versions:** MBASIC Extension

## Purpose

To display detailed help information for a specific interpreter setting.

## Remarks

HELP SET displays comprehensive documentation for a named setting, including:
- Full setting name
- Description of what the setting controls
- Valid values and data type
- Default value
- Scope (session, user, system)
- Related settings
- Usage examples

This is useful for understanding what a setting does before changing it, or for discovering the valid values for a setting.

## Example

```basic
HELP SET "display.width"
HELP SET "editor.tabsize"

10 INPUT "Setting name"; S$
20 HELP SET S$
30 INPUT "New value"; V
40 SET S$ V
```

## Notes

- This is a modern extension not present in original MBASIC 5.21
- Setting names are case-insensitive
- Unknown setting names produce an error message
- Use SHOW SETTINGS to discover available setting names

## See Also
- [FRE](../functions/fre.md) - Arguments to FRE are dummy arguments
- [INKEY$](../functions/inkey_dollar.md) - Returns either a one-character string cont~ining a character read from the terminal or a null string if no character is pending at the terminal
- [INP](../functions/inp.md) - Returns the byte read from port I
- [LIMITS](limits.md) - Display resource usage and interpreter limits
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
