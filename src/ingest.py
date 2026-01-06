import os

DATA_DIR = "data/raw"

def load_and_chunk(chunk_size=500):
    chunks = []

    for filename in os.listdir(DATA_DIR):
        with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
            text = f.read()

        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i+chunk_size])

    return chunks
print("ingest.py loaded successfully")
