from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class TrafficDensity(Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class SignalState(Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"

@dataclass
class VehicleDetectionResult:
    """Results from vehicle detection analysis"""
    contour_count: int
    motion_count: int
    cascade_count: int
    final_count: int
    confidence: float
    detection_method: str
    processing_time: float

@dataclass
class TrafficAnalysis:
    """Complete traffic analysis result"""
    analysis_id: str
    timestamp: datetime
    vehicle_counts: Dict[str, int]
    traffic_density: Dict[str, TrafficDensity]
    signal_states: Dict[str, SignalState]
    recommendations: List[str]
    detection_qualities: Dict[str, float]
    total_vehicles: int
    emergency_mode: bool
    processing_time: float

@dataclass
class ImageAnalysis:
    """Individual image analysis result"""
    direction: str
    vehicle_count: int
    density_level: TrafficDensity
    detection_quality: float
    processed_image_path: Optional[str] = None
    original_image_path: Optional[str] = None

@dataclass
class SystemStatistics:
    """System performance and traffic statistics"""
    total_analyses: int
    average_vehicles: float
    max_vehicles: int
    min_vehicles: int
    emergency_mode_count: int
    average_processing_time: float
    analysis_period: str

@dataclass
class OptimizationParameters:
    """Parameters for signal optimization"""
    min_green_time: int
    max_green_time: int
    density_thresholds: Dict[TrafficDensity, int]
    peak_hours: Dict[str, tuple]
    emergency_threshold: int