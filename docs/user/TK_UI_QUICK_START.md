# MBASIC Tk UI - Quick Start Guide

## Starting the Tk UI

```bash
python3 mbasic.py --backend tk [filename.bas]
```

Or simply:
```bash
python3 mbasic.py [filename.bas]
```

The Tk UI is the default graphical interface for MBASIC.

## First Program - Hello World

1. Start the Tk UI: `python3 mbasic.py --backend tk`
2. In the editor window, type:
   ```basic
   10 PRINT "HELLO, WORLD!"
   20 END
   ```
3. Press **Ctrl+R** to run
4. See output in the lower pane

## Essential Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl+R** | Run program |
| **Ctrl+S** | Save file |
| **Ctrl+O** | Open file |
| **Ctrl+N** | New program |
| **Ctrl+I** | Smart insert blank line |
| **Ctrl+E** | Renumber program |
| **Ctrl+V** | Show/hide Variables window |
| **Ctrl+T** | Step through code |
| **Ctrl+B** | Toggle breakpoint |

## Screen Layout

```
┌────────────────────────────────────────────────────┐
│ Menu Bar                                           │
├─────────┬──────────────────────────────────────────┤
│ Line #  │  Editor Window                           │
│  Gutter │  - Write your BASIC program here         │
│         │  - Line numbers on left                  │
│  10     │  - Syntax errors marked with ?           │
│  20  ●  │  - Breakpoints marked with ●             │
│  30  ?  │                                           │
│         │                                           │
├─────────┴──────────────────────────────────────────┤
│ Output Window                                      │
│ - Program output appears here                      │
│ - Error messages shown here                        │
│ - Execution status displayed                       │
└────────────────────────────────────────────────────┘
```

## Smart Insert Workflow

**Smart Insert (Ctrl+I)** is the fastest way to add code between existing lines. No more mental math to figure out line numbers!

### Example 1: Basic Usage

You have this program:
```basic
10 PRINT "START"
20 PRINT "END"
```

Want to add a line between them?

1. Click on line 10 (or position cursor anywhere on that line)
2. Press **Ctrl+I**
3. A blank line 15 is automatically inserted!

Result:
```basic
10 PRINT "START"
15
20 PRINT "END"
```

The cursor is positioned right after the line number, ready to type.

### Example 2: No Gap - Auto Renumber

You have consecutive lines:
```basic
10 PRINT "ONE"
11 PRINT "TWO"
12 PRINT "THREE"
```

Position cursor on line 10, press **Ctrl+I**:

A dialog appears: "No room between lines 10 and 11. Would you like to renumber the program to make room?"

Click **Yes** → Lines 11 onwards are renumbered to 1000, 1010, 1020... creating plenty of room!

Result:
```basic
10 PRINT "ONE"
15
1000 PRINT "TWO"
1010 PRINT "THREE"
```

### Example 3: At End of Program

You have:
```basic
10 PRINT "START"
20 PRINT "MIDDLE"
30 PRINT "END"
```

Cursor on line 30, press **Ctrl+I**:

A blank line 40 is inserted (using standard increment of 10).

Result:
```basic
10 PRINT "START"
20 PRINT "MIDDLE"
30 PRINT "END"
40
```

### Smart Insert vs Manual Numbering

**Old way (manual):**
```
1. Look at line 10 and line 20
2. Calculate: (10 + 20) / 2 = 15
3. Type: "15 PRINT ..."
```

**New way (Smart Insert):**
```
1. Position on line 10
2. Press Ctrl+I
3. Start typing your code
```

**Time saved:** ~5-10 seconds per line insertion. Over a programming session, this adds up!

## Typical Workflows

### 1. Write New Program

```
1. Press Ctrl+N for new program
2. Type first line: 10 PRINT "START"
3. Press Enter
4. Type next line: 20 END
5. Press Ctrl+R to run
6. Check output in lower pane
7. Press Ctrl+S to save
```

### 2. Expand Existing Program

You have a working program and need to add functionality:

```
1. Find the spot where new code goes
2. Press Ctrl+I to insert blank line
3. Type your new code
4. Press Ctrl+R to test
5. Press Ctrl+S to save
```

**Example:**
```basic
Before:
10 INPUT "Enter number"; N
20 PRINT "You entered"; N
30 END

After (cursor on 10, Ctrl+I twice):
10 INPUT "Enter number"; N
15 IF N < 0 THEN PRINT "Must be positive" : GOTO 10
17 ' Validate input
20 PRINT "You entered"; N
30 END
```

### 3. Major Restructuring - Use Renumber

Your program has grown and line numbers are a mess:

```
1. Press Ctrl+E (Renumber dialog opens)
2. Set "Start at": 100
3. Set "Increment": 10
4. Click "Renumber"
5. All line numbers and GOTO/GOSUB references updated!
```

**Before renumber:**
```basic
10 X=1
15 Y=2
17 GOTO 10
21 END
```

**After renumber (start=100, increment=10):**
```basic
100 X=1
110 Y=2
120 GOTO 100
130 END
```

Notice: GOTO 10 automatically became GOTO 100!

### 4. Debug with Breakpoints and Variables

```
1. Click line number gutter to set breakpoint (● appears)
2. Press Ctrl+V to open Variables window
3. Press Ctrl+R to run
4. Program stops at breakpoint
5. Check variable values in Variables window
6. Press Ctrl+T to step through code
7. Watch variables update in real-time
8. Press Ctrl+G to continue running
```

**Variables Window Features:**
- Click column headers to sort
- Shows all variables and their current values
- Updates automatically as you step
- Types displayed (integer, float, string, array)

### 5. Advanced Editing - Find and Replace

Large program with repeated code?

```
1. Press Ctrl+H (Find and Replace)
2. Enter find text: "OLDVAR"
3. Enter replace text: "NEWVAR"
4. Click "Replace All"
5. All occurrences updated
```

## Common Tasks

### Load, Edit, Save

```bash
# Start with existing file
python3 mbasic.py --backend tk myprogram.bas

# Or load from menu
1. Press Ctrl+O
2. Browse to file
3. Click Open
4. Edit in editor
5. Press Ctrl+S to save
```

### Create Program Template

```basic
10 REM Program: [Name]
20 REM Author: [Your Name]
30 REM Date: [Date]
40 REM Purpose: [Description]
50 REM
100 ' Initialize variables
110
200 ' Main program
210
900 ' Subroutines
910
1000 END
```

Use **Ctrl+I** to fill in sections!

### Fix Syntax Errors

Red **?** markers appear in line number gutter for syntax errors:

```
1. Look for ? in gutter
2. Read error in output pane
3. Fix the syntax
4. ? disappears automatically (100ms delay)
5. Press Ctrl+R to run
```

**Common errors:**
- Missing quotes: `PRINT HELLO` → `PRINT "HELLO"`
- Missing THEN: `IF X=1 GOTO 100` → `IF X=1 THEN GOTO 100`
- Typos: `PIRNT` → `PRINT`

### Work with Arrays

```basic
10 DIM A(10)
20 FOR I = 1 TO 10
30   A(I) = I * 10
40 NEXT I
50 PRINT A(5)
60 END
```

Run with **Ctrl+R**, then check Variables window (**Ctrl+V**) to see array contents!

## Tips and Tricks

### 1. Smart Insert for Rapid Development

**Scenario:** You have a skeleton program and need to flesh it out.

```basic
10 REM Initialize
100 REM Process
200 REM Output
300 END
```

Use Smart Insert (Ctrl+I) to add details under each section header without worrying about line numbers!

### 2. Renumber Before Sharing

Your development version might have messy line numbers:
```basic
10 PRINT "START"
15 X=1
17 Y=2
21 GOTO 50
50 END
```

Before sharing, make it clean:
1. Press **Ctrl+E**
2. Start=10, Increment=10
3. Result:
```basic
10 PRINT "START"
20 X=1
30 Y=2
40 GOTO 50
50 END
```

### 3. Use Comments Liberally

MBASIC supports two comment styles:
```basic
10 REM This is a remark statement
20 ' This is also a comment (shorter!)
```

Add comments while developing with Smart Insert:
```basic
10 X = 5
' Ctrl+I here creates line 15
15 ' Calculate result
20 Y = X * 10
```

### 4. Variables Window for Arrays

When working with arrays, keep Variables window open:

```basic
10 DIM SCORES(5)
20 FOR I = 1 TO 5
30   INPUT "Score"; SCORES(I)
40 NEXT I
```

Run this with **Ctrl+V** window open - you'll see each array element as it's filled!

### 5. Execution Stack for Loops

Press **Ctrl+K** to see Execution Stack while stepping through nested loops:

```basic
10 FOR I = 1 TO 3
20   FOR J = 1 TO 2
30     PRINT I; J
40   NEXT J
50 NEXT I
```

The stack shows:
```
FOR I=1 TO 3 STEP 1  [I=1]
  FOR J=1 TO 2 STEP 1  [J=1]
```

Perfect for debugging complex loop logic!

### 6. Quick Testing Cycle

Fastest workflow for iterative development:

```
Type → Ctrl+R → Check → Edit → Ctrl+R → Check → ...
```

No need to save between test runs! Save with **Ctrl+S** only when you're happy with results.

### 7. Breakpoint Shortcuts

**Mouse:** Click line number to toggle breakpoint
**Keyboard:** Position cursor, press **Ctrl+B**

Try both and use whichever feels faster!

## Next Steps

### Learn More About...

- **Debugging**: See [Debugging Features](../docs/help/common/debugging.md)
- **Keyboard Shortcuts**: See [Tk Keyboard Shortcuts](../docs/help/ui/tk/keyboard-shortcuts.md)
- **BASIC Language**: See [Language Reference](../docs/help/common/language/index.md)
- **Editor Features**: See [Editor Commands](../docs/help/common/editor-commands.md)

### Try These Sample Programs

Start with simple examples in `basic/` directory:

```bash
python3 mbasic.py --backend tk basic/hello.bas
python3 mbasic.py --backend tk basic/loops.bas
python3 mbasic.py --backend tk basic/arrays.bas
```

### Master These Skills

In order of importance:

1. **Smart Insert (Ctrl+I)** - Essential for efficient editing
2. **Run/Step/Continue (Ctrl+R/T/G)** - Core debugging workflow
3. **Variables Window (Ctrl+V)** - See what your program is doing
4. **Renumber (Ctrl+E)** - Keep code organized
5. **Breakpoints (Ctrl+B)** - Stop at critical points
6. **Save Often (Ctrl+S)** - Protect your work

### Common Mistakes to Avoid

❌ **Manually calculating line numbers** → Use Smart Insert instead
❌ **Running without saving** → Save first with Ctrl+S
❌ **Ignoring ? markers** → Fix syntax errors before running
❌ **Not using Variables window** → You're debugging blind!
❌ **Stepping through entire program** → Set breakpoints, use Continue

## Getting Help

- **In-app help**: Press **F1** or use Help menu
- **Online docs**: See `docs/` directory
- **Examples**: Check `basic/` directory
- **Issues**: Report at GitHub repository

---

**Welcome to MBASIC!** Start with simple programs, use Smart Insert to build them up, and explore the debugging features. You'll be productive in minutes!
