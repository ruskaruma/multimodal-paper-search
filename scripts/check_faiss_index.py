import faiss

index = faiss.read_index("data/faiss_index.bin")
print("[DONE]FAISS index loaded successfully.")
print("Number of vectors:", index.ntotal)
print("Embedding dimension:", index.d)
