import numpy as np

class BaseEVEnv:
    def __init__(self, seed=42):
        self.rng = np.random.default_rng(seed)

    def reset(self):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError

    def state(self):
        return self.observation