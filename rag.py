from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np
import faiss
import requests

class MiniRAG:
    def __init__(self, chunks):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

        self.chunks = chunks
        embeddings = self.model.encode(chunks)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings))

    def retrieve(self, query, k=5):
        query_vec = self.model.encode([query])
        distances, indices = self.index.search(query_vec, k)

        candidates = [self.chunks[i] for i in indices[0]]

        pairs = [(query, c) for c in candidates]
        scores = self.reranker.predict(pairs)

        ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)

        return [r[0] for r in ranked[:3]]  # ✅ FIXED

    def build_prompt(self, context, query):
        return f"""
You are a strict AI assistant.

STRICT RULES:
- Answer ONLY from context
- If not found → "Not found in documents"
- Extract ALL relevant points
- Answer in bullet points

Context:
{context}

Question:
{query}

Answer:
"""

    def generate_api_answer(self, prompt):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        return f"Error: {data}"

    def generate_local_answer(self, prompt):
        from transformers import pipeline

        generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base"
        )

        result = generator(prompt, max_length=200)
        return result[0]["generated_text"]

    def compare_models(self, query):
        retrieved = self.retrieve(query)
        context = "\n\n".join(retrieved)

        prompt = self.build_prompt(context, query)

        api_ans = self.generate_api_answer(prompt)
        local_ans = self.generate_local_answer(prompt)

        return retrieved, api_ans, local_ans