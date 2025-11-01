# Web UI Text Highlighting - Visual Markers for Find, Breakpoints, and Step

## Issue

The web UI currently uses plain `ui.textarea()` which doesn't support rich text highlighting. We need visual highlighting like TK UI for:

1. **Find results** - Yellow highlight on found text (remains visible when dialog closes)
2. **Breakpoints** - Red marker/highlight on lines with breakpoints
3. **Current statement during step** - Green/blue highlight showing which line is executing

**Current problems:**
- ✅ ~~Find scrolls to text but no highlight visible while dialog open~~ (FIXED: now scrolls properly)
- ✅ ~~When dialog closes, scrolls back to beginning, then jumps back (bad UX)~~ (FIXED: scroll stays stable)
- ❌ No visible highlight on found text (requires CodeMirror - can't fix with plain textarea)
- ❌ Selection highlight disappears when you type (would replace found text)
- ❌ Breakpoints show in output log but no visual marker on the line
- ❌ Step/statement highlighting not implemented

## TK UI Implementation (Reference)

From `src/ui/tk_ui.py`:

**Find highlight (line 1836):**
```python
self.editor_text.text.tag_add("find_highlight", pos, end_pos)
```

**Current statement highlight (line 2841):**
```python
self.editor_text.text.tag_add('current_statement', start_idx, end_idx)
```

**Tag configuration:**
TK uses `tag_configure()` to set background colors for each tag type:
- `find_highlight` - yellow background
- `current_statement` - green/blue background for step debugging
- `breakpoint` - red background or marker

**Key difference:** TK Text widget supports multiple named tags with different styles that can overlap and persist independently of selection.

## Problem with Plain Textarea

HTML `<textarea>` elements:
- Only support plain text
- Only have ONE selection range (which users can modify by typing)
- No support for multiple styled text ranges
- No support for persistent background highlights
- No way to add visual markers

**Using selection for highlighting has problems:**
1. Highlight disappears when user clicks elsewhere
2. Typing replaces the highlighted text
3. Can't have multiple highlights (find + breakpoint + current statement)
4. Selection scrolls back when dialog closes

## Solution Options

### Option A: Upgrade to Code Editor Component

Replace `ui.textarea()` with a proper code editor:

**CodeMirror 6** (Modern, well-supported):
- Supports text decorations/markers
- Line gutters for breakpoint markers
- Multiple selection ranges with custom styling
- Excellent API for programmatic control
- Syntax highlighting (bonus!)

**Monaco Editor** (VS Code's editor):
- Very feature-rich
- Heavier weight
- Excellent for complex editing

**Ace Editor**:
- Lightweight alternative
- Good highlighting support

**Implementation for CodeMirror 6:**
```python
from nicegui import ui

# Use ui.html() or ui.add_body_html() to embed CodeMirror
editor_container = ui.element('div').classes('w-full h-96')

# Load CodeMirror via CDN and configure
ui.add_head_html('''
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/codemirror@6/dist/index.css">
<script src="https://cdn.jsdelivr.net/npm/codemirror@6"></script>
''')

# Create editor with Python/BASIC-like syntax
ui.run_javascript('''
import {EditorView, Decoration} from "@codemirror/view"
import {StateEffect, StateField} from "@codemirror/state"

// Define decoration types
const findMark = Decoration.mark({class: "cm-find-highlight"})
const breakpointMark = Decoration.mark({class: "cm-breakpoint"})
const currentLineMark = Decoration.line({class: "cm-current-line"})

// Add to editor state...
''')
```

**CSS for highlights:**
```css
.cm-find-highlight { background-color: yellow; }
.cm-breakpoint { background-color: #ffcccc; }
.cm-current-line { background-color: #ccffcc; }
```

### Option B: ContentEditable Div with Spans

Use a `contenteditable` div instead of textarea:

**Pros:**
- Can insert `<span>` elements with background colors
- More control over styling
- No external dependencies

**Cons:**
- Much more complex to manage
- Need to handle all keyboard input manually
- Cursor position tracking is hard
- Copy/paste behavior quirky
- **Not recommended** - too much work for little gain

### Option C: Hybrid Approach (Overlay Highlights)

Keep textarea but overlay highlights using absolutely positioned divs:

**Concept:**
1. Keep `ui.textarea()` for editing
2. Create an overlay div with same dimensions
3. Calculate pixel positions for highlights
4. Draw colored divs at those positions
5. Make overlay `pointer-events: none` so clicks pass through

**Pros:**
- Keep existing textarea
- Don't need to rewrite editing logic

**Cons:**
- Very complex position calculations
- Breaks with font size changes, scrolling
- Fragile and hard to maintain
- **Not recommended**

### Option D: Dual-Pane Approach

Show highlights in a separate read-only pane:

**Not suitable** - defeats the purpose of in-place highlighting

## Recommended Solution

**Use CodeMirror 6** (Option A)

**Why:**
1. Designed for code editing with syntax highlighting
2. Excellent decoration/marker API
3. Well-maintained and modern
4. Can add line numbers, breakpoint gutters
5. Better UX than plain textarea anyway
6. Future-proof for syntax highlighting BASIC code

**Migration path:**
1. Create new `CodeMirrorEditor` component wrapper
2. Implement basic text editing
3. Add find highlighting with decorations
4. Add breakpoint markers in gutter
5. Add current statement highlighting
6. Test all editing operations still work
7. Swap out `ui.textarea()` for new component

## Implementation Tasks

### Part 1: CodeMirror Integration (REQUIRED)

1. **Add CodeMirror to Web UI**
   - Load CodeMirror 6 via CDN or npm
   - Create editor instance in NiceGUI
   - Wire up basic text editing

2. **Implement text operations**
   - Get/set editor content
   - Handle user edits
   - Preserve cursor position
   - Handle copy/paste

3. **Event handlers**
   - On change callback to update backend
   - Keyboard shortcuts
   - Focus management

### Part 2: Find Highlighting

1. **Add find decoration**
   - Create yellow highlight decoration type
   - Apply to found text ranges
   - Persist across dialog open/close
   - Clear when new search starts

2. **Scroll to highlight**
   - Use CodeMirror's scroll API
   - Center found text in viewport
   - Don't reset scroll when dialog closes

### Part 3: Breakpoint Markers

1. **Add gutter for breakpoints**
   - Show red circle/dot for breakpoint lines
   - Click gutter to toggle breakpoint
   - Update when breakpoints added/removed

2. **Line background for breakpoints**
   - Optional: light red background on breakpoint lines
   - Or just gutter marker

### Part 4: Current Statement Highlighting

1. **Step debugging highlight**
   - Green/blue background for current executing line
   - Update during step/next/continue
   - Clear when program finishes

2. **Coordinate with debugger**
   - Callback from interpreter on statement change
   - Update highlight in real-time

### Part 5: Testing

1. Find text → should highlight yellow
2. Close find dialog → highlight stays, scroll stays
3. Toggle breakpoint → red marker appears
4. Step through code → current line highlights green
5. Multiple features at once → find + breakpoint + current line all visible

## Priority

**HIGH** - This significantly impacts usability

Current workaround (text selection) is:
- Confusing to users
- Doesn't persist
- Conflicts with editing
- Missing for breakpoints entirely

## Timeline

Estimate: **1-2 days** for full implementation with CodeMirror

## Related Code

- `src/ui/web/nicegui_backend.py:1096` - Current editor creation
- `src/ui/web/nicegui_backend.py:687-723` - Find highlighting (broken)
- `src/ui/web/nicegui_backend.py:1381-1412` - Breakpoint display (broken)
- `src/ui/tk_ui.py:1836` - TK find highlighting (reference)
- `src/ui/tk_ui.py:2841` - TK statement highlighting (reference)

## Date Created

2025-11-01
