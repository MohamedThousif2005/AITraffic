import React from 'react';
import { Car } from 'lucide-react';
import { SIGNAL_STATES, DENSITY_LEVELS, DENSITY_COLORS } from '../../utils/constants';
import './TrafficLight.css';

const TrafficLight = ({ direction, state, vehicleCount, density }) => {
  const getDensityColor = (density) => {
    return DENSITY_COLORS[density] || DENSITY_COLORS.very_low;
  };

  const getDensityText = (density) => {
    return density.replace('_', ' ').toUpperCase();
  };

  return (
    <div className={`traffic-light ${direction}`}>
      {/* Traffic Light */}
      <div className="light-housing">
        <div 
          className={`light red ${state === SIGNAL_STATES.RED ? 'active' : ''}`}
          title="Red Light"
        ></div>
        <div 
          className={`light yellow ${state === SIGNAL_STATES.YELLOW ? 'active' : ''}`}
          title="Yellow Light"
        ></div>
        <div 
          className={`light green ${state === SIGNAL_STATES.GREEN ? 'active' : ''}`}
          title="Green Light"
        ></div>
      </div>

      {/* Direction and Info */}
      <div className="light-info">
        <div className="direction">{direction.toUpperCase()}</div>
        
        {/* Vehicle Count */}
        <div className="vehicle-count">
          <Car size={14} className="vehicle-icon" />
          <span>{vehicleCount}</span>
        </div>

        {/* Density Indicator */}
        <div 
          className="density-indicator"
          style={{ backgroundColor: getDensityColor(density) }}
          title={`Traffic density: ${getDensityText(density)}`}
        >
          {getDensityText(density).charAt(0)}
        </div>
      </div>

      {/* Status Badge */}
      <div className={`status-badge ${state}`}>
        {state.toUpperCase()}
      </div>
    </div>
  );
};

export default TrafficLight;