import logging
from typing import Dict, List, Tuple
import random
from datetime import datetime

logger = logging.getLogger(__name__)

class SignalOptimizer:
    """Optimizes traffic signals based on traffic analysis"""
    
    def __init__(self, config):
        self.config = config
        self.signal_history = []
        self.emergency_mode = False
        self.peak_hours = {
            'morning': (7, 10),    # 7 AM - 10 AM
            'evening': (16, 19)    # 4 PM - 7 PM
        }
    
    def optimize_signals(self, vehicle_counts: Dict[str, int], 
                        traffic_density: Dict[str, str],
                        previous_states: Dict[str, str] = None) -> Dict[str, str]:
        """
        Optimize traffic signals based on current traffic conditions
        """
        try:
            current_hour = datetime.now().hour
            is_peak_hour = self._is_peak_hour(current_hour)
            
            # Get base signal states
            if is_peak_hour:
                signal_states = self._peak_hour_optimization(vehicle_counts, traffic_density)
            else:
                signal_states = self._normal_optimization(vehicle_counts, traffic_density)
            
            # Apply emergency mode if needed
            if self._should_activate_emergency_mode(traffic_density):
                signal_states = self._emergency_optimization(vehicle_counts, traffic_density)
                self.emergency_mode = True
                logger.info("Emergency traffic mode activated")
            else:
                self.emergency_mode = False
            
            # Ensure smooth transitions from previous states
            if previous_states:
                signal_states = self._ensure_smooth_transition(previous_states, signal_states)
            
            # Log optimization decision
            self._log_optimization_decision(vehicle_counts, signal_states, is_peak_hour)
            
            return signal_states
            
        except Exception as e:
            logger.error(f"Error optimizing signals: {str(e)}")
            return self._get_default_signals()
    
    def _normal_optimization(self, vehicle_counts: Dict[str, int], 
                           traffic_density: Dict[str, str]) -> Dict[str, str]:
        """Optimize signals for normal traffic conditions"""
        total_vehicles = sum(vehicle_counts.values())
        
        if total_vehicles == 0:
            return self._get_default_signals()
        
        # Find direction with maximum vehicles
        max_direction = max(vehicle_counts, key=vehicle_counts.get)
        max_vehicles = vehicle_counts[max_direction]
        
        # Check if there's a clear priority
        other_directions = [d for d in vehicle_counts.keys() if d != max_direction]
        other_avg = sum(vehicle_counts[d] for d in other_directions) / len(other_directions)
        
        if max_vehicles > other_avg * 2.5:  # Clear priority
            signal_states = {direction: 'red' for direction in vehicle_counts.keys()}
            signal_states[max_direction] = 'green'
        else:
            # Give green to perpendicular directions with most traffic
            signal_states = self._optimize_perpendicular_groups(vehicle_counts, traffic_density)
        
        return signal_states
    
    def _peak_hour_optimization(self, vehicle_counts: Dict[str, int], 
                              traffic_density: Dict[str, str]) -> Dict[str, str]:
        """Optimize signals for peak hour traffic conditions"""
        total_vehicles = sum(vehicle_counts.values())
        
        if total_vehicles == 0:
            return self._get_default_signals()
        
        # During peak hours, prioritize main roads and coordinate signals
        main_road_priority = self._identify_main_roads(vehicle_counts, traffic_density)
        
        if main_road_priority:
            signal_states = {direction: 'red' for direction in vehicle_counts.keys()}
            for direction in main_road_priority[:2]:  # Allow up to 2 directions green
                signal_states[direction] = 'green'
        else:
            signal_states = self._optimize_perpendicular_groups(vehicle_counts, traffic_density)
        
        return signal_states
    
    def _emergency_optimization(self, vehicle_counts: Dict[str, int], 
                              traffic_density: Dict[str, str]) -> Dict[str, str]:
        """Optimize signals for emergency traffic conditions"""
        # In emergency mode, clear the most congested direction first
        congested_directions = [
            dir for dir, density in traffic_density.items() 
            if density in ['high', 'very_high']
        ]
        
        if congested_directions:
            signal_states = {direction: 'red' for direction in vehicle_counts.keys()}
            # Give green to the most congested direction
            most_congested = max(congested_directions, 
                               key=lambda d: vehicle_counts[d])
            signal_states[most_congested] = 'green'
        else:
            signal_states = self._normal_optimization(vehicle_counts, traffic_density)
        
        return signal_states
    
    def _optimize_perpendicular_groups(self, vehicle_counts: Dict[str, int],
                                     traffic_density: Dict[str, str]) -> Dict[str, str]:
        """Optimize by giving green to perpendicular direction groups"""
        # Group directions by perpendicular pairs
        north_south = ['north', 'south']
        east_west = ['east', 'west']
        
        ns_traffic = sum(vehicle_counts[d] for d in north_south)
        ew_traffic = sum(vehicle_counts[d] for d in east_west)
        
        signal_states = {direction: 'red' for direction in vehicle_counts.keys()}
        
        if ns_traffic > ew_traffic * 1.5:
            # Prioritize North-South
            for direction in north_south:
                signal_states[direction] = 'green'
        elif ew_traffic > ns_traffic * 1.5:
            # Prioritize East-West
            for direction in east_west:
                signal_states[direction] = 'green'
        else:
            # Balanced traffic - give green to the group with highest single direction
            max_ns = max(vehicle_counts[d] for d in north_south)
            max_ew = max(vehicle_counts[d] for d in east_west)
            
            if max_ns >= max_ew:
                busiest_ns = max(north_south, key=lambda d: vehicle_counts[d])
                signal_states[busiest_ns] = 'green'
            else:
                busiest_ew = max(east_west, key=lambda d: vehicle_counts[d])
                signal_states[busiest_ew] = 'green'
        
        return signal_states
    
    def _identify_main_roads(self, vehicle_counts: Dict[str, int],
                           traffic_density: Dict[str, str]) -> List[str]:
        """Identify main roads based on traffic patterns"""
        # Sort directions by vehicle count (descending)
        sorted_directions = sorted(vehicle_counts.keys(), 
                                 key=lambda d: vehicle_counts[d], 
                                 reverse=True)
        
        main_roads = []
        for direction in sorted_directions:
            if traffic_density[direction] in ['medium', 'high', 'very_high']:
                main_roads.append(direction)
        
        return main_roads
    
    def _should_activate_emergency_mode(self, traffic_density: Dict[str, str]) -> bool:
        """Check if emergency mode should be activated"""
        very_high_count = sum(1 for density in traffic_density.values() 
                            if density == 'very_high')
        high_count = sum(1 for density in traffic_density.values() 
                        if density == 'high')
        
        # Activate emergency mode if 3+ directions are high/very high density
        return (very_high_count >= 2) or (very_high_count + high_count >= 3)
    
    def _is_peak_hour(self, current_hour: int) -> bool:
        """Check if current time is during peak hours"""
        for period, (start, end) in self.peak_hours.items():
            if start <= current_hour < end:
                return True
        return False
    
    def _ensure_smooth_transition(self, previous_states: Dict[str, str],
                                new_states: Dict[str, str]) -> Dict[str, str]:
        """Ensure smooth transition between signal states"""
        # For now, return new states directly
        # In production, you might implement yellow light transitions
        return new_states
    
    def _get_default_signals(self) -> Dict[str, str]:
        """Get default signal states"""
        return {
            'north': 'red',
            'south': 'red', 
            'east': 'green',
            'west': 'red'
        }
    
    def _log_optimization_decision(self, vehicle_counts: Dict[str, int],
                                 signal_states: Dict[str, str], is_peak_hour: bool):
        """Log the optimization decision for monitoring"""
        green_directions = [d for d, state in signal_states.items() if state == 'green']
        total_vehicles = sum(vehicle_counts.values())
        
        logger.info(f"Signal optimization - "
                   f"Peak hour: {is_peak_hour}, "
                   f"Total vehicles: {total_vehicles}, "
                   f"Green signals: {green_directions}")