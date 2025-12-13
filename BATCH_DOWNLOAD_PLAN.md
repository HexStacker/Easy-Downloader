# Batch Download Feature - Implementation Plan

## Overview
Implement batch downloading functionality to allow users to download multiple videos at once.

## Architecture

### Backend Changes

#### 1. New Models (`backend/app/models.py`)
- `BatchDownloadRequest` - Model for batch download requests
  - `urls: List[str]` - List of YouTube URLs
  - `type: DownloadType` - Download type for all videos
  - `format: Optional[str]` - Output format
  - `resolution: Optional[Resolution]` - Video resolution
  - `audio_bitrate: Optional[str]` - Audio bitrate

- `BatchJobResponse` - Response for batch job creation
  - `batch_id: str` - Unique batch identifier
  - `job_ids: List[str]` - Individual job IDs
  - `total_count: int` - Total number of videos
  - `status: JobStatus` - Overall batch status

- `BatchStatusResponse` - Batch status response
  - `batch_id: str`
  - `total_count: int`
  - `completed_count: int`
  - `failed_count: int`
  - `processing_count: int`
  - `jobs: List[StatusResponse]` - Individual job statuses
  - `overall_progress: float` - Overall progress percentage

#### 2. New Routes (`backend/app/api/routes.py`)
- `POST /api/batch/download` - Create batch download job
- `GET /api/batch/status/{batch_id}` - Get batch status
- `GET /api/batch/download/{batch_id}` - Download all completed files as ZIP
- `POST /api/batch/cleanup/{batch_id}` - Clean up batch job

#### 3. Batch Manager Service (`backend/app/services/batch_manager.py`)
- Track batch jobs and their individual downloads
- Aggregate status from multiple jobs
- Handle batch-level operations
- Create ZIP archives for completed batches

### Frontend Changes

#### 1. New Component: `BatchDownloadForm` (`frontend/src/components/BatchDownloadForm/`)
- Text area for multiple URLs (one per line)
- URL validation and duplicate detection
- Shared settings for all videos (type, format, quality)
- Visual URL list with remove option
- Batch size limit (e.g., max 10 videos)

#### 2. New Component: `BatchProgressTracker` (`frontend/src/components/BatchProgressTracker/`)
- Overall batch progress bar
- Individual progress for each video
- Expandable/collapsible video list
- Success/failure indicators per video
- Download all button when complete
- Individual download buttons for each video

#### 3. Updated `App.jsx`
- Add batch mode toggle
- Switch between single and batch download forms
- Handle batch job tracking
- Manage multiple progress trackers

#### 4. Updated API Service (`frontend/src/services/api.js`)
- `initiateBatchDownload(urls, params)` - Start batch download
- `getBatchStatus(batchId)` - Get batch status
- `downloadBatch(batchId)` - Download ZIP of all files
- `cleanupBatch(batchId)` - Clean up batch

## Implementation Steps

### Phase 1: Backend Foundation
1. ✅ Create new models for batch operations
2. ✅ Implement BatchManager service
3. ✅ Add batch API routes
4. ✅ Add ZIP creation functionality
5. ✅ Update rate limiting for batch requests

### Phase 2: Frontend UI
1. ✅ Create BatchDownloadForm component
2. ✅ Create BatchProgressTracker component
3. ✅ Add batch mode toggle in App.jsx
4. ✅ Update API service with batch methods

### Phase 3: Integration & Testing
1. ✅ Test batch download flow
2. ✅ Test error handling
3. ✅ Test ZIP download
4. ✅ Test cleanup
5. ✅ Responsive design testing

### Phase 4: Polish
1. ✅ Add animations and transitions
2. ✅ Improve error messages
3. ✅ Add helpful tooltips
4. ✅ Update documentation

## Features

### User Experience
- **URL Input**: Paste multiple URLs (one per line) or upload text file
- **Validation**: Real-time URL validation with error highlighting
- **Duplicate Detection**: Automatically detect and remove duplicate URLs
- **Batch Limit**: Maximum 10 videos per batch (configurable)
- **Progress Tracking**: 
  - Overall batch progress
  - Individual video progress
  - Success/failure indicators
- **Download Options**:
  - Download all as ZIP
  - Download individual files
  - Retry failed downloads

### Technical Features
- **Concurrent Processing**: Process multiple downloads simultaneously (respecting rate limits)
- **Error Handling**: Continue batch even if individual downloads fail
- **Resource Management**: Automatic cleanup of temporary files
- **ZIP Compression**: Efficient ZIP creation for completed batches
- **Progress Streaming**: Real-time progress updates via polling

## Constraints & Limits

- **Max URLs per batch**: 10 (to prevent abuse)
- **Rate Limiting**: Batch requests count as multiple requests
- **Concurrent Downloads**: Max 2 per IP (existing limit)
- **File Size**: Individual file size limits still apply
- **Storage**: Temporary storage for batch files (auto-cleanup after 1 hour)

## UI/UX Design

### Batch Download Form
```
┌─────────────────────────────────────────┐
│  📋 Batch Download                      │
│                                         │
│  Paste YouTube URLs (one per line):    │
│  ┌─────────────────────────────────┐   │
│  │ https://youtube.com/watch?v=... │   │
│  │ https://youtube.com/watch?v=... │   │
│  │ https://youtube.com/watch?v=... │   │
│  └─────────────────────────────────┘   │
│  📊 3 valid URLs • 0 duplicates         │
│                                         │
│  Download Type: [Video ▼]               │
│  Format: [MP4 ▼]                        │
│  Quality: [Best ▼]                      │
│                                         │
│  [⬇️ Download All (3 videos)]           │
└─────────────────────────────────────────┘
```

### Batch Progress Tracker
```
┌─────────────────────────────────────────┐
│  📦 Batch Download Progress             │
│                                         │
│  Overall: ████████░░ 75% (3/4)         │
│                                         │
│  ▼ Individual Downloads:                │
│  ✅ Video 1.mp4 - 12 MB                 │
│  ✅ Video 2.mp4 - 8 MB                  │
│  ⏳ Video 3.mp4 - 45%                   │
│  ❌ Video 4.mp4 - Failed                │
│                                         │
│  [📦 Download All as ZIP]               │
└─────────────────────────────────────────┘
```

## Next Steps

1. Start with backend implementation (models, services, routes)
2. Create frontend components
3. Integrate and test
4. Polish UI/UX
5. Update documentation

## Notes

- Keep single download functionality intact
- Make batch download an optional feature (toggle)
- Ensure backward compatibility
- Add proper error handling and user feedback
- Consider adding batch download history
