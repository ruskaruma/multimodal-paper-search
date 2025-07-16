import fitz  
import os
def extract_images_from_pdf(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    os.makedirs(output_dir, exist_ok=True)
    image_count = 0
    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"fig_{page_index+1}_{img_index+1}.{image_ext}"
            image_path = os.path.join(output_dir, image_filename)
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            print(f"✅ Saved image: {image_filename}")
            image_count += 1
    print(f"\n📦 Total images extracted: {image_count}")
if __name__ == "__main__":
    pdf_path = "../pdfs/sample.pdf"
    output_dir = "../data/images"
    extract_images_from_pdf(pdf_path, output_dir)
