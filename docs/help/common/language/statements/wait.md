---
category: hardware
description: To suspend program execution while monitoring the status of a machine input port
keywords: ['command', 'data', 'for', 'if', 'input', 'loop', 'next', 'number', 'program', 'put']
syntax: WAIT <port number>, I[,J]
title: WAIT
type: statement
---

# WAIT

## Implementation Note

⚠️ **Not Implemented**: This feature requires direct hardware I/O port access and is not implemented in this Python-based interpreter.

**Behavior**: Statement is parsed but no operation is performed

**Why**: Cannot access hardware I/O ports from a Python interpreter. WAIT was used to synchronize with hardware devices by polling I/O ports.

**Alternative**: For delays, use a busy loop or timer logic in BASIC. For event synchronization, restructure the program to use sequential logic instead of hardware polling.

**Historical Reference**: The documentation below is preserved from the original MBASIC 5.21 manual for historical reference.

---

## Syntax

```basic
WAIT <port number>, I[,J]
```

Where:
- **port number**: Integer expression specifying the I/O port to monitor
- **I**: Integer expression for AND mask
- **J**: Optional integer expression for XOR mask (default: 0)

## Purpose

To suspend program execution while monitoring the status of a machine input port.

## Remarks

The WAIT statement causes execution to be suspended until a specified machine input port develops a specified bit pattern. The data read at the port is exclusive ORed with the integer expression J, and then ANDed with I. If the result is zero, BASIC-80 loops back and reads the data at the port again. If the result is nonzero, execution continues with the next statement. If J is omitted, it is assumed to be zero.

**CAUTION**: It is possible to enter an infinite loop with the WAIT statement, in which case it will be necessary to manually restart the machine.

## Example

```basic
100 WAIT 32,2
```

## See Also
- [CALL](call.md) - To call an assembly language subroutine
- [OUT](out.md) - To send a byte to a machine output port
- [POKE](poke.md) - To write a byte into a memory location
