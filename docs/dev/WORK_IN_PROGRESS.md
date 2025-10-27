# Work in Progress

## Task
Fix Tk UI error display - red ? appears but no error message shown

## Problem
User pasted BASIC program, got red ? on most lines, but:
- No error messages in output window
- Clicking red ? doesn't show the error
- User has no idea what's wrong

## Test Program
```basic
10 max_x%=20
20 mas_y%=23
10 dim b(max_x%,max_y%)
20 for x%=0 to max_x%
30   for y%=0 to max_y%
30     b(x%,y%)=x% * y%
40 next x%,y%
50 goto 10
```

Issues I can see:
- Duplicate line numbers (10, 20, 30 appear twice)
- Invalid NEXT syntax: `next x%,y%`
- Typo: mas_y% vs max_y%

## Status
- ✅ Found where red ? is added (tk_widgets.py set_error)
- ✅ Found where error messages were being thrown away
- ✅ Fixed error message storage in line metadata
- ✅ Fixed error message display in status bar when cursor on error line
- ✅ Updated all set_error calls to pass error messages

## Files to Check
- src/ui/tk_ui.py - Red ? indicator logic
- Error display in output window
- Click handler for red ?

## Context
This is a critical usability bug - users can't fix errors if they don't know what they are.
