from fastapi import FastAPI
from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

app = FastAPI()

@app.get("/")
def greet_json():
    return {
        "message": "EV Routing + Charging RL Environments Ready",
        "available_envs": ["easy", "medium", "hard"]
    }

@app.get("/reset/{env_name}")
def reset_env(env_name: str):
    env = get_env(env_name)
    obs = env.reset()
    return {"observation": obs.tolist()}

@app.get("/step/{env_name}/{action}")
def step_env(env_name: str, action: float):
    env = get_env(env_name)
    obs, reward, done, info = env.step(float(action))
    return {
        "observation": obs.tolist(),
        "reward": reward,
        "done": done
    }

def get_env(name):
    if name == "easy": return EasyEVEnv()
    if name == "medium": return MediumEVEnv()
    if name == "hard": return HardEVEnv()
    raise ValueError("Unknown env")

