import os
import streamlit as st
from docx import Document
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ---------------- Load Documents ----------------
def load_documents(folder="documents"):
    texts = []
    sources = []

    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_dir, folder)

    if not os.path.exists(folder_path):
        return texts, sources

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)

        # Try DOCX
        if file.endswith(".docx"):
            try:
                doc = Document(path)
                content = "\n".join(p.text for p in doc.paragraphs)
            except Exception:
                print(f"Skipping unreadable file: {file}")
                continue

        # TXT fallback (guaranteed to work)
        elif file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

        else:
            continue

        if content.strip():
            texts.append(content)
            sources.append(file)

    return texts, sources


# ---------------- Simple Text Splitter ----------------
def split_text(text, chunk_size=400):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

# ---------------- Build Vector Store ----------------
def build_faiss(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    return index, embeddings, model

# ---------------- Answer Question ----------------
def answer_question(query, chunks, sources, index, model):
    query_emb = model.encode([query]).astype("float32")
    distances, indices = index.search(query_emb, 1)

    # Relaxed threshold
    if distances[0][0] > 5.0:
        return "❌ I don’t have enough information in the documents.", None

    answer = chunks[indices[0][0]]
    return answer, sources[0]


# ---------------- Streamlit UI ----------------
st.title("📄 Document-Based Q&A AI Agent (No Hallucination)")

docs, doc_sources = load_documents()
if not docs:
    st.error("No readable documents found. Please add .docx or .txt files.")
    st.stop()


all_chunks = []
for text in docs:
    all_chunks.extend(split_text(text))

index, embeddings, model = build_faiss(all_chunks)

query = st.text_input("Ask a question from internal documents:")

if query:
    answer, source = answer_question(query, all_chunks, doc_sources, index, model)

    st.subheader("Answer")
    st.write(answer)

    if source:
        st.subheader("Source")
        st.write(source)
        st.subheader("Source")
x)

