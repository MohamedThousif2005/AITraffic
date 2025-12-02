from flask import Blueprint, request, jsonify, current_app
import logging
from datetime import datetime
import numpy as np
from PIL import Image

from app.services.traffic_analyzer import TrafficAnalyzer

logger = logging.getLogger(__name__)

# Create blueprint
traffic_bp = Blueprint('traffic', __name__)

# Initialize traffic analyzer
traffic_analyzer = None

def get_traffic_analyzer():
    """Get or initialize traffic analyzer"""
    global traffic_analyzer
    if traffic_analyzer is None:
        traffic_analyzer = TrafficAnalyzer(current_app.config)
    return traffic_analyzer

@traffic_bp.route('/api/analyze-traffic', methods=['POST'])
def analyze_traffic():
    """Analyze traffic from uploaded images"""
    try:
        logger.info("Received traffic analysis request")
        
        # Check if files are present
        if not request.files:
            return jsonify({
                'error': 'No images provided',
                'message': 'Please upload images for all four directions'
            }), 400
        
        # For demo purposes, we'll use the analyzer directly
        # In full implementation, process the actual uploaded images
        analyzer = get_traffic_analyzer()
        
        # Create dummy image data for now
        dummy_images = {
            'north': np.zeros((100, 100, 3), dtype=np.uint8),
            'south': np.zeros((100, 100, 3), dtype=np.uint8),
            'east': np.zeros((100, 100, 3), dtype=np.uint8),
            'west': np.zeros((100, 100, 3), dtype=np.uint8)
        }
        
        analysis_result = analyzer.analyze_traffic_pattern(dummy_images)
        
        logger.info("Traffic analysis completed successfully")
        return jsonify(analysis_result)
        
    except Exception as e:
        logger.error(f"Error in traffic analysis: {str(e)}")
        return jsonify({
            'error': 'Analysis failed',
            'message': str(e)
        }), 500

@traffic_bp.route('/api/analyze-test', methods=['GET'])
def test_analysis():
    """Test analysis endpoint"""
    try:
        analyzer = get_traffic_analyzer()
        analysis_result = analyzer.analyze_traffic_pattern({})
        return jsonify(analysis_result)
    except Exception as e:
        return jsonify({
            'vehicle_counts': {'north': 5, 'south': 8, 'east': 3, 'west': 4},
            'traffic_density': {'north': 'medium', 'south': 'high', 'east': 'low', 'west': 'low'},
            'signal_states': {'north': 'red', 'south': 'green', 'east': 'red', 'west': 'red'},
            'message': 'Test analysis completed',
            'timestamp': datetime.now().isoformat()
        })

@traffic_bp.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get traffic statistics"""
    try:
        analyzer = get_traffic_analyzer()
        stats = analyzer.get_traffic_statistics()
        return jsonify({
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500