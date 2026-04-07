from easy_ev_env import EasyEVEnv
from medium_ev_env import MediumEVEnv
from hard_ev_env import HardEVEnv


# ---------------------------------------------------------
#      ENV FACTORY
# ---------------------------------------------------------
def load_model(env_name: str):
    """
    env_name: 'easy' | 'medium' | 'hard'
    returns: env instance
    """
    env_name = env_name.lower()

    if env_name == "easy":
        return EasyEVEnv()
    elif env_name == "medium":
        return MediumEVEnv()
    elif env_name == "hard":
        return HardEVEnv()
    else:
        raise ValueError("Invalid environment name. Use: easy, medium, hard.")


# ---------------------------------------------------------
#      PREDICT FUNCTION
# ---------------------------------------------------------
def predict(env, action: float):
    """
    Runs a single step of the EV environment.
    action: float (0–1)
    returns dict: {observation, reward, done}
    """
    obs, reward, done, truncated, info = env.step([action])

    return {
        "observation": obs.tolist(),
        "reward": float(reward),
        "done": bool(done)
    }


# ---------------------------------------------------------
#      TEST EXECUTION (used by HF eval)
# ---------------------------------------------------------
if __name__ == "__main__":
    # choose which env to test
    env = load_model("easy")    # change to "medium" or "hard"
    
    obs, _ = env.reset()
    print("Initial Observation:", obs)

    result = predict(env, 0.5)
    print("After Step:", result)