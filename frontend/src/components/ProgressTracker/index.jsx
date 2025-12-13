import React from 'react';
import './style.css';

const ProgressTracker = ({ status, progress, onDownload, onCancel, error, filename, fileSize }) => {
    const formatSize = (bytes) => {
        if (!bytes) return 'Unknown size';
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 Byte';
        const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
        return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
    };

    const isCompleted = status === 'completed';
    const isFailed = status === 'failed';
    const isProcessing = status === 'processing' || status === 'pending';

    return (
        <div className="card progress-tracker">
            <div className="progress-tracker-header">
                <h3 className="progress-tracker-title">
                    {isCompleted ? 'Download Ready!' : isFailed ? 'Download Failed' : 'Processing...'}
                </h3>
                {isProcessing && (
                    <button
                        onClick={onCancel}
                        className="progress-tracker-cancel-btn"
                    >
                        Cancel
                    </button>
                )}
            </div>

            {isFailed ? (
                <div className="progress-tracker-error">
                    <p className="progress-tracker-error-title">Error:</p>
                    <p className="progress-tracker-error-message">{error || 'An unknown error occurred'}</p>
                </div>
            ) : (
                <div className="progress-tracker-content">
                    <div className="progress-tracker-bar-container">
                        <div
                            className={`progress-tracker-bar ${isCompleted ? 'progress-tracker-bar-completed' : 'progress-tracker-bar-processing'}`}
                            style={{ width: `${progress}%` }}
                        />
                    </div>

                    <div className="progress-tracker-info">
                        <span>{Math.round(progress)}%</span>
                        <span>{fileSize ? formatSize(fileSize) : 'Calculating size...'}</span>
                    </div>

                    {isCompleted && (
                        <div className="progress-tracker-completion">
                            <div className="progress-tracker-completion-content">
                                <div className="progress-tracker-icon-wrapper">
                                    <svg className="progress-tracker-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                    </svg>
                                </div>
                                <div className="progress-tracker-file-info">
                                    <p className="progress-tracker-filename">
                                        {filename}
                                    </p>
                                    <p className="progress-tracker-filesize">{formatSize(fileSize)}</p>
                                    <p className="progress-tracker-success-message">
                                        ✓ File downloaded to your browser's download folder
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default ProgressTracker;
