#!/usr/bin/env python3
"""
NiceGUI-based web interface for MBASIC.

Provides a modern web IDE for running BASIC programs with:
- Code editor with syntax highlighting
- Real-time output display
- Interactive INPUT support
- File save/load
- Multi-user sessions
"""

from nicegui import ui, app
from pathlib import Path
import sys
import asyncio
from datetime import datetime

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from iohandler.web_io import WebIOHandler
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from runtime import Runtime
from editing import ProgramManager


class MBasicWebIDE:
    """Main MBASIC Web IDE application."""

    def __init__(self):
        """Initialize the IDE."""
        self.editor = None
        self.output_log = None
        self.status_label = None
        self.running = False
        self.current_file = "untitled.bas"

        # MBASIC components
        self.io_handler = None
        self.runtime = None
        self.interpreter = None
        self.program_manager = None

    def create_ui(self):
        """Create the main UI layout."""
        # Page configuration
        ui.colors(primary='#1976D2', secondary='#26A69A', accent='#9C27B0')

        # Header
        with ui.header().classes('items-center justify-between'):
            ui.label('MBASIC 5.21 Web IDE').classes('text-h5')
            ui.label('').bind_text_from(self, 'current_file')

        # Main content area with splitter
        with ui.splitter(value=50).classes('w-full h-full') as splitter:

            # Left panel: Code editor
            with splitter.before:
                with ui.card().classes('w-full h-full'):
                    ui.label('Program Editor').classes('text-h6 mb-2')

                    # Editor (using textarea for now, will upgrade to Monaco later)
                    self.editor = ui.textarea(
                        label='BASIC Code',
                        placeholder='10 PRINT "HELLO WORLD"\n20 END'
                    ).classes('w-full').props('rows=20 outlined')

                    # Set initial example code
                    self.editor.value = '''10 REM MBASIC Web IDE Example
20 PRINT "Welcome to MBASIC 5.21!"
30 PRINT
40 FOR I = 1 TO 5
50   PRINT "Count: "; I
60 NEXT I
70 PRINT
80 PRINT "Try editing this code and click RUN"
90 END
'''

                    # Toolbar
                    with ui.row().classes('gap-2'):
                        ui.button('Run', on_click=self.run_program, icon='play_arrow').props('color=primary')
                        ui.button('Stop', on_click=self.stop_program, icon='stop').props('color=negative')
                        ui.button('Clear Output', on_click=self.clear_output, icon='clear_all')
                        ui.button('New', on_click=self.new_program, icon='note_add')
                        ui.button('Examples', on_click=self.show_examples, icon='menu_book')

            # Right panel: Output
            with splitter.after:
                with ui.card().classes('w-full h-full'):
                    ui.label('Output').classes('text-h6 mb-2')

                    # Output log
                    self.output_log = ui.log(max_lines=1000).classes('w-full h-96')
                    self.output_log.push('MBASIC 5.21 Web Interpreter')
                    self.output_log.push('Ready')
                    self.output_log.push('')

        # Footer status bar
        with ui.footer():
            self.status_label = ui.label('Ready').classes('text-sm')

    async def run_program(self):
        """Run the BASIC program."""
        if self.running:
            ui.notify('Program already running', type='warning')
            return

        self.running = True
        self.status_label.text = 'Running...'
        self.output_log.push('')
        self.output_log.push('> RUN')

        try:
            code = self.editor.value

            # Parse the program
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()

            # Create custom I/O handler for web
            self.io_handler = WebIOHandler(self.output_log)

            # Create runtime and interpreter
            self.runtime = Runtime(self.io_handler)
            self.interpreter = Interpreter(ast, self.runtime)

            # Run program in background
            await asyncio.to_thread(self.interpreter.run)

            self.output_log.push('')
            self.status_label.text = 'Program completed'
            ui.notify('Program completed', type='positive')

        except SyntaxError as e:
            error_msg = f'Syntax Error: {str(e)}'
            self.output_log.push(error_msg)
            self.status_label.text = 'Syntax error'
            ui.notify(error_msg, type='negative')

        except Exception as e:
            error_msg = f'Error: {str(e)}'
            self.output_log.push(error_msg)
            self.status_label.text = 'Error'
            ui.notify(error_msg, type='negative')

        finally:
            self.running = False

    def stop_program(self):
        """Stop the running program."""
        if not self.running:
            ui.notify('No program running', type='warning')
            return

        # TODO: Implement program interruption
        ui.notify('Stop not yet implemented', type='info')

    def clear_output(self):
        """Clear the output log."""
        self.output_log.clear()
        self.output_log.push('MBASIC 5.21 Web Interpreter')
        self.output_log.push('Ready')
        self.output_log.push('')
        ui.notify('Output cleared')

    def new_program(self):
        """Create a new program."""
        self.editor.value = '10 \n'
        self.current_file = 'untitled.bas'
        ui.notify('New program created')

    async def show_examples(self):
        """Show example programs menu."""
        examples = {
            'Hello World': '''10 PRINT "HELLO WORLD"
20 END
''',
            'Loops': '''10 REM Loop Example
20 FOR I = 1 TO 10
30   PRINT I; " squared is "; I*I
40 NEXT I
50 END
''',
            'Fibonacci': '''10 REM Fibonacci Sequence
20 A = 0
30 B = 1
40 FOR I = 1 TO 10
50   PRINT A;
60   C = A + B
70   A = B
80   B = C
90 NEXT I
100 PRINT
110 END
''',
            'User Input': '''10 REM User Input Example
20 PRINT "What is your name?"
30 INPUT N$
40 PRINT "Hello, "; N$; "!"
50 PRINT "Enter a number:"
60 INPUT X
70 PRINT "Your number squared is "; X*X
80 END
''',
        }

        # Create selection dialog
        with ui.dialog() as dialog, ui.card():
            ui.label('Choose an Example Program').classes('text-h6')

            for name, code in examples.items():
                ui.button(
                    name,
                    on_click=lambda c=code: self.load_example(c, dialog)
                ).props('flat color=primary').classes('w-full')

            ui.button('Cancel', on_click=dialog.close).props('flat')

        dialog.open()

    def load_example(self, code, dialog):
        """Load an example program into the editor."""
        self.editor.value = code
        ui.notify('Example loaded')
        dialog.close()


def create_app():
    """Create and configure the NiceGUI app."""
    ide = MBasicWebIDE()
    ide.create_ui()


# Run the app
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title='MBASIC 5.21 Web IDE',
        port=8080,
        reload=False,
        show=False,  # Don't auto-open browser
    )
