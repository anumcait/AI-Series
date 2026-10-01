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
