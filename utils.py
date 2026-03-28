import os
import re
from langchain_text_splitters import MarkdownTextSplitter


def load_documents(folder="data"):
    docs = []

    # Safety check (important for Streamlit Cloud)
    if not os.path.exists(folder):
        print("Folder not found:", folder)
        return []

    for file in os.listdir(folder):
        if file.endswith(".md") or file.endswith(".txt"):
            file_path = os.path.join(folder, file)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                # remove numbering like 1), 2)
                content = re.sub(r"\d+\)", "", content)

                docs.append(content)

    print("Loaded documents:", len(docs))
    return docs


def chunk_documents(docs):
    splitter = MarkdownTextSplitter(chunk_size=300, chunk_overlap=50)

    chunks = []
    for doc in docs:
        chunks.extend(splitter.split_text(doc))

    print("Total chunks:", len(chunks))
    return chunks