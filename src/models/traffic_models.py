from pydantic import BaseModel, Field, field_validator
from enum import Enum
from datetime import datetime


class SignalDirection(str, Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class TrafficSignalTiming(BaseModel):
    direction: SignalDirection
    current_time: int = Field(ge=0, le=60)
    last_time: int = Field(ge=0, le=60)
    car_count: int = Field(ge=0, le=100)

    @field_validator("current_time", "last_time")
    @classmethod
    def validate_timing(cls, v):
        if not 0 <= v <= 60:
            raise ValueError("Timing must be between 0 and 60 seconds")
        return v

    class Config:
        use_enum_values = True


class TrafficCycleData(BaseModel):
    cycle_number: int = Field(gt=0)
    timestamp: datetime = Field(default_factory=datetime.now)
    current_green_signal: SignalDirection
    high_traffic_road: SignalDirection
    north_signal: TrafficSignalTiming
    south_signal: TrafficSignalTiming
    east_signal: TrafficSignalTiming
    west_signal: TrafficSignalTiming
    total_cars: int
    average_wait_time: float
    efficiency_score: float

    def calculate_efficiency(self) -> float:
        total = self.total_cars
        traffic_penalty = (total / 400) * 50

        wait_times = [
            self.north_signal.last_time,
            self.south_signal.last_time,
            self.east_signal.last_time,
            self.west_signal.last_time,
        ]
        avg = sum(wait_times) / 4
        variance = sum((w - avg) ** 2 for w in wait_times) / 4
        balance_score = max(0, 50 - variance)

        return round(max(0, min(100, balance_score - traffic_penalty)), 2)

    class Config:
        use_enum_values = True
