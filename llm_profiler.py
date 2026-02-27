# llm_profiler.py
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

from openai import OpenAI

def llm_profile(data, profile, api_key):
    client = OpenAI(api_key=api_key)

    prompt = f"""
    Analyze the following data and profile.
    Data: {data}
    Profile: {profile}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content