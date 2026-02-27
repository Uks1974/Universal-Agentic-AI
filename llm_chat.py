# llm_chat.py
from utils_llm import llm_call

from openai import OpenAI

def chat_with_data(context, question, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content



def chat_with_data(data_context, user_question):
    prompt = f"""
Answer the user's question using ONLY the information below.
If the answer is not present, say so clearly.

DATA CONTEXT:
{data_context}

QUESTION:
{user_question}
"""

    return llm_call(
        system_prompt="You answer strictly from provided data.",
        user_prompt=prompt
    )