# Web UI Sandboxed Filesystem Implementation

## Issue

The web UI currently uses `RealFileSystemProvider` which allows BASIC programs to access the **real server filesystem**. This is a critical security vulnerability when the web UI is publicly accessible.

Additionally, there's no way for users to:
- Upload data files (`.dat`, `.txt`) into the sandbox for their BASIC programs to read
- Download data files created by BASIC programs back to their computer
- See what files exist in their sandbox filesystem

## Current State

### Security Problem
- Web UI creates interpreters without specifying a filesystem provider
- Interpreter defaults to `RealFileSystemProvider()` (line 107-109 in `src/interpreter.py`)
- **Any visitor can read/write files on the server!**

### Missing Features
- No file upload UI for data files
- No file download UI for sandbox files
- No file manager to view/delete sandbox files

## Sandboxed Filesystem Details

**Implementation:** `src/filesystem/sandboxed_fs.py`

**Storage:**
- Server-side in-memory Python storage (NOT browser localStorage)
- Per-user isolation via `user_id`
- Files stored in `_user_filesystems` class variable: `{user_id: {filename: content}}`

**Limits:**
- Max file size: **1 MB** (1024 * 1024 bytes) per file
- Max files: **50 files** per user
- Total: Up to **50 MB** per user session

**Features:**
- No real filesystem access
- No path traversal (`../` blocked)
- CP/M style uppercase filenames
- Optional read-only example files (shared across all users)

## Solution Required

### Part 1: Fix Security Vulnerability (CRITICAL)

1. **Create sandboxed filesystem for each web client**
   - Generate unique `user_id` per session (use NiceGUI's session ID?)
   - Create `SandboxedFileSystemProvider(user_id)` instance
   - Pass to `Interpreter()` constructor via `filesystem_provider` parameter

2. **Update all interpreter creation sites**
   - Line 1629: `self.interpreter = Interpreter(...)`
   - Line 1772: `self.interpreter = Interpreter(...)`
   - Line 1824: `self.interpreter = Interpreter(...)`
   - Line 2557: `interpreter = Interpreter(...)`

   Add: `filesystem_provider=self.sandboxed_fs` or similar

3. **Store filesystem in backend instance**
   - Create `self.sandboxed_fs` in `NiceGUIBackend.__init__()`
   - Keep it alive for the client session

### Part 2: File Manager UI (Enhancement)

Add new menu item: **File > Manage Data Files**

**File Manager Dialog:**
```
┌─────────────────────────────────────────┐
│ Data File Manager                       │
├─────────────────────────────────────────┤
│                                         │
│ Upload File:  [Choose File] [Upload]   │
│                                         │
│ Files in Sandbox:                       │
│ ┌─────────────────────────────────────┐ │
│ │ Filename       Size      Actions    │ │
│ │ DATA.TXT       1.2 KB    Download   │ │
│ │ SCORES.DAT     234 B     Download   │ │
│ │ OUTPUT.TXT     5.6 KB    Download   │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Storage: 3 files, 7.0 KB / 50 MB       │
│                                         │
│ [Clear All Files]         [Close]      │
└─────────────────────────────────────────┘
```

**Features:**
- **Upload**: Browse for file, upload to sandbox
- **Download**: Download individual files from sandbox
- **Delete**: Remove individual files
- **Clear All**: Delete all sandbox files
- **Storage indicator**: Show files used and total capacity

### Part 3: Pre-load Example Data Files (Optional)

Use `SandboxedFileSystemProvider.add_example_file()` to provide read-only example data files:
- Sample CSV data
- Text file examples
- Game high scores
- etc.

### Part 4: User Accounts and Persistent Storage (Future Enhancement)

**Current Problem:**
- Files stored in-memory (Python process memory)
- Lost when server restarts or session expires
- Up to 50 MB per user hangs in memory
- Can't switch computers and keep files

**Solution: User Accounts with Disk-Backed Sandboxed Storage**

**Architecture:**
1. **User Authentication**
   - Simple username/password login
   - Or OAuth (Google, GitHub, etc.)
   - Session tied to authenticated user ID

2. **Disk-Backed Sandboxed Filesystem**
   - Store files on server disk: `/mbasic_data/users/{user_id}/`
   - Still sandboxed (no path traversal, chroot-like)
   - Files persist across sessions and server restarts
   - User can log in from any device and access their files

3. **Storage Structure**
   ```
   /mbasic_data/
     users/
       user_12345/
         PROGRAM.BAS
         DATA.TXT
         SCORES.DAT
       user_67890/
         GAME.BAS
         OUTPUT.TXT
   ```

4. **Security**
   - Each user's directory isolated (no access to other users)
   - Path validation prevents `../` traversal
   - Disk quotas enforce 50 MB limit per user
   - Regular cleanup of inactive accounts

5. **Benefits**
   - Files persist across sessions
   - Switch computers (same account = same files)
   - Can implement "Save workspace" feature
   - Programs and data files travel together

**Implementation Options:**

**Option A: Extend SandboxedFileSystemProvider**
- Add `storage_mode='memory'|'disk'` parameter
- Add `storage_path` for disk mode
- Keep same API, just change backing store

**Option B: New DiskSandboxedFileSystemProvider**
- Separate class for disk-backed storage
- Inherits from `FileSystemProvider`
- Cleaner separation of concerns

**Database Schema (Simple SQLite):**
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    email TEXT,
    created_at TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE user_quotas (
    user_id INTEGER PRIMARY KEY,
    storage_used INTEGER,  -- bytes
    storage_limit INTEGER, -- bytes (default 50MB)
    file_count INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

**Priority:** LOW (do after basic sandboxed FS works)

**Related:**
- Could integrate with browser localStorage for offline work
- Could add file sharing (share data files between users)
- Could add file versioning/backup

## Implementation Notes

### File Upload
```python
def _handle_file_upload(self, e):
    """Handle data file upload to sandbox."""
    content = e.content.read()  # bytes
    filename = e.name

    # Save to sandbox
    try:
        # Normalize filename (uppercase, no paths)
        normalized = self.sandboxed_fs._normalize_filename(filename)
        self.sandboxed_fs._save_file_content(normalized, content)
        self._notify(f'Uploaded {filename}', type='positive')
    except Exception as ex:
        self._notify(f'Upload failed: {ex}', type='negative')
```

### File Download
```python
def _handle_file_download(self, filename):
    """Download file from sandbox."""
    try:
        content = self.sandboxed_fs._files.get(filename)
        if content:
            ui.download(content, filename)
        else:
            self._notify(f'File not found: {filename}', type='negative')
    except Exception as ex:
        self._notify(f'Download failed: {ex}', type='negative')
```

### List Files
```python
def _list_sandbox_files(self):
    """Get list of files in sandbox."""
    files = []
    for filename, content in self.sandboxed_fs._files.items():
        size = len(content) if isinstance(content, (str, bytes)) else 0
        files.append({
            'name': filename,
            'size': size,
            'size_str': f'{size / 1024:.1f} KB' if size > 1024 else f'{size} B'
        })
    return files
```

## Testing

1. **Security test**: Verify BASIC programs cannot access server filesystem
2. **Upload test**: Upload `.txt` file, verify BASIC can read it with `OPEN "I"`
3. **Download test**: BASIC creates file with `OPEN "O"`, verify user can download it
4. **Limits test**: Try uploading file > 1 MB, verify error
5. **Limits test**: Try uploading 51st file, verify error
6. **Session isolation**: Open two browser tabs, verify separate filesystems

## Example Use Case

**User workflow:**
1. User has `SCORES.DAT` on their computer (high scores from old game)
2. User uploads `SCORES.DAT` via File Manager
3. User loads `GAME.BAS` and runs it
4. BASIC code: `OPEN "I", #1, "SCORES.DAT"` - reads uploaded file
5. Game runs, updates scores
6. BASIC code: `OPEN "O", #1, "SCORES.DAT"` - writes new scores
7. User downloads updated `SCORES.DAT` via File Manager

## Priority

**CRITICAL** - Security fix (Part 1) must be done before any public deployment

**HIGH** - File manager UI (Part 2) needed for file I/O to be useful

**LOW** - Example files (Part 3) nice-to-have

## Related Code

- `src/filesystem/sandboxed_fs.py` - Sandboxed filesystem implementation
- `src/interpreter.py:96-110` - Interpreter initialization with filesystem
- `src/ui/web/nicegui_backend.py:1629,1772,1824,2557` - Interpreter creation sites
- `src/ui/web/nicegui_backend.py:2675-2705` - Web UI startup and backend creation

## Date Created

2025-11-01
