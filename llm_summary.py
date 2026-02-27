# llm_summary.py

from utils_llm import llm_call
from openai import OpenAI

def generate_executive_summary(chat_history, context, api_key):
    """
    Generates a one-page executive summary based on:
    - AI understanding
    - User chat history
    """

    client = OpenAI(api_key=api_key)

    chat_text = ""
    for item in chat_history:
        chat_text += f"Q: {item['Q']}\nA: {item['A']}\n\n"

    prompt = f"""
    You are a senior consultant preparing a one-page executive summary.

    Context (AI Understanding):
    {context}

    User Interactions:
    {chat_text}

    Prepare an executive summary with:
    - Background
    - Key insights
    - Risks / issues
    - Recommendations
    - Future actions
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert consultant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content