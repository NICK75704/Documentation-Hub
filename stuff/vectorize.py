import ollama
import chromadb
import os

data_dir = 'stuff/data/'

def vectorize(data_dir, chunk_size=300):
    client = chromadb.Client()
    collection = client.create_collection(name = "docs")
    all_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    for i in range(len(all_files)):
        with open(f"{all_files[i]}.json", 'r') as f:
            