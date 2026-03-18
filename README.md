# Mini RAG Assistant (Construction Domain)

## Overview
This project implements a Retrieval-Augmented Generation (RAG) system for answering construction-related queries using internal documents (policies, FAQs, specifications).

The system retrieves relevant document chunks and generates answers strictly grounded in retrieved context, avoiding hallucinations.

---

## System Architecture

User Query → Embedding → FAISS Retrieval → Context → LLM → Answer

---

## Models Used

### Embedding Model
- all-MiniLM-L6-v2 (Sentence Transformers)
- Reason: Lightweight, fast, and provides strong semantic similarity for retrieval tasks

### LLM
- OpenRouter API (openai/gpt-3.5-turbo)
- Reason: Free, reliable, and suitable for grounded answer generation

---

## Implementation Details

### 1. Document Processing
- Documents are loaded from `.md` files
- Chunking is performed using Markdown-aware splitting
- Chunk size: 300 with overlap of 50
- This ensures meaningful semantic segmentation

---

### 2. Vector Search (FAISS)
- All chunks are converted into embeddings
- FAISS index is built for efficient similarity search
- Top-k (k=3) relevant chunks are retrieved for each query

---

### 3. Grounded Answer Generation
The LLM is strictly instructed to:
- Use ONLY retrieved context
- Avoid external knowledge
- Return "Not found in documents" if answer is missing

This ensures:
- No hallucination
- High reliability

---

### 4. Transparency & Explainability
The system explicitly displays:
- Retrieved document chunks (context)
- Final generated answer

---

## Evaluation

Test queries were used to evaluate:

- Retrieval relevance → High
- Hallucination → None observed
- Answer completeness → Good with structured prompts

### Example:
**Query:** What factors affect construction project delays?

**Observation:**
- Correct chunks retrieved
- Answer generated only from context
- No external assumptions

---

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py