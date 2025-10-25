# Syntax Checking Improvements

## Changes Made

### Issue 1: Fixed errors remain in output window
**Problem:** When syntax errors are fixed, the error messages remain in the output window.

**Solution:** Track whether the output window is currently showing syntax errors using `_showing_syntax_errors` flag. Clear the output window only when errors are fixed AND the output was showing syntax errors.

**Code changes:**
- Added `_showing_syntax_errors = False` flag in `__init__()`
- Modified `_display_syntax_errors()` to:
  - Set `_showing_syntax_errors = True` when displaying errors
  - Clear output and set `_showing_syntax_errors = False` when no errors and flag is True

### Issue 2: Errors show while typing incomplete lines
**Problem:** Syntax checking triggers 0.1s after every keystroke, showing annoying errors for incomplete statements like "FOR I = 1".

**Solution:** Only check syntax when leaving a line or pressing control keys, not during normal typing.

**Code changes:**
- Removed syntax checking from `_perform_deferred_refresh()` (which triggers on every keystroke)
- Added syntax checking to `keypress()` when:
  - Control keys are pressed (Ctrl+R, Ctrl+S, etc.)
  - Up/Down arrows are pressed (leaving current line)
  - Page Up/Down, Home/End are pressed (navigation)
  - Enter key is pressed

**Benefits:**
- No more annoying error messages while typing incomplete statements
- Errors appear when you navigate away from the line or run a command
- Much better user experience

## Testing

Created `utils/test_syntax_checking.py` to verify:
1. ✅ Incomplete lines show errors when checked
2. ✅ Bare identifiers show errors
3. ✅ Valid statements don't show errors
4. ✅ Errors are cleared from output when fixed
5. ✅ Lines with errors are marked with '?', valid lines are not

All tests pass successfully.

## Files Modified

- `/home/wohl/cl/mbasic/src/ui/curses_ui.py`
  - Added `_showing_syntax_errors` flag
  - Modified `_display_syntax_errors()` to clear output when errors fixed
  - Removed syntax checking from `_perform_deferred_refresh()`
  - Added syntax checking to `keypress()` for navigation/control keys

## Usage

**Before:** Syntax errors appeared 0.1s after every keystroke, even for incomplete lines.

**After:** Syntax errors only appear when:
- You press Up/Down arrow to move to another line
- You press a control key (Ctrl+R, Ctrl+S, etc.)
- You press Page Up/Down, Home/End
- You press Enter to create a new line

**Example workflow:**
```
Type: 10 FOR I = 1     (no error shown while typing)
Press Down arrow       (syntax check runs, error shown in output if incomplete)
Complete: TO 10        (finish the statement)
Press Down arrow       (syntax check runs, error clears from output)
```
