from fastapi import FastAPI
from pydantic import BaseModel
from src.retriever import ask_question

app = FastAPI(title="Clinical RAG – Hypertension")

class Query(BaseModel):
    question: str

@app.post("/query")
def query_rag(q: Query):
    answer = ask_question(q.question)
    return {"answer": answer}
