import React from 'react';
import 'remixicon/fonts/remixicon.css';
import './style.css';

const SocialLink = ({ href, icon }) => (
    <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="social-link"
    >
        <i className={icon}></i>
    </a>
);

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-container">
                <div className="footer-content">
                    <div className="footer-info">
                        <p className="footer-copyright">
                            © {new Date().getFullYear()} Easy Downloader. All rights reserved.
                        </p>
                        <p className="footer-author">
                            Created by HexStacker
                        </p>
                    </div>

                    <div className="footer-social">
                        <SocialLink
                            href="https://github.com/HexStacker"
                            icon="ri-github-fill"
                        />
                        <SocialLink
                            href="https://www.linkedin.com/in/muhammad-hasan-22b56a385"
                            icon="ri-linkedin-box-fill"
                        />
                        <SocialLink
                            href="https://x.com/HexStacker"
                            icon="ri-twitter-x-fill"
                        />
                        <SocialLink
                            href="https://hexstacker.vercel.app/"
                            icon="ri-article-fill"
                        />
                        <SocialLink
                            href="mailto:hexstacker.freelance@gmail.com"
                            icon="ri-mail-fill"
                        />
                        <SocialLink
                            href="https://www.instagram.com/hex.stacker"
                            icon="ri-instagram-fill"
                        />
                        <SocialLink
                            href="https://www.youtube.com/@HexStacker"
                            icon="ri-youtube-fill"
                        />
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
