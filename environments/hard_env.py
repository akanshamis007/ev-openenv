import numpy as np
from environments.base_ev_model import BaseEVEnv

class HardEVFleetEnv(BaseEVEnv):
    """
    Hard Task:
    Choose route + charging + speed to minimize total cost.
    Multi-step episode.
    """

    def __init__(self):
        super().__init__()
        self.step_id = 0
        self.reset()

    def reset(self):
        self.total_reward = 0
        self.battery = 80
        self.distance_left = self.rng.uniform(100, 200)
        self.traffic = self.rng.uniform(0.5, 2.5)
        self.step_id = 0

        self.observation = np.array([self.distance_left, self.battery, self.traffic])
        return self.observation

    def step(self, action):
        speed, charger = action

        # Travel
        distance_step = speed * 0.2
        self.distance_left -= distance_step
        energy_used = 0.3 * distance_step
        self.battery -= energy_used
        
        # Charging
        if charger == 1:
            self.battery = min(100, self.battery + 20)
            cost = 15
        else:
            cost = 0

        # Reward = negative total time + penalties
        travel_time = distance_step / speed * self.traffic
        reward = -(travel_time + cost)

        self.total_reward += reward
        self.step_id += 1

        done = (self.distance_left <= 0) or (self.battery <= 0) or (self.step_id >= 20)

        self.observation = np.array([self.distance_left, self.battery, self.traffic])

        return self.observation, reward, done, {
            "total_reward": self.total_reward,
            "battery": self.battery,
            "distance_left": self.distance_left
        }