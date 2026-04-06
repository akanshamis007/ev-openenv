import streamlit as st
from environments.easy_env import EasyEVEnv

st.title("⚡ Open EV Environment GUI")

if st.button("Create Environment"):
    env = EasyEVEnv()
    st.success("Environment Created!")
    st.write("Observation:", env.reset())

