# Work in Progress

## Task
Implement array element selector - allow editing ANY array cell by typing indices

## Status
- ✅ Implemented Tk UI - dialog with subscripts field
- ✅ Implemented Curses UI - two-step prompt (indices then value)
- ✅ Implemented Web UI - dialog with subscripts field
- ⏳ Ready for testing

## Files Being Modified
- src/ui/tk_ui.py - Adding subscripts input to _edit_array_element
- src/ui/curses_ui.py - Adding subscripts prompt
- src/ui/web/web_ui.py - Adding subscripts input field

## Implementation Plan
1. Tk UI: Add subscripts Entry field to dialog
2. Curses UI: Two-step prompt (get indices, then value)
3. Web UI: Add subscripts input field to dialog
4. Test with 1D, 2D, and 3D arrays

## Context/Notes
User has requested this 5 times - need to implement NOW, not document.
Current limitation: Can only edit last accessed array element.
Target: User types "1,2,3" to choose which element to edit.
