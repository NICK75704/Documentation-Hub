import ollama
import chromadb
import os
import json
import hashlib

DATA_DIR = 'stuff/data/'
EMBEDDING_MODEL = "nomic-embed-text"
CHROMA_PATH = 'stuff/db/'
REGISTRY_PATH = os.path.join(CHROMA_PATH, 'processed_registry.json')

def get_file_hash(text):
    """Generates a deterministic ID based on content."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def load_registry():
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_registry(registry):
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, 'w') as f:
        json.dump(registry, f)

def vectorize(data_dir=DATA_DIR, embedding_model=EMBEDDING_MODEL, chunk_size_limit=100):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name="docs")
    
    registry = load_registry()
    
    ids, embeddings, documents, metadatas = [], [], [], []
    
    all_files = []
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".json"):
                all_files.append(os.path.join(root, file))

    for file_path in all_files:
        mtime = os.path.getmtime(file_path)
        if file_path in registry and registry[file_path] == mtime:
            print(f"Skipping {file_path} (No changes detected)")
            continue

        print(f"Processing {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                d = json.load(f)
                file_metadata = d.get("metadata", {})
                
                chunks = []
                if "content" in d:
                    content_data = d["content"]
                    chunks = content_data if isinstance(chunks, list) else content_data.get("chunks", [])
                
                if not chunks:
                    continue

                for chunk_text in chunks:
                    chunk_id = get_file_hash(chunk_text)
                    
                    if chunk_id in ids:
                        continue

                    response = ollama.embeddings(model=embedding_model, prompt=chunk_text)
                    embedding = response["embedding"]

                    ids.append(chunk_id)
                    embeddings.append(embedding)
                    documents.append(chunk_text)
                    metadatas.append({
                        "source": file_metadata.get("file_name", "unknown"),
                        "path": file_metadata.get("file_path", "unknown"),
                        "preview": chunk_text[:50]
                    })

                    if len(ids) >= chunk_size_limit:
                        collection.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
                        ids, embeddings, documents, metadatas = [], [], [], []

            registry[file_path] = mtime
            save_registry(registry)
            
            if ids:
                collection.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
                ids, embeddings, documents, metadatas = [], [], [], []

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print("Vectorization complete.")

if __name__ == "__main__":
    vectorize()