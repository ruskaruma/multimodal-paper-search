

import fitz 
import os
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num, page in enumerate(doc, start=1):
        text += f"\n--- Page {page_num} ---\n"
        text += page.get_text()
    return text
def save_text(text, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Saved extracted text to: {output_path}")
if __name__ == "__main__":
    pdf_file = "../pdfs/sample.pdf"
    output_path = "../data/sample_text.txt"
    if not os.path.isfile(pdf_file):
        print(f"❌ File not found: {pdf_file}")
    else:
        text = extract_text(pdf_file)
        save_text(text, output_path)
