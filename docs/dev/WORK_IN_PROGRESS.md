# Work in Progress

No active work in progress.

## Recently Completed

### PC (Program Counter) Refactoring (v1.0.276-283)
✅ **COMPLETE** - Hardware-inspired PC/NPC design implemented
- Replaced scattered 4-variable position tracking with clean PC objects
- Simplified execution loop (320 lines → 160 lines)
- Enabled statement-level breakpoints and trace
- Removed all legacy code (tick_old, deprecated fields)
- Documented cached state fields for UI compatibility

See `docs/dev/PC_REFACTORING_COMPLETE.md` for full details.

### Web UI Improvements (v1.0.265-274)
✅ **COMPLETE** - All sizing, scrolling, and notification issues resolved
- Fixed textarea sizing using Quasar rows property
- Fixed auto-scroll to bottom of output pane
- Unified notification system (all popups logged to output)
- Fixed immediate mode runtime errors

Both projects tested and committed. No pending work.
