# JavaScript Backend - Unimplemented Features

## Status: Phase 1-4 Complete

This document tracks what's **not yet implemented** in the JavaScript backend.

---

## ✅ IMPLEMENTED (Core Features)

### Control Flow
- ✓ GOTO / ON GOTO
- ✓ GOSUB / RETURN
- ✓ FOR / NEXT (variable-indexed with state tracking)
- ✓ WHILE / WEND
- ✓ IF / THEN / ELSE

### I/O
- ✓ PRINT (with separators)
- ✓ READ / DATA / RESTORE

### Variables & Arrays
- ✓ LET (assignment)
- ✓ DIM (array declarations)
- ✓ Array access (subscripts)

### Other
- ✓ REM (comments - skipped)
- ✓ END

---

## ⚠️ STUBBED (Partially Implemented)

### INPUT
**Status**: Stub only - prints "TODO" comment
**Issue**: Requires async handling in browser (prompt) vs Node.js (readline)
**Priority**: HIGH - needed for interactive programs

### DEF FN
**Status**: Collection works, generation returns empty
**Issue**: Need to generate JavaScript functions
**Priority**: MEDIUM - used in some programs

---

## ❌ NOT IMPLEMENTED

### I/O Statements
- LINE INPUT - Read entire line including commas/quotes
- INPUT # - Read from file
- PRINT # - Write to file
- PRINT USING - Formatted output
- LPRINT - Print to line printer (could map to console)
- WRITE - CSV-formatted output
- WRITE # - Write to file

### File Operations
- OPEN - Open file for I/O
- CLOSE - Close file
- RESET - Close all files
- KILL - Delete file
- NAME - Rename file
- FILES - List directory
- FIELD - Define random file buffer
- GET - Read random file record
- PUT - Write random file record
- LSET / RSET - Format string for random files
- LOF - Length of file (would be function)
- EOF - End of file test (would be function)
- LOC - Current file position (would be function)

### String Operations
- MID$ assignment - Modify substring in place

### Program Control
- STOP - Halt execution (like END but different)
- CONT - Continue after STOP (interactive only)
- CHAIN - Load and run another program
- RUN - Start program execution
- LOAD - Load program (interactive)
- SAVE - Save program (interactive)
- MERGE - Merge another program
- NEW - Clear program (interactive)
- DELETE - Delete line range (interactive)
- RENUM - Renumber lines (interactive)

### Error Handling
- ON ERROR GOTO - Set error handler
- RESUME - Resume after error
- ERROR - Trigger error
- ERL - Line number where error occurred (function)
- ERR - Error code (function)

### System/Hardware
- POKE - Write to memory address
- OUT - Output to I/O port
- WAIT - Wait for I/O port condition
- SYSTEM - Exit to operating system
- CLS - Clear screen (could implement in browser)
- LOCATE - Position cursor (could implement)
- COLOR - Set colors (could implement)
- WIDTH - Set screen/printer width

### Arrays
- ERASE - Clear array to defaults
- SWAP - Swap two variables
- OPTION BASE - Set array base 0/1 (handled in semantic analysis)
- COMMON - Share variables between chained programs

### Other
- RANDOMIZE - Seed random generator (could implement)
- CALL - Call machine language subroutine
- DEF SEG - Set memory segment
- DEF type statements - Type declarations (handled in semantic analysis)
- TRON / TROFF - Trace on/off (debugging)
- CLEAR - Set memory limits
- LIMITS - Show memory limits
- STEP - Single-step execution (debugging)

### Interactive/Editor Commands (Not Relevant)
- LIST - List program
- HELP - Show help
- SET - Configure settings
- SHOW - Show settings

---

## 🔧 KNOWN ISSUES / TODOs

### Minor Fixes Needed
1. **GOSUB return address** - Currently uses current_line as placeholder, should calculate next statement/line properly
2. **FOR loop skip** - When initial condition not met, need to jump to line after NEXT (not implemented)
3. **NEXT without variable** - Currently errors, should use most recent FOR loop

### Missing Runtime Functions
- TAB() - Tab to column (mentioned in PRINT but not implemented)
- SPC() - Print N spaces (mentioned in PRINT but not implemented)
- INSTR() - Find substring position (in spec but not in runtime)
- SPACE$() - Generate N spaces
- STRING$() - Repeat character N times
- FIX() - Truncate to integer
- SGN() - Sign of number
- CINT() / CSNG() / CDBL() - Type conversions
- HEX$() / OCT$() - Number to hex/octal string
- POS() - Current print position
- PEEK() - Read memory
- INP() - Read I/O port
- USR() - Call machine code

---

## 📊 Implementation Priority

### HIGH (Needed for most programs)
1. INPUT - User input
2. RANDOMIZE - Proper random seeding
3. CLS / LOCATE - Screen control (for browser output)
4. TAB() / SPC() - Print formatting
5. INSTR() - String searching

### MEDIUM (Nice to have)
1. DEF FN - User-defined functions
2. SWAP - Variable swapping
3. MID$ assignment - String modification
4. PRINT USING - Formatted output
5. Additional string functions (SPACE$, STRING$, etc.)
6. Additional math functions (FIX, SGN, conversions)

### LOW (Specialized/Advanced)
1. File I/O (OPEN, CLOSE, etc.)
2. Error handling (ON ERROR, RESUME)
3. CHAIN - Program chaining
4. Graphics (implementation-specific)
5. Sound (implementation-specific)
6. Machine code / hardware access (POKE, PEEK, CALL, etc.)

### NOT APPLICABLE (Interactive/Editor)
- LIST, NEW, RUN, LOAD, SAVE, DELETE, RENUM
- HELP, SET, SHOW
- CONT, STEP

---

## 📝 Notes

- **File I/O**: Could implement with localStorage (browser) and fs module (Node.js)
- **Graphics**: Could use Canvas API (browser), skip in Node.js
- **Sound**: Could use Web Audio API (browser), skip in Node.js
- **Screen control**: Could implement CLS/LOCATE/COLOR for browser, map to ANSI codes in Node.js
- **Hardware access**: POKE/PEEK/OUT/INP not meaningful in JavaScript, could stub or error

---

**Last Updated**: 2025-11-13
**Version**: 1.0.898
