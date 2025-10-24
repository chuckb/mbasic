"""Curses UI backend for MBASIC interpreter.

This module provides a text-based visual UI using Python's curses library.
Curses provides a full-screen terminal interface with multiple windows,
making it suitable for a classic BASIC IDE experience.
"""

from .base import UIBackend
from runtime import Runtime
from interpreter import Interpreter


class CursesBackend(UIBackend):
    """Curses-based text UI backend.

    Provides a full-screen terminal UI with:
    - Split screen: editor on top, output on bottom
    - Status line showing current mode and line number
    - Function key commands (F1=Help, F2=Run, F3=List, F5=Save, F9=Load)
    - Visual line editing with cursor movement
    - Scrollable output window

    Usage:
        from iohandler.console import ConsoleIOHandler
        from editing import ProgramManager
        from ui.curses_ui import CursesBackend

        io = ConsoleIOHandler()
        program = ProgramManager(def_type_map)
        backend = CursesBackend(io, program)
        backend.start()  # Runs curses UI until user exits
    """

    def __init__(self, io_handler, program_manager):
        """Initialize curses backend.

        Args:
            io_handler: IOHandler for I/O operations
            program_manager: ProgramManager instance
        """
        super().__init__(io_handler, program_manager)

        # Runtime and interpreter for program execution
        self.runtime = None
        self.interpreter = None

        # Curses state
        self.stdscr = None
        self.editor_win = None
        self.output_win = None
        self.status_win = None

        # Editor state
        self.current_line = 1
        self.cursor_pos = 0
        self.scroll_offset = 0

    def start(self) -> None:
        """Start the curses UI.

        Initializes curses, creates windows, and runs the main event loop.
        """
        import curses
        try:
            curses.wrapper(self._curses_main)
        except KeyboardInterrupt:
            pass  # Clean exit on Ctrl+C

    def _curses_main(self, stdscr):
        """Main curses loop (called by curses.wrapper).

        Args:
            stdscr: Main curses screen window
        """
        import curses

        self.stdscr = stdscr

        # Initialize colors if available
        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)    # Status line
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Editor
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Output
            curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)     # Errors

        # Create windows
        self._create_windows()

        # Draw initial UI
        self._refresh_all()

        # Main event loop
        while True:
            key = self.stdscr.getch()

            if key == ord('q') or key == ord('Q'):
                # Quit
                break
            elif key == curses.KEY_F2:
                # F2 = Run
                self._run_program()
            elif key == curses.KEY_F3:
                # F3 = List
                self._list_program()
            elif key == curses.KEY_F5:
                # F5 = Save
                self._save_program()
            elif key == curses.KEY_F9:
                # F9 = Load
                self._load_program()
            elif key == curses.KEY_UP:
                self._move_cursor_up()
            elif key == curses.KEY_DOWN:
                self._move_cursor_down()
            elif key == curses.KEY_LEFT:
                self._move_cursor_left()
            elif key == curses.KEY_RIGHT:
                self._move_cursor_right()
            elif key == ord('\n') or key == curses.KEY_ENTER:
                self._handle_enter()
            elif key >= 32 and key < 127:
                # Printable character
                self._insert_char(chr(key))

            self._refresh_all()

    def _create_windows(self):
        """Create curses windows for UI layout."""
        import curses

        height, width = self.stdscr.getmaxyx()

        # Status line at bottom (1 line)
        self.status_win = curses.newwin(1, width, height - 1, 0)

        # Editor window (top 2/3)
        editor_height = (height - 1) * 2 // 3
        self.editor_win = curses.newwin(editor_height, width, 0, 0)

        # Output window (bottom 1/3, minus status line)
        output_height = (height - 1) - editor_height
        self.output_win = curses.newwin(output_height, width, editor_height, 0)

        # Enable scrolling for output window
        self.output_win.scrollok(True)

    def _refresh_all(self):
        """Refresh all windows."""
        self._draw_status()
        self._draw_editor()
        self._draw_output()

        self.stdscr.refresh()
        self.status_win.refresh()
        self.editor_win.refresh()
        self.output_win.refresh()

    def _draw_status(self):
        """Draw status line."""
        import curses

        self.status_win.clear()

        if curses.has_colors():
            self.status_win.bkgd(' ', curses.color_pair(1))

        status_text = f" MBASIC 5.21 | Line {self.current_line} | F2=Run F3=List F5=Save F9=Load Q=Quit"
        self.status_win.addstr(0, 0, status_text)

    def _draw_editor(self):
        """Draw editor window showing program lines."""
        import curses

        self.editor_win.clear()

        if curses.has_colors():
            self.editor_win.bkgd(' ', curses.color_pair(2))

        # Get visible program lines
        lines = sorted(self.program.lines.items())
        height, width = self.editor_win.getmaxyx()

        # Draw lines
        for i, (line_num, line_text) in enumerate(lines[self.scroll_offset:]):
            if i >= height:
                break
            self.editor_win.addstr(i, 0, f"{line_text[:width-1]}")

        # Draw cursor if in editor
        # TODO: Implement cursor positioning

    def _draw_output(self):
        """Draw output window."""
        import curses

        if curses.has_colors():
            self.output_win.bkgd(' ', curses.color_pair(3))

        # Output is drawn by IOHandler during program execution
        # This just sets up the window appearance

    def _run_program(self):
        """Run the current program."""
        try:
            # Get program AST
            program_ast = self.program.get_program_ast()

            # Create runtime and interpreter
            self.runtime = Runtime(self.program.line_asts, self.program.lines)
            self.interpreter = Interpreter(self.runtime, self.io)

            # Clear output window
            self.output_win.clear()

            # Run the program
            # TODO: Redirect output to curses output window
            self.interpreter.run()

            self._add_output("Program finished\n")

        except Exception as e:
            self._add_error(f"Runtime error: {e}\n")

    def _list_program(self):
        """List program to output window."""
        self.output_win.clear()
        lines = self.program.get_lines()
        for line_num, line_text in lines:
            self._add_output(f"{line_text}\n")

    def _save_program(self):
        """Save program to file."""
        # TODO: Implement file dialog or prompt
        self._add_output("Save not yet implemented\n")

    def _load_program(self):
        """Load program from file."""
        # TODO: Implement file dialog or prompt
        self._add_output("Load not yet implemented\n")

    def _move_cursor_up(self):
        """Move cursor up one line."""
        if self.current_line > 1:
            self.current_line -= 1

    def _move_cursor_down(self):
        """Move cursor down one line."""
        self.current_line += 1

    def _move_cursor_left(self):
        """Move cursor left one character."""
        if self.cursor_pos > 0:
            self.cursor_pos -= 1

    def _move_cursor_right(self):
        """Move cursor right one character."""
        self.cursor_pos += 1

    def _handle_enter(self):
        """Handle Enter key - parse and add line."""
        # TODO: Get current line text from editor
        # TODO: Parse and add to program
        pass

    def _insert_char(self, char):
        """Insert character at cursor position."""
        # TODO: Implement character insertion
        pass

    def _add_output(self, text):
        """Add text to output window."""
        self.output_win.addstr(text)

    def _add_error(self, text):
        """Add error text to output window."""
        import curses
        if curses.has_colors():
            self.output_win.addstr(text, curses.color_pair(4))
        else:
            self.output_win.addstr(text)

    # UIBackend interface methods

    def cmd_run(self) -> None:
        """Execute RUN command - run the program."""
        self._run_program()

    def cmd_list(self, args: str = "") -> None:
        """Execute LIST command - list program lines."""
        self._list_program()

    def cmd_new(self) -> None:
        """Execute NEW command - clear program."""
        self.program.clear()
        self._add_output("Program cleared\n")

    def cmd_save(self, filename: str) -> None:
        """Execute SAVE command - save to file."""
        try:
            self.program.save_to_file(filename)
            self._add_output(f"Saved to {filename}\n")
        except Exception as e:
            self._add_error(f"Save error: {e}\n")

    def cmd_load(self, filename: str) -> None:
        """Execute LOAD command - load from file."""
        try:
            success, errors = self.program.load_from_file(filename)
            if errors:
                for line_num, error in errors:
                    self._add_error(error + "\n")
            if success:
                self._add_output(f"Loaded from {filename}\n")
                self._draw_editor()  # Refresh editor display
        except Exception as e:
            self._add_error(f"Load error: {e}\n")

    def cmd_delete(self, args: str) -> None:
        """Execute DELETE command - delete line range."""
        # TODO: Implement
        pass

    def cmd_renum(self, args: str) -> None:
        """Execute RENUM command - renumber lines."""
        # TODO: Implement
        pass

    def cmd_cont(self) -> None:
        """Execute CONT command - continue after STOP."""
        # TODO: Implement
        pass
