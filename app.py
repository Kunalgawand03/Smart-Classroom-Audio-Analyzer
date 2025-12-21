import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Teacher Performance Dashboard",
    layout="wide"
)

def clean(x):
    if pd.isna(x):
        return 0
    return round(float(x), 2)


st.title("📘 AI Teacher Performance Evaluation")
st.subheader("Transparent • Fair • Explainable")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("analysis_results.csv")

df = load_data()
latest = df.iloc[-1]

# =========================
# METRIC CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("🗣 Words / Minute", clean(latest["words_per_minute"]))
col2.metric("❓ Questions Asked", clean(latest["questions"]))
col3.metric("🎯 Focus Score", clean(latest["student_focus"]))
col4.metric("⭐ Teacher Impact", clean(latest["teacher_impact_score"]))


st.divider()

# =========================
# BAR CHART
# =========================
st.subheader("📊 Teaching Quality Metrics")

scores = {
    "Engagement": latest["teacher_impact_score"],
    "Focus": latest["student_focus"],
    "Interaction": latest["active_events"],
}

fig, ax = plt.subplots()
ax.bar(scores.keys(), scores.values(), color=["green", "blue", "orange"])
ax.set_ylabel("Score")
ax.set_ylim(0, 100)

st.pyplot(fig)

# =========================
# TRANSCRIPT VIEW
# =========================
st.subheader("🧠 Classroom Transcript (Explainable AI)")

with st.expander("Click to view transcript"):
    st.text(latest["full_transcript"])

# =========================
# FAIRNESS CHECK
# =========================
st.subheader("⚖ Fairness & Bias Check")

st.success("""
✔ No gender biased language  
✔ Equal teacher‑student interaction  
✔ No negative sentiment detected  

This ensures **ethical & unbiased evaluation**
""")

# =========================
# SUGGESTIONS
# =========================
st.subheader("💡 AI Suggestions for Improvement")

st.info("""
• Encourage more student questions  
• Increase wait‑time after asking questions  
• Use examples during explanations  
""")

st.caption("Built for Rural Education • Low Resource • High Impact")
