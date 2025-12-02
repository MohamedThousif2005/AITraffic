from flask import Blueprint, jsonify
import logging
from datetime import datetime
import psutil
import os

logger = logging.getLogger(__name__)

# Create blueprint
health_bp = Blueprint('health', __name__)

@health_bp.route('/api/health', methods=['GET'])
def health_check():
    """Comprehensive health check endpoint"""
    try:
        # System information
        system_info = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'AI Traffic Management System',
            'version': '1.0.0'
        }
        
        # System metrics
        system_metrics = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'active_connections': len(psutil.net_connections()),
            'process_memory_mb': psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        }
        
        # Service status
        service_status = {
            'vehicle_detection': 'operational',
            'signal_optimization': 'operational',
            'image_processing': 'operational',
            'api_endpoints': 'operational'
        }
        
        response = {
            **system_info,
            'system_metrics': system_metrics,
            'service_status': service_status,
            'message': 'All systems operational'
        }
        
        logger.debug("Health check completed successfully")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'message': 'System health check failed'
        }), 500

@health_bp.route('/api/status', methods=['GET'])
def system_status():
    """Detailed system status endpoint"""
    try:
        status_info = {
            'system': 'AI Traffic Management System',
            'environment': os.getenv('FLASK_ENV', 'development'),
            'debug_mode': os.getenv('DEBUG', 'True').lower() == 'true',
            'startup_time': datetime.now().isoformat(),
            'python_version': os.sys.version,
            'platform': os.sys.platform
        }
        
        return jsonify(status_info)
        
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        return jsonify({'error': 'Status check failed'}), 500

@health_bp.route('/api/info', methods=['GET'])
def system_info():
    """System information and capabilities"""
    info = {
        'system': {
            'name': 'AI Traffic Management System',
            'description': 'Intelligent traffic signal optimization using computer vision',
            'version': '1.0.0',
            'author': 'Traffic AI Team'
        },
        'capabilities': [
            'Multi-directional traffic analysis',
            'AI-powered vehicle detection',
            'Real-time signal optimization',
            'Traffic density classification',
            'Emergency mode detection',
            'Image processing and enhancement'
        ],
        'endpoints': {
            '/api/health': 'System health check',
            '/api/status': 'System status',
            '/api/info': 'System information',
            '/api/analyze-traffic': 'Traffic analysis (POST)',
            '/api/statistics': 'Traffic statistics (GET)'
        },
        'supported_image_formats': ['JPEG', 'PNG', 'GIF', 'BMP'],
        'max_file_size': '16MB'
    }
    
    return jsonify(info)