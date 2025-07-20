import os
import re
import json

def extract_captions_from_text(text):
    #Regex to find Figure, Fig., Table with their number and caption text
    pattern=r"(Figure|Fig\.?|Table)\s+(\d+)[\.:]?\s+(.*?)(?=\n[A-Z]|\Z)"
    matches=re.findall(pattern, text, re.IGNORECASE | re.DOTALL)

    captions=[]
    for label, number, caption_text in matches:
        clean=caption_text.strip().replace("\n", " ")
        full_caption=f"{label} {number}: {clean}"
        captions.append(full_caption)

    return captions

def extract_all_possible_captions(paper_json):
    return extract_captions_from_text(
        "\n".join([
            paper_json.get("title", ""),
            paper_json.get("abstract", ""),
            paper_json.get("body_text", "")
        ])
    )

def map_captions_to_images(json_dir, image_dir, output_file):
    result = {}

    #Step 1:Listing all the image files like 2507.13353v1_fig2.png
    image_files = [
        f for f in os.listdir(image_dir)
        if f.endswith((".png", ".jpg", ".jpeg")) and "_fig" in f
    ]

    #Step 2: Grouping images by paper ID
    paper_to_images = {}
    for image_file in sorted(image_files):  # Sort = stable order
        paper_id = image_file.split("_fig")[0]
        paper_to_images.setdefault(paper_id, []).append(image_file)

    #Step 3:For each paper, matchinh N captions to N images
    for paper_id, images in paper_to_images.items():
        json_path = os.path.join(json_dir, f"{paper_id}.json")
        if not os.path.exists(json_path):
            print(f"[!] Skipping {paper_id} — JSON not found")
            continue

        try:
            with open(json_path, "r") as f:
                paper_json = json.load(f)

            captions = extract_all_possible_captions(paper_json)
            num_matches = min(len(images), len(captions))

            for i in range(num_matches):
                result[images[i]] = captions[i]

            #Remove unmatched image files
            for i in range(num_matches, len(images)):
                image_file = images[i]
                img_path = os.path.join(image_dir, image_file)
                if os.path.exists(img_path):
                    os.remove(img_path)

        except Exception as e:
            print(f"[!] Error processing {paper_id}: {e}")
            continue

    #Step 4: Saving thefinal caption mapping
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[DONE] Mapped {len(result)} images to captions → {output_file}")
