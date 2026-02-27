# utils_llm.py

from openai import OpenAI

def llm_call(messages, api_key, model="gpt-4o-mini"):
    """
    Generic LLM call utility.
    Uses user-provided API key (BYOK).
    """

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content
