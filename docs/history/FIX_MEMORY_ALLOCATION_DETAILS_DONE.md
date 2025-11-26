# Fix Memory Allocation - Implementation Details

## Research Summary (completed 2025-11-23)

### Problem Statement
The current implementation uses a fixed 2048-byte string pool allocated from the heap at compile time.
Original MBASIC 5.21 allocated ALL unused space to the string pool, maximizing available memory.

### Finding 1: End of Program in z88dk

**Solution**: Use z88dk's section boundary symbols

From z88dk wiki ([CRT documentation](https://github.com/z88dk/z88dk/wiki/CRT)):
- `__BSS_tail` marks the end of the BSS section (end of program)
- `__BSS_head` marks the start of BSS section
- `__BSS_size` is the size of BSS section

In C code:
```c
extern unsigned char __BSS_tail;
/* &__BSS_tail is the first free byte after the program */
```

### Finding 2: File Buffer Sizes in Original MBASIC 5.21

From `docs/history/original_mbasic_src/dcpm.mac`:

**File Data Block Structure:**
```
Offset   Size   Description
------   ----   -----------
0        1      File mode (0=closed, 1=seq input, 2=seq output, 3=random)
1        33     FCB (CP/M File Control Block)
34       2      locofs - current location (sectors read/written)
36       1      ornofs - bytes originally in buffer
37       1-2    nmlofs - bytes left / print position
38       1-2    (padding/2nd block space for other systems)
41       128    datofs - sector buffer (datpsc = 128 bytes)
------
Total: 169 bytes for SEQUENTIAL files

For RANDOM files, add:
169      2      fd.siz - variable record size (default 128)
171      2      fd.phy - current physical record #
173      2      fd.log - current logical record #
175      1      fd.chg - change flag
176      2      fd.ops - output print position
178      N      fd.dat - field buffer (size = fd.siz, default 128)
------
Total: ~306 bytes for RANDOM files (with 128-byte records)
```

**Recommendation**: Reserve ~256 bytes per sequential file, ~384 bytes per random file.
Conservative default: 512 bytes per file (handles mixed usage).

### Finding 3: z88dk Heap Allocation

When using `-DAMALLOC`:
- Heap size is automatically calculated at runtime
- Approximately 75% of TPA (Transient Program Area) goes to heap
- TPA = space between program load point (0x0100) and BDOS

**Clarification on "75% of TPA":**
Looking at the z88dk source, `-DAMALLOC` allocates a heap that starts after BSS and grows toward the stack.
The "75%" is approximate and depends on system configuration. The key point is heap is dynamically sized.

## Implementation Plan

### New Configuration Variables

Add to `codegen_backend.py` config:

```python
# Memory configuration
self.outer_heap_pad = self.config.get('outer_heap_pad', 1024)  # Safety margin before stack
self.max_open_files = self.config.get('max_open_files', 5)     # Expected open files
self.file_buffer_size = self.config.get('file_buffer_size', 512)  # Bytes per file
self.inner_heap_pad = self.config.get('inner_heap_pad', 256)   # General heap padding
```

### Option A: Dynamic String Pool at Runtime (Recommended)

Modify `mb25_init()` to accept 0 as "use available heap".

**Heap Size Calculation:**
```
heap_size = SP - outer_pad - stack_size - __BSS_tail
```

Where:
- **SP** = current stack pointer at startup
- **outer_pad** = safety margin (config, default 1024)
- **stack_size** = configured stack size (config, default 512)
- **__BSS_tail** = end of program (z88dk section boundary symbol)

**String Pool Size Calculation:**

**TESTED: z88dk FCBs are statically allocated in BSS, not heap!**

From [z88dk cpm.h](https://github.com/z88dk/z88dk/blob/master/include/cpm.h):
- Each FCB is 176 bytes (36-byte FCB + 7-byte library extension + 133-byte cache with 128-byte sector buffer)
- FCBs are allocated as static array: `struct fcb _fcb[MAXFILES]`
- This array is in BSS section, so `__BSS_tail` already accounts for it

Therefore:
```
heap_size = SP - outer_pad - stack_size - __BSS_tail
string_pool_size = heap_size - malloc_overhead
```

Where:
- **malloc_overhead** = ~20 bytes (for malloc's internal block header/linking)

All heap can go to strings since file buffers are already in BSS (counted in `__BSS_tail`).

**mb25_string.c changes:**
```c
extern unsigned char __BSS_tail;  /* z88dk section boundary */

mb25_error_t mb25_init(uint16_t pool_size) {
    if (pool_size == 0) {
        /* Calculate heap size (use unsigned to avoid overflow):
         * heap_size = SP - outer_pad - stack_size - &__BSS_tail
         */
        uint16_t sp;
        __asm__("ld hl, 0\n add hl, sp" : "=r"(sp));  /* Get current SP */

        uint16_t outer_pad = 1024;   /* Safety margin before stack */
        uint16_t stack_size = 512;   /* Reserved for C library stack */
        uint16_t program_end = (uint16_t)&__BSS_tail;

        /* All arithmetic with unsigned to prevent signed overflow */
        uint16_t heap_size = sp - outer_pad - stack_size - program_end;

        /* FCBs are in BSS (static array), so no need to reserve for file I/O */
        /* Subtract malloc overhead for block header */
        uint16_t malloc_overhead = 20;
        pool_size = heap_size - malloc_overhead;

        /* Sanity check - if calculation went negative (wrapped), use fallback */
        if (pool_size < 1024) {
            pool_size = 2048;  /* Fallback to safe default */
        }
    }

    /* Rest of existing init code... */
}
```

**codegen_backend.py changes:**
```python
# Pass 0 to mb25_init for dynamic sizing
code.append(self.indent() + 'if (mb25_init(0) != MB25_SUCCESS) {')
```

### Memory Layout Diagram

```
CP/M Memory Map with Dynamic String Pool:

0x0000 ┌─────────────────────────┐
       │  System Page (256 bytes)│
0x0100 ├─────────────────────────┤ TPA Start
       │  Program Code           │
       │  (from .COM file)       │
       ├─────────────────────────┤
       │  Static Variables       │
       │  String Descriptors     │
       │  GOSUB Stack array      │
       │  FCB array (176 bytes   │ ← File buffers are HERE (in BSS)
       │   × MAXFILES)           │   not in heap!
       ├─────────────────────────┤ __BSS_tail
       │                         │
       │  ┌─────────────────────┐│
       │  │ String Pool         ││ ← heap_size bytes
       │  │ (via malloc)        ││   All heap goes to strings
       │  └─────────────────────┘│
       │                         │
       │  outer_pad (1024)       │ ← Safety margin
       │  stack_size (512)       │ ← Reserved for C stack
       ├─────────────────────────┤ SP (Stack Pointer at startup)
       │  Stack (grows down)     │
       ├─────────────────────────┤ BDOS entry (from 0x0006)
       │  BDOS                   │
       └─────────────────────────┘

heap_size = SP - outer_pad - stack_size - __BSS_tail
string_pool_size = heap_size
```

## Files to Modify

1. **runtime/strings/mb25_string.c**
   - Add `extern unsigned char __BSS_tail;`
   - Modify `mb25_init()` to handle pool_size=0

2. **runtime/strings/mb25_string.h**
   - Update documentation for mb25_init()

3. **src/codegen_backend.py**
   - Add new config variables
   - Change mb25_init call to pass 0 (or computed value)

4. **docs/dev/COMPILER_MEMORY_CONFIG.md**
   - Update documentation

5. **docs/dev/DYNAMIC_STRING_POOL_TODO.md**
   - Mark as completed (or move to history)

## Testing Plan

1. Create test program that prints FRE("") before/after file operations
2. Test on different "CP/M" memory sizes (16K, 32K, 48K, 64K)
3. Verify string operations work with large string pool
4. Test edge cases: very small systems, many open files

## Related Documentation

- [STRING_ALLOCATION_AND_GARBAGE_COLLECTION.md](compiler_optimizations/STRING_ALLOCATION_AND_GARBAGE_COLLECTION.md)
- [DYNAMIC_STRING_POOL_DONE.md](DYNAMIC_STRING_POOL_DONE.md)
- [COMPILER_MEMORY_CONFIG.md](../dev/COMPILER_MEMORY_CONFIG.md)
- z88dk wiki: https://github.com/z88dk/z88dk/wiki/CRT
- CP/M file handling in original source: `docs/history/original_mbasic_src/dcpm.mac`
