#!/usr/bin/env python3
"""
Main entry point for the Traffic AI Management System
"""

import os
import sys
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def setup_logging():
    """Setup basic logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()
    
    # Create application instance
    app = create_app()
    
    # Get configuration
    config = app.config
    
    # Ensure upload directories exist
    os.makedirs(config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(config['PROCESSED_FOLDER'], exist_ok=True)
    
    # Log startup information
    logger = logging.getLogger(__name__)
    logger.info("🚦 Starting AI Traffic Management System")
    logger.info(f"📁 Upload folder: {config['UPLOAD_FOLDER']}")
    logger.info(f"🔧 Debug mode: {config['DEBUG']}")
    logger.info(f"🌐 CORS origins: {config['CORS_ORIGINS']}")
    
    # Run application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )

if __name__ == '__main__':
    main()