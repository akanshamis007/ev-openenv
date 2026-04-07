import gradio as gr
import requests

API_URL = "http://0.0.0.0:7860"   # HF internal API

# -------------------------------
# Helper functions to call backend
# -------------------------------

def backend_reset(env_name):
    try:
        res = requests.get(f"{API_URL}/reset?env={env_name}").json()
        return res
    except Exception as e:
        return {"error": str(e)}

def backend_step(env_name, action):
    try:
        res = requests.get(f"{API_URL}/step?env={env_name}&action={action}").json()
        return res
    except Exception as e:
        return {"error": str(e)}

# -----------------------------------
# Convert observation → 2D Grid Image
# -----------------------------------

import numpy as np
from PIL import Image, ImageDraw

GRID_SIZE = 500
CELL = 50

def draw_map(observation):
    """
    observation = {
       "ev_position": [x, y],
       "charging_stations": [[x1,y1], [x2,y2]],
       "destination": [x,y],
       ...
    }
    """
    canvas = Image.new("RGB", (GRID_SIZE, GRID_SIZE), "white")
    draw = ImageDraw.Draw(canvas)

    # Draw grid
    for i in range(0, GRID_SIZE, CELL):
        draw.line((i,0,i,GRID_SIZE), fill="lightgray")
        draw.line((0,i,GRID_SIZE,i), fill="lightgray")

    # Charging Stations
    for cs in observation.get("charging_stations", []):
        x = cs[0] * CELL
        y = cs[1] * CELL
        draw.rectangle((x, y, x+CELL, y+CELL), fill="blue")
    
    # Destination
    if "destination" in observation:
        x = observation["destination"][0] * CELL
        y = observation["destination"][1] * CELL
        draw.rectangle((x, y, x+CELL, y+CELL), fill="green")

    # EV Position
    if "ev_position" in observation:
        x = observation["ev_position"][0] * CELL
        y = observation["ev_position"][1] * CELL
        draw.rectangle((x, y, x+CELL, y+CELL), fill="red")

    return canvas

# ---------------------
# GUI Logic
# ---------------------

def reset(env):
    res = backend_reset(env)
    if "observation" in res:
        img = draw_map(res["observation"])
        return img, str(res["observation"]), "Environment Reset!"
    return None, "Error", str(res)

def step(env, action):
    res = backend_step(env, action)
    if "observation" in res:
        img = draw_map(res["observation"])
        reward = res.get("reward", 0)
        done = res.get("done", False)

        info = f"Reward: {reward}\nDone: {done}\nInfo: {res.get('info','')}"
        return img, str(res["observation"]), info

    return None, "Error", str(res)


# ------------------------------
# Gradio GUI Layout
# ------------------------------

with gr.Blocks(title="EV Routing RL Environment") as demo:
    gr.Markdown("# 🚗 EV Routing + Charging RL Environment (GUI)")

    with gr.Row():
        env_dropdown = gr.Dropdown(["easy", "medium", "hard"], label="Select Environment")

    with gr.Row():
        btn_reset = gr.Button("🔄 Reset Environment")
        btn_up = gr.Button("⬆️ Move Up (0)")
        btn_down = gr.Button("⬇️ Move Down (1)")
        btn_left = gr.Button("⬅️ Move Left (2)")
        btn_right = gr.Button("➡️ Move Right (3)")
        btn_charge = gr.Button("🔌 Charge EV (4)")

    with gr.Row():
        map_output = gr.Image(label="EV Map", type="pil")
        obs_output = gr.Textbox(label="Observation")
        info_output = gr.Textbox(label="Info / Reward")

    # Button logic
    btn_reset.click(fn=reset, inputs=[env_dropdown], outputs=[map_output, obs_output, info_output])
    btn_up.click(fn=step, inputs=[env_dropdown], outputs=[map_output, obs_output, info_output], kwargs={"action":0})
    btn_down.click(fn=step, inputs=[env_dropdown], outputs=[map_output, obs_output, info_output], kwargs={"action":1})
    btn_left.click(fn=step, inputs=[env_dropdown], outputs=[map_output, obs_output, info_output], kwargs={"action":2})
    btn_right.click(fn=step, inputs=[env_dropdown], outputs=[map_output, obs_output, info_output], kwargs={"action":3})
    btn_charge.click(fn=step, inputs=[env_dropdown], outputs=[map_output, obs_output, info_output], kwargs={"action":4})

demo.launch(server_name="0.0.0.0", server_port=7860)

