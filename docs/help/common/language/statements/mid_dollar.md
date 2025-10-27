---
category: strings
description: To replace a portion of one string with    another string
keywords:
- command
- function
- if
- mid
- number
- print
- return
- statement
- string
syntax: MID$«string expl>,n[,m])=<string exp2>
title: MID$
type: statement
---

# MID$

## Syntax

```basic
MID$«string expl>,n[,m])=<string exp2>
_where nand m are integer expressions and
<string expl> and <string exp2> are string
expressions.
```

## Purpose

To replace a portion of one string with    another string.

## Remarks

The characters in <string expl>, beginning at position n, are replaced by the characters in <string exp2>. The optional m refers, to the number of characters from <string exp2> that will be used in the replacement.       If m is omitted, all of <string exp2> is used. However, regardless of whether m is omitted or included, the replacement of characters never goes beyond the original length of <string expl>.

## Example

```basic
10 A$="KANSAS CITY, MO"
              20 MID$(A$,14)="KS"
              30 PRINT A$
              RUN
              KANSAS CITY, KS
              MID$ is also a function that returns a substring
              of a given string. See Section 3.24.
```

## See Also

*Related statements will be linked here*