import streamlit as st
from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

ENV_MAP = {
    "Easy": EasyEVEnv,
    "Medium": MediumEVEnv,
    "Hard": HardEVEnv,
}

WEATHER_NAMES = {
    0: "☀️ Clear — Safe driving, low battery drain",
    1: "🌧 Rain — Reduced speed, higher battery drain",
    2: "⛈ Storm — Very low speed, heavy battery drain"
}

def convert_obs_to_dict(obs):
    speed, battery, distance, weather_code = obs
    return {
        "Speed (km/h)": float(speed),
        "Battery (%)": float(battery),
        "Distance Remaining (km)": float(distance),
        "Weather": WEATHER_NAMES.get(int(weather_code), "Unknown"),
    }

st.title("⚡ EV Routing RL Environment (Interactive GUI)")

# ------------------------------
# EXPANDED DETAILED INSTRUCTIONS
# ------------------------------
with st.expander("📘 FULL INSTRUCTIONS (Highly Recommended)"):
    st.markdown("""
## 🔹 Action Meaning
| Action | Meaning |
|--------|---------|
| **0.0** | No throttle (slowest, battery efficient) |
| **1.0** | Full throttle (fastest, drains battery more) |
| **0.5** | Medium acceleration |

The throttle controls **speed directly**.

---

## 🔹 Observation Meaning
| Field | Meaning |
|-------|---------|
| **Speed (km/h)** | Current vehicle speed after throttle & weather limit |
| **Battery (%)** | Remaining battery capacity |
| **Distance Remaining (km)** | How far the EV is from the goal |
| **Weather** | Clear → Easy, Rain → Medium, Storm → Hard |

---

## 🔹 Weather Effects
### ☀️ Clear  
- Normal speed  
- Normal battery usage  

### 🌧 Rain  
- Speed limited to **70%**  
- Battery drains **20% faster**

### ⛈ Storm  
- Speed limited to **40%**  
- Battery drains **50% faster**  

---

## 🔹 Reward System
Reward = **progress** – **battery penalty**

You get points for:
- decreasing distance

You lose points for:
- wasting battery  
- driving fast in storm  

Hard mode amplifies penalties.

---

## 🔹 Difficulty Levels
### 🟢 Easy
- High battery  
- Low traffic  
- Mostly clear weather  

### 🟡 Medium
- Balanced  
- Random rain  

### 🔴 Hard (Frontier Challenge)
- Low battery  
- Heavy traffic  
- Many storm events  
- Highest penalty rates  

---

""")

# -----------------------------
# UI Controls
# -----------------------------

env_name = st.sidebar.selectbox("Choose Environment", ["Easy", "Medium", "Hard"])
env = ENV_MAP[env_name]()

if st.sidebar.button("Reset Environment"):
    obs = env.reset()
    st.session_state["obs"] = obs
    st.session_state["done"] = False

if "obs" not in st.session_state:
    st.session_state["obs"] = env.reset()
    st.session_state["done"] = False

obs = st.session_state["obs"]

st.subheader("🔍 Observation")
st.table(convert_obs_to_dict(obs))

action = st.slider("Action (Throttle)", 0.0, 1.0, 0.5, 0.1)

if st.button("Step"):
    if not st.session_state["done"]:
        new_obs, reward, done, _ = env.step(action)
        st.session_state["obs"] = new_obs
        st.session_state["done"] = done

        st.success(f"Reward: **{reward:.3f}** | Done: **{done}**")
        st.table(convert_obs_to_dict(new_obs))
    else:
        st.warning("Episode finished. Please reset.")