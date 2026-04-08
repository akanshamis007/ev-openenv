from fastapi import FastAPI
from pydantic import BaseModel
from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

app = FastAPI()

# Default environment (Easy)
env = EasyEVEnv()

class StepRequest(BaseModel):
    action: float

@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs.tolist()}

@app.get("/state")
def state():
    return {"observation": env._get_obs().tolist()}

@app.post("/step")
def step(req: StepRequest):
    obs, reward, done, _ = env.step(req.action)
    return {
        "observation": obs.tolist(),
        "reward": reward,
        "done": done
    }