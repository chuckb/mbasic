# TODO: Dynamic String Pool Sizing

## Background

The compiler was partially updated to use dynamic memory sizing:

- **Heap size**: Now dynamic via `-DAMALLOC` (~75% of TPA at runtime)
- **String pool**: Still fixed at compile time (currently hardcoded to 2048 bytes)

Only part of the shift from fixed addresses to dynamic sizing got done. The string pool should also be dynamic.

## Current (Broken) Behavior

```c
// Generated code passes fixed compile-time value
mb25_init(2048);  // WRONG - should use most of available heap
```

## Intended Behavior

String pool should use most of available heap at runtime, like original MBASIC which used all free memory between program/variables and BDOS.

## Questions to Resolve

1. How should `mb25_init()` determine available heap?
   - Use `mallinfo()` if available in z88dk?
   - Probe with malloc/free to find available space?
   - Pass 0 to mean "use most of available heap"?

2. What percentage of heap should the string pool use?
   - 90%? Leave some for file I/O buffers?
   - User configurable via CLEAR command?

3. Should this match original MBASIC behavior exactly?
   - Original: string heap grew downward from MEMSIZ
   - Original: CLEAR n,m could reserve string space

## Files to Update

- `runtime/strings/mb25_string.c` - `mb25_init()` to detect/use available memory
- `src/codegen_backend.py` - Remove fixed `string_pool_size` config
- `docs/dev/COMPILER_MEMORY_CONFIG.md` - Update once fixed

## Related

- Heap detection works via z88dk's `-DAMALLOC` flag
- GOSUB uses separate `gosub_stack[100]` array, not C call stack
