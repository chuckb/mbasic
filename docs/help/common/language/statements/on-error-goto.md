---
category: error-handling
description: To enable error trapping and specify the   first line of the error handling subroutine
keywords: ['command', 'error', 'execute', 'for', 'goto', 'if', 'line', 'number', 'print', 'statement']
syntax: ON ERROR GOTO <line number>
title: ON ERROR GOTO
type: statement
---

# ON ERROR GOTO

## Syntax

```basic
ON ERROR GOTO <line number>
```

## Purpose

To enable error trapping and specify the   first line of the error handling subroutine.

## Remarks

Once error trapping has been enabled all errors detected, including direct mode errors (e.g., Syntax errors), will cause a jump to         the specified error handling subroutine. If <line number> does not exist, an "Undefined line" error   results.   To disable error trapping, execute an ON ERROR ~TO O.    Subsequent errors will print an error message and halt execution. An ON ERROR GOTO 0 statement that appears in an error trapping subroutine causes BASIC-SO to stop and print the error message for the error that caused the trap.     It is recommended that all error trapping subroutines execute an ON ERROR GOTO 0 if an error is encountered for which there is no recovery action. NOTE:         If an error occurs during execution of an error handling subroutine, the BASIC error message is printed   and   execution   terminates.   Error trapping   does   not occur within the error handling subroutine.

## Example

```basic
10 ON ERROR GOTO 1000
```

## See Also
- [ERROR](error.md) - 1) To simulate the occurrence of a BASIC-80 error1   or 2) to allow error codes to be defined by the user
- [RESUME](resume.md) - Continue program execution after error recovery
