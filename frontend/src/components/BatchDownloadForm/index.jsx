import React, { useState, useEffect } from 'react';
import './style.css';

const BatchDownloadForm = ({ onSubmit, isLoading }) => {
    const [urls, setUrls] = useState('');
    const [downloadType, setDownloadType] = useState('video');
    const [format, setFormat] = useState('mp4');
    const [resolution, setResolution] = useState('best');
    const [audioBitrate, setAudioBitrate] = useState('128k');
    const [urlList, setUrlList] = useState([]);
    const [validationErrors, setValidationErrors] = useState([]);

    // Parse URLs whenever the textarea changes
    useEffect(() => {
        const lines = urls.split('\n').filter(line => line.trim() !== '');
        const parsed = lines.map((line, index) => {
            const url = line.trim();
            const isValid = validateYouTubeUrl(url);
            return { url, isValid, index };
        });
        setUrlList(parsed);

        // Check for duplicates
        const urlSet = new Set();
        const errors = [];
        parsed.forEach((item, idx) => {
            if (!item.isValid) {
                errors.push(`Line ${idx + 1}: Invalid YouTube URL`);
            } else if (urlSet.has(item.url)) {
                errors.push(`Line ${idx + 1}: Duplicate URL`);
            } else {
                urlSet.add(item.url);
            }
        });
        setValidationErrors(errors);
    }, [urls]);

    const validateYouTubeUrl = (url) => {
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/;
        return pattern.test(url);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const validUrls = urlList.filter(item => item.isValid).map(item => item.url);
        const uniqueUrls = [...new Set(validUrls)];

        if (uniqueUrls.length === 0) {
            return;
        }

        if (uniqueUrls.length > 10) {
            alert('Maximum 10 videos allowed per batch');
            return;
        }

        const params = {
            urls: uniqueUrls,
            type: downloadType,
            format: format,
            resolution: downloadType === 'video' ? resolution : undefined,
            audio_bitrate: downloadType === 'audio' ? audioBitrate : undefined
        };

        onSubmit(params);
    };

    const handleRemoveUrl = (index) => {
        const lines = urls.split('\n');
        lines.splice(index, 1);
        setUrls(lines.join('\n'));
    };

    const validCount = urlList.filter(item => item.isValid).length;
    const uniqueCount = new Set(urlList.filter(item => item.isValid).map(item => item.url)).size;
    const duplicateCount = validCount - uniqueCount;

    return (
        <div className="card batch-download-form">
            <form onSubmit={handleSubmit}>
                <div className="form-header">
                    <h2 className="form-title">📦 Batch Download</h2>
                    <p className="form-subtitle">Download multiple videos at once (max 10)</p>
                </div>

                <div className="form-group">
                    <label className="form-label">
                        YouTube URLs (one per line)
                    </label>
                    <textarea
                        className="batch-url-input"
                        value={urls}
                        onChange={(e) => setUrls(e.target.value)}
                        placeholder="https://youtube.com/watch?v=...&#10;https://youtube.com/watch?v=...&#10;https://youtube.com/watch?v=..."
                        rows={6}
                        disabled={isLoading}
                    />

                    {urlList.length > 0 && (
                        <div className="url-stats">
                            <span className={validCount > 0 ? 'stat-valid' : 'stat-invalid'}>
                                ✓ {uniqueCount} valid URL{uniqueCount !== 1 ? 's' : ''}
                            </span>
                            {duplicateCount > 0 && (
                                <span className="stat-warning">
                                    ⚠ {duplicateCount} duplicate{duplicateCount !== 1 ? 's' : ''}
                                </span>
                            )}
                            {validationErrors.length > 0 && (
                                <span className="stat-error">
                                    ✗ {validationErrors.length} error{validationErrors.length !== 1 ? 's' : ''}
                                </span>
                            )}
                        </div>
                    )}

                    {validationErrors.length > 0 && (
                        <div className="validation-errors">
                            {validationErrors.slice(0, 3).map((error, idx) => (
                                <div key={idx} className="error-message">{error}</div>
                            ))}
                            {validationErrors.length > 3 && (
                                <div className="error-message">
                                    ... and {validationErrors.length - 3} more error{validationErrors.length - 3 !== 1 ? 's' : ''}
                                </div>
                            )}
                        </div>
                    )}
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label className="form-label">Download Type</label>
                        <select
                            className="input-field"
                            value={downloadType}
                            onChange={(e) => {
                                setDownloadType(e.target.value);
                                if (e.target.value === 'audio') {
                                    setFormat('mp3');
                                } else {
                                    setFormat('mp4');
                                }
                            }}
                            disabled={isLoading}
                        >
                            <option value="video">Video</option>
                            <option value="audio">Audio Only</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="form-label">Format</label>
                        <select
                            className="input-field"
                            value={format}
                            onChange={(e) => setFormat(e.target.value)}
                            disabled={isLoading}
                        >
                            {downloadType === 'audio' ? (
                                <>
                                    <option value="mp3">MP3</option>
                                    <option value="m4a">M4A</option>
                                </>
                            ) : (
                                <>
                                    <option value="mp4">MP4</option>
                                    <option value="mkv">MKV</option>
                                </>
                            )}
                        </select>
                    </div>
                </div>

                {downloadType === 'video' && (
                    <div className="form-group">
                        <label className="form-label">Video Quality</label>
                        <select
                            className="input-field"
                            value={resolution}
                            onChange={(e) => setResolution(e.target.value)}
                            disabled={isLoading}
                        >
                            <option value="best">Best Available</option>
                            <option value="1080">1080p</option>
                            <option value="720">720p</option>
                            <option value="480">480p</option>
                        </select>
                    </div>
                )}

                {downloadType === 'audio' && (
                    <div className="form-group">
                        <label className="form-label">Audio Quality</label>
                        <select
                            className="input-field"
                            value={audioBitrate}
                            onChange={(e) => setAudioBitrate(e.target.value)}
                            disabled={isLoading}
                        >
                            <option value="128k">Standard (128kbps)</option>
                            <option value="192k">High (192kbps)</option>
                            <option value="256k">Very High (256kbps)</option>
                            <option value="320k">Maximum (320kbps)</option>
                        </select>
                    </div>
                )}

                <button
                    type="submit"
                    className="btn-primary batch-submit-btn"
                    disabled={isLoading || uniqueCount === 0 || uniqueCount > 10 || validationErrors.length > 0}
                >
                    {isLoading ? (
                        <>⏳ Processing...</>
                    ) : (
                        <>⬇️ Download All ({uniqueCount} video{uniqueCount !== 1 ? 's' : ''})</>
                    )}
                </button>
            </form>
        </div>
    );
};

export default BatchDownloadForm;
