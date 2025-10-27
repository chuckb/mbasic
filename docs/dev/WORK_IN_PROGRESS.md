# Work in Progress

## Task
Fix error display - user still getting red ? with no error message

## Problem
After my fix, user still sees:
- Red ? on lines with errors
- No error message when cursor on line
- Clicking red ? doesn't show error

## Test Code
```basic
10 max_x%=20
20 max_y%=23
30 dim b(max_x%,max_y%)
40 for x%=0 to max_x%
50   for y%=0 to max_y%
60     b(x%,y%)=x% * y%
70 next x%,y%          <- ERROR: Invalid syntax (can't do next x%,y%)
80 goto 10
```

## Issues to Fix
1. My status bar solution requires cursor movement - might not be intuitive
2. No click handler for red ? indicator
3. Need to test if error messages are actually being captured

## Status
- ⏳ Testing current implementation
- ⏸️ Add click handler for red ? in status column
- ⏸️ Consider showing all errors in output on validation

## Next Steps
1. Add click handler to status column (●/?) indicators
2. Show error in dialog or output when clicking ?
3. Maybe auto-show all errors in output window
