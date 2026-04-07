import numpy as np

class BaseEVModel:
    """
    Base class for EV RL Environments:
    - battery_level (0–100 %)
    - speed (0–120 km/h)
    - distance_remaining (km)
    - charging_station_distance (km)
    """

    def __init__(self, battery_capacity=50, max_speed=90, traffic_factor=0.5):
        self.battery_capacity = battery_capacity
        self.max_speed = max_speed
        self.traffic_factor = traffic_factor
        self.reset()

    def reset(self):
        self.battery_level = self.battery_capacity
        self.speed = 0
        self.distance_remaining = 40      # route length (km)
        self.charging_station_distance = 10  # next station (km)
        return self._get_obs()

    def _get_obs(self):
        return np.array([
            self.battery_level / self.battery_capacity,  # normalized 0–1
            self.speed / self.max_speed,                 # normalized
            self.distance_remaining / 40,                # normalized
            self.charging_station_distance / 10          # normalized
        ], dtype=np.float32)

    def _apply_physics(self, action_speed):
        energy_consumption = action_speed * (1 + self.traffic_factor * 0.5)
        self.battery_level -= energy_consumption * 0.05
        self.battery_level = max(0, self.battery_level)

        self.speed = action_speed
        distance_covered = self.speed * 0.1
        self.distance_remaining = max(0, self.distance_remaining - distance_covered)

        self.charging_station_distance -= distance_covered

        if self.charging_station_distance <= 0:
            self.charging_station_distance = 10  # new station every 10 km

    def step(self, action_speed):
        self._apply_physics(action_speed)

        done = False
        reward = 0

        if self.distance_remaining <= 0:
            reward += 100   # reached destination
            done = True

        if self.battery_level <= 0:
            reward -= 50    # battery empty
            done = True

        reward += self.speed * 0.1       # fast progress
        reward += self.battery_level * 0.01  # conserve battery

        return self._get_obs(), reward, done, {}