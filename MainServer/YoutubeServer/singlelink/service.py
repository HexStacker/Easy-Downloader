"""
Single Link Service
Business logic for single video downloads
"""

import os
import uuid
import yt_dlp
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SingleLinkService:
    """Service for handling single video downloads"""
    
    def __init__(self):
        self.downloads = {}  # In-memory storage, will be replaced with DB
        self.temp_dir = Path('./temp/singlelink')
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def get_video_info(self, url):
        """
        Extract video information without downloading
        
        Args:
            url: YouTube video URL
            
        Returns:
            dict: Video information including title, duration, formats, etc.
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Extract relevant information
                return {
                    'success': True,
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader'),
                    'view_count': info.get('view_count'),
                    'upload_date': info.get('upload_date'),
                    'description': info.get('description', '')[:500],  # First 500 chars
                    'formats': self._extract_formats(info.get('formats', []))
                }
                
        except Exception as e:
            logger.error(f"Error extracting video info: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _extract_formats(self, formats):
        """Extract and organize available formats"""
        video_formats = []
        audio_formats = []
        
        for fmt in formats:
            if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                # Combined video+audio format
                video_formats.append({
                    'format_id': fmt.get('format_id'),
                    'ext': fmt.get('ext'),
                    'quality': fmt.get('format_note', 'unknown'),
                    'filesize': fmt.get('filesize'),
                    'resolution': f"{fmt.get('width')}x{fmt.get('height')}" if fmt.get('width') else None
                })
            elif fmt.get('acodec') != 'none':
                # Audio only
                audio_formats.append({
                    'format_id': fmt.get('format_id'),
                    'ext': fmt.get('ext'),
                    'quality': fmt.get('format_note', 'unknown'),
                    'filesize': fmt.get('filesize'),
                    'abr': fmt.get('abr')
                })
        
        return {
            'video': video_formats[:10],  # Top 10 video formats
            'audio': audio_formats[:5]     # Top 5 audio formats
        }
    
    def download_video(self, url, format_type='mp4', quality='best'):
        """
        Download a video
        
        Args:
            url: YouTube video URL
            format_type: 'mp4' or 'mp3'
            quality: 'best', '720p', '1080p', etc.
            
        Returns:
            dict: Download information including download_id
        """
        try:
            download_id = str(uuid.uuid4())
            output_path = self.temp_dir / download_id
            output_path.mkdir(exist_ok=True)
            
            # Configure yt-dlp options based on format
            if format_type == 'mp3':
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                    'quiet': False,
                }
            else:
                # Video format
                format_selector = self._get_format_selector(quality)
                ydl_opts = {
                    'format': format_selector,
                    'outtmpl': str(output_path / '%(title)s.%(ext)s'),
                    'quiet': False,
                }
            
            # Store download info
            self.downloads[download_id] = {
                'id': download_id,
                'url': url,
                'format': format_type,
                'quality': quality,
                'status': 'downloading',
                'progress': 0,
                'created_at': datetime.now().isoformat(),
                'output_path': str(output_path)
            }
            
            # Start download (in production, this should be async/background task)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                self.downloads[download_id].update({
                    'status': 'completed',
                    'progress': 100,
                    'filename': os.path.basename(filename),
                    'file_path': filename,
                    'title': info.get('title')
                })
            
            return {
                'success': True,
                'download_id': download_id
            }
            
        except Exception as e:
            logger.error(f"Error downloading video: {str(e)}")
            if download_id in self.downloads:
                self.downloads[download_id]['status'] = 'failed'
                self.downloads[download_id]['error'] = str(e)
            return {'success': False, 'error': str(e)}
    
    def _get_format_selector(self, quality):
        """Get yt-dlp format selector based on quality"""
        quality_map = {
            'best': 'bestvideo+bestaudio/best',
            '2160p': 'bestvideo[height<=2160]+bestaudio/best',
            '1440p': 'bestvideo[height<=1440]+bestaudio/best',
            '1080p': 'bestvideo[height<=1080]+bestaudio/best',
            '720p': 'bestvideo[height<=720]+bestaudio/best',
            '480p': 'bestvideo[height<=480]+bestaudio/best',
            '360p': 'bestvideo[height<=360]+bestaudio/best',
        }
        return quality_map.get(quality, 'bestvideo+bestaudio/best')
    
    def get_download_status(self, download_id):
        """Get download status by ID"""
        if download_id not in self.downloads:
            return {'error': 'Download not found'}
        
        return self.downloads[download_id]
    
    def get_file_path(self, download_id):
        """Get file path for completed download"""
        if download_id not in self.downloads:
            raise FileNotFoundError('Download not found')
        
        download = self.downloads[download_id]
        
        if download['status'] != 'completed':
            raise FileNotFoundError('Download not completed')
        
        file_path = download.get('file_path')
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError('File not found')
        
        return file_path
