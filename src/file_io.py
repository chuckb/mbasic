"""
File I/O abstraction for MBASIC interpreter.

Provides sandboxed file operations for different UI contexts:
- RealFileIO: Direct filesystem access (TK, Curses, CLI)
- SandboxedFileIO: Browser localStorage (Web UI)
"""

from typing import List, Tuple
from abc import ABC, abstractmethod


class FileIO(ABC):
    """Abstract interface for file operations.

    Different UIs provide different implementations:
    - Local UIs (TK/Curses/CLI): RealFileIO (direct filesystem)
    - Web UI: SandboxedFileIO (browser localStorage)
    """

    @abstractmethod
    def list_files(self, filespec: str = "") -> List[Tuple[str, int, bool]]:
        """List files matching filespec pattern.

        Args:
            filespec: File pattern (e.g., "*.BAS", "*.txt")
                     Empty string means "*" (all files)

        Returns:
            List of (filename, size_bytes, is_dir) tuples
            size_bytes may be None if size cannot be determined
        """
        pass

    @abstractmethod
    def load_file(self, filename: str) -> str:
        """Load file contents.

        Args:
            filename: Name of file to load

        Returns:
            File contents as string

        Raises:
            FileNotFoundError: File does not exist
            IOError: File cannot be read
        """
        pass

    @abstractmethod
    def save_file(self, filename: str, content: str) -> None:
        """Save file contents.

        Args:
            filename: Name of file to save
            content: File contents to write

        Raises:
            IOError: File cannot be written
        """
        pass

    @abstractmethod
    def delete_file(self, filename: str) -> None:
        """Delete a file.

        Args:
            filename: Name of file to delete

        Raises:
            FileNotFoundError: File does not exist
        """
        pass

    @abstractmethod
    def file_exists(self, filename: str) -> bool:
        """Check if file exists.

        Args:
            filename: Name of file to check

        Returns:
            True if file exists, False otherwise
        """
        pass


class RealFileIO(FileIO):
    """Real filesystem access for local UIs (TK, Curses, CLI).

    Uses Python's standard file operations to access the local filesystem.
    Users can read/write files in their current working directory.
    """

    def list_files(self, filespec: str = "") -> List[Tuple[str, int, bool]]:
        """List files in local filesystem matching pattern."""
        import glob
        import os

        # Default pattern if no argument
        pattern = filespec.strip().strip('"').strip("'") if filespec else "*"
        if not pattern:
            pattern = "*"

        # Get matching files
        files = sorted(glob.glob(pattern))

        # Build result list
        result = []
        for filename in files:
            try:
                if os.path.isdir(filename):
                    result.append((filename, None, True))
                elif os.path.isfile(filename):
                    size = os.path.getsize(filename)
                    result.append((filename, size, False))
                else:
                    result.append((filename, None, False))
            except OSError:
                result.append((filename, None, False))

        return result

    def load_file(self, filename: str) -> str:
        """Load file from local filesystem."""
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

    def save_file(self, filename: str, content: str) -> None:
        """Save file to local filesystem."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    def delete_file(self, filename: str) -> None:
        """Delete file from local filesystem."""
        import os
        os.remove(filename)

    def file_exists(self, filename: str) -> bool:
        """Check if file exists in local filesystem."""
        import os
        return os.path.exists(filename)


class SandboxedFileIO(FileIO):
    """Sandboxed file operations for web UI.

    Uses browser localStorage for file storage.
    Files are stored per-user session with 'mbasic_file_' prefix.
    No access to server filesystem - all files are client-side only.
    """

    def __init__(self, backend):
        """Initialize sandboxed file I/O.

        Args:
            backend: NiceGUIBackend instance for JavaScript execution
        """
        self.backend = backend

    def list_files(self, filespec: str = "") -> List[Tuple[str, int, bool]]:
        """List files in browser localStorage.

        Returns list of files stored in this user's session.
        Pattern matching is done client-side.
        """
        import fnmatch

        pattern = filespec.strip().strip('"').strip("'") if filespec else "*"
        if not pattern:
            pattern = "*"

        # Get all files from localStorage via JavaScript
        try:
            # Use ui.run_javascript to execute in browser
            from nicegui import ui
            files_json = ui.run_javascript('''
                (() => {
                    const files = [];
                    for (let i = 0; i < localStorage.length; i++) {
                        const key = localStorage.key(i);
                        if (key.startsWith('mbasic_file_')) {
                            const filename = key.substring(12);  // Remove 'mbasic_file_' prefix
                            const content = localStorage.getItem(key);
                            files.push({
                                name: filename,
                                size: content ? content.length : 0
                            });
                        }
                    }
                    return files;
                })()
            ''', timeout=5.0)

            # Filter by pattern
            result = []
            if files_json:
                for file_info in files_json:
                    filename = file_info['name']
                    if fnmatch.fnmatch(filename, pattern):
                        result.append((filename, file_info['size'], False))

            return sorted(result)

        except Exception:
            # If JavaScript fails, return empty list
            return []

    def load_file(self, filename: str) -> str:
        """Load file from browser localStorage."""
        from nicegui import ui

        try:
            content = ui.run_javascript(f'''
                localStorage.getItem('mbasic_file_{filename}')
            ''', timeout=5.0)

            if content is None:
                raise FileNotFoundError(f"File not found: {filename}")

            return content

        except Exception as e:
            if "not found" in str(e).lower():
                raise FileNotFoundError(f"File not found: {filename}")
            raise IOError(f"Error loading file: {e}")

    def save_file(self, filename: str, content: str) -> None:
        """Save file to browser localStorage."""
        from nicegui import ui

        try:
            # Escape content for JavaScript
            escaped_content = content.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')

            ui.run_javascript(f'''
                localStorage.setItem('mbasic_file_{filename}', '{escaped_content}')
            ''', timeout=5.0)

        except Exception as e:
            raise IOError(f"Error saving file: {e}")

    def delete_file(self, filename: str) -> None:
        """Delete file from browser localStorage."""
        from nicegui import ui

        try:
            if not self.file_exists(filename):
                raise FileNotFoundError(f"File not found: {filename}")

            ui.run_javascript(f'''
                localStorage.removeItem('mbasic_file_{filename}')
            ''', timeout=5.0)

        except Exception as e:
            if "not found" in str(e).lower():
                raise
            raise IOError(f"Error deleting file: {e}")

    def file_exists(self, filename: str) -> bool:
        """Check if file exists in browser localStorage."""
        from nicegui import ui

        try:
            exists = ui.run_javascript(f'''
                localStorage.getItem('mbasic_file_{filename}') !== null
            ''', timeout=5.0)
            return bool(exists)

        except Exception:
            return False
