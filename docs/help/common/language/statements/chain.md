---
category: program-control
description: To call a program and pass variables to it            from the current program
keywords: ['chain', 'command', 'file', 'for', 'function', 'if', 'line', 'number', 'open', 'program']
syntax: CHAIN [MERGE] <filename>[,[<line number exp>]
title: CHAIN
type: statement
---

# CHAIN

## Syntax

```basic
CHAIN [MERGE] <filename>[,[<line number exp>]
[,ALL] [,DELETE<range>]]
```

**Versions:** Disk

## Purpose

To call a program and pass variables to it            from the current program.

## Remarks

## See Also
- [CLEAR](clear.md) - To set all numeric variables to zero and all string variables to null; and, optionally, 'to set the end of memory and the amount of stack space
- [COMMON](common.md) - To pass variables to a CHAINed program
- [CONT](cont.md) - To continue program execution after a Control-C has been typed, or a STOP or END statement has been executed
- [END](end.md) - To terminate program execution, close all   files and return to command level
- [NEW](new.md) - To delete the program currently   in   memory   and clear all variables
- [RUN](run.md) - Executes the current program or loads and runs a program from disk
- [STOP](stop.md) - To terminate program      execution   and    return   to command level
- [SYSTEM](system.md) - Exits MBASIC and returns to the operating system
