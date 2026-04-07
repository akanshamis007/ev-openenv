import streamlit as st
import numpy as np
from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

st.title("⚡ EV RL Environment Dashboard")

env_name = st.selectbox("Select Environment", ["easy","medium","hard"])

def get_env(name):
    if name == "easy": return EasyEVEnv()
    if name == "medium": return MediumEVEnv()
    if name == "hard": return HardEVEnv()

env = get_env(env_name)

if st.button("Reset Environment"):
    obs = env.reset()
    st.write("Initial Observation:", obs)

action = st.slider("Action (0–1)", 0.0, 1.0, 0.5)

if st.button("Step"):
    obs, reward, done, info = env.step(float(action))
    st.write("Observation:", obs)
    st.write("Reward:", reward)
    st.write("Done:", done)