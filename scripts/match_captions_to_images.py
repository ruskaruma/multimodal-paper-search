import fitz
import os
import json
def extract_images_with_position(pdf_path):
    doc = fitz.open(pdf_path)
    image_map = {}
    for page_num, page in enumerate(doc, start=1):
        imglist = page.get_images(full=True)
        for img_index, img in enumerate(imglist):
            xref = img[0]
            bbox = page.get_image_bbox(xref)
            key = f"fig_{page_num}_{img_index+1}.png"
            image_map[key] = {
                "page": page_num,
                "bbox": [bbox.x0, bbox.y0, bbox.x1, bbox.y1]
            }
    return image_map
    
def load_captions(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
def match_captions_to_images(image_map, captions):
    matched = {}
    for img_name, img_info in image_map.items():
        page = img_info["page"]
        img_y = img_info["bbox"][1]  # y0

        #Finding all captions on same page
        page_captions = [
            (key, cap) for key, cap in captions.items()
            if cap["page"] == page
        ]
        #Finding caption with closest vertical distance (simple heuristic)
        best_caption = None
        min_distance = float("inf")
        for key, cap in page_captions:
            cap_y = cap["bbox"][1]
            distance = abs(cap_y - img_y)
            if distance < min_distance:
                min_distance = distance
                best_caption = cap["text"]
        if best_caption:
            matched[img_name] = best_caption
    return matched
def save_matched(matched, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(matched, f, indent=2)
    print(f"✅ Saved matched captions to {output_path}")
if __name__ == "__main__":
    pdf_path = "../pdfs/sample.pdf"
    caption_path = "../data/captions.json"
    output_path = "../data/captions_matched.json"
    image_map = extract_images_with_position(pdf_path)
    captions = load_captions(caption_path)
    matched = match_captions_to_images(image_map, captions)
    save_matched(matched, output_path)
