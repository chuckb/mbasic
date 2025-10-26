---
category: mathematical
description: Returns the truncated integer part of X
keywords:
- fix
- for
- function
- if
- next
- number
- print
- return
syntax: FIX(X)
title: FIX
type: function
---

# FIX

## Syntax

```basic
FIX(X)
```

**Versions:** Extended, Disk

## Description

Returns the truncated integer part of X. FIX(X) is equivalent to SGN(X)*INT(ABS(X)). The major difference between FIX and INT is that FIX does not return the next lower number for negative X.

## Example

```basic
PRINT FIX(58.75)
58
Ok
PRINT FIX(-58.75)
-58
Ok
```

## See Also

* [INT](int.md) - Integer part (rounds down for negative numbers)
* [SGN](sgn.md) - Sign function
* [ABS](abs.md) - Absolute value