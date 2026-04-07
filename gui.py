import streamlit as st
from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

ENV_MAP = {
    "easy": EasyEVEnv,
    "medium": MediumEVEnv,
    "hard": HardEVEnv
}

st.title("🔋 EV RL Environment Simulator")

env_choice = st.selectbox("Select Environment", ["easy", "medium", "hard"])
env = ENV_MAP[env_choice]()

if st.button("Reset Environment"):
    st.session_state["obs"] = env.reset()

if "obs" not in st.session_state:
    st.session_state["obs"] = env.reset()

st.subheader("Observation")
st.write(st.session_state["obs"])

action = st.slider("Action (0 → no throttle, 1 → full throttle)", 0.0, 1.0, 0.5)

if st.button("Step"):
    obs, reward, done, _ = env.step(action)
    st.session_state["obs"] = obs
    st.write("Reward:", reward)
    st.write("Done:", done)

    if done:
        st.success("Episode finished. Reset to start again.")