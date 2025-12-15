import random


class TrafficIntersectionAgent:
    def __init__(self, high_traffic_road="north"):
        self.high_traffic_road = high_traffic_road
        self.traffic_counts = {d: random.randint(6, 10) for d in ["north", "south", "east", "west"]}
        self.traffic_counts[high_traffic_road] = random.randint(18, 26)

        self.current_green = "north"
        self.green_time_elapsed = 0
        self.green_timings = {d: {"current": 0, "last": 0} for d in self.traffic_counts}
        self.min_green_time = 5
        self.base_green_time = 10
        self.max_queue = 100
        self.cycle_number = 0

    def calculate_green_time(self, road):
        extra = min(self.traffic_counts[road] // 3, 20)
        return self.base_green_time + extra

    def add_traffic(self):
        for road in self.traffic_counts:
            if road == self.current_green:
                drain = random.randint(4, 8)
                self.traffic_counts[road] = max(0, self.traffic_counts[road] - drain)
            else:
                inc = random.randint(4, 8) if road == self.high_traffic_road else random.randint(1, 3)
                self.traffic_counts[road] = min(self.max_queue, self.traffic_counts[road] + inc)

    def switch_light(self):
        self.green_timings[self.current_green]["last"] = self.green_time_elapsed
        roads = ["north", "east", "south", "west"]
        idx = roads.index(self.current_green)
        self.current_green = roads[(idx + 1) % 4]
        self.green_time_elapsed = 0
        return self.current_green == "north"

    def run_cycle(self):
        self.add_traffic()
        self.green_time_elapsed += 1
        self.green_timings[self.current_green]["current"] = self.green_time_elapsed

        if self.green_time_elapsed >= max(self.min_green_time, self.calculate_green_time(self.current_green)):
            if self.switch_light():
                self.cycle_number += 1
                return True
        return False
