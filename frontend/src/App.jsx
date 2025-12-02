import React, { useState } from 'react';
import { Upload, TrafficCone, Car, Lightbulb } from 'lucide-react';
import ImageUpload from './components/ImageUpload/ImageUpload';
import TrafficIntersection from './components/TrafficIntersection/TrafficIntersection';
import AnalysisResults from './components/AnalysisResults/AnalysisResults';
import { analyzeTraffic } from './services/api';
import './App.css';

function App() {
  const [images, setImages] = useState({
    north: null,
    south: null,
    east: null,
    west: null
  });
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImagesUpload = (uploadedImages) => {
    setImages(uploadedImages);
    setError(null);
  };

  const handleAnalyzeTraffic = async () => {
    if (!Object.values(images).every(img => img !== null)) {
      setError('Please upload images for all four directions');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const result = await analyzeTraffic(images);
      setAnalysis(result);
    } catch (err) {
      setError(err.message || 'Failed to analyze traffic. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const allImagesUploaded = Object.values(images).every(img => img !== null);

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <TrafficCone size={40} className="logo-icon" />
            <div className="logo-text">
              <h1>AI Traffic Management System</h1>
              <p>Intelligent traffic signal optimization using computer vision</p>
            </div>
          </div>
          <div className="header-stats">
            {analysis && (
              <div className="stats">
                <div className="stat">
                  <Car size={20} />
                  <span>Total Vehicles: {Object.values(analysis.vehicle_counts).reduce((a, b) => a + b, 0)}</span>
                </div>
                <div className="stat">
                  <Lightbulb size={20} />
                  <span>Green Signals: {Object.values(analysis.signal_states).filter(s => s === 'green').length}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <div className="container">
          {/* Upload Section */}
          <section className="section upload-section">
            <div className="section-header">
              <Upload size={28} className="section-icon" />
              <h2>Upload Road Images</h2>
            </div>
            <p className="section-description">
              Upload images from all four directions of the intersection for AI analysis
            </p>
            
            <ImageUpload onImagesUpload={handleImagesUpload} />
            
            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            <button 
              className={`analyze-button ${loading ? 'loading' : ''}`}
              onClick={handleAnalyzeTraffic}
              disabled={!allImagesUploaded || loading}
            >
              {loading ? (
                <>
                  <div className="spinner"></div>
                  Analyzing Traffic Patterns...
                </>
              ) : (
                <>
                  <TrafficCone size={20} />
                  Analyze Traffic Patterns
                </>
              )}
            </button>
          </section>

          {/* Results Section */}
          {analysis && (
            <>
              {/* Traffic Intersection Visualization */}
              <section className="section visualization-section">
                <div className="section-header">
                  <TrafficCone size={28} className="section-icon" />
                  <h2>Live Intersection View</h2>
                </div>
                <TrafficIntersection analysis={analysis} />
              </section>

              {/* Analysis Results */}
              <AnalysisResults analysis={analysis} />
            </>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="container">
          <p>&copy; 2024 AI Traffic Management System. Built with React.js + Python AI.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;