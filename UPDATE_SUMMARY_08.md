# Update Summary: Version 2.5.4 - YouTube JS Runtime Fix

**Date:** 2025-12-13
**Version:** 2.5.4
**Component:** Backend

## Changes
- **Backend (`service.py`)**: Added `extractor_args` configuration to yt-dlp to bypass JavaScript runtime requirement.
- Configured yt-dlp to use `player_client=['default', 'web']` which allows YouTube extraction without Node.js/PhantomJS.
- **Backend (`app.py`)**: Bumped version to 2.5.4.
- **Frontend (`package.json`)**: Bumped version to 2.5.4.

## Reason
- The 500 errors were caused by yt-dlp requiring a JavaScript runtime (Node.js) which isn't available in the Railway container.
- YouTube has deprecated extraction without JS runtime, but yt-dlp provides a workaround using alternative player clients.
- This fix allows downloads to work without installing additional JavaScript runtimes.

## Testing
- Tested locally with URL: `https://www.youtube.com/watch?v=8SeFSmvx3AA`
- Video title: "Modern CSS Border & Box Shadow Gradient Effect | Old vs New Design"
- Duration: 2:25
