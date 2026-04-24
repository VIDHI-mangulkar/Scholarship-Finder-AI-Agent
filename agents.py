import os
import datetime
import requests
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# =========================
# LLM (OLLAMA)
# =========================
def safe_generate(prompt):
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            }
        )
        return res.json().get("response", "No response")
    except Exception as e:
        return f"❌ ERROR: {str(e)}"


# =========================
# STEP 1 — SEARCH
# =========================
def search_agent(profile):
    year = datetime.datetime.now().year

    query = f"""
    latest scholarships {year} {year+1}
    for {profile}
    eligibility deadline apply funding
    """

    return tavily.search(query=query, max_results=5)


# =========================
# STEP 2 — PER SCHOLARSHIP ANALYSIS
# =========================
def eligibility_agent(profile, data):
    try:
        results = data.get("results", [])

        if not results:
            return "No scholarships found."

        final_output = ""

        for r in results:
            title = r.get("title")
            content = r.get("content")
            url = r.get("url")

            # filter irrelevant results
            if "scholarship" not in title.lower():
                continue

            prompt = f"""
Student Profile:
{profile}

Scholarship:
Title: {title}
Description: {content}

Give structured output:

1. Eligibility Criteria (bullet points)
2. Deadline (exact or estimated year)
3. Benefits (amount, coverage)
4. Why it matches this student specifically
5. Application Tips (practical and actionable)

Be specific, avoid generic answers.
"""

            response = safe_generate(prompt)

            final_output += f"""
-----------------------------
🎓 {title}

{response}

🔗 Apply: {url}
-----------------------------
"""

        return final_output

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


# =========================
# STEP 3 — RECOMMENDATION (RANKING)
# =========================
def recommendation_agent(text):
    return safe_generate(f"""
From the scholarships below:

{text}

Do:
1. Rank TOP 3 scholarships (best → least)
2. Explain WHY ranking
3. Give application strategy
4. Highlight deadlines urgency

Make it decision-focused and clear.
""")
