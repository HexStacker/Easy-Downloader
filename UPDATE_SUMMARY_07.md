# Update Summary: Version 2.5.3 - Enhanced Error Logging

**Date:** 2025-12-13
**Version:** 2.5.3
**Component:** Backend

## Changes
- **Backend (`routes.py`)**: Added comprehensive error logging with `logger.exception()` to capture full stack traces in Railway logs.
- **Backend (`routes.py`)**: Improved JSON validation and error response formatting.
- **Backend (`routes.py`)**: Changed response key from `download_id` to `job_id` for consistency with frontend expectations.
- **Backend (`app.py`)**: Bumped version to 2.5.3.
- **Frontend (`package.json`)**: Bumped version to 2.5.3.

## Reason
- The 500 errors are occurring but we can't see the actual error message. This update ensures all errors are properly logged to Railway's console and returned to the frontend with descriptive messages.
- Once deployed, check Railway logs to see the actual exception causing the 500 error.
