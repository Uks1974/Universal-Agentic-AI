# llm_analysis_agent.py
from openai import OpenAI
from utils_llm import llm_call

def generate_brief_analysis(context, api_key):
    """
    Generates brief analysis, risks, and recommended actions
    based on AI understanding.
    """

    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are a senior data analyst.

    Based on the following AI understanding of the data,
    provide:
    1. Brief analysis
    2. Key issues or risks
    3. Recommended actions
    4. Future steps

    Data Understanding:
    {context}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content