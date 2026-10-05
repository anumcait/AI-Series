# 🚀 Day 18 — Build a Vector Database Search 🔎🗄️

**Storing and retrieving knowledge by meaning.**

## 🎯 Project

Build a small **AI Knowledge Search System** using a local vector database.

The application will:

- Store knowledge documents.
- Generate embeddings using Sentence Transformers.
- Store embeddings in ChromaDB.
- Store metadata with every document.
- Accept a user's natural-language question.
- Search the vector database for semantically similar documents.
- Return the top matching results.

## 🔄 How It Works

```text
Knowledge Documents
        ↓
Embedding Model
        ↓
Vector Embeddings
        ↓
┌──────────────────┐
│     ChromaDB     │
│   Vector Store   │
└──────────────────┘
        ↑
        │
   User Question
        ↓
Query Embedding
        ↓
Similarity Search
        ↓
    Top-K Results
```

## 🧠 What Is a Vector Database?

A **vector database** is a database designed to store and search numerical vectors.

AI embedding models convert text into vectors.

For example:

```text
"Terraform manages infrastructure"
                ↓
        Embedding Model
                ↓
[0.12, -0.42, 0.73, 0.18, ...]
```

The vector represents the semantic meaning of the text.

A vector database can compare a query vector against stored vectors and find documents with the closest meaning.

---

## 🔎 Why Use a Vector Database?

Traditional keyword search looks for matching words.

For example:

```text
Query:
How can I automate cloud infrastructure?
```

A keyword search might look for:

```text
automate
cloud
infrastructure
```

But semantic search can understand that:

```text
Terraform allows infrastructure to be managed as code.
```

is highly relevant even though it does not contain the exact phrase:

```text
automate cloud infrastructure
```

The vector database searches based on **semantic similarity** rather than simply matching words.

---

## 🗄️ ChromaDB

For this project, we will use **ChromaDB** as the local vector database.

ChromaDB allows us to:

- Store documents
- Store embeddings
- Store metadata
- Create collections
- Perform similarity searches
- Persist data locally

No cloud database is required.

---

## 📁 Project Structure

Create the Day 18 project like this:

```text
Day-18/
│
├── documents.py
├── semantic_search.py
├── requirements.txt
└── chroma_db/
```

The `chroma_db` directory will be created automatically when the application runs.

---

## 📦 requirements.txt

Create a `requirements.txt` file:

```text
chromadb
sentence-transformers
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## 📚 Knowledge Base

Create `documents.py`:

```python
documents = [
    {
        "text": "AWS EC2 provides scalable virtual servers.",
        "category": "Cloud",
        "technology": "AWS EC2"
    },
    {
        "text": "Amazon S3 provides object storage.",
        "category": "Cloud",
        "technology": "Amazon S3"
    },
    {
        "text": "Docker packages applications into containers.",
        "category": "DevOps",
        "technology": "Docker"
    },
    {
        "text": "Kubernetes manages containerized workloads.",
        "category": "DevOps",
        "technology": "Kubernetes"
    },
    {
        "text": "Terraform allows infrastructure to be managed as code.",
        "category": "DevOps",
        "technology": "Terraform"
    },
    {
        "text": "GitLab CI/CD automates software delivery pipelines.",
        "category": "DevOps",
        "technology": "GitLab CI/CD"
    },
    {
        "text": "Amazon RDS provides managed relational databases.",
        "category": "Database",
        "technology": "Amazon RDS"
    }
]
```

Each document contains three pieces of information:

```text
Document
   │
   ├── text
   ├── category
   └── technology
```

The `text` will be embedded and searched.

The `category` and `technology` will be stored as metadata.

---

## 🔢 Embedding Model

We will use Sentence Transformers to convert text into vectors.

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
```

The model converts text into numerical embeddings.

Example:

```python
text = "Terraform manages infrastructure"

embedding = model.encode(text)

print(embedding)
```

The result is a vector containing numerical values.

The important concept is:

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

The embedding model **creates the vector**.

---

## 🗃️ Creating the ChromaDB Database

Create `semantic_search.py`:

```python
import chromadb
from sentence_transformers import SentenceTransformer

from documents import documents

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create persistent ChromaDB client
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Create collection
collection = client.get_or_create_collection(
    name="devops_knowledge",
    metadata={
        "hnsw:space": "cosine"
    }
)
```

The important part is:

```python
chromadb.PersistentClient(
    path="./chroma_db"
)
```

This creates a persistent local database.

The data remains available after the Python program exits.

---

## 📥 Store Documents

First, extract the document text:

```python
texts = [
    document["text"]
    for document in documents
]
```

Generate embeddings:

```python
embeddings = model.encode(
    texts,
    normalize_embeddings=True
).tolist()
```

Now store the documents, embeddings, and metadata in ChromaDB:

```python
collection.upsert(
    ids=[
        "doc1",
        "doc2",
        "doc3",
        "doc4",
        "doc5",
        "doc6",
        "doc7"
    ],
    documents=texts,
    embeddings=embeddings,
    metadatas=[
        {
            "category": document["category"],
            "technology": document["technology"]
        }
        for document in documents
    ]
)
```

Now ChromaDB contains:

```text
Document
    +
Embedding
    +
Metadata
```

---

## 🏷️ Metadata

Each document contains metadata.

For example:

```python
{
    "category": "DevOps",
    "technology": "Terraform"
}
```

Metadata stores additional information about the document.

Conceptually:

```text
Document
    │
    ├── Text
    │
    ├── Embedding
    │
    └── Metadata
          ├── category
          └── technology
```

Metadata becomes very useful when building advanced retrieval systems.

For example, we could later search only within:

```text
category = DevOps
```

while still using semantic similarity.

---

## 🔍 Searching the Vector Database

Create a search function:

```python
def search(query, top_k=3):

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results
```

The query follows the same embedding process:

```text
User Question
      ↓
Embedding Model
      ↓
Query Vector
      ↓
ChromaDB
      ↓
Similarity Search
      ↓
Top-K Results
```

The vector database compares the query vector against the stored vectors.

---

## 📊 Display Search Results

Add a function to display the results:

```python
def display_results(results):

    documents_found = results["documents"][0]
    metadatas_found = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n" + "=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)

    for index, document in enumerate(documents_found):

        metadata = metadatas_found[index]

        distance = distances[index]

        similarity = 1 - distance

        print(f"\nRank {index + 1}")
        print(f"Technology: {metadata['technology']}")
        print(f"Category: {metadata['category']}")
        print(f"Similarity: {similarity:.2f}")
        print(f"Content: {document}")
```

---

## 🚀 Complete `semantic_search.py`

The complete application:

```python
import chromadb
from sentence_transformers import SentenceTransformer

from documents import documents

# --------------------------------
# Load embedding model
# --------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# --------------------------------
# Create persistent ChromaDB
# --------------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)

# --------------------------------
# Create collection
# --------------------------------

collection = client.get_or_create_collection(
    name="devops_knowledge",
    metadata={
        "hnsw:space": "cosine"
    }
)

# --------------------------------
# Store documents
# --------------------------------

texts = [
    document["text"]
    for document in documents
]

embeddings = model.encode(
    texts,
    normalize_embeddings=True
).tolist()

collection.upsert(
    ids=[
        "doc1",
        "doc2",
        "doc3",
        "doc4",
        "doc5",
        "doc6",
        "doc7"
    ],
    documents=texts,
    embeddings=embeddings,
    metadatas=[
        {
            "category": document["category"],
            "technology": document["technology"]
        }
        for document in documents
    ]
)

# --------------------------------
# Search
# --------------------------------

def search(query, top_k=3):

    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results

# --------------------------------
# Display results
# --------------------------------

def display_results(results):

    documents_found = results["documents"][0]
    metadatas_found = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n" + "=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)

    for index, document in enumerate(documents_found):

        metadata = metadatas_found[index]

        distance = distances[index]

        similarity = 1 - distance

        print(f"\nRank {index + 1}")
        print(f"Technology: {metadata['technology']}")
        print(f"Category: {metadata['category']}")
        print(f"Similarity: {similarity:.2f}")
        print(f"Content: {document}")

# --------------------------------
# User interface
# --------------------------------

if __name__ == "__main__":

    print("AI Knowledge Search")
    print("-" * 30)

    while True:

        query = input("\nEnter your question (or 'exit'): ")

        if query.lower() == "exit":
            break

        results = search(query, top_k=3)

        display_results(results)
```

---

## ▶️ Run the Application

From the Day 18 directory:

```bash
python semantic_search.py
```

You will see:

```text
AI Knowledge Search
------------------------------
```

Enter a question:

```text
How can I automate cloud infrastructure?
```

The application should return results similar to:

```text
============================================================
SEARCH RESULTS
============================================================

Rank 1
Technology: Terraform
Category: DevOps
Similarity: 0.xx
Content: Terraform allows infrastructure to be managed as code.

Rank 2
Technology: GitLab CI/CD
Category: DevOps
Similarity: 0.xx
Content: GitLab CI/CD automates software delivery pipelines.

Rank 3
Technology: AWS EC2
Category: Cloud
Similarity: 0.xx
Content: AWS EC2 provides scalable virtual servers.
```

The exact similarity values can vary depending on the embedding model and implementation.

---

## 🔄 Search Flow

When the user enters:

```text
How can I automate cloud infrastructure?
```

the application performs:

```text
                    User Query
                        │
                        ▼
              Sentence Transformer
                        │
                        ▼
                  Query Vector
                        │
                        ▼
                ┌─────────────┐
                │   ChromaDB  │
                └─────────────┘
                        │
                        ▼
              Compare Vectors
                        │
                        ▼
                  Top 3 Results
                        │
                        ▼
              Display Documents
```

---

## 🧩 Understanding the Components

There are two important components in this system.

### Embedding Model

The embedding model **creates vectors**.

```text
Text
 ↓
Sentence Transformer
 ↓
Vector
```

### Vector Database

ChromaDB **stores and searches vectors**.

```text
Vector
 ↓
ChromaDB
 ↓
Similarity Search
 ↓
Relevant Documents
```

They perform different jobs.

The embedding model is responsible for understanding the text and converting it into a numerical representation.

The vector database is responsible for storing those vectors and efficiently retrieving similar vectors.

---

## 📦 What Is a Collection?

A ChromaDB collection is a logical container for related data.

In this project:

```python
collection = client.get_or_create_collection(
    name="devops_knowledge"
)
```

The collection contains our DevOps knowledge.

Conceptually:

```text
ChromaDB
   │
   └── devops_knowledge
          │
          ├── Document 1
          ├── Document 2
          ├── Document 3
          ├── Document 4
          └── ...
```

A collection keeps related documents and their associated embeddings and metadata together.

---

## 🎯 What Is Top-K Retrieval?

We normally don't want every document in the database.

We want the most relevant documents.

For example:

```python
collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)
```

Here:

```text
n_results = 3
```

means:

> Return the top 3 most relevant documents.

This is called **Top-K retrieval**.

```text
Query
 ↓
Vector Search
 ↓
1. Best match
2. Second best match
3. Third best match
```

The value of `K` can be changed depending on the application.

---

## 📏 Distance vs Similarity

ChromaDB returns a distance value when using cosine distance.

For normalized vectors, a simple way to present an approximate similarity score is:

```python
similarity = 1 - distance
```

A smaller cosine distance means that the vectors are closer.

A larger similarity value means that the documents are more semantically similar.

The displayed similarity should be treated as a ranking signal rather than an absolute percentage of relevance.

---

## 💾 Persistence

One important feature of ChromaDB is persistence.

We use:

```python
chromadb.PersistentClient(
    path="./chroma_db"
)
```

The vector database is therefore stored locally.

The project will create:

```text
Day-18/
│
├── documents.py
├── semantic_search.py
├── requirements.txt
│
└── chroma_db/
```

The `chroma_db` directory contains the persisted database files.

This means the vectors and stored data don't need to exist only in a Python list while the application is running.

---

## 🧪 Day 18 Challenge

Extend the application to make it more realistic.

### Challenge 1 — Add More Technologies

Add documents for:

```text
Prometheus
Grafana
Jenkins
Ansible
Azure
Google Cloud
Redis
PostgreSQL
```

Give each document:

```python
{
    "text": "...",
    "category": "...",
    "technology": "..."
}
```

---

### Challenge 2 — Change Top-K

Allow the user to specify how many results they want.

For example:

```text
How many results? 5
```

Then use:

```python
results = search(query, top_k=5)
```

---

### Challenge 3 — Metadata Filtering

Add the ability to search only within a category.

For example:

```text
Category: DevOps
Query: How can I automate infrastructure?
```

This introduces an important vector-database capability:

```text
Semantic Search
      +
Metadata Filtering
```

The system can use both meaning-based retrieval and structured metadata.

---

## 🧠 Key Concepts to Understand

By the end of Day 18, you should understand:

- What a vector database is
- Why semantic search benefits from vector databases
- What ChromaDB is
- What a collection is
- How documents are stored
- How embeddings are stored
- What metadata is
- How similarity search works
- What Top-K retrieval means
- How query embeddings are generated
- How vectors are persisted locally
- What cosine distance means
- The difference between an embedding model and a vector database

---

## 🔑 Most Important Distinction

Remember:

```text
Embedding Model
      ↓
Creates Vector
      ↓
Vector Database
      ↓
Stores + Searches Vector
```

The embedding model and vector database are **different components**.

The embedding model converts meaning into numbers.

The vector database stores those numbers and retrieves the vectors that are most similar to a query.

---

## 🏗️ Final Day 18 Architecture

```text
                 KNOWLEDGE BASE
                       │
                       ▼
              ┌─────────────────┐
              │ Embedding Model │
              └─────────────────┘
                       │
                       ▼
                  Embeddings
                       │
                       ▼
              ┌─────────────────┐
              │     ChromaDB    │
              │                 │
              │ Documents       │
              │ Embeddings      │
              │ Metadata        │
              └─────────────────┘
                       ▲
                       │
                 Query Embedding
                       ▲
                       │
                 User Question
                       │
                       ▼
              Similarity Search
                       │
                       ▼
                  Top-K Results
```

---
