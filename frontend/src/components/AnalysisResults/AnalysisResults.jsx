import React from 'react';
import { Lightbulb, TrendingUp, Clock, AlertTriangle, Car, TrafficCone } from 'lucide-react';
import { DENSITY_COLORS, DENSITY_TEXT_COLORS, SIGNAL_COLORS } from '../../utils/constants';
import './AnalysisResults.css';

const AnalysisResults = ({ analysis }) => {
  const { vehicle_counts, traffic_density, signal_states, recommendations, analysis_timestamp } = analysis;

  const getDensityDisplay = (density) => {
    return density.replace('_', ' ').toUpperCase();
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  const totalVehicles = Object.values(vehicle_counts).reduce((sum, count) => sum + count, 0);
  const greenSignals = Object.values(signal_states).filter(state => state === 'green').length;

  return (
    <section className="section analysis-results">
      <div className="section-header">
        <TrendingUp size={28} className="section-icon" />
        <h2>Detailed Analysis Results</h2>
      </div>

      <div className="analysis-grid">
        {/* Vehicle Count Summary */}
        <div className="analysis-card">
          <h3>Vehicle Count Summary</h3>
          <div className="vehicle-summary">
            <div className="total-vehicles">
              <Car size={24} />
              <span>Total Vehicles: {totalVehicles}</span>
            </div>
            <div className="direction-breakdown">
              {Object.entries(vehicle_counts).map(([direction, count]) => (
                <div key={direction} className="direction-count">
                  <span className="direction-name">{direction.toUpperCase()}:</span>
                  <span className="vehicle-number">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Traffic Density */}
        <div className="analysis-card">
          <h3>Traffic Density Levels</h3>
          <div className="density-levels">
            {Object.entries(traffic_density).map(([direction, density]) => (
              <div key={direction} className="density-item">
                <span className="density-direction">{direction.toUpperCase()}</span>
                <span 
                  className="density-badge"
                  style={{
                    backgroundColor: DENSITY_COLORS[density],
                    color: DENSITY_TEXT_COLORS[density]
                  }}
                >
                  {getDensityDisplay(density)}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Signal Status */}
        <div className="analysis-card">
          <h3>Signal Status</h3>
          <div className="signal-status-grid">
            {Object.entries(signal_states).map(([direction, state]) => (
              <div key={direction} className="signal-status-item">
                <div className="signal-direction">{direction.toUpperCase()}</div>
                <div 
                  className="signal-indicator"
                  style={{ backgroundColor: SIGNAL_COLORS[state] }}
                ></div>
                <div className="signal-state">{state.toUpperCase()}</div>
              </div>
            ))}
          </div>
          <div className="signal-summary">
            <div className="summary-item">
              <TrafficCone size={16} />
              <span>Green Signals: {greenSignals}</span>
            </div>
            <div className="summary-item">
              <Car size={16} />
              <span>Total Vehicles: {totalVehicles}</span>
            </div>
          </div>
        </div>

        {/* AI Recommendations */}
        <div className="analysis-card recommendations-card">
          <div className="card-header">
            <Lightbulb size={24} className="card-icon" />
            <h3>AI Recommendations</h3>
          </div>
          <div className="recommendations-list">
            {recommendations && recommendations.length > 0 ? (
              recommendations.map((recommendation, index) => (
                <div key={index} className="recommendation-item">
                  <AlertTriangle size={16} className="recommendation-icon" />
                  <span>{recommendation}</span>
                </div>
              ))
            ) : (
              <div className="no-recommendations">
                <Lightbulb size={32} className="no-rec-icon" />
                <p>No specific recommendations at this time.</p>
                <p className="no-rec-subtitle">Traffic flow appears to be optimal.</p>
              </div>
            )}
          </div>
        </div>

        {/* AI Model Information */}
<div className="analysis-card ai-info-card">
  <div className="card-header">
    <span className="ai-icon">🤖</span>
    <h3>AI Model Analysis</h3>
  </div>
  <div className="ai-info">
    <div className="ai-model">
      <span className="ai-label">Model:</span>
      <span className="ai-value">AdvancedTrafficAI v2.0</span>
    </div>
    <div className="ai-confidence">
      <span className="ai-label">Confidence:</span>
      <span className="ai-value">{analysis.ai_confidence * 100}%</span>
    </div>
    <div className="ai-processing">
      <span className="ai-label">Processing Time:</span>
      <span className="ai-value">{analysis.processing_time_ms}ms</span>
    </div>
  </div>
</div>

        {/* Analysis Information */}
        <div className="analysis-card metadata-card">
          <div className="card-header">
            <Clock size={20} className="card-icon" />
            <h3>Analysis Information</h3>
          </div>
          <div className="metadata-content">
            <div className="metadata-item">
              <span className="metadata-label">Analysis Time:</span>
              <span className="metadata-value">{formatTimestamp(analysis_timestamp)}</span>
            </div>
            <div className="metadata-item">
              <span className="metadata-label">Total Directions:</span>
              <span className="metadata-value">4</span>
            </div>
            <div className="metadata-item">
              <span className="metadata-label">System Status:</span>
              <span className="metadata-value status-active">Active</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AnalysisResults;