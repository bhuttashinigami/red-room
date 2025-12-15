CREATE TABLE IF NOT EXISTS signal_cycles (
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
    west_cars INTEGER
);
