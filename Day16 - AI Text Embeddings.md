# 🚀 Day 16 — Understanding AI Text Embeddings 🔢

## Goal

Build a Python application that converts sentences into **numerical embeddings** and compares their semantic similarity.

Instead of:

    Text
     ↓
    Prompt
     ↓
    Gemini
     ↓
    Answer

Day 16 introduces:

    Text
     ↓
    Embedding Model
     ↓
    Vector
     ↓
    Similarity
     ↓
    Meaning

The application will:

- Generate embeddings for sentences
- Display the vector representation
- Calculate cosine similarity
- Compare related and unrelated sentences
- Perform a simple semantic search
- Find the sentence most similar to a query

---

# 🧠 What Are Embeddings?

An embedding is a numerical representation of text meaning.

For example:

    "I love working with Python."
                ↓
         Embedding Model
                ↓
    [0.023, -0.184, 0.421, ...]

Another sentence:

    "Python programming is my favorite."
                ↓
    [0.031, -0.176, 0.408, ...]

The vectors don't need to contain human-readable information.

The important concept is:

    Similar meaning
          ↓
    Similar vectors
          ↓
    Higher similarity

While unrelated sentences should generally have lower similarity.

---

# 1. Project Structure

Create:

    Day-16/
    ├── embedding_explorer.py
    ├── sentences.txt
    └── requirements.txt

After running the application:

    embedding_results.json

will be created.

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

---

# 4. Create the Test Sentences

Create:

    sentences.txt

Use these five sentences:

    Python is a programming language.
    I enjoy writing Python applications.
    AWS provides cloud computing services.
    Cloud infrastructure can be deployed on AWS.
    I like eating pizza.

Each line represents one sentence.

This is important because the Python application will read the sentences dynamically instead of hardcoding them inside the embedding function.

---

# 5. Embedding Model

For this project, use:

    all-MiniLM-L6-v2

The model is provided through `sentence-transformers`.

The application will do:

    Sentence
       ↓
    all-MiniLM-L6-v2
       ↓
    Embedding Vector

You don't need to understand every dimension of the vector.

The purpose of Day 16 is to understand **how text can be represented mathematically**.

---

# 6. Cosine Similarity

To compare two embeddings, we'll use **cosine similarity**.

Conceptually:

    Vector A
       ↘
        Similarity
       ↗
    Vector B

The score is commonly interpreted roughly as:

    Closer to 1
        ↓
    More similar direction

    Closer to 0
        ↓
    Less similar

For this exercise, don't treat a particular numerical threshold as universal. Similarity scores depend on the embedding model and the type of text.

---

# 7. Python Application

Create:

    embedding_explorer.py

Use:

    import json

    import numpy as np
    from sentence_transformers import SentenceTransformer

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    MODEL_NAME = "all-MiniLM-L6-v2"
    SENTENCES_FILE = "sentences.txt"
    OUTPUT_FILE = "embedding_results.json"

    # --------------------------------------------------
    # Load sentences
    # --------------------------------------------------

    def load_sentences(filename: str) -> list[str]:
        """Read sentences from a text file."""

        with open(filename, "r", encoding="utf-8") as file:
            sentences = [
                line.strip()
                for line in file
                if line.strip()
            ]

        return sentences

    # --------------------------------------------------
    # Cosine similarity
    # --------------------------------------------------

    def cosine_similarity(
        vector_a: np.ndarray,
        vector_b: np.ndarray
    ) -> float:
        """Calculate cosine similarity between two vectors."""

        dot_product = np.dot(vector_a, vector_b)

        magnitude_a = np.linalg.norm(vector_a)
        magnitude_b = np.linalg.norm(vector_b)

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return float(
            dot_product / (magnitude_a * magnitude_b)
        )

    # --------------------------------------------------
    # Generate embeddings
    # --------------------------------------------------

    def generate_embeddings(
        model: SentenceTransformer,
        sentences: list[str]
    ) -> np.ndarray:
        """Generate embeddings for a list of sentences."""

        return model.encode(
            sentences,
            convert_to_numpy=True
        )

    # --------------------------------------------------
    # Find most similar sentence
    # --------------------------------------------------

    def find_most_similar(
        query: str,
        model: SentenceTransformer,
        sentences: list[str],
        embeddings: np.ndarray
    ) -> tuple[str, float]:
        """Find the stored sentence closest to the query."""

        query_embedding = model.encode(
            query,
            convert_to_numpy=True
        )

        results = []

        for sentence, embedding in zip(
            sentences,
            embeddings
        ):
            score = cosine_similarity(
                query_embedding,
                embedding
            )

            results.append((sentence, score))

        results.sort(
            key=lambda item: item[1],
            reverse=True
        )

        return results[0]

    # --------------------------------------------------
    # Main application
    # --------------------------------------------------

    def main():

        print("=" * 60)
        print("          DAY 16 - TEXT EMBEDDING EXPLORER")
        print("=" * 60)

        # Load sentences
        print("\nReading sentences...")

        sentences = load_sentences(SENTENCES_FILE)

        print(f"Loaded {len(sentences)} sentences.")

        # Load model
        print("\nLoading embedding model...")
        print(f"Model: {MODEL_NAME}")

        model = SentenceTransformer(MODEL_NAME)

        print("Embedding model loaded.")

        # Generate embeddings
        print("\nGenerating embeddings...")

        embeddings = generate_embeddings(
            model,
            sentences
        )

        print("Embeddings generated.")

        # Display embeddings
        print("\n" + "=" * 60)
        print("EMBEDDINGS")
        print("=" * 60)

        embedding_results = []

        for index, (
            sentence,
            embedding
        ) in enumerate(
            zip(sentences, embeddings),
            start=1
        ):

            print(f"\nSentence {index}:")
            print(sentence)

            print(f"Vector dimensions: {len(embedding)}")

            print("First 5 vector values:")
            print(embedding[:5])

            embedding_results.append({
                "sentence": sentence,
                "dimensions": len(embedding),
                "embedding_preview": embedding[:5].tolist()
            })

        # --------------------------------------------------
        # Part 2 - Compare sentences
        # --------------------------------------------------

        print("\n" + "=" * 60)
        print("SIMILARITY COMPARISON")
        print("=" * 60)

        # Sentence A vs Sentence B
        similarity_ab = cosine_similarity(
            embeddings[0],
            embeddings[1]
        )

        print("\nSentence A:")
        print(sentences[0])

        print("\nSentence B:")
        print(sentences[1])

        print(
            f"\nCosine Similarity: {similarity_ab:.4f}"
        )

        # Sentence A vs Sentence C
        similarity_ac = cosine_similarity(
            embeddings[0],
            embeddings[4]
        )

        print("\n" + "-" * 60)

        print("\nSentence A:")
        print(sentences[0])

        print("\nSentence C:")
        print(sentences[4])

        print(
            f"\nCosine Similarity: {similarity_ac:.4f}"
        )

        # --------------------------------------------------
        # Part 3 - Semantic search
        # --------------------------------------------------

        query = "I want to learn Python programming."

        print("\n" + "=" * 60)
        print("SEMANTIC SEARCH")
        print("=" * 60)

        print("\nQuery:")
        print(query)

        query_embedding = model.encode(
            query,
            convert_to_numpy=True
        )

        search_results = []

        for sentence, embedding in zip(
            sentences,
            embeddings
        ):
            score = cosine_similarity(
                query_embedding,
                embedding
            )

            search_results.append({
                "sentence": sentence,
                "similarity": score
            })

        # Highest similarity first
        search_results.sort(
            key=lambda item: item["similarity"],
            reverse=True
        )

        print("\nSimilarity Results:")

        for result in search_results:
            print(
                f"{result['similarity']:.4f} → "
                f"{result['sentence']}"
            )

        # Most similar sentence
        best_match = search_results[0]

        print("\nMost Similar Sentence:")
        print(best_match["sentence"])

        print(
            f"Similarity Score: "
            f"{best_match['similarity']:.4f}"
        )

        # --------------------------------------------------
        # Save results
        # --------------------------------------------------

        output = {
            "model": MODEL_NAME,
            "sentences": embedding_results,
            "comparisons": {
                "sentence_1_vs_sentence_2": similarity_ab,
                "sentence_1_vs_sentence_5": similarity_ac
            },
            "semantic_search": {
                "query": query,
                "results": search_results
            }
        }

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                output,
                file,
                indent=2
            )

        print("\nResults saved to:")
        print(OUTPUT_FILE)

    if __name__ == "__main__":
        main()

---

# 8. Run the Application

Execute:

    python embedding_explorer.py

The first time you run it, the embedding model may need to be downloaded, so it can take longer than subsequent runs.

You should see something similar to:

    ============================================================
              DAY 16 - TEXT EMBEDDING EXPLORER
    ============================================================

    Reading sentences...
    Loaded 5 sentences.

    Loading embedding model...
    Model: all-MiniLM-L6-v2

    Embedding model loaded.

    Generating embeddings...
    Embeddings generated.

---

# 9. Examine the Embeddings

The application will display something similar to:

    Sentence 1:
    Python is a programming language.

    Vector dimensions: 384

    First 5 vector values:
    [ 0.0123 -0.0842  0.0317  0.0921 -0.0148]

You may see different exact numbers depending on the model/library version.

The important thing is:

    Python is a programming language.
                    ↓
              384-dimensional
                 vector

Don't try to interpret:

    0.0123
    -0.0842
    0.0317

individually.

The **whole vector** represents the sentence.

---

# 10. Part 1 — Generate Embeddings

Your first experiment is simply:

    Sentence 1
        ↓
    Embedding

    Sentence 2
        ↓
    Embedding

    Sentence 3
        ↓
    Embedding

    Sentence 4
        ↓
    Embedding

    Sentence 5
        ↓
    Embedding

You have now converted text into numerical representations.

This is the fundamental difference from your previous projects.

---

# 11. Part 2 — Compare Similarity

The program compares:

### Comparison 1

    Python is a programming language.
                  ↕
    I enjoy writing Python applications.

Both sentences discuss Python/programming, so you should generally see a relatively high similarity compared with an unrelated sentence.

### Comparison 2

    Python is a programming language.
                  ↕
    I like eating pizza.

These sentences have very different meanings, so the similarity should generally be lower.

The exact scores are model-dependent.

---

# 12. Part 3 — Semantic Search

Now we give the application a query:

    I want to learn Python programming.

The application does:

                         Query
                           │
                           ▼
             "I want to learn Python programming."
                           │
                           ▼
                    Embedding Model
                           │
                           ▼
                      Query Vector
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Vector 1      Vector 2      Vector 3
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                   Cosine Similarity
                           │
                           ▼
                     Sort Results
                           │
                           ▼
                  Highest Similarity

The output will look roughly like:

    Similarity Results:

    0.xxxx → Python is a programming language.
    0.xxxx → I enjoy writing Python applications.
    0.xxxx → Cloud infrastructure can be deployed on AWS.
    0.xxxx → AWS provides cloud computing services.
    0.xxxx → I like eating pizza.

    Most Similar Sentence:
    Python is a programming language.

    Similarity Score: 0.xxxx

Don't expect those exact scores or necessarily that exact ordering—the model determines the actual numerical results.

---

# 13. Generated File

After running the program:

    embedding_results.json

will be created.

The structure will look like:

    {
      "model": "all-MiniLM-L6-v2",
      "sentences": [
        {
          "sentence": "Python is a programming language.",
          "dimensions": 384,
          "embedding_preview": [
            0.0123,
            -0.0842,
            0.0317,
            0.0921,
            -0.0148
          ]
        }
      ],
      "comparisons": {
        "sentence_1_vs_sentence_2": 0.0,
        "sentence_1_vs_sentence_5": 0.0
      },
      "semantic_search": {
        "query": "I want to learn Python programming.",
        "results": []
      }
    }

The numbers shown here are placeholders. Your program will write the actual values.

---

# 14. Project Structure After Running

You should now have:

    Day-16/
    ├── embedding_explorer.py
    ├── sentences.txt
    ├── requirements.txt
    └── embedding_results.json

---


# 🔥 Why Embeddings Matter

This simple project is the foundation for:

    Semantic Search
          ↓
    Recommendation Systems
          ↓
    Document Retrieval
          ↓
    Vector Databases
          ↓
    RAG
          ↓
    AI Knowledge Bases

For example, imagine you have **10,000 company documents**.

Instead of asking an LLM to read all 10,000 every time:

    10,000 Documents
           ↓
    Generate embeddings
           ↓
    Store vectors
           ↓
    User asks a question
           ↓
    Embed the question
           ↓
    Similarity search
           ↓
    Retrieve relevant documents
           ↓
    Send relevant documents to LLM
           ↓
          Answer

That is the basic idea behind a modern **RAG pipeline**.

---

# 📚 Key Concepts Learned

- Text embeddings
- Vector representations
- Embedding dimensions
- Sentence Transformers
- `all-MiniLM-L6-v2`
- NumPy arrays
- Dot product
- Vector magnitude
- Cosine similarity
- Semantic similarity
- Semantic search
- Vector-based retrieval
- Foundation of RAG
- Vector databases

---

### Screenshots
