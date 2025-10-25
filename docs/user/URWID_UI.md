# Urwid-based Curses UI

## Overview

The new urwid-based curses UI provides a modern, full-screen terminal interface for MBASIC. It replaces the legacy npyscreen implementation with a cleaner, more maintainable codebase.

## Installation

```bash
# Install urwid
pip install urwid

# Or install all optional dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Start with new urwid UI
python3 mbasic.py --backend curses

# Load a program file
python3 mbasic.py --backend curses program.bas
```

## Features

### Current Implementation

- **Full-screen editor** - Multi-line text editor for BASIC programs
- **Output window** - Displays program execution results
- **Status bar** - Shows current state and keyboard shortcuts
- **Program execution** - Run BASIC programs and see output
- **Help system** - Built-in help dialog (press Ctrl+H)
- **Line-based editing** - Traditional BASIC line number editing

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+Q` | Quit the program |
| `Ctrl+H` | Show help dialog |
| `Ctrl+R` | Run the current program |
| `Ctrl+L` | List program lines |
| `Ctrl+N` | New program (clear editor) |
| `Ctrl+S` | Save program to file |
| `Ctrl+O` | Open/Load program from file |

### UI Layout

```
┌─────────────────────────────────────────────┐
│ Editor (70% of screen)                      │
│ ┌─────────────────────────────────────────┐ │
│ │ 10 PRINT "Hello, World!"                │ │
│ │ 20 PRINT "2 + 2 = "; 2 + 2              │ │
│ │ 30 END                                  │ │
│ │                                         │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ Output (30% of screen)                      │
│ ┌─────────────────────────────────────────┐ │
│ │ Hello, World!                           │ │
│ │ 2 + 2 =  4                              │ │
│ │ Program completed                       │ │
│ └─────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│ Status: Ready - Press Ctrl+H for help          │
└─────────────────────────────────────────────┘
```

## How to Use

### 1. Enter a Program

Type BASIC code with line numbers in the editor:

```basic
10 PRINT "Hello, World!"
20 FOR I = 1 TO 5
30 PRINT "Count: "; I
40 NEXT I
50 END
```

### 2. Run the Program

Press `Ctrl+R` to execute. The output will appear in the output window below the editor.

### 3. List the Program

Press `Ctrl+L` to see a formatted listing of your program.

### 4. Clear and Start Over

Press `Ctrl+N` to clear the editor and start a new program.

### 5. Get Help

Press `Ctrl+H` anytime to see the help dialog with all keyboard shortcuts.

## Implementation Details

### Architecture

The urwid UI follows the standard `UIBackend` interface defined in `src/ui/base.py`:

```python
class CursesBackend(UIBackend):
    """Urwid-based curses UI backend."""

    def __init__(self, io_handler, program_manager):
        # Initialize widgets
        self.editor = EditorWidget()
        self.output = urwid.Text("")
        self.status_bar = urwid.Text("...")

    def start(self):
        # Create UI layout
        self._create_ui()
        # Run main loop
        self.loop.run()
```

### Program Execution

When you press `Ctrl+R`, the UI:

1. **Parses editor content** - Extracts line-numbered statements
2. **Loads into program manager** - Converts text to program lines
3. **Creates capturing IO handler** - Intercepts PRINT output
4. **Runs interpreter** - Executes the program
5. **Displays results** - Shows output in the output window

### Output Capture

Program output is captured using a custom IO handler:

```python
class CapturingIOHandler:
    def __init__(self, output_list):
        self.output_list = output_list

    def output(self, text, end='\n'):
        """Capture PRINT statements to list."""
        self.output_list.append(str(text))
```

This allows PRINT statements to display in the output window instead of the terminal.

### Widget Structure

The UI uses urwid's pile layout:

```python
pile = urwid.Pile([
    ('weight', 7, editor_frame),    # 70% - Editor
    ('weight', 3, output_frame),    # 30% - Output
    ('pack', self.status_bar)       # Fixed - Status
])
```

## Features

The urwid-based curses UI provides a modern, full-featured terminal interface:

- **Active Maintenance**: urwid is actively maintained with regular updates
- **Comprehensive Documentation**: Extensive documentation and examples available
- **Clean API**: Pythonic and intuitive widget library
- **Better Performance**: Optimized rendering and event handling
- **No Cursor Bugs**: Stable cursor positioning and display
- **Extensive Widgets**: Rich widget library for complex UIs

## Current Limitations

### Implemented Features

- ✅ **Program execution** - Run BASIC programs
- ✅ **INPUT statements** - Interactive user input via dialog
- ✅ **File operations** - Save and Load programs (Ctrl+S, Ctrl+O)
- ✅ **Program listing** - View program lines (Ctrl+L)
- ✅ **Help system** - Built-in help dialog (Ctrl+H)

### Not Yet Implemented

- **Breakpoints** - Visual breakpoint indicators
- **Debugging** - Step, Continue, End commands
- **Menus** - File, Edit, Run menus
- **Syntax highlighting** - Colorized BASIC keywords
- **Mouse support** - Click to position cursor, toggle breakpoints
- **Line editing** - Auto-renum, delete ranges

### Future Development

Advanced features planned for future releases:
- Breakpoints and debugging (Step, Continue, End)
- Full menu system
- Mouse support for all operations

## Development

### Adding New Features

1. Edit `src/ui/curses_ui.py`
2. Add keyboard shortcut in `_handle_input()`
3. Implement handler method (e.g., `_save_program()`)
4. Update help text in `_show_help()`
5. Test with real programs

### Testing

Manual testing:

```bash
# Create test program
cat > test.bas << 'EOF'
10 PRINT "Test"
20 END
EOF

# Run with urwid UI
python3 mbasic.py --backend curses test.bas
```

### Debug Mode

To see error details:

```bash
python3 mbasic.py --backend curses --debug
```

Errors will appear in the output window with full tracebacks.

## Roadmap

### Short Term (v1.0)

- [ ] Add INPUT statement support
- [ ] Implement Save/Load from UI
- [ ] Add line editing commands
- [ ] Improve error messages

### Medium Term (v1.5)

- [ ] Add breakpoint support
- [ ] Implement Step/Continue/End
- [ ] Add syntax highlighting
- [ ] Create menu system

### Long Term (v2.0)

- [ ] Mouse support for all operations
- [ ] Split-pane view (code + output side-by-side)
- [ ] Watch window for variables
- [ ] Call stack viewer
- [ ] Deprecate npyscreen backend

## Resources

- **Urwid Tutorial**: http://urwid.org/tutorial/
- **Urwid Reference**: http://urwid.org/reference/
- **MBASIC Docs**: `docs/` directory
- **UI Architecture**: `src/ui/base.py`
- **Migration Guide**: `docs/dev/URWID_MIGRATION.md`

## Troubleshooting

### "No module named 'urwid'"

Install urwid:

```bash
pip install urwid
```

### "Terminal too small"

urwid requires a minimum terminal size. Resize your terminal window.

### Display issues

If you see garbled text or incorrect layouts:

1. Make sure your terminal supports UTF-8
2. Try resizing the terminal
3. Use a different terminal emulator

## Contributing

To contribute to the urwid UI:

1. Read `docs/dev/URWID_MIGRATION.md`
2. Follow the coding style in `src/ui/curses_ui.py`
3. Test your changes thoroughly
4. Update documentation

## License

Same as MBASIC interpreter - see `LICENSE` file.
