import numpy as np
from environments.base_ev_model import BaseEVEnv

class EasyEVEnv(BaseEVEnv):
    """
    Easy Task:
    Predict energy needed to move from A → B with random distance + speed.
    Action = predicted energy (kWh)
    Reward = negative absolute error
    """
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.distance = self.rng.uniform(2, 20)     # km
        self.speed = self.rng.uniform(20, 80)       # km/h
        self.true_energy = 0.2 * self.distance + 0.01 * self.speed
        self.observation = np.array([self.distance, self.speed])
        return self.observation

    def step(self, action):
        predicted = float(action)
        error = abs(predicted - self.true_energy)
        reward = -error
        done = True
        return self.observation, reward, done, {"true_energy": self.true_energy}