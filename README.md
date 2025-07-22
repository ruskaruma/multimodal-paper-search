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

## Project Structure, what it should look like after you have run all the scripts correctly.


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

### The dataset that I used here is too long to upload on the repository. Run the script below to download the dataset.
Download the dataset:

        python3 scripts/download_arxiv_pdfs.py  

Install dependencies:

      
      pip install -r requirements.txt

      
Build the FAISS index:
        
             python3 scripts/build_faiss_index.py
        

Run a search query: 
  
          python3 scripts/query_faiss.py --query "A diagram showing CNN architecture with ReLU and pooling layers"

## Status:
The end-to-end pipeline has been implemented and tested on a collection of research papers. The current version supports text-to-figure search using combined embeddings. Index contains over 2,600 multimodal vectors.


         
                                                                                                             
Run this command to download the dataset that was used in the project. Rest should be good to go. 
Give a star if it was helpful to you  :-)



## Future Work and Scalability Plan

This project presents a functional prototype of a multimodal scientific figure search engine that integrates textual and visual embeddings using SciBERT and CLIP, with FAISS as the similarity backend. The following roadmap outlines directions for future improvements, extensions, and scalability.

### Current Capabilities

- Extraction of text, figures, and captions from research paper PDFs.
- Generation of embeddings for both text and image modalities.
- Caption-to-figure alignment and indexing via FAISS.
- Retrieval using similarity search with basic evaluation metrics (e.g., Precision@k).

---

### Planned Extensions

#### 1. System Robustness and Scalability
- Migrate from local indexing to scalable vector databases (e.g., Pinecone, Weaviate, Qdrant).
- Implement batch processing, logging, and failure recovery mechanisms.
- Add multiprocessing for faster embedding and indexing pipelines.

#### 2. Enhanced Search Experience
- Implement cross-modal search (image-to-text and text-to-image).
- Introduce semantic filtering using metadata (title, authors, publication year).
- Support question-answering over visual scientific data.

#### 3. Frontend and API Development
- Build a FastAPI or Flask backend for RESTful multimodal queries.
- Design an intuitive frontend interface to browse retrieved figures.
- Integrate authentication, rate limiting, and analytics for real-world usage.

#### 4. Model Improvements
- Fine-tune domain-specific CLIP or vision transformers on annotated figure-caption pairs.
- Explore joint embedding spaces with contrastive learning across modalities.
- Experiment with lightweight models for deployment on constrained hardware.

#### 5. Evaluation and Benchmarking
- Establish a gold-standard benchmark dataset for multimodal figure search.
- Include recall, NDCG, and MAP in evaluation metrics.
- Conduct human evaluations to assess result quality.

#### 6. Dataset and Crawler Extension
- Extend corpus to include multiple open-access repositories beyond arXiv (e.g., PubMed Central, bioRxiv).
- Automate scheduled crawling and embedding of new papers.
- Maintain versioning and timestamping of index snapshots.

#### 7. Application Extensions
- Build integrations for research tools such as Zotero, Notion, or Overleaf plugins.
- Offer browser extensions for in-page figure search.
- Develop dataset search features (e.g., locating papers that release datasets or benchmarks).


## Now, you can either fork this repository or send a PR in any of the above-given planned extensions.

---
