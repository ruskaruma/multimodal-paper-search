#Code for scripts/extract_text_figures.py
import fitz  
import os
import json
from pathlib import Path
from PIL import Image
import uuid
def extract_text_and_images(pdf_path, output_json_dir, output_image_dir):
    doc=fitz.open(pdf_path)
    paper_id=Path(pdf_path).stem
    title=""
    abstract=""
    body_text=""

    #Trying to find the title of the paper and the abstract heuristically
    full_text=""
    for page in doc:
        full_text+=page.get_text()
    lines=full_text.split('\n')
    title=lines[0].strip()
    abstract_start=next((i for i, l in enumerate(lines) if "abstract" in l.lower()), None)
    if abstract_start is not None:
        abstract="\n".join(lines[abstract_start + 1 : abstract_start+5]).strip()

    body_text="\n".join(lines)

    # Save text metadata
    json_data={
        "paper_id": paper_id,
        "title": title,
        "abstract": abstract,
        "body_text": body_text
    }
    os.makedirs(output_json_dir, exist_ok=True)
    with open(os.path.join(output_json_dir, f"{paper_id}.json"), "w") as f:
        json.dump(json_data, f, indent=2)

    #Snippet fot extracting images
    os.makedirs(output_image_dir, exist_ok=True)
    img_count=0
    for page_num in range(len(doc)):
        page=doc[page_num]
        images=page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref=img[0]
            base_image=doc.extract_image(xref)
            image_bytes=base_image["image"]
            image_ext =base_image["ext"]
            image_filename = f"{paper_id}_fig{img_count}.{image_ext}"
            image_path = os.path.join(output_image_dir, image_filename)
            with open(image_path, "wb") as img_out:
                img_out.write(image_bytes)
            img_count += 1

    print(f"[{paper_id}] Extracted {img_count} images and metadata.")

