# Compiler Memory Configuration

## Overview

The MBASIC-2025 compiler generates CP/M programs that use all available memory for strings.

## CP/M Memory Layout

```
CP/M Memory Map:

0x0000 ┌─────────────────────────┐
       │  Warm boot jump (3)     │
0x0003 │  IOBYTE, Disk byte (2)  │
0x0005 │  BDOS entry jump (3)    │
       │  (address at 0x0006)    │
       ├─────────────────────────┤
0x005C │  Default FCB            │
0x0080 │  Command line / DMA     │
0x0100 ├─────────────────────────┤ TPA Start
       │                         │
       │  Program Code           │
       │  (compiled from BASIC)  │
       │                         │
       ├─────────────────────────┤
       │  Static Variables       │
       │  String Descriptors     │
       │  GOSUB Return Stack     │ ← int gosub_stack[100] array
       │  File Control Blocks    │ ← z88dk FCBs are static, not heap
       ├─────────────────────────┤ __BSS_tail
       │                         │
       │  STRING POOL            │ ← All available memory (~56KB on 64K)
       │  (dynamic size)         │
       │                         │
       ├─────────────────────────┤ SP - 1024 (stack reserve)
       │  Stack reserve          │
       ├─────────────────────────┤ SP
       │  ↑ Stack (grows down)   │
       ├─────────────────────────┤
       │  BDOS                   │
0xFFFF └─────────────────────────┘
```

## String Pool Allocation

The string pool uses **all available memory** from `__BSS_tail` to `SP - stack_reserve`.

**No heap/malloc needed** - the pool is allocated directly at startup:

```c
extern unsigned char __BSS_tail;
uint16_t pool_size = SP - 1024 - (uint16_t)&__BSS_tail;
mb25_init((uint8_t *)&__BSS_tail, pool_size);
```

Key points:
- `__BSS_tail` is the z88dk symbol marking end of BSS (end of program data)
- File I/O buffers (FCBs) are in BSS, not heap - already counted in `__BSS_tail`
- 1024 bytes reserved for stack safety margin
- Typical pool size: ~56KB on 64K CP/M system

## GOSUB Stack

GOSUB/RETURN uses a compiler-generated array, NOT the C call stack:

```c
int gosub_stack[100];  /* Return IDs */
int gosub_sp = 0;      /* Stack pointer */
```

The C stack (CRT_STACK_SIZE) is only for z88dk library function calls.

## Garbage Collection

GC uses in-place compaction with shell sort (no stdlib required):

1. Sort string descriptors by address (shell sort - O(n log n))
2. Compact strings forward using memmove (handles overlaps)
3. Re-sort descriptors by ID (shell sort)
4. Reset allocator to end of compacted data

**No temporary buffer** - compaction happens in-place within the pool.
**No stdlib** - inline shell sort avoids qsort function pointer overhead.

## Monitoring at Runtime

```basic
10 PRINT "String pool free:", FRE("")
```

`FRE("")` returns free space in the string pool.

## Implementation Files

- `runtime/strings/mb25_string.c` - String system implementation
- `runtime/strings/mb25_string.h` - String system header
- `src/codegen_backend.py` - Code generation (pool initialization)
