# scripts/download_arxiv_pdfs.py
import os
import time
import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm

#Parameters
SAVE_DIR = "pdfs"
QUERY = "deep learning OR transformers OR resnet OR attention OR bert OR llm"
MAX_RESULTS = 500
RESULTS_PER_CALL = 100
BASE_URL = "http://export.arxiv.org/api/query?"

#Ensure that the save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)
def fetch_arxiv_entries(start_index, max_results):
    query_url = (
        f"{BASE_URL}"
        f"search_query=all:{QUERY.replace(' ', '+')}"
        f"&start={start_index}"
        f"&max_results={max_results}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )
    response = requests.get(query_url, timeout=10)
    if response.status_code != 200:
        raise Exception(f"arXiv API error: {response.status_code}")
    return ET.fromstring(response.content)

def extract_pdf_url(entry):
    for link in entry.findall("{http://www.w3.org/2005/Atom}link"):
        if link.attrib.get("title") == "pdf":
            return link.attrib["href"] + ".pdf"
    return None

def download_pdf(url, save_path):
    try:
        response = requests.get(url, stream=True, timeout=15)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
        else:
            return False
    except Exception as e:
        print(f"Download failed: {e}")
        return False

def main():
    downloaded = 0
    start = 0

    with tqdm(total=MAX_RESULTS, desc="Downloading PDFs") as pbar:
        while downloaded < MAX_RESULTS:
            root = fetch_arxiv_entries(start_index=start, max_results=RESULTS_PER_CALL)
            entries = root.findall("{http://www.w3.org/2005/Atom}entry")
            if not entries:
                break

            for entry in entries:
                paper_id = entry.find("{http://www.w3.org/2005/Atom}id").text.split("/")[-1]
                pdf_url = extract_pdf_url(entry)
                if not pdf_url:
                    continue

                filename = os.path.join(SAVE_DIR, f"{paper_id}.pdf")
                if not os.path.exists(filename):
                    success = download_pdf(pdf_url, filename)
                    if success:
                        downloaded += 1
                        pbar.update(1)
                        time.sleep(0.5)  # polite delay
                if downloaded >= MAX_RESULTS:
                    break

            start += RESULTS_PER_CALL
            time.sleep(3)  # to avoid hitting API limits

    print(f"Downloaded {downloaded} PDFs into /{SAVE_DIR}")

if __name__ == "__main__":
    main()