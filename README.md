# 🏗️ Construction AI Assistant (Mini RAG)

## 📌 Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system for answering construction-related queries using internal documents such as policies, FAQs, and specifications.

The system retrieves relevant document chunks and generates answers **strictly grounded in the retrieved context**, ensuring accuracy and preventing hallucinations.

---

## 🧠 System Architecture

```
User Query → Embedding → FAISS Retrieval → Context → LLM → Answer
```

---

## ⚙️ Models Used

### 🔹 Embedding Model

* **all-MiniLM-L6-v2 (Sentence Transformers)**
* **Reason:** Lightweight, fast, and provides strong semantic similarity for retrieval tasks

---

### 🔹 LLM (Primary - API)

* **OpenRouter API → openai/gpt-3.5-turbo**
* **Reason:**

  * Reliable and accurate
  * Strong grounding capability
  * Suitable for real-time applications

---

### 🔹 LLM (Bonus - Local Model)

* **HuggingFace → google/flan-t5-base**
* **Reason:**

  * Runs locally (offline capability)
  * Enables comparison with API-based model
  * Demonstrates bonus requirement

---

## 📄 Implementation Details

### 1. Document Processing

* Documents are loaded from `.md` files
* Markdown-aware chunking is applied
* **Chunk size:** 300
* **Overlap:** 50

This ensures meaningful segmentation and better retrieval performance.

---

### 2. Vector Search (FAISS)

* Each chunk is converted into embeddings
* A FAISS index is built for efficient similarity search
* Top-k (**k = 3**) relevant chunks are retrieved for each query

---

### 3. Grounded Answer Generation

The LLM is strictly instructed to:

* Use **ONLY retrieved context**
* Avoid any external knowledge
* Return:

  ```
  Not found in documents
  ```

  if the answer is missing

This ensures:

* No hallucination
* High reliability

---

### 4. Transparency & Explainability

The system explicitly displays:

* 📄 Retrieved document chunks (context)
* 🤖 Final generated answer

This allows users to verify how answers are derived.

---

## ⭐ Bonus Features

### 1. Local LLM Integration

* Implemented using HuggingFace Transformers
* Model: **Flan-T5**
* Works as fallback and comparison model

---

### 2. Model Comparison

The system displays answers from:

* 🤖 OpenRouter (API model)
* 🧠 HuggingFace Local Model

---

### 3. Observations

| Feature      | OpenRouter (API) | Local Model (Flan-T5) |
| ------------ | ---------------- | --------------------- |
| Accuracy     | High             | Moderate              |
| Grounding    | Strong           | Weaker                |
| Completeness | Full             | Partial               |
| Latency      | Medium           | Fast                  |
| Cost         | API-based        | Free                  |

**Conclusion:**

* OpenRouter produces more complete and reliable answers
* Local model demonstrates offline capability but may miss details

---

## 🧪 Evaluation

Multiple test queries were used to evaluate performance:

### Example Query

**"What factors affect construction project delays?"**

### Results

* Relevant chunks retrieved correctly
* OpenRouter produced complete grounded answer
* Local model produced partially correct output
* No hallucination observed

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Add OpenRouter API Key

In `rag.py`, replace:

```python
"Authorization": "Bearer YOUR_API_KEY"
```

with your actual API key.

---

### 3. Run the Application

```bash
streamlit run app.py
```

---

### 4. Open in Browser

```
http://localhost:8501
```

---

## 📂 Project Structure

```
mini-rag/
│
├── app.py              # Streamlit UI (Premium interface)
├── rag.py              # Core RAG pipeline + model comparison
├── utils.py            # Document loading & chunking
├── data/               # Input documents (.md files)
├── requirements.txt
└── README.md
```

---

## 🔒 Notes

* Ensure a valid OpenRouter API key is used
* Place your documents inside the `data/` folder
* First run may take time due to model loading

---

## 🔮 Future Improvements

* Hybrid search (keyword + vector)
* Advanced re-ranking
* Confidence scoring
* Cloud deployment (Streamlit Cloud / HuggingFace Spaces)

---

## 🏁 Conclusion

This project successfully demonstrates:

* Retrieval-Augmented Generation (RAG)
* Semantic search using FAISS
* Grounded answer generation
* Transparency and explainability
* Comparison between API-based and local LLMs

---
