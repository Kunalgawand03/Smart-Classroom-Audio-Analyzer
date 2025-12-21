def engagement_score(questions, interactions):
    score = min(100, questions * 5 + interactions * 3)
    return score
