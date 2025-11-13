# Page Visits Tracking Cleanup

## Summary
Removed dead code related to `page_visits` table tracking that was never being used.

## Problem
The root URL (`/`) immediately redirects to `/ide`, so the landing page HTML that calls `/api/track-visit` was never served. This resulted in:
- `/api/track-visit` endpoint never being called
- `page_visits` MySQL table always empty
- Dead code in the codebase

## What Actually Matters
**`ide_sessions` table** is what tracks real usage and gets populated with data. The IP logging fix we deployed earlier applies to this table.

## Changes Made

### Removed from `src/ui/web/nicegui_backend.py`
Deleted the `/api/track-visit` endpoint (lines 4021-4035):
```python
# Landing page visit tracking endpoint
@app.post('/api/track-visit')
def track_visit(...):
    ...
```

### Files Not Touched
- `src/usage_tracker.py` - The `track_page_visit()` method remains in case it's useful later
- `deployment/landing-page/index.html` - Landing page HTML remains (not used but harmless)
- Database schema - `page_visits` table can be dropped manually (see below)

## Database Cleanup (Optional)

If you want to remove the unused `page_visits` table from MySQL:

```sql
-- Check if table has any data (should be empty)
SELECT COUNT(*) FROM page_visits;

-- Drop the table
DROP TABLE IF EXISTS page_visits;
```

**Note**: This is optional. The empty table doesn't hurt anything, but removing it cleans up the schema.

## What Remains Active

The following usage tracking is still active and working:
- ✅ `ide_sessions` - Tracks IDE session starts/ends with real client IPs
- ✅ `program_executions` - Tracks program runs
- ✅ `feature_usage` - Tracks feature usage

All of these use the fixed IP extraction that gets real client IPs from X-Forwarded-For header.

## Related Documents
- `docs/dev/IP_LOGGING_FIX.md` - IP address logging fix for Kubernetes
- `docs/dev/USAGE_TRACKING_INTEGRATION.md` - Original usage tracking setup (now outdated regarding page_visits)
- `DEPLOY_NOTE_IP_LOGGING_FIX.md` - Deployment note for IP fix

## Date
2025-11-13
