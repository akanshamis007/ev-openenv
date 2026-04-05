---
title: Open Ev Env
emoji: 👁
colorFrom: indigo
colorTo: yellow
sdk: docker
pinned: false
license: mit
short_description: A 3-task real-world EV (Electric Vehicle) environment
app_file: app.py
---

# ⚡ Open-EV: Real-World EV Decision-Making RL Environment

A complete RL-ready simulation suite for Electric Vehicles.

Built for the OpenEV × Meta × Scaler School Hackathon.

🛰️ 📌 Overview

This repository contains 3 fully-implemented real-world EV RL environments, each exposing a clean Gym-style API:

obs = env.reset()
obs, reward, done, info = env.step(action)
state = env.state()

Unlike toy RL tasks, these are practical EV problems that require:
✔ real-world constraints
✔ noisy observations
✔ multi-step planning
✔ non-trivial reward shaping

All tasks are runnable directly on Hugging Face Spaces using Docker.

🗂️ Folder Structure
open_ev_env/
│
├── app.py                 # FastAPI demo + baseline inference
├── Dockerfile
├── requirements.txt
├── README.md
│
└── environments/
    ├── __init__.py
    ├── base_env.py
    ├── easy_env.py
    ├── medium_env.py
    ├── hard_env.py
🧭 Environment Suite

Below is the complete description of the three RL tasks included.

🍃 1. Easy Task: Optimal Charging Station Selection
(Fast, Single-Step Decision with Real Metrics)
🎯 Goal:

Choose the best charging station among multiple options.

Agent observes:
Distance to station
Queue length / wait time
Charging speed
Charging cost
Action:

Select one station (Discrete: N)

Reward Function:
reward = -distance - wait_time + charging_speed - cost
Episode ends:

After 1 action → deterministic, small.

🧠 Example Observation
{
  "station_1": [0.4, 0.2, 0.8, 0.5],
  "station_2": [0.3, 0.1, 0.6, 0.7]
}
ASCII Diagram
       (You)
         |
   -----------------------
   |         |           |
Station A  Station B   Station C
 dist=3     dist=5      dist=1
 cost=low   cost=high   cost=mid
🛣️ 2. Medium Task: Trip Energy Management
(Continuous control over speed and energy budget)
🎯 Goal:

Drive an EV across a route without running out of battery while minimizing energy waste.

Agent observes:
Battery level (SOC)
Distance to next checkpoint
Current speed
Charger availability on route
Action Space:

Continuous speed control

speed_change ∈ [-1, +1]
Rewards:

✔ positive for forward progress
✔ penalty for high energy waste
✔ big penalty for battery < 5%

ASCII Diagram
[Start] ----(20km)---- [Charger] ----(30km)---- [End]
   | SOC=100%           | SOC=70%             | Target
🌆 3. Hard Task: City EV Navigation Under Constraints
(Grid navigation with traffic, SOC, noisy observations)
🎯 Goal:

Navigate a city grid → reach destination with sufficient battery.

Challenges:
Traffic zones
High-drain segments
Charger scarcity
Partial observability
Action Space (Discrete)
0 = up
1 = down
2 = left
3 = right
ASCII Map
+--------- City Grid ----------+
| A | . | T | . | C | . |  E   |
| . | T | . | . | T | . |  .   |
| . | . | C | . | . | T |  .   |
| S | . | . | C | . | . |  .   |
+------------------------------+

S = Start  
E = End  
T = Traffic  
C = Charger  
. = free road  
🧱 Core Architecture
BaseEnv (shared utilities)
   ├── EasyEnv     (discrete, single-step)
   ├── MediumEnv   (continuous, multi-step)
   └── HardEnv     (grid world, partially observable)

Each environment implements:

reset()
step(action)
state()
reward shaping
done conditions
🧪 Baseline Inference Script

The included app.py runs all 3 tasks with a simple policy.

Example output:
Easy task score: 1.22
Medium task score: 38.7
Hard task score: 12.4
🔌 Quick Start (Local)
pip install -r requirements.txt
python app.py
🚀 Deploy on Hugging Face Spaces

This Space uses Docker.

Required files:
Dockerfile
requirements.txt
app.py
environments/ folder

After pushing your repo:

Your app runs on:

http://<your_space>.hf.space:7860
🧮 Scoring System
Factor	Reward
Progress	+1 per step
Energy efficiency	0.2 × saved kWh
Stopping at charger	+5
Running out of battery	-20
Traffic penalty	-1 each

🏆 Why This Project Is Unique

✔ Real-world EV problems, not games
✔ Multi-task suite → easy/medium/hard
✔ Handles partial observability
✔ Includes deterministic baseline
✔ Fully containerized

👤 Authors

Akansha Mishra
OpenEV RL Hackathon Participant
Hugging Face: AKANSHA18
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
