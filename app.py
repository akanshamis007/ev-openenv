import json
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import gradio as gr

# Import environments
from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

app = FastAPI()

# Active environment
ENV = EasyEVEnv()

# --------------------------
# API SCHEMA
# --------------------------
class ActionRequest(BaseModel):
    action: float

# --------------------------
# API ROUTES REQUIRED BY OPENENV
# --------------------------

@app.post("/reset")
def reset_env():
    obs = ENV.reset()
    return {"observation": obs}

@app.post("/step")
def step_env(req: ActionRequest):
    obs, reward, done, info = ENV.step(req.action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state_env():
    return {
        "speed": ENV.speed,
        "battery": ENV.battery,
        "distance": ENV.distance,
        "weather": ENV.weather_mode
    }

# --------------------------
# GRADIO GUI
# --------------------------

def gui_reset():
    obs = ENV.reset()
    return f"Reset Successful.\nObservation:\n{obs}"

def gui_step(action):
    obs, reward, done, info = ENV.step(float(action))
    return f"Observation: {obs}\nReward: {reward}\nDone: {done}"

with gr.Blocks() as demo:
    gr.Markdown("# EV OpenEnv GUI")

    reset_btn = gr.Button("Reset")
    out1 = gr.Textbox(label="Output")

    reset_btn.click(fn=gui_reset, outputs=out1)

    action = gr.Slider(0, 1, step=0.1, label="Action (Throttle)")
    step_btn = gr.Button("Step")

    step_btn.click(fn=gui_step, inputs=action, outputs=out1)

# Integrate GUI with FastAPI
app = gr.mount_gradio_app(app, demo, path="/")

# --------------------------
# STARTUP
# --------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

