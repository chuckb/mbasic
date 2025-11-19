# Crash Logging and Auto-Restart Documentation

## Overview

The MBASIC web UI deployment includes comprehensive crash logging and automatic restart functionality, matching the Kubernetes cluster behavior.

## Crash Logging System

### 1. Global Crash Handler

**File**: `src/crash_handler.py`

The global crash handler catches all uncaught exceptions that would normally crash the process:

- **Installed at startup**: Automatically enabled when the web UI starts
- **Logs to MySQL**: All crashes are logged to the `web_errors` table with full stack traces
- **Logs to stderr**: Also logs to systemd journal for immediate visibility
- **Special handling**: Ignores KeyboardInterrupt (Ctrl+C) for graceful shutdown

### 2. Error Logging Module

**File**: `src/error_logger.py`

Provides structured error logging for both expected and unexpected errors:

- **Expected errors**: Syntax errors, parse errors (not logged by default)
- **Unexpected errors**: Runtime crashes, exceptions (always logged with stack traces)
- **Dual logging**: Can log to both MySQL and stderr simultaneously
- **Session tracking**: Links errors to user sessions for debugging

### 3. Database Schema

**Table**: `mbasic_logs.web_errors`

```sql
CREATE TABLE web_errors (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME(3) DEFAULT CURRENT_TIMESTAMP(3),
    session_id VARCHAR(255),
    error_type VARCHAR(100),
    is_expected BOOLEAN DEFAULT FALSE,
    context VARCHAR(500),      -- Function where error occurred
    message TEXT,              -- Error message
    stack_trace TEXT,          -- Full Python stack trace
    user_agent TEXT,
    request_path VARCHAR(500),
    version VARCHAR(50),
    created_at DATETIME(3) DEFAULT CURRENT_TIMESTAMP(3)
);
```

### 4. Configuration

**File**: `config/multiuser.json`

```json
{
  "error_logging": {
    "type": "mysql",           // "stderr", "mysql", or "both"
    "mysql": {
      "unix_socket": "/run/mysqld/mysqld.sock",
      "user": "mbasic",
      "password": "...",
      "database": "mbasic_logs",
      "table": "web_errors"
    },
    "log_expected_errors": false  // Don't log syntax errors
  }
}
```

## Auto-Restart System

### 1. Systemd Service Configuration

**File**: `/etc/systemd/system/mbasic-web.service`

```ini
[Service]
Type=simple
Restart=always           # Always restart on failure
RestartSec=10           # Wait 10 seconds before restart
StandardOutput=journal  # Log stdout to systemd journal
StandardError=journal   # Log stderr to systemd journal
```

**Restart behavior**:
- **On crash**: Service automatically restarts after 10 seconds
- **On manual stop**: Service does NOT restart (only on failure)
- **On system reboot**: Service starts automatically (enabled)

### 2. Comparison with Kubernetes

| Feature | Kubernetes | Systemd (mbasic1) |
|---------|-----------|-------------------|
| Auto-restart on crash | ✓ (restartPolicy: Always) | ✓ (Restart=always) |
| Health checks | ✓ (liveness/readiness probes) | Manual via systemctl |
| Crash logging to MySQL | ✓ (global handler) | ✓ (global handler) |
| Load balancing | ✓ (3-10 replicas) | ✗ (single instance) |
| Rolling updates | ✓ | Manual restart required |

## Viewing Crash Logs

### From MySQL

```bash
# View recent crashes
mysql -u mbasic -p mbasic_logs << 'SQL'
SELECT
    timestamp,
    error_type,
    context,
    LEFT(message, 100) as message_preview,
    version
FROM web_errors
WHERE is_expected = FALSE
ORDER BY timestamp DESC
LIMIT 20;
SQL

# View crash with full stack trace
mysql -u mbasic -p mbasic_logs << 'SQL'
SELECT
    timestamp,
    error_type,
    context,
    message,
    stack_trace
FROM web_errors
WHERE id = <error_id>;
SQL

# Count crashes by type
mysql -u mbasic -p mbasic_logs << 'SQL'
SELECT
    error_type,
    COUNT(*) as count
FROM web_errors
WHERE is_expected = FALSE
GROUP BY error_type
ORDER BY count DESC;
SQL
```

### From Systemd Journal

```bash
# View service logs in real-time
sudo journalctl -u mbasic-web -f

# View recent crashes
sudo journalctl -u mbasic-web | grep -E "FATAL|CRASH|Exception"

# View logs since last boot
sudo journalctl -u mbasic-web -b

# View logs for specific time range
sudo journalctl -u mbasic-web --since "2 hours ago"
```

## Service Management

### Status and Control

```bash
# Check service status
sudo systemctl status mbasic-web

# Restart service (for updates/config changes)
sudo systemctl restart mbasic-web

# Stop service (will NOT auto-restart)
sudo systemctl stop mbasic-web

# Start service
sudo systemctl start mbasic-web

# View service configuration
systemctl cat mbasic-web
```

### Monitoring

```bash
# Monitor service restarts
sudo systemctl status mbasic-web | grep "Active:"

# Check restart count
sudo systemctl show mbasic-web -p NRestarts

# View detailed status
sudo systemctl show mbasic-web
```

## Testing Crash Handling

### Manual Crash Test

To test that crashes are logged and the service restarts:

1. **Trigger a crash** (for testing only):
   ```bash
   # Send SIGSEGV to the process (simulates a crash)
   sudo kill -SEGV $(pgrep -f "mbasic --ui web")
   ```

2. **Check the logs**:
   ```bash
   # Check systemd detected the crash
   sudo journalctl -u mbasic-web -n 50

   # Check if service restarted
   sudo systemctl status mbasic-web

   # Check MySQL for crash log
   mysql -u mbasic -p mbasic_logs -e "SELECT * FROM web_errors ORDER BY id DESC LIMIT 1\G"
   ```

3. **Verify auto-restart**:
   ```bash
   # Service should be running again
   sudo systemctl is-active mbasic-web
   # Should output: active
   ```

## Crash Prevention Best Practices

1. **Monitor error logs regularly** to catch recurring issues
2. **Set up alerts** for crash rates exceeding threshold
3. **Review stack traces** to identify root causes
4. **Update code** to handle edge cases that cause crashes
5. **Consider rate limiting** if crashes are user-triggered

## Differences from Kubernetes Setup

### Advantages of Current Setup
- ✓ Simpler configuration and debugging
- ✓ Lower resource overhead (no container orchestration)
- ✓ Direct access to logs via journalctl
- ✓ Same crash logging to MySQL

### Kubernetes Advantages
- ✓ Automatic load balancing across multiple instances
- ✓ Health check monitoring (liveness/readiness probes)
- ✓ Automatic scaling based on load
- ✓ Zero-downtime rolling updates

## Future Enhancements

To make the systemd setup more similar to Kubernetes:

1. **Add health check monitoring**:
   - Create a systemd timer to check `/health` endpoint
   - Alert on failures

2. **Add Redis for session persistence**:
   - Prevents session loss on restart
   - Configure `NICEGUI_REDIS_URL` environment variable

3. **Add automated alerting**:
   - Send email/slack on crash
   - Integrate with monitoring system (Prometheus, etc.)

## Related Files

- `src/crash_handler.py` - Global exception handler
- `src/error_logger.py` - Error logging module
- `src/multiuser_config.py` - Configuration management
- `config/multiuser.json` - Runtime configuration
- `/etc/systemd/system/mbasic-web.service` - Service definition
