# llm_questions.py
from utils_llm import llm_call

def generate_llm_questions(profile_text):
    prompt = f"""
Based on the following data understanding, suggest 5 intelligent
questions a senior officer or manager may ask.

Data understanding:
{profile_text}
"""

    response = llm_call(
        system_prompt="You generate insightful analytical questions.",
        user_prompt=prompt
    )

    return [q.strip("- ") for q in response.split("\n") if q.strip()]