"""
Playlist Routes
API endpoints for playlist downloads
"""

from flask import request, jsonify, send_file
from . import playlist_bp
from .service import PlaylistService
import logging

logger = logging.getLogger(__name__)
service = PlaylistService()

@playlist_bp.route('/info', methods=['POST'])
def get_playlist_info():
    """
    Get playlist information without downloading
    
    Request body:
    {
        "url": "https://youtube.com/playlist?list=..."
    }
    """
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        info = service.get_playlist_info(url)
        return jsonify(info), 200
        
    except Exception as e:
        logger.error(f"Error getting playlist info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@playlist_bp.route('/download', methods=['POST'])
def download_playlist():
    """
    Download entire playlist
    
    Request body:
    {
        "url": "https://youtube.com/playlist?list=...",
        "format": "mp4",
        "quality": "best",
        "start_index": 1,  # Optional
        "end_index": 10    # Optional
    }
    """
    try:
        data = request.get_json()
        url = data.get('url')
        format_type = data.get('format', 'mp4')
        quality = data.get('quality', 'best')
        start_index = data.get('start_index')
        end_index = data.get('end_index')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        result = service.download_playlist(url, format_type, quality, start_index, end_index)
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'playlist_id': result.get('playlist_id'),
                'message': 'Playlist download started'
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 500
            
    except Exception as e:
        logger.error(f"Error downloading playlist: {str(e)}")
        return jsonify({'error': str(e)}), 500

@playlist_bp.route('/status/<playlist_id>', methods=['GET'])
def get_playlist_status(playlist_id):
    """Get playlist download status"""
    try:
        status = service.get_playlist_status(playlist_id)
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error getting playlist status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@playlist_bp.route('/download/<playlist_id>', methods=['GET'])
def download_playlist_zip(playlist_id):
    """Download playlist as ZIP file"""
    try:
        zip_path = service.create_playlist_zip(playlist_id)
        return send_file(zip_path, as_attachment=True, download_name=f'playlist_{playlist_id}.zip')
    except Exception as e:
        logger.error(f"Error creating playlist ZIP: {str(e)}")
        return jsonify({'error': str(e)}), 500

@playlist_bp.route('/cancel/<playlist_id>', methods=['POST'])
def cancel_playlist(playlist_id):
    """Cancel a playlist download"""
    try:
        result = service.cancel_playlist(playlist_id)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error canceling playlist: {str(e)}")
        return jsonify({'error': str(e)}), 500
