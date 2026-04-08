def grade_easy(rewards):
    score = sum(rewards) / 8
    return max(0, min(score, 1))