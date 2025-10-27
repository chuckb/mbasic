---
category: program-control
description: To terminate program execution, close all   files and return to command
  level
keywords:
- close
- command
- else
- end
- execute
- file
- goto
- if
- print
- program
syntax: END
title: END
type: statement
---

# END

## Syntax

```basic
END
```

**Versions:** SK, Extended, Disk

## Purpose

To terminate program execution, close all   files and return to command level.

## Remarks

END statements may be placed anywbere in the program to terminate execution. Unlike the STOP statement, END does not cause a BREAK message to be printed.    An END statement at the end of a program is optional. BASIC-aO·always returns to command level after an END is executed.

## Example

```basic
520 IF K>lOOO THEN END ELSE GOTO 20
```

## See Also

*Related statements will be linked here*