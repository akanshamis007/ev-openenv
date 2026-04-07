import numpy as np
import gym

class BaseEVModel(gym.Env):

    WEATHER_CLEAR = 0
    WEATHER_RAIN = 1
    WEATHER_STORM = 2

    WEATHER_NAMES = {
        WEATHER_CLEAR: "☀️ Clear",
        WEATHER_RAIN: "🌧 Rain",
        WEATHER_STORM: "⛈ Storm",
    }

    WEATHER_SPEED_LIMIT = {
        WEATHER_CLEAR: 1.0,
        WEATHER_RAIN: 0.7,
        WEATHER_STORM: 0.4,
    }

    WEATHER_BATTERY_DRAIN = {
        WEATHER_CLEAR: 1.0,
        WEATHER_RAIN: 1.2,
        WEATHER_STORM: 1.5,
    }

    def __init__(self, battery_capacity, max_speed, traffic_factor):
        super().__init__()

        # Config
        self.battery_capacity = battery_capacity
        self.max_speed = max_speed
        self.traffic_factor = traffic_factor

        # Gym spaces
        self.action_space = gym.spaces.Box(low=0.0, high=1.0, shape=(1,))
        self.observation_space = gym.spaces.Box(
            low=np.array([0, 0, 0, 0]),
            high=np.array([max_speed, battery_capacity, 200, 2])
        )

        self.reset()

    def reset(self):
        self.battery = float(self.battery_capacity)
        self.distance = 100.0      # km to destination
        self.speed = 0.0
        self.weather_mode = np.random.choice([0, 1, 2])  # 0=clear,1=rain,2=storm
        return self._get_obs()

    def _get_obs(self):
        return np.array([
            self.speed,
            self.battery,
            self.distance,
            self.weather_mode,
        ], dtype=float)

    def step(self, action):
        throttle = float(np.clip(action, 0, 1))

        # Speed based on throttle
        weather_speed_limit = self.WEATHER_SPEED_LIMIT[self.weather_mode]
        self.speed = throttle * self.max_speed * weather_speed_limit

        # Battery drain
        drain_factor = self.WEATHER_BATTERY_DRAIN[self.weather_mode]
        self.battery -= (self.speed / 10) * drain_factor

        # Distance reduction
        distance_reduction = (self.speed * (1 - self.traffic_factor)) / 10
        self.distance -= distance_reduction

        # Reward = progress - penalty
        reward = distance_reduction * 0.05 - max(0, -self.battery) * 0.001

        done = False
        if self.distance <= 0:
            reward += 5
            done = True
        if self.battery <= 0:
            reward -= 5
            done = True

        return self._get_obs(), reward, done, {}