# 🚀 Day 17 — AI Semantic Search 🔎

## Goal
Build a Python application that searches a collection of DevOps and Cloud documents based on **semantic meaning** instead of exact keyword matching.

Instead of:

    User Query
        ↓
    Keyword Matching
        ↓
    Matching Words
        ↓
    Results

Day 17 introduces:

    Documents
        ↓
    Embedding Model
        ↓
    Document Vectors
        ↓
    User Query
        ↓
    Query Vector
        ↓
    Cosine Similarity
        ↓
    Ranking
        ↓
    Top 3 Results

The application will:

- Create a small Cloud/DevOps knowledge collection
- Generate embeddings for the documents
- Generate an embedding for the user query
- Calculate cosine similarity
- Rank documents by similarity
- Return the top 3 most relevant results
- Demonstrate searching by meaning instead of exact keywords

---

# 🧠 What Is Semantic Search?

Traditional keyword search looks for exact words.

For example:

    How can I automate AWS infrastructure?

A keyword search may look for:

    AWS
    automate
    infrastructure

Semantic search works differently.

It converts the query and documents into numerical vectors called **embeddings**.

For example:

    "How can I automate AWS infrastructure?"
                    ↓
              Embedding Model
                    ↓
                Query Vector

And:

    "Terraform allows infrastructure to be defined as code."
                    ↓
              Embedding Model
                    ↓
              Document Vector

The two vectors can then be compared using cosine similarity.

The important idea is:

    Similar meaning
          ↓
    Similar vector representation
          ↓
    Higher similarity

The query does not necessarily need to contain the exact word:

    Terraform

to retrieve a document about Terraform.

---

# 1. Project Structure

Create:

    Day-17/
    ├── semantic_search.py
    ├── documents.py
    └── requirements.txt

After running the application:

    __pycache__/

may also be created automatically by Python.

The final structure may look like:

    Day-17/
    ├── semantic_search.py
    ├── documents.py
    ├── requirements.txt
    └── __pycache__/

---

# 2. Install Dependencies

Activate your virtual environment:

    source ../../venv/Scripts/activate

Install:

    python -m pip install -U sentence-transformers numpy

Verify:

    python -c "from sentence_transformers import SentenceTransformer; print('sentence-transformers works')"

And:

    python -c "import numpy; print('numpy works')"

---

# 3. requirements.txt

Create:

    requirements.txt

Use:

    sentence-transformers
    numpy

Install:

    python -m pip install -r requirements.txt

If the installation fails because Python is using a different environment, verify:

    which python

The Python executable should point to your virtual environment.

For example:

    /d/AI-Series/venv/Scripts/python

Then verify pip:

    python -m pip --version

This is preferable to using a separate `pip` executable because it ensures pip belongs to the Python interpreter being used to run the project.

---

# 4. Create the Knowledge Collection

Create:

    documents.py

Use these Cloud and DevOps documents:

    documents = [
        "AWS EC2 provides resizable compute capacity.",
        "Amazon S3 is an object storage service.",
        "Docker packages applications into portable containers.",
        "Kubernetes orchestrates containerized applications.",
        "Terraform allows infrastructure to be defined as code.",
        "GitLab CI/CD automates software build and deployment pipelines.",
        "AWS Lambda runs code without managing servers.",
        "Amazon RDS provides managed relational databases.",
        "AWS VPC provides networking capabilities for cloud resources.",
        "Prometheus collects metrics and monitors applications and infrastructure.",
        "Grafana provides dashboards for monitoring metrics and system performance.",
        "Ansible automates configuration management and application deployment.",
        "Jenkins automates continuous integration and continuous delivery.",
        "Amazon CloudWatch monitors AWS resources and applications.",
        "Docker Compose defines and runs multi-container applications."
    ]

Each item represents one document in our small knowledge collection.

---

# 5. Embedding Model

For this project, use:

    all-MiniLM-L6-v2

The model is provided through `sentence-transformers`.

The application will do:

    Document
        ↓
    all-MiniLM-L6-v2
        ↓
    Document Embedding

The user query follows the same process:

    User Query
        ↓
    all-MiniLM-L6-v2
        ↓
    Query Embedding

The query embedding can then be compared with all document embeddings.

---

# 6. Cosine Similarity

To compare the query embedding with each document embedding, we use **cosine similarity**.

Conceptually:

    Query Vector
          ↘
           Similarity
          ↗
    Document Vector

The basic formula is:

    cosine similarity =
        (A · B) / (||A|| × ||B||)

In general:

    Higher similarity
        ↓
    More similar vector direction

    Lower similarity
        ↓
    Less similar vector direction

For this project, don't treat a particular numerical threshold as universal.

Similarity scores depend on:

- The embedding model
- The document text
- The query
- The domain
- The amount of context

The main purpose here is to rank the documents relative to one another.

---

# 7. Python Application

Create:

    semantic_search.py

Use:

    from sentence_transformers import SentenceTransformer
    import numpy as np

    from documents import documents

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    MODEL_NAME = "all-MiniLM-L6-v2"
    TOP_K = 3

    # --------------------------------------------------
    # Load embedding model
    # --------------------------------------------------

    print("🔄 Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("✅ Embedding model loaded.")

    # --------------------------------------------------
    # Generate document embeddings
    # --------------------------------------------------

    print("🔄 Generating document embeddings...")

    document_embeddings = model.encode(
        documents,
        convert_to_numpy=True
    )

    print("✅ Document embeddings generated.")

    # --------------------------------------------------
    # Cosine similarity
    # --------------------------------------------------

    def cosine_similarity(
        vector_a: np.ndarray,
        vector_b: np.ndarray
    ) -> float:
        """Calculate cosine similarity between two vectors."""

        dot_product = np.dot(
            vector_a,
            vector_b
        )

        magnitude_a = np.linalg.norm(vector_a)
        magnitude_b = np.linalg.norm(vector_b)

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return float(
            dot_product /
            (magnitude_a * magnitude_b)
        )

    # --------------------------------------------------
    # Semantic search
    # --------------------------------------------------

    def semantic_search(
        query: str,
        top_k: int = TOP_K
    ):
        """Find documents that are semantically similar to a query."""

        # Convert query into an embedding
        query_embedding = model.encode(
            query,
            convert_to_numpy=True
        )

        results = []

        # Compare query against every document
        for index, document_embedding in enumerate(
            document_embeddings
        ):

            similarity = cosine_similarity(
                query_embedding,
                document_embedding
            )

            results.append({
                "document": documents[index],
                "similarity": similarity
            })

        # Highest similarity first
        results.sort(
            key=lambda result: result["similarity"],
            reverse=True
        )

        return results[:top_k]

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------

    def display_results(
        query: str,
        results: list[dict]
    ):
        """Display search results."""

        print("\n" + "=" * 60)
        print("🔎 SEMANTIC SEARCH RESULTS")
        print("=" * 60)

        print(f"\nQuery: {query}")

        for rank, result in enumerate(
            results,
            start=1
        ):

            print(f"\n{rank}. {result['document']}")

            print(
                f"   Similarity: "
                f"{result['similarity']:.4f}"
            )

    # --------------------------------------------------
    # Main application
    # --------------------------------------------------

    def main():

        print("=" * 60)
        print("       🚀 DAY 17 — AI SEMANTIC SEARCH")
        print("=" * 60)

        print("\nSearch by meaning, not just keywords.")
        print("Type 'exit' to quit.")

        while True:

            query = input("\nSearch: ").strip()

            # Exit condition
            if query.lower() == "exit":

                print("\n👋 Goodbye!")

                break

            # Empty query
            if not query:

                print(
                    "⚠️ Please enter a search query."
                )

                continue

            # Perform semantic search
            results = semantic_search(
                query,
                TOP_K
            )

            # Display results
            display_results(
                query,
                results
            )

    # --------------------------------------------------
    # Run application
    # --------------------------------------------------

    if __name__ == "__main__":
        main()

---

# 8. Run the Application

Navigate to the project:

    cd /d/AI-Series/Practice-Lab/Day-17

Activate the virtual environment if necessary:

    source ../../venv/Scripts/activate

Verify Python:

    which python

Verify the package:

    python -m pip show sentence-transformers

Then run:

    python semantic_search.py

The first run may take longer because the Sentence Transformer model needs to be downloaded and loaded.

---

# 9. Test Query — Infrastructure Automation

Enter:

    How can I automate infrastructure?

The application should return documents related to infrastructure automation.

Relevant documents include:

    Terraform allows infrastructure to be defined as code.

    Ansible automates configuration management and application deployment.

The important point is that the query does not explicitly mention:

    Terraform

or:

    Ansible

The model uses semantic similarity to connect the concepts.

---

# 10. Test Query — AWS Object Storage

Enter:

    Which AWS service provides object storage?

A highly relevant result should be:

    Amazon S3 is an object storage service.

The query uses:

    object storage

while the document contains:

    object storage service

The embedding model represents the meaning of the text so that the relevant document can be retrieved.

---

# 11. Test Query — Containers

Enter:

    How can I run applications in containers?

Relevant documents should include:

    Docker packages applications into portable containers.

    Kubernetes orchestrates containerized applications.

    Docker Compose defines and runs multi-container applications.

The search engine compares the meaning of the query against all stored document vectors.

---

# 12. Test Query — Managed Database

Enter:

    What can I use for managed relational databases?

A highly relevant result should be:

    Amazon RDS provides managed relational databases.

Again, the query does not need to exactly reproduce the document sentence.

---

# 13. Example Output

A typical session may look like:

    ============================================================
           🚀 DAY 17 — AI SEMANTIC SEARCH
    ============================================================

    Search by meaning, not just keywords.
    Type 'exit' to quit.

    Search: How can I automate infrastructure?

    ============================================================
    🔎 SEMANTIC SEARCH RESULTS
    ============================================================

    Query: How can I automate infrastructure?

    1. Terraform allows infrastructure to be defined as code.
       Similarity: 0.xxxx

    2. Ansible automates configuration management and application deployment.
       Similarity: 0.xxxx

    3. GitLab CI/CD automates software build and deployment pipelines.
       Similarity: 0.xxxx

The exact similarity scores and ordering depend on the model and the text.

---

# 14. What Happens Internally?

When the application starts, it loads the model:

    SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

Then every document is converted into an embedding:

    Document
        ↓
    Embedding Model
        ↓
    Document Vector

For example:

    Terraform allows infrastructure to be defined as code.
                            ↓
                     Embedding Model
                            ↓
                       Document Vector

These vectors are stored in memory in:

    document_embeddings

---

# 15. User Query Processing

When the user enters:

    How can I automate infrastructure?

The query is converted into an embedding:

    User Query
        ↓
    Embedding Model
        ↓
    Query Vector

The query vector is then compared with every document vector.

---

# 16. Similarity Calculation

For every document:

    Query Vector
         ↓
    Cosine Similarity
         ↓
    Document Vector

For example:

    Query
      │
      ├── Document 1 → 0.xxxx
      ├── Document 2 → 0.xxxx
      ├── Document 3 → 0.xxxx
      ├── Document 4 → 0.xxxx
      ├── Document 5 → 0.xxxx
      └── Document N → 0.xxxx

The application then sorts the documents:

    Highest Similarity
            ↓
        Document 1
        Document 2
        Document 3
            ↓
    Lowest Similarity

Finally, it returns:

    Top 3

---

# 17. Complete Semantic Search Pipeline

The complete Day 17 system is:

    Documents
        ↓
    Sentence Transformer
        ↓
    Document Embeddings
        ↓
    Store Embeddings
        ↓
        │
        │
    User Query
        ↓
    Sentence Transformer
        ↓
    Query Embedding
        ↓
    Cosine Similarity
        ↓
    Compare Against Documents
        ↓
    Sort by Similarity
        ↓
    Top 3 Results

---

# 18. Keyword Search vs Semantic Search

## Keyword Search

Keyword search primarily depends on matching words.

Example:

    Query:
    How can I automate AWS infrastructure?

The search system may look for:

    AWS
    automate
    infrastructure

It may have difficulty when the relevant document uses different wording.

---

## Semantic Search

Semantic search converts the text into embeddings.

    Query
        ↓
    Query Embedding
        ↓
    Compare Meaning
        ↓
    Relevant Documents

For example:

    Query:
    How can I automate infrastructure?

can retrieve:

    Terraform allows infrastructure to be defined as code.

even though the word:

    Terraform

is not present in the query.

---

# 19. Why Embeddings Are Useful

Embeddings allow machines to work with the semantic representation of text.

Instead of storing only:

    Text

we can also represent it as:

    Text
      ↓
    Numerical Vector

For example:

    "Docker packages applications into portable containers."
                            ↓
                     [0.12, -0.43, ...]
                            ↓
                      Vector Space

Another related sentence may have a nearby representation.

This allows similarity calculations to be performed mathematically.

---

# 20. Top-K Retrieval

The application uses:

    TOP_K = 3

This means only the three highest-scoring documents are returned.

For example:

    Document A → 0.87
    Document B → 0.82
    Document C → 0.76
    Document D → 0.42
    Document E → 0.31

The application returns:

    1. Document A
    2. Document B
    3. Document C

This concept is called **Top-K retrieval**.

---

# 21. Important Note About Similarity Scores

Do not expect specific scores such as:

    0.89
    0.76
    0.52

every time.

The actual score depends on:

- Embedding model
- Query wording
- Document wording
- Number of documents
- Domain
- Model/library versions

For example:

    Terraform document → 0.81

in one experiment does not mean the same document must always produce:

    0.81

with another query.

The important goal of this project is to understand **semantic ranking**.

---

# 22. Interactive Search

The application runs continuously:

    Search: How can I automate infrastructure?

    Results...

    Search: Which AWS service provides object storage?

    Results...

    Search: How can I run applications in containers?

    Results...

The user can continue searching until:

    exit

is entered.

---

# 23. Key Functions

The application has three main parts.

## `cosine_similarity()`

Responsible for comparing two vectors.

    vector_a
        +
    vector_b
        ↓
    Cosine Similarity

---

## `semantic_search()`

Responsible for:

- Embedding the query
- Comparing it with documents
- Calculating similarity
- Sorting results
- Returning Top-K results

---

## `display_results()`

Responsible for presenting:

- Rank
- Document
- Similarity score

---

# 24. What I Built

I built a small semantic search engine that:

1. Stores a collection of Cloud and DevOps knowledge.
2. Loads a Sentence Transformer model.
3. Converts every document into an embedding.
4. Converts the user's query into an embedding.
5. Calculates cosine similarity.
6. Ranks the documents.
7. Returns the top 3 results.

---

# 25. What I Learned

Day 17 introduced the basic retrieval pipeline:

    Text
        ↓
    Embedding
        ↓
    Vector
        ↓
    Similarity
        ↓
    Ranking
        ↓
    Retrieval

The most important idea is:

    Search by meaning
          ↓
    Not only by keywords

---

# 26. Connection to RAG

Semantic search is one of the fundamental building blocks of **Retrieval-Augmented Generation (RAG)**.

Day 17:

    Documents
        ↓
    Embeddings
        ↓
    Similarity Search
        ↓
    Top Results

A future RAG system can extend this:

    Documents
        ↓
    Chunking
        ↓
    Embeddings
        ↓
    Vector Database
        ↓
    Semantic Retrieval
        ↓
    Relevant Context
        ↓
    LLM
        ↓
    Generated Answer

The important progression is:

    Day 16
    Understanding Embeddings
        ↓
    Day 17
    Semantic Search
        ↓
    Future
    Vector Databases
        ↓
    Future
    RAG

---

# 27. Future Improvements

This basic semantic search engine can later be extended with:

- More documents
- PDF documents
- TXT documents
- Markdown documents
- Persistent embeddings
- FAISS
- ChromaDB
- Vector databases
- Metadata filtering
- Hybrid search
- RAG
- LLM-generated answers
- Web interface
- REST API

For Day 17, the goal is intentionally simple.

The main concept is:

    Documents
        ↓
    Embeddings
        ↓
    Query Embedding
        ↓
    Cosine Similarity
        ↓
    Ranking
        ↓
    Top 3 Results

---

### Technologies Used

- Python
- Sentence Transformers
- NumPy
- Cosine Similarity

### Main Learning

**Semantic search allows applications to search information by meaning instead of relying only on exact keywords.**

---

> Search by meaning, not just keywords.

### Screenshots
