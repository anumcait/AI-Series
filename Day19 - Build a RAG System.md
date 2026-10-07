# 🚀 Day 19 — Build a RAG System 📚🤖

> Retrieve relevant internal knowledge and generate grounded AI answers.

## 🎯 Objective

Build a simple **RAG Knowledge Assistant** that:

1. Stores internal DevOps knowledge in ChromaDB.
2. Converts the user's question into an embedding.
3. Retrieves relevant documents using semantic search.
4. Sends only the retrieved context to Gemini.
5. Returns a grounded answer with its sources.

The knowledge source is **internal only**. No web search or external documents are used.

---

## 🏗️ Architecture

```text
Internal Documents
       ↓
Document Embeddings
       ↓
    ChromaDB
       ↑
       │
User Question
       ↓
Query Embedding
       ↓
Similarity Search
       ↓
Relevant Documents
       ↓
     Context
       ↓
     Gemini
       ↓
Grounded Answer
       +
    Sources
```

---

## 📁 Project Structure

```text
Day-19/
│
├── venv/
├── chroma_db/
│
├── documents.py
├── rag.py
├── requirements.txt
└── day.md
```

---

## 📦 requirements.txt

```text
sentence-transformers
chromadb
google-genai
```

Install:

```bash
pip install -r requirements.txt
```

---

## 📄 documents.py

This file contains the internal knowledge base.

```python
documents = [
    "AWS EC2 provides virtual compute capacity.",

    "Amazon S3 is an object storage service.",

    "Amazon RDS provides managed relational databases.",

    "AWS Lambda runs code without provisioning servers.",

    "Docker packages applications into portable containers.",

    "Kubernetes orchestrates containerized workloads.",

    "Terraform allows infrastructure to be defined as code.",

    "GitLab CI/CD automates software build and deployment pipelines."
]
```

These documents are the **source of truth** for the RAG application.

---

## 🔑 Gemini API Key

Set the API key as an environment variable.

PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Do not hard-code the API key inside the Python files.

---

# 🧠 Core RAG Implementation

## 📄 rag.py

```python
import os
import json

import chromadb
from sentence_transformers import SentenceTransformer
from google import genai

from documents import documents

# --------------------------------------------------
# Configuration
# --------------------------------------------------

CHROMA_PATH = "./chroma_db"

COLLECTION_NAME = "day19_devops_knowledge"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TOP_K = 3

MAX_DISTANCE = 0.8

GEMINI_MODEL = "gemini-2.5-flash"

# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

# --------------------------------------------------
# Create ChromaDB
# --------------------------------------------------

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

try:
    collection = chroma_client.get_collection(
        name=COLLECTION_NAME
    )

except Exception:

    collection = chroma_client.create_collection(
        name=COLLECTION_NAME
    )

# --------------------------------------------------
# Store internal documents
# --------------------------------------------------

if collection.count() == 0:

    print("Creating document embeddings...")

    embeddings = embedding_model.encode(
        documents
    ).tolist()

    ids = [
        f"doc_{i}"
        for i in range(len(documents))
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )

    print(
        f"Stored {len(documents)} documents."
    )

# --------------------------------------------------
# Gemini client
# --------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception(
        "GEMINI_API_KEY is not set."
    )

client = genai.Client(
    api_key=api_key
)

# --------------------------------------------------
# Retrieve relevant documents
# --------------------------------------------------

def retrieve_documents(question):

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )

    documents_found = results["documents"][0]

    distances = results["distances"][0]

    retrieved_documents = []

    retrieved_distances = []

    for document, distance in zip(
        documents_found,
        distances
    ):

        if distance <= MAX_DISTANCE:

            retrieved_documents.append(
                document
            )

            retrieved_distances.append(
                distance
            )

    return (
        retrieved_documents,
        retrieved_distances
    )

# --------------------------------------------------
# Generate grounded answer
# --------------------------------------------------

def generate_answer(
    question,
    retrieved_documents
):

    if not retrieved_documents:

        return {
            "answer": (
                "I couldn't find relevant information "
                "about this in the provided knowledge base."
            ),
            "sources": []
        }

    context = "\n\n".join(
        retrieved_documents
    )

    prompt = f"""
You are an internal DevOps knowledge assistant.

Answer the question using ONLY the provided
internal knowledge.

Rules:

- Do not use general knowledge.
- Do not invent information.
- Do not use information outside the context.
- If the answer is not available, say that
  you could not find it in the knowledge base.

Internal Knowledge:
-------------------------
{context}
-------------------------

Question:
{question}

Give a concise answer.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    answer = response.text.strip()

    return {
        "answer": answer,
        "sources": retrieved_documents
    }

# --------------------------------------------------
# RAG pipeline
# --------------------------------------------------

def rag(question):

    print("\n" + "=" * 60)
    print("QUESTION")
    print("=" * 60)

    print(question)

    retrieved_documents, distances = (
        retrieve_documents(question)
    )

    print("\nRetrieved Documents:")

    for index, document in enumerate(
        retrieved_documents,
        start=1
    ):

        print(
            f"{index}. {document}"
        )

        print(
            f"   Distance: "
            f"{distances[index - 1]:.4f}"
        )

    result = generate_answer(
        question,
        retrieved_documents
    )

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(result["answer"])

    print("\nSources:")

    if result["sources"]:

        for source in result["sources"]:
            print(f"- {source}")

    else:

        print("No sources found.")

    print("\nJSON Response:")

    print(
        json.dumps(
            result,
            indent=2
        )
    )

# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("DAY 19 - RAG KNOWLEDGE ASSISTANT")
    print("=" * 60)

    print(
        "Knowledge source: Internal ChromaDB"
    )

    while True:

        question = input(
            "\nAsk a question (or type 'exit'): "
        )

        if question.lower() == "exit":
            break

        if not question.strip():
            continue

        rag(question)
```

---

# 🔄 How the Code Works

### 1. Documents are embedded

```python
embeddings = embedding_model.encode(
    documents
).tolist()
```

Each internal document becomes a vector.

### 2. Documents are stored

```python
collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings
)
```

ChromaDB stores the documents and their embeddings.

### 3. User question is embedded

```python
query_embedding = embedding_model.encode(
    question
).tolist()
```

### 4. ChromaDB retrieves relevant documents

```python
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=TOP_K
)
```

### 5. Retrieved documents become context

```python
context = "\n\n".join(
    retrieved_documents
)
```

### 6. Gemini receives the context

```python
response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents=prompt
)
```

The prompt explicitly restricts Gemini to the internal context.

---

# 🧪 Test 1 — Infrastructure

Question:

```text
How can I automate infrastructure?
```

Expected retrieval:

```text
Terraform allows infrastructure to be defined as code.
```

Expected answer:

```text
Terraform can be used to automate infrastructure
by defining infrastructure as code.
```

Example response:

```json
{
  "answer": "Terraform can be used to automate infrastructure by defining infrastructure as code.",
  "sources": [
    "Terraform allows infrastructure to be defined as code."
  ]
}
```

---

# 🧪 Test 2 — AWS Storage

Question:

```text
Which AWS service should I use for storing files?
```

Relevant internal document:

```text
Amazon S3 is an object storage service.
```

Expected answer:

```text
Amazon S3 is suitable for storing files because
it is an object storage service.
```

---

# 🧪 Test 3 — Docker

Question:

```text
What does Docker do?
```

Relevant source:

```text
Docker packages applications into portable containers.
```

The answer should be generated from this internal document.

---

# 🚫 Test 4 — Hallucination

Question:

```text
What is AWS CloudFront?
```

CloudFront does not exist in our knowledge base.

Expected:

```text
I couldn't find relevant information about this
in the provided knowledge base.
```

Sources:

```json
[]
```

This demonstrates **grounded generation**.

---

# ⭐ Why Sources Matter

The application returns:

```json
{
  "answer": "...",
  "sources": [
    "Terraform allows infrastructure to be defined as code."
  ]
}
```

The `sources` are the actual documents retrieved from the internal ChromaDB.

This provides basic **traceability**:

```text
Answer
  ↓
Retrieved Context
  ↓
Internal Source Document
```

---

# 🎯 Key Concept

Traditional LLM:

```text
Question
   ↓
LLM
   ↓
Answer
```

RAG:

```text
Question
   ↓
Retrieve Internal Knowledge
   ↓
Relevant Context
   ↓
LLM
   ↓
Grounded Answer
```

The main idea is:

> **Retrieval finds the knowledge. Generation turns the retrieved knowledge into an answer.**

## ✅ Day 19 Outcome

You have built a complete RAG pipeline with:

- Internal knowledge
- Embeddings
- ChromaDB
- Semantic retrieval
- Context construction
- Gemini generation
- Source attribution
- Basic hallucination protection

```text
RETRIEVAL
    +
GENERATION
    =
   RAG
```

### Screenshots
