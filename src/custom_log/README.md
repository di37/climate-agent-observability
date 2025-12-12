# 📋 Custom Logging Module

## Overview

Dedicated module for application logging configuration and utilities.

## Purpose

Provides centralized logging setup for the Climate Agriculture Agent with:
- File logging (persistent)
- Console logging (real-time)
- Timestamp formatting
- Log level management

## Module Contents

### `logging_config.py`

**Function:** `setup_logging(level=logging.INFO)`

**Purpose:** Configure application-wide logging

**Features:**
- ✅ Dual output (file + console)
- ✅ Timestamped entries
- ✅ Configurable log levels
- ✅ Structured format
- ✅ Automatic log directory creation

**Usage:**
```python
from src.custom_log import setup_logging

# Setup logging
logger = setup_logging()

# Use throughout application
logger.info("Application started")
logger.warning("Potential issue")
logger.error("Error occurred")
```

## Configuration

### Log File Location

```
logs/agent.log
```

### Log Format

```
TIMESTAMP - MODULE - LEVEL - MESSAGE
2025-12-11 21:30:00 - __main__ - INFO - Application starting
```

### Log Levels

| Level | Purpose | Example |
|-------|---------|---------|
| DEBUG | Detailed info | Trace IDs, SQL queries |
| INFO | Normal flow | Query completed, scores added |
| WARNING | Non-critical issues | Prompt fetch failed |
| ERROR | Errors | Database error, API failure |

## Usage Examples

### Basic Setup

```python
from src.custom_log import setup_logging
import logging

# Configure logging
logger = setup_logging()

# Log messages
logger.info("Agent initialized")
logger.debug("Processing query...")
logger.warning("Using default prompts")
logger.error("Failed to connect")
```

### Custom Log Level

```python
import logging
from src.custom_log import setup_logging

# More verbose (development)
logger = setup_logging(level=logging.DEBUG)

# Less verbose (production)
logger = setup_logging(level=logging.WARNING)
```

### Module-Specific Loggers

```python
import logging
from src.custom_log import setup_logging

# Setup once
setup_logging()

# Get logger for specific module
logger = logging.getLogger(__name__)
logger.info("Module-specific message")
```

## Environment Variable

Control log level via environment:

```bash
# .env
LOG_LEVEL=DEBUG
```

```python
import os
import logging
from src.custom_log import setup_logging

log_level = os.getenv("LOG_LEVEL", "INFO")
setup_logging(level=getattr(logging, log_level))
```

## Log Output

### Console Output

```
2025-12-11 21:30:00 - src.agents.climate_agent - INFO - Agent initialized
2025-12-11 21:30:05 - src.agents.climate_agent - INFO - Query completed
```

### File Output

Same content saved to `logs/agent.log`:
- Persistent across runs
- Can be analyzed later
- Useful for debugging

## Integration

### Used By All Modules

```python
# main.py
from src.custom_log import setup_logging
logger = setup_logging()

# climate_agent.py
import logging
logger = logging.getLogger(__name__)
logger.info("Agent ready")

# database_tools.py
import logging
logger = logging.getLogger(__name__)
logger.debug("Executing SQL")
```

## Advanced Features

### Log Rotation (Future)

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/agent.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

### Structured Logging (Future)

```python
from pythonjsonlogger import jsonlogger

handler = logging.FileHandler('logs/agent.json')
handler.setFormatter(jsonlogger.JsonFormatter())
```

### Remote Logging (Future)

```python
# Send logs to external service
from logging.handlers import HTTPHandler

handler = HTTPHandler(
    'logs.example.com',
    '/api/logs',
    method='POST'
)
```

## Comparison

### Before (In utils/)

```
src/utils/
├── logging_config.py     ← Mixed with other utilities
├── langfuse_init.py
├── scoring.py
└── validators.py
```

### After (Dedicated folder)

```
src/custom_log/           ← Dedicated logging module
└── logging_config.py

src/utils/                ← Only validation utilities
└── validators.py

src/observability/        ← Only Langfuse functionality
├── tracing.py
├── scoring.py
└── prompts.py
```

## Benefits

✅ **Clear Organization** - Logging has its own folder  
✅ **Easy to Find** - Know where logging code lives  
✅ **Extensible** - Easy to add log utilities  
✅ **Reusable** - Copy folder to other projects  
✅ **Professional** - Proper separation of concerns  

## Summary

### Folder Purpose

**`src/custom_log/`** = Application logging functionality
- Configuration
- Setup
- Utilities

### Import

```python
from src.custom_log import setup_logging
```

### File

- `logging_config.py` (28 lines)
- Clean, focused, reusable

---

**Dedicated logging module created!** 📋✅

