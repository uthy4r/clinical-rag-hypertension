import os
from dotenv import load_dotenv
from openai import OpenAI
from src.vectorstore import index
from src.embeddings import embed_texts

load_dotenv()  # 👈 REQUIRED HERE TOO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_question(question, top_k=5):
    query_embedding = embed_texts([question])[0]

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    context = "\n\n".join(
        match["metadata"]["text"] for match in results["matches"]
    )

    prompt = f"""
You are a clinical decision support system.

You must follow these rules:
- Use ONLY the evidence provided below
- Do NOT hallucinate
- If recommendations depend on ASCVD risk, explain both cases clearly
- If evidence is insufficient, explicitly say so

Evidence:
{context}

Question:
{question}

Answer format:
- Start with a direct answer
- Clearly distinguish:
  • Stage 1 hypertension with ASCVD risk <10%
  • Stage 1 hypertension with ASCVD risk ≥10%
- Cite sources in square brackets, e.g. [ACC/AHA 2017], [WHO 2021]
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content
