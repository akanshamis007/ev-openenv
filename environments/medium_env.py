import numpy as np
from .base_ev_model import BaseEVModel

class MediumEVEnv(BaseEVModel):
    """
    Adds action:
    0 = drive slow
    1 = drive medium
    2 = drive fast
    3 = stop and charge
    """
    def __init__(self):
        super().__init__(battery_capacity=60, max_speed=90, traffic_factor=0.3)

    def step(self, action):
        if action == 3:   # charge
            self.battery_level = min(self.battery_capacity, self.battery_level + 5)
            return self._get_obs(), -1, False, {}  # small cost for time

        speed_map = {0: 20, 1: 40, 2: 70}
        speed = speed_map[action]

        return super().step(speed)