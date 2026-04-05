import numpy as np
from .base_env import BaseEVEnv

class MediumEVRouteEnv(BaseEVEnv):
    """
    Medium Task:
    EV routing with traffic factor + charging cost.
    Action: [chosen_speed, chosen_charger_type]
    Reward: time_penalty + charging_cost_penalty
    """

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.distance = self.rng.uniform(10, 50)
        self.traffic = self.rng.uniform(0.8, 2.0)      # multiplier
        self.battery = self.rng.uniform(40, 100)        # %
        self.observation = np.array([self.distance, self.traffic, self.battery])
        return self.observation

    def step(self, action):
        speed, charger = action   # charger: 0=slow,1=fast
        
        travel_time = self.distance / speed * self.traffic
        
        energy_used = 0.25 * self.distance
        self.battery -= energy_used

        charge_cost = 5 if charger == 0 else 12
        
        reward = -(travel_time + charge_cost)

        done = True

        return self.observation, reward, done, {
            "travel_time": travel_time,
            "charge_cost": charge_cost,
        }