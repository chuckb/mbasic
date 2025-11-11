# MBASIC Compiler - Remaining Work

## Status Summary
The MBASIC-to-C compiler (via z88dk for CP/M) has substantial functionality but several areas remain unimplemented.

## ✅ Currently Implemented

### Core Language Features
- **Variables**: INTEGER (%), SINGLE (!), DOUBLE (#), STRING ($)
- **Arrays**: Multi-dimensional with DIM, automatic flattening to 1D
- **Expressions**: Full arithmetic, relational, logical operators
- **Type declarations**: DEFINT, DEFSNG, DEFDBL, DEFSTR

### Control Flow
- IF/THEN/ELSE
- FOR/NEXT loops
- WHILE/WEND loops
- GOTO/GOSUB/RETURN
- ON...GOTO/ON...GOSUB (computed branches)
- END, STOP

### Data Operations
- DATA/READ/RESTORE (with string support)
- LET assignments
- SWAP statement

### Functions
- **Math**: ABS, SGN, INT, FIX, SIN, COS, TAN, ATN, EXP, LOG, SQR, RND
- **String**: LEFT$, RIGHT$, MID$, CHR$, STR$, SPACE$, STRING$, HEX$, OCT$
- **String analysis**: LEN, ASC, VAL, INSTR
- **Type conversion**: CINT, CSNG, CDBL
- **User-defined**: DEF FN

### I/O Operations
- PRINT (basic, not USING)
- INPUT (keyboard input)

### Other
- REM comments
- RANDOMIZE
- POKE/OUT (placeholders only)

## ❌ Not Yet Implemented

### Critical Features

#### 1. File I/O (High Priority)
- **OPEN** - Open file for I/O
- **CLOSE** - Close file
- **INPUT #** - Read from file
- **LINE INPUT #** - Read line from file
- **PRINT #** - Write to file
- **WRITE #** - Write comma-delimited data
- **GET/PUT** - Random access file operations
- **FIELD** - Define record structure
- **LSET/RSET** - Left/right justify in field
- **EOF()** - End of file function
- **LOC()** - Current file position
- **LOF()** - Length of file

#### 2. Error Handling
- **ON ERROR GOTO** - Set error trap
- **RESUME** - Resume after error
- **RESUME NEXT** - Resume at next statement
- **RESUME line** - Resume at specific line
- **ERR** - Error code variable
- **ERL** - Error line variable
- **ERROR** - Generate error

#### 3. Formatted Output
- **PRINT USING** - Formatted print
- **LPRINT** - Print to printer
- **LPRINT USING** - Formatted printer output
- **WIDTH** - Set output width
- **TAB()** - Tab to column
- **SPC()** - Output spaces

### Secondary Features

#### 4. String Operations
- **MID$ statement** - Replace substring (MID$(A$,3,2)="XY")

#### 5. Memory/System Operations
- **CLEAR** - Clear variables and set memory
- **FRE()** - Free memory function
- **VARPTR()** - Variable pointer
- **PEEK()** - Read memory (currently returns 0)
- **INP()** - Read I/O port (currently returns 0)
- **WAIT** - Wait for port condition
- **SYSTEM** - Return to operating system

#### 6. Program Control (Interpreter-Specific)
These are primarily for interactive use and may not be needed in compiled code:
- **LIST** - List program
- **LOAD/SAVE/MERGE** - Program file operations
- **NEW** - Clear program
- **DELETE** - Delete lines
- **RENUM** - Renumber lines
- **CONT** - Continue after STOP
- **CHAIN** - Chain to another program
- **RUN** - Run program (could be supported for chaining)
- **TRON/TROFF** - Trace on/off
- **STEP** - Single step

#### 7. Advanced Features
- **COMMON** - Share variables between chained programs
- **ERASE** - Deallocate arrays
- **OPTION BASE** - Set array base (partially supported)
- **CLS** - Clear screen
- **RESET** - Reset disk system
- **KILL** - Delete file
- **NAME** - Rename file
- **FILES** - List files

#### 8. Binary Data Functions
- **CVI/CVS/CVD** - Convert string to numeric
- **MKI$/MKS$/MKD$** - Convert numeric to string

#### 9. Device I/O
- **CALL** - Call machine language routine

## Implementation Priority

### Phase 1: Essential for Real Programs
1. **File I/O** - Critical for data processing
2. **Error handling** - Needed for robust programs
3. **PRINT USING** - Common formatting need

### Phase 2: Enhanced Functionality
4. **String operations** (MID$ statement)
5. **Screen control** (CLS, WIDTH)
6. **Memory functions** (FRE, VARPTR)

### Phase 3: Advanced Features
7. **Binary data functions**
8. **Program chaining** (CHAIN, COMMON)
9. **Device I/O** (CALL)

### Phase 4: Interpreter Features (Optional)
10. Interactive commands (LIST, LOAD, SAVE, etc.)

## Technical Challenges

### File I/O Implementation
- Need to map BASIC file numbers to C FILE* pointers
- Handle different file modes (INPUT, OUTPUT, RANDOM)
- Implement record-based access for RANDOM files

### Error Handling
- Need to implement setjmp/longjmp for ON ERROR GOTO
- Track error codes and line numbers
- Handle RESUME properly

### PRINT USING
- Complex format string parsing
- Number formatting with #, comma, decimal point
- String field formatting

## Test Coverage Needed
- File I/O test suite
- Error handling test cases
- PRINT USING format tests
- Binary data conversion tests

## Estimated Effort
- File I/O: 2-3 days
- Error handling: 1-2 days
- PRINT USING: 1 day
- Other string operations: 1 day
- Remaining features: 2-3 days

**Total: ~1-2 weeks for comprehensive implementation**

## Notes
- Some features (TRON/TROFF, LIST, etc.) are primarily for interactive interpreters and may not be needed in compiled code
- CP/M-specific features may need special handling in z88dk
- Consider which features are essential vs. nice-to-have for the target use case