def grade_medium(rewards):
    score = (sum(rewards) - 1) / 10
    return max(0, min(score, 1))