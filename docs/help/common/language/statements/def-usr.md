---
category: subroutines
description: To specify the starting address of an assembly language subroutine
keywords: ['def', 'usr', 'assembly', 'subroutine', 'address', 'statement']
syntax: DEF USR[<digit>]=<integer expression>
title: DEF USR
type: statement
---

# DEF USR

## Syntax

```basic
DEF USR[<digit>]=<integer expression>
```

**Versions:** Extended, Disk

## Purpose

To specify the starting address of an assembly language subroutine.

## Remarks

- `<digit>` may be any digit from 0 to 9. The digit corresponds to the number of the USR routine whose address is being specified.
- If `<digit>` is omitted, DEF USR0 is assumed.
- The value of `<integer expression>` is the starting address of the USR routine.
- Any number of DEF USR statements may appear in a program to redefine subroutine starting addresses, thus allowing access to as many subroutines as necessary.
- See Appendix C, Assembly Language Subroutines, in the original MBASIC documentation for details on writing assembly language routines.

## Example

```basic
200 DEF USR0=24000
210 X=USR0(Y^2/2.89)
```

This example defines USR routine 0 to start at memory location 24000, then calls it with a calculated parameter.

## Notes

**⚠️ Implementation Note:** In this Python implementation of MBASIC, assembly language subroutines are not supported. The DEF USR statement is parsed for compatibility but does not provide actual functionality.

## See Also
- [USR](../functions/usr.md) - Call assembly language subroutine
- [DEF FN](def-fn.md) - Define user-defined function
- [POKE](poke.md) - Write byte to memory location
- [PEEK](../functions/peek.md) - Read byte from memory location