---
category: NEEDS_CATEGORIZATION
description: Returns a string whose one element has ASCII code I
keywords: ['crr', 'error', 'for', 'function', 'print', 'return', 'string']
syntax: CHR$(I)
title: CRR$
type: function
---

# CRR$

## Syntax

```basic
CHR$(I)
```

## Description

Returns a string whose one element has ASCII code I. (ASCII codes are listed in Appendix M.) CHR$ is commonly used to send a special character to the terminal. For instance, the BEL character could be sent (CHR$(7» as a preface to an error message, or a form feed could be sent (CRR$(12» to clear a CRT screen and return the cursor to the home position.

## Example

```basic
PRINT CHR$ (66)
 B
 Ok
 See the ASC function for ASCII-to-numeric
 conversion.
```

## See Also
- [CLOAD THIS COMMAND IS NOT INCLUDED IN THE DEC VT180 VERSION](../statements/cload.md) - To load a program or an array from cassette tape into memory
- [COBL](cobl.md) - Converts X to a double precision number
- [CSAVE THIS COMMAND IS NOT INCLUDED IN THE DEC VT180 VERSION](../statements/csave.md) - To save the program or an       array   currently     in memory on cassette tape
- [CVI, CVS, CVD](cvi-cvs-cvd.md) - Convert string values to numeric values
- [DEFINT/SNG/DBL/STR](../statements/defint-sng-dbl-str.md) - To declare variable types as integer,        single precision, double precision, or string
- [ERR AND ERL VARIABLES](../statements/err-erl-variables.md) - NEEDS_DESCRIPTION
- [INPUT#](../statements/input_hash.md) - To read data items from a sequential disk    file and assign them to program variables
- [LINE INPUT](../statements/line-input.md) - To input an entire line (up to 254 characters) to   a string variable, without the use of delimiters
- [LPRINT AND LPRINT USING](../statements/lprint-lprint-using.md) - To print data at the line printer
- [MKI$, MKS$, MKD$](mki_dollar-mks_dollar-mkd_dollar.md) - Convert numeric values to string values
- [SPACES](spaces.md) - Returns a string of spaces of length X
- [TAB](tab.md) - Spaces to position I on the terminal
