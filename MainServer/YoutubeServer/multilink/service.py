"""
Multi Link Service
Business logic for batch video downloads
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

class MultiLinkService:
    """Service for handling multiple video downloads"""
    
    def __init__(self):
        self.batches = {}  # In-memory storage, will be replaced with DB
        self.temp_dir = Path('./temp/multilink')
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.max_workers = 3  # Max concurrent downloads
    
    def create_batch(self, urls, format_type='mp4', quality='best'):
        """
        Create a batch download job
        
        Args:
            urls: List of YouTube video URLs
            format_type: 'mp4' or 'mp3'
            quality: Video quality
            
        Returns:
            dict: Batch information including batch_id
        """
        try:
            batch_id = str(uuid.uuid4())
            output_path = self.temp_dir / batch_id
            output_path.mkdir(exist_ok=True)
            
            # Initialize batch info
            self.batches[batch_id] = {
                'id': batch_id,
                'urls': urls,
                'format': format_type,
                'quality': quality,
                'status': 'pending',
                'total': len(urls),
                'completed': 0,
                'failed': 0,
                'progress': 0,
                'created_at': datetime.now().isoformat(),
                'output_path': str(output_path),
                'videos': []
            }
            
            # Start batch download in background (in production, use Celery or similar)
            self._process_batch(batch_id)
            
            return {
                'success': True,
                'batch_id': batch_id
            }
            
        except Exception as e:
            logger.error(f"Error creating batch: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _process_batch(self, batch_id):
        """Process batch download with concurrent workers"""
        batch = self.batches[batch_id]
        batch['status'] = 'downloading'
        
        urls = batch['urls']
        output_path = Path(batch['output_path'])
        
        # Download videos concurrently
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {
                executor.submit(self._download_single, url, output_path, batch['format'], batch['quality']): url 
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    batch['videos'].append(result)
                    
                    if result['success']:
                        batch['completed'] += 1
                    else:
                        batch['failed'] += 1
                    
                    # Update progress
                    batch['progress'] = int((batch['completed'] + batch['failed']) / batch['total'] * 100)
                    
                except Exception as e:
                    logger.error(f"Error downloading {url}: {str(e)}")
                    batch['failed'] += 1
                    batch['videos'].append({
                        'url': url,
                        'success': False,
                        'error': str(e)
                    })
        
        # Mark batch as completed
        batch['status'] = 'completed'
        batch['completed_at'] = datetime.now().isoformat()
    
    def _download_single(self, url, output_path, format_type, quality):
        """Download a single video"""
        try:
            video_id = str(uuid.uuid4())[:8]
            
            # Configure yt-dlp options
            if format_type == 'mp3':
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': str(output_path / f'{video_id}_%(title)s.%(ext)s'),
                    'quiet': True,
                }
            else:
                format_selector = self._get_format_selector(quality)
                ydl_opts = {
                    'format': format_selector,
                    'outtmpl': str(output_path / f'{video_id}_%(title)s.%(ext)s'),
                    'quiet': True,
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                return {
                    'url': url,
                    'success': True,
                    'title': info.get('title'),
                    'filename': os.path.basename(filename),
                    'file_path': filename
                }
                
        except Exception as e:
            logger.error(f"Error downloading {url}: {str(e)}")
            return {
                'url': url,
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
    
    def get_batch_status(self, batch_id):
        """Get batch status by ID"""
        if batch_id not in self.batches:
            return {'error': 'Batch not found'}
        
        batch = self.batches[batch_id]
        
        return {
            'batch_id': batch_id,
            'status': batch['status'],
            'total': batch['total'],
            'completed': batch['completed'],
            'failed': batch['failed'],
            'progress': batch['progress'],
            'created_at': batch['created_at'],
            'completed_at': batch.get('completed_at'),
            'videos': batch['videos']
        }
    
    def create_batch_zip(self, batch_id):
        """Create ZIP file containing all downloaded videos"""
        if batch_id not in self.batches:
            raise FileNotFoundError('Batch not found')
        
        batch = self.batches[batch_id]
        
        if batch['status'] != 'completed':
            raise ValueError('Batch download not completed')
        
        output_path = Path(batch['output_path'])
        zip_path = output_path.parent / f'{batch_id}.zip'
        
        # Create ZIP file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for video in batch['videos']:
                if video['success'] and os.path.exists(video['file_path']):
                    zipf.write(video['file_path'], arcname=video['filename'])
        
        return str(zip_path)
    
    def cancel_batch(self, batch_id):
        """Cancel a batch download"""
        if batch_id not in self.batches:
            return {'error': 'Batch not found'}
        
        batch = self.batches[batch_id]
        
        if batch['status'] == 'completed':
            return {'error': 'Batch already completed'}
        
        batch['status'] = 'cancelled'
        batch['cancelled_at'] = datetime.now().isoformat()
        
        return {
            'success': True,
            'message': 'Batch cancelled'
        }
