import fitz  
import os
import json
def extract_captions(pdf_path):
    doc = fitz.open(pdf_path)
    captions = {}
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")  #like this:(x0, y0, x1, y1, text, block_no)
        for block in blocks:
            text = block[4].strip()
            if text.lower().startswith(("figure", "fig.", "table")):
                key = f"page_{page_num}_caption_{len(captions)+1}"
                captions[key] = {
                    "text": text,
                    "page": page_num,
                    "bbox": block[:4]
                }
    return captions
def save_captions(captions, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(captions, f, indent=2)
    print(f"✅ Saved captions to {output_path}")
if __name__ == "__main__":
    pdf_path = "../pdfs/sample.pdf"
    output_path = "../data/captions.json"
    captions = extract_captions(pdf_path)
    save_captions(captions, output_path)
