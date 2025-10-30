# Error Handling

**Status:** PLACEHOLDER - Documentation in progress

This page will cover:
- Common errors and how to fix them
- ON ERROR GOTO statement
- ERL and ERR functions
- RESUME statement
- Debugging errors

## Placeholder

For now, see:
- `docs/help/common/language/statements/on-error-goto.md` - Error handling statement
- `docs/help/common/language/statements/err-erl-variables.md` - Error variables
- `docs/help/common/language/statements/resume.md` - RESUME statement
- `docs/help/common/language/appendices/error-codes.md` - Error code reference

Error handling in MBASIC:
```basic
10 ON ERROR GOTO 1000
20 ' Your code here
30 END
1000 PRINT "Error"; ERR; "at line"; ERL
1010 RESUME NEXT
```
