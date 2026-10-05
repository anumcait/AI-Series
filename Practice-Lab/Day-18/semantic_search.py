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
