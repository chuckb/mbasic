# Library Browser Feature - TODO

⏳ **Status:** TODO - Not yet started

## Overview

Add a library browser feature that allows users to browse and load example BASIC programs, games, and utilities from within the UI. Originally intended for the Web UI to send programs from the server, but would be useful for any visual UI (Tkinter, Web, future GUIs).

## Motivation

- **372 BASIC programs** already exist in the `basic/` directory
- Users (especially beginners) would benefit from discovering example programs
- Games like blackjack, baccarat, calendar utilities, etc. are immediately runnable
- Makes the UI more discoverable and educational
- Web UI especially benefits since users can't easily browse the server filesystem

## Current State

### Existing Programs

The repository contains 372+ BASIC programs including:
- **Games**: bacarrat.bas, blkjk.bas, tankie.bas, othello.bas
- **Utilities**: calendar.bas, convert.bas, diary.bas, budget.bas
- **Educational**: mathtest.bas, benchmk.bas, sample*.bas
- **Technical**: Various RBS, RBB, and communication programs

### Current Load Mechanisms

Each UI has its own file loading:
- **CLI**: LOAD "filename" command
- **Curses**: Ctrl+L opens file browser dialog
- **Tkinter**: File → Open menu, file browser dialog
- **Web**: Open button uploads file from user's computer (cannot access server files)

## Proposed Implementation

### Architecture

**Server-Side:**
1. Create `basic/library/` directory with curated examples
2. Organize into categories:
   - `games/` - Interactive games
   - `demos/` - Visual demonstrations
   - `tutorials/` - Learning examples with comments
   - `utilities/` - Useful tools (calendar, converters, etc.)
   - `classic/` - Historical CP/M programs
3. Create `library_index.json` with metadata:
   ```json
   {
     "games": [
       {
         "filename": "blackjack.bas",
         "title": "Blackjack",
         "description": "Classic card game",
         "author": "Unknown",
         "year": "1981",
         "lines": 250,
         "tags": ["game", "card", "interactive"]
       }
     ]
   }
   ```

**UI Integration:**

**Web UI (Priority 1):**
- Add "Examples" button to toolbar or File menu
- Dialog shows categorized list of programs
- Click to load into editor (replaces current program, with warning)
- Server endpoint: `GET /api/library` returns index
- Server endpoint: `GET /api/library/{category}/{filename}` returns program text

**Tkinter UI (Priority 2):**
- Add File → Load Example submenu
- Hierarchical menu with categories
- Loads directly from `basic/library/` filesystem

**Curses UI (Priority 3):**
- Add Ctrl+E (Examples) keybinding
- Text-based menu browser (similar to help browser)
- Loads directly from `basic/library/` filesystem

**CLI (Priority 4):**
- Add EXAMPLES command to list available programs
- EXAMPLE "name" to load one
- EXAMPLE LIST "category" to list by category

### Security Considerations

**Web UI:**
- Only serve files from `basic/library/` directory (sandboxed)
- Validate filenames to prevent path traversal attacks
- Read-only access (users can't modify server files)
- Rate limiting on library endpoints

**All UIs:**
- Confirm before replacing current program
- Show preview/description before loading

## Implementation Plan

### Phase 1: Organization (1-2 hours)
- [ ] Create `basic/library/` directory structure
- [ ] Curate 20-30 best programs from existing collection
- [ ] Move to organized categories
- [ ] Add header comments explaining what each program does
- [ ] Test that all programs parse and run correctly

### Phase 2: Metadata (1 hour)
- [ ] Create `library_index.json` with all program metadata
- [ ] Write utility script to auto-generate basic metadata (line count, etc.)
- [ ] Manually add descriptions, tags, categories

### Phase 3: Web UI (2-3 hours)
- [ ] Add `/api/library` endpoint to nicegui_backend.py
- [ ] Add `/api/library/{category}/{filename}` endpoint
- [ ] Create library browser dialog in Web UI
- [ ] Add "Examples" button to toolbar
- [ ] Test loading programs

### Phase 4: Other UIs (2-4 hours)
- [ ] Tkinter: Add File → Load Example menu
- [ ] Curses: Add Ctrl+E examples browser
- [ ] CLI: Add EXAMPLES and EXAMPLE commands
- [ ] Update UI documentation

### Phase 5: Testing & Documentation (1-2 hours)
- [ ] Test library browser in all UIs
- [ ] Update help documentation
- [ ] Add library browser to feature parity tracking
- [ ] Create user guide for finding examples

## Example Programs to Include

### Games (Immediate Fun)
- Blackjack (blkjk.bas)
- Baccarat (bacarrat.bas)
- Tankie (tankie.bas) - if it's a tank game

### Tutorials (Learning)
- Hello World (create simple one if not exists)
- FOR loop examples
- INPUT/PRINT examples
- Array examples
- File I/O examples

### Utilities (Useful Tools)
- Calendar (calendar.bas, calendr5.bas)
- Unit converter (convert.bas)
- Math test (mathtest.bas)
- Benchmark (benchmk.bas)

### Demos (Visual/Interesting)
- Astronomy calculator (astrnmy2.bas)
- Big calendar printer (bigcal2.bas)
- Character frequency analyzer (charfreq.bas)

## Testing Criteria

- [ ] All library programs parse without errors
- [ ] All library programs run to completion (or clean exit)
- [ ] Library browser shows all categories
- [ ] Clicking program loads it correctly
- [ ] Confirmation dialog appears before replacing current program
- [ ] Server endpoints secure (no path traversal)
- [ ] Works on all supported browsers (Web UI)
- [ ] Documentation is clear and complete

## Related Files

- `src/ui/web/nicegui_backend.py` - Web UI implementation
- `src/ui/tk_ui.py` - Tkinter UI implementation
- `src/ui/curses_ui.py` - Curses UI implementation
- `src/cli.py` - CLI command handling
- `basic/` - Current program storage
- `docs/help/ui/*/` - UI-specific documentation

## Future Enhancements (Post-MVP)

- User-contributed programs (upload to library)
- Program rating/favorites system
- Search/filter programs by keyword
- "Run in sandbox" button to preview without loading
- Syntax highlighting in preview
- Export library to static HTML catalog
- Download entire library as ZIP

## Priority

**MEDIUM** - Nice-to-have feature that improves user experience significantly, especially for beginners and the Web UI. Not blocking any core functionality.

## Estimated Effort

**8-12 hours total** (spread across phases)

## Dependencies

- No blocking dependencies
- Web UI already has dialog/menu infrastructure
- File serving already works for Open button
- Just needs organization and UI integration

## Success Metrics

- Users can discover and load example programs without documentation
- At least 20 high-quality examples available
- Feature documented in all UI help guides
- No security vulnerabilities in file serving
- Positive user feedback on discoverability

---

**Created:** 2025-10-29
**Last Updated:** 2025-10-29
