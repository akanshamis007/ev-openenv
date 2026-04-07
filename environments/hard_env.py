import numpy as np
from .base_ev_model import BaseEVModel

class HardEVEnv(BaseEVModel):
    """
    Hardest version — weather + traffic + battery aging.
    Action: continuous speed (0–1) scaled to (0–120 km/h)
    """
    def __init__(self):
        super().__init__(battery_capacity=70, max_speed=120, traffic_factor=0.5)
        self.weather = 1.0  # 1 = clear,  1.5 = rain, 2 = storm

    def reset(self):
        self.weather = np.random.choice([1.0, 1.3, 1.6])
        return super().reset()

    def step(self, action):
        speed = float(action) * self.max_speed

        # energy penalty from weather
        self.battery_level -= self.weather * 0.3

        obs, reward, done, info = super().step(speed)

        reward -= (self.weather - 1) * 5  # weather penalty

        return obs, reward, done, info