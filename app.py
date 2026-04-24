import streamlit as st
from agents import *
from judge import judge_agent

st.set_page_config(page_title="Scholarship AI Agent", layout="wide")

# =========================
# UI STYLE
# =========================
st.markdown("""
<style>
.stApp { background: linear-gradient(to right, #eef2ff, #f8fafc); }
.card {
    background:white; padding:15px;
    border-radius:12px; border:1px solid #ddd;
    margin-bottom:10px;
}
.step {
    background:#e0f2fe;
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 Scholarship Finder AI Agent")

# =========================
# INPUTS
# =========================
course = st.selectbox("Course", [
    "10th","11th","12th","Diploma","B.Tech","B.Arch",
    "BA","BSc","BCom","LLB","MBA","M.Tech"
])

country = st.selectbox("Country", [
    "India","USA","UK","Canada","Germany","Australia"
])

cgpa = st.text_input("CGPA (Optional)")

profile = f"""
Course: {course}
Country: {country}
CGPA: {cgpa if cgpa else "Not Provided"}
"""

# =========================
# RUN
# =========================
if st.button("🚀 Run AI Agent"):

    eligible = ""
    rec = ""

    # STEP 1
    st.subheader("🔍 Step 1: Search Results")
    try:
        data = search_agent(profile)

        for item in data.get("results", []):
            st.markdown(f"""
            <div class="card">
            <b>{item['title']}</b><br>
            {item['content']}<br>
            <a href="{item['url']}" target="_blank">Apply</a>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(e)
        data = {}

    # STEP 2
    st.subheader("📝 Step 2: Eligibility + Summary")

    try:
        eligible = eligibility_agent(profile, data)
        st.markdown(f"<div class='step'>{eligible}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(e)
        eligible = ""

    # STEP 3
    st.subheader("🏆 Step 3: Recommendations")

    try:
        rec = recommendation_agent(eligible)
        st.markdown(f"<div class='step'>{rec}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(e)
        rec = ""

    # STEP 4
    st.subheader("⚖️ Step 4: AI Evaluation")

    try:
        judge = judge_agent(rec)
        st.markdown(f"<div class='step'>{judge}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(e)