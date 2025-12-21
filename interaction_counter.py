import re
from typing import Dict

def count_interactions(text: str) -> Dict[str, int]:
    """Counts questions, doubts, hand raises, and assignments using keywords."""

    text_lower = text.lower()

    # --- 1. Questions ---
    question_patterns = [
        r"\?", 
        r"why", r"how", r"what", r"when", r"where", r"can you", r"could you", r"is it"
    ]

    question_count = sum(len(re.findall(p, text_lower)) for p in question_patterns)

    # --- 2. Doubts ---
    doubt_patterns = [
        r"doubt", r"i didn't understand", r"explain", r"repeat", r"once again"
    ]

    doubt_count = sum(len(re.findall(p, text_lower)) for p in doubt_patterns)

    # --- 3. Hand Raises ---
    raise_patterns = [
        r"raise your hand", r"hands up", r"who knows", r"answer please"
    ]

    raise_count = sum(len(re.findall(p, text_lower)) for p in raise_patterns)

    # --- 4. Assignments ---
    assignment_patterns = [
        r"assignment", r"homework", r"submit", r"project", r"worksheet"
    ]

    assignment_count = sum(len(re.findall(p, text_lower)) for p in assignment_patterns)

    # total events = sum of all interactions
    total = question_count + doubt_count + raise_count + assignment_count

    return {
        "questions": question_count,
        "doubts": doubt_count,
        "hand_raises": raise_count,
        "assignments": assignment_count,
        "total_active_events": total
    }
