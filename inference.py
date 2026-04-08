import os
import json
import time
from openai import OpenAI
import requests
import yaml

# ============================================================
# Load ENV VARS (MANDATORY for validator)
# ============================================================

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME   = os.getenv("MODEL_NAME")
HF_TOKEN     = os.getenv("HF_TOKEN")

if not API_BASE_URL or not MODEL_NAME or not HF_TOKEN:
    raise RuntimeError("Missing required environment variables: API_BASE_URL, MODEL_NAME, HF_TOKEN")

# OpenAI client
client = OpenAI(
    api_key=HF_TOKEN,
    base_url=API_BASE_URL
)

# ============================================================
# Load tasks from openenv.yaml
# ============================================================

with open("openenv.yaml", "r") as f:
    spec = yaml.safe_load(f)

TASKS = [t["id"] for t in spec.get("tasks", [])]
ENV_URL = "http://localhost:7860"     # HF Space server internal URL

# ============================================================
# Helper: call the environment endpoints
# ============================================================

def env_reset():
    r = requests.post(f"{ENV_URL}/reset")
    return r.json()

def env_state():
    r = requests.get(f"{ENV_URL}/state")
    return r.json()

def env_step(action):
    r = requests.post(f"{ENV_URL}/step", json={"action": action})
    return r.json()

# ============================================================
# Helper: Ask LLM for action
# ============================================================

def llm_action(observation):
    """Query LLM to choose an action"""
    try:
        msg = [
            {"role": "system", "content": "You are a reinforcement learning agent. Respond ONLY with an integer action."},
            {"role": "user", "content": f"Observation: {json.dumps(observation)}. Give next action:"}
        ]

        out = client.chat.completions.create(
            model=MODEL_NAME,
            messages=msg,
            temperature=0
        )

        ans = out.choices[0].message.content.strip()

        # Convert to integer safely
        return int(ans)

    except Exception:
        return 0   # Fallback safe action


# ============================================================
# MAIN LOOP FOR ALL TASKS
# ============================================================

def run_task(task_id):

    # Start log
    print(f'[START] {json.dumps({"task_id": task_id})}', flush=True)

    obs = env_reset()
    done = False
    total_reward = 0.0
    step_count = 0

    while not done:
        action = llm_action(obs)
        result = env_step(action)

        obs = result.get("observation", obs)
        reward = float(result.get("reward", 0))
        done = bool(result.get("done", False))

        total_reward += reward
        step_count += 1

        # STEP LOG (required)
        print(
            f'[STEP] {json.dumps({"observation": obs, "action": action, "reward": reward})}',
            flush=True
        )

        # Safety break if env misconfigured
        if step_count > 1000:
            break

    # END LOG (required)
    print(
        f'[END] {json.dumps({"task_id": task_id, "score": total_reward})}',
        flush=True
    )


# ============================================================
# RUN ALL TASKS SEQUENTIALLY
# ============================================================

if __name__ == "__main__":
    for tid in TASKS:
        run_task(tid)
        time.sleep(1)