import sqlite3
from models.traffic_models import (
    TrafficSignalTiming,
    TrafficCycleData,
    SignalDirection,
)

DB_PATH = "database/signalData.db"

def init_db():
    """Initialize database and create signal_cycles table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS signal_cycles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cycle_number INTEGER,
            north_current_time INTEGER,
            north_last_time INTEGER,
            south_current_time INTEGER,
            south_last_time INTEGER,
            east_current_time INTEGER,
            east_last_time INTEGER,
            west_current_time INTEGER,
            west_last_time INTEGER,
            current_green_signal TEXT,
            high_traffic_road TEXT,
            north_cars INTEGER,
            south_cars INTEGER,
            east_cars INTEGER,
            west_cars INTEGER,
            efficiency_score REAL
        )
    """)
    conn.commit()
    conn.close()


def save_cycle(agent):
    """Save the current cycle data from the agent to the database."""
    # Create Pydantic TrafficSignalTiming objects
    north = TrafficSignalTiming(
        direction=SignalDirection.NORTH,
        current_time=agent.green_timings["north"]["current"],
        last_time=agent.green_timings["north"]["last"],
        car_count=agent.traffic_counts["north"]
    )
    south = TrafficSignalTiming(
        direction=SignalDirection.SOUTH,
        current_time=agent.green_timings["south"]["current"],
        last_time=agent.green_timings["south"]["last"],
        car_count=agent.traffic_counts["south"]
    )
    east = TrafficSignalTiming(
        direction=SignalDirection.EAST,
        current_time=agent.green_timings["east"]["current"],
        last_time=agent.green_timings["east"]["last"],
        car_count=agent.traffic_counts["east"]
    )
    west = TrafficSignalTiming(
        direction=SignalDirection.WEST,
        current_time=agent.green_timings["west"]["current"],
        last_time=agent.green_timings["west"]["last"],
        car_count=agent.traffic_counts["west"]
    )

    # Create TrafficCycleData object
    cycle = TrafficCycleData(
        cycle_number=agent.cycle_number,
        current_green_signal=agent.current_green,
        high_traffic_road=agent.high_traffic_road,
        north_signal=north,
        south_signal=south,
        east_signal=east,
        west_signal=west,
        total_cars=sum(agent.traffic_counts.values()),
        average_wait_time=sum(v["last"] for v in agent.green_timings.values()) / 4,
        efficiency_score=0
    )

    # Calculate efficiency
    cycle.efficiency_score = cycle.calculate_efficiency()

    # Insert into database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO signal_cycles (
            cycle_number,
            north_current_time,
            north_last_time,
            south_current_time,
            south_last_time,
            east_current_time,
            east_last_time,
            west_current_time,
            west_last_time,
            current_green_signal,
            high_traffic_road,
            north_cars,
            south_cars,
            east_cars,
            west_cars,
            efficiency_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        cycle.cycle_number,
        cycle.north_signal.current_time,
        cycle.north_signal.last_time,
        cycle.south_signal.current_time,
        cycle.south_signal.last_time,
        cycle.east_signal.current_time,
        cycle.east_signal.last_time,
        cycle.west_signal.current_time,
        cycle.west_signal.last_time,
        cycle.current_green_signal,
        cycle.high_traffic_road,
        cycle.north_signal.car_count,
        cycle.south_signal.car_count,
        cycle.east_signal.car_count,
        cycle.west_signal.car_count,
        cycle.efficiency_score
    ))
    conn.commit()
    conn.close()

    return cycle


