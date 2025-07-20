import os
import faiss
import json
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
from argparse import ArgumentParser

import warnings
warnings.filterwarnings("ignore", category=UserWarning)  #Suppressing TypedStorage warning because my CLI look messy
warnings.filterwarnings("ignore", category=FutureWarning)  #Suppress res

#Loading SciBERT (the text encoder)
print("🔠 Loading SciBERT...")
scibert_tokenizer=AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
scibert_model=AutoModel.from_pretrained("allenai/scibert_scivocab_uncased")

#parsing the input query
parser=ArgumentParser()
parser.add_argument("--query", type=str, required=True)
args=parser.parse_args()

#Tokenizing the query
tokens=scibert_tokenizer(args.query, return_tensors="pt", truncation=True, padding=True)
with torch.no_grad():
    text_emb=scibert_model(**tokens).last_hidden_state.mean(dim=1).squeeze().numpy()

print(f"Text embedding shape: {text_emb.shape}")

#Zero vector for image embedding
image_emb=np.zeros(512, dtype=np.float32)

#Combining
embedding=np.concatenate([image_emb, text_emb])
print(f"Combined query embedding shape: {embedding.shape}")

#Loading FAISS index
print("[LOADING] Loading FAISS index...")
index=faiss.read_index("data/faiss_index.bin")
with open("data/faiss_id_map.json") as f:
    id_map = json.load(f)

print(f"FAISS index dimension: {index.d}")

#Sanity check of the query before search
if embedding.shape[0] != index.d:
    raise ValueError(f"[❌] Dimension mismatch: query has {embedding.shape[0]}, index expects {index.d}")

#Search of the query
D, I = index.search(np.expand_dims(embedding, axis=0), 5)

#Show top 5 results, if not just top
print("\n🔍 Top 5 results:")
for i, idx in enumerate(I[0]):
    if idx == -1:
        continue
    print(f"{i + 1}. {id_map[str(idx)]} (distance: {D[0][i]:.4f})")
