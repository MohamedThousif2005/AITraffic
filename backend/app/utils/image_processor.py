import cv2
import numpy as np
from PIL import Image, ImageEnhance
import io
import base64
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Handles image processing operations for traffic analysis"""
    
    def __init__(self):
        self.enhancement_factors = {
            'contrast': 1.2,
            'brightness': 1.1,
            'sharpness': 1.1
        }
    
    def preprocess_image(self, image_array: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better vehicle detection
        """
        try:
            # Convert to RGB if needed
            if len(image_array.shape) == 3 and image_array.shape[2] == 3:
                # Convert BGR to RGB
                image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image_array
            
            # Enhance image quality
            enhanced = self._enhance_image(image_rgb)
            
            # Apply noise reduction
            denoised = cv2.medianBlur(enhanced, 3)
            
            return denoised
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return image_array
    
    def _enhance_image(self, image_array: np.ndarray) -> np.ndarray:
        """
        Enhance image quality using PIL
        """
        try:
            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(image_array)
            
            # Enhance contrast
            contrast_enhancer = ImageEnhance.Contrast(pil_image)
            enhanced = contrast_enhancer.enhance(self.enhancement_factors['contrast'])
            
            # Enhance brightness
            brightness_enhancer = ImageEnhance.Brightness(enhanced)
            enhanced = brightness_enhancer.enhance(self.enhancement_factors['brightness'])
            
            # Enhance sharpness
            sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
            enhanced = sharpness_enhancer.enhance(self.enhancement_factors['sharpness'])
            
            # Convert back to numpy array
            return np.array(enhanced)
            
        except Exception as e:
            logger.warning(f"Image enhancement failed: {str(e)}")
            return image_array
    
    def resize_image(self, image_array: np.ndarray, target_size: Tuple[int, int] = (640, 640)) -> np.ndarray:
        """
        Resize image to target dimensions
        """
        return cv2.resize(image_array, target_size, interpolation=cv2.INTER_AREA)
    
    def extract_roi(self, image_array: np.ndarray, roi_percentage: float = 0.7) -> np.ndarray:
        """
        Extract Region of Interest (road area)
        """
        height, width = image_array.shape[:2]
        
        # Calculate ROI coordinates (center portion of the image)
        roi_width = int(width * roi_percentage)
        roi_height = int(height * roi_percentage)
        
        start_x = (width - roi_width) // 2
        start_y = (height - roi_height) // 2
        
        return image_array[start_y:start_y + roi_height, start_x:start_x + roi_width]
    
    def detect_edges(self, image_array: np.ndarray) -> np.ndarray:
        """
        Detect edges in the image using Canny edge detection
        """
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return edges
    
    def convert_to_base64(self, image_array: np.ndarray) -> str:
        """
        Convert numpy array to base64 string
        """
        try:
            # Convert to PIL Image
            pil_image = Image.fromarray(image_array)
            
            # Convert to bytes
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG', quality=85)
            
            # Convert to base64
            img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return f"data:image/jpeg;base64,{img_str}"
            
        except Exception as e:
            logger.error(f"Error converting image to base64: {str(e)}")
            return ""
    
    def save_processed_image(self, image_array: np.ndarray, filename: str, upload_folder: str) -> str:
        """
        Save processed image to disk
        """
        try:
            filepath = f"{upload_folder}/processed_{filename}"
            cv2.imwrite(filepath, cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR))
            return filepath
        except Exception as e:
            logger.error(f"Error saving processed image: {str(e)}")
            return ""

# Global instance
image_processor = ImageProcessor()