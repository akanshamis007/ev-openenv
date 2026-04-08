def grade_hard(rewards):
    survival = 1 if rewards[-1] > 0 else 0
    progress_score = min(1, max(0, sum(rewards) / 15))
    return 0.4 * survival + 0.6 * progress_score