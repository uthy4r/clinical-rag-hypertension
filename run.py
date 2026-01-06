from src.ingest import load_and_chunk
from src.vectorstore import store_chunks
from src.retriever import ask_question

print("Indexing clinical guidelines...")
chunks = load_and_chunk()
store_chunks(chunks)
print("Indexing complete.\n")

while True:
    q = input("Ask a hypertension question (or exit): ")
    if q.lower() == "exit":
        break

    answer = ask_question(q)
    print("\nAnswer:\n", answer)
    print("-" * 50)
