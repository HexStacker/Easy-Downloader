import React, { useState } from 'react';
import './style.css';
import AlertModal from '../AlertModal/index';

const DownloadForm = ({ onSubmit, isLoading }) => {
    const [url, setUrl] = useState('');
    const [type, setType] = useState('GIF');
    const [format, setFormat] = useState('mp4');
    const [resolution, setResolution] = useState('best');
    const [audioBitrate, setAudioBitrate] = useState('128k');
    const [error, setError] = useState('');
    const [alertModal, setAlertModal] = useState({ isOpen: false, title: '', message: '' });

    const validateYouTubeUrl = (url) => {
        // Comprehensive YouTube URL validation
        const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/|v\/|shorts\/)|youtu\.be\/)[\w-]{11}(\S*)?$/;
        return youtubeRegex.test(url);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        // Trim whitespace
        const trimmedUrl = url.trim();

        // Check if URL is empty
        if (!trimmedUrl) {
            setError('Please enter a YouTube URL');
            setAlertModal({
                isOpen: true,
                title: 'URL Required',
                message: 'Please enter a YouTube URL to continue.'
            });
            return;
        }

        // Validate YouTube URL
        if (!validateYouTubeUrl(trimmedUrl)) {
            setError('Invalid YouTube URL. Please enter a valid YouTube video link.');
            setAlertModal({
                isOpen: true,
                title: 'Invalid YouTube URL',
                message: 'Please enter a valid YouTube video link.\n\nAccepted formats:\n• https://www.youtube.com/watch?v=VIDEO_ID\n• https://youtu.be/VIDEO_ID\n• https://www.youtube.com/shorts/VIDEO_ID\n• https://www.youtube.com/embed/VIDEO_ID'
            });
            return;
        }

        onSubmit({
            url: trimmedUrl,
            type: type === 'GIF' ? 'video' : type === 'video' ? 'both' : type,
            format,
            resolution: type === 'audio' ? undefined : resolution,
            audio_bitrate: type === 'GIF' ? undefined : audioBitrate
        });
    };

    // Update format options when type changes
    const handleTypeChange = (newType) => {
        setType(newType);
        if (newType === 'audio') {
            setFormat('mp3');
        } else {
            setFormat('mp4');
        }
    };

    return (
        <div className="card download-form-container">
            <form onSubmit={handleSubmit} className="download-form">
                <div className="form-group">
                    <label htmlFor="url" className="form-label">
                        YouTube URL
                    </label>
                    <div className="input-wrapper">
                        <input
                            type="text"
                            id="url"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            placeholder="https://www.youtube.com/watch?v=..."
                            className="input-field url-input"
                            disabled={isLoading}
                        />
                        <div className="input-icon">
                            <svg fill="currentColor" viewBox="0 0 24 24">
                                <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z" />
                            </svg>
                        </div>
                    </div>
                    {error && <p className="error-message">{error}</p>}
                </div>

                <div className="form-grid">
                    <div className="form-group">
                        <label className="form-label">
                            Download Type
                        </label>
                        <div className="type-selector">
                            {['GIF', 'audio', 'video'].map((t) => (
                                <button
                                    key={t}
                                    type="button"
                                    onClick={() => handleTypeChange(t)}
                                    className={`type-button ${type === t ? 'active' : ''}`}
                                    disabled={isLoading}
                                >
                                    {t.charAt(0).toUpperCase() + t.slice(1)}
                                </button>
                            ))}
                        </div>
                    </div>

                    <div className="form-group">
                        <label htmlFor="format" className="form-label">
                            Format
                        </label>
                        <select
                            id="format"
                            value={format}
                            onChange={(e) => setFormat(e.target.value)}
                            className="input-field"
                            disabled={isLoading}
                        >
                            {type === 'audio' ? (
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

                {type !== 'audio' && (
                    <div className="form-group">
                        <label htmlFor="resolution" className="form-label">
                            Video Resolution
                        </label>
                        <select
                            id="resolution"
                            value={resolution}
                            onChange={(e) => setResolution(e.target.value)}
                            className="input-field"
                            disabled={isLoading}
                        >
                            <option value="best">Best Available</option>
                            <option value="1080">1080p</option>
                            <option value="720">720p</option>
                            <option value="480">480p</option>
                        </select>
                    </div>
                )}

                {type !== 'GIF' && (
                    <div className="form-group">
                        <label htmlFor="bitrate" className="form-label">
                            Audio Quality
                        </label>
                        <select
                            id="bitrate"
                            value={audioBitrate}
                            onChange={(e) => setAudioBitrate(e.target.value)}
                            className="input-field"
                            disabled={isLoading}
                        >
                            <option value="320k">High (320kbps)</option>
                            <option value="192k">Medium (192kbps)</option>
                            <option value="128k">Standard (128kbps)</option>
                        </select>
                    </div>
                )}

                <button
                    type="submit"
                    disabled={isLoading}
                    className={`btn-primary submit-button ${isLoading ? 'loading' : ''}`}
                >
                    {isLoading ? (
                        <>
                            <svg className="spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="spinner-circle" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="spinner-path" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Starting Download...
                        </>
                    ) : (
                        <>
                            <svg className="download-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                            </svg>
                            Download Now
                        </>
                    )}
                </button>
            </form>

            <AlertModal
                isOpen={alertModal.isOpen}
                onClose={() => setAlertModal({ isOpen: false, title: '', message: '' })}
                title={alertModal.title}
                message={alertModal.message}
                type="error"
            />
        </div>
    );
};

export default DownloadForm;

