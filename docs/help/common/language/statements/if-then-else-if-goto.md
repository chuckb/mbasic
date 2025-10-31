---
category: control-flow
description: Make decisions and control program flow based on conditional expressions
keywords: ['if', 'then', 'else', 'goto', 'condition', 'test', 'decision', 'branch', 'nested']
aliases: ['if-then', 'if-goto', 'if-then-else']
syntax: IF expression THEN statement|line_number [ELSE statement|line_number]
related: ['while-wend', 'for-next', 'goto', 'on-goto']
title: IF ••• THEN[ ••• ELSE] AND IF ••• GOTO
type: statement
---

# IF ••• THEN[ ••• ELSE] AND IF ••• GOTO

## Syntax

```basic
IF <expression> THEN <statement(s»          <line number>
,
[ELSE <statement(s)>     I <line number>]
IF <expression> GOTO <line number>
[ELSE <statement(s)>     I <line number>]
```

**Versions:** SK, Extended, Disk NOTE:          The ELSE clause is allowed only in Extended        and Disk versions.

## Purpose

To make a decision regarding program flow       based on the result returned by an expression.

## Remarks

## See Also
- [FOR ••• NEXT](for-next.md) - Execute statements repeatedly with a loop counter
- [GOSUB •.. RETURN](gosub-return.md) - Branch to and return from a subroutine
- [GOTO](goto.md) - Branch unconditionally to a specified line number
- [ON ••• GOSUB AND ON ••• GOTO](on-gosub-on-goto.md) - To branch to one of several specified line numbers, depending on the value returned when an expression is evaluated
- [WHILE ••• WEND](while-wend.md) - Execute statements in a loop while a condition is true
