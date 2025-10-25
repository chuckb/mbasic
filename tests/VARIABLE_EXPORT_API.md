# Variable Export API

## Summary

The variable export API has been simplified to a single method: `get_all_variables()`.

This method **always includes** `last_read` and `last_write` tracking information directly with each variable. There is no "metadata" concept - the tracking info is just part of the variable.

## Available Method

### `get_all_variables()` - Complete variable information

Returns a list of dicts with complete variable information **including tracking**.

```python
[
  {
    'name': 'x',                    # Base name without suffix
    'type_suffix': '%',             # $, %, !, or #
    'is_array': False,
    'value': 42,
    'last_read': {
      'line': 20,
      'position': 5,
      'timestamp': 1234.567
    },
    'last_write': {
      'line': 10,
      'position': 4,
      'timestamp': 1234.500
    }
  },
  {
    'name': 'a',
    'type_suffix': '%',
    'is_array': True,
    'dimensions': [5, 3],
    'base': 0,
    'last_read': None,              # Arrays don't track access yet
    'last_write': None
  }
]
```

**Use case:** All variable inspection and UI display.

**Sorting:** The UI can sort the list however it wants - by name, by type, by most recent access, etc.

---

## Tracking Info Structure

Every variable includes tracking information directly:

```python
'last_read': {
  'line': <BASIC line number>,
  'position': <character position in source>,
  'timestamp': <time.perf_counter() - high precision>
} or None

'last_write': {
  'line': <BASIC line number or -1 for debugger/prompt>,
  'position': <character position or None>,
  'timestamp': <time.perf_counter()>
} or None
```

**Special values:**
- `None` - Variable never read/written
- `line: -1` in `last_write` - Set from debugger or command prompt

---

## Usage Example

```python
# Get all variables
vars = runtime.get_all_variables()

# Access tracking info directly
for v in vars:
    if not v['is_array']:
        print(f"{v['name']}{v['type_suffix']} = {v['value']}")
        if v['last_read']:
            print(f"  Last read at line {v['last_read']['line']}")
        if v['last_write']:
            print(f"  Last written at line {v['last_write']['line']}")
```

---

## Internal Storage

Variables are stored as:

```python
self._variables = {
    'x%': {
        'value': 42,
        'last_read': {'line': 20, 'position': 5, 'timestamp': 1234.567},
        'last_write': {'line': 10, 'position': 4, 'timestamp': 1234.500}
    }
}
```

**No separate metadata dict** - everything is inline with the variable.
