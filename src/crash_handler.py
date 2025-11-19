"""Global crash handler for MBASIC web UI.

Catches uncaught exceptions and logs them to MySQL before process termination.
This ensures all crashes are logged even if they bypass normal error handling.
"""

import sys
import traceback
from typing import Optional


def setup_crash_handler():
    """Install global exception hook to log crashes to MySQL.

    This catches any uncaught exception that would normally crash the process
    and logs it to the database before allowing the process to terminate.
    """

    def crash_exception_handler(exc_type, exc_value, exc_traceback):
        """Global exception handler for uncaught exceptions.

        Args:
            exc_type: Exception type
            exc_value: Exception instance
            exc_traceback: Traceback object
        """
        # Don't log KeyboardInterrupt (Ctrl+C)
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # Log to stderr immediately
        sys.stderr.write("\n" + "="*70 + "\n")
        sys.stderr.write("FATAL: UNCAUGHT EXCEPTION - PROCESS WILL CRASH\n")
        sys.stderr.write("="*70 + "\n")
        sys.stderr.write(f"Exception Type: {exc_type.__name__}\n")
        sys.stderr.write(f"Exception Value: {exc_value}\n")
        sys.stderr.write("\nStack Trace:\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)
        sys.stderr.write("="*70 + "\n")
        sys.stderr.flush()

        # Try to log to MySQL
        try:
            from src.error_logger import get_logger
            logger = get_logger()

            # Create exception instance
            exception = exc_value if exc_value else exc_type()

            # Get stack trace as string
            import io
            trace_io = io.StringIO()
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=trace_io)
            stack_trace_str = trace_io.getvalue()

            # Manually log to MySQL (bypass normal error handling)
            if logger._ensure_mysql_connection():
                try:
                    cursor = logger._mysql_connection.cursor()

                    query = """
                        INSERT INTO web_errors
                        (timestamp, session_id, error_type, is_expected, context,
                         message, stack_trace, user_agent, request_path, version)
                        VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    from src.version import VERSION
                    values = (
                        'CRASH',  # session_id
                        exc_type.__name__,  # error_type
                        False,  # is_expected
                        'GLOBAL_CRASH_HANDLER',  # context
                        str(exc_value),  # message
                        stack_trace_str,  # stack_trace
                        None,  # user_agent
                        None,  # request_path
                        VERSION  # version
                    )

                    cursor.execute(query, values)
                    cursor.close()

                    sys.stderr.write("✓ Crash logged to MySQL database\n")
                    sys.stderr.flush()

                except Exception as db_error:
                    sys.stderr.write(f"✗ Failed to log crash to MySQL: {db_error}\n")
                    sys.stderr.flush()
            else:
                sys.stderr.write("✗ MySQL connection not available for crash logging\n")
                sys.stderr.flush()

        except Exception as log_error:
            sys.stderr.write(f"✗ Error while trying to log crash: {log_error}\n")
            traceback.print_exc(file=sys.stderr)
            sys.stderr.flush()

        # Call the default exception handler to exit
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    # Install the crash handler
    sys.excepthook = crash_exception_handler
    sys.stderr.write("✓ Global crash handler installed - all crashes will be logged to MySQL\n")
    sys.stderr.flush()
