# Multimodal Research Paper Search Engine

This project implements a semantic search engine over scientific papers by combining textual and visual features extracted from figures in research PDFs. It allows users to query using natural language and retrieves the most relevant figure images based on multimodal similarity.

## Features

- PDF parsing and extraction of figure images and captions.
- Caption embedding using SciBERT.
- Image embedding using OpenAI CLIP.
- Fusion of text and image embeddings into a single multimodal vector.
- Indexing of multimodal vectors using FAISS for efficient similarity search.
- Query interface that embeds input text and retrieves nearest figure matches.
- Example queries tested for model validation.
- Full environment specified via `requirements.txt`.

## Project Structure


        multimodal-paper-search/
        │
        ├── data/                          #Processed and indexed data
        │   ├── embeddings/               #Numpy embeddings for text+image
        │   ├── images/                   #Extracted images from papers
        │   ├── captions.json             #Mappings of figure to caption
        │   ├── faiss_index.bin           #FAISS binary index
        │   ├── faiss_combined.index      #Optional/alternate FAISS index
        │   ├── faiss_id_map.json         #Mapping of FAISS index to filenames
        │   ├── faiss_mapping.json        #Possibly same or old mapping
        │
        ├── ipynb_notebooks/              #Jupyter notebooks for development
        │   ├── caption_mapping.ipynb     #Maps image captions to figures
        │   ├── embed_text_images.ipynb   #Embeds text and image content
        │   ├── extract_text_figures.ipynb #Parses text and extracts figures
        │
        ├── json/                         #Parsed structured text (JSONs)
        │
        ├── pdfs/                         #Raw downloaded arXiv papers
        │
        ├── scripts/                      #Main pipeline scripts
        │   ├── build_faiss_index.py      #Builds multimodal FAISS index
        │   ├── download_arxiv_papers.py  #Downloads PDFs from arXiv
        │   ├── embed_images.py           #Image embedding with CLIP
        │   ├── extract_text_figures.py   #Extracts text & figures from PDF
        │   ├── match_captions_text_figures.py #Matches text with images
        │   ├── query_faiss.py            #Search script using FAISS
        │
        ├── tools/                        #Debugging or utility notebooks
        │   ├── debug_caption_mapping.ipynb
        │
        ├── LICENSE                       #License file
        ├── README.md                     #Project overview and instructions
        ├── requirements.txt              #All required dependencies

## Getting Started

Install dependencies:

      
      pip install -r requirements.txt

      
Build the FAISS index:
        
             python3 scripts/build_faiss_index.py
        

Run a search query: 
  
          python3 scripts/query_faiss.py --query "A diagram showing CNN architecture with ReLU and pooling layers"

## Status:
The end-to-end pipeline has been implemented and tested on a collection of research papers. The current version supports text-to-figure search using combined embeddings. Index contains over 2,600 multimodal vectors.

## In porgress


Let me know if you want a lighter version for a personal portfolio or a public demo.

Give a star if it was helpful to you  :-)

    
