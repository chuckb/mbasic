# Variable Export API Simplification - Summary

## What Changed

The variable export API has been simplified from 3 methods to 1 method.

### Before (3 methods)

1. **`get_all_variables()`** - Returned simple dict `{name: value}`
2. **`get_variables_by_recent_access()`** - Returned list of dicts sorted by access time
3. **`get_variables_detailed()`** - Returned list of dicts with full info

### After (1 method)

**`get_all_variables()`** - Returns list of dicts with complete variable information

## API Changes

### Method Signature

```python
runtime.get_all_variables()  # No parameters
```

Returns:
```python
[
  {
    'name': 'x',              # Base name without suffix
    'type_suffix': '%',       # $, %, !, or #
    'is_array': False,
    'value': 42,
    'last_read': {...},       # Always included
    'last_write': {...}       # Always included
  },
  ...
]
```

### Key Changes

1. **Deleted Methods**:
   - `get_variables_by_recent_access()` - DELETED
   - Old simple `get_all_variables()` - DELETED

2. **Renamed Method**:
   - `get_variables_detailed()` → `get_all_variables()`

3. **Removed Concept**:
   - No more "metadata" terminology
   - No more `include_metadata` parameters
   - Tracking info (last_read, last_write) is now always included as direct fields

4. **Updated `update_variables()`**:
   - Now accepts list of dicts (from `get_all_variables()`)
   - Previously accepted simple dict `{name: value}`

## Benefits

1. **Simpler**: Only one method to learn and use
2. **Consistent**: Always returns the same format
3. **Complete**: Always includes all information including tracking
4. **Flexible**: UI can sort/filter the list however it wants

## Migration Guide

### Old Code

```python
# Get simple values
values = runtime.get_all_variables()  # Returns dict

# Get with metadata
vars = runtime.get_variables_detailed(include_metadata=True)
for v in vars:
    metadata = v['metadata']  # Nested structure
    last_read = metadata['last_read']

# Get sorted by recent access
recent = runtime.get_variables_by_recent_access(include_metadata=True)
```

### New Code

```python
# Get all variable information (includes tracking)
vars = runtime.get_all_variables()  # Returns list

# Access tracking info directly
for v in vars:
    last_read = v['last_read']  # Direct access, no 'metadata' key

# Sort however you want
by_recent = sorted(vars,
                  key=lambda v: max(
                      v['last_read']['timestamp'] if v['last_read'] else 0,
                      v['last_write']['timestamp'] if v['last_write'] else 0
                  ),
                  reverse=True)
```

## Files Updated

### Source Code
- `src/runtime.py`:
  - Deleted `get_variables_by_recent_access()` (lines 366-424)
  - Deleted old `get_all_variables()` (lines 729-755)
  - Renamed `get_variables_detailed()` to `get_all_variables()`
  - Updated `update_variables()` to accept new format

### Tests
- `tests/test_no_metadata.py` - Updated to test simplified API
- `tests/test_debugger_set.py` - Updated to use new API
- `tests/test_what_is_returned.py` - Simplified to show single method
- `tests/test_metadata.py` - Updated terminology (metadata → tracking)
- `tests/test_export_api.py` - Updated to use new API
- `tests/test_variable_tracking.py` - Updated to use new API
- `tests/test_final_api.py` - NEW: Demonstrates final API

### Documentation
- `tests/VARIABLE_EXPORT_API.md` - Updated to document single method
- `tests/API_SIMPLIFICATION_SUMMARY.md` - NEW: This file

## Verification

All tests pass:
```bash
cd tests
python3 test_no_metadata.py       # ✓ PASS
python3 test_debugger_set.py      # ✓ PASS
python3 test_export_api.py        # ✓ PASS
python3 test_metadata.py          # ✓ PASS
python3 test_final_api.py         # ✓ PASS
```

No lingering references to old methods in src directory.
