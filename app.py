import streamlit as st
from agents import *
from judge import judge_agent

st.set_page_config(page_title="Scholarship AI Agent", layout="wide")

st.title("🎓 Scholarship AI Agent (Ollama + Llama3)")

course = st.selectbox("Course", ["10th","12th","B.Tech","MBA","M.Tech","Law","Architecture"])
country = st.selectbox("Country", ["India","USA","UK","Canada"])
cgpa = st.text_input("CGPA (optional)")

profile = f"{course}, {country}, CGPA {cgpa}"

if st.button("🚀 Run Agent"):

    st.subheader("Step 1: Search")
    data = search_agent(profile)

    for r in data["results"]:
        st.write("###", r["title"])
        st.write(r["content"])
        st.write("🔗", r["url"])
        st.write("---")

    st.subheader("Step 2: Eligibility")
    eligible = eligibility_agent(profile, data)
    st.write(eligible)

    st.subheader("Step 3: Recommendation")
    rec = recommendation_agent(eligible)
    st.write(rec)

    st.subheader("Step 4: Evaluation")
    judge = judge_agent(rec)
    st.write(judge)
