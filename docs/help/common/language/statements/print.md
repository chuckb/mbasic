# PRINT Statement

Output text and numbers to the screen.

## Syntax

```basic
PRINT [expression] [separator] [expression] ...
```

Where separator is:
- `;` - No space between values
- `,` - Tab to next print zone (14 columns)

## Description

The PRINT statement outputs text, numbers, and expressions to the screen. If no expression is given, it prints a blank line.

## Examples

### Basic Output
```basic
10 PRINT "Hello, World!"
20 PRINT 42
```

### Multiple Values
```basic
10 A = 10
20 B = 20
30 PRINT "A="; A; " B="; B
```
Output: `A=10 B=20`

### Using Commas for Columns
```basic
10 PRINT "Name", "Age", "Score"
20 PRINT "Alice", 25, 95
```

### Suppressing Newline
```basic
10 PRINT "Enter your name: ";
20 INPUT N$
```

## Notes

- The semicolon (`;`) suppresses the automatic newline
- PRINT with no arguments prints a blank line
- Commas (`,`) tab to next 14-column zone
- String literals use double quotes: `"text"`

## See Also

- [INPUT](input.md) - Get input from user
- [Variables](../data-types.md) - About variables and types
