import requests
import datetime
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

MODEL = "llama3"


def safe_generate(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]
    except Exception as e:
        return f"❌ ERROR: {str(e)}"


def search_agent(profile):
    year = datetime.datetime.now().year
    query = f"latest scholarships {year} for {profile}"
    return tavily.search(query=query, max_results=5)


def eligibility_agent(profile, data):
    results = data.get("results", [])
    output = ""

    for r in results:
        prompt = f"""
Student Profile: {profile}

Scholarship:
{r['title']}
{r['content']}

Give:
- Eligibility
- Deadline
- Benefits
- Tips
"""

        res = safe_generate(prompt)

        output += f"""
--------------------
🎓 {r['title']}
{res}
🔗 {r['url']}
--------------------
"""

    return output


def recommendation_agent(text):
    prompt = f"""
Rank top 3 scholarships:

{text}

Explain why + strategy
"""
    return safe_generate(prompt)
