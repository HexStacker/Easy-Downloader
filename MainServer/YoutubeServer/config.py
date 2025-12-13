"""
YouTube Server Configuration
"""

import os
from pathlib import Path

class YoutubeConfig:
    """Configuration for YouTube download service"""
    
    # Download settings
    TEMP_DIR = os.getenv('YOUTUBE_TEMP_DIR', './temp')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 500 * 1024 * 1024))  # 500MB default
    
    # yt-dlp settings
    YT_DLP_OPTIONS = {
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
        'format': 'best',
    }
    
    # Rate limiting
    MAX_CONCURRENT_DOWNLOADS = int(os.getenv('MAX_CONCURRENT_DOWNLOADS', 3))
    RATE_LIMIT = os.getenv('RATE_LIMIT', '1M')  # 1MB/s default
    
    # Timeout settings
    DOWNLOAD_TIMEOUT = int(os.getenv('DOWNLOAD_TIMEOUT', 300))  # 5 minutes
    
    @staticmethod
    def init_app():
        """Initialize application directories"""
        Path(YoutubeConfig.TEMP_DIR).mkdir(parents=True, exist_ok=True)
