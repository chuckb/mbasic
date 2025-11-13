# FOR Loop Stack Behavior in Real MBASIC 5.21 - Test Results

## Date
2025-11-13

## Summary

Tested real MBASIC 5.21 to determine FOR loop stack behavior. **Key finding**: Jumping out of a FOR loop (via GOTO, ON GOTO, etc.) implicitly removes that loop from the stack, allowing the loop variable to be reused immediately.

## Test Results

### Test 1: Maximum FOR Loop Depth
**File**: `tests/for_test1_depth.bas`

**Result**: ✅ Real MBASIC supports at least 10 levels of nested FOR loops

**Conclusion**: No 8-level limit enforced. The "8-deep circular buffer" may have been a documentation note or optimization detail, but MBASIC supports deeper nesting.

```
Testing FOR loop depth...
Depth 1
Depth 2
Depth 3
Depth 4
Depth 5
Depth 6
Depth 7
Depth 8
Depth 9
Depth 10
Success! Max depth >= 10
```

### Test 2: Nine Nested Loops
**File**: `tests/for_test2_overflow.bas`

**Result**: ✅ 9 nested loops work without error

**Conclusion**: No overflow error at 9 levels. Stack is sufficiently deep (likely limited only by memory).

### Test 3: Jump Out and Reuse Variable (CRITICAL TEST)
**File**: `tests/for_test3_jump_reuse.bas`

**Result**: ✅ **Jumping out of a FOR loop allows immediate reuse of the loop variable**

**Code pattern**:
```basic
30 FOR I=1 TO 10
40 PRINT "I=";I
50 IF I=3 THEN GOTO 100
60 NEXT I
...
100 PRINT "Jumped out at I=";I
110 PRINT "Starting new FOR I loop..."
120 FOR I=1 TO 5    ' This works! No error!
130 PRINT "New I=";I
140 NEXT I
```

**Output**:
```
Starting FOR I loop...
I= 1
I= 2
I= 3
Jumped out at I= 3
Starting new FOR I loop...
New I= 1
New I= 2
New I= 3
New I= 4
New I= 5
Success!
```

**Conclusion**: When you GOTO out of a FOR loop, real MBASIC removes that loop from the active stack. The variable becomes available for reuse immediately.

### Test 4: NEXT Without Matching FOR
**File**: `tests/for_test4_next_search.bas`

**Result**: ❌ Error: "FOR Without NEXT in 30"

**Conclusion**: NEXT requires a matching FOR on the stack. If you jump over a FOR and try to NEXT it, you get an error.

### Test 5: Multiple Jumps with Same Variable
**File**: `tests/for_test5_circular.bas`

**Result**: ✅ Can jump out of FOR I and start new FOR I nine times in succession

**Code pattern**:
```basic
30 FOR I=1 TO 1:PRINT "Loop 1":GOTO 50
50 FOR I=1 TO 1:PRINT "Loop 2":GOTO 70
70 FOR I=1 TO 1:PRINT "Loop 3":GOTO 90
... (9 times total)
```

**Output**:
```
Loop 1
Loop 2
Loop 3
Loop 4
Loop 5
Loop 6
Loop 7
Loop 8
Loop 9
9 jumps OK, all same var
```

**Conclusion**: Each GOTO implicitly pops the FOR from the stack before the next FOR is pushed. No circular buffer overflow.

### Test 6: Super Star Trek Pattern
**File**: `tests/for_test6_super_trek.bas`

**Result**: ✅ Works exactly as in Super Star Trek

**Code pattern**:
```basic
50 FOR I=1 TO 9
60 IF LEFT$(A$,3)<>MID$(A1$,3*I-2,3) THEN 90
80 ON I GOTO 200,210,220,230,240,250,260,270,280
90 NEXT I
...
200 PRINT "Handler 1":FOR I=1 TO 2:PRINT "I=";I:NEXT I:GOTO 300
```

**Output**:
```
Match at I= 1
Handler 1
I= 1
I= 2
Handler done, I= 3
```

**Conclusion**: The exact Super Star Trek pattern works. Handler can use FOR I even though it was jumped to from inside a FOR I loop.

## Implementation Implications

### Current Bug
Our MBASIC implementation raises this error:
```
FOR loop variable I already active - nested FOR loops with same variable not allowed
```

This is **incorrect** for the case where you GOTO out of a FOR loop before starting a new one.

### Correct Behavior

1. **Nested FOR with same variable (should error)**:
   ```basic
   10 FOR I=1 TO 10
   20   FOR I=1 TO 5  ' ERROR - truly nested
   30   NEXT I
   40 NEXT I
   ```
   This should still be an error - you can't have two active FOR loops with the same variable in a nested fashion.

2. **Jump out then reuse (should work)**:
   ```basic
   10 FOR I=1 TO 10
   20   IF I=5 THEN GOTO 100
   30 NEXT I
   100 FOR I=1 TO 5  ' OK - previous loop exited
   110 NEXT I
   ```
   This should work - the GOTO at line 20 should remove the first FOR I from the stack.

### Stack Management Rules

Based on these tests, real MBASIC appears to implement these rules:

1. **FOR pushes** an entry onto the FOR loop stack
2. **NEXT pops** the matching entry from the stack
3. **GOTO/ON GOTO out of a FOR** implicitly removes that FOR (and any nested within it) from the stack
4. **Starting a FOR with same variable** as an active FOR is only an error if both are on the stack simultaneously

### Implementation Strategy

Our runtime needs to:

1. **Track current execution position** (PC/line number)
2. **When executing GOTO/ON GOTO**: Pop any FOR loops from the stack whose range (start line to NEXT line) contains the current position but doesn't contain the target position
3. **When executing FOR**: Check if variable is already active on the stack (error if yes, unless previous one was implicitly popped)

Alternative simpler approach:
- **When executing FOR**: If variable already exists on stack, pop the old one before pushing the new one
- This would match the observed behavior where reusing a variable after jumping out "just works"

## Stack Structure

Real MBASIC's FOR loop stack appears to be:
- **Not limited to 8 entries** (supports at least 10)
- **Not circular** (no wraparound - just allows deeper nesting)
- **Separate from GOSUB stack** (likely - GOSUB is for return addresses)
- **May share with WHILE/WEND** (needs separate testing)

The "8-deep circular buffer" mentioned by the user may have been:
- An early CP/M BASIC variant
- A different BASIC implementation
- A misremembering
- Documentation that described implementation details but not limits

## Recommended Fix

Modify `src/runtime.py` to allow FOR variable reuse when jumping out of loops:

```python
def _execute_for(self, var_name, start, end, step):
    # If variable already active, check if we jumped out
    if var_name in self.for_stack:
        # Option 1: Just replace it (simplest)
        self._pop_for_loop(var_name)

    # Push new FOR loop
    self._push_for_loop(var_name, start, end, step, next_line)
```

This matches the observed behavior where the second FOR with the same variable implicitly replaces the first.

## Files Referenced

Test programs:
- `tests/for_test1_depth.bas` - Depth test (10 levels)
- `tests/for_test2_overflow.bas` - Overflow test (9 levels)
- `tests/for_test3_jump_reuse.bas` - Jump and reuse (critical test)
- `tests/for_test4_next_search.bas` - NEXT stack search
- `tests/for_test5_circular.bas` - Multiple jumps same var
- `tests/for_test6_super_trek.bas` - Super Star Trek pattern

Implementation files to modify:
- `src/runtime.py` - FOR loop stack management
- `src/interpreter.py` - GOTO/ON GOTO implementation (maybe)
- `src/statements/control_flow.py` - FOR/NEXT implementation

## Related Documentation

- `docs/dev/FOR_LOOP_JUMP_TODO.md` - Original issue description
- `tests/HOW_TO_RUN_REAL_MBASIC.md` - How to test with real MBASIC 5.21
