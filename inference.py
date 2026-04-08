import os
import json
import time
import yaml
import requests
from openai import OpenAI

# ============================================================
# Load Required Env Vars
# ============================================================

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME   = os.getenv("MODEL_NAME")
HF_TOKEN     = os.getenv("HF_TOKEN")

if not API_BASE_URL or not MODEL_NAME or not HF_TOKEN:
    raise RuntimeError("Missing required environment variables API_BASE_URL / MODEL_NAME / HF_TOKEN")

client = OpenAI(
    api_key=HF_TOKEN,
    base_url=API_BASE_URL
)

# ============================================================
# Load openenv.yaml Task List
# ============================================================

with open("openenv.yaml", "r") as f:
    spec = yaml.safe_load(f)

TASKS = spec.get("tasks", [])

ENV_URL = "http://localhost:7860"

# ============================================================
# Environment API
# ============================================================

def env_reset(env_id):
    r = requests.post(f"{ENV_URL}/reset", json={"env_id": env_id})
    r.raise_for_status()
    return r.json()

def env_step(action):
    r = requests.post(f"{ENV_URL}/step", json={"action": action})
    r.raise_for_status()
    return r.json()

def env_state():
    r = requests.get(f"{ENV_URL}/state")
    r.raise_for_status()
    return r.json()

# ============================================================
# Ask LLM for Action
# ============================================================

def llm_action(observation):
    msg = [
        {"role": "system",
         "content": "You are an RL agent. Output only a float in [0,1]. Nothing else."},
        {"role": "user",
         "content": f"Observation: {json.dumps(observation)}. Give next action:"}
    ]

    try:
        out = client.chat.completions.create(
            model=MODEL_NAME,
            messages=msg,
            temperature=0
        )
        ans = out.choices[0].message.content.strip()
        return float(ans)
    except:
        return 0.0

# ============================================================
# Task Loop
# ============================================================

def run_task(task):

    task_id = task["id"]
    env_id  = task["env"]

    # --------------------
    # START BLOCK
    # --------------------
    print("[START]")
    print(f"task: {task_id}")
    print(f"env: {env_id}")
    print(f"model: {MODEL_NAME}")
    print("metadata: {}")
    print("", flush=True)

    obs = env_reset(env_id)
    done = False
    total_reward = 0.0
    step_num = 0

    while not done:

        action = llm_action(obs)

        result = env_step(action)

        obs = result.get("observation", obs)
        reward = float(result.get("reward", 0.0))
        done = bool(result.get("done", False))

        total_reward += reward
        step_num += 1

        # --------------------
        # STEP BLOCK
        # --------------------
        print("[STEP]")
        print(f"step: {step_num}")
        print(f"action: {action}")
        print(f"reward: {reward}")
        print(f"done: {str(done).lower()}")
        print(f"observation: {json.dumps(obs)}")
        print("", flush=True)

        if step_num > 1000:
            break

    # --------------------
    # END BLOCK
    # --------------------
    print("[END]")
    print(f"task: {task_id}")
    print(f"env: {env_id}")
    print(f"score: {total_reward}")
    print("", flush=True)


# ============================================================
# RUN ALL TASKS
# ============================================================

if __name__ == "__main__":
    for task in TASKS:
        run_task(task)
        time.sleep(1)