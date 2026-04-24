import requests

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


def judge_agent(text):
    prompt = f"""
Evaluate this output:

{text}

Give:
- Relevance /5
- Clarity /5
- Usefulness /5
- Overall Score /5
- Summary
"""
    return safe_generate(prompt)
