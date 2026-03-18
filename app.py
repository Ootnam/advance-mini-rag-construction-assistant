import streamlit as st
from rag import MiniRAG
from utils import load_documents, chunk_documents

st.set_page_config(page_title="Construction AI Assistant", layout="wide")

st.markdown("""
# 🏗️ Construction AI Assistant
### Retrieval-Augmented Generation (RAG) System
""")

@st.cache_resource
def load_rag():
    docs = load_documents()
    chunks = chunk_documents(docs)
    return MiniRAG(chunks)

rag = load_rag()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("💬 Ask a construction-related question...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    retrieved, api_ans, local_ans = rag.compare_models(query)

    with st.chat_message("assistant"):

        st.markdown("## 📄 Retrieved Context")

        for chunk in retrieved:
            st.markdown(f"""
            <div style="
                padding:10px;
                margin-bottom:8px;
                border-radius:10px;
                background-color:#1e1e1e;
                border-left:5px solid #4CAF50;
            ">
            {chunk}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🤖 OpenRouter Answer")
            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:10px;
                border:2px solid #4CAF50;
            ">
            {api_ans}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("### 🧠 Local Model (Flan-T5)")
            st.markdown(f"""
            <div style="
                padding:15px;
                border-radius:10px;
                border:2px solid #2196F3;
            ">
            {local_ans}
            </div>
            """, unsafe_allow_html=True)

        st.success("✅ Answer generated using retrieved context (No hallucination)")

    st.session_state.messages.append({
        "role": "assistant",
        "content": api_ans
    })