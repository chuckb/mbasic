---
category: system
description: To set the printed line width in number        of characters for the terminal or line printer
keywords: ['command', 'for', 'function', 'if', 'line', 'number', 'print', 'return', 'statement', 'width']
syntax: WIDTH [LPRINT] <integer expression>
title: WIDTH
type: statement
---

# WIDTH

## Implementation Note

⚠️ **Emulated as No-Op**: This statement is parsed for compatibility but performs no operation.

**Behavior**: Statement executes successfully without errors, but does not affect output width.

**Why**: Terminal and UI width is controlled by the operating system or UI framework, not the BASIC program. The WIDTH statement cannot actually change these settings.

**Note**: Programs using WIDTH will run without errors, but width settings are silently ignored.

**Limitations**: The "WIDTH LPRINT" syntax is not supported (parse error). Only the simple "WIDTH <number>" form is accepted.

**Historical Reference**: The documentation below is preserved from the original MBASIC 5.21 manual for historical reference.

---

## Syntax

```basic
WIDTH <integer expression>
```

Original MBASIC 5.21 also supported:
```basic
WIDTH LPRINT <integer expression>  ' NOT SUPPORTED in this implementation
```

## Purpose

To set the printed line width in number of characters for the terminal or line printer.

## Remarks

If the LPRINT option is omitted, the line width is set at the terminal. If LPRINT is included, the line width is set at the line printer. <integer expression> must have a value in the range 15 to 255.      The default width is 72 characters. If <integer expression> is 255, the line width is "infinite," that is, BASIC never inserts a carriage return. However, the position of the cursor or the print head, as given by the POS or LPOS function, returns to zero after position 255.

## Example

```basic
10 PRINT "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
               RUN
               ABCDEFGHIJKLMNOPQRSTUVWXYZ
               Ok
               WIDTH 18
               Ok
               RUN
               ABCDEFGHIJKLMNOPQR
               STUVWXYZ
               Ok
BASIC-SO COMMANDS AND STATEMENTS                      Page 2-S4
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
- [TRON/TROFF](tron-troff.md) - To trace the execution of program statements
- [USR](../functions/usr.md) - Calls the user's assembly language subroutine with the argument X
- [VARPTR](../functions/varptr.md) - Returns the memory address of a variable
