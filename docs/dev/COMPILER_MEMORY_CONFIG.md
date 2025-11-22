# Compiler Memory Configuration

## Overview

The MBASIC-2025 compiler generates CP/M programs that automatically detect available memory at runtime.

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
       ├─────────────────────────┤
       │                         │
       │  Heap (~75% of TPA)     │ ← Runtime allocated via -DAMALLOC
       │                         │
       │  Contains:              │
       │  - String pool          │
       │  - File I/O buffers     │
       │                         │
       ├─────────────────────────┤
       │  Free Space             │
       ├─────────────────────────┤ ← SP (from BDOS entry at 0x0006)
       │  ↑ Stack (grows down)   │ ← For C library calls only
       ├─────────────────────────┤
       │                         │
       │  BDOS                   │
       │                         │
       ├─────────────────────────┤
       │  CCP                    │
0xFFFF └─────────────────────────┘
```

## Runtime Memory Detection

The compiler uses z88dk's `-DAMALLOC` flag which:

1. Reads the BDOS entry point from address 0x0006
2. Calculates available TPA (Transient Program Area)
3. Allocates approximately 75% of TPA as heap
4. Adapts to actual system memory (works on 16K, 32K, 48K, 64K systems)

**Heap size is dynamic** - adapts to the system at runtime.

## GOSUB Stack

GOSUB/RETURN uses a compiler-generated array, NOT the C call stack:

```c
int gosub_stack[100];  /* Return IDs */
int gosub_sp = 0;      /* Stack pointer */
```

The C stack (CRT_STACK_SIZE) is only for z88dk library function calls.

## String Pool

**STATUS: Partially implemented - needs work**

The string pool is allocated from the heap at startup via `mb25_init()`.

Currently the pool size is fixed at compile time (2048 bytes). This should be changed to use most of available heap dynamically, like original MBASIC.

See: [DYNAMIC_STRING_POOL_TODO.md](DYNAMIC_STRING_POOL_TODO.md)

### Garbage Collection

GC uses in-place compaction:

1. Sort string descriptors by address (qsort - O(n log n))
2. Compact strings forward using memmove (handles overlaps)
3. Resort descriptors by ID
4. Reset allocator to end of compacted data

**No temporary buffer** - compaction happens in-place within the pool.

## Monitoring at Runtime

```basic
10 PRINT "String pool free:", FRE("")
```

`FRE("")` returns free space in the string pool.

## See Also

- [DYNAMIC_STRING_POOL_TODO.md](DYNAMIC_STRING_POOL_TODO.md) - Fix string pool to be dynamic
- [runtime/strings/mb25_string.c](https://github.com/avwohl/mbasic/blob/main/runtime/strings/mb25_string.c) - String system implementation
