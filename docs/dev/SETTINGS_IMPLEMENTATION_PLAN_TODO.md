# Settings Implementation Plan - TODO

⏳ **Status:** TODO
**Priority:** HIGH (User-requested feature)
**Created:** 2025-10-30

## Overview

Implement Settings Dialog/UI in all clients to allow users to customize preferences, particularly auto-numbering settings (start at 10 vs 100, increment by 10 vs 100).

## Background

**Current Status:**
- ✅ Settings infrastructure exists (`src/settings.py`, `src/settings_definitions.py`)
- ✅ TK has settings dialog (`src/ui/tk_settings_dialog.py`)
- ✅ Curses has settings widget (`src/ui/curses_settings_widget.py`)
- ❌ Web UI has no settings access (CRITICAL - user requested)
- ❌ CLI has no SETSETTING/SHOWSETTINGS commands
- ❌ Visual UI has no settings (not yet developed)

**User Request:**
> "Some people like to start at 10, some 100, some increment by 10 some 100"

Currently Web UI hardcodes these values in `nicegui_backend.py:138-141`.

## Implementation Plan

### Phase 1: Web UI Settings Dialog (HIGH PRIORITY)

**Goal:** Allow Web UI users to configure auto-numbering preferences

#### 1.1 Create Settings Dialog Component
- **File:** `src/ui/web/web_settings_dialog.py`
- **UI:** NiceGUI modal dialog
- **Sections:**
  - Editor Settings
    - ☑ Enable auto-numbering
    - Starting line number [10]
    - Line number increment [10]
  - Resource Limits (view-only for now)
- **Buttons:** Cancel, Save

#### 1.2 Connect to Settings System
- Replace hardcoded values in `nicegui_backend.py:138-141`
- Load from `SettingsManager`
- Save to browser localStorage or settings file
- Sync between tabs if possible

#### 1.3 Add Menu Item
- File → Settings or Edit → Preferences
- Keyboard shortcut (consider Ctrl+,)

#### 1.4 Testing
- [ ] Dialog opens
- [ ] Settings load from storage
- [ ] Settings save correctly
- [ ] Auto-numbering respects settings
- [ ] Settings persist across page reload

**Estimated Effort:** 3-4 hours

---

### Phase 2: CLI Settings Commands (MEDIUM PRIORITY)

**Goal:** Allow CLI users to view and modify settings

#### 2.1 SHOWSETTINGS Command
```basic
Ok
SHOWSETTINGS
editor.auto_number = True
editor.auto_number_step = 10
limits.max_variables = 1000
...

Ok
SHOWSETTINGS editor
editor.auto_number = True
editor.auto_number_step = 10
```

- **Syntax:** `SHOWSETTINGS [filter]`
- **Filter:** Optional prefix (e.g., "editor", "limits")
- **Output:** Key = Value pairs

#### 2.2 SETSETTING Command
```basic
Ok
SETSETTING editor.auto_number_step 100
Setting updated: editor.auto_number_step = 100

Ok
SETSETTING invalid.key value
Error: Unknown setting 'invalid.key'
```

- **Syntax:** `SETSETTING key value`
- **Validation:** Use `settings_definitions.py` validation
- **Errors:** Clear error messages for invalid keys/values

#### 2.3 Add to CLI Help
- Update `docs/help/ui/cli/` documentation
- Add SHOWSETTINGS and SETSETTING to command list

#### 2.4 Testing
- [ ] SHOWSETTINGS displays all settings
- [ ] SHOWSETTINGS filter works
- [ ] SETSETTING updates values
- [ ] SETSETTING validates input
- [ ] Settings persist across CLI restart
- [ ] HELP SHOWSETTINGS works
- [ ] HELP SETSETTING works

**Estimated Effort:** 2-3 hours

---

### Phase 3: Curses UI Settings Enhancement (LOW PRIORITY)

**Goal:** Ensure Curses settings widget is complete

#### 3.1 Audit Existing Widget
- Review `src/ui/curses_settings_widget.py`
- Check if all settings from `settings_definitions.py` are accessible
- Verify auto-numbering settings work

#### 3.2 Add Missing Settings
- If any settings missing from widget, add them
- Group logically (Editor, Limits, Help, etc.)

#### 3.3 Games Library Menu Item
- Curses currently missing Games Library feature
- Add Ctrl+G or similar to open games library in browser
- (Or implement text-mode games browser)

#### 3.4 Testing
- [ ] Settings widget opens
- [ ] All settings editable
- [ ] Settings save/load correctly
- [ ] Help integration works

**Estimated Effort:** 1-2 hours

---

### Phase 4: Testing Infrastructure (HIGH PRIORITY)

**Goal:** Automated tests for settings in all UIs

#### 4.1 Settings Test Suite
Create `tests/regression/ui/test_settings.py`:
- Test settings dialog/UI opens in each UI
- Test settings load defaults
- Test settings save and persist
- Test settings affect behavior (auto-numbering)
- Test invalid values rejected

#### 4.2 Manual Test Procedures
Create `tests/manual/test_settings_manual.md`:
- Step-by-step testing for each UI
- Expected results
- Edge cases (invalid input, defaults, etc.)

#### 4.3 Update Feature Tracking
- Mark settings as tested in `UI_FEATURE_PARITY_TRACKING.md`
- Add to automated test suite
- Document test coverage

**Estimated Effort:** 2-3 hours

---

### Phase 5: Documentation (MEDIUM PRIORITY)

**Goal:** User-facing documentation for settings

#### 5.1 Help Documentation
- `docs/help/ui/web/settings.md` - Web UI settings guide
- `docs/help/ui/cli/settings.md` - CLI settings commands
- `docs/help/ui/curses/settings.md` - Curses settings guide
- `docs/help/ui/tk/settings.md` - TK settings guide
- `docs/help/common/settings.md` - General settings overview

#### 5.2 Quick Reference
- Add settings section to `docs/user/QUICK_REFERENCE.md`
- List all available settings
- Common use cases (auto-numbering preferences)

#### 5.3 In-App Help
- Ensure HELP SETTINGS works in all UIs
- Context-sensitive help in settings dialogs

**Estimated Effort:** 2 hours

---

## Acceptance Criteria

### Minimum (Phase 1 + 2)
- [ ] Web UI has Settings dialog with auto-numbering preferences
- [ ] CLI has SHOWSETTINGS and SETSETTING commands
- [ ] Users can change auto-number start (10, 100, etc.)
- [ ] Users can change auto-number increment (10, 100, etc.)
- [ ] Settings persist across sessions
- [ ] Settings work correctly (auto-numbering uses new values)

### Complete (All Phases)
- [ ] All UIs have settings access
- [ ] All settings in `settings_definitions.py` are accessible
- [ ] Automated tests for settings
- [ ] Manual test procedures documented
- [ ] User documentation complete
- [ ] Feature tracking updated

## Implementation Order

**Sprint 1 (Week 1): Critical User-Facing**
1. Phase 1: Web UI Settings Dialog (3-4 hours)
2. Phase 2: CLI Settings Commands (2-3 hours)
3. Basic testing (1 hour)

**Sprint 2 (Week 2): Testing & Polish**
4. Phase 4: Testing Infrastructure (2-3 hours)
5. Phase 3: Curses Enhancement (1-2 hours)
6. Phase 5: Documentation (2 hours)

**Total Estimated Effort:** 11-15 hours

## Success Metrics

1. **User Satisfaction:**
   - User can configure auto-number start/increment without editing code
   - Settings are discoverable (menu item, help command)

2. **Code Quality:**
   - No hardcoded settings in UI code
   - All UIs use `SettingsManager`
   - Settings properly validated

3. **Testing:**
   - Settings changes tested in all UIs
   - Automated tests catch regressions
   - Manual testing documented

4. **Feature Parity:**
   - `UI_FEATURE_PARITY_TRACKING.md` shows ✅ for Settings Dialog in all UIs
   - 40/40 features tracked and implemented

## Related Documents

- `docs/dev/SETTINGS_FEATURE_GAP_ANALYSIS.md` - How gap occurred
- `docs/dev/ALL_FEATURES_CANONICAL_NAMES.txt` - Feature #30: Settings Dialog
- `src/settings.py` - Settings infrastructure
- `src/settings_definitions.py` - All setting definitions
- `src/ui/tk_settings_dialog.py` - TK reference implementation
- `src/ui/curses_settings_widget.py` - Curses reference implementation

## Notes

### Auto-Numbering Settings Details

From `src/settings_definitions.py`:
- `editor.auto_number` (bool, default True) - Enable/disable
- `editor.auto_number_step` (int, default 10) - Increment size

Common preferences:
- Classic BASIC: start=10, step=10
- Large programs: start=100, step=100
- Dense code: start=10, step=1
- Modern style: start=1000, step=10

### Settings Storage

- **TK/Curses:** File-based (`~/.mbasic/settings.json`)
- **Web UI:** Browser localStorage recommended
  - Alternative: Server-side settings (requires backend)
- **CLI:** File-based (same as TK/Curses)

### Potential Issues

1. **Web UI localStorage limits**
   - Typically 5-10MB, plenty for settings
   - Consider JSON compression if needed

2. **Settings migration**
   - If settings format changes, need migration
   - Version settings file format

3. **Scope conflicts**
   - Global vs project vs file settings
   - Document precedence clearly

---

**Created:** 2025-10-30
**Last Updated:** 2025-10-30
**Owner:** Development team
**Reviewer:** Product owner (user)
