# Web UI Output Area Improvements

## Status: ⏳ TODO

## Issues

### 1. Output Should Auto-Scroll to Bottom
**Status:** ⏳ TODO
**Priority:** HIGH

**Problem:** When program produces output, the output textarea doesn't automatically scroll to show the latest output. User has to manually scroll down.

**Solution:**
- When appending output, automatically scroll the textarea to bottom
- NiceGUI textarea can be scrolled programmatically
- Add after `self.output.value += text` in `_append_output()`

**Implementation:**
```python
def _append_output(self, text):
    """Append text to output pane."""
    self.output.value += text
    # Auto-scroll to bottom
    # Need to use JavaScript or NiceGUI method to scroll
```

**Files to Modify:**
- `src/ui/web/nicegui_backend.py` - `_append_output()` method

---

### 2. Output Buffer Limiting
**Status:** ⏳ TODO
**Priority:** MEDIUM

**Problem:** Output area can grow indefinitely, causing browser memory issues and slow performance with long-running programs.

**Solution:**
- Keep only last N lines in output buffer (configurable)
- Default: 2000-3000 lines
- When buffer exceeds limit, remove oldest lines
- Store in settings/config

**Implementation:**
```python
class NiceGUIBackend:
    def __init__(self, ...):
        self.output_max_lines = 3000  # Default, should come from config

    def _append_output(self, text):
        """Append text to output pane with buffer limiting."""
        self.output.value += text

        # Limit buffer size
        lines = self.output.value.split('\n')
        if len(lines) > self.output_max_lines:
            # Keep last N lines
            lines = lines[-self.output_max_lines:]
            self.output.value = '\n'.join(lines)
            # Optionally show indicator that old output was trimmed
            if not self.output.value.startswith('[... output truncated ...]\n'):
                self.output.value = '[... output truncated ...]\n' + self.output.value

        # Auto-scroll to bottom
        # ...
```

**Configuration:**
- Add to Settings dialog (when implemented)
- Setting: "Output Buffer Lines" (default: 3000)
- Minimum: 100
- Maximum: 10000

**Files to Modify:**
- `src/ui/web/nicegui_backend.py` - `_append_output()` method
- Settings dialog (when created)

---

### 3. Log Errors to stderr
**Status:** ⏳ TODO
**Priority:** HIGH

**Problem:** Errors in the web UI are only shown in the browser, not logged to terminal/stderr. Makes debugging difficult when user reports issues.

**Solution:**
- Wrap all menu handlers and critical methods with try/except
- Log exceptions to stderr using `sys.stderr.write()` or logging module
- Include traceback for debugging
- Still show error in web UI, but also log it

**Implementation:**
```python
import sys
import traceback

def _menu_run(self):
    """Run > Run Program - Execute program."""
    try:
        # ... existing code ...
    except Exception as e:
        error_msg = f"Error in _menu_run: {e}"

        # Log to stderr
        sys.stderr.write(f"\n{'='*70}\n")
        sys.stderr.write(f"WEB UI ERROR: {error_msg}\n")
        sys.stderr.write(f"{'='*70}\n")
        traceback.print_exc(file=sys.stderr)
        sys.stderr.write(f"{'='*70}\n\n")
        sys.stderr.flush()

        # Show in UI
        ui.notify(f'Error: {e}', type='negative')
        self._set_status(f'Error: {e}')
```

**Files to Modify:**
- `src/ui/web/nicegui_backend.py` - All menu handlers and critical methods
- Consider creating a decorator: `@log_errors_to_stderr`

---

### 4. Better Web Browser Emulator for Testing
**Status:** ⏳ TODO - Research Needed
**Priority:** MEDIUM

**Problem:** Current testing uses NiceGUI's `user` fixture which has limitations (async deadlock with INPUT). Need better web testing that allows full browser simulation.

**Current State:**
- NiceGUI testing: Fast, pure Python, but limited (no real browser)
- Async deadlock prevents testing INPUT statements
- 6/7 tests passing, 1 skipped

**Research Options:**

**Option 1: Playwright** (Recommended)
- Full browser automation (Chromium, Firefox, WebKit)
- Python API
- Fast, modern, well-maintained
- Supports async/await
- Can handle complex interactions
- Installation: `pip install playwright && playwright install`

**Option 2: Selenium**
- Industry standard
- Full browser control
- Slower than Playwright
- More setup required
- Installation: `pip install selenium`

**Option 3: Puppeteer (via pyppeteer)**
- Chrome/Chromium only
- Python port of Node Puppeteer
- Good for headless testing
- Installation: `pip install pyppeteer`

**Option 4: Keep NiceGUI Testing + Manual Tests**
- Current approach
- Fast automated tests for basic functionality
- Manual testing for complex features (INPUT, file operations)
- Document manual test procedures

**Recommendation:**
- Start with **Option 1 (Playwright)**
- Create parallel test suite in `tests/playwright/`
- Keep existing NiceGUI tests for fast smoke testing
- Use Playwright for full integration tests including INPUT

**Implementation Plan:**
1. Install Playwright: `pip install playwright pytest-playwright`
2. Initialize browsers: `playwright install`
3. Create `tests/playwright/test_web_ui_integration.py`
4. Write tests for INPUT and other interactive features
5. Update CI/CD to run both test suites

**Files to Create:**
- `tests/playwright/test_web_ui_integration.py`
- `tests/playwright/conftest.py`
- Update `requirements.txt` with `playwright` and `pytest-playwright`

---

## Summary

### Priority Order
1. **HIGH:** Auto-scroll output to bottom
2. **HIGH:** Log errors to stderr
3. **MEDIUM:** Output buffer limiting
4. **MEDIUM:** Research and implement Playwright testing

### Implementation Time Estimates
- Auto-scroll: 30 minutes
- Error logging: 1-2 hours (all handlers)
- Buffer limiting: 1 hour
- Playwright setup: 2-3 hours (research + basic tests)

---

## Related Files
- `src/ui/web/nicegui_backend.py` - Main implementation
- `tests/nicegui/test_mbasic_web_ui.py` - Current tests
- `docs/dev/WEB_UI_MISSING_FEATURES.md` - Feature parity tracking
