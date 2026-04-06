import gradio as gr
from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

active_env = None
ENV_MAP = {
    "easy": EasyEVEnv,
    "medium": MediumEVEnv,
    "hard": HardEVEnv
}

def reset_env(env_type):
    global active_env
    active_env = ENV_MAP[env_type]()
    obs = active_env.reset()
    return f"Environment reset: {env_type}\nInitial State: {obs}"

def step_env(action):
    global active_env
    if active_env is None:
        return "❌ Please reset the environment first!"
    obs, reward, done, info = active_env.step(float(action))
    return f"""
Observation: {obs}
Reward: {reward}
Done: {done}
Info: {info}
"""

with gr.Blocks() as demo:
    gr.Markdown("# ⚡ Open EV RL GUI Environment")
    gr.Markdown("Interact with real EV routing & charging tasks")

    env_choice = gr.Dropdown(["easy","medium","hard"], label="Select Environment")

    reset_btn = gr.Button("Reset Environment")
    reset_output = gr.Textbox(label="Environment Output")

    action_number = gr.Number(label="Enter Action")
    step_btn = gr.Button("Take Step")
    step_output = gr.Textbox(label="Step Output")

    reset_btn.click(reset_env, inputs=[env_choice], outputs=[reset_output])
    step_btn.click(step_env, inputs=[action_number], outputs=[step_output])

demo.launch(server_name="0.0.0.0", server_port=7860)