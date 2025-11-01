# Web UI File Browser Double-Click Support

## Issue
Double-clicking files in the web UI file browser doesn't open them. Users must select file then click Open button.

## Root Cause
NiceGUI's `.on('dblclick')` event doesn't fire on `ui.row()` elements. Multiple attempts failed:

### Attempted Solutions (All Failed)
1. **v1.0.331**: Lambda with async function - `lambda p=file_path: self._handle_file_doubleclick(p)`
2. **v1.0.332**: Factory function returning async closure - `make_dblclick_handler(file_path)`
3. **v1.0.333**: `functools.partial` binding - `partial(self._handle_file_doubleclick, file_path)`
4. **v1.0.333**: Factory with explicit select+open and debug logging

None of these produce any output in stderr, meaning the event handler isn't being called at all.

## Why It Fails
- NiceGUI `.on('dblclick')` doesn't work on regular `ui.row()` elements
- Only specific components support it (e.g., `table.on('rowDblclick')` works - see line 299)
- The event simply never fires

## Possible Solutions

### Option 1: Use JavaScript addEventListener
Directly attach `dblclick` event handler via JavaScript:
```python
file_row.on('dblclick', handler)  # This doesn't work
# Instead:
ui.run_javascript(f'''
    document.querySelector('[data-id="{file_row.id}"]')
        .addEventListener('dblclick', () => {{
            // Call Python handler
        }});
''')
```
Problem: Need to expose Python callback to JavaScript

### Option 2: Track Click Timing
Detect double-click by tracking time between clicks:
```python
last_click_time = 0
last_click_file = None

def _on_file_click(file_path):
    now = time.time()
    if (now - last_click_time < 0.5 and
        last_click_file == file_path):
        # Double click!
        await _open_selected()
    else:
        # Single click
        _select_file(file_path)
    last_click_time = now
    last_click_file = file_path
```
Problem: Complicates logic, may feel laggy

### Option 3: Add "Open on Select" Toggle
Add checkbox: "☐ Open files immediately when selected"
- When enabled, single click opens file
- When disabled, must use Open button (current behavior)
- Lets user choose their preferred workflow

### Option 4: Do Nothing
Current workaround works fine:
- Single-click to select file
- Click "Open" button to open
- This is explicit and clear
- No risk of accidental opens

## Current Status
**Open button works correctly** (fixed in v1.0.332)
- Users can reliably open files
- Just requires two clicks instead of double-click

## Recommendation
**Option 4 (Do Nothing)** - The Open button workflow is clear and reliable. Double-click is a nice-to-have but not critical for functionality.

If we want to improve UX later, **Option 3** (toggle) or **Option 1** (JavaScript) are best approaches.

## Related Code
- `src/ui/web/nicegui_backend.py:469-481` - File row click/dblclick handlers
- `src/ui/web/nicegui_backend.py:299` - Example of working `rowDblclick` on table
- `src/ui/web/nicegui_backend.py:421-423` - Open button (works correctly)

## Priority
Low - workaround exists and works well

## Date Created
2025-11-01
