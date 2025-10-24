# Visual UI Refactoring Plan

## Goal

Refactor mbasic.py to enable embedding the interpreter in a visual UI while keeping the command-line tool functional. The architecture should use dynamic imports (importlib) and allow customizable I/O handlers.

## Current Architecture Analysis

### Current Structure

```
mbasic.py (85 lines)
├── Imports: lexer, parser, runtime, interpreter, interactive
├── run_file() - Loads and executes a BASIC file
├── main() - Entry point, starts InteractiveMode
└── Uses InteractiveMode.start() for REPL

src/interactive.py (1462 lines)
├── InteractiveMode class
├── I/O: Uses input() and print() directly
├── Commands: RUN, LIST, SAVE, LOAD, NEW, DELETE, RENUM, EDIT, AUTO, etc.
└── Immediate mode execution

src/interpreter.py
├── Interpreter class
├── I/O: Uses print() directly for PRINT statements
└── Uses input() for INPUT statements (via basic_builtins.py)

src/basic_builtins.py
└── I/O: input() for INPUT$, INKEY$, LINE INPUT
```

### Current I/O Points

**Output:**
- `print()` used in ~50+ places across interpreter.py, interactive.py
- PRINT statement execution
- Error messages
- DEBUG output
- Command feedback (LIST, SAVE, etc.)

**Input:**
- `input()` used for:
  - Interactive REPL prompt
  - BASIC INPUT statement
  - INPUT$ function
  - LINE INPUT statement
  - INKEY$ (non-blocking keyboard)

### Current Editing Functions (in InteractiveMode)

- `cmd_list()` - List program lines
- `cmd_save()` - Save to file
- `cmd_load()` - Load from file
- `cmd_new()` - Clear program
- `cmd_delete()` - Delete line range
- `cmd_renum()` - Renumber lines
- `cmd_edit()` - Line editor
- `cmd_auto()` - Auto line numbering
- `cmd_merge()` - Merge files
- `cmd_chain()` - Chain to another program

## Proposed Architecture

### Design Principles

1. **Separation of Concerns**
   - Core interpreter logic (execution) - stays in src/
   - I/O abstraction layer - new
   - UI-specific code - separate modules
   - Command/editing layer - refactored

2. **Dynamic Loading**
   - Use importlib to load UI backends dynamically
   - CLI and GUI both implement same interface
   - Selectable via command line or config

3. **I/O Abstraction**
   - All I/O goes through an IOHandler interface
   - Default: ConsoleIOHandler (current behavior)
   - Visual: GUIIOHandler (for visual UI)

4. **Editing Abstraction**
   - Core editing operations (add/delete/renumber lines)
   - UI-specific editors (CLI line editor vs GUI visual editor)

### New Directory Structure

```
mbasic/
├── mbasic.py                   # Main entry point (refactored)
├── src/
│   ├── core/                   # NEW: Core interpreter (no I/O)
│   │   ├── __init__.py
│   │   ├── engine.py           # Refactored interpreter (I/O abstracted)
│   │   ├── lexer.py            # Move from src/
│   │   ├── parser.py           # Move from src/
│   │   ├── runtime.py          # Move from src/
│   │   ├── ast_nodes.py        # Move from src/
│   │   ├── tokens.py           # Move from src/
│   │   └── basic_builtins.py   # Move and refactor
│   │
│   ├── io/                     # NEW: I/O abstraction
│   │   ├── __init__.py
│   │   ├── base.py             # IOHandler interface
│   │   ├── console.py          # ConsoleIOHandler (default)
│   │   └── gui.py              # GUIIOHandler (visual UI)
│   │
│   ├── editing/                # NEW: Editing abstraction
│   │   ├── __init__.py
│   │   ├── base.py             # ProgramEditor interface
│   │   ├── manager.py          # ProgramManager (line storage/AST)
│   │   └── commands.py         # Core editing commands
│   │
│   └── ui/                     # NEW: UI implementations
│       ├── __init__.py
│       ├── base.py             # UIBackend interface
│       ├── cli.py              # CLIBackend (current interactive.py)
│       └── visual.py           # VisualBackend (for GUI)
│
├── backends/                   # NEW: Pluggable UI backends
│   ├── __init__.py
│   ├── cli.py                  # CLI backend module
│   └── visual.py               # Visual UI backend module
│
└── examples/                   # NEW: Usage examples
    ├── embed_cli.py            # Example: CLI embedding
    ├── embed_gui.py            # Example: GUI embedding
    └── custom_io.py            # Example: Custom I/O handler
```

### Core Components

#### 1. IOHandler Interface (src/io/base.py)

```python
class IOHandler:
    """Abstract interface for I/O operations"""

    def output(self, text: str, end: str = '\n') -> None:
        """Output text (like print())"""
        raise NotImplementedError

    def input(self, prompt: str = '') -> str:
        """Input text (like input())"""
        raise NotImplementedError

    def input_line(self, prompt: str = '') -> str:
        """Input a full line (LINE INPUT)"""
        raise NotImplementedError

    def input_char(self, blocking: bool = True) -> str:
        """Input single character (INKEY$, INPUT$)"""
        raise NotImplementedError

    def clear_screen(self) -> None:
        """Clear screen (CLS)"""
        raise NotImplementedError

    def error(self, message: str) -> None:
        """Output error message"""
        raise NotImplementedError

    def debug(self, message: str) -> None:
        """Output debug message (if DEBUG enabled)"""
        raise NotImplementedError
```

#### 2. ProgramManager (src/editing/manager.py)

```python
class ProgramManager:
    """Manages program lines and ASTs (extracted from InteractiveMode)"""

    def __init__(self, def_type_map: dict):
        self.lines: Dict[int, str] = {}        # line_number -> text
        self.line_asts: Dict[int, LineNode] = {}  # line_number -> AST
        self.def_type_map = def_type_map
        self.current_file: Optional[str] = None

    def add_line(self, line_number: int, line_text: str) -> bool:
        """Add or replace a line, returns True if parse succeeded"""
        ...

    def delete_line(self, line_number: int) -> bool:
        """Delete a line"""
        ...

    def delete_range(self, start: int, end: int) -> None:
        """Delete a range of lines"""
        ...

    def get_line(self, line_number: int) -> Optional[str]:
        """Get line text"""
        ...

    def get_lines(self, start: int = None, end: int = None) -> List[Tuple[int, str]]:
        """Get lines in range, sorted"""
        ...

    def renumber(self, new_start: int, old_start: int, increment: int) -> None:
        """Renumber lines"""
        ...

    def clear(self) -> None:
        """Clear all lines"""
        ...

    def save_to_file(self, filename: str) -> None:
        """Save program to file"""
        ...

    def load_from_file(self, filename: str) -> bool:
        """Load program from file, returns True on success"""
        ...

    def get_ast(self) -> ProgramNode:
        """Build ProgramNode from current lines"""
        ...
```

#### 3. InterpreterEngine (src/core/engine.py)

```python
class InterpreterEngine:
    """Core interpreter engine with abstracted I/O"""

    def __init__(self, io_handler: IOHandler):
        self.io = io_handler
        self.runtime = None

    def run_program(self, program: ProgramNode) -> None:
        """Execute a BASIC program"""
        ...

    def execute_line(self, line: LineNode) -> Any:
        """Execute a single line (immediate mode)"""
        ...

    def break_execution(self) -> None:
        """Handle Ctrl+C / BREAK"""
        ...

    def continue_execution(self) -> None:
        """Continue after STOP or Ctrl+C"""
        ...
```

#### 4. UIBackend Interface (src/ui/base.py)

```python
class UIBackend:
    """Abstract interface for UI backends"""

    def __init__(self, io_handler: IOHandler, program_manager: ProgramManager):
        self.io = io_handler
        self.program = program_manager
        self.engine = InterpreterEngine(io_handler)

    def start(self) -> None:
        """Start the UI"""
        raise NotImplementedError

    def cmd_run(self) -> None:
        """Execute RUN command"""
        ...

    def cmd_list(self, args: str) -> None:
        """Execute LIST command"""
        ...

    # Other commands...

    def execute_immediate(self, statement: str) -> None:
        """Execute immediate mode statement"""
        ...
```

### Refactoring Steps

#### Phase 1: I/O Abstraction

**Goal**: Extract all I/O into IOHandler interface

1. **Create src/io/ directory structure**
   - base.py: IOHandler interface
   - console.py: ConsoleIOHandler (wraps print/input)
   - gui.py: GUIIOHandler stub

2. **Refactor interpreter.py → src/core/engine.py**
   - Pass IOHandler to constructor
   - Replace `print()` with `self.io.output()`
   - Replace error messages with `self.io.error()`
   - Replace DEBUG print with `self.io.debug()`

3. **Refactor basic_builtins.py**
   - Pass IOHandler to built-in functions
   - Replace `input()` with `io_handler.input()`
   - Replace `print()` with `io_handler.output()`

4. **Test**: Ensure CLI still works with ConsoleIOHandler

**Time Estimate**: 2-3 hours

#### Phase 2: Program Management

**Goal**: Extract line/AST management from InteractiveMode

1. **Create src/editing/ directory**
   - manager.py: ProgramManager class
   - commands.py: Core editing commands

2. **Extract from interactive.py**:
   - Line storage (self.lines, self.line_asts)
   - Parsing logic (parse_single_line)
   - SAVE/LOAD/NEW/DELETE/RENUM logic
   - Move to ProgramManager

3. **Test**: Ensure editing commands work

**Time Estimate**: 2-3 hours

#### Phase 3: UI Abstraction

**Goal**: Make InteractiveMode a UI backend

1. **Create src/ui/ directory**
   - base.py: UIBackend interface
   - cli.py: Refactored InteractiveMode

2. **Refactor InteractiveMode → CLIBackend**
   - Use ProgramManager instead of direct line storage
   - Use InterpreterEngine instead of direct Interpreter
   - Keep CLI-specific: REPL loop, line editor

3. **Create visual.py stub**
   - Minimal VisualBackend implementation
   - Document interface for GUI integration

**Time Estimate**: 3-4 hours

#### Phase 4: Dynamic Loading

**Goal**: Use importlib to load backends dynamically

1. **Refactor mbasic.py**
   - Add --backend argument (cli/visual)
   - Use importlib.import_module() to load backend
   - Pass IOHandler and ProgramManager to backend

2. **Create backend loader**:
   ```python
   def load_backend(backend_name: str, io_handler: IOHandler,
                    program_manager: ProgramManager) -> UIBackend:
       module = importlib.import_module(f'backends.{backend_name}')
       return module.create_backend(io_handler, program_manager)
   ```

3. **Test**: Ensure both CLI and stub visual backend work

**Time Estimate**: 1-2 hours

#### Phase 5: Visual UI Preparation (DEFERRED)

**Goal**: Stop before implementing visual UI, evaluate mobile-friendly options

**Status**: This phase is intentionally deferred until after Phases 1-4 are complete.

**Rationale**: The architecture created in Phases 1-4 (IOHandler, UIBackend) is framework-agnostic. Before committing to a specific visual framework, we'll evaluate cross-platform options for **iOS, Android, and desktop**.

**Potential Mobile Frameworks to Evaluate**:
1. **Kivy** - Python native, runs on iOS/Android/Desktop, touch-friendly
2. **BeeWare (Toga)** - Native widgets on each platform, Python-based
3. **PyQt/PySide** - QML for mobile, mature framework
4. **React Native + Python bridge** - Web tech, native performance
5. **Flutter + Python bridge** - High-performance, beautiful UIs
6. **Web-based (PWA)** - HTML5/JavaScript calling Python backend via REST/WebSocket

**Evaluation Criteria**:
- iOS and Android support (primary requirement)
- Touch input and gesture support
- Native feel vs web view performance
- Deployment complexity (app store requirements)
- Screen size adaptation (phone/tablet)
- Text editor widget quality
- Development velocity
- Python integration quality

**Phase 5 Implementation**:
After Phase 4, we'll create a separate document (MOBILE_UI_EVALUATION.md) analyzing each framework with:
- Proof-of-concept implementations
- Pros/cons for MBASIC use case
- Recommended approach
- Implementation plan for chosen framework

**Time Estimate**: TBD (depends on framework choice and evaluation time)

### Migration Strategy

**Backward Compatibility:**
- Keep `mbasic.py` working exactly as before (default CLI)
- `python3 mbasic.py` → CLI mode (no changes for users)
- `python3 mbasic.py --backend visual` → Visual mode

**Gradual Migration:**
1. Phase 1-3: Refactor internal structure (no API changes)
2. Phase 4: Add dynamic loading (optional --backend flag)
3. **STOP**: Evaluate mobile UI frameworks before Phase 5
4. Phase 5: Implement chosen mobile/visual backend (deferred)

**Testing:**
- After each phase, run existing test suite
- Ensure `python3 mbasic.py` still works
- Ensure `python3 mbasic.py program.bas` still works

## API for Visual UI Developers

### Example: Custom Visual UI

```python
from src.io.base import IOHandler
from src.editing.manager import ProgramManager
from src.ui.base import UIBackend
from src.core.engine import InterpreterEngine
from parser import TypeInfo

class MyGUIIOHandler(IOHandler):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def output(self, text: str, end: str = '\n') -> None:
        self.text_widget.insert('end', text + end)

    def input(self, prompt: str = '') -> str:
        # Show dialog or input field
        return self.show_input_dialog(prompt)

    # ... implement other methods

class MyVisualUI(UIBackend):
    def __init__(self, io_handler, program_manager):
        super().__init__(io_handler, program_manager)
        # Your GUI setup here

    def start(self):
        # Start your GUI main loop
        pass

# Usage:
io = MyGUIIOHandler(my_text_widget)
manager = ProgramManager(default_def_type_map())
ui = MyVisualUI(io, manager)
ui.start()
```

### Example: Embed in Existing App

```python
import importlib

def create_mbasic_interpreter(output_callback, input_callback):
    """Create embedded MBASIC interpreter"""

    # Custom I/O handler
    class CallbackIOHandler(IOHandler):
        def output(self, text: str, end: str = '\n'):
            output_callback(text + end)

        def input(self, prompt: str = ''):
            return input_callback(prompt)

        # ... other methods

    # Load backend dynamically
    backend_module = importlib.import_module('src.ui.cli')

    io = CallbackIOHandler()
    manager = ProgramManager(default_def_type_map())
    backend = backend_module.CLIBackend(io, manager)

    return backend
```

## Benefits of This Architecture

### For CLI Users
- **No Changes**: Existing workflow unchanged
- **Performance**: No overhead from abstraction (Python duck typing)
- **Backward Compatible**: All existing scripts work

### For Visual UI Developers
- **Clean API**: IOHandler and UIBackend interfaces
- **Flexible I/O**: Custom handlers for any UI framework
- **Embeddable**: Drop interpreter into existing apps
- **Dynamic Loading**: No need to modify mbasic.py

### For Maintainers
- **Separation of Concerns**: Core logic vs UI vs I/O
- **Testable**: Mock IOHandler for testing
- **Extensible**: New backends without touching core
- **Clear Boundaries**: Well-defined interfaces

## Implementation Checklist

### Phase 1: I/O Abstraction
- [ ] Create src/io/ directory structure
- [ ] Implement IOHandler interface (base.py)
- [ ] Implement ConsoleIOHandler (console.py)
- [ ] Refactor interpreter.py to use IOHandler
- [ ] Refactor basic_builtins.py to use IOHandler
- [ ] Test: CLI functionality unchanged

### Phase 2: Program Management
- [ ] Create src/editing/ directory
- [ ] Implement ProgramManager class
- [ ] Extract line storage from InteractiveMode
- [ ] Extract parsing from InteractiveMode
- [ ] Extract SAVE/LOAD from InteractiveMode
- [ ] Test: All editing commands work

### Phase 3: UI Abstraction
- [ ] Create src/ui/ directory
- [ ] Implement UIBackend interface
- [ ] Refactor InteractiveMode → CLIBackend
- [ ] Update InteractiveMode to use ProgramManager
- [ ] Update InteractiveMode to use InterpreterEngine
- [ ] Test: Interactive mode works

### Phase 4: Dynamic Loading
- [ ] Add importlib loading to mbasic.py
- [ ] Add --backend command line argument
- [ ] Create backend loader function
- [ ] Create backends/ directory
- [ ] Test: CLI backend loads dynamically
- [ ] Document: How to create custom backends

### Phase 5: Mobile/Visual UI (DEFERRED)
**STOP HERE - Complete Phases 1-4 first, then evaluate mobile frameworks**
- [ ] Create MOBILE_UI_EVALUATION.md
- [ ] Evaluate Kivy, BeeWare, PyQt, React Native, Flutter, PWA
- [ ] Build proof-of-concept for top 2-3 options
- [ ] Choose framework based on iOS/Android support
- [ ] Design mobile-specific UI (touch, gestures, screen sizes)
- [ ] Implement chosen framework
- [ ] Document: Mobile UI integration guide

## Timeline Estimate

**Phases 1-4 (Core Refactoring)**: 8-12 hours
- Phase 1: 2-3 hours (I/O abstraction)
- Phase 2: 2-3 hours (Program management)
- Phase 3: 3-4 hours (UI abstraction)
- Phase 4: 1-2 hours (Dynamic loading)

**Phase 5 (Mobile UI)**: TBD - Deferred pending framework evaluation
- Framework evaluation: 2-4 hours
- Proof-of-concepts: 4-8 hours
- Implementation: 8-20 hours (varies by framework)
- Documentation: 2-4 hours

## Risks and Mitigations

### Risk: Breaking existing functionality
**Mitigation**: Test after each phase, maintain backward compatibility

### Risk: Performance overhead
**Mitigation**: Python duck typing is fast, minimal overhead

### Risk: Complex refactoring
**Mitigation**: Incremental approach, keep old code until new works

### Risk: Different UI paradigms (CLI vs GUI)
**Mitigation**: Clean abstractions, document differences

## Future Extensions

Once the refactoring is complete, these become possible:

1. **Web UI**: Create a web-based backend using Flask/Django
2. **Jupyter**: Jupyter notebook integration
3. **IDE Plugin**: VS Code or other IDE plugins
4. **Headless**: Run BASIC programs as services
5. **Testing**: Mock I/O for comprehensive testing
6. **Network**: Remote BASIC execution (telnet-like)

## Mobile Platform Considerations

### iOS and Android Requirements

The architecture must support:
- **Touch Input**: No mouse, touch gestures (tap, swipe, pinch)
- **Screen Sizes**: Phone (3-7") to tablet (8-13")
- **Virtual Keyboard**: Screen space management when keyboard is visible
- **App Store Requirements**: Code signing, sandboxing, review process
- **Native vs Web Feel**: Balance between performance and development speed

### Framework Requirements for MBASIC

1. **Text Editing Widget**
   - Line numbers display
   - Syntax highlighting (nice to have)
   - Touch-friendly scrolling
   - Selection and cursor control

2. **Output Display**
   - Monospace font support
   - Scrollable text output
   - Clear screen capability
   - ANSI/cursor positioning (for CLS, LOCATE)

3. **Input Handling**
   - Dialog for INPUT statement
   - Keyboard management
   - INKEY$ simulation (button or gesture)

4. **Program Management**
   - File picker for LOAD/SAVE
   - Visual line editor
   - RUN/STOP buttons
   - Program listing view

### Recommended Evaluation Order

After Phase 4 completion:

1. **Kivy** (Try first)
   - Pro: Pure Python, iOS/Android/Desktop proven
   - Pro: Good documentation, active community
   - Con: Custom widget look (not native)

2. **BeeWare** (Try second)
   - Pro: Native widgets on each platform
   - Pro: Python-native philosophy
   - Con: Younger project, less mature

3. **Web-based (PWA)** (Fallback)
   - Pro: Easiest cross-platform
   - Pro: Familiar web technologies
   - Con: Need Python backend (API approach)

## Conclusion

This refactoring plan provides a clear path to making MBASIC embeddable in visual UIs while maintaining CLI functionality. The architecture uses standard Python patterns (importlib, abstract interfaces) and follows best practices for separation of concerns.

**Key Decision**: The plan deliberately stops after Phase 4 to evaluate mobile frameworks properly. The IOHandler and UIBackend architecture is framework-agnostic and will work with any UI technology chosen for iOS/Android support.

The incremental approach ensures each phase is testable and doesn't break existing functionality. Phases 1-4 create a flexible, embeddable BASIC interpreter core that can be wrapped in any UI framework - command-line, desktop GUI, mobile app, or web interface.
