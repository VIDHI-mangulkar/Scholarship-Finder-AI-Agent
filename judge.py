import requests

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
        return res.json().get("response", "")
    except Exception as e:
        return f"❌ ERROR: {str(e)}"


def judge_agent(output):
    prompt = f"""
Evaluate this scholarship assistant output:

{output}

Strictly evaluate based on:
- Personalization
- Practical usefulness
- Clarity
- Actionable insights

Return:

Relevance: X/5
Clarity: X/5
Usefulness: X/5
Overall: X/5

Summary: short explanation
"""

    return safe_generate(prompt)
