# MBASIC Curses UI Keyboard Shortcuts

> **Note:** This document is specific to the Curses UI. Different UIs have different keyboard shortcuts:
> - **Curses UI:** See this document
> - **Tk UI:** See [TK_UI_QUICK_START.md](TK_UI_QUICK_START.md)
> - **Web UI:** See `docs/help/ui/web/` for Web-specific shortcuts
> - **CLI:** Command-based interface (no keyboard shortcuts)

> **Important:** In Curses UI, `Ctrl+H` opens Help, while in Tk UI, `Ctrl+H` opens Find and Replace. See [UI_FEATURE_COMPARISON.md](UI_FEATURE_COMPARISON.md) for details.

## Global Commands

| Key | Action |
|-----|--------|
| `Ctrl+Q` | Quit |
| `Ctrl+C` | Quit (alternative) |
| `Ctrl+U` | Activate menu bar (arrows navigate, Enter selects) |
| `^F` | This help |
| `Ctrl+P` | Settings |
| `Ctrl+W` | Toggle variables watch window |
| `Menu only` | Toggle execution stack window (no keyboard shortcut in Curses) |

## Program Management

| Key | Action |
|-----|--------|
| `Ctrl+R` | Run program |
| `Ctrl+N` | New program |
| `Ctrl+O` | Open/Load program |
| `Ctrl+V` | Save program |
| `Shift+Ctrl+V` | Save As |
| `Shift+Ctrl+O` | Recent files |

## Editing

| Key | Action |
|-----|--------|
| `Ctrl+B` | Toggle breakpoint on current line |
| `Ctrl+D` | Delete current line |
| `Ctrl+J` | Insert line |
| `Ctrl+E` | Renumber all lines (RENUM) |

## Debugger (when program running)

| Key | Action |
|-----|--------|
| `Ctrl+G` | Continue execution (Go) |
| `Ctrl+K` | Step Line - execute all statements on current line |
| `Ctrl+T` | Step Statement - execute one statement at a time |
| `Ctrl+X` | Stop execution (eXit) |
| `Ctrl+W` | Show/hide variables window |
| `Menu only` | Show/hide execution stack window (Tk UI: Ctrl+K) |

## Variables Window (when visible)

| Key | Action |
|-----|--------|
| `s` | Cycle sort mode (Name → Accessed → Written → Read → Type → Value) |
| `d` | Toggle sort direction (ascending ↑ / descending ↓) |

## Navigation

| Key | Action |
|-----|--------|
| `Tab` | Switch between editor and output |
| `ESC` | Cancel dialogs and input prompts |

