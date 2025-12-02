import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('Response received:', response.status);
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.error || `Server error: ${error.response.status}`;
      throw new Error(message);
    } else if (error.request) {
      // Request made but no response received
      throw new Error('No response from server. Please check if the backend is running.');
    } else {
      // Something else happened
      throw new Error('Request failed. Please check your connection.');
    }
  }
);

/**
 * Analyze traffic patterns from uploaded images
 * @param {Object} images - Object containing images for each direction
 * @returns {Promise<Object>} Analysis results
 */
export const analyzeTraffic = async (images) => {
  try {
    const formData = new FormData();
    
    // Append each image to form data
    Object.entries(images).forEach(([direction, imageData]) => {
      if (imageData && imageData.file) {
        formData.append(direction, imageData.file);
      }
    });

    console.log('Sending traffic analysis request...');
    const response = await api.post('/analyze-traffic', formData);
    
    console.log('Analysis completed successfully');
    return response.data;
  } catch (error) {
    console.error('Traffic analysis failed:', error);
    throw error;
  }
};

/**
 * Health check for backend service
 * @returns {Promise<Object>} Health status
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export default api;