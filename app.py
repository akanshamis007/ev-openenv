from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

app = FastAPI()

active_env = None

ENV_MAP = {
    "easy": EasyEVEnv,
    "medium": MediumEVEnv,
    "hard": HardEVEnv
}

# ------------------------------
# GUI PAGE
# ------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Open EV RL GUI</title>
    </head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>⚡ Open EV RL Interactive Environment</h1>

        <h3>1. Select Environment</h3>
        <form action="/reset" method="post">
            <select name="env">
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
            </select>
            <button type="submit">Reset Environment</button>
        </form>

        <h3>2. Take Step</h3>
        <form action="/step" method="post">
            Action: <input type="number" name="action" step="0.1">
            <button type="submit">Step</button>
        </form>

        <h3>Output</h3>
        <iframe src="/output" width="100%" height="300px"></iframe>
    </body>
    </html>
    """

# ------------------------------
# OUTPUT PAGE
# ------------------------------
latest_output = "No output yet."

@app.get("/output", response_class=HTMLResponse)
def show_output():
    return f"<pre>{latest_output}</pre>"

# ------------------------------
# RESET ENV
# ------------------------------
@app.post("/reset")
def reset_env(env: str = Form(...)):
    global active_env, latest_output

    active_env = ENV_MAP[env]()
    obs = active_env.reset()

    latest_output = f"Environment reset to {env}\nInitial State: {obs}"
    return HTMLResponse("<script>window.location='/'</script>")

# ------------------------------
# STEP
# ------------------------------
@app.post("/step")
def step_env(action: float = Form(...)):
    global active_env, latest_output

    if active_env is None:
        latest_output = "❗ Error: Reset the environment first."
    else:
        obs, reward, done, info = active_env.step(float(action))
        latest_output = f"Observation: {obs}\nReward: {reward}\nDone: {done}\nInfo: {info}"

    return HTMLResponse("<script>window.location='/'</script>")
