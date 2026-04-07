from fastapi import FastAPI
from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

app = FastAPI()

def get_env(name):
    if name == "easy": return EasyEVEnv()
    if name == "medium": return MediumEVEnv()
    if name == "hard": return HardEVEnv()
    raise ValueError("Unknown environment")

@app.get("/")
def index():
    return {"message": "EV Routing RL Environment Ready", "envs": ["easy","medium","hard"]}

@app.get("/reset/{env_name}")
def reset(env_name: str):
    env = get_env(env_name)
    obs = env.reset()
    return {"obs": obs.tolist()}

@app.get("/step/{env_name}/{action}")
def step(env_name: str, action: float):
    env = get_env(env_name)
    obs, reward, done, info = env.step(action)
    return {
        "obs": obs.tolist(),
        "reward": reward,
        "done": done
    }

