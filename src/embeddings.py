import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 👈 THIS LINE IS CRITICAL

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_texts(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [d.embedding for d in response.data]
