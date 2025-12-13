"""
Multi Link Routes
API endpoints for multiple video downloads
"""

from flask import request, jsonify, send_file
from . import multilink_bp
from .service import MultiLinkService
import logging

logger = logging.getLogger(__name__)
service = MultiLinkService()

@multilink_bp.route('/batch', methods=['POST'])
def create_batch_download():
    """
    Create a batch download for multiple videos
    
    Request body:
    {
        "urls": ["url1", "url2", "url3"],
        "format": "mp4",
        "quality": "best"
    }
    """
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        format_type = data.get('format', 'mp4')
        quality = data.get('quality', 'best')
        
        if not urls or not isinstance(urls, list):
            return jsonify({'error': 'URLs array is required'}), 400
        
        if len(urls) > 50:
            return jsonify({'error': 'Maximum 50 URLs allowed per batch'}), 400
        
        result = service.create_batch(urls, format_type, quality)
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'batch_id': result.get('batch_id'),
                'total_videos': len(urls),
                'message': 'Batch download created'
            }), 200
        else:
            return jsonify({'error': result.get('error')}), 500
            
    except Exception as e:
        logger.error(f"Error creating batch download: {str(e)}")
        return jsonify({'error': str(e)}), 500

@multilink_bp.route('/batch/<batch_id>', methods=['GET'])
def get_batch_status(batch_id):
    """Get batch download status"""
    try:
        status = service.get_batch_status(batch_id)
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error getting batch status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@multilink_bp.route('/batch/<batch_id>/download', methods=['GET'])
def download_batch_zip(batch_id):
    """Download all videos in batch as ZIP file"""
    try:
        zip_path = service.create_batch_zip(batch_id)
        return send_file(zip_path, as_attachment=True, download_name=f'batch_{batch_id}.zip')
    except Exception as e:
        logger.error(f"Error creating batch ZIP: {str(e)}")
        return jsonify({'error': str(e)}), 500

@multilink_bp.route('/batch/<batch_id>/cancel', methods=['POST'])
def cancel_batch(batch_id):
    """Cancel a batch download"""
    try:
        result = service.cancel_batch(batch_id)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error canceling batch: {str(e)}")
        return jsonify({'error': str(e)}), 500
