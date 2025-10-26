# Auto-Numbering and Line Insertion for Visual UIs

## Date: 2025-10-26

## Problem Statement

In CLI/Curses mode, users enter lines one at a time with explicit line numbers:
```
10 PRINT "HELLO"
20 PRINT "WORLD"
```

To insert between them, they type a line with an intermediate number:
```
15 PRINT "MIDDLE"
```

In visual editors (Tk/Web), users have a continuous text editor where they can:
- Type anywhere in the editor
- Edit existing lines
- Insert new lines

**The challenge**: How do users efficiently insert multiple lines between two existing lines, especially when there's limited or no numeric space between them?

**Example scenario**:
```
10 PRINT "START"
20 PRINT "END"
```

User wants to insert 10 lines between 10 and 20. How do they:
1. Open space for the new lines?
2. Get appropriate line numbers assigned?
3. Know how much space to allocate when they might not know how many lines they'll need?

## Current Workflow

### Existing Capabilities

**Tk UI**:
- Text editor with syntax checking
- Ctrl+E: Renumber dialog (start, increment)
- Automatic sorting on save
- Manual line number entry

**Web UI**:
- Textarea editor with line numbers column
- Sort button: Sorts lines by line number
- Renumber button: Renumber dialog (start, increment)
- Manual line number entry

**Curses UI**:
- Line-by-line editor (more like CLI)
- Ctrl+E: RENUM command
- Manual line number entry

### Current Insertion Workflow

**Option 1: Manual + Renumber**
1. User manually types intermediate line numbers (15, 16, 17...)
2. If no space, user clicks Renumber first
3. Example: Renumber with start=10, increment=10 → creates 10, 20, 30, 40...
4. Now there's space for 9 lines between each

**Option 2: Manual + Sort**
1. User types any line numbers (even duplicates or out of order)
2. Click Sort to organize
3. Click Renumber to create proper spacing
4. Insert new lines in the spaces

## Proposed Solutions

### Option A: Smart Insertion Mode (Assisted)

**Concept**: Add an "Insert Lines" feature that helps users insert between existing lines.

**Workflow**:
1. User positions cursor between line 10 and line 20
2. User clicks "Insert Lines" button or presses Ctrl+I
3. Dialog appears:
   - "Insert after line: 10"
   - "Before line: 20"
   - "How many lines? [input]"
4. System automatically:
   - Picks appropriate line numbers (11, 12, 13... or 15, 16, 17...)
   - Inserts blank lines at cursor position
   - Numbers them appropriately
5. User types code into the blank lines
6. If more lines needed, they can repeat or manually continue numbering

**Pros**:
- Explicit user control
- Clear intent
- Works with limited space
- No magic behavior

**Cons**:
- Requires knowing how many lines needed in advance
- Extra UI complexity
- What if user picks a number that doesn't fit?

**Implementation notes**:
- Could use midpoint numbering: between 10 and 20, use 15, 16, 17...
- If no space (e.g., 10 and 11), automatically trigger renumber first
- Or use decimal numbers temporarily: 10.1, 10.2, then renumber to integers

### Option B: Continuous Insertion Mode (Classic BASIC)

**Concept**: Mimic classic BASIC editor behavior with continuous line insertion.

**Workflow**:
1. User positions cursor after line 10
2. User presses Ctrl+I or clicks "Insert Mode"
3. System enters insertion mode:
   - Creates blank line with next sequential number (11 or 15, depending on space)
   - User types code
   - When user presses Enter, creates another blank numbered line
   - Continues until user presses Esc or clicks outside
4. System automatically manages line numbers during insertion

**Pros**:
- Natural BASIC editing flow
- No need to know line count in advance
- Familiar to classic BASIC users
- Continuous workflow

**Cons**:
- Requires modal editing state
- What happens when numbers run out?
- More complex state management
- Might feel weird in a modern GUI

**Implementation notes**:
- Could show visual indicator that insertion mode is active
- Auto-renumber when running out of space
- ESC key exits mode

### Option C: Unnumbered Editing + Auto-Number (Modern)

**Concept**: Let users edit without line numbers, automatically number when needed.

**Workflow**:
1. User edits program without worrying about line numbers
2. Lines can be completely unnumbered in the editor
3. When user clicks Run, Save, or "Number Lines":
   - System automatically assigns line numbers (10, 20, 30...)
   - Updates GOTO/GOSUB references
   - Displays numbered version
4. User can switch between numbered and unnumbered view

**Pros**:
- Modern editing experience
- No mental overhead for line numbers
- Easy insertion anywhere
- Familiar to modern programmers

**Cons**:
- Not authentic BASIC experience
- GOTO/GOSUB must use labels or be rewritten
- Breaks traditional BASIC workflow
- Some programs rely on specific line numbers (ON GOTO, computed GOTO)

**Implementation notes**:
- Would need label system or line number rewriting
- Could show line numbers in gutter only
- Significant parser/runtime changes needed

### Option D: Smart Renumber (Enhanced Current)

**Concept**: Enhance current renumber feature to be more intelligent.

**Workflow**:
1. User types lines with any numbers (even duplicates/gaps)
2. When renumbering:
   - Analyzes current line distribution
   - Offers smart defaults:
     * "You have 45 lines. Recommended: start=10, increment=10"
     * "You have 200 lines. Recommended: start=100, increment=100"
   - Shows preview of result
3. User can adjust or accept
4. Renumber creates appropriate spacing

**Enhanced features**:
- "Make space after line X" option
- "Renumber selection only" option
- "Keep line X fixed, renumber around it" option

**Pros**:
- Builds on existing functionality
- No new modes or workflows
- Smart assistance without magic
- Backward compatible

**Cons**:
- Still requires user to think about numbering
- Doesn't solve "how many lines?" question
- More UI complexity

## Recommended Approach

**Phase 1: Enhanced Renumber (Option D)**
- Start with current renumber dialog
- Add smart defaults based on line count
- Add "Renumber with extra spacing" option (e.g., increment=100 for lots of room)
- Show preview before applying
- Document best practices

**Phase 2: Quick Insert (Simplified Option A)**
- Add "Insert Blank Line" command (Ctrl+Shift+I)
- Automatically picks line number between current and next
- User can repeat to insert multiple lines
- No modal state, just quick insertion
- If no space, auto-suggests renumber

**Phase 3: Consider Option B or C based on user feedback**
- Gather usage data
- See if users want continuous insertion mode
- Evaluate if unnumbered editing makes sense

## Documentation Needed

### User Guide: "Working with Line Numbers"

**Topic 1: Basic Insertion**
```
Q: How do I insert lines between line 10 and line 20?

A: You have several options:

1. Manual numbering:
   - Type intermediate numbers (15, 16, 17...)
   - Works if there's space between the lines

2. Create space first:
   - Click Renumber button
   - Choose start=10, increment=10
   - This creates 10, 20, 30, 40...
   - Now you have room for 9 lines between each

3. Use sort and renumber:
   - Type any line numbers you want
   - Click Sort to organize
   - Click Renumber to create even spacing
```

**Topic 2: Renumbering Best Practices**
```
Q: What increment should I use?

A: It depends on your program size:
- Small programs (< 50 lines): increment=10
- Medium programs (50-200 lines): increment=10 or 20
- Large programs (> 200 lines): increment=100
- Lots of insertions expected: increment=100

The larger the increment, the more room for future insertions.
```

**Topic 3: Workflow Tips**
```
Q: What's the best workflow for editing?

A: We recommend:

1. Draft mode:
   - Don't worry about perfect numbering
   - Use any numbers (10, 11, 12, 100, 200...)
   - Focus on writing the code

2. Organize:
   - Click Sort to put lines in order
   - Click Renumber to create nice spacing
   - This gives you a clean numbered program

3. Insert as needed:
   - Add new lines with intermediate numbers
   - When you run out of space, renumber again
```

## Implementation Priority

1. ✅ **Current state**: Manual numbering + Renumber button (DONE)
2. 📝 **Document current workflow**: Add user guide section (TODO)
3. 🔧 **Quick enhancements**:
   - Smarter renumber defaults (analyze line count)
   - "Insert blank line" quick command
   - Renumber preview
4. 🎯 **Future consideration**: Continuous insertion mode (if user feedback supports it)

## Open Questions

1. **Do users want automatic numbering, or explicit control?**
   - Classic BASIC users might prefer manual
   - Modern users might prefer auto

2. **Should visual UIs mimic CLI behavior, or modernize it?**
   - Authentic vs. convenient
   - Learning tool vs. productivity tool

3. **Is line number management a feature or a pain point?**
   - Some users enjoy the control
   - Others find it tedious

4. **Should we support multiple editing modes?**
   - CLI-style (current)
   - Insertion mode (proposed)
   - Unnumbered mode (future)
   - Let users choose?

## Related Files

- `src/ui/tk_ui.py` - Tk editor implementation
- `src/ui/web/web_ui.py` - Web editor implementation
- `src/ui/curses_ui.py` - Curses editor (reference)
- `src/editing/manager.py` - Program manager with renumber logic

## References

- Classic BASIC editors: Apple II, Commodore 64, IBM BASIC
- Modern BASIC IDEs: QB64, FreeBASIC IDE, Visual Studio
- Line editor behavior: ED, EDLIN (historical context)
