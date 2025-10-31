---
category: control-flow
description: Execute statements in a loop while a condition is true
keywords: ['while', 'wend', 'loop', 'condition', 'test', 'repeat', 'nested']
aliases: ['while-wend']
syntax: WHILE expression ... WEND
related: ['for-next', 'if-then-else-if-goto', 'goto']
title: WHILE ••• WEND
type: statement
---

# WHILE ••• WEND

## Syntax

```basic
WHILE <expression>
[<loop statements>]
WEND
```

## Purpose

To execute a series of statements in a   loop   as long as a given condition is true.

## Remarks

If <expression> is not zero (Le., true), <loop statements>    are  executed   until    the WEND statement is encountered. BASIC then returns to the WHILE statement and checks <expression>. If it is still true, the process is repeated.    If it is not true, execution resumes with the statement following the WEND statement. WHILE/WEND loops may be nested to any level. Each WEND will match the most recent WHILE. An unmatched WHILE statement causes       a    nWHILE without WEND n error, and an unmatched WEND statement causes a nWEND without WHILE n error,.

## Example

```basic
90~BUBBLE SORT ARRAY A$
              100 FLIPS=l ~FORCE ONE PASS TaRU LOOP
              110 WHILE FLIPS
              115        FLIPS=O
              120        FOR I=l TO J-l
              130                IF A$(I»A$(I+l) THEN
                                         SWAP A$(I) ,A$(I+l) :FLIPS=l
              140        NEXT I
              150 WEND
```

## See Also
- [FOR ••• NEXT](for-next.md) - Execute statements repeatedly with a loop counter
- [GOSUB •.. RETURN](gosub-return.md) - Branch to and return from a subroutine
- [GOTO](goto.md) - Branch unconditionally to a specified line number
- [IF ••• THEN[ ••• ELSE] AND IF ••• GOTO](if-then-else-if-goto.md) - Make decisions and control program flow based on conditional expressions
- [ON ••• GOSUB AND ON ••• GOTO](on-gosub-on-goto.md) - To branch to one of several specified line numbers, depending on the value returned when an expression is evaluated
