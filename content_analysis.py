def explanation_clarity(text):
    sentences = text.split(".")
    avg_len = sum(len(s.split()) for s in sentences if s.strip()) / max(1, len(sentences))

    if avg_len < 12:
        return "HIGH"
    elif avg_len < 20:
        return "MEDIUM"
    else:
        return "LOW"


def vocabulary_level(text):
    words = text.split()
    long_words = [w for w in words if len(w) > 7]
    ratio = len(long_words) / max(1, len(words))

    if ratio < 0.1:
        return "Appropriate for Grade 5"
    elif ratio < 0.2:
        return "Moderate"
    else:
        return "Complex"


def concept_coverage(text):
    keywords = ["chapter", "definition", "example", "question", "explain"]
    hits = sum(1 for k in keywords if k in text.lower())
    return min(100, hits * 20)
