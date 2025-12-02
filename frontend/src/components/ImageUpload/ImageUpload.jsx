import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, Camera } from 'lucide-react';
import './ImageUpload.css';

const ImageUpload = ({ onImagesUpload }) => {
  const [images, setImages] = useState({
    north: null,
    south: null,
    east: null,
    west: null
  });

  const onDrop = useCallback((acceptedFiles) => {
    const newImages = { ...images };
    const directions = ['north', 'south', 'east', 'west'];
    
    // Reset all images first if we're doing bulk upload
    if (acceptedFiles.length === 4) {
      directions.forEach(dir => { newImages[dir] = null; });
    }
    
    acceptedFiles.forEach((file, index) => {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        const direction = acceptedFiles.length === 4 ? directions[index] : Object.keys(newImages).find(dir => !newImages[dir]) || directions[index];
        
        newImages[direction] = {
          file: file,
          preview: e.target.result,
          name: file.name,
          size: file.size
        };
        
        setImages({ ...newImages });
        
        // Check if all images are uploaded
        if (Object.values(newImages).every(img => img !== null)) {
          onImagesUpload(newImages);
        }
      };
      
      reader.readAsDataURL(file);
    });
  }, [images, onImagesUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp']
    },
    multiple: true
  });

  const removeImage = (direction) => {
    const newImages = { ...images, [direction]: null };
    setImages(newImages);
    onImagesUpload(newImages);
  };

  const handleIndividualUpload = (direction, event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const newImages = {
          ...images,
          [direction]: {
            file: file,
            preview: e.target.result,
            name: file.name,
            size: file.size
          }
        };
        setImages(newImages);
        onImagesUpload(newImages);
      };
      reader.readAsDataURL(file);
    }
  };

  const allImagesUploaded = Object.values(images).every(img => img !== null);

  return (
    <div className="image-upload">
      {/* Bulk Upload Area */}
      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'active' : ''} ${allImagesUploaded ? 'complete' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="dropzone-content">
          <Upload size={48} className="dropzone-icon" />
          {isDragActive ? (
            <p>Drop the images here...</p>
          ) : (
            <>
              <p className="dropzone-title">Drag & drop 4 images here</p>
              <p className="dropzone-subtitle">or click to select files</p>
              <p className="dropzone-hint">One for each direction: North, South, East, West</p>
            </>
          )}
        </div>
      </div>

      {/* Individual Upload Grid */}
      <div className="upload-grid">
        {Object.entries(images).map(([direction, imageData]) => (
          <div key={direction} className="upload-slot">
            <div className="upload-slot-header">
              <h3 className="direction-title">{direction.toUpperCase()}</h3>
              {imageData && (
                <button 
                  className="remove-button"
                  onClick={() => removeImage(direction)}
                  title="Remove image"
                >
                  <X size={16} />
                </button>
              )}
            </div>

            <div className="upload-area">
              {imageData ? (
                <div className="image-preview">
                  <img 
                    src={imageData.preview} 
                    alt={`${direction} view`}
                    className="preview-image"
                  />
                  <div className="image-info">
                    <span className="image-name">{imageData.name}</span>
                    <span className="image-size">
                      {(imageData.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </div>
                </div>
              ) : (
                <label className="upload-placeholder">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleIndividualUpload(direction, e)}
                    style={{ display: 'none' }}
                  />
                  <Camera size={32} className="placeholder-icon" />
                  <span>Click to upload</span>
                </label>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Upload Status */}
      <div className="upload-status">
        <div className={`status-indicator ${allImagesUploaded ? 'complete' : 'incomplete'}`}>
          {allImagesUploaded ? '✓ All images uploaded' : 'Upload images for all 4 directions'}
        </div>
        <div className="upload-count">
          {Object.values(images).filter(img => img !== null).length} / 4 images uploaded
        </div>
      </div>
    </div>
  );
};

export default ImageUpload;