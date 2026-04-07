import streamlit as st
from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

st.title("⚡ EV RL Environment")

choice = st.selectbox("Select Environment", ["easy", "medium", "hard"])

if choice == "easy": env = EasyEVEnv()
if choice == "medium": env = MediumEVEnv()
if choice == "hard": env = HardEVEnv()

if st.button("Reset"):
    obs = env.reset()
    st.write("Observation:", obs)

action = st.slider("Action (Speed Control 0-1)", 0.0, 1.0, 0.5)

if st.button("Step"):
    obs, reward, done, _ = env.step(action)
    st.write("Obs:", obs)
    st.write("Reward:", reward)
    st.write("Done:", done)