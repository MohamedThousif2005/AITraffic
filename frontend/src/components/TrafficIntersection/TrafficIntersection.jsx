import React from 'react';
import TrafficLight from '../TrafficLight/TrafficLight';
import { DIRECTIONS } from '../../utils/constants';
import './TrafficIntersection.css';

const TrafficIntersection = ({ analysis }) => {
  const { vehicle_counts, signal_states, traffic_density } = analysis;

  return (
    <div className="traffic-intersection">
      <div className="intersection-container">
        {/* Roads */}
        <div className="road vertical-road"></div>
        <div className="road horizontal-road"></div>
        
        {/* Center of intersection */}
        <div className="intersection-center"></div>

        {/* Traffic Lights */}
        <div className="traffic-light-container north">
          <TrafficLight 
            direction={DIRECTIONS.NORTH}
            state={signal_states[DIRECTIONS.NORTH]}
            vehicleCount={vehicle_counts[DIRECTIONS.NORTH]}
            density={traffic_density[DIRECTIONS.NORTH]}
          />
        </div>

        <div className="traffic-light-container south">
          <TrafficLight 
            direction={DIRECTIONS.SOUTH}
            state={signal_states[DIRECTIONS.SOUTH]}
            vehicleCount={vehicle_counts[DIRECTIONS.SOUTH]}
            density={traffic_density[DIRECTIONS.SOUTH]}
          />
        </div>

        <div className="traffic-light-container east">
          <TrafficLight 
            direction={DIRECTIONS.EAST}
            state={signal_states[DIRECTIONS.EAST]}
            vehicleCount={vehicle_counts[DIRECTIONS.EAST]}
            density={traffic_density[DIRECTIONS.EAST]}
          />
        </div>

        <div className="traffic-light-container west">
          <TrafficLight 
            direction={DIRECTIONS.WEST}
            state={signal_states[DIRECTIONS.WEST]}
            vehicleCount={vehicle_counts[DIRECTIONS.WEST]}
            density={traffic_density[DIRECTIONS.WEST]}
          />
        </div>

        {/* Direction Labels */}
        <div className="direction-label north-label">NORTH</div>
        <div className="direction-label south-label">SOUTH</div>
        <div className="direction-label east-label">EAST</div>
        <div className="direction-label west-label">WEST</div>

        {/* Traffic Flow Indicators */}
        <div className="flow-indicator north-flow">↓</div>
        <div className="flow-indicator south-flow">↑</div>
        <div className="flow-indicator east-flow">←</div>
        <div className="flow-indicator west-flow">→</div>
      </div>

      {/* Legend */}
      <div className="intersection-legend">
        <div className="legend-item">
          <div className="legend-color green"></div>
          <span>Green Signal</span>
        </div>
        <div className="legend-item">
          <div className="legend-color yellow"></div>
          <span>Yellow Signal</span>
        </div>
        <div className="legend-item">
          <div className="legend-color red"></div>
          <span>Red Signal</span>
        </div>
        <div className="legend-item">
          <div className="legend-color vehicle"></div>
          <span>Vehicle Count</span>
        </div>
      </div>
    </div>
  );
};

export default TrafficIntersection;