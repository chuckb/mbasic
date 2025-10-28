---
title: Common Workflows
type: guide
ui: tk
description: Step-by-step guides for common tasks
keywords: [tk, workflows, guide, tutorial]
---

# Common Workflows

Step-by-step guides for typical development tasks.

## 1. Write New Program

1. Press {{kbd:new_program}}
2. Type: `10 PRINT "START"`
3. Press Enter
4. Type: `20 END`
5. Press {{kbd:run_program}}
6. Check output
7. Press {{kbd:save_file}}

## 2. Expand Existing Program

You have working code and need to add more:

1. Find where to insert new code
2. Press {{kbd:smart_insert}} to insert blank line
3. Type your new code
4. Press {{kbd:run_program}} to test
5. Press {{kbd:save_file}}

## 3. Debug with Breakpoints

1. Click line number gutter to set breakpoint (● appears)
2. Press {{kbd:toggle_variables}} to open Variables window
3. Press {{kbd:run_program}}
4. Program stops at breakpoint
5. Check variable values
6. Press {{kbd:step_statement}} to step through code
7. Variables update in real-time
8. Press {{kbd:continue_execution}} to continue

## 4. Fix Syntax Errors

1. Look for red **?** in line number gutter
2. Read error in output pane
3. Fix the syntax
4. **?** disappears automatically (100ms delay)
5. Press {{kbd:run_program}} to test

## 5. Renumber Before Sharing

Your development version has messy line numbers. Make it clean:

1. Press {{kbd:renumber}}
2. Set Start=10, Increment=10
3. Click "Renumber"
4. All GOTO/GOSUB references automatically updated!

[← Back to Tk GUI Help](index.md)
