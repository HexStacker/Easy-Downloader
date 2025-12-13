# Update Summary: Global CORS Configuration

**Date:** 2025-12-13
**Component:** Backend

## Changes
- Updated `app.py` to apply CORS to all routes (`/*`) instead of just `/api/*`.
- Configured CORS to respect the `CORS_ORIGINS` environment variable, supporting multiple origins (e.g., Vercel and Localhost).

## Reason
- A mismatch between the requested URL (missing `/api`) and the CORS policy scope caused the server to reject requests without CORS headers, masking the underlying 404 error.
- By allowing CORS globally, the frontend will now receive proper error responses (like 404 Not Found) if the URL is incorrect, instead of a generic Network Error, aiding in debugging.
- This also ensures that the Vercel deployment allows requests from its specifc domain.
