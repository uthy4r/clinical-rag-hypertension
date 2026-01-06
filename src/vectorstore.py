import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from src.embeddings import embed_texts

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

INDEX_NAME = "clinical-hypertension"

# Create index if it doesn't exist
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(INDEX_NAME)

def store_chunks(chunks, batch_size=50):
    embeddings = embed_texts(chunks)

    vectors = [
        (str(i), embeddings[i], {"text": chunks[i]})
        for i in range(len(chunks))
    ]

    # Upsert in batches to avoid request size limits
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(batch)
