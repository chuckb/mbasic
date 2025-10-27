# Work in Progress

## Task
Investigate why context affects validation - user rightfully questions this

## User's Question
"How does context make a syntax error or not?"

They're RIGHT - syntax errors should be independent of context!

## Things That ARE Context-Dependent (SEMANTIC, not syntactic):
- Whether a variable is defined
- Whether a function is defined
- Type checking

## Things That ARE NOT Context-Dependent (SYNTACTIC):
- Statement structure (FOR must have TO)
- Token sequences (can't have "PRINT + + 5")
- Parentheses matching
- Valid keywords

## What def_type_map Actually Does
It tracks **DEF FN** user-defined functions:
```basic
10 DEF FNA(X) = X * 2
20 PRINT FNA(5)  <- Parser needs to know FNA is a function, not variable
```

## The Real Question
Why were lines 10-50 showing errors? Let me test:
```basic
10 max_x%=20        <- Simple assignment - pure syntax
20 max_y%=23        <- Simple assignment - pure syntax
30 dim b(max_x%,max_y%)  <- Actually INVALID in MBASIC! DIM needs constants!
```

## Status
- ✅ Tested and found REAL problem: Underscores in variable names!
- ✅ User confirmed they want per-line validation (immediate feedback)
- ✅ Reverted context-based validation - was solving wrong problem
- ✅ Keeping simple per-line syntax checking

## Real Issue
User's program had:
- `max_x%` ← INVALID! Underscore not allowed in MBASIC
- `max_y%` ← INVALID! Underscore not allowed in MBASIC

MBASIC variable names: Letters and digits only, no underscores
Valid: `MAXX%`, `MAXVALUE%`
Invalid: `max_x%`, `my_var%`

## What Works Now
- Each line validated as typed (user likes this)
- Clear error messages via click/cursor/output
- Error: "Lexer error at 1:4: Unexpected character: '_'"
