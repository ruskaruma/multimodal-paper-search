import fitz  
import os
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text  
if __name__ == "__main__":
    pdf_file = "../pdfs/sample.pdf"
    output_path = "../data/sample_text.txt"
    os.makedirs("../data", exist_ok=True)
    text = extract_text(pdf_file)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved extracted text to {output_path}")
