import numpy as np
import random

class BaseEVModel:
    WEATHER_MODES = {
        "clear": 1.0,
        "rain": 0.8,
        "storm": 0.6
    }

    def __init__(self, battery_capacity=50, max_speed=60, traffic_factor=0.1, total_distance=40):
        self.battery_capacity = battery_capacity
        self.max_speed = max_speed
        self.traffic_factor = traffic_factor
        self.total_distance = total_distance

        # Guarantee weather_mode is NEVER None
        self.weather_mode = "clear"

        self.reset()

    def reset(self):
        self.battery_level = float(self.battery_capacity)
        self.distance_remaining = float(self.total_distance)
        self.speed = 0.0

        # Always pick a valid weather
        self.weather_mode = random.choice(list(self.WEATHER_MODES.keys()))

        return self._get_obs()

    def _get_obs(self):
        """Return fully named observation dict."""
        return {
            "battery": float(self.battery_level),
            "distance_remaining": float(self.distance_remaining),
            "speed": float(self.speed),
            "weather_mode": self.weather_mode
        }

    def step(self, action):
        """
        action ∈ [0,1] → normalized throttle
        """
        action = float(np.clip(action, 0, 1))

        # Convert action to speed
        self.speed = action * self.max_speed

        # Weather + traffic reduce speed
        weather_factor = self.WEATHER_MODES[self.weather_mode]
        effective_speed = self.speed * weather_factor * (1 - self.traffic_factor)

        # Reduce distance
        self.distance_remaining -= effective_speed * 0.1
        self.distance_remaining = max(self.distance_remaining, 0)

        # Battery consumption
        self.battery_level -= (self.speed / self.max_speed) * 2.0
        self.battery_level = max(self.battery_level, 0)

        # DONE CONDITIONS
        done = False
        reward = 0.0

        # Reward for progress
        reward += (effective_speed / self.max_speed) * 0.1

        # Penalty if battery low
        if self.battery_level <= 0:
            done = True
            reward -= 1.0
        # Goal reached
        elif self.distance_remaining <= 0:
            done = True
            reward += 1.0

        return self._get_obs(), float(reward), done, {}