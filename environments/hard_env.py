from .base_ev_model import BaseEVModel
import random

class HardEVEnv(BaseEVModel):
    """Frontier challenge: harsh weather, long distance, random penalties."""

    def __init__(self):
        super().__init__(
            battery_capacity=100,
            max_speed=90,
            traffic_factor=0.25,
            total_distance=120
        )

    def step(self, action):
        # RANDOM event: weather flips mid-episode
        if random.random() < 0.15:
            self.weather_mode = random.choice(list(self.WEATHER_MODES.keys()))

        # RANDOM traffic spikes
        original_traffic = self.traffic_factor
        if random.random() < 0.10:
            self.traffic_factor += 0.2  # sudden jam

        # normal step
        obs, reward, done, info = super().step(action)

        # battery overheating penalty
        if self.speed > 70 and self.battery_level < 40:
            reward -= 0.4

        # restore original traffic
        self.traffic_factor = original_traffic

        return obs, reward, done, info