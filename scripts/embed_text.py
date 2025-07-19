import os
import json
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm

# === Configuration ===
JSON_DIR = "../data/json"
EMBEDDING_DIR = "../data/embeddings/text"
MODEL_NAME = "allenai/scibert_scivocab_uncased"  # swap with bge or sentence-transformers model
USE_CUDA = torch.cuda.is_available()

# === Setup ===
os.makedirs(EMBEDDING_DIR, exist_ok=True)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()
if USE_CUDA:
    model = model.cuda()

def extract_text_from_json(json_data):
    title = json_data.get("title", "")
    abstract = json_data.get("abstract", "")
    
    # Optionally include full text
    body_sections = json_data.get("sections", [])
    body = " ".join(section.get("text", "") for section in body_sections)
    
    # Combine all text for embedding
    full_text = title + " " + abstract + " " + body
    return full_text.strip()

def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    if USE_CUDA:
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        last_hidden_state = outputs.last_hidden_state  # [batch, seq_len, hidden_dim]
        embedding = last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
        return embedding

def main():
    files = [f for f in os.listdir(JSON_DIR) if f.endswith(".json")]
    print(f"📄 Found {len(files)} JSON files to embed.")

    for fname in tqdm(files, desc="Embedding papers"):
        paper_id = fname.replace(".json", "")
        json_path = os.path.join(JSON_DIR, fname)
        output_path = os.path.join(EMBEDDING_DIR, paper_id + ".npy")

        if os.path.exists(output_path):
            continue  # already processed

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
            text = extract_text_from_json(json_data)
            if not text.strip():
                print(f"⚠️ Skipping {paper_id}, no valid text")
                continue
            embedding = embed_text(text)
            np.save(output_path, embedding)
        except Exception as e:
            print(f"❌ Failed to process {paper_id}: {e}")

if __name__ == "__main__":
    main()
