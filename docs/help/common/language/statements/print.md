---
title: PRINT
type: statement
category: input-output
keywords: ['print', 'output', 'display', 'console', 'write', 'show', 'terminal', 'question mark']
aliases: ['?']
description: Output text and values to the screen
syntax: PRINT [expression[;|,]...]
related: ['input', 'print-using', 'write', 'lprint']
---

# PRINT

## Syntax

```basic
PRINT [<list of expressions>]
PRINT USING <string   exp>~<list   of expressions>
```

**Versions:** 8K, Extended, Disk Extended, Disk

## Purpose

To output data at the terminal. To print strings or numbers    using    a   specified format •. Remarks        <list of expressions> is comprised of the string and            expressions or numeric expressions that are to

## Remarks


## Example

```basic
be printed, separated by semicolons.     <string
               exp> is a string literal (or variable) comprised
               of   special   formatting   ch?lracters.   These
               formatting characters (see below) determine the
               field and the format of the printed strings or
               numbers.
                          String Fields
               When PRINT USING is used to print strings, one
               of three formatting characters may be used to
               format the string field:
       "!"     Specifies that only the first character       in   the
               given string is to be printed.
"\n spaces\"     Specifies that 2+n characters from the string
               are to be printed. If the backslashes are typed
               with no spaces, two characters will be printed~
               with   one   space, three characters will be
               printed, and so on. If the string is longer
               than   the   field, the extra characters are
               ignored. If the field is lonnger than the
               string, the string will be left-justified in the
               field and padded with spaces on the right.
               Example:
               10 A$="LOOK":B$="OUT"
               30 PRINT USING "!"~A$~B$
               40 PRINT USING"\ \"~A$~B$
               50 PRINT USING"\    \"~A$~B$~"!!"
               RUN
               LO
               LOOKOUT
               LOOK OUT   !!
    "&"    Specifies a variable length string field. When
           the field is specified with "&", the string is
           output exactly as input. Example:
           10 A$="LOOK" :B$="OUT"
           20 PRINT USING "!"~A$~
           30 PRINT USING "&"~B$
           RUN
           LOUT
                          Numeric Fields
           When PRINT USING is used to print numbers, the
           following special characters may be used to
           format the numeric field:
      #    A number sign is used to represent each digit
           position.   Digit positions are always filled.
           If the number to be printed has fewer digits
           than positions specified, the number will be
           right-justified (preceded by spaces)   in the
           field.
            A decimal point may be inserted at any position
            in the field.     If the format string specifies
            that a digit is to precede the decimal point,
            the digit will always be printed (as 0 if
            necessary). Numbers are rounded as necessary.
            PRINT USING    nit.iin~.78
             0.78
            PRINT USING    "##i.t#"~987.654
            987.65
            PRINT USING "ii.ii    "~10.2,5.3,66.789,.234
            10.20    5.30   66.79     0.23
            In the last example, three spaces were inserted
            at the end of the format string to separate the
            printed values on the line.
      +     A plus sign at the beginning or end of the
            format string will cause ·the sign of the number
            (plus or minus) to be printed before or after
            the number.
           A minus sign at the end of the format field will
           cause negative numbers to be printed with a
           trailing minus sign.
            PRINT USING "+.....   ";-68.95,2.4,55.6,-.9
            -68.95    +2.40   +55.60    -0.90
            PRINT USING " •••• #-    ";-68.95,22.449,-7.01
            68.95-   22.45        7.01-
     **     A double asterisk at the beginning of the format
            string causes leading spaces in the numeric
            field to be filled with asterisks. The ** also
            specifies positions for two more digits.
            PRINT USING "** •• #   ";12.39,-0.9,765.1
            *12.4   *-0.9    765.1
     $$     A double dollar sign causes a dollar sign to be
            printed to the immediate left of the formatted
            number.   The $$ specifies two      more   digit
            positions, one of which is the dollar sign. The
            exponential format cannot be used with $$.
            Negative numbers cannot be used unless the minus
            sign trails to the right.
            PRINT USING "$$## •• '.";456.78
             $456.78
    **$    The **$ at the beginning of a format string
           combines the effects of the above two symbols.
           Leading spaces will be asterisk-filled and a
           dollar sign will be printed before the number.
           **$ specifies three more digit positions, one of
           which is the dollar sign.
            PRINT USING "**$ ••• '.";2.34
            ***$2.34
            A comma that is to the left of the decimal point
            in a formatting string causes a comma to be
            printed to the left of every third digit to the
            left of the decimal point. A comma that is at
            the en~ of the format string is printed as part
            of the string. A comma specifies another digit
            position. The comma has no effect if used with
            the exponential (AAAA) format.
            PRINT USING " •• '., ••• ";1234.5
            1,234.50
            PRINT USING " ••••••• ,";1234.5
            1234.50,
           Four carats (or up-arrows) may be placed after
           the   digit   position   characters to specify
           exponential format. The four carats allow space
           for E+xx to be printed.       Any decimal point
           position may be specified.      The significant
           digits are left-justified, and the exponent is
           adjusted. Unless a leading + or trailing + or -
           is specified, one digit position will be used to
           the left of the decimal point to print a space
           or a minus sign.
            PRINT USING   "*#.#*~~~~";234.56
             2.35E+02
            PRINT USING   ".####~~~~-";888888
             .8889E+06
            PRINT USING "+.##AAAA";123
            +.12E+03
           An underscore in the format string causes the
           next   character to be output as a literal
           character.
            PRINT USING "_1##.#*_1 ";12.34
            112.341
            The literal character    itself   may   be   an
            underscore by placing "_" in the format string.
      %     If the number to be printed is larger than the
            specified numeric field, a percent sign is
            printed in front of the number.     If rounding
            causes the number to exceed the field, a percent
            sign will be printed in front of the rounded
            number.
            PRINT USING "##.##";111.22
            %111.22
            PRINT USING ".##";.999
            %1.00
            If the number of digits specified exceeds 24, an
            "Illegal function call" error will result.
```

## See Also
- [INPUT](input.md) - Read user input from the terminal during program execution
- [WRITE](write.md) - To output data at the terminal
