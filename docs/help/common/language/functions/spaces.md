---
category: NEEDS_CATEGORIZATION
description: Returns a string of spaces of length X
keywords: ['for', 'function', 'next', 'print', 'return', 'spaces', 'string']
syntax: SPACE$(X)
title: SPACES
type: function
---

# SPACES

## Syntax

```basic
SPACE$(X)
```

**Versions:** Extended, Disk

## Description

Returns a string of spaces of length X. The expression X is rounded to an integer and must be in the range 0 to 255.

## Example

```basic
10 FOR I = 1 TO 5
 20 X$ = SPACE$(I)
 30 PRINT X$;I
 40 NEXT I
 RUN
 1
 2
 3
 4
 5
 Ok
 Also see the SPC function.
```

## See Also
- [CLOAD THIS COMMAND IS NOT INCLUDED IN THE DEC VT180 VERSION](../statements/cload.md) - To load a program or an array from cassette tape into memory
- [COBL](cobl.md) - Converts X to a double precision number
- [CRR$](crr_dollar.md) - Returns a string whose one element has ASCII code I
- [CSAVE THIS COMMAND IS NOT INCLUDED IN THE DEC VT180 VERSION](../statements/csave.md) - To save the program or an       array   currently     in memory on cassette tape
- [CVI, CVS, CVD](cvi-cvs-cvd.md) - Convert string values to numeric values
- [DEFINT/SNG/DBL/STR](../statements/defint-sng-dbl-str.md) - To declare variable types as integer,        single precision, double precision, or string
- [ERR AND ERL VARIABLES](../statements/err-erl-variables.md) - NEEDS_DESCRIPTION
- [INPUT#](../statements/input_hash.md) - To read data items from a sequential disk    file and assign them to program variables
- [LINE INPUT](../statements/line-input.md) - To input an entire line (up to 254 characters) to   a string variable, without the use of delimiters
- [LPRINT AND LPRINT USING](../statements/lprint-lprint-using.md) - To print data at the line printer
- [MKI$, MKS$, MKD$](mki_dollar-mks_dollar-mkd_dollar.md) - Convert numeric values to string values
- [TAB](tab.md) - Spaces to position I on the terminal
