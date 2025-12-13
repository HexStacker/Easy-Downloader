# Update Summary: Version 2.5.2 - Error Handling & Stability

**Date:** 2025-12-13
**Version:** 2.5.2
**Component:** Backend

## Changes
- **Backend (`service.py`)**: Updated `yt-dlp` configuration to include stability flags: `nocheckcertificate`, `ignoreerrors: False`, `geo_bypass`, and `noplaylist`.
- **Frontend (`App.jsx`)**: Improved error handling to correctly display error messages returned by the backend, helping users identify why a download failed.
- **Backend (`app.py`)**: Bumped version to 2.5.2.

## Reason
- To resolve potential 500 "Internal Server Error" issues caused by SSL validation failures or geo-blocking in strict server environments like Railway.
- To surface the actual underlying error to the user interface for better debugging.
