import math

def safe_number(x):
    if x is None:
        return 0
    if isinstance(x, float) and math.isnan(x):
        return 0
    return x

def retention_score(students_continuing, total_students):
    students_continuing = safe_number(students_continuing)
    total_students = safe_number(total_students)

    if total_students <= 0:
        return 0

    return round((students_continuing / total_students) * 100, 2)

def engagement_score(active_events, total_events):
    active_events = safe_number(active_events)
    total_events = safe_number(total_events)

    if total_events <= 0:
        return 0

    return round((active_events / total_events) * 100, 2)

def curiosity_index(extra_actions, total_students):
    extra_actions = safe_number(extra_actions)
    total_students = safe_number(total_students)

    if total_students <= 0:
        return 0

    return round((extra_actions / total_students) * 100, 2)

def teacher_impact_score(retention, engagement, curiosity, performance,
                         w1=0.4, w2=0.3, w3=0.2, w4=0.1):

    retention = safe_number(retention)
    engagement = safe_number(engagement)
    curiosity = safe_number(curiosity)
    performance = safe_number(performance)

    score = (
        (w1 * retention) +
        (w2 * engagement) +
        (w3 * curiosity) +
        (w4 * performance)
    )

    return round(score, 2)
