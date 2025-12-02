from flask import Flask
from flask_cors import CORS
import os
import sys

# Add parent directory to path to import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import get_config

def create_app(config_name=None):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = 'default'
    
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from app.routes.health_routes import health_bp
    from app.routes.traffic_routes import traffic_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(traffic_bp)
    
    # Error handlers
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return {
            'error': 'Bad Request',
            'message': 'The request could not be understood by the server',
            'status_code': 400
        }, 400
    
    @app.errorhandler(404)
    def not_found(error):
        return {
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status_code': 404
        }, 404
    
    @app.errorhandler(413)
    def too_large(error):
        return {
            'error': 'File Too Large',
            'message': 'The uploaded file exceeds the maximum allowed size',
            'status_code': 413
        }, 413
    
    @app.errorhandler(500)
    def internal_error(error):
        return {
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred',
            'status_code': 500
        }, 500