from sentence_transformers import SentenceTransformer
import numpy as np

from documents import documents

# --------------------------------------------------
# 1. Load the embedding model
# --------------------------------------------------

print("🔄 Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("✅ Model loaded successfully!")

# --------------------------------------------------
# 2. Create embeddings for all documents
# --------------------------------------------------

print("🔄 Creating document embeddings...")

document_embeddings = model.encode(
    documents,
    convert_to_numpy=True
)

print("✅ Document embeddings created!")

# --------------------------------------------------
# 3. Calculate cosine similarity
# --------------------------------------------------

def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.
    """

    similarity = np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) *
        np.linalg.norm(vector_b)
    )

    return similarity


# --------------------------------------------------
# 4. Semantic search function
# --------------------------------------------------

def semantic_search(query, top_k=3):
    """
    Search documents based on semantic meaning.

    Args:
        query: User's search query
        top_k: Number of results to return

    Returns:
        Top matching documents with similarity scores
    """

    # Convert the user query into an embedding
    query_embedding = model.encode(
        query,
        convert_to_numpy=True
    )

    results = []

    # Compare query with every document
    for index, document_embedding in enumerate(document_embeddings):

        similarity = cosine_similarity(
            query_embedding,
            document_embedding
        )

        results.append({
            "document": documents[index],
            "similarity": similarity
        })

    # Sort results by similarity
    results.sort(
        key=lambda result: result["similarity"],
        reverse=True
    )

    # Return only top K results
    return results[:top_k]

# --------------------------------------------------
# 5. Display search results
# --------------------------------------------------

def display_results(query, results):

    print("\n" + "=" * 60)
    print(f"🔎 Query: {query}")
    print("=" * 60)

    for rank, result in enumerate(results, start=1):

        print(f"\n{rank}. {result['document']}")
        print(
            f"   Similarity: {result['similarity']:.4f}"
        )


# --------------------------------------------------
# 6. Main application
# --------------------------------------------------

def main():

    print("\n🚀 Day 17 — AI Semantic Search")
    print("Search by meaning, not just keywords.")
    print("Type 'exit' to quit.")

    while True:

        query = input("\nSearch: ").strip()

        # Exit condition
        if query.lower() == "exit":
            print("\n👋 Goodbye!")
            break

        # Prevent empty searches
        if not query:
            print("⚠️ Please enter a search query.")
            continue

        # Perform semantic search
        results = semantic_search(
            query,
            top_k=3
        )

        # Display results
        display_results(
            query,
            results
        )


# --------------------------------------------------
# 7. Run the application
# --------------------------------------------------

if __name__ == "__main__":
    main()