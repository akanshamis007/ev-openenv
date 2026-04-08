import os
import time
import numpy as np
from graders import ProgressRewardGrader, SafetyPenaltyGrader, BalancedGrader

from environments.easy_env import EasyEVEnv
from environments.medium_env import MediumEVEnv
from environments.hard_env import HardEVEnv

MAX_STEPS = 100


def run_episode(env, grader, task_name, env_name):
    print(f"[START] task={task_name} env={env_name} model=baseline", flush=True)

    obs = env.reset()
    rewards_log = []
    steps_taken = 0
    error_msg = "null"

    for step in range(1, MAX_STEPS + 1):
        # Simple agent → throttle proportional to remaining distance
        throttle = float(min(1.0, obs[2] / 100))

        try:
            obs, reward, done, info = env.step([throttle])
        except Exception as e:
            error_msg = str(e)
            break

        graded_reward = grader.compute(reward, obs, done)
        rewards_log.append(graded_reward)
        steps_taken = step

        print(
            f"[STEP] step={step} action={throttle:.2f} reward={graded_reward:.2f} "
            f"done={str(done).lower()} error=null",
            flush=True
        )

        if done:
            break

    score = float(sum(rewards_log))
    score = max(0.0, min(1.0, score))  # clamp

    print(
        f"[END] success={str(score >= 0.1).lower()} steps={steps_taken} "
        f"score={score:.3f} rewards={','.join(f'{r:.2f}' for r in rewards_log)}",
        flush=True
    )


if __name__ == "__main__":
    # Define environments
    envs = {
        "easy": EasyEVEnv(),
        "medium": MediumEVEnv(),
        "hard": HardEVEnv(),
    }

    # Define graders
    graders = {
        "progress": ProgressRewardGrader(),
        "safety": SafetyPenaltyGrader(),
        "balanced": BalancedGrader(),
    }

    # Run all combos
    for env_name, env in envs.items():
        for grader_name, grader in graders.items():
            task_name = f"{env_name}-{grader_name}"
            run_episode(env, grader, task_name, env_name)