# scripts/embed_images.py

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import os
import numpy as np
import torch
from PIL import Image
from tqdm import tqdm
from transformers import CLIPProcessor, CLIPModel

#Laoding CLIP model and processor
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

#Set paths
image_dir = "data/images"
output_dir = "data/embeddings"
os.makedirs(output_dir, exist_ok=True)

#Iterating over all the images that are in the directory
for filename in tqdm(os.listdir(image_dir)):
    if not filename.lower().endswith(".png"):
        continue

    image_path=os.path.join(image_dir, filename)
    try:
        image=Image.open(image_path).convert("RGB")
        inputs=clip_processor(images=image, return_tensors="pt")

        with torch.no_grad():
            features=clip_model.get_image_features(**inputs)

        #Ensuring the output is of the expected shape
        if features.ndim != 2 or features.shape[0] != 1:
            raise ValueError(f"Unexpected feature shape: {features.shape}")

        embedding=features.squeeze(0).numpy()  #Shape: (512,)
        np.save(os.path.join(output_dir, f"{filename}_image.npy"), embedding)

    except Exception as e:
        print(f"[FAIL!!]Failed on {filename}: {e}")
