from rag import MiniRAG
from utils import load_documents, chunk_documents

docs = load_documents()
chunks = chunk_documents(docs)
rag = MiniRAG(chunks)

questions = [
    "What factors affect construction project delays?",
    "What safety rules are mentioned?",
    "What materials are used?",
    "What causes project cost increase?"
]

for q in questions:
    print("="*50)
    print("QUESTION:", q)

    retrieved, api_ans, local_ans = rag.compare_models(q)

    print("\nAPI ANSWER:\n", api_ans)
    print("\nLOCAL ANSWER:\n", local_ans)