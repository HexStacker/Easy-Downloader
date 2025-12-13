import React, { useState, useEffect } from 'react';
import './style.css';

const LegalNotice = ({ onAccept }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [hasAccepted, setHasAccepted] = useState(false);

    useEffect(() => {
        const accepted = localStorage.getItem('tos_accepted');
        if (!accepted) {
            setIsOpen(true);
        } else {
            setHasAccepted(true);
            onAccept();
        }
    }, [onAccept]);

    const handleAccept = () => {
        localStorage.setItem('tos_accepted', 'true');
        setIsOpen(false);
        setHasAccepted(true);
        onAccept();
    };

    if (!isOpen) return null;

    return (
        <div className="legal-notice-overlay">
            <div className="legal-notice-modal">
                <div className="legal-notice-header">
                    <div className="legal-notice-icon-wrapper">
                        <svg className="legal-notice-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                    </div>
                    <h3 className="legal-notice-title">Legal Notice & Terms of Service</h3>
                </div>

                <div className="legal-notice-content">
                    <p>
                        This system must comply with YouTube's Terms of Service and all copyright laws.
                    </p>
                    <div className="legal-notice-highlight">
                        <p className="legal-notice-highlight-title">You agree to only download videos:</p>
                        <ul className="legal-notice-list">
                            <li>That you own personally</li>
                            <li>Where the uploader has given explicit permission</li>
                            <li>Where downloading is allowed by license (e.g., Creative Commons)</li>
                        </ul>
                    </div>
                    <p>
                        By proceeding, you confirm that you have the right to download the content and accept full responsibility for your actions.
                    </p>
                    <p className="legal-notice-warning">
                        ⚠️ You must accept these terms to use this service.
                    </p>
                </div>

                <div className="legal-notice-buttons">
                    <button
                        onClick={handleAccept}
                        className="legal-notice-btn legal-notice-btn-primary"
                    >
                        I Agree & Continue
                    </button>
                </div>
            </div>
        </div>
    );
};

export default LegalNotice;
