"""
Playlist Service
Business logic for playlist downloads
"""

import os
import uuid
import yt_dlp
import zipfile
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)

class PlaylistService:
    """Service for handling playlist downloads"""
    
    def __init__(self):
        self.playlists = {}  # In-memory storage, will be replaced with DB
        self.temp_dir = Path('./temp/playlist')
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.max_workers = 3  # Max concurrent downloads
    
    def get_playlist_info(self, url):
        """
        Extract playlist information without downloading
        
        Args:
            url: YouTube playlist URL
            
        Returns:
            dict: Playlist information including title, video count, videos list
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,  # Don't download, just get info
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                videos = []
                for entry in info.get('entries', []):
                    if entry:
                        videos.append({
                            'id': entry.get('id'),
                            'title': entry.get('title'),
                            'duration': entry.get('duration'),
                            'url': entry.get('url') or f"https://youtube.com/watch?v={entry.get('id')}"
                        })
                
                return {
                    'success': True,
                    'title': info.get('title'),
                    'uploader': info.get('uploader'),
                    'video_count': len(videos),
                    'videos': videos
                }
                
        except Exception as e:
            logger.error(f"Error extracting playlist info: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def download_playlist(self, url, format_type='mp4', quality='best', start_index=None, end_index=None):
        """
        Download a playlist
        
        Args:
            url: YouTube playlist URL
            format_type: 'mp4' or 'mp3'
            quality: Video quality
            start_index: Start from this video index (1-based)
            end_index: End at this video index (1-based)
            
        Returns:
            dict: Playlist download information
        """
        try:
            playlist_id = str(uuid.uuid4())
            output_path = self.temp_dir / playlist_id
            output_path.mkdir(exist_ok=True)
            
            # Get playlist info first
            playlist_info = self.get_playlist_info(url)
            
            if not playlist_info.get('success'):
                return {'success': False, 'error': playlist_info.get('error')}
            
            videos = playlist_info['videos']
            
            # Apply index filtering if specified
            if start_index is not None or end_index is not None:
                start = (start_index - 1) if start_index else 0
                end = end_index if end_index else len(videos)
                videos = videos[start:end]
            
            # Initialize playlist info
            self.playlists[playlist_id] = {
                'id': playlist_id,
                'url': url,
                'title': playlist_info['title'],
                'format': format_type,
                'quality': quality,
                'status': 'pending',
                'total': len(videos),
                'completed': 0,
                'failed': 0,
                'progress': 0,
                'created_at': datetime.now().isoformat(),
                'output_path': str(output_path),
                'videos': videos,
                'downloaded_videos': []
            }
            
            # Start playlist download in background
            self._process_playlist(playlist_id)
            
            return {
                'success': True,
                'playlist_id': playlist_id,
                'total_videos': len(videos)
            }
            
        except Exception as e:
            logger.error(f"Error creating playlist download: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _process_playlist(self, playlist_id):
        """Process playlist download with concurrent workers"""
        playlist = self.playlists[playlist_id]
        playlist['status'] = 'downloading'
        
        videos = playlist['videos']
        output_path = Path(playlist['output_path'])
        
        # Download videos concurrently
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_video = {
                executor.submit(
                    self._download_single, 
                    video['url'], 
                    output_path, 
                    playlist['format'], 
                    playlist['quality'],
                    idx + 1,
                    video['title']
                ): video 
                for idx, video in enumerate(videos)
            }
            
            for future in as_completed(future_to_video):
                video = future_to_video[future]
                try:
                    result = future.result()
                    playlist['downloaded_videos'].append(result)
                    
                    if result['success']:
                        playlist['completed'] += 1
                    else:
                        playlist['failed'] += 1
                    
                    # Update progress
                    playlist['progress'] = int((playlist['completed'] + playlist['failed']) / playlist['total'] * 100)
                    
                except Exception as e:
                    logger.error(f"Error downloading video {video['title']}: {str(e)}")
                    playlist['failed'] += 1
                    playlist['downloaded_videos'].append({
                        'url': video['url'],
                        'title': video['title'],
                        'success': False,
                        'error': str(e)
                    })
        
        # Mark playlist as completed
        playlist['status'] = 'completed'
        playlist['completed_at'] = datetime.now().isoformat()
    
    def _download_single(self, url, output_path, format_type, quality, index, title):
        """Download a single video from playlist"""
        try:
            # Use index for filename ordering
            filename_prefix = f"{index:03d}_"
            
            # Configure yt-dlp options
            if format_type == 'mp3':
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': str(output_path / f'{filename_prefix}%(title)s.%(ext)s'),
                    'quiet': True,
                }
            else:
                format_selector = self._get_format_selector(quality)
                ydl_opts = {
                    'format': format_selector,
                    'outtmpl': str(output_path / f'{filename_prefix}%(title)s.%(ext)s'),
                    'quiet': True,
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                return {
                    'url': url,
                    'index': index,
                    'success': True,
                    'title': info.get('title'),
                    'filename': os.path.basename(filename),
                    'file_path': filename
                }
                
        except Exception as e:
            logger.error(f"Error downloading {title}: {str(e)}")
            return {
                'url': url,
                'index': index,
                'title': title,
                'success': False,
                'error': str(e)
            }
    
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
    
    def get_playlist_status(self, playlist_id):
        """Get playlist status by ID"""
        if playlist_id not in self.playlists:
            return {'error': 'Playlist not found'}
        
        playlist = self.playlists[playlist_id]
        
        return {
            'playlist_id': playlist_id,
            'title': playlist['title'],
            'status': playlist['status'],
            'total': playlist['total'],
            'completed': playlist['completed'],
            'failed': playlist['failed'],
            'progress': playlist['progress'],
            'created_at': playlist['created_at'],
            'completed_at': playlist.get('completed_at'),
            'videos': playlist['downloaded_videos']
        }
    
    def create_playlist_zip(self, playlist_id):
        """Create ZIP file containing all downloaded videos"""
        if playlist_id not in self.playlists:
            raise FileNotFoundError('Playlist not found')
        
        playlist = self.playlists[playlist_id]
        
        if playlist['status'] != 'completed':
            raise ValueError('Playlist download not completed')
        
        output_path = Path(playlist['output_path'])
        zip_path = output_path.parent / f'{playlist_id}.zip'
        
        # Create ZIP file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for video in playlist['downloaded_videos']:
                if video['success'] and os.path.exists(video['file_path']):
                    zipf.write(video['file_path'], arcname=video['filename'])
        
        return str(zip_path)
    
    def cancel_playlist(self, playlist_id):
        """Cancel a playlist download"""
        if playlist_id not in self.playlists:
            return {'error': 'Playlist not found'}
        
        playlist = self.playlists[playlist_id]
        
        if playlist['status'] == 'completed':
            return {'error': 'Playlist already completed'}
        
        playlist['status'] = 'cancelled'
        playlist['cancelled_at'] = datetime.now().isoformat()
        
        return {
            'success': True,
            'message': 'Playlist download cancelled'
        }
