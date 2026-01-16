📄 Document-Based Q&A AI Agent
Problem

Build an AI agent that answers user questions only using internal documents and avoids hallucination when information is missing.

Solution

A Streamlit-based document Q&A system that uses semantic search to retrieve answers strictly from internal documents. If relevant information is not found, the system safely refuses to answer.

Tech Stack

Python

Streamlit

SentenceTransformers

FAISS

How It Works

Loads internal documents from the documents/ folder

Converts text into embeddings

Searches relevant content using FAISS

Returns grounded answers with source reference

Refuses out-of-scope questions

Example Queries

Answered:

What technologies are used?

Refused:

Who is the CEO?

Run the App
pip install -r requirements.txt
streamlit run app.py

Key Feature

✅ No hallucination — answers are strictly document-based.