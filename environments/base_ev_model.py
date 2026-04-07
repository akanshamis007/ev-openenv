import numpy as np
import random

class BaseEVModel:
    """
    Base class for all EV RL environments.
    Action: float in [0,1] = speed scaling
    Observation: [battery, distance_left, traffic, weather_mode]
    """

    WEATHER_MODES = {
        "clear": 1.00,
        "cloudy": 1.05,
        "rain": 1.10,
    }
    WEATHER_LIST = ["clear", "cloudy", "rain"]

    def __init__(self, battery_capacity, route_length, traffic_factor):
        self.battery_capacity = battery_capacity
        self.route_length = route_length
        self.traffic_factor = traffic_factor

        self.battery = None
        self.distance_left = None
        self.weather_mode = None

    def reset(self):
        self.battery = self.battery_capacity
        self.distance_left = self.route_length
        self.weather_mode = random.choice(self.WEATHER_LIST)

        return self._get_obs()

    def step(self, action):
        action = float(np.clip(action, 0.0, 1.0))

        # stochastic weather transitions (hard mode uses 0.2 probability)
        if random.random() < 0.2:
            self.weather_mode = random.choice(self.WEATHER_LIST)

        weather_factor = self.WEATHER_MODES[self.weather_mode]

        # consumption grows with speed * traffic * weather
        consumption = (0.5 + action) * self.traffic_factor * 5 * weather_factor

        # movement reduces with traffic + weather
        move = (action * 5) / (self.traffic_factor * weather_factor)

        self.battery -= consumption
        self.distance_left -= move

        done = False
        reward = 0

        if self.distance_left <= 0:
            reward = 1.0
            done = True

        if self.battery <= 0:
            reward = -1.0
            done = True

        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        weather_idx = self.WEATHER_LIST.index(self.weather_mode)
        return np.array([
            round(self.battery, 2),
            round(self.distance_left, 2),
            round(self.traffic_factor, 2),
            weather_idx
        ], dtype=float)