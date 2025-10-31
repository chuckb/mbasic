---
category: input-output
description: Read user input from the terminal during program execution
keywords: ['input', 'read', 'prompt', 'keyboard', 'user', 'interactive', 'question mark', 'readline']
syntax: INPUT[;] ["prompt string";]variable[,variable...]
related: ['print', 'line-input', 'read-data']
title: INPUT
type: statement
---

# INPUT

## Syntax

```basic
INPUT[:] [<"prompt string">:]<list of variables>
```

## Purpose

To allow input from the terminal during      program execution.

## Remarks


## Example

```basic
10 INPUT x
            20 PRINT X "SQUARED IS" X"'2
            30 END
            RUN
            ? 5      (The 5 was typed in by the user
                      in response to the question mark.)
             5 SQUARED IS 25
            Ok
            LIST
            10 PI=3.14
            20 INPUT "WHAT IS THE RADIUS":R
            30 A=PI*R"'2
            40 PRINT "THE AREA OF THE CIRCLE IS":A
            50 PRINT
            60 GOTO 20
            Ok
            RUN
            WHAT IS THE RADIUS? 7.4 (User types 7.4)
            THE AREA OF THE CIRCLE IS 171.946
            WHAT IS THE RADIUS?
            etc.
```

## See Also
- [LINE INPUT](line-input.md) - To input an entire line (up to 254 characters) to   a string variable, without the use of delimiters
- [PRINT](print.md) - Output text and values to the screen
- [WRITE](write.md) - To output data at the terminal
