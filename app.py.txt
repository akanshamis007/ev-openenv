from fastapi import FastAPI
from environments.easy_env import EasyEVRouteEnv
from environments.medium_env import MediumEVRouteEnv
from environments.hard_env import HardEVFleetEnv

app = FastAPI()

envs = {
    "easy": EasyEVRouteEnv(),
    "medium": MediumEVRouteEnv(),
    "hard": HardEVFleetEnv()
}

@app.get("/")
def home():
    return {"message": "EV Routing + Charging RL Environments Ready"}

@app.get("/reset/{level}")
def reset(level: str):
    obs = envs[level].reset().tolist()
    return {"observation": obs}

@app.post("/step/{level}")
def step(level: str, action: list):
    obs, reward, done, info = envs[level].step(action)
    return {
        "observation": obs.tolist(),
        "reward": reward,
        "done": done,
        "info": info
    }