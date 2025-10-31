---
category: system
description: Configure interpreter settings at runtime
keywords: ['set', 'setting', 'configure', 'option', 'preference', 'runtime']
syntax: SET "setting.name" value
title: SET (setting)
type: statement
related: ['showsettings', 'helpsetting']
---

# SET (setting)

## Syntax

```basic
SET "setting.name" value
```

**Versions:** MBASIC Extension

## Purpose

To configure interpreter settings and options at runtime.

## Remarks

SET allows programs to dynamically configure interpreter behavior by modifying settings. The setting name is a string in dotted notation (e.g., "display.width", "editor.tabsize").

Settings can control:
- Display and output formatting
- Editor behavior
- Runtime options
- UI preferences

Settings persist for the current session or can be saved to configuration files depending on the setting scope.

## Example

```basic
SET "display.width" 80
SET "editor.tabsize" 4

10 SET "runtime.strict_mode" 1
20 PRINT "Strict mode enabled"

100 INPUT "Tab size"; T
110 SET "editor.tabsize" T
```

## Notes

- This is a modern extension not present in original MBASIC 5.21
- Available settings are implementation-specific
- Use SHOW SETTINGS to list all available settings
- Use HELP SET "name" to get help on a specific setting
- Invalid setting names produce an error

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
- [SHOW SETTINGS](showsettings.md) - Display current interpreter settings
- [TRON/TROFF](tron-troff.md) - To trace the execution of program statements
- [USR](../functions/usr.md) - Calls the user's assembly language subroutine with the argument X
- [VARPTR](../functions/varptr.md) - Returns the memory address of a variable
- [WIDTH](width.md) - To set the printed line width in number        of characters for the terminal or line printer
