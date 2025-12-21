def fairness_check(text):
    bias_words = ["boys", "girls", "weak", "stupid"]
    found = [w for w in bias_words if w in text.lower()]

    if not found:
        return "No bias detected"
    else:
        return f"Potential bias words found: {found}"
