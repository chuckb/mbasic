# Variables

**Status:** PLACEHOLDER - Documentation in progress

This page will cover:
- Variable naming rules
- Variable types (INTEGER, SINGLE, DOUBLE, STRING)
- Type suffixes (%, $, !, #)
- DEFINT/DEFSTR/DEFDBL/DEFSNG statements
- Variable scope
- Arrays (DIM statement)

## Placeholder

For now, see:
- `docs/help/common/language/data-types.md` - Data type overview
- `docs/help/common/language/statements/defint-sng-dbl-str.md` - Type declarations
- `docs/help/common/language/statements/dim.md` - Array declaration
- `docs/help/common/language/statements/let.md` - Variable assignment

## Quick Reference

**Type Suffixes:**
- `%` - Integer (e.g., `COUNT%`)
- `$` - String (e.g., `NAME$`)
- `!` - Single precision (default)
- `#` - Double precision (e.g., `PRICE#`)

**Type Declarations:**
```basic
DEFINT I-N    ' Variables starting with I-N are integers
DEFSTR S      ' Variables starting with S are strings
DEFDBL D-E    ' Variables starting with D-E are double precision
```
