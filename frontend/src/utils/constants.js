// Traffic signal constants
export const SIGNAL_STATES = {
  RED: 'red',
  YELLOW: 'yellow',
  GREEN: 'green'
};

// Traffic density levels
export const DENSITY_LEVELS = {
  VERY_LOW: 'very_low',
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  VERY_HIGH: 'very_high'
};

// Direction constants
export const DIRECTIONS = {
  NORTH: 'north',
  SOUTH: 'south',
  EAST: 'east',
  WEST: 'west'
};

// Density level colors
export const DENSITY_COLORS = {
  very_low: '#d4edda',
  low: '#cce7ff', 
  medium: '#fff3cd',
  high: '#f8d7da',
  very_high: '#dc3545'
};

// Density level text colors
export const DENSITY_TEXT_COLORS = {
  very_low: '#155724',
  low: '#004085',
  medium: '#856404',
  high: '#721c24',
  very_high: '#ffffff'
};

// Signal state colors
export const SIGNAL_COLORS = {
  red: '#e74c3c',
  yellow: '#f39c12',
  green: '#27ae60'
};

// Default analysis state
export const DEFAULT_ANALYSIS = {
  vehicle_counts: {
    north: 0,
    south: 0,
    east: 0,
    west: 0
  },
  traffic_density: {
    north: 'very_low',
    south: 'very_low',
    east: 'very_low',
    west: 'very_low'
  },
  signal_states: {
    north: 'red',
    south: 'red',
    east: 'red',
    west: 'red'
  },
  recommendations: [],
  analysis_timestamp: new Date().toISOString()
};