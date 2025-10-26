# MBASIC Web UI

Modern web-based IDE for MBASIC using NiceGUI.

## Quick Start

```bash
cd src/ui/web
python3 web_ui.py
```

Open browser to: `http://localhost:8080`

## Features

- ✅ Code editor with example programs
- ✅ Real-time output display
- ✅ Interactive INPUT support via dialogs
- ✅ Error handling and display
- ✅ Multi-pane layout

## Requirements

```bash
pip install nicegui
```

## Documentation

See `/docs/dev/WEB_UI_IMPLEMENTATION.md` for full details.

## Architecture

- **Framework**: NiceGUI (FastAPI + Vue/Quasar)
- **I/O Handler**: `src/iohandler/web_io.py`
- **Execution**: Async background thread
- **Port**: 8080 (configurable)

## Next Steps

- File save/load
- Monaco/CodeMirror editor
- Syntax highlighting
- Debugger integration
