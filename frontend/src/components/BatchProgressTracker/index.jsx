import React, { useState } from 'react';
import './style.css';

const BatchProgressTracker = ({ batchStatus, onDownload, onCancel, onDownloadIndividual }) => {
    const [isExpanded, setIsExpanded] = useState(true);

    if (!batchStatus) return null;

    const {
        batch_id,
        total_count,
        completed_count,
        failed_count,
        processing_count,
        pending_count,
        overall_progress,
        status,
        jobs
    } = batchStatus;

    const isCompleted = status === 'completed';
    const isFailed = status === 'failed';
    const isProcessing = status === 'processing' || status === 'pending';

    const formatSize = (bytes) => {
        if (!bytes) return 'Unknown size';
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 Byte';
        const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
        return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
    };

    const getStatusIcon = (jobStatus) => {
        switch (jobStatus) {
            case 'completed':
                return '✅';
            case 'failed':
                return '❌';
            case 'processing':
                return '⏳';
            case 'pending':
                return '⏸️';
            default:
                return '⏸️';
        }
    };

    const getStatusColor = (jobStatus) => {
        switch (jobStatus) {
            case 'completed':
                return 'job-completed';
            case 'failed':
                return 'job-failed';
            case 'processing':
                return 'job-processing';
            case 'pending':
                return 'job-pending';
            default:
                return 'job-pending';
        }
    };

    return (
        <div className="card batch-progress-tracker">
            <div className="batch-header">
                <h3 className="batch-title">
                    {isCompleted ? '📦 Batch Complete!' : isFailed ? '📦 Batch Failed' : '📦 Batch Processing...'}
                </h3>
                {isProcessing && (
                    <button
                        onClick={onCancel}
                        className="batch-cancel-btn"
                    >
                        Cancel All
                    </button>
                )}
            </div>

            {/* Overall Progress */}
            <div className="batch-overall-progress">
                <div className="progress-header">
                    <span className="progress-label">Overall Progress</span>
                    <span className="progress-percentage">{Math.round(overall_progress)}%</span>
                </div>
                <div className="batch-progress-bar-container">
                    <div
                        className={`batch-progress-bar ${isCompleted ? 'batch-progress-bar-completed' : 'batch-progress-bar-processing'}`}
                        style={{ width: `${overall_progress}%` }}
                    />
                </div>
                <div className="batch-stats">
                    <span className="stat-item stat-total">📊 Total: {total_count}</span>
                    {completed_count > 0 && <span className="stat-item stat-completed">✅ Completed: {completed_count}</span>}
                    {processing_count > 0 && <span className="stat-item stat-processing">⏳ Processing: {processing_count}</span>}
                    {pending_count > 0 && <span className="stat-item stat-pending">⏸️ Pending: {pending_count}</span>}
                    {failed_count > 0 && <span className="stat-item stat-failed">❌ Failed: {failed_count}</span>}
                </div>
            </div>

            {/* Individual Jobs */}
            <div className="batch-jobs-section">
                <button
                    className="jobs-toggle-btn"
                    onClick={() => setIsExpanded(!isExpanded)}
                >
                    <span>{isExpanded ? '▼' : '▶'} Individual Downloads ({jobs.length})</span>
                </button>

                {isExpanded && (
                    <div className="jobs-list">
                        {jobs.map((job, index) => (
                            <div key={job.job_id} className={`job-item ${getStatusColor(job.status)}`}>
                                <div className="job-icon">
                                    {getStatusIcon(job.status)}
                                </div>
                                <div className="job-info">
                                    <div className="job-title">
                                        {job.filename || `Video ${index + 1}`}
                                    </div>
                                    <div className="job-details">
                                        {job.status === 'completed' && (
                                            <span className="job-size">{formatSize(job.file_size)}</span>
                                        )}
                                        {job.status === 'processing' && job.progress && (
                                            <span className="job-progress">{Math.round(job.progress)}%</span>
                                        )}
                                        {job.status === 'failed' && job.error && (
                                            <span className="job-error">{job.error}</span>
                                        )}
                                    </div>
                                </div>
                                {job.status === 'completed' && (
                                    <button
                                        className="job-download-btn"
                                        onClick={() => onDownloadIndividual(job.job_id)}
                                        title="Download this file"
                                    >
                                        ⬇️
                                    </button>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Download All Button */}
            {completed_count > 0 && (
                <div className="batch-actions">
                    <button
                        className="btn-primary batch-download-all-btn"
                        onClick={onDownload}
                    >
                        📦 Download All Completed ({completed_count} file{completed_count !== 1 ? 's' : ''})
                    </button>
                    {completed_count === total_count && (
                        <p className="batch-success-message">
                            ✓ All files ready! Click above to download each file individually.
                        </p>
                    )}
                </div>
            )}
        </div>
    );
};

export default BatchProgressTracker;
