"""
Single Link Routes
API endpoints for single video downloads
"""

from flask import request, jsonify, send_file
from . import singlelink_bp
from .service import SingleLinkService
import logging

logger = logging.getLogger(__name__)
service = SingleLinkService()

@singlelink_bp.route('/info', methods=['POST'])
def get_video_info():
    """
    Get video information without downloading
    
    Request body:
    {
        "url": "https://youtube.com/watch?v=..."
    }
    """
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        info = service.get_video_info(url)
        return jsonify(info), 200
        
    except Exception as e:
        logger.error(f"Error getting video info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@singlelink_bp.route('/download', methods=['POST'])
def download_video():
    """
    Download a single video
    
    Request body:
    {
        "url": "https://youtube.com/watch?v=...",
        "format": "mp4",  # or "mp3"
        "quality": "best"  # or specific quality like "720p"
    }
    """
    try:
        data = request.get_json()
        url = data.get('url')
        format_type = data.get('format', 'mp4')
        quality = data.get('quality', 'best')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        result = service.download_video(url, format_type, quality)
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'download_id': result.get('download_id'),
                'message': 'Download started'
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 500
            
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        return jsonify({'error': str(e)}), 500

@singlelink_bp.route('/status/<download_id>', methods=['GET'])
def get_download_status(download_id):
    """Get download status by ID"""
    try:
        status = service.get_download_status(download_id)
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error getting download status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@singlelink_bp.route('/file/<download_id>', methods=['GET'])
def get_download_file(download_id):
    """Download the file by ID"""
    try:
        file_path = service.get_file_path(download_id)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Error sending file: {str(e)}")
        return jsonify({'error': str(e)}), 404
