---
category: control-flow
description: Execute statements repeatedly with a loop counter
keywords: ['for', 'next', 'loop', 'iteration', 'counter', 'step', 'nested', 'repeat']
syntax: FOR variable = start TO end [STEP increment]
related: ['while-wend', 'goto', 'gosub-return']
title: FOR ••• NEXT
type: statement
---

# FOR ••• NEXT

## Syntax

```basic
FOR <variable>=x TO y [STEP z]
NEXT [<variable>] [,<variable> ••• ]
where x, y and z are numeric expressions.
```

**Versions:** SK, Extended, Disk

## Purpose

To allow a series of instructions        to         be performed in a loop a given number of times.

## Remarks

## See Also
- [GOSUB •.. RETURN](gosub-return.md) - Branch to and return from a subroutine
- [GOTO](goto.md) - Branch unconditionally to a specified line number
- [IF ••• THEN[ ••• ELSE] AND IF ••• GOTO](if-then-else-if-goto.md) - Make decisions and control program flow based on conditional expressions
- [ON ••• GOSUB AND ON ••• GOTO](on-gosub-on-goto.md) - To branch to one of several specified line numbers, depending on the value returned when an expression is evaluated
- [WHILE ••• WEND](while-wend.md) - Execute statements in a loop while a condition is true
