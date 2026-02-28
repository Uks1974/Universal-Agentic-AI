# llm_chat.py
print("DEBUG: llm_chat.py loaded, chat_with_data has api_key")
from utils_llm import llm_call

def chat_with_data(context, question, api_key):
    """
    Answers user questions based on AI understanding of the data.
    """

    messages = [
        {"role": "system", "content": "You are a helpful data analyst."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
    ]

    return llm_call(messages, api_key)

