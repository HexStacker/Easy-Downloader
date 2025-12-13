import React from 'react';
import './style.css';

const AlertModal = ({ isOpen, onClose, title, message, type = 'error' }) => {
    if (!isOpen) return null;

    return (
        <div className="alert-overlay" onClick={onClose}>
            <div className="alert-modal" onClick={(e) => e.stopPropagation()}>
                <div className="alert-header">
                    <div className={`alert-icon-wrapper ${type}`}>
                        {type === 'error' ? (
                            <svg className="alert-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        ) : (
                            <svg className="alert-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                        )}
                    </div>
                    <h3 className="alert-title">{title}</h3>
                </div>

                <div className="alert-content">
                    <p className="alert-message">{message}</p>
                </div>

                <div className="alert-footer">
                    <button onClick={onClose} className="alert-btn">
                        OK
                    </button>
                </div>
            </div>
        </div>
    );
};

export default AlertModal;
