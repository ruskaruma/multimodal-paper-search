import os
import json
import numpy as np
import faiss

embedding_dir="data/embeddings"
index_path="data/faiss_index.bin"
id_map_path="data/faiss_id_map.json"

image_embeddings = []
id_map = {}

print("Loading embeddings...")
for filename in os.listdir(embedding_dir):
    if not filename.endswith("_image.npy"):
        continue
    base_name=filename.replace("_image.npy", "")
    text_file =os.path.join(embedding_dir, base_name + "_text.npy")
    image_file =os.path.join(embedding_dir, filename)

    if not os.path.exists(text_file):
        print(f"Missing text embedding for {base_name}")
        continue

    try:
        text_emb=np.load(text_file)
        image_emb=np.load(image_file)

        if text_emb.shape[0] != 768 or image_emb.shape[0] != 512:
            print(f"Skipped {base_name}: unexpected embedding dimensions")
            continue

        multimodal_emb =np.concatenate([text_emb, image_emb])
        image_embeddings.append(multimodal_emb)
        id_map[len(image_embeddings) - 1] = base_name  # No .png suffix
    except Exception as e:
        print(f"Failed on {base_name}: {e}")

if len(image_embeddings)==0:
    print(" No valid embeddings found. Exiting.")
    exit(1)

image_embeddings=np.stack(image_embeddings).astype("float32")
index=faiss.IndexFlatL2(image_embeddings.shape[1])
index.add(image_embeddings)

os.makedirs("data", exist_ok=True)
faiss.write_index(index, index_path)
with open(id_map_path, "w") as f:
    json.dump(id_map, f)

print(f"[DONE] FAISS index saved to {index_path}")
print(f"[DONE] ID map saved to {id_map_path}")
print(f"[ TABLE ] Index contains {index.ntotal} vectors of dimension {index.d}")
