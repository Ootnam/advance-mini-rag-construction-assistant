import os
import re
from langchain_text_splitters import MarkdownTextSplitter

for file in os.listdir(folder):
    if file.endswith(".md"):
        docs = []

        for file in os.listdir(folder):
            if file.endswith(".md") or file.endswith(".txt"):
                with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                    content = f.read()

                    # remove numbering like 1), 2)
                    content = re.sub(r"\d+\)", "", content)

                    docs.append(content)

    return docs


def chunk_documents(docs):
    splitter = MarkdownTextSplitter(chunk_size=300, chunk_overlap=50)

    chunks = []
    for doc in docs:
        chunks.extend(splitter.split_text(doc))

    return chunks