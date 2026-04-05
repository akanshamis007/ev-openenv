import requests
import random

BASE = "http://localhost:7860"

def run_env(level):
    print("Running level:", level)
    r = requests.get(f"{BASE}/reset/{level}").json()
    obs = r["observation"]
    done = False

    while not done:
        action = [random.uniform(20,80), random.randint(0,1)]
        resp = requests.post(f"{BASE}/step/{level}", json=action).json()
        obs = resp["observation"]
        done = resp["done"]
        print(resp)

if __name__ == "__main__":
    run_env("easy")
    run_env("medium")
    run_env("hard")