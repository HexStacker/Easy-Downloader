import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import DownloadForm from './components/DownloadForm/index';
import ProgressTracker from './components/ProgressTracker/index';
import BatchDownloadForm from './components/BatchDownloadForm/index';
import BatchProgressTracker from './components/BatchProgressTracker/index';
import LegalNotice from './components/LegalNotice/index';
import Docs from './components/Docs/index';
import Footer from './components/Footer/index';
import { downloadService } from './services/api';
import logo from './assets/logo.png';

function App() {
    const [activeTab, setActiveTab] = useState('downloader');
    const [downloadMode, setDownloadMode] = useState('single'); // 'single' or 'batch'

    // Single download state
    const [jobId, setJobId] = useState(null);
    const [status, setStatus] = useState(null);
    const [progress, setProgress] = useState(0);
    const [fileInfo, setFileInfo] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const eventSourceRef = useRef(null);

    // Batch download state
    const [batchId, setBatchId] = useState(null);
    const [batchStatus, setBatchStatus] = useState(null);
    const [isBatchLoading, setIsBatchLoading] = useState(false);
    const batchPollRef = useRef(null);

    // Cleanup on unmount
    useEffect(() => {
        return () => {
            if (eventSourceRef.current) {
                eventSourceRef.current.close();
            }
            if (batchPollRef.current) {
                clearInterval(batchPollRef.current);
            }
        };
    }, []);

    // Single Download Handlers
    const handleDownloadSubmit = async (params) => {
        try {
            setIsLoading(true);
            setError(null);
            setStatus('pending');
            setProgress(0);
            setFileInfo(null);

            const response = await downloadService.initiateDownload(params);
            setJobId(response.job_id);
            startProgressTracking(response.job_id);
        } catch (err) {
            console.error('Download failed:', err);
            setError(err.response?.data?.detail || 'Failed to start download. Please try again.');
            setStatus('failed');
            setIsLoading(false);
        }
    };

    const startProgressTracking = (id) => {
        const pollInterval = setInterval(async () => {
            try {
                const data = await downloadService.getStatus(id);
                setStatus(data.status);

                if (data.progress) {
                    setProgress(data.progress);
                }

                if (data.status === 'completed') {
                    setFileInfo({
                        filename: data.filename,
                        size: data.file_size
                    });
                    setProgress(100);
                    setIsLoading(false);
                    clearInterval(pollInterval);

                    setTimeout(() => {
                        handleDownloadFile(id);
                    }, 500);
                } else if (data.status === 'failed') {
                    setError(data.error || 'Download failed');
                    setIsLoading(false);
                    clearInterval(pollInterval);
                }
            } catch (e) {
                console.error('Error fetching status:', e);
            }
        }, 1000);

        eventSourceRef.current = { close: () => clearInterval(pollInterval) };
    };

    const handleDownloadFile = (id = jobId) => {
        if (id) {
            const downloadUrl = downloadService.getDownloadUrl(id);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = '';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    };

    const handleCancel = async () => {
        if (jobId) {
            try {
                await downloadService.cleanupJob(jobId);
            } catch (e) {
                console.error('Cleanup error:', e);
            }
        }

        if (eventSourceRef.current) {
            eventSourceRef.current.close();
        }

        setJobId(null);
        setStatus(null);
        setProgress(0);
        setFileInfo(null);
        setIsLoading(false);
    };

    // Batch Download Handlers
    const handleBatchDownloadSubmit = async (params) => {
        try {
            setIsBatchLoading(true);
            setBatchStatus(null);

            const response = await downloadService.initiateBatchDownload(params);
            setBatchId(response.batch_id);
            startBatchProgressTracking(response.batch_id);
        } catch (err) {
            console.error('Batch download failed:', err);
            alert(err.response?.data?.detail || 'Failed to start batch download. Please try again.');
            setIsBatchLoading(false);
        }
    };

    const startBatchProgressTracking = (id) => {
        const pollInterval = setInterval(async () => {
            try {
                const data = await downloadService.getBatchStatus(id);
                setBatchStatus(data);

                if (data.status === 'completed' || data.status === 'failed') {
                    setIsBatchLoading(false);
                    clearInterval(pollInterval);
                }
            } catch (e) {
                console.error('Error fetching batch status:', e);
            }
        }, 1000);

        batchPollRef.current = pollInterval;
    };

    const handleBatchDownload = () => {
        // Download all completed files individually
        if (batchStatus && batchStatus.jobs) {
            batchStatus.jobs.forEach(job => {
                if (job.status === 'completed') {
                    setTimeout(() => {
                        handleDownloadFile(job.job_id);
                    }, 500);
                }
            });
        }
    };

    const handleBatchCancel = async () => {
        if (batchId) {
            try {
                await downloadService.cleanupBatch(batchId);
            } catch (e) {
                console.error('Batch cleanup error:', e);
            }
        }

        if (batchPollRef.current) {
            clearInterval(batchPollRef.current);
        }

        setBatchId(null);
        setBatchStatus(null);
        setIsBatchLoading(false);
    };

    const handleLegalAccept = () => {
        // User accepted TOS
    };

    return (
        <div className="app-container">
            <LegalNotice onAccept={handleLegalAccept} />

            <main className="app-main">
                <div className="app-header">
                    <div className="app-icon-wrapper">
                        <img src={logo} alt="Logo" className="app-icon" />
                    </div>
                    <h1 className="app-title">
                        Easy Downloader
                    </h1>
                    <p className="app-subtitle">
                        Download Videos in high-quality. Fast, free, and secure.
                    </p>
                </div>

                {activeTab === 'downloader' ? (
                    <div className="app-content">
                        {/* Download Mode Toggle */}
                        <div className="download-mode-toggle">
                            <button
                                className={`mode-btn ${downloadMode === 'single' ? 'active' : ''}`}
                                onClick={() => setDownloadMode('single')}
                            >
                                📥 Single Download
                            </button>
                            <button
                                className={`mode-btn ${downloadMode === 'batch' ? 'active' : ''}`}
                                onClick={() => setDownloadMode('batch')}
                            >
                                📦 Batch Download
                            </button>
                        </div>

                        {/* Single Download Mode */}
                        {downloadMode === 'single' && (
                            <>
                                <DownloadForm onSubmit={handleDownloadSubmit} isLoading={isLoading && status === 'pending'} />

                                {(status || error) && (
                                    <ProgressTracker
                                        status={status}
                                        progress={progress}
                                        error={error}
                                        filename={fileInfo?.filename}
                                        fileSize={fileInfo?.size}
                                        onDownload={handleDownloadFile}
                                        onCancel={handleCancel}
                                    />
                                )}
                            </>
                        )}

                        {/* Batch Download Mode */}
                        {downloadMode === 'batch' && (
                            <>
                                <BatchDownloadForm
                                    onSubmit={handleBatchDownloadSubmit}
                                    isLoading={isBatchLoading}
                                />

                                {batchStatus && (
                                    <BatchProgressTracker
                                        batchStatus={batchStatus}
                                        onDownload={handleBatchDownload}
                                        onCancel={handleBatchCancel}
                                        onDownloadIndividual={handleDownloadFile}
                                    />
                                )}
                            </>
                        )}
                    </div>
                ) : (
                    <Docs />
                )}

                {/* Navigation Tabs */}
                <div className="app-tabs">
                    <button
                        className={`tab-button ${activeTab === 'downloader' ? 'active' : ''}`}
                        onClick={() => setActiveTab('downloader')}
                    >
                        📥 Downloader
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'docs' ? 'active' : ''}`}
                        onClick={() => setActiveTab('docs')}
                    >
                        📚 Documentation
                    </button>
                </div>
            </main>

            <Footer />
        </div>
    );
}

export default App;
