import React from 'react';
import './style.css';
import logo from '../../assets/logo.png';

const Docs = () => {
    return (
        <div className="docs-container">
            <div className="docs-hero">
                <img src={logo} alt="Easy Downloader Logo" className="docs-logo" />
                <h1 className="docs-title">Easy Downloader</h1>
                <p className="docs-tagline">Your Ultimate Video & Audio Download Solution</p>
            </div>

            <div className="docs-content">
                {/* About Section */}
                <section className="docs-section">
                    <h2 className="section-title">📖 About This Project</h2>
                    <div className="section-content">
                        <p>
                            <strong>Easy Downloader</strong> is a powerful, user-friendly web application designed to help you download high-quality videos and audio from various online platforms. Built with modern web technologies, it provides a seamless experience for content downloading while ensuring compliance with platform terms of service.
                        </p>
                        <p>
                            This project was created to simplify the process of downloading content for personal use, educational purposes, and offline viewing. Whether you need to save a tutorial, music video, or educational content, Easy Downloader makes it fast and easy.
                        </p>
                    </div>
                </section>

                {/* How It Works */}
                <section className="docs-section">
                    <h2 className="section-title">⚙️ How It Works</h2>
                    <div className="section-content">
                        <div className="steps-grid">
                            <div className="step-card">
                                <div className="step-number">1</div>
                                <h3>Copy URL</h3>
                                <p>Copy the video URL from YouTube or any supported platform</p>
                            </div>
                            <div className="step-card">
                                <div className="step-number">2</div>
                                <h3>Paste & Select</h3>
                                <p>Paste the URL and choose your preferred format and quality</p>
                            </div>
                            <div className="step-card">
                                <div className="step-number">3</div>
                                <h3>Download</h3>
                                <p>Click download and get your file instantly</p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Current Features */}
                <section className="docs-section">
                    <h2 className="section-title">✨ Current Features</h2>
                    <div className="section-content">
                        <div className="features-grid">
                            <div className="feature-card">
                                <div className="feature-icon">🎥</div>
                                <h3>YouTube Support</h3>
                                <p>Download videos from YouTube in multiple formats and resolutions</p>
                            </div>
                            <div className="feature-card">
                                <div className="feature-icon">🎵</div>
                                <h3>Audio Extraction</h3>
                                <p>Extract audio in MP3 or M4A format with customizable bitrates</p>
                            </div>
                            <div className="feature-card">
                                <div className="feature-icon">📱</div>
                                <h3>Responsive Design</h3>
                                <p>Works perfectly on desktop, tablet, and mobile devices</p>
                            </div>
                            <div className="feature-card">
                                <div className="feature-icon">⚡</div>
                                <h3>Fast Processing</h3>
                                <p>Quick download processing with real-time progress tracking</p>
                            </div>
                            <div className="feature-card">
                                <div className="feature-icon">🎨</div>
                                <h3>Modern UI</h3>
                                <p>Beautiful, intuitive interface with smooth animations</p>
                            </div>
                            <div className="feature-card">
                                <div className="feature-icon">🔒</div>
                                <h3>Secure & Private</h3>
                                <p>Your downloads are processed securely with no data storage</p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Future Updates */}
                <section className="docs-section docs-future">
                    <h2 className="section-title">🚀 Coming Soon - Future Updates</h2>
                    <div className="section-content">
                        <p className="future-intro">We're constantly working to improve Easy Downloader. Here's what's coming next:</p>

                        <div className="platforms-grid">
                            <div className="platform-card">
                                <div className="platform-icon">📸</div>
                                <h3>Instagram</h3>
                                <p>Download photos, videos, reels, and IGTV content</p>
                                <span className="status-badge coming-soon">Coming Soon</span>
                            </div>
                            <div className="platform-card">
                                <div className="platform-icon">👻</div>
                                <h3>Snapchat</h3>
                                <p>Save Snapchat stories and spotlight videos</p>
                                <span className="status-badge coming-soon">Coming Soon</span>
                            </div>
                            <div className="platform-card">
                                <div className="platform-icon">📘</div>
                                <h3>Facebook</h3>
                                <p>Download Facebook videos and live streams</p>
                                <span className="status-badge coming-soon">Coming Soon</span>
                            </div>
                            <div className="platform-card">
                                <div className="platform-icon">🐦</div>
                                <h3>Twitter (X)</h3>
                                <p>Save tweets with videos and GIFs</p>
                                <span className="status-badge coming-soon">Coming Soon</span>
                            </div>
                            <div className="platform-card">
                                <div className="platform-icon">💼</div>
                                <h3>LinkedIn</h3>
                                <p>Download LinkedIn videos and presentations</p>
                                <span className="status-badge coming-soon">Coming Soon</span>
                            </div>
                            <div className="platform-card">
                                <div className="platform-icon">🎵</div>
                                <h3>TikTok</h3>
                                <p>Save TikTok videos without watermark</p>
                                <span className="status-badge coming-soon">Coming Soon</span>
                            </div>
                            <div className="platform-card">
                                <div className="platform-icon">📺</div>
                                <h3>Vimeo</h3>
                                <p>Download high-quality Vimeo videos</p>
                                <span className="status-badge coming-soon">Coming Soon</span>
                            </div>
                            <div className="platform-card">
                                <div className="platform-icon">🎮</div>
                                <h3>Twitch</h3>
                                <p>Save Twitch clips and VODs</p>
                                <span className="status-badge coming-soon">Coming Soon</span>
                            </div>
                        </div>

                        <div className="additional-features">
                            <h3>Additional Features in Development:</h3>
                            <ul>
                                <li>🎬 Batch downloading - Download multiple videos at once</li>
                                <li>📋 Playlist support - Download entire playlists</li>
                                <li>🌙 Dark mode toggle - Switch between light and dark themes</li>
                                <li>📊 Download history - Track your downloaded files</li>
                                <li>🔔 Browser notifications - Get notified when downloads complete</li>
                                <li>⚙️ Advanced settings - More customization options</li>
                            </ul>
                        </div>
                    </div>
                </section>

                {/* Creator Section */}
                <section className="docs-section docs-creator">
                    <h2 className="section-title">👨‍💻 Created By</h2>
                    <div className="section-content">
                        <div className="creator-card">
                            <div className="creator-info">
                                <h3>Muhammad Hasan</h3>
                                <p className="creator-alias">@HexStacker</p>
                                <p className="creator-bio">
                                    Full-stack developer passionate about creating useful tools and applications.
                                    Specializing in modern web technologies including React, Node.js, Python, and more.
                                </p>
                            </div>
                            <div className="creator-links">
                                <h4>Connect with me:</h4>
                                <div className="social-links">
                                    <a href="https://github.com/HexStacker" target="_blank" rel="noopener noreferrer" className="social-btn">
                                        <i className="ri-github-fill"></i> GitHub
                                    </a>
                                    <a href="https://www.linkedin.com/in/muhammad-hasan-22b56a385" target="_blank" rel="noopener noreferrer" className="social-btn">
                                        <i className="ri-linkedin-box-fill"></i> LinkedIn
                                    </a>
                                    <a href="https://x.com/HexStacker" target="_blank" rel="noopener noreferrer" className="social-btn">
                                        <i className="ri-twitter-x-fill"></i> Twitter
                                    </a>
                                    <a href="https://hexstacker.vercel.app/" target="_blank" rel="noopener noreferrer" className="social-btn">
                                        <i className="ri-global-line"></i> Portfolio
                                    </a>
                                    <a href="mailto:hexstacker.freelance@gmail.com" className="social-btn">
                                        <i className="ri-mail-fill"></i> Email
                                    </a>
                                    <a href="https://www.instagram.com/hex.stacker" target="_blank" rel="noopener noreferrer" className="social-btn">
                                        <i className="ri-instagram-fill"></i> Instagram
                                    </a>
                                    <a href="https://www.youtube.com/@HexStacker" target="_blank" rel="noopener noreferrer" className="social-btn">
                                        <i className="ri-youtube-fill"></i> YouTube
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Tech Stack */}
                <section className="docs-section">
                    <h2 className="section-title">🛠️ Technology Stack</h2>
                    <div className="section-content">
                        <div className="tech-grid">
                            <div className="tech-item">
                                <h4>Frontend</h4>
                                <ul>
                                    <li>React.js</li>
                                    <li>Custom CSS</li>
                                    <li>Vite</li>
                                </ul>
                            </div>
                            <div className="tech-item">
                                <h4>Backend</h4>
                                <ul>
                                    <li>Python</li>
                                    <li>FastAPI</li>
                                    <li>yt-dlp</li>
                                </ul>
                            </div>
                            <div className="tech-item">
                                <h4>Deployment</h4>
                                <ul>
                                    <li>Vercel (Frontend)</li>
                                    <li>Railway (Backend)</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Legal Notice */}
                <section className="docs-section docs-legal">
                    <h2 className="section-title">⚖️ Legal & Compliance</h2>
                    <div className="section-content">
                        <div className="legal-notice">
                            <p>
                                <strong>Important:</strong> This tool is designed for personal use only. Users must comply with:
                            </p>
                            <ul>
                                <li>Platform Terms of Service (YouTube, etc.)</li>
                                <li>Copyright laws and regulations</li>
                                <li>Content creator rights and permissions</li>
                            </ul>
                            <p>
                                Only download content that you have the right to download, such as:
                            </p>
                            <ul>
                                <li>Content you own or created</li>
                                <li>Content with explicit permission from the creator</li>
                                <li>Content licensed under Creative Commons or similar licenses</li>
                            </ul>
                        </div>
                    </div>
                </section>

                {/* Support */}
                <section className="docs-section">
                    <h2 className="section-title">💬 Support & Feedback</h2>
                    <div className="section-content">
                        <p>
                            Have questions, suggestions, or found a bug? We'd love to hear from you!
                        </p>
                        <div className="support-options">
                            <a href="mailto:hexstacker.freelance@gmail.com" className="support-btn">
                                📧 Email Support
                            </a>
                            <a href="https://github.com/HexStacker" target="_blank" rel="noopener noreferrer" className="support-btn">
                                🐛 Report an Issue
                            </a>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default Docs;
