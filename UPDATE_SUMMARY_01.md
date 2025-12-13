# Update Summary: Frontend Railway Integration

**Date:** 2025-12-13
**Component:** Frontend

## Changes
- Updated `api.js` to use the deployed Railway backend URL (`https://easy-downloader.up.railway.app/api`) as the default API endpoint.
- This ensures the local frontend development server connects to the production backend instead of failing on localhost.

## Impact
- Resolves `ERR_CONNECTION_REFUSED` errors when trying to download videos from the local frontend.
- Enables full functionality of the frontend without running a local backend instance.
