import chromadb
from sentence_transformers import SentenceTransformer


DB_PATH = "chroma_db"
COLLECTION_NAME = "devops"


print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def load_documents():

    with open(
        "data/devops.txt",
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    return [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]


def build_database():

    documents = load_documents()

    if collection.count() > 0:

        print(
            f"Database already contains "
            f"{collection.count()} documents."
        )

        return

    print(
        f"Creating embeddings for "
        f"{len(documents)} documents..."
    )

    embeddings = model.encode(
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
        f"✅ Added {len(documents)} documents."
    )


if __name__ == "__main__":

    build_database()
