from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

app = FastAPI()
templates = Jinja2Templates(directory="templates")

active_env = None
ENV_MAP = {
    "easy": EasyEVEnv,
    "medium": MediumEVEnv,
    "hard": HardEVEnv
}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/reset")
def reset_env(env: str):
    global active_env
    if env not in ENV_MAP:
        return {"error": "Invalid environment"}
    active_env = ENV_MAP[env]()
    obs = active_env.reset()
    return {"status": "reset", "env": env, "initial_observation": obs}

@app.post("/step")
async def step_env(action: float = Form(...)):
    global active_env
    if active_env is None:
        return {"error": "Environment not reset"}
    obs, reward, done, info = active_env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }